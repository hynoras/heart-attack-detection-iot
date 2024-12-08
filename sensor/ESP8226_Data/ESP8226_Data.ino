#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>
#include <Wire.h>
#include "MAX30105.h"
#include "heartRate.h"
#include <ESP8266HTTPClient.h>  
#include <ArduinoJson.h>        


#define WIFI_SSID "Thanh Cong"
#define WIFI_PSWD "19962002"


#define ECG_PIN A0
#define RATE_SIZE 4

MAX30105 particleSensor;
ESP8266WebServer server(80);

byte rates[RATE_SIZE];
byte rateSpot = 0;
long lastBeat = 0;
float beatsPerMinute;
int beatAvg;

unsigned long lastPostTime = 0;
const unsigned long POST_INTERVAL = 60000;

void setupWiFiServer();
void setupECG();
void setupMAX30105();
void handleServer();
void handleECG();
void handleBPM();
void postHeartbeatToAPI(int irValue, float bpm, int avgBpm, int ecgValue);

void setup() {
    Serial.begin(115200);

    setupWiFiServer();
    setupECG();
    setupMAX30105();
}

void loop() {
    handleServer();
    handleBPM();
    handleECG();
}

void setupWiFiServer() {
    WiFi.begin(WIFI_SSID, WIFI_PSWD);
    Serial.print("Connecting to WiFi ");
    Serial.print(WIFI_SSID);

    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }
    Serial.println("\nConnected!");
    Serial.print("IP Address: ");
    Serial.println(WiFi.localIP());

    server.on("/", []() {
        server.send(200, "text/plain", "Hello from ESP8266!");
    });

    server.on("/status", []() {
        server.send(200, "application/json", "{\"status\":\"OK\",\"uptime\":" + String(millis()) + "}");
    });

    server.onNotFound([]() {
        server.send(404, "text/plain", "404: Not Found");
    });

    server.begin();
    Serial.println("HTTP server started!");
}

void setupECG() {
    pinMode(14, INPUT);
    pinMode(12, INPUT);
    Serial.println("ECG setup complete.");
}

void setupMAX30105() {
    Serial.println("Initializing...");

    Wire.begin(D1, D2);

    if (!particleSensor.begin(Wire, I2C_SPEED_FAST)) {
        Serial.println("MAX30105 was not found. Please check wiring/power.");
        while (1);
    }
    Serial.println("Place your index finger on the sensor with steady pressure.");

    particleSensor.setup();
    particleSensor.setPulseAmplitudeRed(0x0A);
    particleSensor.setPulseAmplitudeGreen(0);
}

void handleServer() {
    server.handleClient();
}

void handleECG() {
    if (digitalRead(10) == 1 || digitalRead(11) == 1) {
        Serial.println("Leads off detected!");
    } else {
        int ecgValue = analogRead(ECG_PIN);
        Serial.print("[ECG] ");
        Serial.println(ecgValue);
    }
    delay(10);
}

void handleBPM() {
    long irValue = particleSensor.getIR();

    if (irValue > 50000 && checkForBeat(irValue) == true) {
        long delta = millis() - lastBeat;
        lastBeat = millis();

        beatsPerMinute = 60 / (delta / 1000.0);

        if (beatsPerMinute < 255 && beatsPerMinute > 20) {
            rates[rateSpot++] = (byte)beatsPerMinute;
            rateSpot %= RATE_SIZE;

            beatAvg = 0;
            for (byte x = 0; x < RATE_SIZE; x++) {
                beatAvg += rates[x];
            }
            beatAvg /= RATE_SIZE;
        }
    } else if (irValue < 50000) {
        beatsPerMinute = 0;
        beatAvg = 0;
        for (byte x = 0; x < RATE_SIZE; x++) {
            rates[x] = 0;
        }
        Serial.print(" No finger?");
    }

    Serial.print("IR=");
    Serial.print(irValue);
    Serial.print(", BPM=");
    Serial.print(beatsPerMinute);
    Serial.print(", Avg BPM=");
    Serial.println(beatAvg);

    int ecgValue = analogRead(ECG_PIN);
    postHeartbeatToAPI(irValue, beatsPerMinute, beatAvg, ecgValue);
}


void postHeartbeatToAPI(int irValue, float bpm, int avgBpm, int ecgValue) {
    if (millis() - lastPostTime >= POST_INTERVAL) {
        WiFiClient client;
        HTTPClient http;

        String serverPath = "http://192.168.100.123:5000/api/send-to-predict-api"; 
        // http://192.168.100.123:5000/api/send-to-predict-api
        // http://192.168.1.17:5000/api/add-heartbeat

        StaticJsonDocument<200> jsonData;
        jsonData["IR"] = irValue;
        jsonData["thalachh"] = bpm;
        jsonData["AvgBPM"] = avgBpm;
        jsonData["restecg"] = ecgValue;

        String jsonString;
        serializeJson(jsonData, jsonString);

        http.begin(client, serverPath);
        http.addHeader("Content-Type", "application/json");

        int httpResponseCode = http.POST(jsonString);

        if (httpResponseCode > 0) {
            Serial.print("POST response: ");
            Serial.println(httpResponseCode);
        } else {
            Serial.print("Error sending POST: ");
            Serial.println(http.errorToString(httpResponseCode).c_str());
        }

        http.end();
        lastPostTime = millis();
    }
}