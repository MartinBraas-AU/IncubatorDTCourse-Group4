import time
import datetime

while True:
    print(f"[alive] {datetime.datetime.utcnow().isoformat()}Z")
    time.sleep(5)
