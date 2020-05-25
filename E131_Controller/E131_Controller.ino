/*
  ESP8266_NeoPixel.ino - Simple sketch to listen for E1.31 data on an ESP8266
                         and drive WS2811 LEDs using the NeoPixel Library

  == Requires Adafruit_NeoPixel - http://github.com/adafruit/Adafruit_NeoPixel

  Project: E131 - E.131 (sACN) library for Arduino
  Copyright (c) 2015 Shelby Merrick
  http://www.forkineye.com

   This program is provided free for you to use in any way that you wish,
   subject to the laws and regulations where you are using it.  Due diligence
   is strongly suggested before using this code.  Please give credit where due.

   The Author makes no warranty of any kind, express or implied, with regard
   to this program or the documentation contained in this document.  The
   Author shall not be liable in any event for incidental or consequential
   damages in connection with, or arising out of, the furnishing, performance
   or use of these programs.

*/

#include <ESP8266WiFi.h>
#include <E131.h>
#include <Adafruit_NeoPixel.h>

#define NUM_PIXELS 300  /* Number of pixels */
#define UNIVERSE1 1      /* Universe1 to listen for */
#define UNIVERSE2 2      /* Universe2 to listen for */
#define CHANNEL_START 1 /* Channel to start listening at */
#define CHANNEL_START2 511 /* Channel to start listening at */
#define DATA_PIN 2      /* Pixel output - GPIO2 */
#define NUMBER_OF_UNIVERSES 1



const uint8_t kMatrixWidth = 16;

const char ssid[] = "Jurasic_Park";         /* Replace with your SSID */
const char passphrase[] = "nobodyExpectedThis";   /* Replace with your WPA2 passphrase */

E131 e131;

Adafruit_NeoPixel pixels = Adafruit_NeoPixel(NUM_PIXELS, DATA_PIN, NEO_GRB + NEO_KHZ800);

void setup() {
  Serial.begin(115200);
  delay(10);

  /* Choose one to begin listening for E1.31 data */
  //e131.begin(ssid, passphrase);                       /* via Unicast on the default port */
  e131.beginMulticast(ssid, passphrase, UNIVERSE1, NUMBER_OF_UNIVERSES);  /* via Multicast for Universe 1 */

  /* Initialize output */
  pixels.begin();
  pixels.show();
}


void setColorWithOrder(int ind, int red, int green, int blue) {
  if ((ind / kMatrixWidth) % 2 == 0) {
    //even row
    pixels.setPixelColor(ind, red , green, blue);
  } else {
    //uneven row
    pixels.setPixelColor(ind + kMatrixWidth - 1 - 2 * (ind % kMatrixWidth), red , green, blue);
  }
}

void loop() {
  /* Parse a packet and update pixels */
  if (e131.parsePacket()) {
    Serial.printf("Universe %u | Packet#: %u / Errors: %u / CH1: %u\n",
                         e131.universe,              // The Universe for this packet
                         e131.stats.num_packets,     // Packet counter
                         e131.stats.packet_errors,   // Packet error counter
                         e131.data[0]);              // Dimmer data for Channel 1
    
  if (e131.universe == UNIVERSE1) {
      for (int i = 0; i < 170; i++) {
        int j = i * 3 + (CHANNEL_START - 1);
        setColorWithOrder(i, e131.data[j], e131.data[j + 1], e131.data[j + 2]);
      }
      pixels.show();
    }

     /* if (e131.universe == UNIVERSE2) {
      for (int i = CHANNEL_START2/3; i < NUM_PIXELS; i++) {
        int j = i * 3 + (CHANNEL_START2 - 1);
        setColorWithOrder(i, e131.data[j], e131.data[j + 1], e131.data[j + 2]);
      }
      pixels.show();
    }*/
  }
}
