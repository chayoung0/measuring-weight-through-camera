#include "HX711.h"

// HX711 circuit wiring
const int LOADCELL_DOUT_PIN_1 = 13;
const int LOADCELL_SCK_PIN_1 = 12;
const int LOADCELL_DOUT_PIN_2= 11;
const int LOADCELL_SCK_PIN_2 = 10;
const int LOADCELL_DOUT_PIN_3 = 9;
const int LOADCELL_SCK_PIN_3 = 8;
const int LOADCELL_DOUT_PIN_4 = 7;
const int LOADCELL_SCK_PIN_4 = 6;

#define VCC2 5 // define pin 5 as VCC2
#define VCC3 4
#define VCC4 3
#define GND2 2 // define pin 2 as Ground 2

float x_max = 66.0; // width of the platform in centimeters
float y_max = 40.0; // height of the platform in centimeters

HX711 loadcell_1, loadcell_2, loadcell_3, loadcell_4;

void setup() {

  pinMode(VCC2,OUTPUT);//define a digital pin as output
  digitalWrite(VCC2, HIGH);// set the above pin as HIGH so it acts as 5V
  pinMode(VCC3,OUTPUT);//define a digital pin as output
  digitalWrite(VCC3, HIGH);// set the above pin as HIGH so it acts as 5V
  pinMode(VCC4,OUTPUT);//define a digital pin as output
  digitalWrite(VCC4, HIGH);// set the above pin as HIGH so it acts as 5V
  pinMode(GND2,OUTPUT);//define a digital pin as output
  digitalWrite(GND2, LOW);// set the above pin as LOW so it acts as Ground 
  
  Serial.begin(9600);

  float calibrationValue_1; // calibration value load cell 1, upper left
  float calibrationValue_2; // calibration value load cell 2, upper right
  float calibrationValue_3; // calibration value load cell 3, lower right
  float calibrationValue_4; // calibration value load cell 4, lower left
  calibrationValue_1 = 1900.0; // this values are obtained by calibrating the scale with known weights
  calibrationValue_2 = 1865.0; 
  calibrationValue_3 = 1850.0; 
  calibrationValue_4 = 1900.0;
  
  loadcell_1.begin(LOADCELL_DOUT_PIN_1, LOADCELL_SCK_PIN_1);
  loadcell_2.begin(LOADCELL_DOUT_PIN_2, LOADCELL_SCK_PIN_2);
  loadcell_3.begin(LOADCELL_DOUT_PIN_3, LOADCELL_SCK_PIN_3);
  loadcell_4.begin(LOADCELL_DOUT_PIN_4, LOADCELL_SCK_PIN_4);

  Serial.println("Setting up the tare weight...");
  loadcell_1.tare();
  loadcell_2.tare();
  loadcell_3.tare();
  loadcell_4.tare();

  Serial.println("Calibrating...");
  loadcell_1.set_scale(calibrationValue_1);
  loadcell_2.set_scale(calibrationValue_2);
  loadcell_3.set_scale(calibrationValue_3);
  loadcell_4.set_scale(calibrationValue_4);
  
}

void loop() {
  if (loadcell_1.is_ready() && loadcell_2.is_ready() && loadcell_3.is_ready() && loadcell_4.is_ready()) {
    long reading_1 = loadcell_1.get_units(5); // the average of 5 readings from the loadcell minus tare weight, divided by the SCALE parameter set with set_scale
    long reading_2 = loadcell_2.get_units(5);
    long reading_3 = loadcell_3.get_units(5);
    long reading_4 = loadcell_4.get_units(5);
    long total_weight = reading_1 + reading_2 + reading_3 + reading_4;
    float x_coordinate = (reading_2 + reading_3)*x_max/total_weight;
    float y_coordinate = (reading_3 + reading_4)*y_max/total_weight;
    Serial.print("HX711 readings: ");
    Serial.print(reading_1);
    Serial.print("\t");
    Serial.print(reading_2);
    Serial.print("\t");
    Serial.print(reading_3);
    Serial.print("\t");
    Serial.print(reading_4);
    Serial.print("\t");
    Serial.print("Total weight: ");
    Serial.print(total_weight);
    Serial.print("\t|\tPosition as (x,y): ");
    //Serial.print("(");
    Serial.print(x_coordinate);
    Serial.print(",");
    Serial.println(y_coordinate);
    //Serial.println(")");
  } else {
    Serial.println("HX711 not found.");
  }

  delay(3000);
}
