FROM python:3.9
ENV PORT=7777 \
    WIDTH=32 \
    HEIGHT=32 \
    PYTHONPATH=/root/ws/client

WORKDIR /root/ws
COPY . .
# hadolint ignore=DL3008
RUN apt-get update && \
    apt-get install --no-install-recommends -y ffmpeg libsm6 libxext6 && \
    rm -rf /var/lib/apt/lists/* && \
    pip install --no-cache-dir -r requirements.txt

CMD ["python", "client/main.py", "${ANIMATION}", "--width", "${WIDTH}", \
    "--height", "${HEIGHT}", "display", "${HOST_IP}", "--port", "${PORT}"]