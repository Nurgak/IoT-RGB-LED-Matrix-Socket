FROM debian:stable-slim
SHELL ["/bin/bash", "-c"]
WORKDIR /root/ws
ENV ANIMATION=AnalogClock \
    WIDTH=32 \
    HEIGHT=32 \
    PORT=7777 \
    TZ=GMT \
    KEY="" \
    CITY="" \
    TEXT="" \
    PYTHONPATH=/root/ws/client

EXPOSE ${PORT}
COPY . .
# hadolint ignore=DL3008
RUN apt-get update && \
    apt-get install --no-install-recommends -y \
    python3-opencv \
    python3-numpy \
    python3-pil \
    python3-pip && \
    rm -rf /var/lib/apt/lists/* && \
    pip install --no-cache-dir -r requirements.txt

CMD cd client && ./main.py "${ANIMATION}" --width "${WIDTH}" --height "${HEIGHT}"  --key "${KEY}" \
    --city "${CITY}" --timezone "${TZ}" --text "${TEXT}" display "${HOST_IP}" --port "${PORT}"