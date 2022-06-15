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
    workdir:
        description:
            - A working directory to expand the ISO into
        type: str
        required: true
    version:
        description:
            - RHEL version to validate the kickstart against, styled as "RHEL8", "RHEL9", etc
        type: str
        required: false
        default: "RHEL8"
        choices: ["RHEL8","RHEL9"]

requires:
- coreutils-single
- glibc-minimal-langpack
- pykickstart
- mtools
- xorriso
- genisoimage
- syslinux
- isomd5sum
- lorax
"""

EXAMPLES = """
- name: inject kickstart into ISO
  osbuild.composer.inject_ks:
    kickstart: "/tmp/mykickstart.ks"
    src_iso: "/tmp/previously_composed.iso"
    dest_iso: "/tmp/with_my_kickstart.iso"
    workdir: "/root/edgeiso/
"""


import os
import traceback

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils._text import to_native, to_text
from ansible.module_utils.common.locale import get_best_parsable_locale

import os
import shutil

def run_cmd(module, cmd_list):

    # get local for shelling out
    locale = get_best_parsable_locale(module)
    lang_env = dict(LANG=locale, LC_ALL=locale, LC_MESSAGES=locale)

    rc, out, err = module.run_command(cmd_list, environ_update=lang_env)
    if (rc != 0) or err:
        module.fail_json("ERROR: Command '%s' failed with return code: %s and error message, '%s'" % (' '.join(cmd_list), rc, err))

    return out

def main():

    arg_spec=dict(
        kickstart=dict(type="str", required=True),
        src_iso=dict(type="str", required=True),
        dest_iso=dict(type="str", required=True),
        workdir=dict(type="str", required=True),
        version=dict(type="str", required=False, default="RHEL8", choices=['RHEL8', 'RHEL9']),
    )

    module = AnsibleModule(
        argument_spec=arg_spec,
    )

    # Sanity checking the paths exist
    for key in arg_spec:
        if key in ["kickstart", "src_iso", "workdir"]:
            if not os.path.exists(module.params[key]):
                module.fail_json("No such file found: %s" % fname)

    # define paths to things we need
    isolinux_config = os.path.join(module.params['workdir'], '/isolinux/isolinux.cfg')
    efi_grub_config = os.path.join(module.params['workdir'], '/EFI/BOOT/grub.cfg')
    efi_dir = os.path.join(module.params['workdir'], '/EFI/BOOT')
    efiboot_imagepath = os.path.join(module.params['workdir'], '/images/efiboot.img')

    # get binary paths
    ksvalidator = module.get_bin_path('ksvalidator')
    isoinfo = module.get_bin_path('isoinfo')
    xorriso = module.get_bin_path('xorriso')
    mtype = module.get_bin_path('mtype')
    mcopy = module.get_bin_path('mcopy')
    mkefiboot = module.get_bin_path('mkefiboot')
    genisoimage = module.get_bin_path('genisoimage')
    isohybrid = module.get_bin_path('isohybrid')
    implantisomd5 = module.get_bin_path('implantisomd5')
    sed = module.get_bin_path('sed')

    # validate the kickstart
    ksvalidator_cmd = [
        ksvalidator, '-v', module.params['version'], module.params['kickstart']
    ]
    ksvalidator_out = run_cmd(module, ksvalidator_cmd)

    # get ISO volume id
    isovolid_cmd = [isoinfo, '-d', '-i', module.params['src_iso']]
    isovolid_out = run_cmd(module, isovolid_cmd)
    try:
        isovolid = [
            line for line in isovolid_out.split('\n') if "Volume id:" in line
        ][0].split(':')[-1].strip()
    except IndexError as e:
        module.fail_json(
            msg="ERROR: Unable to find Volume ID for source ISO: %s" % module.params['src_iso']
        )

    # explode the ISO
    xorriso_cmd = [xorriso, '-osirrox', 'on', '-indev', module.params['src_iso'], '-extract', '/', module.params['workdir']]
    xorriso_out = run_cmd(module, xorriso_cmd)

    # insert kickstart
    shutil.copy(
        module.params['kickstart'],
        os.path.join(module.params['workdir'], module.params['kickstart']),
    )

    # FIXME - do this more cleanly than sed 
    # edit isolinux

    # Remove an existing inst.ks instruction
    sed_cmd = [
        sed, "-i", r"/rescue/n;/LABEL=%s/ s/\<inst.ks[^ ]*//g" % isovolid, isolinux_config
    ]
    sed_cmd_out = run_cmd(module, sed_cmd)

    # Replace an existing inst.ks instruction
    sed_cmd = [
        sed, "-i", 
        r"/rescue/n;/LABEL=%s/ s/\<inst.ks[^ ]*/inst.ks=hd:LABEL=%s:\/%s None/g" % (
            isovolid, isovolid, module.params['kickstart']
        ),
        isolinux_config
    ]
    sed_cmd_out = run_cmd(module, sed_cmd)

    # Inject an inst.ks instruction
    sed_cmd = [
        sed, "-i",
        r"/inst.ks=/n;/rescue/n;/LABEL=%s/ s/$/ inst.ks=hd:LABEL=%s:\/%s None/g" % (
            isovolid, isovolid, module.params['kickstart']
        ),
        isolinux_config
    ]
    sed_cmd_out = run_cmd(module, sed_cmd)

    # FIXME - do this more cleanly than sed 
    # edit efiboot

    # Remove an existing inst.ks instruction
    sed_cmd = [
        sed, "-i",
        r"/rescue/n;/LABEL=%s/ s/\<inst.ks[^ ]*//g" % isovolid,
        efi_grub_config
    ]
    sed_cmd_out = run_cmd(module, sed_cmd)

    # Replace an existing inst.ks instruction
    sed_cmd = [
        sed, "-i",
        r"/rescue/n;/LABEL=%s/ s/\<inst.ks[^ ]*/inst.ks=hd:LABEL=%s:\/%s None/g" % (
            isovolid, isovolid, module.params['kickstart']),
        efi_grub_config
    ]
    sed_cmd_out = run_cmd(module, sed_cmd)

    # Inject an inst.ks instruction
    sed_cmd = [
        sed, "-i",
        r"/inst.ks=/n;/rescue/n;/LABEL=%s/ s/$/ inst.ks=hd:LABEL=%s:\/%s None/g" % (
            isovolid, isovolid, module.params['kickstart']),
        efi_grub_config
    ]
    sed_cmd_out = run_cmd(module, sed_cmd)

    # modify efiboot image
    mtype_cmd = [mtype, "-i", efiboot_imagepath, "::EFI/BOOT/grub.cfg"]
    mtype_out1 = run_cmd(module, mtype_cmd)

    mcopy_cmd = [
        mcopy, "-o", "-i", efiboot_imagepath, efi_grub_config, "::EFI/BOOT/grub.cfg"
    ]
    mcopy_out = run_cmd(module, mcopy_cmd)

    mtype_cmd = [mtype, "-i", efiboot_imagepath, "::EFI/BOOT/grub.cfg"]
    mtype_out2 = run_cmd(module, mtype_cmd)


    # make the new iso image
    genisoimage_cmd = [
        "genisoimage", "-o", module.params["dest_iso"], "-R", "-J", "-V",
        isovolid, "-A", isovolid, "-volset", isovolid, "-b",
        "isolinux/isolinux.bin", "-c", "isolinux/boot.cat", "-boot-load-size",
        "4", "-boot-info-table", "-no-emul-boot", "-verbose", "-debug",
        "-eltorito-alt-boot", "-e" "images/efiboot.img", "-no-emul-boot",
        module.params["workdir"]
    ]
    genisoimage_out = run_cmd(module, genisoimage_cmd)

    # make it bootable
    isohybrid_cmd = [isohybrid, "--uefi", module.params['dest_iso']]
    isohybrid_out = run_cmd(module, isohybrid_cmd)

    # implant md5 checksum
    implantisomd5_cmd = [implantisomd5, module.params['dest_iso']]
    implantisomd5_out = run_cmd(module, implantisomd5_cmd)


    module.exit_json(msg="New ISO can be found at: %s" % module.params['dest_iso'])


if __name__ == "__main__":
    main()
