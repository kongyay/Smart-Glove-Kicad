// Wire Slave Receiver
// by Nicholas Zambetti <http://www.zambetti.com>

// Demonstrates use of the Wire library
// Receives data as an I2C/TWI slave device
// Refer to the "Wire Master Writer" example for use with this

// Created 29 March 2006

// This example code is in the public domain.


#include <Wire.h>

int flexPIN[5] = {18, 19, 20, 21, 22};
int flex[5];

void setup() {
  for (int y = 0; y < 5; y++)
    pinMode(flexPIN[y],INPUT);
    
  Wire.begin(8);                // join i2c bus with address #8
  Serial.begin(115200);           // start serial for output
}

void loop() {
  for (int i = 0; i < 5; i++) {
     flex[i] = analogRead(flexPIN[i]);
  }
  
  Wire.beginTransmission(8); // transmit to device #8
  Wire.write(flex[0]);
  Wire.write(",");
  Wire.write(flex[1]);
  Wire.write(",");
  Wire.write(flex[2]);
  Wire.write(",");
  Wire.write(flex[3]);
  Wire.write(",");
  Wire.write(flex[4]);
  Wire.write("\n");
  Wire.endTransmission();    // stop transmitting

  Serial.print(flex[0]);
    Serial.print("\t");
    Serial.print(flex[1]);
    Serial.print("\t");
    Serial.print(flex[2]);
    Serial.print("\t");
    Serial.print(flex[3]);
    Serial.print("\t");
    Serial.println(flex[4]);
    
  delay(20);
}
