#include <ESP8266WiFi.h>
#include <WebSocketsClient.h>

const char* ssid = "your_wifi_name";
const char* password = "your_wifi_password";

const char* serverAddress = "192.168.1.100";
const int serverPort = 8765;

WebSocketsClient webSocket;

void webSocketEvent(WStype_t type, uint8_t *payload, size_t length) {
    switch(type) {
        case WStype_CONNECTED:
            Serial.println("Connected to WebSocket server!");
            webSocket.sendTXT("Hello from Robot!");
            break;
        case WStype_TEXT:
            Serial.printf("Received from server: %s\n", payload);
            break;
        case WStype_DISCONNECTED:
            Serial.println("Disconnected!");
            break;
    }
}

void setup() {
    Serial.begin(115200);
    WiFi.begin(ssid, password);
    
    while (WiFi.status() != WL_CONNECTED) {
        delay(1000);
        Serial.println("Connecting...");
    }
    
    Serial.println("Connected to WiFi!");

    webSocket.begin(serverAddress, serverPort, "/");
    webSocket.onEvent(webSocketEvent);
}

void loop() {
    webSocket.loop();
    
    String data = "Temperature: " + String(random(20, 30)) + "°C";
    webSocket.sendTXT(data);
    
    delay(5000);
}