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
    src:
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
    - Requires one argument
"""

EXAMPLES = """
- name: Push a blueprint
  infra.osbuild.push_blueprint:
    src: /tmp/blueprint.toml
"""


import os
import traceback

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils._text import to_native, to_text
from ansible_collections.infra.osbuild.plugins.module_utils.weldr import Weldr


def main():
    module = AnsibleModule(
        argument_spec=dict(
            src=dict(type="str", required=False, default=""),
            blueprint=dict(type="str", required=False, default=""),
        ),
        required_one_of=[["src", "blueprint"]],
    )

    weldr = Weldr(module)
    weldr.blueprint_sanity_check()

    if module.params["src"]:
        try:
            with open(module.params["src"], "rb") as fin:
                # ### NOTE ###
                # python3-pytoml and python3-toml act differently and pytoml is
                # what's in RHEL8 but toml is in RHEL9 so we have to read and
                # then toml.loads(to_text(to_text_data) for compatibility with
                # both libraries.
                to_text_data = fin.read()
                data = weldr.toml.loads(to_text(to_text_data))
        except FileNotFoundError:
            module.fail_json(
                msg="Unable to find or access blueprint file provided at src: %s"
                % module.params["src"]
            )

    if module.params["blueprint"]:
        data = weldr.toml.loads(module.params["blueprint"])

    results = weldr.api.post_blueprint_new(weldr.toml.dumps(data))
    module.exit_json(results=results, msg="Blueprint pushed to osbuild composer")


if __name__ == "__main__":
    main()
