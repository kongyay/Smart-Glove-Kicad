void setup() {
    Serial.begin(115200);  // open serial connection to USB Serial port (connected to your computer)
    Serial1.begin(57600);  // open internal serial connection to MT7688AN
                           // in MT7688AN, this maps to device
    pinMode(13, OUTPUT);

    }
 
void loop() {

    digitalWrite(13,0);
    delay(1000);
    digitalWrite(13,1);
    delay(1000);
} 
