# -*- coding: utf-8 -*-
# Copyright: Red Hat Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import socket
from unittest.mock import Mock

import pytest

from .....plugins.modules.start_compose import start_compose
from .utils import AnsibleExitJson
from .utils import AnsibleFailJson
from .utils import mock_module
from .utils import mock_weldr

__metaclass = type

args = {
    "blueprint": "test_blueprint",
    "size": 0,
    "profile": "",
    "image_name": "",
    "allow_duplicate": True,
    "compose_type": "edge-commit",
    "ostree_ref": "",
    "ostree_parent": "",
    "ostree_url": "",
    "timeout": 60,
}


def test_start_compose_not_valid_image_type():
    args["compose_type"] = "not-valid"
    module = mock_module(args)
    weldr = mock_weldr()
    with pytest.raises(AnsibleFailJson) as fail_json_obj:
        start_compose(module, weldr=weldr)
    assert "not a valid image type" in str(fail_json_obj)


def test_start_compose_not_supported_image_type():
    args["compose_type"] = "edge-installer"
    module = mock_module(args)
    weldr = mock_weldr()
    with pytest.raises(AnsibleFailJson) as fail_json_obj:
        start_compose(module, weldr=weldr)
    assert "not a supported image type" in str(fail_json_obj)


def test_start_compose_unable_to_determine_build():
    module = mock_module(args)
    weldr = mock_weldr()
    weldr.api.post_compose = Mock(side_effect=socket.timeout())
    with pytest.raises(AnsibleFailJson) as fail_json_obj:
        start_compose(module, weldr=weldr)
    assert "Unable to determine state of build" in str(fail_json_obj)


def test_start_compose_submitted_queue():
    module = mock_module(args)
    weldr = mock_weldr()
    with pytest.raises(AnsibleExitJson) as exit_json_obj:
        start_compose(module, weldr=weldr)
    assert "Compose submitted to queue" in str(exit_json_obj)


def test_start_compose_submitted_duplicate():
    args["allow_duplicate"] = False
    module = mock_module(args)
    weldr = mock_weldr()
    with pytest.raises(AnsibleExitJson) as exit_json_obj:
        start_compose(module, weldr=weldr)
    assert "Not queuing a duplicate versioned" in str(exit_json_obj)
