"""TO-DO: Write a description of what this XBlock is."""

import json
import pkg_resources
import six
from datetime import datetime, timedelta
from django.conf import settings

from azure.storage.blob import generate_blob_sas, BlobSasPermissions
from web_fragments.fragment import Fragment
from xblock.core import XBlock
from webob import Response
from xblock.fields import Scope, String


# Make '_' a no-op so we can scrape strings
def _(text):
    return text

class AzureVideoplayerXblock(XBlock):
    """
    TO-DO: document what your XBlock does.
    """

    # Fields are defined on the class.  You can access them in your code as
    # self.<fieldname>.
    azure_video_name = String(
        display_name=_("Azure Video Name"),
        help=_("Get Video Name to be displayed in XBlock."),
        default="",
        scope=Scope.settings,
    )
    azure_video_url = String(
        display_name=_("Azure Video URL"),
        help=_("Get Video URL to be displayed in XBlock."),
        default="",
        scope=Scope.settings,
    )
    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")

    # TO-DO: change this view to display your data your own way.
    def student_view(self, context=None):
        """
        The primary view of the AzureVideoplayerXblock, shown to students
        when viewing courses.
        """
        html_str = self.resource_string("static/html/azurevideoplayerxblock.html")
        frag = Fragment(six.text_type(html_str).format(block=self))

        frag.add_css(self.resource_string("static/css/azurevideoplayerxblock.css"))
        frag.add_javascript(self.resource_string("static/js/src/azurevideoplayerxblock.js"))
        frag.initialize_js('AzureVideoplayerXblock')
        return frag

    def studio_view(self, context):
        """
        Create a fragment used to display the edit view in the Studio.
        """
        html_str = self.resource_string("static/html/azurevideoplayerxblock_edit.html")
        frag = Fragment(six.text_type(html_str).format(azure_video_url=self.azure_video_url, azure_video_name=self.azure_video_name))
        js_str = self.resource_string("static/js/src/azurevideoplayerxblock_edit.js")
        frag.add_javascript(six.text_type(js_str))
        frag.initialize_js('AzureVideoplayerEditBlock')

        return frag
    
    @staticmethod
    def json_response(data):
        return Response(
            json.dumps(data), content_type="application/json", charset="utf8"
        )

    @XBlock.json_handler
    def studio_submit(self, data, suffix=''):
        """
        Called when submitting the form in Studio.
        """
        response = {'result': 'success', "errors": []}
        if not data.get('azure_video_name', None):
            response['errors'].append('Azure video name is required')
            return self.json_response(response)
        self.azure_video_name = data.get('azure_video_name')
        self.azure_video_url = self.get_azure_video_url(self.azure_video_name)

        return self.json_response(response)

    def get_azure_video_url(self, blob_name):
        sas_token = self.generate_sas_token(blob_name)
        video_url = f"https://{settings.AZURE_ACCOUNT_NAME}.blob.core.windows.net/{settings.AZURE_CONTAINER}/{blob_name}?{sas_token}"
        return video_url

    def generate_sas_token(self, blob_name):
        sas_token = generate_blob_sas(
            account_name=settings.AZURE_ACCOUNT_NAME,
            container_name=settings.AZURE_CONTAINER,
            blob_name=blob_name,
            account_key=settings.AZURE_ACCOUNT_KEY,
            permission=BlobSasPermissions(read=True),
            expiry=datetime.utcnow() + timedelta(hours=1)  # Set expiration time
        )
        return sas_token


    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
            ("AzureVideoplayerXblock",
             """<AzureVideoplayerXblock/>
             """)
        ]
