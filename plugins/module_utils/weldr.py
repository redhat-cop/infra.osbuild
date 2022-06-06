# -*- coding: utf-8 -*-
#
# (c) 2022, Adam Miller (admiller@redhat.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from ansible.module_utils._text import to_bytes, to_native, to_text
from ansible_collections.osbuild.composer.plugins.module_utils.weldrapiv1 import WeldrV1
from ansible.module_utils.urls import Request

import json

class Weldr(object):
    """
    Weldr

    This is the base class for interacting with the weldr API over a local UNIX socket
    """

    def __init__(self, module, unix_socket="/run/weldr/api.socket"):
        """
        initializer 

        :module:          AnsibleModule, instance of AnsibleModule
        :unix_socket:     string, local UNIX Socket that Weldr service is listening on
        """

        self.module = module
        self.unix_socket = unix_socket
        self.request = Request(unix_socket=self.unix_socket)

        status = json.load(self.request.open('GET', 'http://localhost/api/status'))
        if status['api'] == "1":
            self.api = WeldrV1(self)
        else:
            module.fail_json(msg='Unsupported Weldr API found. Expected "1", got "%s"' % status['api'])

        # Because we can't have nice things
        try:
            try:
                import toml
                HAS_TOML = True
                self.toml = toml
            except ImportError:
                HAS_TOML = False

            if not HAS_TOML:
                try:
                    import pytoml as toml
                    HAS_TOML = True
                    self.toml = toml
                except ImportError:
                    HAS_TOML = False
            self.HAS_TOML = HAS_TOML
        except exception as e:
            self.module.fail_json(msg="Exception encountered during execution: %s" % to_text(e))

    def check_status(self):
        """
        check_status of local weldr

        """

    def blueprint_sanity_check(self):
        """
        blueprint_sanity_check
        """
        if not self.HAS_TOML:
            self.module.fail_json(msg='The python "pytom" or "toml" library is required for working with blueprints.')




