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
module: get_all_finished_images
short_description: Returns all finished images
description:
    - Returns all finished images
author:
    - Matthew Sandoval (@matoval)
"""

EXAMPLES = """
- name: Get list of all created images
  infra.osbuild.get_all_finished_images:
  register: all_images
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.infra.osbuild.plugins.module_utils.weldr import Weldr


def main():
    module = AnsibleModule(
        argument_spec=dict(),
    )

    weldr = Weldr(module)

    all_images = weldr.api.get_compose_finished()

    module.exit_json(msg="Returned %s images" % len(all_images["finished"]), result=all_images)


if __name__ == "__main__":
    main()
