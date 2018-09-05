int data;

void setup() {
    Serial.begin(115200);  // open serial connection to USB Serial port (connected to your computer)
    Serial1.begin(57600);  // open internal serial connection to MT7688AN
                           // in MT7688AN, this maps to device
    pinMode(13, OUTPUT);
    pinMode(18, INPUT);
    Serial.println("<READY>");
    }
 
void loop() {
    //Serial.println(analogRead(18));
    data = analogRead(18);
    Serial.print("FLEX sends ... ");
    Serial.println(data);
    Serial1.print(data);

    if (Serial1.available() > 0) {
       Serial.print("MPU sends ... ");
       Serial.println((char)Serial1.read());
    }
 
    delay(100);
} 
