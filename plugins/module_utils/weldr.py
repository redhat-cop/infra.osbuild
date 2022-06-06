# -*- coding: utf-8 -*-
#
# (c) 2022, Adam Miller (admiller@redhat.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from ansible.module_utils.urls import Request

class Weldr(object):
    """
    Weldr

    This is the base class for interacting with the weldr API over a local UNIX socket
    """

    def __init__(self, module, unix_socket="/run/weldr/api.socket"):
        """
        initializer 

        :module:          AnsibleModule, instance of AnsibleModule
        :unix_socket:     string, local UNIX Socket that Weldr service is listening on
        """

        self.module = module
        self.unix_socket = unix_socket
        self.request = Request(unix_socket=self.unix_socket)

        status = self.request.open('GET', 'http://localhost/api/status').read()
        if status['api'] == "1":
            weldr = WeldrV1(module, unix_socket)
        else:
            module.fail_json(msg='Unsupported Weldr API found. Expected "1", got "%s"' % status['api'])


    def check_status(self):
        """
        check_status of local weldr

        """




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

        # api.router.GET("/api/v:version/projects/list", api.projectsListHandler)
        raise NotImplementedError
        # api.router.GET("/api/v:version/projects/list/", api.projectsListHandler)
        raise NotImplementedError

        # // these are the same, except that modules/info also includes dependencies
        # api.router.GET("/api/v:version/modules/info", api.modulesInfoHandler)
        raise NotImplementedError
        # api.router.GET("/api/v:version/modules/info/*modules", api.modulesInfoHandler)
        raise NotImplementedError
        # api.router.GET("/api/v:version/projects/info", api.modulesInfoHandler)
        raise NotImplementedError
        # api.router.GET("/api/v:version/projects/info/*modules", api.modulesInfoHandler)
        raise NotImplementedError

        # api.router.GET("/api/v:version/blueprints/list", api.blueprintsListHandler)
        raise NotImplementedError
        # api.router.GET("/api/v:version/blueprints/info/*blueprints", api.blueprintsInfoHandler)
        raise NotImplementedError
        # api.router.GET("/api/v:version/blueprints/depsolve/*blueprints", api.blueprintsDepsolveHandler)
        raise NotImplementedError
        # api.router.GET("/api/v:version/blueprints/freeze/*blueprints", api.blueprintsFreezeHandler)
        raise NotImplementedError
        # api.router.GET("/api/v:version/blueprints/diff/:blueprint/:from/:to", api.blueprintsDiffHandler)
        raise NotImplementedError
        # api.router.GET("/api/v:version/blueprints/changes/*blueprints", api.blueprintsChangesHandler)
        raise NotImplementedError
        # api.router.POST("/api/v:version/blueprints/new", api.blueprintsNewHandler)
        raise NotImplementedError
        # api.router.POST("/api/v:version/blueprints/workspace", api.blueprintsWorkspaceHandler)
        raise NotImplementedError
        # api.router.POST("/api/v:version/blueprints/undo/:blueprint/:commit", api.blueprintUndoHandler)
        raise NotImplementedError
        # api.router.POST("/api/v:version/blueprints/tag/:blueprint", api.blueprintsTagHandler)
        raise NotImplementedError
        # api.router.DELETE("/api/v:version/blueprints/delete/:blueprint", api.blueprintDeleteHandler)
        raise NotImplementedError
        # api.router.DELETE("/api/v:version/blueprints/workspace/:blueprint", api.blueprintDeleteWorkspaceHandler# # )
        raise NotImplementedError

        # api.router.POST("/api/v:version/compose", api.composeHandler)
        raise NotImplementedError
        # api.router.DELETE("/api/v:version/compose/delete/:uuids", api.composeDeleteHandler)
        raise NotImplementedError
        # api.router.GET("/api/v:version/compose/types", api.composeTypesHandler)
        raise NotImplementedError
        # api.router.GET("/api/v:version/compose/queue", api.composeQueueHandler)
        raise NotImplementedError
        # api.router.GET("/api/v:version/compose/status/:uuids", api.composeStatusHandler)
        raise NotImplementedError
        # api.router.GET("/api/v:version/compose/info/:uuid", api.composeInfoHandler)
        raise NotImplementedError
        # api.router.GET("/api/v:version/compose/finished", api.composeFinishedHandler)
        raise NotImplementedError
        # api.router.GET("/api/v:version/compose/failed", api.composeFailedHandler)
        raise NotImplementedError
        # api.router.GET("/api/v:version/compose/image/:uuid", api.composeImageHandler)
        raise NotImplementedError
        # api.router.GET("/api/v:version/compose/metadata/:uuid", api.composeMetadataHandler)
        raise NotImplementedError
        # api.router.GET("/api/v:version/compose/results/:uuid", api.composeResultsHandler)
        raise NotImplementedError
        # api.router.GET("/api/v:version/compose/logs/:uuid", api.composeLogsHandler)
        raise NotImplementedError
        # api.router.GET("/api/v:version/compose/log/:uuid", api.composeLogHandler)
        raise NotImplementedError
        # api.router.POST("/api/v:version/compose/uploads/schedule/:uuid", api.uploadsScheduleHandler)
        raise NotImplementedError
        # api.router.DELETE("/api/v:version/compose/cancel/:uuid", api.composeCancelHandler)
        raise NotImplementedError

        # api.router.DELETE("/api/v:version/upload/delete/:uuid", api.uploadsDeleteHandler)
        raise NotImplementedError
        # api.router.GET("/api/v:version/upload/info/:uuid", api.uploadsInfoHandler)
        raise NotImplementedError
        # api.router.GET("/api/v:version/upload/log/:uuid", api.uploadsLogHandler)
        raise NotImplementedError
        # api.router.POST("/api/v:version/upload/reset/:uuid", api.uploadsResetHandler)
        raise NotImplementedError
        # api.router.DELETE("/api/v:version/upload/cancel/:uuid", api.uploadsCancelHandler)
        raise NotImplementedError

        # api.router.GET("/api/v:version/upload/providers", api.providersHandler)
        raise NotImplementedError
        # api.router.POST("/api/v:version/upload/providers/save", api.providersSaveHandler)
        raise NotImplementedError
        # api.router.DELETE("/api/v:version/upload/providers/delete/:provider/:profile", api.providersDeleteHandler)
        raise NotImplementedError

        # api.router.GET("/api/v:version/distros/list", api.distrosListHandler)
        raise NotImplementedError
