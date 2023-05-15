# -*- coding: utf-8 -*-
# Copyright: Red Hat Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
import json
from unittest.mock import MagicMock
from unittest.mock import patch

import pytest

from .....plugins.module_utils.weldrapiv1 import WeldrV1
from ..modules.utils import AnsibleExitJson
from ..modules.utils import mock_module
from ..modules.utils import mock_weldr

# from ..modules.utils import AnsibleFailJson


def test_get_status(mocker):
    weldr = mock_weldr()
    weldrv1 = WeldrV1(weldr)
    with pytest.raises(NotImplementedError):
        weldrv1.get_status()


# Projects source
@pytest.mark.skip(reason="Test not implemented yet")
def test_get_projects_source_list(mocker):
    # weldr = mock_weldr()
    # weldrv1 = WeldrV1(weldr)

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


@pytest.mark.skip(reason="Test not implemented yet")
def test_get_projects_source_info(mocker):
    pass


@pytest.mark.skip(reason="Test not implemented yet")
def test_get_projects_source_info_sources(mocker):
    pass


@pytest.mark.skip(reason="Test not implemented yet")
def test_post_projects_source_new(mocker):
    pass


@pytest.mark.skip(reason="Test not implemented yet")
def test_delete_projects_source(mocker):
    pass


# Projects depsolve
def test_get_projects_depsolve(mocker):
    weldr = mock_weldr()
    weldrv1 = WeldrV1(weldr)
    with pytest.raises(NotImplementedError):
        weldrv1.get_projects_depsolve()


def test_get_projects_depsolve_projects(mocker):
    weldr = mock_weldr()
    weldrv1 = WeldrV1(weldr)
    with pytest.raises(NotImplementedError):
        weldrv1.get_projects_depsolve_projects(projects=1)


# Modules/projects list
@pytest.mark.skip(reason="Test not implemented yet")
def test_get_modules_list(mocker):
    pass


def test_get_modules_list_modules(mocker):
    weldr = mock_weldr()
    weldrv1 = WeldrV1(weldr)
    with pytest.raises(NotImplementedError):
        weldrv1.get_modules_list_modules(modules=1)


def test_get_projects_list(mocker):
    weldr = mock_weldr()
    weldrv1 = WeldrV1(weldr)
    with pytest.raises(NotImplementedError):
        weldrv1.get_projects_list()


def test_get_projects_lists(mocker):
    weldr = mock_weldr()
    weldrv1 = WeldrV1(weldr)
    with pytest.raises(NotImplementedError):
        weldrv1.get_projects_lists()


# Modules/projects info with dependencies
# these are the same, except that modules/info also includes dependencies
def test_get_modules_info(mocker):
    weldr = mock_weldr()
    weldrv1 = WeldrV1(weldr)
    with pytest.raises(NotImplementedError):
        weldrv1.get_modules_info()


def test_get_modules_info_modules(mocker):
    weldr = mock_weldr()
    weldrv1 = WeldrV1(weldr)
    with pytest.raises(NotImplementedError):
        weldrv1.get_modules_info_modules(modules=1)


def test_get_projects_info(mocker):
    weldr = mock_weldr()
    weldrv1 = WeldrV1(weldr)
    with pytest.raises(NotImplementedError):
        weldrv1.get_projects_info()


def test_get_projects_info_modules(mocker):
    weldr = mock_weldr()
    weldrv1 = WeldrV1(weldr)
    with pytest.raises(NotImplementedError):
        weldrv1.get_projects_info_modules(modules=1)


# Blueprints
@pytest.mark.skip(reason="Test not implemented yet")
def test_get_blueprints_list(mocker):
    pass


@pytest.mark.skip(reason="Test not implemented yet")
def test_get_blueprints_info(mocker):
    pass


def test_get_blueprints_depsolve(mocker):
    weldr = mock_weldr()
    weldrv1 = WeldrV1(weldr)
    with pytest.raises(NotImplementedError):
        weldrv1.get_blueprints_depsolve(blueprints=1)


def test_get_blueprints_freeze(mocker):
    weldr = mock_weldr()
    weldrv1 = WeldrV1(weldr)
    with pytest.raises(NotImplementedError):
        weldrv1.get_blueprints_freeze(blueprints=1)


def test_get_blueprints_diff(mocker):
    weldr = mock_weldr()
    weldrv1 = WeldrV1(weldr)
    with pytest.raises(NotImplementedError):
        weldrv1.get_blueprints_diff(blueprint_from=1, blueprint_to=2)


