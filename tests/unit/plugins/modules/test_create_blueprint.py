# -*- coding: utf-8 -*-

# Copyright: Red Hat Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass = type

from unittest.mock import MagicMock

from .....plugins.modules.create_blueprint import create_blueprint
from .conftest import mock_weldr  # noqa

args = {
    "dest": "/tmp/blueprint.toml",
    "name": "test_blueprint",
    "description": "",
    "distro": "",
    "version_type": "patch",
    "packages": [],
    "groups": [],
    "customizations": {"user": "bob"}
}

module = MagicMock()
module.params = args


def test_create_blueprint(mock_weldr):
    create_blueprint(module, weldr=mock_weldr)
    file = open(args["dest"], "r")
    assert file.read() == 'name = "test_blueprint"\ndescription = "test_blueprint"\nversion = "0.0.2"\n\n[customizations]\nuser = "bob"\n'
