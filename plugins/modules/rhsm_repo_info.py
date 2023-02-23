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
module: rhsm_repo_info
short_description: Gather information about rhsm repositories
description:
    - Gather information about rhsm repositories
author:
    - Adam Miller (@maxamillion)
    - Matthew Sandoval (@matoval)
options:
    repos:
        description:
            - Name of rhsm repository
        type: list
        elements: str
        required: true
"""

EXAMPLES = """
- name: Add source for custom packages
  infra.osbuild.rhsm_repo_info:
    name:
     - rhocp-ironic-4.12-for-rhel-8-x86_64-rpms
  register: rhsm_repo_info_out

- name: Debug rhsm_repo_info_out
  ansible.builtin.debug:
    var: rhsm_repo_info_out
"""

from ansible.module_utils.basic import AnsibleModule

import os
import configparser


def main() -> None:
    module = AnsibleModule(
        argument_spec=dict(
            repos=dict(type="list", required=True, elements="str", no_log=False),
        ),
        supports_check_mode=True
    )

    rhsm_info = []
    has_changed: bool = False
    for file in os.listdir("/etc/yum.repos.d/"):
        confp = configparser.ConfigParser()
        confp.read_file(open("/etc/yum.repos.d/%s" % file))
        for repo in module.params["repos"]:
            try:
                items = dict(confp.items(repo))
                rhsm_info.append({
                    "name": repo,
                    "base_url": items["baseurl"],
                    "type": "yum-baseurl",
                    "check_ssl": True if items['sslverify'] == '1' else False,
                    "check_gpg": True if items['gpgcheck'] == '1' else False,
                    "gpgkey_paths": items['gpgkey'],
                    "state": 'present',
                })
                has_changed = True
            except Exception:
                module.fail_json("Could not find %s in file, /etc/yum.repos.d/redhat.repo. Error: %s" % (repo, Exception))

    module.exit_json(changed=has_changed, rhsm_info=rhsm_info)


if __name__ == "__main__":
    main()