def test_get_blueprints_change_commit(mocker):
    weldr = mock_weldr()
    weldrv1 = WeldrV1(weldr)
    with pytest.raises(NotImplementedError):
        weldrv1.get_blueprints_change_commit(blueprints=1, commit=2)


def test_get_blueprints_changes(mocker):
    weldr = mock_weldr()
    weldrv1 = WeldrV1(weldr)
    with pytest.raises(NotImplementedError):
        weldrv1.get_blueprints_changes(blueprints=1)


@pytest.mark.skip(reason="Test not implemented yet")
def test_post_blueprint_new(mocker):
    pass


def test_post_blueprints_workspace(mocker):
    weldr = mock_weldr()
    weldrv1 = WeldrV1(weldr)
    with pytest.raises(NotImplementedError):
        weldrv1.post_blueprints_workspace(workspace=1)


def test_post_blueprints_undo_commit(mocker):
    weldr = mock_weldr()
    weldrv1 = WeldrV1(weldr)
    with pytest.raises(NotImplementedError):
        weldrv1.post_blueprints_undo_commit(blueprint=1, commit=2)


def test_post_blueprints_tag(mocker):
    weldr = mock_weldr()
    weldrv1 = WeldrV1(weldr)
    with pytest.raises(NotImplementedError):
        weldrv1.post_blueprints_tag(blueprint=1)


def test_delete_blueprints(mocker):
    weldr = mock_weldr()
    weldrv1 = WeldrV1(weldr)
    with pytest.raises(NotImplementedError):
        weldrv1.delete_blueprints(blueprint=1)


def test_delete_blueprints_workspace(mocker):
    weldr = mock_weldr()
    weldrv1 = WeldrV1(weldr)
    with pytest.raises(NotImplementedError):
        weldrv1.delete_blueprints_workspace(blueprint=1)


# Composes
def test_post_compose(mocker):
    weldr = mock_weldr()
    weldrv1 = WeldrV1(weldr)

    EXPECTED_RETURNED_VALUE = {"status_code": 200, "body": {"body": {}, "msg": "go home", "status": 200}}
    FETCH_URL_INFO = {"body": {}, "msg": "go home", "status": 200}
    FETCH_URL_RESPONSE = MagicMock()
    FETCH_URL_RESPONSE.read.return_value = json.dumps(FETCH_URL_INFO, ensure_ascii=False).encode("utf-8")
    FETCH_URL_RETURN_VALUE = (FETCH_URL_RESPONSE, FETCH_URL_INFO)
    compose_settings: dict[str, str] = {"blueprint_name": "test_blueprint_aap", "compose_type": "edge_installer", "branch": "master", "size": 42}
    with patch(target="ansible_collections.infra.osbuild.plugins.module_utils.weldrapiv1.fetch_url", return_value=FETCH_URL_RETURN_VALUE):
        actual_returned_value = weldrv1.post_compose(compose_settings)
        assert actual_returned_value == EXPECTED_RETURNED_VALUE, f"Expected '{EXPECTED_RETURNED_VALUE}',\nactual = '{actual_returned_value}'"


def test_post_compose_negative(mocker):
    weldr = mock_weldr()
    weldrv1 = WeldrV1(weldr)

    EXPECTED_RETURNED_VALUE = {"status_code": 200, "body": {"body": {}, "msg": "go home", "status": 200}}
    FETCH_URL_INFO = {"body": {}, "msg": "go home", "status": 403}
    FETCH_URL_RESPONSE = MagicMock()
    FETCH_URL_RESPONSE.read.return_value = json.dumps(FETCH_URL_INFO, ensure_ascii=False).encode("utf-8")
    FETCH_URL_RETURN_VALUE = (FETCH_URL_RESPONSE, FETCH_URL_INFO)
    compose_settings: dict[str, str] = {"blueprint_name": "test_blueprint_aap", "compose_type": "edge_installer", "branch": "master", "size": 42}
    with patch(target="ansible_collections.infra.osbuild.plugins.module_utils.weldrapiv1.fetch_url", return_value=FETCH_URL_RETURN_VALUE):
        import socket

        with pytest.raises(socket.timeout):
            actual_returned_value = weldrv1.post_compose(compose_settings)
            assert actual_returned_value == EXPECTED_RETURNED_VALUE, f"Expected '{EXPECTED_RETURNED_VALUE}',\nactual = '{actual_returned_value}'"


