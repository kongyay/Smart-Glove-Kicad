
void printSerial1(bool showAcc)
{   
  if(showAcc) {
    Serial1.print(accel_x);
    Serial1.print(" ");
    Serial1.print(accel_y);
    Serial1.print(" ");
    Serial1.print(accel_z);
    Serial1.print("|");
    
    Serial1.print(gyro_x);
    Serial1.print(" ");
    Serial1.print(gyro_y);
    Serial1.print(" ");
    Serial1.print(gyro_z);
    Serial1.print("|");

    Serial1.print(magnetom_x);
    Serial1.print(" ");
    Serial1.print(magnetom_y);
    Serial1.print(" ");
    Serial1.print(magnetom_z);
    Serial1.print("|");
  }
    
    Serial1.print(flex[0]);
    Serial1.print(" ");
    Serial1.print(flex[1]);
    Serial1.print(" ");
    Serial1.print(flex[2]);
    Serial1.print(" ");
    Serial1.print(flex[3]);
    Serial1.print(" ");
    Serial1.println(flex[4]);
}


void printSerial(bool showAcc)
{   
  if(showAcc) 
    //Serial.print("[A]:\t");
    Serial.print(accel_x);
    Serial.print("\t");
    Serial.print(accel_y);
    Serial.print("\t");
    Serial.print(accel_z);
    Serial.print("\t");

    //Serial.print("[G]:\t");
    Serial.print(gyro_x);
    Serial.print("\t");
    Serial.print(gyro_y);
    Serial.print("\t");
    Serial.print(gyro_z);
    Serial.print("\t");

    //Serial.print("[M]:\t");
    Serial.print(magnetom_x);
    Serial.print("\t");
    Serial.print(magnetom_y);
    Serial.print("\t");
    Serial.print(magnetom_z);
    Serial.print("\t");
  
    
    //Serial.print("[F]:\t");
    Serial.print(flex[0]);
    Serial.print("\t");
    Serial.print(flex[1]);
    Serial.print("\t");
    Serial.print(flex[2]);
    Serial.print("\t");
    Serial.print(flex[3]);
    Serial.print("\t");
    Serial.println(flex[4]);
}
