/*
  The sensor outputs provided by the library are the raw 16-bit values
  obtained by concatenating the 8-bit high and low magnetometer data registers.
  They can be converted to units of gauss using the
  conversion factors specified in the datasheet for your particular
  device and full scale setting (gain).

  Example: An LIS3MDL gives a magnetometer X axis reading of 1292 with its
  default full scale setting of +/- 4 gauss. The GN specification
  in the LIS3MDL datasheet (page 8) states a conversion factor of 6842
  LSB/gauss (where LSB means least significant bit) at this FS setting, so the raw
  reading of 1292 corresponds to 1292 / 6842 = 0.1888 gauss.
*/

/*
  The sensor outputs provided by the library are the raw
  16-bit values obtained by concatenating the 8-bit high and
  low accelerometer and gyro data registers. They can be
  converted to units of g and dps (degrees per second) using
  the conversion factors specified in the datasheet for your
  particular device and full scale setting (gain).

  Example: An LSM6DS33 gives an accelerometer Z axis reading
  of 16276 with its default full scale setting of +/- 2 g. The
  LA_So specification in the LSM6DS33 datasheet (page 11)
  states a conversion factor of 0.061 mg/LSB (least
  significant bit) at this FS setting, so the raw reading of
  16276 corresponds to 16276 * 0.061 = 992.8 mg = 0.9928 g.
*/


#include <Wire.h>
#include <LIS3MDL.h>
#include <LSM6.h>
#define PERIOD 50
#define SAMPLE_SIZE 5
#define GRAVITY 256

int SENSOR_SIGN[9] = {1,1,1,-1,-1,-1,1,1,1}; //Correct directions x,y,z - gyro, accelerometer, magnetometer
int imuData[6]; //array that stores the gyro and accelerometer data
int imuDataOffset[6] = {0, 0, 0, 0, 0, 0}; //Array that stores the Offset of the sensors
int gyro_x;
int gyro_y;
int gyro_z;
int accel_x;
int accel_y;
int accel_z;
int magnetom_x;
int magnetom_y;
int magnetom_z;
float c_magnetom_x;
float c_magnetom_y;
float c_magnetom_z;
float MAG_Heading;

int flexPIN[5] = {18, 19, 20, 21, 22};
int sample[5][5];
int flex[5];


char report[160];
char debug[160];

void setup()
{
  pinMode(13, OUTPUT);
  pinMode(18, INPUT);

  for (int y = 0; y < 5; y++)
    pinMode(flexPIN[y],INPUT);

  Serial.begin(9600);
  Serial1.begin(57600);  // open internal serial connection to MT7688imuData
  while (!Serial)
    Serial.println("<Starting...>");

  I2C_Init();
  delay(1500);

  Accel_Init();
  Compass_Init();
  Gyro_Init();
  delay(20);

  for (int i = 0; i < 32; i++) // We take some readings...
  {
    Read_Gyro();
    Read_Accel();
    for (int y = 0; y < 6; y++) // Cumulate values
      imuDataOffset[y] += imuData[y];
    delay(20);
  }

  for (int y = 0; y < 6; y++)
    imuDataOffset[y] = imuDataOffset[y] / 32;

  imuDataOffset[5] -= GRAVITY * SENSOR_SIGN[5];

  Serial.println("Offset:");
  for (int y = 0; y < 6; y++)
    Serial.println(imuDataOffset[y]);

  delay(2000);

  for (int s = 0; s < SAMPLE_SIZE; s++) {
    for (int i = 0; i < 5; i++) {
      sample[i][s] = analogRead(flexPIN[i]);
    }
  }

  Serial.println("<READY>");
}


void loop()
{
  Read_Accel();
  Read_Gyro();
  Read_Compass();    // Read I2C magnetometer
  Compass_Heading(); // Calculate magnetic heading

  for (int s = 0; s < SAMPLE_SIZE; s++) {
    for (int i = 0; i < 5; i++) {
      if (s == SAMPLE_SIZE - 1) {
        sample[i][s] = analogRead(flexPIN[i]);
      } else {
        sample[i][s] = sample[i][s + 1];
        int sum = 0;
        for (int k = 0; k < SAMPLE_SIZE; k++) {
          sum += sample[i][k];
        }
        flex[i] = sum / SAMPLE_SIZE;
      }
    }
  }

  if (Serial1.available() > 0) {
    //Serial.print("MPU sends ... ");
    //Serial.println((char)Serial1.read());
  }

  printSerial(true);
  printSerial1(true);

  delay(PERIOD);

}
