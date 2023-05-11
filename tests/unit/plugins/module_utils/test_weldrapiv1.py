# -*- coding: utf-8 -*-
# Copyright: Red Hat Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from unittest.mock import patch

import pytest

from ..modules.utils import AnsibleExitJson
from ..modules.utils import mock_module
from ..modules.utils import mock_weldr
from plugins.module_utils.weldrapiv1 import WeldrV1

# from ..modules.utils import AnsibleFailJson


def test__init__(mocker):
    weldr = mock_weldr()
    weldrv1 = WeldrV1(weldr)
    assert weldrv1 is not None


def test_get_status(mocker):
    weldr = mock_weldr()
    weldrv1 = WeldrV1(weldr)
    with pytest.raises(NotImplementedError):
        weldrv1.get_status()
        assert False, "get_status() did not raise an exception"


# Projects source
def test_get_projects_source_list(mocker):
    weldr = mock_weldr()
    weldrv1 = WeldrV1(weldr)  # noqa F841

    args = {}
    module = mock_module(args)
    MOCK_FUNCTION_RETURN_VALUE = "Initial return value"
    with pytest.raises(AnsibleExitJson) as exit_json_obj:  # noqa F841
        MOCK_FUNCTION_RETURN_VALUE = module.exit_json("No result")
    EXPECTED_RESULTS = MOCK_FUNCTION_RETURN_VALUE  # noqa F841
    with patch(target="plugins.module_utils.weldrapiv1.open", return_value=MOCK_FUNCTION_RETURN_VALUE):
        # actual_results = weldrv1.get_projects_source_list()
        # assert actual_results == EXPECTED_RESULTS
        pass


def test_get_projects_source_info(mocker):
    pass


def test_get_projects_source_info_sources(mocker):
    pass


def test_post_projects_source_new(mocker):
    pass


def test_delete_projects_source(mocker):
    pass


# Projects depsolve
def test_get_projects_depsolve(mocker):
    weldr = mock_weldr()
    weldrv1 = WeldrV1(weldr)
    with pytest.raises(NotImplementedError):
        weldrv1.get_projects_depsolve()
        assert False, "get_projects_depsolve() did not raise an exception"


def test_get_projects_depsolve_projects(mocker):
    weldr = mock_weldr()
    weldrv1 = WeldrV1(weldr)
    with pytest.raises(NotImplementedError):
        weldrv1.get_projects_depsolve_projects(projects=1)
        assert False, "get_projects_depsolve_projects() did not raise an exception"


# Modules/projects list
def test_get_modules_list(mocker):
    pass


def test_get_modules_list_modules(mocker):
    weldr = mock_weldr()
    weldrv1 = WeldrV1(weldr)
    with pytest.raises(NotImplementedError):
        weldrv1.get_modules_list_modules(modules=1)
        assert False, "get_modules_list_modules() did not raise an exception"


def test_get_projects_list(mocker):
    weldr = mock_weldr()
    weldrv1 = WeldrV1(weldr)
    with pytest.raises(NotImplementedError):
        weldrv1.get_projects_list()
        assert False, "get_projects_list() did not raise an exception"


def test_get_projects_lists(mocker):
    weldr = mock_weldr()
    weldrv1 = WeldrV1(weldr)
    with pytest.raises(NotImplementedError):
        weldrv1.get_projects_lists()
        assert False, "get_projects_lists() did not raise an exception"


# Modules/projects info with dependencies
# these are the same, except that modules/info also includes dependencies
def test_get_modules_info(mocker):
    weldr = mock_weldr()
    weldrv1 = WeldrV1(weldr)
    with pytest.raises(NotImplementedError):
        weldrv1.get_modules_info()
        assert False, "get_modules_info() did not raise an exception"


def test_get_modules_info_modules(mocker):
    weldr = mock_weldr()
    weldrv1 = WeldrV1(weldr)
    with pytest.raises(NotImplementedError):
        weldrv1.get_modules_info_modules(modules=1)
        assert False, "get_modules_info_modules() did not raise an exception"


def test_get_projects_info(mocker):
    weldr = mock_weldr()
    weldrv1 = WeldrV1(weldr)
    with pytest.raises(NotImplementedError):
        weldrv1.get_projects_info()
        assert False, "get_projects_info() did not raise an exception"


def test_get_projects_info_modules(mocker):
    weldr = mock_weldr()
    weldrv1 = WeldrV1(weldr)
    with pytest.raises(NotImplementedError):
        weldrv1.get_projects_info_modules(modules=1)
        assert False, "get_projects_info_modules() did not raise an exception"


