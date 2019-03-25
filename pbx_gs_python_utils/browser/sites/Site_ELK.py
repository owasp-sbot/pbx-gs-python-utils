import json
from time import sleep

from syncer import sync

from browser.API_Browser import API_Browser
from browser.Browser_Lamdba_Helper import Browser_Lamdba_Helper
from utils.Dev import Dev
from utils.Lambdas_Helpers import slack_message
from utils.aws.secrets import Secrets


class Site_ELK:
    def __init__(self,api_browser=None,team_id=None, channel=None):
        self._browser       = None
        self.headless       = True
        self.auto_close     = True
        self.username       = None
        self.password       = None
        self.server_url     = None
        self.aws_secrets_id = 'gsbot-elk-login-details'
        self.team_id        = team_id
        self.channel        = channel
        if api_browser:
            self._browser   = api_browser
        else:
            self._browser   = None
        self.setup()

    def setup(self):
        login_details   = json.loads(Secrets(self.aws_secrets_id).value())
        self.username   = login_details.get('username')
        self.password   = login_details.get('password')
        self.server_url = login_details.get('server_url')
        if self._browser is None:
            self._browser = API_Browser(headless=self.headless, auto_close=self.auto_close).sync__setup_browser()
        return self._browser

    def browser(self):
        return self._browser

    async def connect(self):
        await self.open('/aaaa')
        return await self.is_user_logged_in()

    async def is_user_logged_in(self):
        html = await self.browser().html_raw()
        logged_out = '/login/bootstrap.js' in html
        return {'logged-out': logged_out}

    def log_status(self,message):
        if self.team_id and self.channel:
            slack_message(message, [], self.channel, self.team_id)

    async def login(self):
        browser = self.browser()
        url = await browser.url()
        if '/login?next=/' in url:
            username = self.username
            password = self.password
            self.log_status('Logging in to ES using user: `{0}`'.format(username))
            page = await browser.page()
            await page.waitForSelector('input[name=username]', {'timeout': 10000})      # specific to version x of Kibana
            await page.type('input[name=username]', username)
            await page.type('input[name=password]', password)
            #await page.click('button');                                                # doesn't work in Lambda
            await browser.js_execute("document.querySelector('button').click()")
            await page.waitForNavigation()                                              # this will hang if login fails
            self.log_status('Login complete'.format(username))

    async def logout(self):
        await self.open('/logout', 'networkidle0')

    async def open(self, path,wait_until=None):
        url = self.server_url + path
        Dev.print(url)
        await self.browser().open(url,wait_until=wait_until)

    def screenshot(self):
        return self.browser().sync__screenshot()

    @sync
    async def sync__connect_and_login(self):
        await self.connect()
        #await self.logout()
        await self.login()
        #await self.dashboards()
        return await self.is_user_logged_in()

    @sync
    async def sync__dashboards(self):
        await self.open('/app/kibana#/dashboards', 'networkidle0')
        page = await self.browser().page()
        await page.waitForSelector('.euiTitle')

    @sync
    async def sync__dashboard(self,goto_id):
        await self.browser().page_size(2000,1000)
        #await self.open('/app/kibana#/dashboard/{0}'.format(dashboard_id), 'networkidle0')
        await self.open('/goto/{0}'.format(goto_id), 'networkidle0')

        page = await self.browser().page()
        await page.waitForSelector('.kuiLocalSearch')

    @sync
    async def sync__dashboard_project(self, key):
        await self.browser().page_size(1500, 1000)
        #key = 'GSSP-171'
        #key = 'GSSP-126'
        self.log_status('Opening dashboard for project: {0}'.format(key))
        url = "/app/kibana#/dashboard/12d60b50-3a46-11e9-9a33-8728e06b70ec?_g=(refreshInterval:(pause:!f,value:5000),time:(from:now-15m,mode:quick,to:now))&_a=(description:'',filters:!(('$state':(store:appState),meta:(alias:!n,disabled:!f,index:e00d6380-23d9-11e9-b0a8-31c201c03efd,key:project_id,negate:!f,params:(query:{0},type:phrase),type:phrase,value:{0}),query:(match:(project_id:(query:{0},type:phrase))))),fullScreenMode:!f,options:(darkTheme:!f,hidePanelTitles:!f,useMargins:!t),panels:!((embeddableConfig:(),gridData:(h:12,i:'1',w:16,x:0,y:0),id:c2cb0b90-3a42-11e9-9a33-8728e06b70ec,panelIndex:'1',type:visualization,version:'6.6.1'),(embeddableConfig:(),gridData:(h:12,i:'2',w:12,x:16,y:0),id:'89544f80-3a41-11e9-9a33-8728e06b70ec',panelIndex:'2',type:visualization,version:'6.6.1'),(embeddableConfig:(),gridData:(h:15,i:'3',w:28,x:0,y:12),id:fdb7ce30-3a35-11e9-9a33-8728e06b70ec,panelIndex:'3',type:visualization,version:'6.6.1')),query:(language:kuery,query:''),timeRestore:!f,title:'GS%20Budget%20-%20Projects%20Simple',viewMode:view)".format(key)
        await self.open(url)
        #await self.open('/goto/{0}'.format(goto_id), 'networkidle0')
        page = await self.browser().page()
        await page.waitForSelector('.visWrapper')#''.kbnAggTable__group')



    @sync
    async def sync__is_logged_in(self):
        return await self.is_user_logged_in()

class ELK_Commands:

    @staticmethod
    def is_logged_in(team_id=None, channel=None, params=None):
        elk = params.pop()
        return elk.sync__is_logged_in()

    @staticmethod
    def dashboard(team_id=None, channel=None, params=None):
        elk            = params.pop()
        browser_helper = params.pop()
        dashboard_id   = params.pop()
        elk.sync__dashboard(dashboard_id)
        png_data = browser_helper.get_screenshot_png()
        return browser_helper.send_png_data_to_slack(team_id, channel, None, png_data)

    @staticmethod
    def dashboard_project(team_id=None, channel=None, params=None):
        elk            = params.pop()
        browser_helper = params.pop()
        key            = params.pop()
        clip           = {'x': 190, 'y': 130, 'width': 755, 'height': 725 }

        elk.sync__dashboard_project(key)
        #dashboard_id = '549e8579f763bc82ed6cd69cf4c62954'
        #elk.sync__dashboard(dashboard_id)

        png_data = browser_helper.get_screenshot_png(clip=clip,full_page=False)

        return browser_helper.send_png_data_to_slack(team_id, channel, None, png_data)

    @staticmethod
    def dashboards(team_id=None, channel=None, params=None):
        elk = params.pop()
        browser_helper = params.pop()

        elk.sync__dashboards()

        png_data = browser_helper.get_screenshot_png()
        return browser_helper.send_png_data_to_slack(team_id, channel, None, png_data)

    @staticmethod
    def url(team_id=None, channel=None, params=None):
        elk            = params.pop()
        browser_helper = params.pop()
        return browser_helper.api_browser.sync__url()


    @staticmethod
    def screenshot(team_id=None, channel=None, params=None):
        elk = params.pop()
        browser_helper = params.pop()
        png_data = browser_helper.get_screenshot_png()
        return browser_helper.send_png_data_to_slack(team_id, channel, None, png_data)