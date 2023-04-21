# -*- coding: utf-8 -*-

# Copyright: Red Hat Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass = type

from unittest.mock import patch, mock_open
import pytest

from .....plugins.modules.rhsm_repo_info import rhsm_repo_info
from .utils import mock_module, AnsibleFailJson, AnsibleExitJson  # pylint: disable=unused-import

args = {
    "repos": [
        "rhocp-4.12-for-rhel-8-x86_64-rpms",
        "fast-datapath-for-rhel-8-x86_64-rpms"
    ]
}

test_rhsm_repo_info_results = {
    'changed': True,
    'base_url': 'test.com',
    'check_gpg': False,
    'check_ssl': False,
    'gpgkey_paths': 'test1234',
    'name': 'rhocp-4.12-for-rhel-8-x86_64-rpms',
    'state': 'present',
    'type': 'yum-baseurl'
}


class mock_config_parser():
    def read_file(self, value):
        self.values = value
        return value

    def items(self, value):
        return {
            "baseurl": "test.com",
            "sslverify": False,
            "gpgcheck": False,
            "gpgkey": "test1234"
        }


class mock_config_parser_exception():
    def read_file(self, value):
        self.values = value
        return value

    def items(self, value):
        return {}


def test_rhsm_repo_info():
    module = mock_module(args)
    with patch("os.listdir") as mock_listdir:
        mock_listdir.return_value = ['test_file1']
        with patch("configparser.ConfigParser") as mock_configparser:
            mock_configparser.return_value = mock_config_parser()
            with patch("builtins.open", mock_open(read_data="{'test': 'testing'}")):
                with pytest.raises(AnsibleExitJson) as exit_json_obj:
                    rhsm_repo_info(module)
    for item in test_rhsm_repo_info_results:
        assert item in str(exit_json_obj)


def test_rhsm_repo_info_exception():
    module_exception = mock_module(args)
    with patch("os.listdir") as mock_listdir:
        mock_listdir.return_value = ['test_file1']
        with patch("configparser.ConfigParser") as mock_configparser:
            mock_configparser.return_value = mock_config_parser_exception()
            with patch("builtins.open", mock_open(read_data="{'test': 'testing'}")):
                with pytest.raises(AnsibleFailJson) as fail_json_obj:
                    rhsm_repo_info(module_exception)
    assert 'Could not find rhocp-4.12-for-rhel-8-x86_64-rpms in file, /etc/yum.repos.d/redhat.repo.' in str(fail_json_obj)
