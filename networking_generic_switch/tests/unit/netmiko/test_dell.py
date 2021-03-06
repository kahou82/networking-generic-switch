# Copyright 2016 Mirantis, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import mock

from networking_generic_switch.devices.netmiko_devices import dell
from networking_generic_switch.tests.unit.netmiko import test_netmiko_base


class TestNetmikoDellNos(test_netmiko_base.NetmikoSwitchTestBase):

    def _make_switch_device(self):
        device_cfg = {'device_type': 'netmiko_dell_force10'}
        return dell.DellNos(device_cfg)

    @mock.patch('networking_generic_switch.devices.netmiko_devices.'
                'NetmikoSwitch.send_commands_to_device')
    def test_add_network(self, m_exec):
        self.switch.add_network(33, '0ae071f5-5be9-43e4-80ea-e41fefe85b21')
        m_exec.assert_called_with(
            ['interface vlan 33', 'name 0ae071f55be943e480eae41fefe85b21'])

    @mock.patch('networking_generic_switch.devices.netmiko_devices.'
                'NetmikoSwitch.send_commands_to_device')
    def test_del_network(self, mock_exec):
        self.switch.del_network(33)
        mock_exec.assert_called_with(['no interface vlan 33'])

    @mock.patch('networking_generic_switch.devices.netmiko_devices.'
                'NetmikoSwitch.send_commands_to_device')
    def test_plug_port_to_network(self, mock_exec):
        self.switch.plug_port_to_network(3333, 33)
        mock_exec.assert_called_with(
            ['interface vlan 33', 'untagged 3333'])

    @mock.patch('networking_generic_switch.devices.netmiko_devices.'
                'NetmikoSwitch.send_commands_to_device')
    def test_delete_port(self, mock_exec):
        self.switch.delete_port(3333, 33)
        mock_exec.assert_called_with(
            ['interface vlan 33', 'no untagged 3333'])

    def test__format_commands(self):
        cmd_set = self.switch._format_commands(
            dell.DellNos.ADD_NETWORK,
            segmentation_id=22,
            network_id=22)
        self.assertEqual(cmd_set, ['interface vlan 22', 'name 22'])

        cmd_set = self.switch._format_commands(
            dell.DellNos.DELETE_NETWORK,
            segmentation_id=22)
        self.assertEqual(cmd_set, ['no interface vlan 22'])

        cmd_set = self.switch._format_commands(
            dell.DellNos.PLUG_PORT_TO_NETWORK,
            port=3333,
            segmentation_id=33)
        self.assertEqual(cmd_set,
                         ['interface vlan 33', 'untagged 3333'])
        cmd_set = self.switch._format_commands(
            dell.DellNos.DELETE_PORT,
            port=3333,
            segmentation_id=33)
        self.assertEqual(cmd_set,
                         ['interface vlan 33', 'no untagged 3333'])
