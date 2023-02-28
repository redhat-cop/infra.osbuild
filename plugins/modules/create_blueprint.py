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
- Chris Santiago (@resoluteCoder)
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
    distro:
        description:
            - Name of distribution, if left blank the distro is inferred from the build server
        type: str
        required: false
        choices: ["", "rhel-8", "rhel-9", "centos-8", "centos-9", "fedora-36", "fedora-37"]
        default: ""
    description:
        description:
            - Long-form description of the blueprint
        type: str
        required: false
        default: ""
    version_type:
        description:
            - Specify which version segment will be incremented.
            - Major will increment the first segment 1.0.0
            - Minor will increment the second segment 0.1.0
            - Patch will increment the last segment 0.0.1
            - For more information please visit https://semver.org/
        type: str
        required: false
        choices: ['major', 'minor', 'patch']
        default: "patch"
    packages:
        description:
            - List of package names to add to the blueprint
        type: list
        elements: str
        default: []
        required: false
    groups:
        description:
            - List of package groups to add to the blueprint
        type: list
        elements: str
        default: []
        required: false
    customizations:
        description:
            - Dictionary of customizations
            - Please visit the following URL for information on valid customizations and reference the Examples section of this document for guideance https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/8/html/composing_a_customized_rhel_system_image/creating-system-images-with-composer-command-line-interface_composing-a-customized-rhel-system-image#creating-a-composer-blueprint-with-command-line-interface_creating-system-images-with-composer-command-line-interface
        type: dict
        default: {}
        required: false
notes:
    - The C(distro) field will default to the distro of the builder server
      the build is executed on. If any other distro is defined than the same
      one that the builder server is running then that configuration must
      be provided in C(/etc/osbuild-composer/repositories/).
"""

EXAMPLES = """
- name: create blueprint on  host
  infra.osbuild.create_blueprint:
    dest: "/tmp/blueprint.toml"
    name: "my-rhel-edge-blueprint"
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

from ansible.module_utils._text import to_native, to_text
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.infra.osbuild.plugins.module_utils.weldr import Weldr


def increment_version(version: str, version_type: str) -> str:
    major, minor, patch = version.split('.')
    if version_type == 'major':
        return f'{int(major) + 1}.{minor}.{patch}'
    if version_type == 'minor':
        return f'{major}.{int(minor) + 1}.{patch}'
    return f'{major}.{minor}.{int(patch) + 1}'


def main() -> None:
    module: AnsibleModule = AnsibleModule(
        argument_spec=dict(
            dest=dict(type="str", required=True),
            name=dict(type="str", required=True),
            description=dict(type="str", required=False, default=""),
            distro=dict(type="str", required=False, default="", choices=['', 'rhel-8', 'rhel-9', 'centos-8', 'centos-9', 'fedora-36', 'fedora-37']),
            version_type=dict(type="str", required=False, default="patch", choices=['major', 'minor', 'patch']),
            packages=dict(type="list", required=False, elements="str", default=[]),
            groups=dict(type="list", required=False, elements="str", default=[]),
            customizations=dict(type="dict", required=False, default={}),
        ),
    )
    weldr: Weldr = Weldr(module)

    if not module.params["description"]:
        description: str = module.params["name"]
    else:
        description: str = module.params["description"]

    toml_data: dict = {
        "name": f"{module.params['name']}",
        "description": f"{description}"
    }
    if module.params["distro"]:
        toml_data["distro"]: str = f"{module.params['distro']}"

    blueprint_version = ""
    try:
        blueprint_version: str = '0.0.1'
        blueprint_exists: bool = True
        results: dict = weldr.api.get_blueprints_info(module.params['name'])
        for error in results['errors']:
            if error['id'] == 'UnknownBlueprint':
                blueprint_exists: bool = False

        if blueprint_exists:
            current_version: str = results['blueprints'][0]['version']
            blueprint_version: str = increment_version(current_version, module.params['version_type'])

        toml_data["version"]: str = f"{blueprint_version}"
    except Exception as e:
        module.fail_json(msg=f'Error: {e}. OSbuild composer service is unavailable')

    if module.params["packages"]:
        toml_data["packages"]: list = []
        for package in module.params["packages"]:
            toml_data["packages"].append({"name": f"{package}", "version": "*"})

    if module.params["groups"]:
        toml_data["groups"]: list = []
        for group in module.params["groups"]:
            toml_data["groups"].append({"name": f"{group}"})

    toml_data["customizations"]: dict = {}
    for key, customization in module.params["customizations"].items():

        if isinstance(customization, str):
            toml_data["customizations"][key]: str = customization
            continue

        # TODO since the module dict can only contain one of each key,
        # multiple users, filesystem definitions, etc. can't be done yet
        double_square_brackets: list = ["user", "filesystem", "sshkey"]
        if key in double_square_brackets:
            toml_data["customizations"][key]: list = []
            toml_data["customizations"][key].append(customization)
        else:
            toml_data["customizations"][key]: dict = customization

    try:
        with open(module.params["dest"], "w") as fd:
            weldr.toml.dump(toml_data, fd)
    except Exception as e:
        module.fail_json(
            msg=f'Failed to write to file: {module.params["dest"]}', error=e
        )

    module.exit_json(
        msg=f'Blueprint file written to location: {module.params["dest"]}',
        changed=True,
        current_version=blueprint_version
    )


if __name__ == "__main__":
    main()
