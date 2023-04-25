# -*- coding: utf-8 -*-

# Copyright: Red Hat Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)

__metaclass = type

from unittest.mock import Mock
import pytest
from plugins.modules.wait_compose import wait_compose

from .utils import mock_weldr, get_blueprint_info_mock, mock_module, AnsibleFailJson, AnsibleExitJson  # pylint: disable=unused-import

args = {
    "compose_id": "930a1584-8737-4b61-ba77-582780f0ff2d",
    "timeout": 2,
    "query_frequency": 1,
}

def test_wait_compose_finished():
    module = mock_module(args)
    weldr = mock_weldr()
    with pytest.raises(AnsibleExitJson) as exit_json_obj:
        wait_compose(module, weldr=weldr)
    assert 'Compose FINISHED' in str(exit_json_obj)

def test_wait_compose_failed():
    args['compose_id'] = '030a1584-8737-4b61-ba77-582780f0ff2e'
    module = mock_module(args)
    weldr = mock_weldr()
    with pytest.raises(AnsibleFailJson) as exit_json_obj:
        wait_compose(module, weldr=weldr)
    assert 'Compose FAILED' in str(exit_json_obj)

def test_wait_compose_timeout():
    args['compose_id'] = '0000'
    module = mock_module(args)
    weldr = mock_weldr()
    with pytest.raises(AnsibleFailJson) as exit_json_obj:
        wait_compose(module, weldr=weldr)
    assert 'TIMEOUT REACHED' in str(exit_json_obj)
