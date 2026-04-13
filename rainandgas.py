#define BLYNK_TEMPLATE_NAME "Home Safety1"
#define BLYNK_TEMPLATE_ID "TMPL3EuyxLYYi"
#define BLYNK_AUTH_TOKEN "UMKDHXIOlRqpRhSOugVnJ4ZXpI-2bRo7"
char ssid[] = "nag";                                                  
char pass[] = "nageswari";
#define MQ2_SENSOR    D0 //A0
#define RAIN_SENSOR   D1  //D1
#define GREEN_LED     D5 //D5 
#define RED_LED       D7 //D7
#define WIFI_LED      16
#define BLYNK_PRINT Serial
#include <ESP8266WiFi.h>
#include <BlynkSimpleEsp8266.h>
int MQ2_SENSOR_Value = 0;
int RAIN_SENSOR_Value = 0;
bool isconnected = false;
char auth[] = BLYNK_AUTH_TOKEN;
#define VPIN_BUTTON_1    V1 
#define VPIN_BUTTON_2    V2
BlynkTimer timer;
void checkBlynkStatus() { // called every 2 seconds by SimpleTimer
 getSensorData();
  isconnected = Blynk.connected();
  if (isconnected == true) {
    digitalWrite(WIFI_LED, LOW);
    sendSensorData();
    Serial.println("Blynk Connected");
  }
  else{
    digitalWrite(WIFI_LED, HIGH);
    Serial.println("Blynk Not Connected");
  }
}
void getSensorData()
{
  MQ2_SENSOR_Value = map(analogRead(MQ2_SENSOR), 0, 1024, 0, 100);
  MQ2_SENSOR_Value = analogRead(MQ2_SENSOR);
  RAIN_SENSOR_Value = digitalRead(RAIN_SENSOR);
  Serial.print("MQ2:: ");
  Serial.println(MQ2_SENSOR_Value);
  Serial.print("Rain:: ");
  Serial.println(RAIN_SENSOR_Value);
  if (MQ2_SENSOR_Value == 0 || RAIN_SENSOR_Value == 0 ){
    digitalWrite(GREEN_LED, LOW);
    digitalWrite(RED_LED, HIGH);
  } else{
    digitalWrite(GREEN_LED, HIGH);
    digitalWrite(RED_LED, LOW);
  }
  delay(1500);
}
void sendSensorData()
{  
  Blynk.virtualWrite(VPIN_BUTTON_1, MQ2_SENSOR_Value);
 if (MQ2_SENSOR_Value == 0)
  {
    Blynk.logEvent("gas", "Gas Detected!");
    Blynk.virtualWrite(VPIN_BUTTON_1, "gas detected!");
  }
  if (RAIN_SENSOR_Value == 0 )
  {
    Blynk.logEvent("rain", "Water Detected!");
    Blynk.virtualWrite(VPIN_BUTTON_2, "Water Detected!");
  }
  else if (RAIN_SENSOR_Value == 1 )
  {
    Blynk.virtualWrite(VPIN_BUTTON_2, "No Water Detected.");
  } 
}void setup()
{
 Serial.begin(9600);
  pinMode(MQ2_SENSOR, INPUT);
  pinMode(RAIN_SENSOR, INPUT);
  pinMode(GREEN_LED, OUTPUT);
  pinMode(RED_LED, OUTPUT);
  digitalWrite(GREEN_LED, LOW);
  digitalWrite(RED_LED, LOW);
  WiFi.begin(ssid, pass);
  timer.setInterval(2000L, checkBlynkStatus);
  Blynk.config(auth);
  delay(1000);
}void loop(){
  getSensorData();
  Blynk.run();
  timer.run();
  delay(1000);
} 
