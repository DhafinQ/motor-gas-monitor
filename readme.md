# Factory Condition Monitoring

An industrial IoT monitoring system for monitoring motor status, gas pressure, and gas leak conditions.

The project uses:

- **Node-RED** — data processing and automation
- **InfluxDB** — time-series data storage
- **Grafana** — monitoring dashboard and visualization
- **Docker Compose** — containerized deployment

## Architecture

```text
Sensors / IoT Device
        │
        ▼
    Node-RED
        │
        ▼
    InfluxDB
        │
        ▼
     Grafana
        │
        ▼
 Monitoring Dashboard
````

## Requirements

Before running the project, make sure you have:

* Docker
* Docker Compose
* Git

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/DhafinQ/motor-gas-monitor.git
cd motor-gas-monitor
```

### 2. Create the environment file

Copy the example environment file:

```bash
cp .env.example .env
```

Then edit `.env` and configure your credentials.

Example:

```env
# Grafana
GF_SECURITY_ADMIN_USER=admin
GF_SECURITY_ADMIN_PASSWORD=admin

# InfluxDB
INFLUX_ADMIN_USER=admin
INFLUX_ADMIN_PASS=change-me
INFLUX_ORG=my-org
INFLUX_BUCKET=factory_data_v2
INFLUX_TOKEN=change-me

# Email / SMTP
EMAIL_USER=your-email@gmail.com
EMAIL_PASS=your-app-password
```

> Do not commit `.env` to the repository.

## 3. Start the project

Build the required images and start all containers:

```bash
docker compose up -d --build
```

## 4. Access the services

### Grafana

Open:

```text
http://localhost:3000
```

Login using the Grafana credentials configured in `.env`.

### Node-RED

Open:

```text
http://localhost:1880
```

### InfluxDB

Open:

```text
http://localhost:8086
```

## Grafana Dashboard

The Grafana datasource and dashboard are automatically provisioned when the container starts.

<p align="center"><img src="https://drive.google.com/uc?export=view&id=1qoqjhBnWspnlt7TWvKvvEdlDCjRQSwQG" width="800"></p>

The dashboard provides monitoring for:

* Motor status
* Gas pressure / concentration
* Gas leak information
* Sensor data over time
* Motor status alerts everytime a motor status is changed via email 

No manual Grafana dashboard import should be required.

## Stop the Project

Stop the containers:

```bash
docker compose down
```

