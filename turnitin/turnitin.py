"""TO-DO: Write a description of what this XBlock is."""

from datetime import datetime
import pkg_resources
from django.utils import translation
from xblock.core import XBlock
from xblock.fields import Integer, Scope
from xblock.fragment import Fragment
from xblockutils.resources import ResourceLoader

from .turnitin_api.handlers import (get_eula_page,
                                    post_accept_eula_version,
                                    post_create_submission,
                                    )

@XBlock.needs("user")
@XBlock.needs("user_state")
class TurnitinXBlock(XBlock):
    """
    TO-DO: document what your XBlock does.
    """

    # Fields are defined on the class.  You can access them in your code as
    # self.<fieldname>.

    # TO-DO: delete count, and define your own fields.
    count = Integer(
        default=0, scope=Scope.user_state,
        help="A simple counter, to show something happening",
    )

    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")
    
    def studio_view(self, context=None):
        """
        The primary view of the TurnitinXBlock, shown to students
        when viewing courses.
        """
        if context:
            pass  # TO-DO: do something based on the context.
        html = self.resource_string("static/html/cms.html")
        frag = Fragment(html.format(self=self))
        frag.add_css(self.resource_string("static/css/turnitin.css"))

        # Add i18n js
        statici18n_js_url = self._get_statici18n_js_url()
        if statici18n_js_url:
            frag.add_javascript_url(self.runtime.local_resource_url(self, statici18n_js_url))

        frag.add_javascript(self.resource_string("static/js/src/turnitin.js"))
        frag.initialize_js('TurnitinXBlock')
        return frag

    # TO-DO: change this view to display your data your own way.
    def student_view(self, context=None):
        """
        The primary view of the TurnitinXBlock, shown to students
        when viewing courses.
        """
        if context:
            pass  # TO-DO: do something based on the context.
        html = self.resource_string("static/html/turnitin.html")
        frag = Fragment(html.format(self=self))
        frag.add_css(self.resource_string("static/css/turnitin.css"))

        # Add i18n js
        statici18n_js_url = self._get_statici18n_js_url()
        if statici18n_js_url:
            frag.add_javascript_url(self.runtime.local_resource_url(self, statici18n_js_url))

        frag.add_javascript(self.resource_string("static/js/src/turnitin.js"))
        frag.initialize_js('TurnitinXBlock')
        return frag

    # TO-DO: change this handler to perform your own actions.  You may need more
    # than one handler, or you may not need any handlers at all.
    @XBlock.json_handler
    def increment_count(self, data, suffix=''):
        """
        An example handler, which increments the data.
        """
        if suffix:
            pass  # TO-DO: Use the suffix when storing data.
        # Just to show data coming in...
        assert data['hello'] == 'world'

        self.count += 1
        return {"count": self.count}
    





    @XBlock.json_handler
    def get_eula_agreement(self, data, suffix=''):
        return get_eula_page()
    

    @XBlock.json_handler
    def accept_eula_agreement(self, data, suffix=''):
        user_service = self.runtime.service(self, 'user')
        user_id = user_service.get_current_user().opt_attrs['edx-platform.user_id']
        date_now = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
        payload = {
            "user_id": str(user_id), "accepted_timestamp": date_now, "language": "en-US"
        }
        return post_accept_eula_version(payload)

    def create_turnitin_submission_object(self):
        current_user = self.runtime.service(self, 'user').get_current_user()
        user_email = current_user.emails[0]
        user_name = current_user.full_name.split()
        user_id = current_user.opt_attrs['edx-platform.user_id']
        anonymous_user_id = current_user.opt_attrs['anonymous_user_id']
        date_now = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

        payload={
        "owner": anonymous_user_id,
        "title": self.location,
        "submitter": user_id,
        "owner_default_permission_set": "LEARNER",
        "submitter_default_permission_set": "INSTRUCTOR",
        "extract_text_only": False,
        "metadata": {
          "owners": [
            {
              "id": anonymous_user_id,
              "given_name": user_name[0] if user_name else "",
              "family_name": ' '.join(user_name[1:]) if len(user_name) > 1 else "",
              "email": user_email
            }
            ],
          "submitter": {
            "id": user_id,
            "given_name": user_name[0] if user_name else "",
            "family_name": ' '.join(user_name[1:]) if len(user_name) > 1 else "",
            "email": user_email
            },

          "original_submitted_time": date_now,
            }
        }
        return post_create_submission(payload)
        













    # TO-DO: change this to create the scenarios you'd like to see in the
    # workbench while developing your XBlock.
    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
            ("TurnitinXBlock",
             """<turnitin/>
             """),
            ("Multiple TurnitinXBlock",
             """<vertical_demo>
                <turnitin/>
                <turnitin/>
                <turnitin/>
                </vertical_demo>
             """),
        ]

    @staticmethod
    def _get_statici18n_js_url():
        """
        Returns the Javascript translation file for the currently selected language, if any.
        Defaults to English if available.
        """
        locale_code = translation.get_language()
        if locale_code is None:
            return None
        text_js = 'public/js/translations/{locale_code}/text.js'
        lang_code = locale_code.split('-')[0]
        for code in (locale_code, lang_code, 'en'):
            loader = ResourceLoader(__name__)
            if pkg_resources.resource_exists(
                    loader.module_name, text_js.format(locale_code=code)):
                return text_js.format(locale_code=code)
        return None

    @staticmethod
    def get_dummy():
        """
        Dummy method to generate initial i18n
        """
        return translation.gettext_noop('Dummy')
