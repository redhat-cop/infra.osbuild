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
module: create_blueprint
short_description: Create a new blueprint file
description:
    - Create a new blueprint file
author:
- Adam Miller (@maxamillion)
options:
    dest:
        description:
            - Destination location on the remote Weldr host for the blueprint 
        type: str
        required: true
    name:
        description:
            - Name of blueprint, must not contain spaces
        type: str
        required: true
    description:
        description:
            - Long-form description of the blueprint
        type: str
        required: false
    version:
        description:
            - Semantic Versioned (https://semver.org/) version number
        type: str
        required: false
        default: "0.0.1"
    packages:
        description:
            - List of package names to add to the blueprint
        type: list
        default: []
        required: false
    groups:
        description:
            - List of package groups to add to the blueprint
        type: list
        default: []
        required: false
    customizations:
        description:
            - Dictionary of customizations
            - Please visit the follow URL for information on valid customizations and reference the Examples section of this document for guideance https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/8/html/composing_a_customized_rhel_system_image/creating-system-images-with-composer-command-line-interface_composing-a-customized-rhel-system-image#creating-a-composer-blueprint-with-command-line-interface_creating-system-images-with-composer-command-line-interface
        type: dict
        default: {}
        required: false
"""

EXAMPLES = """
- name: create blueprint on  host
  osbuild.composer.create_blueprint:
    dest: "/tmp/blueprint.toml"
    name: "my-rhel-edge-blueprint"
    version: "0.0.5"
    packages:
      - "vim-enhanced"
      - "ansible-core"
      - "git"
    customizations:
      kernel:
        append: "nomst=force"
      user:
        name: "bob"
        description: "Bob's a data scientist who like's map reduce"
        password: "PASSWORD-HASH"
        key: "PUBLIC-SSH-KEY"
        home: "/home/bob/"
        shell: "/usr/bin/bash"
        groups: '["users", "wheel"]'
"""


import os
import traceback

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils._text import to_native, to_text
from ansible_collections.osbuild.composer.plugins.module_utils.weldr import Weldr


def main():
    module = AnsibleModule(
        argument_spec=dict(
            dest=dict(type="str", required=True),
            name=dict(type="str", required=True),
            description=dict(type="str", required=False, default=""),
            version=dict(type="str", required=False, default="0.0.1"),
            packages=dict(type="list", required=False, default=[]),
            groups=dict(type="list", required=False, default=[]),
            customizations=dict(type="dict", required=False, default={}),
        ),
    )

    weldr = Weldr(module)
    if not module.params['description']:
        description = module.params['name']
    else:
        description = module.params['description']

    toml_file = (
        f'name = "{module.params["name"]}"\n'
        f'description = "{description}"\n'
        f'version = "{module.params["version"]}"\n'
        f'\n'
    )

    for package in module.params['packages']:
        toml_file += (
            f'[[packages]]\n'
            f'name = "{package}"\n'
            f'version = "*"\n'
            f'\n'
        )

    for group in module.params['groups']:
        toml_file += (
            f'[[groups]]\n'
            f'name = "{group}"\n'
            f'\n'
        )

    for key, customization in module.params['customizations'].items():
        toml_file += f'[[customizations.{key}]]\n'
        for k, v in customization.items():
            if v.startswith('['):
                toml_file += f'{k} = {v}\n'
            else:
                toml_file += f'{k} = "{v}"\n'

        toml_file += '\n'

    try:
        with open(module.params['dest'], 'w') as fd:
            fd.write(toml_file)
    except Exception as e:
        module.fail_json(msg=f'Failed to write to file: {module.params["dest"]}', error=e)

    module.exit_json(msg=f'Blueprint file written to location: {module.params["dest"]}')


if __name__ == "__main__":
    main()
