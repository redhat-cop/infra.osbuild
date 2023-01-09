# -*- coding: utf-8 -*-
#
# (c) 2022, Adam Miller (admiller@redhat.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from ansible.module_utils._text import to_bytes, to_native, to_text
from ansible_collections.infra.osbuild.plugins.module_utils.weldrapiv1 import WeldrV1
import ansible.module_utils.six.moves.urllib.error as urllib_error
from ansible.module_utils.urls import Request
from ansible.module_utils.urls import fetch_url

import json
import os
import tempfile


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
        self.request = Request(unix_socket=self.unix_socket, timeout=120)
        try:
            status = json.load(self.request.open("GET", "http://localhost/api/status"))
            if status["api"] == "1":
                self.api = WeldrV1(self)
            else:
                module.fail_json(
                    msg='Unsupported Weldr API found. Expected "1", got "%s"'
                    % status["api"]
                )
        except (ConnectionRefusedError, OSError, urllib_error.URLError):
            module.fail_json(
                msg="Connection to osbuild-composer service failed, please ensure service is running"
            )
        except Exception as e:
            module.fail_json(msg=to_text(e))

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
        except Exception as e:
            self.module.fail_json(
                msg="Exception encountered during execution: %s" % to_text(e)
            )

    def blueprint_sanity_check(self):
        """
        blueprint_sanity_check
        """
        if not self.HAS_TOML:
            self.module.fail_json(
                msg='The python "pytom" or "toml" library is required for working with blueprints.'
            )

    def fetch_file(
        self,
        module,
        url,
        data=None,
        headers=None,
        method=None,
        use_proxy=True,
        force=False,
        last_mod_time=None,
        timeout=10,
        unredirected_headers=None,
        unix_socket=None,
    ):
        """

        NOTE: This is an unix_socket patched version of ansible.module_utils.urls.fetch_file
              and will be removed in the future once this PR has shipped GA:
                https://github.com/ansible/ansible/pull/78143

        Download and save a file via HTTP(S) or FTP (needs the module as parameter).
        This is basically a wrapper around fetch_url().

        :arg module: The AnsibleModule (used to get username, password etc. (s.b.).
        :arg url:             The url to use.

        :kwarg data:          The data to be sent (in case of POST/PUT).
        :kwarg headers:       A dict with the request headers.
        :kwarg method:        "POST", "PUT", etc.
        :kwarg boolean use_proxy:     Default: True
        :kwarg boolean force: If True: Do not get a cached copy (Default: False)
        :kwarg last_mod_time: Default: None
        :kwarg int timeout:   Default: 10
        :kwarg unredirected_headers: (optional) A list of headers to not attach on a redirected request

        :returns: A string, the path to the downloaded file.
        """
        # download file
        bufsize = 65536
        file_name, file_ext = os.path.splitext(str(url.rsplit("/", 1)[1]))
        fetch_temp_file = tempfile.NamedTemporaryFile(
            dir=module.tmpdir, prefix=file_name, suffix=file_ext, delete=False
        )
        module.add_cleanup_file(fetch_temp_file.name)
        try:
            rsp, info = fetch_url(
                module,
                url,
                data,
                headers,
                method,
                use_proxy,
                force,
                last_mod_time,
                timeout,
                unredirected_headers=unredirected_headers,
                unix_socket=unix_socket,
            )
            if not rsp:
                module.fail_json(msg="Failure downloading %s, %s" % (url, info["msg"]))
            data = rsp.read(bufsize)
            while data:
                fetch_temp_file.write(data)
                data = rsp.read(bufsize)
            fetch_temp_file.close()
        except Exception as e:
            module.fail_json(msg="Failure downloading %s, %s" % (url, to_native(e)))
        return fetch_temp_file.name
