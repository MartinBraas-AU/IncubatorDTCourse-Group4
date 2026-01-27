import os
import time
import random
from datetime import datetime, timezone

from influxdb_client import InfluxDBClient, Point, WriteOptions

INFLUX_URL = os.getenv("INFLUX_URL", "http://localhost:8086")
INFLUX_TOKEN = os.getenv("INFLUX_TOKEN", "YOUR_TOKEN")
INFLUX_ORG = os.getenv("INFLUX_ORG", "dt-course")
INFLUX_BUCKET = os.getenv("INFLUX_BUCKET", "experimental")

client = InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org=INFLUX_ORG)
write_api = client.write_api(write_options=WriteOptions(batch_size=1))

try:
    for i in range(12):  # 12 * 5s = 60s
        value = 20.0 + random.random() * 5.0
        ts = datetime.now(timezone.utc)

        p = (
            Point("temperature")
            .tag("sensor", "python")
            .field("value", float(value))
            .time(ts)  # explicit timestamp
        )

        write_api.write(bucket=INFLUX_BUCKET, org=INFLUX_ORG, record=p)
        print(f"Wrote: {ts.isoformat()} value={value:.2f}")
        time.sleep(5)
finally:
    client.close()