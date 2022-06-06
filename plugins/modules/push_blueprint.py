#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: Red Hat Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
from ansible_collections.osbuild.composer.plugins.module_utils.weldr import Weldr

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
requirements:
  - composer-cli
options:
    path:
        description:
            - Path to blueprint toml file on osbuild system that should be pushed into composer
        type: str
        default: ""
        required: true
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


def main():
    module = AnsibleModule(
        argument_spec=dict(
            path=dict(type="str", required=True),
        ),
    )


    weldr = Weldr(module)
    try:


    except Exception as e:
        module.fail_json(msg=to_native(e), exception=traceback.format_exc())


if __name__ == "__main__":
    main()
