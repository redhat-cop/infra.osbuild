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
        """

        self.module = module
        self.unix_socket = unix_socket
        self.request = Request(unix_socket=self.unix_socket)

    def check_status(self):
        """
        check_status of local weldr

        """

        get_req = self.request.open('GET', 'http://localhost/api/status').read()
        import q; q.q(get_req)


# api.router.GET("/api/status", api.statusHandler)
# api.router.GET("/api/v:version/projects/source/list", api.sourceListHandler)
# api.router.GET("/api/v:version/projects/source/info/", api.sourceEmptyInfoHandler)
# api.router.GET("/api/v:version/projects/source/info/:sources", api.sourceInfoHandler)
# api.router.POST("/api/v:version/projects/source/new", api.sourceNewHandler)
# api.router.DELETE("/api/v:version/projects/source/delete/*source", api.sourceDeleteHandler)

# api.router.GET("/api/v:version/projects/depsolve", api.projectsDepsolveHandler)
# api.router.GET("/api/v:version/projects/depsolve/*projects", api.projectsDepsolveHandler)

# api.router.GET("/api/v:version/modules/list", api.modulesListHandler)
# api.router.GET("/api/v:version/modules/list/*modules", api.modulesListHandler)
# api.router.GET("/api/v:version/projects/list", api.projectsListHandler)
# api.router.GET("/api/v:version/projects/list/", api.projectsListHandler)

# // these are the same, except that modules/info also includes dependencies
# api.router.GET("/api/v:version/modules/info", api.modulesInfoHandler)
# api.router.GET("/api/v:version/modules/info/*modules", api.modulesInfoHandler)
# api.router.GET("/api/v:version/projects/info", api.modulesInfoHandler)
# api.router.GET("/api/v:version/projects/info/*modules", api.modulesInfoHandler)

# api.router.GET("/api/v:version/blueprints/list", api.blueprintsListHandler)
# api.router.GET("/api/v:version/blueprints/info/*blueprints", api.blueprintsInfoHandler)
# api.router.GET("/api/v:version/blueprints/depsolve/*blueprints", api.blueprintsDepsolveHandler)
# api.router.GET("/api/v:version/blueprints/freeze/*blueprints", api.blueprintsFreezeHandler)
# api.router.GET("/api/v:version/blueprints/diff/:blueprint/:from/:to", api.blueprintsDiffHandler)
# api.router.GET("/api/v:version/blueprints/changes/*blueprints", api.blueprintsChangesHandler)
# api.router.POST("/api/v:version/blueprints/new", api.blueprintsNewHandler)
# api.router.POST("/api/v:version/blueprints/workspace", api.blueprintsWorkspaceHandler)
# api.router.POST("/api/v:version/blueprints/undo/:blueprint/:commit", api.blueprintUndoHandler)
# api.router.POST("/api/v:version/blueprints/tag/:blueprint", api.blueprintsTagHandler)
# api.router.DELETE("/api/v:version/blueprints/delete/:blueprint", api.blueprintDeleteHandler)
# api.router.DELETE("/api/v:version/blueprints/workspace/:blueprint", api.blueprintDeleteWorkspaceHandler# # )

# api.router.POST("/api/v:version/compose", api.composeHandler)
# api.router.DELETE("/api/v:version/compose/delete/:uuids", api.composeDeleteHandler)
# api.router.GET("/api/v:version/compose/types", api.composeTypesHandler)
# api.router.GET("/api/v:version/compose/queue", api.composeQueueHandler)
# api.router.GET("/api/v:version/compose/status/:uuids", api.composeStatusHandler)
# api.router.GET("/api/v:version/compose/info/:uuid", api.composeInfoHandler)
# api.router.GET("/api/v:version/compose/finished", api.composeFinishedHandler)
# api.router.GET("/api/v:version/compose/failed", api.composeFailedHandler)
# api.router.GET("/api/v:version/compose/image/:uuid", api.composeImageHandler)
# api.router.GET("/api/v:version/compose/metadata/:uuid", api.composeMetadataHandler)
# api.router.GET("/api/v:version/compose/results/:uuid", api.composeResultsHandler)
# api.router.GET("/api/v:version/compose/logs/:uuid", api.composeLogsHandler)
# api.router.GET("/api/v:version/compose/log/:uuid", api.composeLogHandler)
# api.router.POST("/api/v:version/compose/uploads/schedule/:uuid", api.uploadsScheduleHandler)
# api.router.DELETE("/api/v:version/compose/cancel/:uuid", api.composeCancelHandler)

# api.router.DELETE("/api/v:version/upload/delete/:uuid", api.uploadsDeleteHandler)
# api.router.GET("/api/v:version/upload/info/:uuid", api.uploadsInfoHandler)
# api.router.GET("/api/v:version/upload/log/:uuid", api.uploadsLogHandler)
# api.router.POST("/api/v:version/upload/reset/:uuid", api.uploadsResetHandler)
# api.router.DELETE("/api/v:version/upload/cancel/:uuid", api.uploadsCancelHandler)

# api.router.GET("/api/v:version/upload/providers", api.providersHandler)
# api.router.POST("/api/v:version/upload/providers/save", api.providersSaveHandler)
# api.router.DELETE("/api/v:version/upload/providers/delete/:provider/:profile", api.providersDeleteHandler)

# api.router.GET("/api/v:version/distros/list", api.distrosListHandler)
