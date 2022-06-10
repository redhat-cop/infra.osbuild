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
module: wait_compose
short_description: Wait for a compose to complete
description:
    - Wait for a compose to complete
author:
    - Adam Miller (@maxamillion)
options:
    compose_id:
        description:
            - Compose UUID to wait for
        type: str
        default: ""
        required: true
    timeout:
        description:
            - Maximum number of seconds to wait.
        type: int
        default: 1800
        required: false
    query_frequency:
        description:
            - Number of seconds between checking build status
        type: int
        default: 20
        required: false
notes:
- if the compose fails, so will the task
"""

EXAMPLES = """
- name: Wait for compose to complete
  osbuild.composer.wait_compose
    compose_id: "1bb4cc77-828e-42a2-a3de-9517e99ea4e4"
    timeout: 3600
"""

import re
import time

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils._text import to_native, to_text
from ansible_collections.osbuild.composer.plugins.module_utils.weldr import Weldr


def main():
    module = AnsibleModule(
        argument_spec=dict(
            compose_id=dict(type="str", required=True),
            timeout=dict(type="int", required=False, default=1800),
            query_frequency=dict(type="int", required=False, default=20),
        ),
    )

    weldr = Weldr(module)

    timeout_time = time.time() + module.params['timeout']
    while time.time() < timeout_time:

        finished_composes = weldr.api.get_compose_finished()
        found_compose = [ compose for compose in finished_composes['finished'] if compose['id'] == module.params['compose_id']]
        if len(found_compose) > 0:
            module.exit_json(msg="Compose FINISHED", result=found_compose[0])

        failed_composes = weldr.api.get_compose_failed()
        found_compose = [ compose for compose in failed_composes['failed'] if compose['id'] == module.params['compose_id']]
        if len(found_compose) > 0:
            module.fail_json(msg="Compose FAILED", result=found_compose[0])

        time.sleep(module.params['query_frequency'])

    # FIXME - should this be a failure case?
    module.exit_json(msg="TIMEOUT REACHED", result={})


if __name__ == "__main__":
    main()