# Blueprints
def test_get_blueprints_list(mocker):
    pass


def test_get_blueprints_info(mocker):
    pass


def test_get_blueprints_depsolve(mocker):
    weldr = mock_weldr()
    weldrv1 = WeldrV1(weldr)
    with pytest.raises(NotImplementedError):
        weldrv1.get_blueprints_depsolve(blueprints=1)
        assert False, "get_blueprints_depsolve() did not raise an exception"


def test_get_blueprints_freeze(mocker):
    weldr = mock_weldr()
    weldrv1 = WeldrV1(weldr)
    with pytest.raises(NotImplementedError):
        weldrv1.get_blueprints_freeze(blueprints=1)
        assert False, "get_blueprints_freeze() did not raise an exception"


def test_get_blueprints_diff(mocker):
    weldr = mock_weldr()
    weldrv1 = WeldrV1(weldr)
    with pytest.raises(NotImplementedError):
        weldrv1.get_blueprints_diff(blueprint_from=1, blueprint_to=2)
        assert False, "get_blueprints_diff() did not raise an exception"


def test_get_blueprints_change_commit(mocker):
    weldr = mock_weldr()
    weldrv1 = WeldrV1(weldr)
    with pytest.raises(NotImplementedError):
        weldrv1.get_blueprints_change_commit(blueprints=1, commit=2)
        assert False, "get_blueprints_change_commit() did not raise an exception"


def test_get_blueprints_changes(mocker):
    weldr = mock_weldr()
    weldrv1 = WeldrV1(weldr)
    with pytest.raises(NotImplementedError):
        weldrv1.get_blueprints_changes(blueprints=1)
        assert False, "get_blueprints_changes() did not raise an exception"


def test_post_blueprint_new(mocker):
    pass


def test_post_blueprints_workspace(mocker):
    weldr = mock_weldr()
    weldrv1 = WeldrV1(weldr)
    with pytest.raises(NotImplementedError):
        weldrv1.post_blueprints_workspace(workspace=1)
        assert False, "post_blueprints_workspace() did not raise an exception"


def test_post_blueprints_undo_commit(mocker):
    weldr = mock_weldr()
    weldrv1 = WeldrV1(weldr)
    with pytest.raises(NotImplementedError):
        weldrv1.post_blueprints_undo_commit(blueprint=1, commit=2)
        assert False, "post_blueprints_undo_commit() did not raise an exception"


def test_post_blueprints_tag(mocker):
    weldr = mock_weldr()
    weldrv1 = WeldrV1(weldr)
    with pytest.raises(NotImplementedError):
        weldrv1.post_blueprints_tag(blueprint=1)
        assert False, "post_blueprints_tag() did not raise an exception"


def test_delete_blueprints(mocker):
    weldr = mock_weldr()
    weldrv1 = WeldrV1(weldr)
    with pytest.raises(NotImplementedError):
        weldrv1.delete_blueprints(blueprint=1)
        assert False, "delete_blueprints() did not raise an exception"


def test_delete_blueprints_workspace(mocker):
    weldr = mock_weldr()
    weldrv1 = WeldrV1(weldr)
    with pytest.raises(NotImplementedError):
        weldrv1.delete_blueprints_workspace(blueprint=1)
        assert False, "delete_blueprints_workspace() did not raise an exception"


# Composes
def test_post_compose(mocker):
    weldr = mock_weldr()
    weldrv1 = WeldrV1(weldr)

    EXPECTED_RETURNED_VALUE = {"body": "tbd", "error_msg": "go home", "status_code": 999}
    MOCK_FUNCTION_INFO = {"body": "tbd", "msg": "go home", "status": 999}
    MOCK_FUNCTION_RESPONSE = {}
    MOCK_FUNCTION_RETURN_VALUE = (MOCK_FUNCTION_RESPONSE, MOCK_FUNCTION_INFO)
    compose_settings: dict[str, str] = {"blueprint_name": "test_blueprint_aap", "compose_type": "edge_installer", "branch": "master", "size": 42}
    with patch(target="plugins.module_utils.weldrapiv1.fetch_url", return_value=MOCK_FUNCTION_RETURN_VALUE):
        actual_returned_value = weldrv1.post_compose(compose_settings)
        assert actual_returned_value == EXPECTED_RETURNED_VALUE


def test_delete_compose(mocker):
    pass


def test_get_compose_types(mocker):
    pass


def test_get_compose_queue(mocker):
    pass


