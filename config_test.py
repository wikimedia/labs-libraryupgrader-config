"""
Copyright (C) 2019-2020 Kunal Mehta <legoktm@member.fsf.org>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
from collections import OrderedDict
import json
import pytest


def test_releases():
    with open('releases.json') as f:
        releases = json.load(f)

    assert isinstance(releases, dict)

    # Basic sanity check
    assert isinstance(releases['version'], int)
    assert releases['push'] in (True, False)

    # Stuff we expect in master
    assert 'composer' in releases['master']
    assert 'npm' in releases['master']

    # Required keys
    for branch in releases:
        if branch in ('version', 'push'):
            continue
        for manager, updates in releases[branch].items():
            for name, info in updates.items():
                assert 'to' in info
                assert 'weight' in info


def test_repositories():
    with open('repositories.json') as f:
        repositories = json.load(f)

    assert isinstance(repositories, dict)

    # Sanity check
    assert 'canaries' in repositories
    assert 'repositories' in repositories


@pytest.mark.parametrize('fname', ['releases.json', 'repositories.json'])
def test_formatting(fname):
    with open(fname) as f:
        raw = f.read()
    data = json.loads(raw, object_pairs_hook=OrderedDict)
    expected = json.dumps(data, indent='    ') + '\n'
    assert expected == raw
