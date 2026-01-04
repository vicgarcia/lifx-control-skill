"""
Unit tests for the LIFX single-file controller.

Setup:
  uv venv
  source .venv/bin/activate  # or `.venv/bin/activate.fish` on fish shell
  uv pip install -e . pytest lifxlan

Run tests:
  uv run pytest lifx_test.py -v
"""

import pytest
from unittest.mock import Mock, patch
import lifx


class TestLifxController:
    """Test LifxController class."""

    @patch('lifx.LifxLAN')
    def test_init(self, mock_lifxlan):
        controller = lifx.LifxController()
        mock_lifxlan.assert_called_once_with(None)

    @patch('lifx.LifxLAN')
    def test_init_with_num_lights(self, mock_lifxlan):
        controller = lifx.LifxController(num_lights=5)
        mock_lifxlan.assert_called_once_with(5)

    @patch('lifx.LifxLAN')
    def test_list_lights(self, mock_lifxlan):
        # Create mock light
        mock_light = Mock()
        mock_light.mac_addr = 'd0:73:d5:01:02:03'
        mock_light.ip_addr = '192.168.1.100'
        mock_light.get_label.return_value = 'Test Light'
        mock_light.get_power.return_value = 65535
        mock_light.get_color.return_value = (30000, 40000, 50000, 3500)
        mock_light.get_product_name.return_value = 'LIFX Color'

        # Setup mock LAN
        mock_lan_instance = Mock()
        mock_lan_instance.get_lights.return_value = [mock_light]
        mock_lifxlan.return_value = mock_lan_instance

        controller = lifx.LifxController()
        lights = controller.list_lights()

        assert len(lights) == 1
        assert lights[0]['mac'] == 'd0:73:d5:01:02:03'
        assert lights[0]['ip'] == '192.168.1.100'
        assert lights[0]['label'] == 'Test Light'
        assert lights[0]['power'] == 'On'
        assert lights[0]['color'] == (30000, 40000, 50000, 3500)
        assert lights[0]['product'] == 'LIFX Color'

    @patch('lifx.LifxLAN')
    def test_find_light_by_mac(self, mock_lifxlan):
        mock_light = Mock()
        mock_light.mac_addr = 'd0:73:d5:01:02:03'
        mock_light.ip_addr = '192.168.1.100'

        mock_lan_instance = Mock()
        mock_lan_instance.get_lights.return_value = [mock_light]
        mock_lifxlan.return_value = mock_lan_instance

        controller = lifx.LifxController()
        found = controller.find_light(mac='d0:73:d5:01:02:03')

        assert found == mock_light

    @patch('lifx.LifxLAN')
    def test_find_light_by_mac_case_insensitive(self, mock_lifxlan):
        mock_light = Mock()
        mock_light.mac_addr = 'd0:73:d5:01:02:03'

        mock_lan_instance = Mock()
        mock_lan_instance.get_lights.return_value = [mock_light]
        mock_lifxlan.return_value = mock_lan_instance

        controller = lifx.LifxController()
        found = controller.find_light(mac='D0:73:D5:01:02:03')

        assert found == mock_light

    @patch('lifx.LifxLAN')
    def test_find_light_by_ip(self, mock_lifxlan):
        mock_light = Mock()
        mock_light.mac_addr = 'd0:73:d5:01:02:03'
        mock_light.ip_addr = '192.168.1.100'

        mock_lan_instance = Mock()
        mock_lan_instance.get_lights.return_value = [mock_light]
        mock_lifxlan.return_value = mock_lan_instance

        controller = lifx.LifxController()
        found = controller.find_light(ip='192.168.1.100')

        assert found == mock_light

    @patch('lifx.LifxLAN')
    def test_find_light_by_label(self, mock_lifxlan):
        mock_light = Mock()
        mock_light.mac_addr = 'd0:73:d5:01:02:03'
        mock_light.get_label.return_value = 'Office Light'

        mock_lan_instance = Mock()
        mock_lan_instance.get_lights.return_value = [mock_light]
        mock_lifxlan.return_value = mock_lan_instance

        controller = lifx.LifxController()
        found = controller.find_light(label='Office Light')

        assert found == mock_light

    @patch('lifx.LifxLAN')
    def test_find_light_by_label_case_insensitive(self, mock_lifxlan):
        mock_light = Mock()
        mock_light.get_label.return_value = 'Office Light'

        mock_lan_instance = Mock()
        mock_lan_instance.get_lights.return_value = [mock_light]
        mock_lifxlan.return_value = mock_lan_instance

        controller = lifx.LifxController()
        found = controller.find_light(label='office light')

        assert found == mock_light

    @patch('lifx.LifxLAN')
    def test_find_light_not_found(self, mock_lifxlan):
        mock_lan_instance = Mock()
        mock_lan_instance.get_lights.return_value = []
        mock_lifxlan.return_value = mock_lan_instance

        controller = lifx.LifxController()
        found = controller.find_light(mac='nonexistent')

        assert found is None

    @patch('lifx.LifxLAN')
    def test_set_power_on(self, mock_lifxlan):
        mock_light = Mock()
        mock_lan_instance = Mock()
        mock_lifxlan.return_value = mock_lan_instance

        controller = lifx.LifxController()
        controller.set_power(mock_light, True, duration=1000)

        mock_light.set_power.assert_called_once_with(True, duration=1000)

    @patch('lifx.LifxLAN')
    def test_set_power_off(self, mock_lifxlan):
        mock_light = Mock()
        mock_lan_instance = Mock()
        mock_lifxlan.return_value = mock_lan_instance

        controller = lifx.LifxController()
        controller.set_power(mock_light, False, duration=500)

        mock_light.set_power.assert_called_once_with(False, duration=500)

    @patch('lifx.LifxLAN')
    def test_set_color(self, mock_lifxlan):
        mock_light = Mock()
        mock_lan_instance = Mock()
        mock_lifxlan.return_value = mock_lan_instance

        controller = lifx.LifxController()
        controller.set_color(mock_light, 30000, 40000, 50000, 3500, duration=1000)

        expected_color = (30000, 40000, 50000, 3500)
        mock_light.set_color.assert_called_once_with(expected_color, duration=1000)


    @patch('lifx.LifxLAN')
    def test_set_label(self, mock_lifxlan):
        mock_light = Mock()
        mock_lan_instance = Mock()
        mock_lifxlan.return_value = mock_lan_instance

        controller = lifx.LifxController()
        controller.set_label(mock_light, 'New Name')

        mock_light.set_label.assert_called_once_with('New Name')

    @patch('lifx.LifxLAN')
    def test_set_label_truncates_long_names(self, mock_lifxlan):
        mock_light = Mock()
        mock_lan_instance = Mock()
        mock_lifxlan.return_value = mock_lan_instance

        controller = lifx.LifxController()
        long_name = 'A' * 50  # 50 characters
        controller.set_label(mock_light, long_name)

        # Should truncate to 32 characters
        mock_light.set_label.assert_called_once_with('A' * 32)


