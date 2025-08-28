#!/usr/bin/python
# Copyright: Red Hat Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

ANSIBLE_METADATA = {
    "metadata_version": "1.1",
    "status": ["preview"],
    "supported_by": "community",
}

DOCUMENTATION = """
---
module: start_compose
short_description: Start an ostree compose
description:
    - Start an ostree compose
author:
    - Adam Miller (@maxamillion)
    - Chris Santiago (@resoluteCoder)
options:
    blueprint:
        description:
            - Name of blueprint to iniate a build for
        type: str
        required: true
    size:
        description:
            - Image size expressed in MiB
        type: int
        default: 0
        required: false
    profile:
        description:
            - Path to profile toml file
        type: str
        default: ""
        required: false
    image_name:
        description:
            - Image name
        type: str
        default: ""
        required: false
    allow_duplicate:
        description:
            - Allow a duplicate version'd compose.
            - (Default osbuild composer functionality is to allow duplicate composes)
        type: bool
        default: True
        required: false
    compose_type:
        description:
            - type of compose
        type: str
        default: "edge-commit"
        required: false
        choices:
            - ami
            - edge-commit
            - edge-container
            - edge-installer
            - edge-raw-image
            - edge-simplified-installer
            - image-installer
            - oci
            - openstack
            - ova
            - qcow2
            - tar
            - vhd
            - vmdk
            - iot-commit
            - iot-container
            - iot-installer
            - iot-raw-image
            - container
    ostree_ref:
        description:
            - ostree ref
        type: str
        default: ""
        required: false
    ostree_parent:
        description:
            - ostree parent
        type: str
        default: ""
        required: false
    ostree_url:
        description:
            - ostree URL
        type: str
        default: ""
        required: false
    timeout:
        description:
            - timeout for osbuild-compose requests, in seconds
        type: int
        default: 120
        required: false
notes:
    - THIS MODULE IS NOT IDEMPOTENT UNLESS C(allow_duplicate) is set to C(false)
    - The params C(profile) and C(image_name) are required together.
    - The C(profile) option is not fully implemented at this time.
"""

EXAMPLES = """
- name: Start ostree compose size 4096
  infra.osbuild.start_compose:
    blueprint: rhel-for-edge-demo
    image_name: testimage
    size: 4096

- name: Start ostree compose with idempotent transaction
  infra.osbuild.start_compose:
    blueprint: rhel-for-edge-demo
    allow_duplicate: false
"""
import json  # noqa E402
import socket
from typing import Any  # noqa E402

from ansible.module_utils.basic import AnsibleModule  # noqa E402
from ansible_collections.infra.osbuild.plugins.module_utils.weldr import Weldr  # noqa E402

argument_spec = dict(
    blueprint=dict(type="str", required=True),
    size=dict(type="int", required=False, default=0),
    profile=dict(type="str", required=False, default=""),
    image_name=dict(type="str", required=False, default=""),
    allow_duplicate=dict(type="bool", required=False, default=True),
    compose_type=dict(
        type="str",
        required=False,
        default="edge-commit",
        choices=[
            "ami",
            "edge-commit",
            "edge-container",
            "edge-installer",
            "edge-raw-image",
            "edge-simplified-installer",
            "image-installer",
            "oci",
            "openstack",
            "ova",
            "qcow2",
            "tar",
            "vhd",
            "vmdk",
            "iot-commit",
            "iot-container",
            "iot-installer",
            "iot-raw-image",
            "container",
        ],
    ),
    ostree_ref=dict(type="str", required=False, default=""),
    ostree_parent=dict(type="str", required=False, default=""),
    ostree_url=dict(type="str", required=False, default=""),
    timeout=dict(type="int", required=False, default=120),
)


