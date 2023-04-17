# -*- coding: utf-8 -*-

# Copyright: Red Hat Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass = type

import pytest

from .....plugins.modules.create_blueprint import increment_version


@pytest.mark.parametrize('version,version_type,expected', [
    ('0.0.1', 'patch', '0.0.2'),
    ('0.0.1', 'minor', '0.1.1'),
    ('0.0.1', 'major', '1.0.1'),
])
def test_increment_version(version, version_type, expected):
    assert increment_version(version, version_type) == expected


@pytest.mark.parametrize('version,version_type,expected', [
    ('0.0', 'patch', 'not enough values to unpack*'),
    ('asdf', 'minor', 'Version contains non integer values'),
])
def test_increment_version_exception(version, version_type, expected):
    with pytest.raises(ValueError, match=expected):
        increment_version(version, version_type)
