#include <WiFiManager.h>
#include <esp_task_wdt.h>
#include <RGBmatrixPanel.h>
#include <Fonts/FreeSerif9pt7b.h>
#include "config.h"

RGBmatrixPanel matrix(A, B, C, D, CLK, LAT, OE, false, 32, RGB);

static char AP_NAME[24];
WiFiServer server(SERVER_PORT);
TaskHandle_t listen_task_handle;

void setup()
{
  // Needed for WiFi manager debug.
  Serial.begin(115200);

  matrix.begin();
  matrix.print("WiFi\nsetup");

  WiFiManager wifiManager;

  //wifiManager.resetSettings();
  snprintf(AP_NAME, sizeof(AP_NAME), "ESPLEDMatrix-%04X", ESP.getEfuseMac());

  wifiManager.setSTAStaticIPConfig(STATIC_IP, STATIC_GATEWAY, STATIC_SUBNET);
  wifiManager.autoConnect(AP_NAME, AP_PASSWORD);

  // Print the IP on the matrix so the client could connect to it.
  matrix.fillScreen(0);
  matrix.setCursor(0, 0);
  matrix.printf("%d\n%d\n%d\n%d", STATIC_IP[0], STATIC_IP[1], STATIC_IP[2], STATIC_IP[3]);

  server.begin();

  xTaskCreatePinnedToCore(&listen, "listen", 2048, NULL, 1, &listen_task_handle, 0);

  // Prevent the LED matrix from freezing: restart if no new data has been recieved for 120 seconds.
  esp_task_wdt_init(WDT_TIMEOUT, true);
  esp_task_wdt_add(listen_task_handle);
}

void listen(void *pvParameter)
{
  unsigned long time_start_ms = 0;
  uint8_t * buffer_ptr = matrix.backBuffer();
  size_t bytes_read;

  while(true)
  {
    WiFiClient client = server.available();
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
}
