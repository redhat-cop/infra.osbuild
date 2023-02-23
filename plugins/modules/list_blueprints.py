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
module: list_blueprints
short_description: Info module to get a list of blueprints from Weldr
description:
    - Info module to get a list of blueprints from Weldr
author:
- Adam Miller (@maxamillion)
"""

EXAMPLES = """
- name: Get list of blueprints
  infra.osbuild.list_blueprints:
  register: list_blueprints_out

- debug: var=list_blueprints
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.infra.osbuild.plugins.module_utils.weldr import Weldr


def main():
    module = AnsibleModule(
        argument_spec=dict(),
    )

    weldr = Weldr(module)

    results = weldr.api.get_blueprints_list()
    module.exit_json(
        blueprints=results["blueprints"],
        msg="Blueprints list available at 'blueprints' index of registered var.",
    )


if __name__ == "__main__":
    main()
