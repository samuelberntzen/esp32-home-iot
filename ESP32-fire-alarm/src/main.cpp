#include <Arduino.h>
#include <ArduinoJson.h>        // For JSON parsing
#include <HTTPClient.h>         // HTTPClient
#include <WiFi.h>               // WiFi client

// Onboard LED 
#define ONBOARD_LED  2

// IR Sensor parameters
const int flamePin = 13; 
int Flame = HIGH;

// NTP parameters
const char* ntpServer = "pool.ntp.org";
const long  gmtOffset_sec = 0;
const int   daylightOffset_sec = 0; // Use UTC time 

// Function to connect to WiFi
void connectToWifi() {

  // Connect to WiFi
  WiFi.begin(ssid, password);
  Serial.println("Connecting to " + String(ssid));
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("Successfully connected to " + String(ssid));
}

String getCurrentTime() {
  struct tm timeinfo;
  if(!getLocalTime(&timeinfo)){
    // Serial.println("Failed to obtain time");
    return "Failed to obtain time";
  }

  char currentTime [80];
  strftime(currentTime, 80, "%Y-%m-%d %H:%M:%S", &timeinfo);

  return currentTime;
}

// Function to make post requests 
void makePostRequestFireSensor(String time, float sensorReading) {

  // Include sender unit? Probably a good idea, but API models should be rewritten

  // Create JSON
  DynamicJsonDocument doc(2048);

  doc["utcTime"] = String(time);
  doc["isFire"] = sensorReading;

  // Serialize JSON document
  String requestBody;
  serializeJson(doc, requestBody);

  WiFiClient client;  // or WiFiClientSecure for HTTPS
  HTTPClient http;

  // Send request
  String requestPath = apiBaseUrl + "/fire/trigger/";
  http.begin(client, requestPath);
  http.addHeader("Content-Type", "application/json");  
  int httpResponseCode  = http.POST(requestBody);     // Content should be encrypted from client and decrypted in server

  Serial.println(http.errorToString(httpResponseCode ).c_str());

  // Close connection
  http.end();

  // Print request body to Serial
  Serial.println(requestBody);

}

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200); 
  pinMode(ONBOARD_LED,OUTPUT);
  pinMode(flamePin, INPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  int irReadings = digitalRead(flamePin);
  if (irReadings == 0){
    digitalWrite(ONBOARD_LED,HIGH); 

    // Perform procedure
    currentTime = getCurrentTime();

    // Post readings to API 
    // Notify using something

  }    
  else {
    digitalWrite(ONBOARD_LED, LOW);
  }
;
}