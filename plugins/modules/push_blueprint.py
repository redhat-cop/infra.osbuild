#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: Red Hat Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: push_blueprint
short_description: Push a blueprint file into composer
description:
    - Push a blueprint file into composer
author:
- Adam Miller (@maxamillion)
requirements:
  - composer-cli
options:
    path:
        description:
            - Path to blueprint toml file on osbuild system that should be pushed into composer
        type: str
        default: ""
        required: true
'''

EXAMPLES = '''
- name: Push a blueprint
  osbuild.composer.push_blueprint:
    path: /tmp/blueprint.toml
'''

RETURN = '''
msg:
    description: The command standard output
    returned: always
    type: str
    sample: 'No upgrade available.'
'''

import os
import traceback

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils._text import to_native, to_text




def main():
    module = AnsibleModule(
        argument_spec=dict(
            path=dict(type='str', required=True),
        ),
    )

    try:
        changed = False

        try:
            # get a version of the blueprint read in without whitespace for
            # comparison
            # 
            # also get the blueprint name
            with open(module.params['path']) as fd:
                candidate_bp = fd.read()
            cbp_lines = candidate_bp.split('\n')
            bp_name = [x for x in cbp_lines if 'name' in x][0].split()[-1].strip('\'"')

        except FileNotFoundError:
            module.fail_json("File not found at provided path: %s" % module.params['path'])

        cmd = []
        cmd.append(module.get_bin_path("composer-cli"))
        cmd += ['blueprints', 'show', bp_name]
        rc, out, err = module.run_command(cmd)
        if rc != 0:
            changed = True

        # We have to strip all whitespace because composer parses the toml, stores
        # the serialized data and then re-generates the toml for 'blueprints show'
        # and that doesn't preserve whitespace from the original file pushed in
        changed = not (
            [i for i in cbp_lines if i] == [i for i in out.split('\n') if i]
        )

        cmd = []
        cmd.append(module.get_bin_path("composer-cli"))
        cmd += ['blueprints', 'push', module.params['path']]
        rc, out, err = module.run_command(cmd)

        if rc != 0:
            module.fail_json(rc=rc, msg=err)

        module.exit_json(msg=out, changed=changed)

    except Exception as e:
        module.fail_json(msg=to_native(e), exception=traceback.format_exc())


if __name__ == '__main__':
    main()
