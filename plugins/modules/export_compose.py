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
module: export_compose
short_description: Export successfully composed image from osbuild-composer service
description:
    - Export successfully composed image from osbuild-composer service
author:
    - Adam Miller (@maxamillion)
options:
    compose_id:
        description:
            - Compose UUID to export
        type: str
        required: true
    dest:
        description:
            - Destination file on the osbuild-composer machine to put the exported file
        type: str
        required: true
"""

EXAMPLES = """
- name: Export RHEL for Edge compose
  infra.osbuild.export_compose:
    compose_id: "1bb4cc77-828e-42a2-a3de-9517e99ea4e4"
    dest: "/tmp/mycompose_artifact.tar"

- name: Sync file from osbuild-composer system to my Ansbile control host
  ansible.posix.synchronize:
    mode: "pull"
    src: "/tmp/mycompose_artifact.tar"
    dest: "/usr/share/composes/mycompose_artifact.tar"
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.infra.osbuild.plugins.module_utils.weldr import Weldr


def main():
    changed: bool = False
    module = AnsibleModule(
        argument_spec=dict(
            compose_id=dict(type="str", required=True),
            dest=dict(type="str", required=True),
        ),
    )

    weldr = Weldr(module)

    filepath = weldr.api.get_compose_image(
        module.params["compose_id"],
        module.params["dest"],
        module.digest_from_file,
    )
    if filepath is not None:
        changed: bool = True

    module.exit_json(msg="Exported compose payload to %s" % module.params["dest"],
                     changed=changed)


if __name__ == "__main__":
    main()
