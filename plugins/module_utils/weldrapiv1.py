#
# (c) 2022, Adam Miller (admiller@redhat.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt) # noqa: E501
import json
import os
import shutil

import ansible.module_utils.six.moves.urllib.error as urllib_error
from ansible.module_utils._text import to_bytes
from ansible.module_utils._text import to_native
from ansible.module_utils.six.moves.urllib.parse import quote


class WeldrV1:
    """
    WeldrV1

    Base wrapper around the Weldr local socket V1 API
    """

    def __init__(self, weldr):
        """
        initializer

        :module:          AnsibleModule, instance of AnsibleModule
        :unix_socket:     string, local UNIX Socket that Weldr service is listening on # noqa: E501
        """
        self.weldr = weldr

    #######################################################################
    # Some functions have not been implemented yet and will be as needed
    #######################################################################

    # Status
    def get_status(self):
        """
        # api.router.GET("/api/status", api.statusHandler)
        """
        raise NotImplementedError

    # Projects source
    def get_projects_source_list(self):
        """
        get a list of sources back from Weldr

        :return:        dict
        """
        results = json.load(
            self.weldr.request.open(
                "GET", "http://localhost/api/v1/projects/source/list"
            )  # noqa: E501
        )
        return results

    def get_projects_source_info(self, repo_name):
        """
        get detailed information about a particular source

        :repo_name:     str, a string of a repository name
        :return:        dict
        """
        results = json.load(
            self.weldr.request.open(
                "GET",
                "http://localhost/api/v1/projects/source/info/%s" % quote(repo_name),  # noqa: E501
            )
        )
        return results

    def get_projects_source_info_sources(self, repo_name):
        """
        get_projects_source_info_sources

        :repo_name:     str, a source name
        :return:        dict
        """
        results = json.load(
            self.weldr.request.open(
                "GET",
                "http://localhost/api/v1/projects/source/info/%s" % quote(repo_name),  # noqa: E501
                headers={"Content-Type": "application/json"},
            )
        )
        return results

    def post_projects_source_new(self, source):
        """
        post_projects_source_new

        :source:     dict, a dictionary of a source
        :return:        dict
        """
        if type(source) != bytes:
            source = to_bytes(source)
        results = json.load(
            self.weldr.request.open(
                "POST",
                "http://localhost/api/v1/projects/source/new",
                data=source,
                headers={"Content-Type": "application/json"},
            )
        )
        return results

    def delete_projects_source(self, repo_name):
        """
        delete_projects_source

        :repo_name:     str, a source name
        :source:     dict, a dictionary of a source
        """
        results = json.load(
            self.weldr.request.open(
                "DELETE",
                "http://localhost/api/v1/projects/source/delete/%s"
                % quote(repo_name),  # noqa: E501
                headers={"Content-Type": "application/json"},
            )
        )
        return results

    # Projects depsolve
    def get_projects_depsolve(self):
        """
        # api.router.GET("/api/v:version/projects/depsolve", api.projectsDepsolveHandler)  # noqa: E501
        """
        raise NotImplementedError

    def get_projects_depsolve_projects(self, projects):
        """
        # api.router.GET("/api/v:version/projects/depsolve/*projects", api.projectsDepsolveHandler)  # noqa: E501
        """
        raise NotImplementedError

    # Modules/projects list
    def get_modules_list(self):
        """
        get a list of modules back from Weldr

        :return:        list, list of modules dicts
        """
        results = json.load(
            self.weldr.request.open("GET", "http://localhost/api/v1/modules/list")  # noqa: E501
        )  # noqa: E501
        return results

    def get_modules_list_modules(self, modules):
        """
        # api.router.GET("/api/v:version/modules/list/*modules", api.modulesListHandler)  # noqa: E501
        """
        raise NotImplementedError

    def get_projects_list(self):
        """
        # api.router.GET("/api/v:version/projects/list", api.projectsListHandler)  # noqa: E501
        """
        raise NotImplementedError

    def get_projects_lists(self):
        """
        # api.router.GET("/api/v:version/projects/list/", api.projectsListHandler)  # noqa: E501
        """
        raise NotImplementedError

    # Modules/projects info with dependencies
    # // these are the same, except that modules/info also includes dependencies  # noqa: E501
    def get_modules_info(self):
        """
        # api.router.GET("/api/v:version/modules/info", api.modulesInfoHandler)
        """
        raise NotImplementedError

    def get_modules_info_modules(self, modules):
        """
        # api.router.GET("/api/v:version/modules/info/*modules", api.modulesInfoHandler)  # noqa: E501
        """
        raise NotImplementedError

    def get_projects_info(self):
        """
        # api.router.GET("/api/v:version/projects/info", api.modulesInfoHandler)  # noqa: E501
        """
        raise NotImplementedError

    def get_projects_info_modules(self, modules):
        """
        # api.router.GET("/api/v:version/projects/info/*modules", api.modulesInfoHandler)  # noqa: E501
        """
        raise NotImplementedError

    # Blueprints
    def get_blueprints_list(self):
        """
        get a list of blueprints back from Weldr

        :return:    dict
        """
        results = json.load(
            self.weldr.request.open("GET", "http://localhost/api/v1/blueprints/list")  # noqa: E501
        )
        return results

    def get_blueprints_info(self, blueprint):
        """
        get a list of blueprints back from Weldr

        :return:    dict
        """
        results = json.load(
            self.weldr.request.open(
                "GET", "http://localhost/api/v1/blueprints/info/%s" % blueprint
            )  # noqa: E501
        )
        return results

    def get_blueprints_depsolve(self, blueprints):
        """
        # api.router.GET("/api/v:version/blueprints/depsolve/*blueprints", api.blueprintsDepsolveHandler)  # noqa: E501
        """
        raise NotImplementedError

    def get_blueprints_freeze(self, blueprints):
        """
        # api.router.GET("/api/v:version/blueprints/freeze/*blueprints", api.blueprintsFreezeHandler)  # noqa: E501
        """
        raise NotImplementedError

    def get_blueprints_diff(self, blueprint_from, blueprint_to):
        """
        # api.router.GET("/api/v:version/blueprints/diff/:blueprint/:from/:to", api.blueprintsDiffHandler)  # noqa: E501
        """
        raise NotImplementedError

    def get_blueprints_change_commit(self, blueprints, commit):
        """
        # api.router.GET("/api/v:version/blueprints/change/:blueprint/:commit", api.blueprintsChangeHandler)  # noqa: E501
        """
        raise NotImplementedError

    def get_blueprints_changes(self, blueprints):
        """
        # api.router.GET("/api/v:version/blueprints/changes/*blueprints", api.blueprintsChangesHandler)  # noqa: E501
        """
        raise NotImplementedError

    def post_blueprint_new(self, blueprint):
        """
        post_blueprint_new

        :blueprint:     dict, a dictionary of a blueprint
        """
        if type(blueprint) != bytes:
            blueprint = to_bytes(blueprint)
        results = json.load(
            self.weldr.request.open(
                "POST",
                "http://localhost/api/v1/blueprints/new",
                data=blueprint,
                headers={"Content-Type": "text/x-toml"},
            )
        )
        return results

    def post_blueprints_workspace(self, workspace):
        """
        # api.router.POST("/api/v:version/blueprints/workspace", api.blueprintsWorkspaceHandler)  # noqa: E501
        """
        raise NotImplementedError

    def post_blueprints_undo_commit(self, blueprint, commit):
        """
        # api.router.POST("/api/v:version/blueprints/undo/:blueprint/:commit", api.blueprintUndoHandler)  # noqa: E501
        """
        raise NotImplementedError

    def post_blueprints_tag(self, blueprint):
        """
        # api.router.POST("/api/v:version/blueprints/tag/:blueprint", api.blueprintsTagHandler)  # noqa: E501
        """
        raise NotImplementedError

    def delete_blueprints(self, blueprint):
        """
        # api.router.DELETE("/api/v:version/blueprints/delete/:blueprint", api.blueprintDeleteHandler)  # noqa: E501
        """
        raise NotImplementedError

    def delete_blueprints_workspace(self, blueprint):
        """
        # api.router.DELETE("/api/v:version/blueprints/workspace/:blueprint", api.blueprintDeleteWorkspaceHandler)  # noqa: E501
        """
        raise NotImplementedError

    # Composes
    def post_compose(self, compose_settings):
        """
        iniiate a compose

        :return:    dict
        """
        results = "FOOBAR"
        try:
            if type(compose_settings) != bytes:
                compose_settings = to_bytes(compose_settings)
            results = json.load(
                self.weldr.request.open(
                    "POST",
                    "http://localhost/api/v1/compose",
                    data=compose_settings,
                    headers={"Content-Type": "application/json"},
                )
            )
            return results
        except urllib_error.HTTPError as e:
            self.weldr.module.fail_json(
                msg="OSBUILD COMPOSER ERROR: %s" % to_native(e.reason)
            )  # noqa: E501

    def delete_compose(self, compose):
        """
        # api.router.DELETE("/api/v:version/compose/delete/:uuids", api.composeDeleteHandler)  # noqa: E501
        """
        raise NotImplementedError

    def get_compose_types(self):
        """
        get compose types currently supported by weldr instance

        :return:        dict
        """
        results = json.load(
            self.weldr.request.open("GET", "http://localhost/api/v1/compose/types")  # noqa: E501
        )
        return results

    def get_compose_queue(self):
        """
        query current compose queue

        :return:        dict
        """
        results = json.load(
            self.weldr.request.open("GET", "http://localhost/api/v1/compose/queue")  # noqa: E501
        )
        return results

    def get_compose_status(self, compose_uuids):
        """
        # api.router.GET("/api/v:version/compose/status/:uuids", api.composeStatusHandler) # noqa: E501
        query current status of existing compose

        :return:        dict
        """
        results = json.load(
            self.weldr.request.open(
                "GET", "http://localhost/api/v1/compose/status/%s" % compose_uuids  # noqa: E501
            )
        )
        return results

    def get_compose_info(self, compose_uuid):
        """
        # api.router.GET("/api/v:version/compose/info/:uuid", api.composeInfoHandler) # noqa: E501
        query info of existing compose

        :return:        dict
        """
        results = json.load(
            self.weldr.request.open(
                "GET", "http://localhost/api/v1/compose/info/%s" % compose_uuid
            )  # noqa: E501
        )
        return results

    def get_compose_finished(self):
        """
        # api.router.GET("/api/v:version/compose/finished", api.composeFinishedHandler)  # noqa: E501
        query info of completed composes

        :return:        dict
        """
        results = json.load(
            self.weldr.request.open("GET", "http://localhost/api/v1/compose/finished")  # noqa: E501
        )
        return results

    def get_compose_failed(self):
        """
        # api.router.GET("/api/v:version/compose/failed", api.composeFailedHandler)  # noqa: E501
        query list of failed composes

        :return:        dict
        """
        results = json.load(
            self.weldr.request.open("GET", "http://localhost/api/v1/compose/failed")  # noqa: E501
        )
        return results

    def get_compose_image(self, compose_uuid, dest):
        """
        # api.router.GET("/api/v:version/compose/image/:uuid", api.composeImageHandler)  # noqa: E501
        """
        tmpfile = self.weldr.fetch_file(
            self.weldr.module,
            "http://localhost/api/v1/compose/image/%s" % compose_uuid,
            method="GET",
            unix_socket=self.weldr.unix_socket,
        )
        shutil.copy(tmpfile, dest)
        with open(dest) as fd:
            os.fsync(fd)
        os.remove(tmpfile)
        return None

    def get_compose_metadata(self, compose_uuid):
        """
        # api.router.GET("/api/v:version/compose/metadata/:uuid", api.composeMetadataHandler)  # noqa: E501
        """
        raise NotImplementedError

    def get_compose_results(self, compose_uuid):
        """
        # api.router.GET("/api/v:version/compose/results/:uuid", api.composeResultsHandler)  # noqa: E501
        """
        raise NotImplementedError

    def get_compose_logs(self, compose_uuid):
        """
        # api.router.GET("/api/v:version/compose/logs/:uuid", api.composeLogsHandler)  # noqa: E501
        """
        raise NotImplementedError

    def get_compose_log(self, compose_uuid):
        """
        # api.router.GET("/api/v:version/compose/log/:uuid", api.composeLogHandler)  # noqa: E501
        """
        raise NotImplementedError

    def post_compose_uploads_schedule(self, compose_uuid):
        """
        # api.router.POST("/api/v:version/compose/uploads/schedule/:uuid", api.uploadsScheduleHandler)  # noqa: E501
        """
        raise NotImplementedError

    def compose_cancel(self, compose_uuid):
        """
        # api.router.DELETE("/api/v:version/compose/cancel/:uuid", api.composeCancelHandler)  # noqa: E501
        """
        raise NotImplementedError

    # Uploads
    def delete_compose_upload(self, compose_uuid):
        """
        # api.router.DELETE("/api/v:version/upload/delete/:uuid", api.uploadsDeleteHandler)  # noqa: E501
        """
        raise NotImplementedError

    def get_version_info(self, compose_uuid):
        """
        # api.router.GET("/api/v:version/upload/info/:uuid", api.uploadsInfoHandler)  # noqa: E501
        """
        raise NotImplementedError

    def get_version_upload_log(self, compose_uuid):
        """
        # api.router.GET("/api/v:version/upload/log/:uuid", api.uploadsLogHandler)  # noqa: E501
        """
        raise NotImplementedError

    def upload_reset(self, compose_uuid):
        """
        # api.router.POST("/api/v:version/upload/reset/:uuid", api.uploadsResetHandler)  # noqa: E501
        """
        raise NotImplementedError

    def upload_cancel(self, compose_uuid):
        """
        # api.router.DELETE("/api/v:version/upload/cancel/:uuid", api.uploadsCancelHandler)  # noqa: E501
        """
        raise NotImplementedError

    # Upload providers
    def get_upload_providers(self):
        """
        # api.router.GET("/api/v:version/upload/providers", api.providersHandler)  # noqa: E501
        """
        raise NotImplementedError

    def save_providers(self):
        """
        # api.router.POST("/api/v:version/upload/providers/save", api.providersSaveHandler)  # noqa: E501
        """
        raise NotImplementedError

    def delete_provider(self, provider, profile):
        """
        # api.router.DELETE("/api/v:version/upload/providers/delete/:provider/:profile", api.providersDeleteHandler)  # noqa: E501
        """
        raise NotImplementedError

    # Distros
    def get_distros_list(self):
        """
        # api.router.GET("/api/v:version/distros/list", api.distrosListHandler)
        """
        raise NotImplementedError
