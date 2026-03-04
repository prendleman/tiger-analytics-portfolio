# Healthcare Analytics Portfolio — reproducible run
# Build: docker build -t tiger-portfolio .
# Run demo: docker run --rm tiger-portfolio
# Shell:   docker run --rm -it tiger-portfolio /bin/bash
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Default: run one-command demo (generate data + readmission + time series)
CMD ["python", "scripts/run_demo.py"]
