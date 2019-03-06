from unittest import TestCase

from syncer import sync

from browser.sites.Site_ELK import Site_ELK
from utils.Dev import Dev


class Test_Site_ELK(TestCase):
    def setUp(self):
        self.elk = Site_ELK()

    @sync
    async def test_browser(self):
        browser = self.elk.browser()
        url = await browser.url()
        assert '/login?next=/' in url

    @sync
    async def test_connect(self):
        result = await self.elk.connect()
        result.get('logged-out') is True

    @sync
    async def test_login(self):
        await self.elk.login()
        file = '/var/folders/m9/9n4rz4016s72thj0n_yq0nch0000gp/T/tmph8ltb_xk.png'
        png_file = await self.elk.browser().screenshot(file_screenshot=file)
        Dev.pprint(png_file)

    @sync
    async def test_dashboards(self):
        await self.elk.dashboards()
        links = await self.elk.browser().js_eval("$('.euiBasicTable a').length")
        Dev.pprint(links)

    def test_screenshot(self):
        result = self.elk.screenshot()
        Dev.print(result)

    def test_sync_connect_and_login(self):
        result = self.elk.sync__connect_and_login()

        result = self.elk.browser().sync__screenshot(file_screenshot='/tmp/lambda_png_file.png')
        Dev.print(result)

    def test_sync__dashboard(self):
        #id = '9591ebd0-e65f-11e8-abb1-378e282672cc'
        goto_id = '549e8579f763bc82ed6cd69cf4c62954'
        result = self.elk.sync__dashboard(goto_id)

        result = self.elk.browser().sync__screenshot(file_screenshot='/tmp/lambda_png_file.png')
        Dev.print(result)

    def test_sync__dashboard_project(self):
        #id = '9591ebd0-e65f-11e8-abb1-378e282672cc'
        key = 'GSSP-126'
        result = self.elk.sync__dashboard_project(key)

        result = self.elk.browser().sync__screenshot(file_screenshot='/tmp/lambda_png_file.png')
        Dev.print(result)

