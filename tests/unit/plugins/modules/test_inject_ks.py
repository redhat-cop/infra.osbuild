# -*- coding: utf-8 -*-

# Copyright: Red Hat Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass = type

from unittest.mock import patch, Mock
import pytest

from .....plugins.modules.inject_ks import inject_ks
from .utils import mock_module, AnsibleFailJson, AnsibleExitJson

args = {
    "kickstart": "test_kickstart.ks",
    "src_iso": "test.iso",
    "dest_iso": "test_ks.iso",
}


def test_inject_ks():
    module = mock_module(args)
    module.run_command = Mock(return_value=(0, "", ""))
    with patch("os.path.exists") as mock_path_exists:
        mock_path_exists.return_value = True
        with patch("ansible.module_utils.common.locale.get_best_parsable_locale") as mock_get_locale:
            mock_get_locale.return_value = "C"
            with pytest.raises(AnsibleExitJson) as exit_json_obj:
                inject_ks(module=module)
    assert 'Kickstart added to ISO' in str(exit_json_obj)


def test_inject_ks_no_file():
    module = mock_module(args)
    module.run_command = Mock(return_value=(0, "", ""))
    with patch("os.path.exists") as mock_path_exists:
        mock_path_exists.return_value = False
        with pytest.raises(AnsibleFailJson) as fail_json_obj:
            inject_ks(module=module)
    assert 'No such file found' in str(fail_json_obj)


def test_inject_ks_error():
    module = mock_module(args)
    module.run_command = Mock(return_value=(1, "", ""))
    with patch("os.path.exists") as mock_path_exists:
        mock_path_exists.return_value = True
        with patch("ansible.module_utils.common.locale.get_best_parsable_locale") as mock_get_locale:
            mock_get_locale.return_value = "C"
            with pytest.raises(AnsibleFailJson) as fail_json_obj:
                inject_ks(module=module)
    assert "ERROR: Command 'mkksiso test_kickstart.ks test.iso test_ks.iso' failed with return code: 1" in str(fail_json_obj)
