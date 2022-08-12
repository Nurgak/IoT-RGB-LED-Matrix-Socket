/**
 \file
 \brief Main program file for the IOT RGB LED Matrix.
 All parameters are set through the web portal when WiFi credentials are configured.
 \see https://github.com/Nurgak/IoT-RGB-LED-Matrix-Socket
*/
#include <WiFiManager.h>
#include <ArduinoOTA.h>

#include <esp_task_wdt.h>
#include <RGBmatrixPanel.h>
#include <Fonts/FreeSerif9pt7b.h>

#include "config.h"

/** \brief Matrix instance, set pin definitions in config.h. */
RGBmatrixPanel matrix(PIN_A, PIN_B, PIN_C, PIN_D, PIN_CLK, PIN_LAT, PIN_OE, false, 32, PIN_RGB);

/** \brief Flag to indicate if configuration should be saved to SPIFFS. */
bool should_save_config = false;
/** \brief Unique device identifier, partially populated with WiFi MAC address. */
char identifier[24];
/** \brief Listen task handle, used for pausing/resuming and watchdog checking. */
TaskHandle_t listen_task_handle;

/** \brief Server instance, listens to the client sending over the display data. */
WiFiServer server;

void setup()
{
  /** \brief Setup function, called once at the beginning of the program. */
  // Needed for WiFi manager debug.
  Serial.begin(115200);

  // Format FS for testing.
  //SPIFFS.format();

  byte mac[6];
  WiFi.macAddress(mac);
  snprintf(identifier, sizeof(identifier), "ESPLEDMATRIX-%02X%02X%02X", mac[5], mac[4], mac[3]);

  matrix.begin();
  matrix.print("WiFi\nsetup");

  Config::load();
  setupWifi();
  setupOTA();

  // Start the display server with the defined port from the configuration.
  server.begin(atoi(Config::port));

  // Print the IP on the matrix so the client could be configured with it.
  matrix.fillScreen(0);
  matrix.setCursor(0, 0);
  IPAddress ip_address = WiFi.localIP();
  matrix.printf("%d\n%d\n%d\n%d", ip_address[0], ip_address[1], ip_address[2], ip_address[3]);

  // Create the listening task on CPU1 and save its handle.
  xTaskCreatePinnedToCore(&listen, "listen", 2048, NULL, 1, &listen_task_handle, 0);

  // Prevent the LED matrix from freezing: restart if no new data has been recieved for a while.
  esp_task_wdt_init(atoi(Config::timeout), true);
  // Subscribe the listen task to the watchdog.
  esp_task_wdt_add(listen_task_handle);
}

void setupOTA()
{
  /** \brief Over-the-air update setup function. */
  ArduinoOTA.onStart([]()
  {
    esp_task_wdt_delete(listen_task_handle);
    vTaskSuspend(listen_task_handle);
    Serial.println("Start");
  });

  ArduinoOTA.onEnd([]()
  {
    Serial.println("\nEnd");
    // The ESP will reboot at this point, no need to resume the listen task.
  });

  ArduinoOTA.onProgress([](unsigned int progress, unsigned int total)
  {
    Serial.printf("Progress: %u%%\r", (progress / (total / 100)));

    matrix.fillScreen(0);
    matrix.setCursor(0, 0);
    matrix.printf("Prog\n%u%%\r", (progress / (total / 100)));
  });

  ArduinoOTA.onError([](ota_error_t error)
  {
    Serial.printf("Error[%u]: ", error);

    matrix.fillScreen(0);
    matrix.setCursor(0, 0);
    matrix.printf("Error\n%u", error);

    if(error == OTA_AUTH_ERROR)
    {
        Serial.println("Auth Failed");
    }
    else if (error == OTA_BEGIN_ERROR)
    {
        Serial.println("Begin Failed");
    }
    else if (error == OTA_CONNECT_ERROR)
    {
        Serial.println("Connect Failed");
    }
    else if (error == OTA_RECEIVE_ERROR)
    {
        Serial.println("Receive Failed");
    }
    else if (error == OTA_END_ERROR)
    {
        Serial.println("End Failed");
    }

    // Resume normal operation when an error has occurred.
    vTaskResume(listen_task_handle);
    esp_task_wdt_add(listen_task_handle);
  });

  ArduinoOTA.setHostname(identifier);
  ArduinoOTA.setPassword(identifier);
  ArduinoOTA.begin();
}

void saveConfigCallback()
{
  /** \brief Callback function triggered from the WiFi manager front end. */
  should_save_config = true;

  // Restart the server just in case the user changed the port.
  server.begin(atoi(Config::port));
  // Reconfigure the watchdog timeout value in case it was changed.
  esp_task_wdt_init(atoi(Config::timeout), true);
}

void setupWifi()
{
  /** \brief WiFi setup function. */
  WiFiManager wifiManager;

  // Reset WiFI settings for testing.
  //wifiManager.resetSettings();

  WiFiManagerParameter rgbletmatrix_port("port", "Matrix server port", Config::port, sizeof(Config::port));
  WiFiManagerParameter rgbletmatrix_timeout("timeout", "Listen timeout in seconds", Config::timeout, sizeof(Config::timeout));

  wifiManager.setDebugOutput(false);
  wifiManager.setSaveConfigCallback(saveConfigCallback);
  wifiManager.addParameter(&rgbletmatrix_port);
  wifiManager.addParameter(&rgbletmatrix_timeout);
  // Set connection timeout, different from display timeout.
  wifiManager.setTimeout(WIFI_CONNECT_TIMEOUT);

  IPAddress static_ip, static_gw, static_sn;
  static_ip.fromString(Config::static_ip);
  static_gw.fromString(Config::static_gw);
  static_sn.fromString(Config::static_sn);
  wifiManager.setSTAStaticIPConfig(static_ip, static_gw, static_sn);

  WiFi.hostname(identifier);

  // Block here while attempting to connect.
  if(!wifiManager.autoConnect(identifier))
  {
    // Restart when WiFi connection unsuccessful after timeout.
    ESP.restart();
  }

  strcpy(Config::port, rgbletmatrix_port.getValue());
  strcpy(Config::timeout, rgbletmatrix_timeout.getValue());

  if(should_save_config)
  {
    Config::save();
  }
  else
  {
    Config::load();
  }
}

void listen(void *pvParameter)
{
  /** \brief Listen function, updating the matrix display with data recieved from the client. */
  uint8_t * buffer_ptr = matrix.backBuffer();
  size_t bytes_read;
  WiFiClient client;

  while(true)
  {
    client = server.available();
    if(client)
    {
      while(client.connected())
      {
        while(client.available())
        {
          bytes_read = client.readBytesUntil('\n', buffer_ptr, BUFFER_SIZE);
          client.write('\n');
          esp_task_wdt_reset();
          vTaskDelay(1);
        }
        vTaskDelay(1);
      }
      client.stop();
    }
    vTaskDelay(1);
  }
}

void loop()
{
  /** \brief Infinite loop, used for OTA handle call while idle. */
  ArduinoOTA.handle();
}
