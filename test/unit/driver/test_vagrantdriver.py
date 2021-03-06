#  Copyright (c) 2015-2016 Cisco Systems
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#  THE SOFTWARE.

import pytest

from molecule import config
from molecule import core
from molecule import state
from molecule.driver import vagrantdriver

# TODO(retr0h): Test instance create/delete through the vagrant instance.


@pytest.fixture()
def molecule_instance(temp_files, state_path):
    c = temp_files(fixtures=['molecule_vagrant_config'])
    m = core.Molecule(dict())
    m.config = config.Config(configs=c)
    m._state = state.State(state_file=state_path)

    return m


@pytest.fixture()
def vagrant_instance(molecule_instance, request):
    return vagrantdriver.VagrantDriver(molecule_instance)


def test_name(vagrant_instance):
    assert 'vagrant' == vagrant_instance.name


def test_instances(vagrant_instance):
    assert 'aio-01' == vagrant_instance.instances[0]['name']


def test_default_provider(vagrant_instance):
    assert 'virtualbox' == vagrant_instance.default_provider


def test_default_platform(vagrant_instance):
    assert 'ubuntu' == vagrant_instance.default_platform


def test_provider(vagrant_instance):
    assert 'virtualbox' == vagrant_instance.provider


def test_platform(vagrant_instance):
    assert 'ubuntu' == vagrant_instance.platform


def test_platform_setter(vagrant_instance):
    vagrant_instance.platform = 'foo_platform'

    assert 'foo_platform' == vagrant_instance.platform


def test_valid_providers(vagrant_instance):
    expected = [{'type': 'virtualbox', 'name': 'virtualbox'}]

    assert expected == vagrant_instance.valid_providers


def test_valid_platforms(vagrant_instance):
    expected = [{'box': 'ubuntu/trusty64', 'name': 'ubuntu'}]

    assert expected == vagrant_instance.valid_platforms


def test_ssh_config_file(vagrant_instance):
    assert '.vagrant/ssh-config' == vagrant_instance.ssh_config_file


def test_ansible_connection_params(vagrant_instance):
    d = vagrant_instance.ansible_connection_params

    assert 'vagrant' == d['user']
    assert 'ssh' == d['connection']


def test_serverspec_args(vagrant_instance):
    assert {} == vagrant_instance.serverspec_args
