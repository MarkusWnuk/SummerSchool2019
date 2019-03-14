#include <Arduino.h>
#include "HX711.h"
#include <PubSubClient.h>
#include <WiFi.h> //Wifi library
#include "esp_wpa2.h" //wpa2 library for connections to Enterprise networks

#include "Adafruit_MQTT.h"
#include "Adafruit_MQTT_Client.h"

#define DOUT 34
#define CLK 33

#define USE_WIFI 1  
#define USE_WPA2_ENTERPRISE 0

#if USE_WPA2_ENTERPRISE

#define EAP_IDENTITY "jter048" //user
#define EAP_PASSWORD ".!Jps8C>E)Xd]" //UoA password
const char* ssid = "UoA-WiFi"; // UoA SSID
#else
const char* ssid = "IRTG_STR"; // UoA SSID
const char* password = "SummerSchool2019"; // UoA SSID
#endif

int counter = 0;
float calibration_factor = 41000;
float scaleval_fl = 0;
unsigned long previousMillis = 0;

HX711 scale(DOUT,CLK);

WiFiClient espClient;
PubSubClient client(espClient);
//const char* mqtt_server = "130.216.153.37";
const char* mqtt_server = "192.169.1.3";

void setup() {

  Serial.begin(9600);

  pinMode(LED_BUILTIN, OUTPUT);

  delay(10);

  WiFi.disconnect(true);  //disconnect form wifi to set new wifi connection
  WiFi.mode(WIFI_STA); //init wifi mode
  #if USE_WPA2_ENTERPRISE
  esp_wifi_sta_wpa2_ent_set_identity((uint8_t *)EAP_IDENTITY, strlen(EAP_IDENTITY)); //provide identity
  esp_wifi_sta_wpa2_ent_set_username((uint8_t *)EAP_IDENTITY, strlen(EAP_IDENTITY)); //provide username --> identity and username is same
  esp_wifi_sta_wpa2_ent_set_password((uint8_t *)EAP_PASSWORD, strlen(EAP_PASSWORD)); //provide password
  esp_wpa2_config_t config = WPA2_CONFIG_INIT_DEFAULT(); //set config settings to default
  esp_wifi_sta_wpa2_ent_enable(&config); //set config settings to enable function
  #endif
  WiFi.begin(ssid,password); //connect to wifi
  Serial.println("Wifi connected");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    //Serial.print(".");
    counter++;
    if(counter>=60){ //after 30 seconds timeout - reset board
      ESP.restart();
    }
  }

  client.setServer(mqtt_server, 1883);
  client.connect("scale");
  Serial.println("MQTT connected");
  Serial.println("Starting transmission");
  delay(1000);
  delay(1000);

  scale.set_scale(calibration_factor);
  scale.tare();
}

void loop() {

  unsigned long currentMillis = millis();

  scaleval_fl = scale.get_units();
  //scaleval_fl = 2;

  if (WiFi.status() == WL_CONNECTED) { //if we are connected to Eduroam network
    counter = 0; //reset counter
  }else if (WiFi.status() != WL_CONNECTED) { //if we lost connection, retry
    WiFi.begin(ssid);      
  }
  while (WiFi.status() != WL_CONNECTED) { //during lost connection, print dots
    delay(50);
    counter++;
    if(counter>=60){ //30 seconds timeout - reset board
    ESP.restart();
    }
  }
  //if (!client.connected()) {
    //reconnect();
  //}

client.loop();

char scaleval[64];
sprintf(scaleval, "{\"F_n\":%2.2f}",scaleval_fl);
client.publish("Force_n",scaleval);
digitalWrite(LED_BUILTIN, !digitalRead(LED_BUILTIN));

unsigned long diffMillis = currentMillis - previousMillis;
previousMillis = currentMillis;
Serial.println(diffMillis,7);

}