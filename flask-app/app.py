from flask import Flask, render_template, jsonify, request
from decimal import Decimal, ROUND_HALF_UP


app = Flask(__name__, template_folder='templates')


import math

from decimal import Decimal, ROUND_HALF_UP

def format_time(minutes):
    total_seconds = int(
        (Decimal(str(minutes)) * Decimal("60"))
        .quantize(Decimal("1"), rounding=ROUND_HALF_UP)
    )

    hours = total_seconds // 3600
    remaining_seconds = total_seconds % 3600
    remaining_minutes = remaining_seconds // 60
    seconds = remaining_seconds % 60

    if hours > 0:
        return f"{hours}:{remaining_minutes:02d}:{seconds:02d}"
    return f"{remaining_minutes}:{seconds:02d}"





def parse_time(time_str):
    """
    Parses a time string in MM:SS or decimal format into minutes.
    """
    try:
        return float(time_str)
    except (ValueError, TypeError):
        parts = str(time_str).split(':')
        if len(parts) == 2:
            minutes = int(parts[0])
            seconds = int(parts[1])
            return minutes + seconds / 60
        return 0


def calculate_race_times(pace_per_km):
    """
    Calculates race times for common distances given a pace in min/km.
    Returns strings in MM:SS or H:MM:SS format.
    """

    if pace_per_km is None:
        raise TypeError("Pace cannot be None")

    if not isinstance(pace_per_km, (int, float)):
        raise TypeError("Pace must be a number")

    if pace_per_km <= 0:
        raise ValueError("Pace must be greater than zero")

    # Distances in km
    distances = {
        "5K": 5,
        "10K": 10,
        "Half Marathon": 21.0975,
        "Marathon": 42.195
    }

    race_times = {}
    for name, km in distances.items():
        # total seconds = pace per km * km * 60, then round to nearest integer
        total_seconds = int(round(pace_per_km * km * 60))
        hours = total_seconds // 3600
        remaining_seconds = total_seconds % 3600
        minutes = remaining_seconds // 60
        seconds = remaining_seconds % 60

        if hours > 0:
            race_times[name] = f"{hours}:{minutes:02d}:{seconds:02d}"
        else:
            race_times[name] = f"{minutes}:{seconds:02d}"

    return race_times



@app.route('/convert', methods=['POST'])
def convert():
    data = request.json
    pace = parse_time(data['pace'])
    input_unit = data['unit']

    if input_unit == 'mile':
        km_pace = pace * 1.60934
        race_times = calculate_race_times(km_pace)
        return jsonify({
            'converted_pace': format_time(km_pace),
            'race_times': race_times
        })
    else:
        mile_pace = pace / 1.60934
        race_times = calculate_race_times(pace)
        return jsonify({
            'converted_pace': format_time(mile_pace),
            'race_times': race_times
        })


@app.route('/')
def home():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
