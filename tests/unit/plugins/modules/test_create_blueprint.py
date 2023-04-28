# -*- coding: utf-8 -*-

# Copyright: Red Hat Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass = type

from unittest.mock import Mock
import pytest

from .....plugins.modules.create_blueprint import create_blueprint
from .utils import mock_weldr, get_blueprint_info_mock, mock_module, AnsibleFailJson, AnsibleExitJson

args = {
    "dest": "/tmp/blueprint.toml",
    "name": "test_blueprint",
    "description": "",
    "distro": "",
    "version_type": "patch",
    "packages": [],
    "groups": [],
    "customizations": {"user": "bob"}
}


def test_create_blueprint():
    module = mock_module(args)
    weldr = mock_weldr()
    with pytest.raises(AnsibleExitJson) as exit_json_obj:
        create_blueprint(module, weldr=weldr)
    file = open(args["dest"], "r")
    assert 'Blueprint file written to location: /tmp/blueprint.toml' in str(exit_json_obj)
    assert file.read() == 'name = "test_blueprint"\ndescription = "test_blueprint"\nversion = "0.0.2"\n\n[customizations]\nuser = "bob"\n'


def test_create_blueprint_first_version():
    args["dest"] = "/tmp/blueprint_first_version.toml"
    args["name"] = "test_blueprint_first_version"
    module_first_version = mock_module(args)
    module_first_version.params = args
    get_blueprint_info_mock_fail = get_blueprint_info_mock
    get_blueprint_info_mock_fail["errors"] = [{"id": "UnknownBlueprint"}]
    weldr_first_version = mock_weldr()
    weldr_first_version.api.get_blueprints_info = Mock(return_value=get_blueprint_info_mock_fail)
    with pytest.raises(AnsibleExitJson) as exit_json_obj:
        create_blueprint(module_first_version, weldr=weldr_first_version)
    file = open(args["dest"], "r")
    read_file = file.read()
    assert 'Blueprint file written to location: /tmp/blueprint_first_version.toml' in str(exit_json_obj)
    assert read_file == 'name = "test_blueprint_first_version"\ndescription = "test_blueprint_first_version"\nversion = "0.0.1"\n\n[customizations]\nuser = "bob"\n'  # noqa yaml[line-length]


def test_create_blueprint_exception():
    module_exception = mock_module(args)
    weldr_exception = mock_weldr()
    weldr_exception.api.get_blueprints_info = Mock(side_effect=NameError('Test exception'))
    with pytest.raises(AnsibleFailJson) as fail_json_obj:
        create_blueprint(module_exception, weldr=weldr_exception)
    assert 'Error: Test exception. OSbuild composer service is unavailable' in str(fail_json_obj.value)
