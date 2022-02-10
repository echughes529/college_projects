#include <Wire.h>   // I2C library
#define RMI2C_ADD 0x20    // RM3100 slave address is 0x20, 0b0100000
#include <Adafruit_MCP4728.h>   // DAC library
Adafruit_MCP4728 mcp;   


int DRDYpin = 13;
int DRDYstate = 0;
long xv, yv, zv;
float max_reading = 5000; // Maximum value is 8388607 (corresponding to 800 microTesla)
float max_output_voltage = 1.0; // Maximum output voltage is 3.3V


void initiateSM();
void confirmDataReady();
void readMeasurementResults();
long processResult();
void sendResultsToDAC();


void setup() {
  pinMode(DRDYpin, INPUT);
  Wire.begin(); // 100kHz default
  mcp.begin();
  Serial.begin(115200);
}

void loop() {
   initiateSM(RMI2C_ADD);
   //confirmDataReady(RMI2C_ADD);
   readMeasurementResults(RMI2C_ADD);
   sendResultsToDAC(xv, yv, zv);  
}

// Initiating single measurement mode
void initiateSM (byte i2Address){
  Wire.beginTransmission(i2Address);
  Wire.write(byte(0b00000000)); // The POLL register
  Wire.write(byte(0b01110000)); // Requesting measurements from all 3 axes
  Wire.endTransmission();
  delay(50); // Need a delay to give DRDY pin time to become HIGH
}

// Optional step to confirm data is ready to collect
void confirmDataReady (byte i2Address){
  DRDYstate = digitalRead(DRDYpin);
  if (DRDYstate == HIGH){
    Serial.println("Data is ready");
  }
  else {
    Serial.println("Error: no data available");
  }
}


void readMeasurementResults(byte i2Address){
  Wire.beginTransmission(i2Address);
  Wire.write(0b00100100); // The MX2 Address (automatically increments), obtaining readings from all axes
  Wire.endTransmission();
  delay(1);
  
  Wire.requestFrom(RMI2C_ADD, 9); // Request 9 bytes (covering all 3 axis registers- each register has 3 bytes) 

    if (9 <= Wire.available()) {
        xv = Wire.read();   // receive highest byte (overwrites previous reading)
        xv = xv << 8;       // shift high byte to be higher 8 bits
        xv |= Wire.read();  // receive low byte as lower 8 bits
        xv = xv << 8;       // shift high bytes to be higher 16 bits
        xv |= Wire.read();  // receive low byte as lower 8 bits
// C gives you an arithmetic shift to the right not a logic shift to the right
        xv = xv << 8;
        xv = xv >> 8;

        yv = Wire.read(); 
        yv = yv << 8;    
        yv |= Wire.read();
        yv = yv << 8;    
        yv |= Wire.read();
        yv = yv << 8;
        yv = yv >> 8;

        zv = Wire.read(); 
        zv = zv << 8;    
        zv |= Wire.read();
        zv = zv << 8;    
        zv |= Wire.read();
        zv = zv << 8;
        zv = zv >> 8;
    }
      // Printing raw data
      Serial.print("Raw Data: ");
      Serial.print(xv);
      Serial.print("  ");
      Serial.print(yv);
      Serial.print("  ");
      Serial.print(zv);
      Serial.println("  ");
}

long processResult(long reading){
  // Ensuring Results are within range stated for RM3100 results
  if (reading < -1 * max_reading){
    reading = -1 * max_reading;
  }
  else if (reading > max_reading){
    reading = max_reading;
  }
  else {
    reading = reading;
  }
  // Converting results to be in DAC input range
  long result = (reading + max_reading) * (max_output_voltage * (4095.0/3.3)/(2.0 * max_reading));
  return result;
}

      
void sendResultsToDAC(long x_reading, long y_reading, long z_reading){

      // Converting results to be processable by DAC
      long x_result = processResult(x_reading);
      long y_result = processResult(y_reading);
      long z_result = processResult(z_reading);

      // Printing DAC inputs
      Serial.print("DAC inputs: ");
      Serial.print(x_result);
      Serial.print(" ");
      Serial.print(y_result);
      Serial.print(" ");
      Serial.println(z_result);

      // Sending results to DAC
      mcp.setChannelValue(MCP4728_CHANNEL_A, x_result);
      mcp.setChannelValue(MCP4728_CHANNEL_B, y_result);
      mcp.setChannelValue(MCP4728_CHANNEL_C, z_result);
}


      
