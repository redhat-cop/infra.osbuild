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
module: add_source
short_description: Add source to add custom packages
description:
    - Add source to add custom packages to image
author:
    - Matthew Sandoval (@matoval)
options:
    repo_name:
        description:
            - Name of the source
        type: str
        required: true
    base_url:
        description:
            - Base url of the source
        type: str
        required: true
    type:
        description:
            - Url type, options are: yum-baseurl, yum-mirrorlist, yum-metalink
        type: str
        required: true
    check_ssl:
        description:
            - Check if the https certificates are valid
        type: bool
        required: true
    check_gpg:
        description:
            - Check that the gpg keys match
        type: bool
        required: true
    gpgkey_urls:
        description:
            - List of gpg key urls
        type: list
        required: false
"""

EXAMPLES = """
- name: Add source for custom packages
  osbuild.composer.add_source:
    repo_name: Everything
    base_url: https://dl.fedoraproject.org/pub/epel/9/Everything/x86_64/
    type: yum-baseurl
    check_ssl: false
    check_gpg: false
"""

import re
import time
import json

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils._text import to_native, to_text, to_bytes
from ansible_collections.osbuild.composer.plugins.module_utils.weldr import Weldr


def main():
    module = AnsibleModule(
        argument_spec=dict(
            repo_name=dict(type="str", required=True),
            base_url=dict(type="str", required=True),
            type=dict(type="str", required=True),
            check_ssl=dict(type="bool", required=True),
            check_gpg=dict(type="bool", required=True),
            gpgkey_urls=dict(type="list", required=False),
        ),
    )

    weldr = Weldr(module)

    new_source = {}
    new_source["name"] = module.params["repo_name"]
    new_source["url"] = module.params["base_url"]
    new_source["type"] = module.params["type"]
    new_source["check_ssl"] = bool(module.params["check_ssl"])
    new_source["check_gpg"] = bool(module.params["check_gpg"])

    if module.params["gpgkey_urls"]:
        gpgkeys = []
        for url in module.params["gpgkey_urls"]:
            gpgkeys.append(url)
        new_source["gpgkey_urls"] = gpgkeys

    results = weldr.api.post_projects_source_new(json.dumps(new_source))

    module.exit_json(results=results, msg="New source add to osbuild composer")


if __name__ == "__main__":
    main()
