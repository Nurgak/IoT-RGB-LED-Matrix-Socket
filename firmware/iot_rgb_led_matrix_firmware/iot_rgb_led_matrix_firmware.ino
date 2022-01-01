#include <WiFi.h>
#include <WiFiManager.h>
#include <RGBmatrixPanel.h>
#include <Fonts/FreeSerif9pt7b.h>
#include "config.h"

RGBmatrixPanel matrix(A, B, C, D, CLK, LAT, OE, false, 32, RGB);

WiFiServer server(SERVER_PORT);

void setup()
{
  matrix.begin();

  matrix.print("WiFi\nsetup");

  WiFiManager wm;
  //wm.resetSettings();
  wm.setShowStaticFields(true);
  wm.setShowDnsFields(true);
  wm.autoConnect();

  IPAddress ip = WiFi.localIP();
  Serial.println(ip);

  // Print the IP on the matrix so the client could connect to it.
  matrix.fillScreen(0);
  matrix.setCursor(0, 0);
  matrix.printf("%d\n%d\n%d\n%d", ip[0], ip[1], ip[2], ip[3]);

  server.begin();

  xTaskCreatePinnedToCore(&listen, "listen", 2048, NULL, 1, NULL, 0);
}

void listen(void *pvParameter)
{
  unsigned long time_start_ms = 0;
  uint8_t * buffer_ptr = matrix.backBuffer();

  while(true)
  {
    WiFiClient client = server.available();
    if(client)
    {
      while(client.connected())
      {
        while(client.available())
        {
          client.readBytesUntil('\n', buffer_ptr, BUFFER_SIZE);
          client.write('\n');
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
