FROM python:3-slim
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
COPY . /app
WORKDIR /app
RUN python3 -m pip install --no-cache-dir -r requirements.txt
ENTRYPOINT [ "./entrypoint.sh" ]
