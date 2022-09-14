#include <Arduino.h>
#include <HTTPClient.h>         // HTTPClient
#include "credentials.h"        // Credentials and other secrets 
#include <WiFi.h>               // WiFi client
#include "time.h"               // Time
#include <ArduinoJson.h>        // For JSON parsing
#include <Adafruit_Sensor.h>    // Sensor library
#include <Wire.h>               // Aaaaah... wire..!
#include "DHT.h"                // temperature sensor
#include <Adafruit_GFX.h>       // GFX for OLED
#include <Adafruit_SSD1306.h>   // Lib for OLED

//Definitions
#define ONBOARD_LED  2
#define DHTPIN 19
#define DHTTYPE DHT22

#define SCREEN_WIDTH 128 // OLED display width, in pixels
#define SCREEN_HEIGHT 64 // OLED display height, in pixels

// Initialize sensor(s)
DHT dht(DHTPIN, DHTTYPE);
Adafruit_SSD1306 display(-1);


// Millis specifications for timing
unsigned long startMillis;  //some global variables available anywhere in the program
unsigned long currentMillis;
const unsigned long period = 600000 ;  //the value is a number of milliseconds

const char* ntpServer = "pool.ntp.org";
const long  gmtOffset_sec = 0;
const int   daylightOffset_sec = 0; // Use UTC time 

// Instantiate HTTP Client
HTTPClient http;
WiFiClient client;  // or WiFiClientSecure for HTTPS

void blinkLed() {
  digitalWrite(ONBOARD_LED,HIGH);
  delay(100);
  digitalWrite(ONBOARD_LED,LOW);
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

// Function to make post requests 
void makePostRequestTemperature(String time, float tempCelsius, float humid) {

  // Include sender unit? Probably a good idea, but API models should be rewritten

  // Create JSON
  DynamicJsonDocument doc(2048);

  doc["dateTimeUtc"] = String(time);
  doc["temperatureCelcius"] = tempCelsius;
  doc["humidityPercentage"] = humid;

  // Serialize JSON document
  String requestBody;
  serializeJson(doc, requestBody);

  // Send request
  String requestPath = apiBaseUrl + "/temperature/add";
  http.begin(client, requestPath);
  http.addHeader("Content-Type", "application/json");  

  int httpResponseCode  = http.POST(requestBody);
}

void setup() {

  // Initializations
  Serial.begin(9600);

  // Initializations
  Wire.begin();
  dht.begin();

  // Begin millis for function timing
  startMillis = millis();  //initial start time

  // Connect to WiFi
  connectToWifi();

  // Init and get the time
  configTime(gmtOffset_sec, daylightOffset_sec, ntpServer);
  String currentTime = getCurrentTime();

  // Display setup
	display.begin(SSD1306_SWITCHCAPVCC, 0x3C);  

  // Display Text
	display.setTextSize(1);
	display.setTextColor(WHITE);
	display.setCursor(0,28);
	display.println("Booting...");
	display.display();
	delay(2000);
	display.clearDisplay();

	// Clear the buffer.
	display.clearDisplay();
}

void loop() {
  

  // Time variables
  String currentTime = getCurrentTime();  // Current time in UTC
  currentMillis = millis();               // Current millis time

  // Save sensor data
  float tempCelsius = dht.readTemperature();        // Temperature
  float humid = dht.readHumidity();                 // Humidity

  // Do this every 15 minutes - rest should be real time data
  if (currentMillis - startMillis >= period) {
    makePostRequestTemperature(
      currentTime, 
      tempCelsius, 
      humid
      );
    blinkLed();
    startMillis = currentMillis;  // Update time
  }

  // Display Text
	display.setTextSize(1);
	display.setTextColor(WHITE);
	display.setCursor(0,0);
  display.println(currentTime);
	display.println("Temperature:\t" + String(tempCelsius)+ "C");
  display.println("Humidity:\t" + String(humid) + "%");
	display.display();
  display.clearDisplay();

}