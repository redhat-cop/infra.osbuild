# -*- coding: utf-8 -*-
#
# (c) 2022, Adam Miller (admiller@redhat.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from ansible.module_utils.urls import Request
from ansible.module_utils._text import to_bytes, to_native, to_text

class WeldrV1(object):
    """
    WeldrV1

    Base wrapper around the Weldr local socket V1 API
    """

    def __init__(self, module, unix_socket):
        """
        initializer

        :module:          AnsibleModule, instance of AnsibleModule
        :unix_socket:     string, local UNIX Socket that Weldr service is listening on
        """
        self.module = module
        self.unix_socket = unix_socket
        self.request = Request(unix_socket=self.unix_socket)

    def get_projects_source_list(self):
        """
        get a list of sources back from Weldr

        :return:        list, list of sources
        """
        req_read = self.request.open('GET', 'http://localhost/api/v1/projects/source/list').read()
        return req_read['sources']

    def get_projects_source_info(self, source):
        """
        get detailed information about a particular source

        :return:        dict, dict containing source information
        """
        req_read = self.request.open('GET', 'http://localhost/api/v1/projects/source/info/%s' % source).read()
        return req_read


    def get_projects_source_info_sources(self, sources):
        """
        # api.router.GET("/api/v:version/projects/source/info/:sources", api.sourceInfoHandler)
        """
        raise NotImplementedError

    def post_projects_source_new(self, source):
        """
        # api.router.POST("/api/v:version/projects/source/new", api.sourceNewHandler)
        """
        raise NotImplementedError

    def delete_projects_source(self, source):
        """
        # api.router.DELETE("/api/v:version/projects/source/delete/*source", api.sourceDeleteHandler)
        """
        raise NotImplementedError

    def get_projects_depsolve(self):
        """
        # api.router.GET("/api/v:version/projects/depsolve", api.projectsDepsolveHandler)
        """
        raise NotImplementedError

    def get_projects_depsolve_projects(self, projects):
        """
        # api.router.GET("/api/v:version/projects/depsolve/*projects", api.projectsDepsolveHandler)
        """
        raise NotImplementedError

    def get_modules_list(self):
        """
        get a list of modules back from Weldr

        :return:        list, list of modules dicts
        """
        req_read = self.request.open('GET', 'http://localhost/api/v1/modules/list').read()
        return req_read['modules']

    def get_modules_list_modules(self, modules):
        """
        # api.router.GET("/api/v:version/modules/list/*modules", api.modulesListHandler)
        """
        raise NotImplementedError

    def get_projects_list(self):
        """
        # api.router.GET("/api/v:version/projects/list", api.projectsListHandler)
        # api.router.GET("/api/v:version/projects/list/", api.projectsListHandler)
        """
        raise NotImplementedError

    def get_modules_info(self):
        """
        # // these are the same, except that modules/info also includes dependencies
        # api.router.GET("/api/v:version/modules/info", api.modulesInfoHandler)
        # api.router.GET("/api/v:version/modules/info/*modules", api.modulesInfoHandler)
        # api.router.GET("/api/v:version/projects/info", api.modulesInfoHandler)
        # api.router.GET("/api/v:version/projects/info/*modules", api.modulesInfoHandler)
        """

    def get_blueprints_list(self):
        """
        # api.router.GET("/api/v:version/blueprints/list", api.blueprintsListHandler)
        """
        raise NotImplementedError

    def get_blueprints_info(self, blueprints):
        """
        # api.router.GET("/api/v:version/blueprints/info/*blueprints", api.blueprintsInfoHandler)
        """
        raise NotImplementedError

    def get_blueprints_depsolve(self, blueprints):
        """
        # api.router.GET("/api/v:version/blueprints/depsolve/*blueprints", api.blueprintsDepsolveHandler)
        """
        raise NotImplementedError

    def get_blueprints_freeze(self, blueprints):
        """
        # api.router.GET("/api/v:version/blueprints/freeze/*blueprints", api.blueprintsFreezeHandler)
        """
        raise NotImplementedError

    def get_blueprints_diff(self, blueprint_from, blueprint_to):
        """
        # api.router.GET("/api/v:version/blueprints/diff/:blueprint/:from/:to", api.blueprintsDiffHandler)
        """
        raise NotImplementedError

    def get_blueprints_changes(self, blueprints):
        """
        # api.router.GET("/api/v:version/blueprints/changes/*blueprints", api.blueprintsChangesHandler)
        """
        raise NotImplementedError

    def post_blueprint_new(self, blueprint):
        """
        # api.router.POST("/api/v:version/blueprints/new", api.blueprintsNewHandler)
        """
        raise NotImplementedError

    def post_blueprints_workspace(self, workspace):
        """
        # api.router.POST("/api/v:version/blueprints/workspace", api.blueprintsWorkspaceHandler)
        """
        raise NotImplementedError

    def post_blueprints_undo_commit(self, blueprint, commit):
        """
        # api.router.POST("/api/v:version/blueprints/undo/:blueprint/:commit", api.blueprintUndoHandler)
        """
        raise NotImplementedError

    def post_blueprints_tag(self, blueprint):
        """
        # api.router.POST("/api/v:version/blueprints/tag/:blueprint", api.blueprintsTagHandler)
        """
        raise NotImplementedError

    def delete_blueprints(self, blueprint):
        """
        # api.router.DELETE("/api/v:version/blueprints/delete/:blueprint", api.blueprintDeleteHandler)
        # api.router.DELETE("/api/v:version/blueprints/workspace/:blueprint", api.blueprintDeleteWorkspaceHandler# # )
        """
        raise NotImplementedError

    def post_compose(self, compose):
        """
        # api.router.POST("/api/v:version/compose", api.composeHandler)
        """
        raise NotImplementedError

    def delete_compose(self, compose):
        """
        # api.router.DELETE("/api/v:version/compose/delete/:uuids", api.composeDeleteHandler)
        """
        raise NotImplementedError

    def get_compose_types(self, compose):
        """
        # api.router.GET("/api/v:version/compose/types", api.composeTypesHandler)
        """
        raise NotImplementedError

    def get_compose_queue(self, compose):
        """
        # api.router.GET("/api/v:version/compose/queue", api.composeQueueHandler)
        """
        raise NotImplementedError

    def get_compuse_status(self, compose_uuids):
        """
        # api.router.GET("/api/v:version/compose/status/:uuids", api.composeStatusHandler)
        raise NotImplementedError
        """

    def get_compose_info(self, compose_uuid):
        """
        # api.router.GET("/api/v:version/compose/info/:uuid", api.composeInfoHandler)
        """
        raise NotImplementedError

    def get_compose_finished(self):
        """
        # api.router.GET("/api/v:version/compose/finished", api.composeFinishedHandler)
        """
        raise NotImplementedError

    def get_compose_failed(self):
        """
        # api.router.GET("/api/v:version/compose/failed", api.composeFailedHandler)
        """
        raise NotImplementedError

    def get_compose_image(self, compuse_uuid):
        """
        # api.router.GET("/api/v:version/compose/image/:uuid", api.composeImageHandler)
        """
        raise NotImplementedError

    def get_compose_metadata(self, compose_uuid):
        """
        # api.router.GET("/api/v:version/compose/metadata/:uuid", api.composeMetadataHandler)
        """
        raise NotImplementedError

    def get_compose_results(self, compose_uuid):
        """
        # api.router.GET("/api/v:version/compose/results/:uuid", api.composeResultsHandler)
        """
        raise NotImplementedError

    def get_compose_logs(self, compose_uuid):
        """
        # api.router.GET("/api/v:version/compose/logs/:uuid", api.composeLogsHandler)
        # api.router.GET("/api/v:version/compose/log/:uuid", api.composeLogHandler)
        """
        raise NotImplementedError

    def post_compose_updloads_schedule(self, compose_uuid):
        """
        # api.router.POST("/api/v:version/compose/uploads/schedule/:uuid", api.uploadsScheduleHandler)
        """
        raise NotImplementedError

    def compose_cancel(self, compose_uuid):
        """
        # api.router.DELETE("/api/v:version/compose/cancel/:uuid", api.composeCancelHandler)
        """
        raise NotImplementedError

    def delete_compose_upload(self, compose_uuid):
        """
        # api.router.DELETE("/api/v:version/upload/delete/:uuid", api.uploadsDeleteHandler)
        """
        raise NotImplementedError

    def get_version_info(self, compose_uuid):
        """
        # api.router.GET("/api/v:version/upload/info/:uuid", api.uploadsInfoHandler)
        """
        raise NotImplementedError

    def get_version_upload_log(self, compose_uuid):
        """
        # api.router.GET("/api/v:version/upload/log/:uuid", api.uploadsLogHandler)
        """
        raise NotImplementedError

    def upload_reset(self, compose_uuid):
        """
        # api.router.POST("/api/v:version/upload/reset/:uuid", api.uploadsResetHandler)
        """
        raise NotImplementedError

    def upload_cancel(self, compose_uuid):
        """
        # api.router.DELETE("/api/v:version/upload/cancel/:uuid", api.uploadsCancelHandler)
        """
        raise NotImplementedError

    def get_upload_providers(self):
        """
        # api.router.GET("/api/v:version/upload/providers", api.providersHandler)
        """
        raise NotImplementedError

    def save_providers(self):
        """
        # api.router.POST("/api/v:version/upload/providers/save", api.providersSaveHandler)
        """
        raise NotImplementedError

    def delete_provider(self, provider, profile):
        """
        # api.router.DELETE("/api/v:version/upload/providers/delete/:provider/:profile", api.providersDeleteHandler)
        """
        raise NotImplementedError

    def get_distros_list(self):
        """
        # api.router.GET("/api/v:version/distros/list", api.distrosListHandler)
        """
        raise NotImplementedError
