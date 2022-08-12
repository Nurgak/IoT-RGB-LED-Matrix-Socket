/**
 * \file config.h
 * \brief Configuration file for the IOT RGB LED Matrix.
 * \see https://github.com/Nurgak/IoT-RGB-LED-Matrix-Socket
 */
#pragma once

#include <ArduinoJson.h>
#include <SPIFFS.h>

//static const bool FORMAT_SPIFFS_IF_FAILED true
static const bool FORMAT_SPIFFS_IF_FAILED = false;
static const unsigned int WIFI_CONNECT_TIMEOUT = 120;
static const unsigned int BUFFER_SIZE = 48 * 32 + 1;
static const unsigned int PIN_CLK = 14;
static const unsigned int PIN_OE  = 13;
static const unsigned int PIN_LAT = 15;
static const unsigned int PIN_A   = 26;
static const unsigned int PIN_B   = 4;
static const unsigned int PIN_C   = 27;
static const unsigned int PIN_D   = 2;

static const unsigned int PIN_UPPER_RED   = 5;
static const unsigned int PIN_UPPER_GREEN = 17;
static const unsigned int PIN_UPPER_BLUE  = 18;
static const unsigned int PIN_LOWER_RED   = 19;
static const unsigned int PIN_LOWER_GREEN = 16;
static const unsigned int PIN_LOWER_BLUE  = 25;

// Define the upper 3 and lower 3 RGB pins.
static uint8_t PIN_RGB[] = {
  PIN_UPPER_RED,
  PIN_UPPER_GREEN,
  PIN_UPPER_BLUE,
  PIN_LOWER_RED,
  PIN_LOWER_GREEN,
  PIN_LOWER_BLUE
};

namespace Config
{
  /** \brief Default static IP of the LED matrix. */
  char static_ip[16] = "192.168.1.254";
  /** \brief Default static gateway. */
  char static_gw[16] = "192.168.1.1";
  /** \brief Default static subnet. */
  char static_sn[16] = "255.255.255.0";
  /** \brief Default server port of the LED matrix. */
  char port[8] = "7777";
  /** \brief Default restart timeout when no data has been recieved, in seconds. */
  char timeout[8] = "120";

  void save()
  {
    /** \brief Save configuration values to SPIFFS. */
    DynamicJsonDocument json(256);
    json["static_ip"] = WiFi.localIP().toString();
    json["static_gw"] = WiFi.gatewayIP().toString();
    json["static_sn"] = WiFi.subnetMask().toString();
    json["port"] = port;
    json["timeout"] = timeout;

    File configFile = SPIFFS.open("/config.json", "w");
    if(!configFile)
    {
      return;
    }

    serializeJson(json, configFile);
    configFile.close();
  }

  void load()
  {
    /** \brief Load configuration values from SPIFFS. */
    if(SPIFFS.begin(FORMAT_SPIFFS_IF_FAILED))
    {
      if(SPIFFS.exists("/config.json"))
      {
        File configFile = SPIFFS.open("/config.json", "r");
        if(configFile)
        {
          const size_t size = configFile.size();
          std::unique_ptr<char[]> buf(new char[size]);

          configFile.readBytes(buf.get(), size);
          DynamicJsonDocument json(256);

          if(DeserializationError::Ok == deserializeJson(json, buf.get()))
          {
            strcpy(static_ip, json["static_ip"]);
            strcpy(static_gw, json["static_gw"]);
            strcpy(static_sn, json["static_sn"]);
            strcpy(port, json["port"]);
            strcpy(timeout, json["timeout"]);
          }
        }
      }
    }
  }
}
