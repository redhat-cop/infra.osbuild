# -*- coding: utf-8 -*-

# Copyright: Red Hat Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass = type

from unittest.mock import Mock, MagicMock
import toml

blueprint_sanity_check_mock = {"errors": []}

get_blueprint_info_mock = {
    "errors": [],
    "blueprints": [{
        "version": "0.0.1"
    }]
}

get_blueprint_list_mock = {
    "errors": [],
    "blueprints": ["test_blueprint_01", "test_blueprint_02", "test_blueprint_03"]
}

post_blueprint_new_mock = {"errors": [], "status": True}

get_projects_source_info_sources_mock = {"errors": []}

delete_projects_source_mock = {"errors": [], "status": True}

post_projects_source_new_mock = {"errors": []}

get_compose_types_mock = {
    "errors": [],
    "types": [
        "ami",
        "edge-commit",
        "edge-container",
        "edge-installer",
        "edge-raw-image",
        "edge-simplified-installer",
        "image-installer",
        "oci",
        "openstack",
        "qcow2",
        "tar",
        "vhd",
        "vmdk",
        "iot-commit",
        "iot-container",
        "iot-installer",
        "iot-raw-image",
        "container"
    ]
}

get_compose_queue_mock = {
    "errors": [],
    "new": [],
    "run": [{
        "id": "930a1584-8737-4b61-ba77-582780f0ff2d",
        "blueprint": "base-image-with-tmux",
        "version": "0.0.5",
        "compose_type": "edge-commit",
        "image_size": 0,
        "queue_status": "RUNNING",
        "job_created": 1654620015.4107578,
        "job_started": 1654620015.415151
    }]
}

get_compose_finished_mock = {
    "errors": [],
    "new": [],
    "finished": [{
        "id": "930a1584-8737-4b61-ba77-582780f0ff2d",
        "blueprint": "base-image-with-tmux",
        "version": "0.0.5",
        "compose_type": "edge-commit",
        "image_size": 8192,
        "queue_status": "FINISHED",
        "job_created": 1654620015.4107578,
        "job_started": 1654620015.415151,
        "job_finished": 1654620302.9069786
    }]
}

get_compose_failed_mock = {
    "errors": [],
    "new": [],
    "failed": [{
        "id": "030a1584-8737-4b61-ba77-582780f0ff2e",
        "blueprint": "base-image-with-tmux",
        "version": "0.0.5",
        "compose_type": "edge-commit",
        "image_size": 8192,
        "queue_status": "FAILED",
        "job_created": 1654620015.4107578,
        "job_started": 1654620015.415151,
        "job_finished": 1654620302.9069786
    }]
}

get_compose_status_mock = {
    "errors": [],
    "uuids": [{
        "id": "930a1584-8737-4b61-ba77-582780f0ff2d",
        "blueprint": "base-image-with-tmux",
        "version": "0.0.5",
        "compose_type": "edge-commit",
        "image_size": 0,
        "queue_status": "RUNNING",
        "job_created": 1654620015.4107578,
        "job_started": 1654620015.415151
    }]
}

post_compose_mock = {"errors": []}


class AnsibleFailJson(Exception):
    """Exception class to be raised by module.fail_json and caught by the test case"""
    pass


class AnsibleExitJson(Exception):
    """Exception class to be raised by module.exit_json and caught by the test case"""
    pass


def fail_json_mock(*args, **kwargs):
    kwargs['failed'] = True
    raise AnsibleFailJson(kwargs)


def exit_json_mock(*args, **kwargs):
    if 'changed' not in kwargs:
        kwargs['changed'] = False
    raise AnsibleExitJson(kwargs)


def mock_module(args):
    module = MagicMock()
    module.fail_json = fail_json_mock
    module.exit_json = exit_json_mock
    module.params = args

    return module


def mock_weldr():
    weldr = Mock(return_value={"api: {}"})

    weldr.blueprint_sanity_check = Mock(return_value=blueprint_sanity_check_mock)
    weldr.api.get_blueprints_info = Mock(return_value=get_blueprint_info_mock)
    weldr.api.get_blueprints_list = Mock(return_value=get_blueprint_list_mock)
    weldr.api.post_blueprint_new = Mock(return_value=post_blueprint_new_mock)
    weldr.api.get_projects_source_info_sources = Mock(return_value=get_projects_source_info_sources_mock)
    weldr.api.delete_projects_source = Mock(return_value=delete_projects_source_mock)
    weldr.api.post_projects_source_new = Mock(return_value=post_projects_source_new_mock)
    weldr.api.get_compose_types = Mock(return_value=get_compose_types_mock)
    weldr.api.get_compose_queue = Mock(return_value=get_compose_queue_mock)
    weldr.api.get_compose_finished = Mock(return_value=get_compose_finished_mock)
    weldr.api.get_compose_failed = Mock(return_value=get_compose_failed_mock)
    weldr.api.get_compose_status = Mock(return_value=get_compose_status_mock)
    weldr.api.post_compose = Mock(return_value=post_compose_mock)
    weldr.toml = toml

    return weldr
