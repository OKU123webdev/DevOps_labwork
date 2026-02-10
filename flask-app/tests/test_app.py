import pytest
from app import calculate_race_times, format_time


def test_format_time():
    assert format_time(0) == "0:00"
    assert format_time(1) == "1:00"
    assert format_time(10) == "10:00"
    assert format_time(60) == "1:00:00"
    assert format_time(181) == "3:01:00"
    assert format_time(611) == "10:11:00"


def test_calculate_race_times_valid_pace():
    expected = {
        "5K": "25:00",
        "10K": "50:00",
        "Half Marathon": "1:45:29",
        "Marathon": "3:30:58"
    }

    assert calculate_race_times(5) == expected


def test_calculate_race_times_zero_pace():
    with pytest.raises(ValueError):
        calculate_race_times(0)


def test_calculate_race_times_negative_pace():
    with pytest.raises(ValueError):
        calculate_race_times(-5)


def test_calculate_race_times_none_input():
    with pytest.raises(TypeError):
        calculate_race_times(None)


def test_calculate_race_times_empty_input():
    with pytest.raises(TypeError):
        calculate_race_times("")
