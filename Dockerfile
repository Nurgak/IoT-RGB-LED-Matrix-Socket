FROM debian:stable-slim
SHELL ["/bin/bash", "-c"]
WORKDIR /root/ws
ENV ANIMATION=analog_clock.AnalogClock \
    WIDTH=32 \
    HEIGHT=32 \
    PORT=7777 \
    TZ=GMT \
    KEY="" \
    CITY="" \
    TEXT="" \
    CURRENT=100 \
    ARGS="" \
    PYTHONPATH=/root/ws/client

EXPOSE ${PORT}
COPY . .

RUN apt-get update \
    && apt-get install --no-install-recommends -y \
    python3-opencv=4.5.* \
    python3-numpy=1:1.19.* \
    python3-pil=8.1.* \
    python3-pip=20.3.* \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir -r requirements.txt

CMD ["./main.sh"]