def start_compose(module, weldr):
    changed: bool = False
    dupe_compose: list = []
    blueprint_info: dict = weldr.api.get_blueprints_info(module.params["blueprint"])
    blueprint_version: int = blueprint_info["blueprints"][0]["version"]

    # Add check if compose_type is supported
    supported_compose_type: dict = weldr.api.get_compose_types()

    is_supported: dict = next((item for item in supported_compose_type["types"] if item["name"] == module.params["compose_type"]), {})

    if not is_supported:
        module.fail_json(
            msg="%s is not a valid image type, valid types are: %s"
            % (module.params["compose_type"], [[v for k, v in t.items() if k == "name"] for t in supported_compose_type["types"]]),
            changed=changed
        )
    else:
        if not is_supported["enabled"]:
            module.fail_json(
                msg="%s is not a supported image type, supported image types are: %s"
                % (module.params["compose_type"], [[v for k, v in t.items() if k == "enabled" and v is True] for t in supported_compose_type["types"]]),
                changed=changed
            )

    if not module.params["allow_duplicate"]:
        # only do all this query and filtering if needed

        compose_queue: dict = weldr.api.get_compose_queue()
        # {"new":[],"run":[{"id":"930a1584-8737-4b61-ba77-582780f0ff2d","blueprint":"base-image-with-tmux","version":"0.0.5","compose_type":"edge-commit","image_size":0,"queue_status":"RUNNING","job_created":1654620015.4107578,"job_started":1654620015.415151}]}

        compose_queue_run_dupe: list = [
            compose for compose in compose_queue["run"] if (compose["blueprint"] == module.params["blueprint"]) and (compose["version"] == blueprint_version)
        ]
        compose_queue_new_dupe: list = [
            compose for compose in compose_queue["new"] if (compose["blueprint"] == module.params["blueprint"]) and (compose["version"] == blueprint_version)
        ]

        compose_finished: dict = weldr.api.get_compose_finished()
        # {"finished":[{"id":"930a1584-8737-4b61-ba77-582780f0ff2d","blueprint":"base-image-with-tmux","version":"0.0.5","compose_type":"edge-commit","image_size":8192,"queue_status":"FINISHED","job_created":1654620015.4107578,"job_started":1654620015.415151,"job_finished":1654620302.9069786}]}
        compose_finished_dupe: list = [
            compose
            for compose in compose_finished["finished"]
            if (compose["blueprint"] == module.params["blueprint"]) and (compose["version"] == blueprint_version)
        ]

        compose_failed: dict = weldr.api.get_compose_failed()
        # {"failed":[]}
        compose_failed_dupe: list = [
            compose
            for compose in compose_failed["failed"]
            if (compose["blueprint"] == module.params["blueprint"]) and (compose["version"] == blueprint_version)
        ]

        dupe_compose: list = compose_queue_run_dupe + compose_queue_new_dupe + compose_failed_dupe + compose_finished_dupe

    if module.params["allow_duplicate"] or (len(dupe_compose) == 0):
        # FIXME - build to POST payload and POST that ish
        compose_settings: dict[str, Any] = {
            "blueprint_name": module.params["blueprint"],
            "compose_type": module.params["compose_type"],
            "branch": "master",
            "size": module.params["size"],
        }

        if module.params["compose_type"] in ["installer", "raw", "edge-commit", "edge-container"]:
            compose_settings["ostree"] = {
                "ref": module.params["ostree_ref"],
                "parent": module.params["ostree_parent"],
                "url": module.params["ostree_url"],
            }

        try:
            result: dict = weldr.api.post_compose(json.dumps(compose_settings), timeout=module.params["timeout"])
        except socket.timeout:
            # it's possible we don't get a response back from weldr because on the
            # very first run including a new content source composer will build a repo cache
            # and when that happens we get an empty JSON response

            compose_queue: dict = weldr.api.get_compose_queue()
            # {"new":[],"run":[{"id":"930a1584-8737-4b61-ba77-582780f0ff2d","blueprint":"base-image-with-tmux","version":"0.0.5","compose_type":"edge-commit","image_size":0,"queue_status":"RUNNING","job_created":1654620015.4107578,"job_started":1654620015.415151}]}

            submitted_compose_uuid: str = ""

            submitted_compose_found_run: list[dict[str, str]] = [
                compose
                for compose in compose_queue["run"]
                if (compose["blueprint"] == module.params["blueprint"]) and (compose["version"] == blueprint_version)
            ]
            if submitted_compose_found_run:
                # we expect it to be RUNNING, so check that first
                submitted_compose_uuid: str = submitted_compose_found_run[0]["id"]
            else:
                # didn't find it running, check for NEW queue status
                submitted_compose_found_new: list = [
                    compose
                    for compose in compose_queue["new"]
                    if (compose["blueprint"] == module.params["blueprint"]) and (compose["version"] == blueprint_version)
                ]

                if submitted_compose_found_new:
                    submitted_compose_uuid: str = submitted_compose_found_new[0]["id"]

                else:
                    # it's not RUNNING and not NEW, so check for FAILURE state
                    compose_failed: dict = weldr.api.get_compose_failed()
                    # {"failed":[]}
                    submitted_compose_found_failed: list = [
                        compose
                        for compose in compose_failed["failed"]
                        if (compose["blueprint"] == module.params["blueprint"]) and (compose["version"] == blueprint_version)
                    ]
                    if submitted_compose_found_failed:
                        submitted_compose_uuid: str = submitted_compose_found_failed[0]["id"]
                    else:
                        module.fail_json(
                            msg="Unable to determine state of build, check osbuild-composer system logs. Also, consider increasing the request timeout",
                            changed=changed
                        )

            if submitted_compose_uuid:
                result: dict = weldr.api.get_compose_status(submitted_compose_uuid)
                result['body'] = {
                    'build_id': submitted_compose_uuid
                }

        if "status_code" in result.keys():
            if result["status_code"] >= 400:
                module.fail_json(
                    msg="Compose returned body: {0}, msg {1}, and status_code {2}".format(result["body"], result["error_msg"], result["status_code"]),
                    changed=changed
                )

        # Having received a non-400+ response, we know a compose has started
        changed: bool = True

        compose_output_types: dict[str, list[str]] = {
            "tar": ["tar", "edge-commit", "iot-commit", "edge-container", "iot-container", "container"],
            "iso": ["edge-installer", "edge-simplified-installer", "iot-installer", "image-installer"],
            "ova": ["ova"],
            "qcow2": ["qcow2", "openstack", "oci"],
            "vmdk": ["vmdk"],
            "vhd": ["vhd"],
            "raw.xz": ["edge-raw-image", "iot-raw-image"],
            "ami": ["ami"],
        }

        output_type: str = ""
        for compose_type, compose_type_list in compose_output_types.items():
            if module.params["compose_type"] in compose_type_list:
                output_type: str = compose_type
        result["output_type"] = output_type

        module.exit_json(msg="Compose submitted to queue", result=result, changed=changed)

    else:
        changed: bool = False
        module.exit_json(
            msg="Not queuing a duplicate versioned compose without allow_duplicate set to true",
            changed=changed,
        )


def main() -> None:
    module: AnsibleModule = AnsibleModule(
        argument_spec=argument_spec,
        required_together=[["image_name", "profile"]],
        required_if=[
            ["compose_type", "edge-installer", ["ostree_url"]],
            ["compose_type", "iot-installer", ["ostree_url"]],
        ],
    )
    weldr: Weldr = Weldr(module)
    start_compose(module, weldr)


if __name__ == "__main__":
    main()