def test_get_compose_status(mocker):
    pass


def test_get_compose_info(mocker):
    pass


def test_get_compose_finished(mocker):
    pass


def test_get_compose_failed(mocker):
    pass


def test_get_compose_image(mocker):
    pass


def test_get_compose_metadata(mocker):
    weldr = mock_weldr()
    weldrv1 = WeldrV1(weldr)
    with pytest.raises(NotImplementedError):
        weldrv1.get_compose_metadata(compose_uuid=1)
        assert False, "get_compose_metadata() did not raise an exception"


def test_get_compose_results(mocker):
    weldr = mock_weldr()
    weldrv1 = WeldrV1(weldr)
    with pytest.raises(NotImplementedError):
        weldrv1.get_compose_results(compose_uuid=1)
        assert False, "get_compose_results() did not raise an exception"


def test_get_compose_logs(mocker):
    weldr = mock_weldr()
    weldrv1 = WeldrV1(weldr)
    with pytest.raises(NotImplementedError):
        weldrv1.get_compose_logs(compose_uuid=1)
        assert False, "get_compose_logs() did not raise an exception"


def test_get_compose_log(mocker):
    weldr = mock_weldr()
    weldrv1 = WeldrV1(weldr)
    with pytest.raises(NotImplementedError):
        weldrv1.get_compose_log(compose_uuid=1)
        assert False, "get_compose_log() did not raise an exception"


def test_post_compose_uploads_schedule(mocker):
    weldr = mock_weldr()
    weldrv1 = WeldrV1(weldr)
    with pytest.raises(NotImplementedError):
        weldrv1.post_compose_uploads_schedule(compose_uuid=1)
        assert False, "post_compose_uploads_schedule() did not raise an exception"


def test_compose_cancel(mocker):
    weldr = mock_weldr()
    weldrv1 = WeldrV1(weldr)
    with pytest.raises(NotImplementedError):
        weldrv1.compose_cancel(compose_uuid=1)
        assert False, "compose_cancel() did not raise an exception"


# Uploads
def test_delete_compose_upload(mocker):
    weldr = mock_weldr()
    weldrv1 = WeldrV1(weldr)
    with pytest.raises(NotImplementedError):
        weldrv1.delete_compose_upload(compose_uuid=1)
        assert False, "delete_compose_upload() did not raise an exception"


def test_get_version_info(mocker):
    weldr = mock_weldr()
    weldrv1 = WeldrV1(weldr)
    with pytest.raises(NotImplementedError):
        weldrv1.get_version_info(compose_uuid=1)
        assert False, "get_version_info() did not raise an exception"


def test_get_version_upload_log(mocker):
    weldr = mock_weldr()
    weldrv1 = WeldrV1(weldr)
    with pytest.raises(NotImplementedError):
        weldrv1.get_version_upload_log(compose_uuid=1)
        assert False, "get_version_upload_log() did not raise an exception"


def test_upload_reset(mocker):
    weldr = mock_weldr()
    weldrv1 = WeldrV1(weldr)
    with pytest.raises(NotImplementedError):
        weldrv1.upload_reset(compose_uuid=1)
        assert False, "upload_reset() did not raise an exception"


def test_upload_cancel(mocker):
    weldr = mock_weldr()
    weldrv1 = WeldrV1(weldr)
    with pytest.raises(NotImplementedError):
        weldrv1.upload_cancel(compose_uuid=1)
        assert False, "upload_cancel() did not raise an exception"


# Upload providers
def test_get_upload_providers(mocker):
    weldr = mock_weldr()
    weldrv1 = WeldrV1(weldr)
    with pytest.raises(NotImplementedError):
        weldrv1.get_upload_providers()
        assert False, "get_upload_providers() did not raise an exception"


def test_save_providers(mocker):
    weldr = mock_weldr()
    weldrv1 = WeldrV1(weldr)
    with pytest.raises(NotImplementedError):
        weldrv1.save_providers()
        assert False, "save_providers() did not raise an exception"


def test_delete_provider(mocker):
    weldr = mock_weldr()
    weldrv1 = WeldrV1(weldr)
    with pytest.raises(NotImplementedError):
        weldrv1.delete_provider(provider=1, profile=2)
        assert False, "delete_provider() did not raise an exception"


# Distros
def test_get_distros_list(mocker):
    weldr = mock_weldr()
    weldrv1 = WeldrV1(weldr)
    with pytest.raises(NotImplementedError):
        weldrv1.get_distros_list()
        assert False, "get_distros_list() did not raise an exception"
