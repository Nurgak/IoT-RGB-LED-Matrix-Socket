#pragma once

static const char* WIFI_SSID = "...";
static const char* WIFI_PASSWORD = "...";
static const unsigned int SERVER_PORT = 7777;
static const unsigned int TIMEOUT_MS = 5;

#define BUFFER_SIZE 16 * 32 * 3

#define CLK 14
#define OE  13
#define LAT 15
#define A   26
#define B   4
#define C   27
#define D   2

static uint8_t RGB[] = {5, 17, 18, 19, 16, 25};