class TestCommandFunctions:
    """Test CLI command functions."""

    @patch('lifx.LifxController')
    def test_cmd_list_no_lights(self, mock_controller_class, capsys):
        mock_controller = Mock()
        mock_controller.list_lights.return_value = []
        mock_controller_class.return_value = mock_controller

        args = Mock()
        args.num_lights = None

        result = lifx.cmd_list(args)

        assert result == 1
        captured = capsys.readouterr()
        assert "No LIFX lights found" in captured.out

    @patch('lifx.LifxController')
    def test_cmd_list_with_lights(self, mock_controller_class, capsys):
        mock_controller = Mock()
        mock_controller.list_lights.return_value = [
            {
                'label': 'Office',
                'ip': '192.168.1.100',
                'mac': 'd0:73:d5:01:02:03',
                'product': 'LIFX Color',
                'power': 'On',
                'color': (30000, 40000, 50000, 3500)
            }
        ]
        mock_controller_class.return_value = mock_controller

        args = Mock()
        args.num_lights = None

        result = lifx.cmd_list(args)

        assert result == 0
        captured = capsys.readouterr()
        assert "Office" in captured.out
        assert "192.168.1.100" in captured.out

    @patch('lifx.LifxController')
    def test_cmd_on_success(self, mock_controller_class, capsys):
        mock_light = Mock()
        mock_light.get_label.return_value = 'Office'

        mock_controller = Mock()
        mock_controller.find_light.return_value = mock_light
        mock_controller_class.return_value = mock_controller

        args = Mock()
        args.mac = None
        args.ip = None
        args.label = 'Office'
        args.duration = 0

        result = lifx.cmd_on(args)

        assert result == 0
        mock_controller.set_power.assert_called_once_with(mock_light, True, duration=0)
        captured = capsys.readouterr()
        assert "turned on" in captured.out

    @patch('lifx.LifxController')
    def test_cmd_on_light_not_found(self, mock_controller_class, capsys):
        mock_controller = Mock()
        mock_controller.find_light.return_value = None
        mock_controller_class.return_value = mock_controller

        args = Mock()
        args.mac = None
        args.ip = None
        args.label = 'NonExistent'
        args.duration = 0

        result = lifx.cmd_on(args)

        assert result == 1
        captured = capsys.readouterr()
        assert "not found" in captured.out

    @patch('lifx.LifxController')
    def test_cmd_off_success(self, mock_controller_class, capsys):
        mock_light = Mock()
        mock_light.get_label.return_value = 'Office'

        mock_controller = Mock()
        mock_controller.find_light.return_value = mock_light
        mock_controller_class.return_value = mock_controller

        args = Mock()
        args.mac = None
        args.ip = None
        args.label = 'Office'
        args.duration = 0

        result = lifx.cmd_off(args)

        assert result == 0
        mock_controller.set_power.assert_called_once_with(mock_light, False, duration=0)
        captured = capsys.readouterr()
        assert "turned off" in captured.out

    @patch('lifx.LifxController')
    def test_cmd_set_success(self, mock_controller_class, capsys):
        mock_light = Mock()
        mock_light.get_label.return_value = 'Office'
        mock_light.get_color.return_value = (30000, 40000, 50000, 3500)

        mock_controller = Mock()
        mock_controller.find_light.return_value = mock_light
        mock_controller_class.return_value = mock_controller

        args = Mock()
        args.mac = None
        args.ip = None
        args.label = 'Office'
        args.hue = 43690
        args.saturation = 65535
        args.brightness = 52428
        args.kelvin = 4000
        args.duration = 1000

        result = lifx.cmd_set(args)

        assert result == 0
        mock_controller.set_color.assert_called_once_with(
            mock_light, 43690, 65535, 52428, 4000, duration=1000
        )
        captured = capsys.readouterr()
        assert "Office" in captured.out

    @patch('lifx.LifxController')
    def test_cmd_set_partial_values(self, mock_controller_class, capsys):
        mock_light = Mock()
        mock_light.get_label.return_value = 'Office'
        mock_light.get_color.return_value = (30000, 40000, 50000, 3500)

        mock_controller = Mock()
        mock_controller.find_light.return_value = mock_light
        mock_controller_class.return_value = mock_controller

        args = Mock()
        args.mac = None
        args.ip = None
        args.label = 'Office'
        args.hue = None
        args.saturation = None
        args.brightness = 32768
        args.kelvin = None
        args.duration = 500

        result = lifx.cmd_set(args)

        assert result == 0
        # Should preserve existing H, S, K and only change B
        mock_controller.set_color.assert_called_once_with(
            mock_light, 30000, 40000, 32768, 3500, duration=500
        )
        captured = capsys.readouterr()
        assert "brightness=32768" in captured.out

    @patch('lifx.LifxController')
    def test_cmd_rename_success(self, mock_controller_class, capsys):
        mock_light = Mock()
        mock_light.get_label.return_value = 'Old Name'

        mock_controller = Mock()
        mock_controller.find_light.return_value = mock_light
        mock_controller_class.return_value = mock_controller

        args = Mock()
        args.mac = None
        args.ip = None
        args.label = 'Old Name'
        args.name = 'New Name'

        result = lifx.cmd_rename(args)

        assert result == 0
        mock_controller.set_label.assert_called_once_with(mock_light, 'New Name')
        captured = capsys.readouterr()
        assert "renamed from 'Old Name' to 'New Name'" in captured.out
