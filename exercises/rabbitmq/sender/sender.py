import os
import time
import pika

host = os.getenv("RABBITMQ_HOST", "localhost")
queue = os.getenv("QUEUE_NAME", "demo_queue")
message = os.getenv("MESSAGE", "hello")

def connect():
    params = pika.ConnectionParameters(host=host, heartbeat=30)
    return pika.BlockingConnection(params)

# small retry loop so it works even if broker is just coming up
for attempt in range(20):
    try:
        conn = connect()
        ch = conn.channel()
        ch.queue_declare(queue=queue, durable=False)
        ch.basic_publish(exchange="", routing_key=queue, body=message.encode())
        print(f"[sender] sent: {message}", flush=True)
        conn.close()
        # break
    except Exception as e:
        print(f"[sender] error: {e} (retrying)", flush=True)
        time.sleep(1)
else:
    raise SystemExit("[sender] failed to send after retries")
