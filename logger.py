from datetime import datetime

log_data = []

def log(message, level="info"):
    now = datetime.now().strftime("%H:%M:%S")
    log_entry = {"time": now, "message": message, "level": level}
    log_data.append(log_entry)
    if len(log_data) > 100:  # Keep only last 100 logs
        log_data.pop(0)
