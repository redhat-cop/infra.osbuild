#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: Red Hat Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

ANSIBLE_METADATA = {
    "metadata_version": "1.1",
    "status": ["preview"],
    "supported_by": "community",
}

DOCUMENTATION = """
---
module: compose_status
short_description: Returns status of composes
description:
    - Returns status of composes
author:
    - Chris Edillon (@jce-redhat)
options:
    compose_types:
       description:
           - Get status of specific compose types
       type: list
       elements: sttr
       required: false
       choices: ["all", "waiting", "running", "finished", "failed"]
       default: ["all"]
"""

EXAMPLES = """
- name: Get status of all composes
  infra.osbuild.compose_status:
  register: all_composes

- name: Get list of failed or finished composes
  infra.osbuild.compose_status:
    compose_types:
      - failed
      - finished
  register: composes_to_delete
"""

RETURN = """
composes:
    description: Current status of existing composes
    returned: always
    type: dict
    sample: {
        "failed": [],
        "finished": [
            {
                "blueprint": "SimplifiedInstall",
                "compose_type": "edge-simplified-installer",
                "id": "03ef3c63-5977-4dc7-af6b-e760f3f9ecdb",
                "image_size": 10737418240,
                "job_created": 1678333520.3677824,
                "job_finished": 1678333735.0659246,
                "job_started": 1678333520.406152,
                "queue_status": "FINISHED",
                "version": "0.0.1"
            },
            {
                "blueprint": "Edge",
                "compose_type": "edge-container",
                "id": "60bc728c-2844-42ee-873f-4a07fc1213a1",
                "image_size": 0,
                "job_created": 1678333194.066046,
                "job_finished": 1678333492.0878892,
                "job_started": 1678333194.0752573,
                "queue_status": "FINISHED",
                "version": "0.0.1"
            }
        ],
        "running": [
            {
                "blueprint": "Edge",
                "compose_type": "edge-container",
                "id": "fb974e1d-aea8-43c9-b148-2b2a8e0500f1",
                "image_size": 0,
                "job_created": 1678377814.3328815,
                "job_started": 1678377814.343578,
                "queue_status": "RUNNING",
                "version": "0.0.2"
            }
        ],
        "waiting": []
    }
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.infra.osbuild.plugins.module_utils.weldr import Weldr


def main():
    module = AnsibleModule(
        argument_spec=dict(
            compose_types=dict(type="list", elements="str",
                required=False, default="all",
                choices=["all", "waiting", "running", "finished", "failed"]),
        ),
    )

    weldr: Weldr = Weldr(module)

    all_composes: dict = {}
    num_composes: int = 0

    if ("all" in module.params["compose_types"] or
            "finished" in module.params["compose_types"]):
        finished_composes: dict = weldr.api.get_compose_finished()
        all_composes.update(finished_composes)
        num_composes += len(finished_composes["finished"])

    if ("all" in module.params["compose_types"] or
            "failed" in module.params["compose_types"]):
        failed_composes: dict = weldr.api.get_compose_failed()
        all_composes.update(failed_composes)
        num_composes += len(failed_composes["failed"])

    if ("all" in module.params["compose_types"] or
            "waiting" in module.params["compose_types"] or
            "running" in module.params["compose_types"]):
        queued_composes: dict = weldr.api.get_compose_queue()
        queued_composes["waiting"] = queued_composes.pop("new")
        queued_composes["running"] = queued_composes.pop("run")

        if "waiting" in module.params["compose_types"]:
            num_composes += len(queued_composes["waiting"])
            del queued_composes["running"]
        elif "running" in module.params["compose_types"]:
            num_composes += len(queued_composes["running"])
            del queued_composes["waiting"]
        else:
            num_composes += len(queued_composes["waiting"] +
                              queued_composes["running"])

        all_composes.update(queued_composes)

    module.exit_json(msg="Returned %s composes" % num_composes,
                     composes=all_composes)


if __name__ == "__main__":
    main()
