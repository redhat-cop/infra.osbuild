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
options:
    path:
        description:
            - Path to kickstart file
        type: str
        required: true
    src:
        description:
            - Path to ISO file that will be used as source to create new ISO with kickstart injected
        type: str
        required: true
    dest:
        description:
            - Path the ISO file with kickstart injected into it should be in
        type: str
        required: true
    workdir:
        description:
            - A working directory to expand the ISO into
        type: str
        required: true
requires:
- coreutils-single
- glibc-minimal-langpack
- pykickstart
- mtools
- xorriso
- genisoimage
- syslinux
- isomd5sum
"""

EXAMPLES = """
- name: inject kickstart into ISO
  osbuild.composer.inject_ks:
    path: "/tmp/mykickstart.ks"
    src: "/tmp/previously_composed.iso"
    dest: "/tmp/with_my_kickstart.iso"
    workdir: "/root/edgeiso/
"""


import os
import traceback

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils._text import to_native, to_text
from ansible.module_utils.common.locale import get_best_parsable_locale

import os


def main():
    module = AnsibleModule(
        argument_spec=dict(
            path=dict(type="str", required=True),
            src=dict(type="str", required=True),
            dest=dict(type="str", required=True),
            workdir=dict(type="str", required=True),
        ),
    )

    locale = get_best_parsable_locale(module)
    lang_env = dict(LANG=locale, LC_ALL=locale, LC_MESSAGES=locale)

    isolinux_config = os.path.join(module.params['workdir'], '/isolinux/isolinux.cfg')
    efi_grub_config = os.path.join(module.params['workdir'], '/EFI/BOOT/grub.cfg')
    efi_dir = os.path.join(module.params['workdir'], '/EFI/BOOT')


    rc, out, err = module.run_command([], environ_update=lang_env)

    try:
        with open(module.params['dest'], 'w') as fd:
            fd.write()
    except Exception as e:
        module.fail_json(msg=f'Failed to write to file: {module.params["dest"]}', error=e)

    module.exit_json(msg=f'Blueprint file written to location: {module.params["dest"]}')


if __name__ == "__main__":
    main()
