#include <ArduinoJson.h>
#include <MQTT.h>
#include "DHT.h"
#include <WiFi.h>

#define AWS_IOT_SUBSCRIBE_TOPIC "Sthelse"
#define DHTTYPE DHT11
// libraries used : https://www.arduino.cc/reference/en/libraries/mqtt/
// https://arduinojson.org/
// adafruit/DHT sensor library
// adafruit/Adafruit Unified Sensor

const int DIGITAL_IN_PIN = 4;
DHT dht(DIGITAL_IN_PIN, DHTTYPE);
WiFiClient net;
MQTTClient client = MQTTClient(256);

const char IOT_PUBLISH_TOPIC[] = "Test";
const char *ntpServer = "pool.ntp.org";
// const char ENDPOINT_URL[] = "192.168.0.104";
const char ENDPOINT_URL[] = "23.23.19.38";

#define THINGNAME "SomeThing"

const char WIFI_SSID[] = "wifi_name_goes_here";
const char WIFI_PASSWORD[] = "wifi_password_goes_here";

void connectAWS()
{
  WiFi.mode(WIFI_STA);
  Serial.println();
  Serial.println("******************************************************");
  Serial.print("Connecting to ");
  Serial.println(WIFI_SSID);

  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());

  // Connect to the MQTT broker on the AWS endpoint we defined earlier
  client.begin(ENDPOINT_URL, 1883, net);

  // Create a message handler
  client.onMessage(messageHandler);

  Serial.print("Connecting to AWS IOT");

  while (!client.connect(THINGNAME, "user", "password"))
  {
    Serial.print(".");
    delay(100);
  }

  if (!client.connected())
  {
    Serial.println("AWS IoT Timeout!");
    return;
  }

  // Subscribe to a topic
  client.subscribe(AWS_IOT_SUBSCRIBE_TOPIC);

  Serial.println("IoT MQTT Connected!");
  Serial.println(client.connected());
}

// Function that gets current epoch time
unsigned long getTime()
{
  time_t now;
  struct tm timeinfo;
  if (!getLocalTime(&timeinfo))
  {
    // Serial.println("Failed to obtain time");
    return (0);
  }
  time(&now);
  return now;
}

void publishMessage(int moisture, unsigned long myTime, float humidity, float temp_celsius)
{
  StaticJsonDocument<200> doc;
  doc["moisture"] = moisture;
  doc["timestamp"] = myTime;
  doc["humidity"] = humidity;
  doc["temp_celsius"] = temp_celsius;
  char jsonBuffer[512];
  serializeJson(doc, jsonBuffer); // print to client

  client.publish(IOT_PUBLISH_TOPIC, jsonBuffer);
}

void messageHandler(String &topic, String &payload)
{
  Serial.println("incoming: " + topic + " - " + payload);

  //  StaticJsonDocument<200> doc;
  //  deserializeJson(doc, payload);
  //  const char* message = doc["message"];
}

const int ANALOG_IN_PIN = 32;
int pin_value = 0;
int num_ticks = 0;
int curr_pin_value = 0;
hw_timer_t *my_timer;
float h;
float t;
void setup()
{
  // put your setup code here, to run once:
  Serial.begin(115200);
  connectAWS();
  my_timer = timerBegin(0, 80, true);
  pinMode(DIGITAL_IN_PIN, INPUT);
  pinMode(ANALOG_IN_PIN, INPUT);
  dht.begin();
  configTime(0, 0, ntpServer);
}

void loop()
{
  // put your main code here, to run repeatedly:

  if (timerReadSeconds(my_timer) >= 2)
  {
    unsigned long myTime = getTime();

    h = dht.readHumidity();
    t = dht.readTemperature(); /*Read default temperature in Celsius*/
    if (isnan(h) || isnan(t))
    { /*if condition to check all reading taken or not*/
      Serial.println(F("Failed to read from DHT sensor!"));
      h = 0;
      t = 0;
      // return;
    }
    Serial.print(pin_value);
    Serial.print(" ");
    Serial.print(num_ticks);
    Serial.print(" ");
    Serial.println(analogRead(ANALOG_IN_PIN));
    Serial.print("Soil Moisture: ");
    Serial.print(pin_value / num_ticks);
    Serial.print(F("  Humidity: ")); /*prints humidity value*/
    Serial.print(h);
    Serial.print(F("%  Temperature: "));
    Serial.print(t);
    Serial.println(F("°C ")); /*prints temperature in Celsius*/
    publishMessage(pin_value / num_ticks, myTime, h, t);
    pin_value = analogRead(ANALOG_IN_PIN);
    num_ticks = 1;
    timerRestart(my_timer);
    client.loop();
  }
  else
  {
    pin_value += analogRead(ANALOG_IN_PIN);
    num_ticks += 1;
    delay(100);
  }
}
