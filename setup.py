import json
import pandas as pd
from datetime import datetime

# Step 1: Ask for initial details
print("Menstrual Cycle Tracker — Initial Setup")
cycle_start = input("Enter your last period start date (YYYY-MM-DD): ")
cycle_length = input("Enter your average cycle length in days (default 28): ") or "28"
period_length = input("Enter your average period length in days (default 5): ") or "5"

# Validate date format
try:
    datetime.strptime(cycle_start, "%Y-%m-%d")
except ValueError:
    print("Invalid date format. Please use YYYY-MM-DD.")
    exit()

# Step 2: Save config.json
config = {
    "cycle_start": cycle_start,
    "cycle_length": int(cycle_length),
    "period_length": int(period_length)
}
with open("config.json", "w") as f:
    json.dump(config, f, indent=4)

print("Saved configuration to config.json")

# Step 3: Create empty menstrual_cycle_log.xlsx
columns = [
    "Date",
    "Cycle Day",
    "Phase",
    "Delay Days",
    "Moon & Feelings",
    "Physical State",
    "Menstrual Flow",
    "Discharge",
    "Emotional State",
    "Mental State",
    "Self-Care"
]
df = pd.DataFrame(columns=columns)
df.to_excel("menstrual_cycle_log.xlsx", index=False)

print("Created menstrual_cycle_log.xlsx with headers")
print("Setup complete! You can now run the GUI.")
