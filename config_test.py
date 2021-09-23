"""
Copyright (C) 2019-2021 Kunal Mehta <legoktm@debian.org>

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
    with open("releases.json") as f:
        releases = json.load(f)

    assert isinstance(releases, dict)

    # Basic sanity check
    assert isinstance(releases["version"], int)
    assert releases["push"] in (True, False)

    # Stuff we expect in main
    assert "composer" in releases["main"]
    assert "npm" in releases["main"]

    # Required keys
    for branch in releases:
        if branch in ("version", "push"):
            continue
        for manager, updates in releases[branch].items():
            for name, info in updates.items():
                assert "to" in info
                assert "weight" in info


def test_repositories():
    with open("repositories.json") as f:
        repositories = json.load(f, object_pairs_hook=OrderedDict)

    assert isinstance(repositories, dict)

    assert repositories["canaries"] == \
           list(sorted(repositories["canaries"])), "canaries not sorted"

    sorted_repos = list(sorted(
        repositories["repositories"],
        # Things that end with * first, then by name
        key=lambda r: (not r.endswith("*"), r))
    )
    assert repositories["repositories"] == \
           sorted_repos, "repositories not sorted"


def test_monitoring():
    with open("monitoring.json") as f:
        monitoring = json.load(f, object_pairs_hook=OrderedDict)
    assert isinstance(monitoring["enabled"], bool)
    for name, info in monitoring["projects"].items():
        # name is set
        assert "name" in info
        # mode is a supported one:
        assert info["mode"] in ["release-monitoring"]
        assert isinstance(info["id"], int)
        # phab list is not empty
        assert info["phab"]
        for hashtag in info["phab"]:
            assert hashtag.startswith("#")
        for url in info["urls"]:
            assert url.startswith('https://')
    # Assert sorted
    assert list(monitoring["projects"]) == \
           list(sorted(monitoring["projects"])), "Projects not sorted"


@pytest.mark.parametrize(
    "fname", ["monitoring.json", "releases.json", "repositories.json"]
)
def test_formatting(fname):
    with open(fname) as f:
        raw = f.read()
    data = json.loads(raw, object_pairs_hook=OrderedDict)
    expected = json.dumps(data, indent="    ") + "\n"
    assert expected == raw
