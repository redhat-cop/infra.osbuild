#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: Red Hat Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

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

from ansible.module_utils.basic import AnsibleModule  # noqa E402

import os  # noqa E402
import configparser  # noqa E402

argument_spec = dict(
    repos=dict(type="list", required=True, elements="str", no_log=False),
)


def rhsm_repo_info(module):
    rhsm_info = []
    has_changed: bool = False
    for repo in module.params["repos"]:
        items = {}
        for file in os.listdir("/etc/yum.repos.d/"):
            confp = configparser.ConfigParser()
            confp.read_file(open("/etc/yum.repos.d/%s" % file))
            if confp.has_section(repo):
                items = dict(confp.items(repo))
                rhsm_info.append(
                    {
                        "name": repo,
                        "base_url": items["baseurl"] if "baseurl" in items else None,
                        "type": "yum-baseurl",
                        "check_ssl": items.get("sslverify") == "1",
                        "check_gpg": items.get("gpgcheck") == "1",
                        "gpgkey_paths": items["gpgkey"] if "gpgkey" in items else None,
                        "state": "present",
                    }
                )
        if not items:
            module.fail_json(msg="Could not find %s in the files inside /etc/yum.repos.d/ directory. Error: %s" % (repo, Exception))

    module.exit_json(changed=has_changed, rhsm_info=rhsm_info)


def main() -> None:
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    rhsm_repo_info(module=module)


if __name__ == "__main__":
    main()
