FROM python:3.10
WORKDIR /app
COPY core/requirements.txt /app/core/requirements.txt
COPY api/requirements.txt /app/api/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/core/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/api/requirements.txt
