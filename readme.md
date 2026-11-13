# Industrial IoT Monitoring: Siemens LOGO! Modbus TCP, Node-RED, InfluxDB & Grafana

Proyek ini merupakan sistem pemantauan industri (*Industrial IoT Monitoring*) secara *real-time* yang dirancang menggunakan arsitektur kontainer (*Docker Compose*). Sistem ini membaca data sensor gas (PPM & Pressure) serta status operasional 8 unit motor melalui protokol **Modbus TCP** (mendukung simulasi Python maupun PLC fisik Siemens LOGO!), memprosesnya di **Node-RED**, menyimpannya ke database *time-series* **InfluxDB v2**, dan memvisualisasikannya secara otomatis melalui dashboard **Grafana**.

---

## 🏗️ Arsitektur & Alur Data

```text
┌─────────────────────────┐       Modbus TCP       ┌─────────────────────────┐
│  Siemens LOGO! PLC      │ ─────────────────────> │       Node-RED          │
│ (atau Fake PLC Python)  │       (Port 5020)      │ (Parser & Batching)     │
└─────────────────────────┘                        └───────────┬─────────────┘
                                                               │ HTTP API / Batch
                                                               ▼
┌─────────────────────────┐       Flux Query       ┌─────────────────────────┐
│        Grafana          │ <───────────────────── │       InfluxDB v2       │
│  (Real-time Dashboard)  │       (Port 8086)      │ (Time-Series Database)  │
└─────────────────────────┘                        └─────────────────────────┘
```

---

## 📁 Struktur Direktori Proyek

```text
simulasi-plc/
├── .env                                # Konfigurasi kredensial terpusat (Token, User, Password)
├── docker-compose.yml                  # Orkestrasi seluruh layanan Docker
├── README.md                           # Dokumentasi proyek
├── fake-plc/                           # Layanan simulasi PLC (Opsional)
│   ├── Dockerfile
│   ├── requirements.txt
│   └── fake_logo_modbus.py
├── nodered-data/                       # Penyimpanan flow dan konfigurasi Node-RED
│   ├── package.json                    # Daftar palette otomatis (Modbus, InfluxDB, Email)
│   ├── settings.js                     # Konfigurasi Node-RED (Credential secret)
│   └── flows.json                      # Logika aliran data otomatis
└── grafana-provisioning/               # Otomatisasi setup Grafana
    ├── datasources/
    │   └── influxdb.yml                # Konfigurasi otomatis koneksi InfluxDB
    └── dashboards/
        ├── default.yml                 # Loader dashboard otomatis
        └── json/
            └── gas_motor.json          # Template visualisasi dashboard
```

---

## 📋 Persyaratan Sistem (*Requirements*)

Sebelum melakukan *deployment*, pastikan perangkat Anda telah terpasang:
1. **Docker Engine** (v20.10 atau lebih baru)
2. **Docker Compose** (v2.0 atau lebih baru)
3. **Git** (opsional, untuk *cloning* repositori)
4. Port lokal yang tersedia dan tidak bentrok: `1880` (Node-RED), `3000` (Grafana), `8086` (InfluxDB), dan `5020` (Modbus TCP Simulator).

---

## 🚀 Tahap Persiapan & Deployment

### 1. Konfigurasi Variabel Lingkungan (`.env`)
Buat atau sesuaikan file `.env` pada direktori utama proyek untuk mengatur kredensial sistem secara terpusat:

```env
# --- INFLUXDB CREDENTIALS ---
INFLUX_ORG=my-org
INFLUX_BUCKET=factory_data_v2
INFLUX_TOKEN=my-super-secret-influx-token-123
INFLUX_ADMIN_USER=admin
INFLUX_ADMIN_PASS=adminpassword123

# --- EMAIL CREDENTIALS (Opsional untuk Alert) ---
EMAIL_USER=notifikasi.factory@gmail.com
EMAIL_PASS=app-password-anda

# --- GRAFANA CREDENTIALS ---
GF_SECURITY_ADMIN_USER=admin
GF_SECURITY_ADMIN_PASSWORD=admin
```

### 2. Menjalankan Sistem (Deploy)

Terdapat dua mode operasional yang dapat dipilih saat menjalankan sistem:

* **Mode Simulasi Lengkap (Dengan Fake PLC Python):**
  Gunakan perintah ini untuk menjalankan seluruh layanan beserta simulator data Modbus TCP.
  ```bash
  docker compose --profile plc up -d --build
  ```

* **Mode Produksi (Tanpa Simulasi / Menggunakan PLC Fisik):**
  Gunakan perintah ini jika Node-RED akan dihubungkan langsung ke perangkat keras Siemens LOGO! asli di jaringan lokal.
  ```bash
  docker compose up -d --build
  ```

### 3. Verifikasi Status Kontainer
Pastikan seluruh kontainer berstatus `Up` / `Running`:
```bash
docker compose ps
```

---

## 🌐 Panduan Akses Layanan

Setelah seluruh kontainer berjalan, layanan dapat diakses melalui browser dengan detail berikut:

| Layanan | URL Akses | Username | Password / Token | Keterangan |
| :--- | :--- | :--- | :--- | :--- |
| **Grafana** | `http://localhost:3000` | `admin` | `admin` | Buka menu **Dashboards** $\rightarrow$ **Monitoring Industri - Gas & Motor**. |
| **Node-RED** | `http://localhost:1880` | *(Tanpa Login)* | *(Tanpa Login)* | Flow dan palette sudah terpasang otomatis. |
| **InfluxDB** | `http://localhost:8086` | `admin` | `adminpassword123` | Bucket utama: `factory_data_v2`. |

---

## 🛠️ Pemeliharaan & Troubleshooting

* **Melihat Log Kontainer:**
  Jika terjadi kendala koneksi antar-layanan, periksa log masing-masing kontainer:
  ```bash
  docker logs nodered_factory --tail 50
  docker logs grafana_factory --tail 50
  ```

* **Menghentikan Sistem:**
  ```bash
  docker compose --profile plc down
  ```

* **Reset Total (Menghapus Database & Cache Volume):**
  Gunakan perintah ini hanya jika ingin mengulang inisialisasi database InfluxDB dan konfigurasi Grafana dari nol:
  ```bash
  docker compose --profile plc down -v
  ```
