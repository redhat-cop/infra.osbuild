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
module: push_blueprint
short_description: Push a blueprint file into composer
description:
    - Push a blueprint file into composer
author:
- Adam Miller (@maxamillion)
options:
    path:
        description:
            - Path to blueprint toml file on osbuild system that should be pushed into composer
        type: str
        default: ""
        required: false
    blueprint:
        description:
            - Blueprint file data itself expressed as multiline string
        type: str
        default: ""
        required: false
notes:
- Requires one of: C(path), C(blueprint)
"""

EXAMPLES = """
- name: Push a blueprint
  osbuild.composer.push_blueprint:
    path: /tmp/blueprint.toml
"""


import os
import traceback

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils._text import to_native, to_text
from ansible_collections.osbuild.composer.plugins.module_utils.weldr import Weldr


def main():
    module = AnsibleModule(
        argument_spec=dict(
            path=dict(type="str", required=False),
            blueprint=dict(type="str", required=False),
        ),
        required_one_of=[["path", "blueprint"]],
    )

    weldr = Weldr(module)
    weldr.blueprint_sanity_check()

    if module.params["path"]:
        try:
            with open(module.params["path"], "rb") as fin:
                data = weldr.toml.load(fin)
        except FileNotFoundError:
            module.fail_json(
                msg="Unable to find or access blueprint file provided at path: %s"
                % module.params["path"]
            )

    if module.params["blueprint"]:
        data = weldr.toml.loads(module.params["blueprint"])

    results = weldr.api.post_blueprint_new(weldr.toml.dumps(data))
    module.exit_json(results=results, msg="Blueprint pushed to osbuild composer")


if __name__ == "__main__":
    main()
