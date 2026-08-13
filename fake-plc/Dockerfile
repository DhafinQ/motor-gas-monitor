FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy script python
COPY fake_logo_modbus.py .

# Expose port Modbus TCP
EXPOSE 5020

CMD ["python", "fake_logo_modbus.py"]