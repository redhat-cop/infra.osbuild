# -*- coding: utf-8 -*-

# Copyright: Red Hat Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass = type

from unittest.mock import Mock
import pytest

from .....plugins.modules.repository import repository
from .utils import mock_weldr, get_blueprint_info_mock, mock_module, AnsibleFailJson, AnsibleExitJson  # pylint: disable=unused-import

args = {
    "repo_name": "test_repo",
    "base_url": "test.com",
    "type": "yum-baseurl",
    "check_ssl": False,
    "check_gpg": False,
    "gpgkey_urls": "",
    "gpgkey_paths": "",
    "rhsm": False,
    "state": "present",
}


def test_repository_update_error():
    module = mock_module(args)
    weldr_update_error = mock_weldr()
    weldr_update_error.api.delete_projects_source = Mock(return_value={
        "status": False,
        "errors": [{
            "id": "UnknownError",
            "msg": "this is an error."
        }]
    })
    with pytest.raises(AnsibleExitJson) as exit_json_obj:
        repository(module, weldr=weldr_update_error)
    assert 'this is an error.' in str(exit_json_obj)


def test_repository_update():
    module = mock_module(args)
    weldr = mock_weldr()
    with pytest.raises(AnsibleExitJson) as exit_json_obj:
        repository(module, weldr=weldr)
    assert 'Source repository, test_repo, was updated.' in str(exit_json_obj)


def test_repository_new():
    module = mock_module(args)
    weldr_new = mock_weldr()
    weldr_new.api.get_projects_source_info_sources = Mock(return_value={
        "errors": [{
            "id": "UnknownSource",
            "msg": "test is not a valid source"
        }]
    })
    with pytest.raises(AnsibleExitJson) as exit_json_obj:
        repository(module, weldr=weldr_new)
    assert 'New source repository, test_repo, was added to osbuild composer' in str(exit_json_obj)


def test_repository_absent_error():
    args_absent = args
    args_absent["state"] = "absent"
    module = mock_module(args_absent)
    weldr_absent_error = mock_weldr()
    weldr_absent_error.api.get_projects_source_info_sources = Mock(return_value={
        "errors": [{
            "id": "UnknownSource",
            "msg": "test is not a valid source"
        }]
    })
    with pytest.raises(AnsibleExitJson) as exit_json_obj:
        repository(module, weldr=weldr_absent_error)
    assert 'test is not a valid source' in str(exit_json_obj)


def test_repository_absent():
    args_absent = args
    args_absent["state"] = "absent"
    module = mock_module(args_absent)
    weldr = mock_weldr()
    with pytest.raises(AnsibleExitJson) as exit_json_obj:
        repository(module, weldr=weldr)
    assert 'Source repository, test_repo, was deleted from osbuild composer' in str(exit_json_obj)
