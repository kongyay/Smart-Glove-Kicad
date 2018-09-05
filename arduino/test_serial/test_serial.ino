char receivedChar;
bool newData = false;

void setup() {
    Serial.begin(115200);  // open serial connection to USB Serial port (connected to your computer)
    Serial1.begin(57600);  // open internal serial connection to MT7688AN
                           // in MT7688AN, this maps to device
    pinMode(13, OUTPUT);
    pinMode(18, INPUT);
    Serial.println("<READY>");
    }
 
void loop() {
    Serial.println(analogRead(18));
    delay(100);
} 


void showNewData() {
 if (newData == true) {
 Serial.print("This just in ... ");
 Serial.println(receivedChar);
 newData = false;
 }
}
