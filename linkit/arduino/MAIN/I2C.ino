#include <LSM6.h>
#include <LIS3MDL.h>

LSM6 gyro_acc;
LIS3MDL mag;

void I2C_Init()
{
  Wire.begin();
}

void Gyro_Init()
{
  // Accel_Init() should have already called gyro_acc.init() and enableDefault()
  gyro_acc.writeReg(LSM6::CTRL2_G, 0x4C); // 104 Hz, 2000 dps full scale
}

void Read_Gyro()
{
  gyro_acc.readGyro();

  imuData[0] = gyro_acc.g.x;
  imuData[1] = gyro_acc.g.y;
  imuData[2] = gyro_acc.g.z;

  gyro_x = SENSOR_SIGN[0] * (imuData[0] - imuDataOffset[0]);
  gyro_y = SENSOR_SIGN[1] * (imuData[1] - imuDataOffset[1]);
  gyro_z = SENSOR_SIGN[2] * (imuData[2] - imuDataOffset[2]);
}

void Accel_Init()
{
  gyro_acc.init();
  gyro_acc.enableDefault();
  gyro_acc.writeReg(LSM6::CTRL1_XL, 0x3C); // 52 Hz, 8 g full scale
}

// Reads x,y and z accelerometer registers
void Read_Accel()
{
  gyro_acc.readAcc();

  imuData[3] = gyro_acc.a.x >> 4; // shift left 4 bits to use 12-bit representation (1 g = 256)
  imuData[4] = gyro_acc.a.y >> 4;
  imuData[5] = gyro_acc.a.z >> 4;

  accel_x = SENSOR_SIGN[3] * (imuData[3] - imuDataOffset[3]);
  accel_y = SENSOR_SIGN[4] * (imuData[4] - imuDataOffset[4]);
  accel_z = SENSOR_SIGN[5] * (imuData[5] - imuDataOffset[5]);
}

void Compass_Init()
{
  mag.init();
  mag.enableDefault();
}

void Read_Compass()
{
  mag.read();

  magnetom_x = SENSOR_SIGN[6] * mag.m.x;
  magnetom_y = SENSOR_SIGN[7] * mag.m.y;
  magnetom_z = SENSOR_SIGN[8] * mag.m.z;
}

void Calculate_Kalman()
{
delta_time = (micros() - timestamp) / 1000000;
 timestamp = micros();

//project the state ahead
 x = x - delta_time * GX;
 y = y - delta_time * GY;

//project the error covariance ahead
 float ptemp = 1.0;
 px = px + abs(px * delta_time * GX) * ptemp;
 py = py + abs(py * delta_time * GY) * ptemp;

//compute Kalman Gain
 kx = px / ( px + 0.003565444 );
 ky = py / ( py + 0.003565444 );

//Update estimate with measurement

x = x + kx * ( pitch - x);
 y = y + ky * (roll - y);
 //Update the error covariance
 px = (1 - kx) * px;
 py = (1 - ky) * py;

Serial.print(x);
Serial.print(" ");

Serial.print(y);
Serial.print(" ");
}

void Compass_Heading()
{
//  float MAG_X;
//  float MAG_Y;
//  float cos_roll;
//  float sin_roll;
//  float cos_pitch;
//  float sin_pitch;
//  
//  cos_roll = cos(roll);
//  sin_roll = sin(roll);
//  cos_pitch = cos(pitch);
//  sin_pitch = sin(pitch);
//  
//  // adjust for LSM303 compass axis offsets/sensitivity differences by scaling to +/-0.5 range
//  c_magnetom_x = (float)(magnetom_x - SENSOR_SIGN[6]*M_X_MIN) / (M_X_MAX - M_X_MIN) - SENSOR_SIGN[6]*0.5;
//  c_magnetom_y = (float)(magnetom_y - SENSOR_SIGN[7]*M_Y_MIN) / (M_Y_MAX - M_Y_MIN) - SENSOR_SIGN[7]*0.5;
//  c_magnetom_z = (float)(magnetom_z - SENSOR_SIGN[8]*M_Z_MIN) / (M_Z_MAX - M_Z_MIN) - SENSOR_SIGN[8]*0.5;
//  
//  // Tilt compensated Magnetic filed X:
//  MAG_X = c_magnetom_x*cos_pitch+c_magnetom_y*sin_roll*sin_pitch+c_magnetom_z*cos_roll*sin_pitch;
//  // Tilt compensated Magnetic filed Y:
//  MAG_Y = c_magnetom_y*cos_roll-c_magnetom_z*sin_roll;
//  // Magnetic Heading
//  MAG_Heading = atan2(-MAG_Y,MAG_X);
}
