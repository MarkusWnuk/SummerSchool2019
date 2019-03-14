#include "Arduino.h"
#include <PubSubClient.h>
#include <string>
#include <WiFi.h> //Wifi library
#include "esp_wpa2.h" //wpa2 library for connections to Enterprise networks

#include <elapsedMillis.h>


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
 
 int flex_pin1 = 36; // pen sensor 
 int flex_pin2 = 37;  
 int flex_pin3 = 38;
 int flex_pin4 = 39;
 int series_R = 150;

long loopcount=0;

WiFiClient espClient;
PubSubClient client(espClient);

//const char* mqtt_server = "130.216.153.37";
const char* mqtt_server = "192.169.1.3";

void setup () {
  pinMode(LED_BUILTIN, OUTPUT);


   pinMode(flex_pin1, INPUT);
   pinMode(flex_pin2, INPUT);
   pinMode(flex_pin3, INPUT);
   pinMode(flex_pin4, INPUT);

  Serial.begin(9600);
  delay(10);
  #if USE_WIFI
  Serial.println();
  Serial.print("Connecting to network: ");
  Serial.println(ssid);
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
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
    counter++;
    if(counter>=60){ //after 30 seconds timeout - reset board
      ESP.restart();
    }
  }
  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address set: "); 
  Serial.println(WiFi.localIP()); //print LAN IP

  client.setServer(mqtt_server, 1883);
  client.connect("pen");
  #else
  Serial.begin(9600);
  #endif
}

const int window_size=15;
int w1[window_size]={0};
int w2[window_size]={0};
int w3[window_size]={0};
int w4[window_size]={0};

int flex_value1;
int flex_value2;
int flex_value3;
int flex_value4;


float wx[window_size]={0};
float wy[window_size]={0};

char json_string[64];

elapsedMillis timeElapsed; //declare global if you don't want it reset every time loop runs
// delay in milliseconds between blinks of the LED
unsigned int interval = 7;

void loop() {
 
#if USE_WIFI
  if (WiFi.status() == WL_CONNECTED) { //if we are connected to Eduroam network
    counter = 0; //reset counter
    //Serial.println("Wifi is still connected with IP: "); 
    //Serial.println(WiFi.localIP());   //inform user about his IP address
  }else if (WiFi.status() != WL_CONNECTED) { //if wed lost connection, retry
    WiFi.begin(ssid);      
  }
  while (WiFi.status() != WL_CONNECTED) { //during lost connection, print dots
    delay(50);
    //Serial.print(".");
    counter++;
    if(counter>=60){ //30 seconds timeout - reset board
    ESP.restart();
    }
  }
  if (!client.connected()) {
    //reconnect();
  }

#endif
//Reading Flex sensor data
flex_value1 = analogRead(flex_pin1);
flex_value2= analogRead(flex_pin2);
flex_value3 = analogRead(flex_pin3);
flex_value4= analogRead(flex_pin4);



w1[loopcount%window_size]=flex_value1;
w2[loopcount%window_size]=flex_value2;
w3[loopcount%window_size]=flex_value3;
w4[loopcount%window_size]=flex_value4;

int sum1=0;
int sum2=0;
int sum3=0;
int sum4=0;

for(int i = 0; i < window_size; i++)
{
  sum1+=w1[i];
  sum2+=w2[i];
  sum3+=w3[i];
  sum4+=w4[i];
}

float ave1=float(sum1)/window_size;
float ave2=float(sum2)/window_size;
float ave3=float(sum3)/window_size;
float ave4=float(sum4)/window_size;

loopcount++;


float flexF1 = (ave1-2307)/-199.300; 
float flexF2 = (ave2-2765)/-204.400;
float flexF3 = (ave3-2500)/-192.700;
float flexF4 = (ave4-2528)/-205.300;

float th1=0.15;
float th2=0.15;
float th3=0.15;
float th4=0.15;

float Fx=0;
float Fy=0;

if ((flexF1>th1) && (flexF1 > flexF3))
{
  Fx=flexF1;
}
if ((flexF3>th3) && (flexF3 > flexF1))
{
  Fx=-flexF3;
}

if ((flexF2>th2) && (flexF2 > flexF4))
{
  Fy=flexF2;
}
if ((flexF4>th4) && (flexF4 > flexF2))
{
  Fy=-flexF4;
}

wx[loopcount%window_size]=Fx;
wy[loopcount%window_size]=Fy;

float sumx=0;
float sumy=0;

for(int i = 0; i < window_size; i++)
{
  sumx+=wx[i];
  sumy+=wy[i];  
}

float avex=sumx/window_size;
float avey=sumy/window_size;

 if (timeElapsed > interval) 
  {				
      sprintf(json_string,"{\"Fx\": %f,\"Fy\":%f}",avex,avey);

      #if USE_WIFI
      client.loop();
      client.publish("Flex_pen",json_string);
      #else
      Serial.println(json_string);
      //delay(100);
      #endif
      digitalWrite(LED_BUILTIN, !digitalRead(LED_BUILTIN));
      timeElapsed = 0;              // reset the counter to 0 so the counting starts over...
  }
}