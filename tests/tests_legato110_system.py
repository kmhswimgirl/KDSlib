import pytest
from unittest.mock import MagicMock, patch
from KDSautolib import Legato110

@pytest.fixture
def legato110():
    with patch("KDSautolib.KdsUtil") as MockKdsUtil:
        instance = Legato110("port", 115200)
        instance.kds.send_line = MagicMock()
        return instance

## --------------- System Commands -------------- ##
def test_address(legato110):
    legato110.address(5)
    legato110.kds.send_line.assert_called_with("address 5")

def test_ascale(legato110):
    legato110.ascale(10)
    legato110.kds.send_line.assert_called_with("ascale 10")

def test_set_device_baud_valid(legato110):
    legato110.set_device_baud(115200)
    legato110.kds.send_line.assert_called_with("baud 115200")

def test_set_device_baud_invalid(capsys, legato110):
    legato110.set_device_baud(12345)
    captured = capsys.readouterr()
    assert "[BAUD]: invalid baudrate" in captured.out

def test_boot(legato110):
    legato110.boot()
    legato110.kds.send_line.assert_called_with("boot")

def test_command_set_valid(legato110):
    legato110.command_set("ultra")
    legato110.kds.send_line.assert_called_with("cmd ultra")

def test_command_set_invalid(capsys, legato110):
    legato110.command_set("invalid")
    captured = capsys.readouterr()
    assert "[CMD]: invalid command" in captured.out

def test_default_config(capsys, legato110):
    legato110.default_config()
    legato110.kds.send_line.assert_called_with("config a400,g1,p2.4,t24,br,n0.1,x33,e100")
    captured = capsys.readouterr()
    assert "Device needs to be power cycled" in captured.out

def test_delete_method(legato110):
    legato110.delete_method("test_method")
    legato110.kds.send_line.assert_called_with("delmethod test_method")

def test_dim_screen_valid(legato110):
    legato110.dim_screen(50)
    legato110.kds.send_line.assert_called_with("dim 50")

def test_dim_screen_invalid(capsys, legato110):
    legato110.dim_screen(150)
    captured = capsys.readouterr()
    assert "Brightness out of valid range" in captured.out

def test_echo(legato110):
    legato110.echo()
    legato110.kds.send_line.assert_called_with("echo")

def test_force(legato110):
    legato110.force(80)
    legato110.kds.send_line.assert_called_with("force 80")

def test_set_footswitch_mode_valid(legato110):
    legato110.set_footswitch_mode("mom")
    legato110.kds.send_line.assert_called_with("ftswitch mom")

def test_set_footswitch_mode_invalid(capsys, legato110):
    legato110.set_footswitch_mode("invalid")
    captured = capsys.readouterr()
    assert "Not a valid footswitch mode" in captured.out

def test_poll(legato110):
    legato110.poll("on")
    legato110.kds.send_line.assert_called_with("poll on")

def test_remote_valid(legato110):
    legato110.remote(10)
    legato110.kds.send_line.assert_called_with("remote 10")

def test_remote_invalid(legato110):
    result = legato110.remote(101)
    assert result == "[REM]: Invalid address."

def test_calibrate_tilt(legato110):
    legato110.calibrate_tilt()
    legato110.kds.send_line.assert_called_with("tilt")

def test_set_time(legato110):
    legato110.set_time("2025-07-01", "12:00:00")
    legato110.kds.send_line.assert_called_with("time 2025-07-01 12:00:00")

## ------------ Syringe Commands ---------- ##

def test_set_syringe_size(legato110):
    legato110.set_syringe_size(10, 5, "ml")
    legato110.kds.send_line.assert_called_with("svolume 5 ml")

def test_set_syringe_count(legato110):
    legato110.set_syringe_count(10)
    legato110.kds.send_line.assert_called_with("gang 10")

## ------------ Run Commands --------------- ##

def test_run(legato110):
    legato110.run()
    legato110.kds.send_line.assert_called_with("run")

def test_reverse_direction(legato110):
    legato110.reverse_direction()
    legato110.kds.send_line.assert_called_with("rrun")

def test_stop(legato110):
    legato110.stop()
    legato110.kds.send_line.assert_called_with("stp")

def test_run_motors_i(legato110):
    legato110.run_motors("infuse")
    legato110.kds.send_line.assert_called_with("irun")

def test_run_motors_w(legato110):
    legato110.run_motors("withdraw")
    legato110.kds.send_line.assert_called_with("wrun")

def test_run_motors_error(capsys, legato110):
    legato110.run_motors("invalid")
    captured = capsys.readouterr()
    assert "[RM]: Invalid input. Requires: [infuse | withdraw]" in captured.out
