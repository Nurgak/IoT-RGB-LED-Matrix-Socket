#!/bin/bash
python3 client/main.py $ANIMATION --width $WIDTH --height $HEIGHT --key $KEY --city $CITY --timezone $TZ --text $TEXT $ARGS display $HOST_IP --port $PORT --current $CURRENT
