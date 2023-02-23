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
module: inject_ks
short_description: Inject Kickstart into composed ISO image.
description:
    - Inject Kickstart into composed ISO image.
author:
- Adam Miller (@maxamillion)
- Matthew Sandoval (@matoval)

options:
    kickstart:
        description:
            - Path to kickstart file
        type: str
        required: true
    src_iso:
        description:
            - Path to ISO file that will be used as source to create new ISO with kickstart injected
        type: str
        required: true
    dest_iso:
        description:
            - Path the ISO file with kickstart injected into it should be in
        type: str
        required: true

"""

EXAMPLES = """
- name: inject kickstart into ISO
  infra.osbuild.inject_ks:
    kickstart: "/tmp/mykickstart.ks"
    src_iso: "/tmp/previously_composed.iso"
    dest_iso: "/tmp/with_my_kickstart.iso"
"""

import os

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common.locale import get_best_parsable_locale

import os


def main():

    arg_spec = dict(
        kickstart=dict(type="str", required=True),
        src_iso=dict(type="str", required=True),
        dest_iso=dict(type="str", required=True),
    )

    module = AnsibleModule(
        argument_spec=arg_spec,
    )

    # Sanity checking the paths exist
    for key in arg_spec:
        if key in ["kickstart", "src_iso", "workdir"]:
            if not os.path.exists(module.params[key]):
                module.fail_json("No such file found: %s" % module.params[key])

    # get local for shelling out
    locale = get_best_parsable_locale(module)
    lang_env = dict(LANG=locale, LC_ALL=locale, LC_MESSAGES=locale)

    # Inject kickstart file to iso
    cmd_list = ["mkksiso", module.params["kickstart"], module.params["src_iso"], module.params["dest_iso"]]
    rc, out, err = module.run_command(cmd_list, environ_update=lang_env)
    if (rc != 0):
        module.fail_json(
            "ERROR: Command '%s' failed with return code: %s and error message, '%s'"
            % (" ".join(cmd_list), rc, err)
        )

    module.exit_json(changed=True, msg="Kickstart added to ISO: %s" % module.params["dest_iso"])


if __name__ == "__main__":
    main()
