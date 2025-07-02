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

def test_remote(legato110):
    legato110.remote(10)
    legato110.kds.send_line.assert_called_with("remote 10")

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

def test_run_motors(capsys, legato110):
    # infuse
    legato110.run_motors("infuse")
    legato110.kds.send_line.assert_called_with("irun")

    # withdraw
    legato110.run_motors("withdraw")
    legato110.kds.send_line.assert_called_with("wrun")

    # error message
    legato110.run_motors("invalid")
    captured = capsys.readouterr()
    assert "[RM]: Invalid input. Requires: [infuse | withdraw]" in captured.out

# ==================== Volume Commands ===================== #
def test_set_target_volume(legato110):
    legato110.set_target_volume(10, "ml")
    legato110.kds.send_line.assert_called_with("tvolume 10 ml")


def test_clear_volume(capsys, legato110):
    legato110.clear_volume("infuse")
    legato110.kds.send_line.assert_called_with("civolume")

    legato110.clear_volume("target")
    legato110.kds.send_line.assert_called_with("ctvolume")

    legato110.clear_volume("bothDirs")
    legato110.kds.send_line.assert_called_with("cvolume")

    legato110.clear_volume("withdraw")
    legato110.kds.send_line.assert_called_with("cwvolume")

    legato110.clear_volume("invalid")
    captured = capsys.readouterr()
    assert "[CV]: command not recognized" in captured.out

# ==================== Time Commands ===================== #

def test_set_target_time(legato110):
    legato110.set_target_time(30)
    legato110.kds.send_line.assert_called_with("ttime 30")

def test_clear_time(capsys, legato110):
    # infuse
    legato110.clear_time("infuse")
    legato110.kds.send_line.assert_called_with("citime")

    # target
    legato110.clear_time("target")
    legato110.kds.send_line.assert_called_with("cttime")

    # both
    legato110.clear_time("both")
    legato110.kds.send_line.assert_called_with("ctime")

    # withdraw
    legato110.clear_time("withdraw")
    legato110.kds.send_line.assert_called_with("cwtime")

    # error handling
    legato110.clear_time("invalid")
    captured = capsys.readouterr()
    assert "[CT]: command not recognized. Use [infuse | target | both | withdraw]" in captured.out

# ==================== Rate Commands ===================== #
    def test_set_infuse_rate(capsys, legato110):
        # max rate
        legato110.set_infuse_rate(setMax = True)
        legato110.kds.send_line.assert_called_with("irate max")

        # min rate
        legato110.set_infuse_rate(setMin = True)
        legato110.kds.send_line.assert_called_with("irate min")

        # other rate
        legato110.set_infuse_rate(rate = 20, units = "ml")
        legato110.kds.send_line.assert_called_with("irate 20 ml")

        # error
        legato110.set_infuse_rate("invalid")
        captured = capsys.readouterr()
        assert "[SIRate]: please check documentation. incorrect cmd format" in captured.out

    def test_set_withdraw_rate(capsys, legato110):
        # max rate
        legato110.set_withdraw_rate(setMax = True)
        legato110.kds.send_line.assert_called_with("wrate max")

        # min rate
        legato110.set_withdraw_rate(setMin = True)
        legato110.kds.send_line.assert_called_with("wrate min")

        # other rate
        legato110.set_withdraw_rate(rate = 20, units = "ml")
        legato110.kds.send_line.assert_called_with("wrate 20 ml")

        # error
        legato110.set_withdraw_rate("invalid")
        captured = capsys.readouterr()
        assert "[SWRate]: please check documentation. incorrect cmd format" in captured.out