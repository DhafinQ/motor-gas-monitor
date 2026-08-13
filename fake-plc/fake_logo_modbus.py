import time
import random
import threading

# Gunakan server.sync BUKAN server.asynchronous
from pymodbus.server.sync import StartTcpServer
from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext

# 1. Inisialisasi Data Block Modbus
coils = ModbusSequentialDataBlock(0, [False] * 10)
holding_registers = ModbusSequentialDataBlock(0, [0] * 10)

store = ModbusSlaveContext(co=coils, hr=holding_registers, zero_mode=True)
context = ModbusServerContext(slaves=store, single=True)

# 2. Loop Simulasi Data dalam Thread Terpisah
def update_data():
    while True:
        try:
            gas_ppm = random.randint(100, 850)
            gas_pressure_int = int(round(random.uniform(1.0, 5.0), 2) * 100)
            motor_statuses = [random.choice([True, False]) for _ in range(6)]

            # Update nilai ke memori Modbus
            store.setValues(3, 0, [gas_ppm, gas_pressure_int]) # FC3 Holding Register
            store.setValues(1, 0, motor_statuses)             # FC1 Coils

            print(f"[Fake LOGO!] Gas PPM: {gas_ppm} | Pressure: {gas_pressure_int/100:.2f} Bar | Motors: {motor_statuses}")
        except Exception as e:
            print("Error updating data:", e)
        time.sleep(2)

# Jalankan thread pembaru data
t = threading.Thread(target=update_data, daemon=True)
t.start()

# 3. Jalankan Sync Server di Port 5020 (Tanpa butuh Twisted)
print("=== Fake Siemens LOGO! Modbus TCP Server Running on Port 502 ===")
StartTcpServer(context, address=("0.0.0.0", 502))