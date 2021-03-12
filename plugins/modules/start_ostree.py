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
module: start_ostree
short_description: Start an ostree compose
description:
    - Start an ostree compose
author:
    - Adam Miller (@maxamillion)
requirements:
    - composer-cli
options:
    blueprint:
        description:
            - Name of bluerprint to iniate a build for
        type: str
        default: ""
        required: true
    image_type:
        description:
            - Image output type
        type: str
        default: "rhel-edge-commit"
        required: false
    size:
        description:
            - Image size expressed in MiB
        type: int
        default: 8192
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
notes:
    - THIS MODULE IS NOT IDEMPOTENT BECAUSE COMPOSER DOES NOT MAINTAIN STATE
    - The params C('profile') and C('image_name') are required together.
"""

EXAMPLES = """
- name: Start ostree compose size 4096
  osbuild.composer.start_ostree
    blueprint: rhel-for-edge-demo
    image_name: testimage
    size: 4096
    profile: testprofile.toml

- name: Start ostree compose 
  osbuild.composer.start_ostree
    blueprint: rhel-for-edge-demo
"""

import re

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils._text import to_native, to_text


def main():
    module = AnsibleModule(
        argument_spec=dict(
            blueprint=dict(type="str", required=True),
            image_type=dict(type="str", required=False, default="rhel-edge-commit"),
            size=dict(type="int", required=False, default=8192),
            profile=dict(type="str", required=False, default=""),
            image_name=dict(type="str", required=False, default=""),
            required_together=(["image_name", "profile"],),
        ),
    )

    try:
        changed = False

        cmd = []
        cmd.append(module.get_bin_path("composer-cli"))
        cmd += ["compose", "start-ostree", "--size", modules.params["size"]]
        cmd += [module.params["image_type"], module.params["blueprint"]]
        if module.params["image_name"]:
            cmd += [module.params["image_name"], module.params["profile"]]

        rc, out, err = module.run_command(cmd)
        if rc == 0:
            changed = True
        else:
            module.fail_json(
                msg="Unknown error occurred.",
                stdout=out,
                stderr=err,
                rc=rc,
                uuid="",
                changed=changed,
            )

        recomp = re.compile(
            r"[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12}"
        )
        try:
            compose_uuid = recomp.search(out).group()
        except AttributeError:
            module.fail_json(
                msg="Unable to find uuid, an unknown error occurred",
                stdout=out,
                stderr=err,
                rc=rc,
                uuid="",
                changed=changed,
            )

        module.exit_json(
            msg="Compose %s placed in queue." % compose_uuid,
            uuid=compose_uuid,
            changed=changed,
            stdout=out,
            stderr=err,
            rc=rc,
        )

    except Exception as e:
        module.fail_json(msg=to_native(e), exception=traceback.format_exc())


if __name__ == "__main__":
    main()
