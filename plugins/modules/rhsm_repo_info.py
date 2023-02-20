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
module: rhsm_repo_info
short_description: Gather information about rhsm repositories
description:
    - Gather information about rhsm repositories
author:
    - Adam Miller (@maxamillion)
    - Matthew Sandoval (@matoval)
options:
"""

EXAMPLES = """
- name: Add source for custom packages
  infra.osbuild.rhsm_repo_info:
    name:
     - rhocp-ironic-4.12-for-rhel-8-x86_64-rpms
  register: rhsm_repo_info_out

- name: Debug rhsm_repo_info_out
  ansible.builtin.debug:
    var: rhsm_repo_info_out
"""

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils._text import to_native, to_text, to_bytes
from ansible_collections.infra.osbuild.plugins.module_utils.weldr import Weldr

import shutil
import configparser

def main() -> None:
    module = AnsibleModule(
        argument_spec=dict(
            name=dict(type="list", required=True),
        ),
    )


    results: dict = {}
    has_changed: bool = False



