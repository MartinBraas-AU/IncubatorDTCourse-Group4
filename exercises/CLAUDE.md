# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A unified sensor data pipeline (RabbitMQ → InfluxDB) for the Digital Twin incubator course. Scalable via `docker compose up --scale`.

## Running

```bash
# Start everything (1 producer, 1 consumer by default)
docker compose up --build

# Scale producers and consumers
docker compose up --scale producer=3 --scale consumer=2
```

InfluxDB UI at http://localhost:8086 (login: admin / password123).

## Architecture

**Producer → RabbitMQ (`sensor_queue`) → Consumer → InfluxDB**

- `producer/producer.py`: Infinite loop generating JSON temperature readings, publishes to RabbitMQ. Unique sensor ID per container (hostname).
- `consumer/consumer.py`: Consumes from RabbitMQ queue, writes points to InfluxDB 2.x. Manual ack, prefetch=1.
- Docker Compose brings up RabbitMQ (port 5672) and InfluxDB (port 8086) with auto-setup.
- Environment config in `.env` (INFLUX_ORG, INFLUX_BUCKET, INFLUX_TOKEN, QUEUE_NAME).

## Message Format

```json
{"ts": "ISO-8601", "value": 22.5, "sensor": "hostname"}
```
