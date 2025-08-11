# cycle_tracker.py
import pandas as pd
from datetime import datetime, timedelta
import os
import json
import ephem

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "menstrual_cycle_log.xlsx")
CONFIG_FILE = os.path.join(BASE_DIR, "cycle_config.json")

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    else:
        config = {
            "last_period_start": datetime.now().strftime("%Y-%m-%d"),
            "cycle_length": 28,
            "delay_days": 0,
            "in_delay": False
        }
        save_config(config)
        return config

def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f)

def get_phase(cycle_day, cycle_length):
    if cycle_day <= 5:
        return "Menstrual Phase"
    elif 6 <= cycle_day <= (cycle_length // 2) - 3:
        return "Follicular Phase"
    elif (cycle_length // 2) - 2 <= cycle_day <= (cycle_length // 2) + 2:
        return "Ovulatory Phase"
    else:
        return "Luteal Phase"

def get_moon_info(lat, lon):
    obs = ephem.Observer()
    obs.lat = str(lat)
    obs.lon = str(lon)
    obs.date = datetime.utcnow()

    moon = ephem.Moon(obs)
    phase = moon.phase

    if phase < 1:
        phase_name = "New Moon"
    elif phase < 50:
        phase_name = "Waxing"
    elif phase > 99:
        phase_name = "Full Moon"
    elif phase > 50:
        phase_name = "Waning"

    constellation = ephem.constellation(moon)[1]
    return phase_name, constellation, phase

def get_today_info():
    config = load_config()
    last_start = datetime.strptime(config["last_period_start"], "%Y-%m-%d")
    today = datetime.now()

    cycle_length = config["cycle_length"]
    days_since_start = (today - last_start).days + 1
    if days_since_start > cycle_length:
        days_since_start = cycle_length

    phase = get_phase(days_since_start, cycle_length)
    lat, lon = 12.55, 77.32
    phase_name, sign, phase_pct = get_moon_info(lat, lon)
    moon_desc = f"Moon is in {sign} — {phase_name} (~{phase_pct:.1f}% illuminated)."

    return {
        "date": today.strftime("%Y-%m-%d %H:%M:%S"),
        "cycle_day": days_since_start,
        "phase": phase,
        "delay_days": config.get("delay_days", 0),
        "moon_desc": moon_desc
    }

def save_entry(entry):
    df_new = pd.DataFrame([entry])
    if os.path.exists(DATA_FILE):
        df_existing = pd.read_excel(DATA_FILE)
        # Remove any existing rows with the same date
        date_str = entry["Date"]
        df_existing = df_existing[df_existing["Date"] != date_str]
        # Append the new entry
        df_all = pd.concat([df_existing, df_new], ignore_index=True)
    else:
        df_all = df_new
    df_all.to_excel(DATA_FILE, index=False)

def get_questions(moon_desc):
    questions = [
        (moon_desc + " How are you feeling under this moon phase?", "Moon Influence"),
        ("How is your physical state today?", "Physical State"),
        ("How is your menstrual flow?", "Flow"),
        ("Describe any fluids/discharge.", "Fluids"),
        ("How is your emotional state?", "Emotional State"),
        ("How is your mental state?", "Mental State"),
        ("What self-care activities did you do?", "Self Care"),
        ("How was your sleep last night?", "Sleep"),
        ("Any dreams worth noting?", "Dreams")
    ]
    return questions