@pytest.mark.skip(reason="Test not implemented yet")
def test_delete_compose(mocker):
    pass


@pytest.mark.skip(reason="Test not implemented yet")
def test_get_compose_types(mocker):
    pass


@pytest.mark.skip(reason="Test not implemented yet")
def test_get_compose_queue(mocker):
    pass


@pytest.mark.skip(reason="Test not implemented yet")
def test_get_compose_status(mocker):
    pass


@pytest.mark.skip(reason="Test not implemented yet")
def test_get_compose_info(mocker):
    pass


@pytest.mark.skip(reason="Test not implemented yet")
def test_get_compose_finished(mocker):
    pass


@pytest.mark.skip(reason="Test not implemented yet")
def test_get_compose_failed(mocker):
    pass


@pytest.mark.skip(reason="Test not implemented yet")
def test_get_compose_image(mocker):
    pass


def test_get_compose_metadata(mocker):
    weldr = mock_weldr()
    weldrv1 = WeldrV1(weldr)
    with pytest.raises(NotImplementedError):
        weldrv1.get_compose_metadata(compose_uuid=1)


def test_get_compose_results(mocker):
    weldr = mock_weldr()
    weldrv1 = WeldrV1(weldr)
    with pytest.raises(NotImplementedError):
        weldrv1.get_compose_results(compose_uuid=1)


def test_get_compose_logs(mocker):
    weldr = mock_weldr()
    weldrv1 = WeldrV1(weldr)
    with pytest.raises(NotImplementedError):
        weldrv1.get_compose_logs(compose_uuid=1)


def test_get_compose_log(mocker):
    weldr = mock_weldr()
    weldrv1 = WeldrV1(weldr)
    with pytest.raises(NotImplementedError):
        weldrv1.get_compose_log(compose_uuid=1)


def test_post_compose_uploads_schedule(mocker):
    weldr = mock_weldr()
    weldrv1 = WeldrV1(weldr)
    with pytest.raises(NotImplementedError):
        weldrv1.post_compose_uploads_schedule(compose_uuid=1)


def test_compose_cancel(mocker):
    weldr = mock_weldr()
    weldrv1 = WeldrV1(weldr)
    with pytest.raises(NotImplementedError):
        weldrv1.compose_cancel(compose_uuid=1)


# Uploads
def test_delete_compose_upload(mocker):
    weldr = mock_weldr()
    weldrv1 = WeldrV1(weldr)
    with pytest.raises(NotImplementedError):
        weldrv1.delete_compose_upload(compose_uuid=1)


def test_get_version_info(mocker):
    weldr = mock_weldr()
    weldrv1 = WeldrV1(weldr)
    with pytest.raises(NotImplementedError):
        weldrv1.get_version_info(compose_uuid=1)


def test_get_version_upload_log(mocker):
    weldr = mock_weldr()
    weldrv1 = WeldrV1(weldr)
    with pytest.raises(NotImplementedError):
        weldrv1.get_version_upload_log(compose_uuid=1)


def test_upload_reset(mocker):
    weldr = mock_weldr()
    weldrv1 = WeldrV1(weldr)
    with pytest.raises(NotImplementedError):
        weldrv1.upload_reset(compose_uuid=1)


def test_upload_cancel(mocker):
    weldr = mock_weldr()
    weldrv1 = WeldrV1(weldr)
    with pytest.raises(NotImplementedError):
        weldrv1.upload_cancel(compose_uuid=1)


# Upload providers
def test_get_upload_providers(mocker):
    weldr = mock_weldr()
    weldrv1 = WeldrV1(weldr)
    with pytest.raises(NotImplementedError):
        weldrv1.get_upload_providers()


def test_save_providers(mocker):
    weldr = mock_weldr()
    weldrv1 = WeldrV1(weldr)
    with pytest.raises(NotImplementedError):
        weldrv1.save_providers()


def test_delete_provider(mocker):
    weldr = mock_weldr()
    weldrv1 = WeldrV1(weldr)
    with pytest.raises(NotImplementedError):
        weldrv1.delete_provider(provider=1, profile=2)


# Distros
def test_get_distros_list(mocker):
    weldr = mock_weldr()
    weldrv1 = WeldrV1(weldr)
    with pytest.raises(NotImplementedError):
        weldrv1.get_distros_list()
