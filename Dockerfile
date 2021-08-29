FROM python:3
ENV PORT=7777 \
    WIDTH=32 \
    HEIGHT=32 \
    PYTHONPATH=/root/ws/client

WORKDIR /root/ws
COPY . .
RUN apt-get update && \
    apt-get install -y ffmpeg libsm6 libxext6 && \
    pip install -r requirements.txt

CMD python client/main.py ${ANIMATION} \
    --width ${WIDTH} \
    --height ${HEIGHT} \
    display ${HOST_IP} --port ${PORT}