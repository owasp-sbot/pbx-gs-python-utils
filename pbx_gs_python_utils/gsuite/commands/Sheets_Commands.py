import base64
from time import time

from gs_budget.create_slides.Project_Slides import Project_Slides
from gs_budget.create_slides.Slides_for_Projects import Slides_for_Projects
from gsuite.GSlides import GSlides
from utils.Dev import Dev
from utils.Lambdas_Helpers import slack_message
from utils.Misc import Misc
from utils.aws.Lambdas import Lambdas


class Sheets_Commands:

    @staticmethod
    def _add_data(data, title):
        gsuite_secret_id = 'gsuite_gsbot_user'
        slides_for_projects = Slides_for_Projects(gsuite_secret_id)
        gsheets = slides_for_projects.gsheets()

        #slack_message(":point_right: Creating Google Sheet with GS Project details ...", [], channel,team_id)
        file_id    = '1ZIHavq-X_Ouo3ZIBn-zrwVTSU-PxWJ-Pt5zuNI66ahw'


        # # 'All Data - GS Projects'
        # sheet_name = 'All Data - {0}'.format(title)
        # sheet_id   = gsheets.sheets_properties_by_title(file_id).get(sheet_name).get('sheetId')
        #
        #
        # gsheets.clear_values(file_id, sheet_name)
        # sheet_data = gsheets.covert_raw_data_to_flat_objects(data)
        # gsheets.set_values(file_id, sheet_name,sheet_data)
        # gsheets.format_headers(file_id, sheet_id, len(sheet_data[0]))

        # 'GS Projects'
        sheet_name    = title
        sheet_id      = gsheets.sheets_properties_by_title(file_id).get(sheet_name).get('sheetId')
        projects_data = []
        for project in data:
            item = {
                        'Key'        : project.get('Key') ,
                        'Title'      : project.get('Summary'),
                        'Description': Misc.remove_html_tags(project.get('Description')),
                        'Issue Links': project.get('Issue Links'),
                        'Rating'     : project.get('Rating'    ),
                        'Priority'   : project.get('Priority'  )}
            projects_data.append(item)
        sheet_data = gsheets.covert_raw_data_to_flat_objects(projects_data)

        gsheets.clear_values(file_id, sheet_name)
        gsheets.set_values(file_id, sheet_name,sheet_data)
        gsheets.format_headers(file_id, sheet_id, len(sheet_data[0]))

    @staticmethod
    def gs_projects(team_id, channel, params):
        gsuite_secret_id = 'gsuite_gsbot_user'
        slides_for_projects = Slides_for_Projects(gsuite_secret_id)

        gs_projects = slides_for_projects.gs_projects()
        Sheets_Commands._add_data(gs_projects, 'GS Projects')

        gs_services = slides_for_projects.gs_services()
        Sheets_Commands._add_data(gs_services, 'GS Services')

        gsheets = slides_for_projects.gsheets()
        file_id = '1ZIHavq-X_Ouo3ZIBn-zrwVTSU-PxWJ-Pt5zuNI66ahw'
        web_link = gsheets.gdrive.file_weblink(file_id)
        text = ":point_right: File updated ... you can see it at: {0} \n\n use `gdocs pdf {1}` to generate the pdf".format(web_link, file_id)
        return text,[]


    @staticmethod
    def live_demo(team_id, channel, params):
        return 42, []