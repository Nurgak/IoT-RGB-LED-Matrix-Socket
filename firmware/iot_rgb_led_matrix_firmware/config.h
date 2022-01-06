#pragma once

static const char * AP_PASSWORD = "rgbledmatrix";
static const IPAddress STATIC_IP(192, 168, 3, 101);
static const IPAddress STATIC_GATEWAY(192, 168, 3, 1);
static const IPAddress STATIC_SUBNET(255, 255, 255, 0);

static const unsigned int SERVER_PORT = 7777;
static const unsigned int TIMEOUT_MS = 5;

#define BUFFER_SIZE 48 * 32 + 1

#define CLK 14
#define OE  13
#define LAT 15
#define A   26
#define B   4
#define C   27
#define D   2

static uint8_t RGB[] = {5, 17, 18, 19, 16, 25};
