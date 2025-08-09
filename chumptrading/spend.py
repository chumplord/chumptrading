import os
from datetime import datetime

import pandas as pd

INPUT_COST_PER_M = 0.40  # Adjust for chosen model
OUTPUT_COST_PER_M = 1.60  # Adjust for chosen model

#Budget settings
DAILY_BUDGET = 1.00 # USD per day
MONTHLY_BUDGET = 20.00 # USD per month

# Log file
LOG_FILE = 'api_usage_log.csv'

def get_logged_spend():
    if not os.path.exists(LOG_FILE):
        return 0, 0

    df = pd.read_csv(LOG_FILE, parse_dates=["timestamp"])
    today = pd.Timestamp.today().normalize()
    month_start = today.replace(day=1)
    daily_spend = df[df["timestamp"] >= today]["cost"].sum()
    monthly_spend = df[df["timestamp"] >= month_start]["cost"].sum()
    return daily_spend, monthly_spend


def check_budget():
    daily_spend, monthly_spend = get_logged_spend()
    if daily_spend >= DAILY_BUDGET:
        raise RuntimeError(f"Daily budget of ${DAILY_BUDGET} reached. Skipping API call.")
    if monthly_spend >= MONTHLY_BUDGET:
        raise RuntimeError(f"Monthly budget of ${MONTHLY_BUDGET} reached. Skipping API call.")


def log_usage(usage, model):
    # Token & cost tracking
    input_tokens = usage.prompt_tokens
    output_tokens = usage.completion_tokens
    input_cost = (input_tokens / 1_000_000) * INPUT_COST_PER_M
    output_cost = (output_tokens / 1_000_000) * OUTPUT_COST_PER_M
    total_cost = input_cost + output_cost

    print(f"\n[USAGE] Input tokens: {input_tokens}, Output tokens: {output_tokens}")
    print(f"[COST ESTIMATE] This run: ${total_cost:.6f}")

    # Log to CSV
    log_entry = pd.DataFrame([{
        "timestamp": datetime.utcnow(),
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "cost": total_cost,
        "model": model
    }])
    if os.path.exists(LOG_FILE):
        log_entry.to_csv(LOG_FILE, mode="a", header=False, index=False)
    else:
        log_entry.to_csv(LOG_FILE, index=False)