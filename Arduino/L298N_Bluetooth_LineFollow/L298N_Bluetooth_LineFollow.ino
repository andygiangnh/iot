#include <SoftwareSerial.h>
#include <QTRSensors.h>

SoftwareSerial bluetoothSerial(12, 13); // RX, TX

QTRSensors qtr;
const uint8_t SensorCount = 5;
uint16_t sensorValues[SensorCount];
int manualCalibration = 0;

// PID Properties
const double KP = 0.15;
const double KI = 0.05;
const double KD = 0.32;
double lastError = 0;
double integral = 0;
const int GOAL = 2000;
int MAX_SPEED = 120;
int autoMode = 0;

int ena1 = 3;
int in1Pin = 4;
int in2Pin = 5;
int ena2 = 6;
int in3Pin = 7;
int in4Pin = 8;
char command;
int speed;
int turnSpeed;

// Kalman Filter constants and variables
double kalmanError = 0;
double P = 1;
const double Q = 0.1;
const double R = 0.1;
double K = 0;
double x = 0; // estimated error

void setup()
{
  pinMode(ena1, OUTPUT);
  pinMode(in1Pin, OUTPUT);
  pinMode(in2Pin, OUTPUT);

  pinMode(ena2, OUTPUT);
  pinMode(in3Pin, OUTPUT);
  pinMode(in4Pin, OUTPUT);

  pinMode(pump, OUTPUT);

  speed = 0;
  stop();
  
  Serial.begin(9600);
  bluetoothSerial.begin(9600);  //Set the baud rate to your Bluetooth module.

  // configure the sensors
  qtr.setTypeRC();
  qtr.setSensorPins((const uint8_t[]){A0, A1, A2, A3, A4}, SensorCount);
  qtr.setEmitterPin(2);

  delay(500);
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, HIGH); // turn on Arduino's LED to indicate we are in calibration mode

  if (manualCalibration)
  {
    uint16_t minVal[5] = {60,60,60,60,60};
    uint16_t maxVal[5] = {1244,1502,1448,1740,2040};
    qtr.calibrationOn.initialized = true;
    qtr.calibrationOn.minimum = (uint16_t *)realloc(qtr.calibrationOn.minimum,sizeof(uint16_t) * 5);
    qtr.calibrationOn.maximum = (uint16_t *)realloc(qtr.calibrationOn.maximum,sizeof(uint16_t) * 5);
    
    for (uint8_t i = 0; i < SensorCount; i++)
    {
      qtr.calibrationOn.minimum[i] = minVal[i];
      qtr.calibrationOn.maximum[i] = maxVal[i];
    }
  } else {
    Serial.println("Starting calibration...");
    calibrateLineSensor();
  } 
}

void calibrateLineSensor() {
  digitalWrite(LED_BUILTIN, HIGH); // indication of calibration start
    // 2.5 ms RC read timeout (default) * 10 reads per calibrate() call
    // = ~25 ms per calibrate() call.
    // Call calibrate() 400 times to make calibration take about 10 seconds.
    for (uint16_t i = 0; i < 400; i++)
    {
      qtr.calibrate();
    }
  
  digitalWrite(LED_BUILTIN, LOW); // turn off Arduino's LED to indicate we are through with calibration

  // print the calibration minimum values measured when emitters were on
  Serial.print("Minimum: ");
  for (uint8_t i = 0; i < SensorCount; i++)
  {
    Serial.print(qtr.calibrationOn.minimum[i]);
    Serial.print('\t');
  }
  Serial.println();
  //print the calibration maximum values measured when emitters were on
  Serial.print("Maximun: ");
  for (uint8_t i = 0; i < SensorCount; i++)
  {
    Serial.print(qtr.calibrationOn.maximum[i]);
    Serial.print('\t');
  }

  Serial.println();
}

void loop()
{
  if(autoMode > 0) {
    // Get line position
    unsigned int position = qtr.readLineBlack(sensorValues);

    // Compute error from line
    int error = GOAL - position;

    // Update Kalman Filter
    kalmanError = kalmanFilter(error);

    // Compute integral
    integral += kalmanError;

    // Compute motor adjustment
    int adjustment = KP*kalmanError + KI*integral + KD*(kalmanError - lastError);

    // Store error for next increment
    lastError = kalmanError;

    // Adjust motors 
    int leftOut = constrain(MAX_SPEED - adjustment, 0, MAX_SPEED);
    int rightOut = constrain(MAX_SPEED + adjustment, 0, MAX_SPEED);
    forwardTurn(leftOut, rightOut);
  }

  if (bluetoothSerial.available() > 0) {
    command = bluetoothSerial.read();
    
    Serial.println(command);

    if(speed == 0) {
      speed = 100;
    }
    Serial.print("Motor Speed="); Serial.println(speed);

    switch (command) {
      case 'X':
        autoMode = 1;
        break;
      case 'x':
        autoMode = 0;
        speed = 0;
        turnSpeed = 0;
        break;
      case 'V':
        calibrateLineSensor();
        break;
      case 'F':
        forward(speed);
        break;
      case 'B':
        back(speed);
        break;
      case 'R':
        right(speed);
        break;
      case 'L':
        left(speed);
        break;
      case 'G':
        turnSpeed = 0.25 * speed;
        forwardRight(speed, turnSpeed);
        break;
      case 'I':
        turnSpeed = 0.25 * speed;
        forwardLeft(speed, turnSpeed);
        break;
      case 'H':
        turnSpeed = 0.25 * speed;
        backRight(speed, turnSpeed);
        break;
      case 'J':
        turnSpeed = 0.25 * speed;
        backLeft(speed, turnSpeed);
        break;
      case '1':
        setSpeed(100);
        MAX_SPEED = 100;
        break;
      case '2':
        setSpeed(150);
        MAX_SPEED = 120;
        break;
      case '3':
        setSpeed(170);
        MAX_SPEED = 140;
        break;
      case '4':
        setSpeed(180);
        MAX_SPEED = 150;
        break;
      case '5':
        setSpeed(190);
        MAX_SPEED = 165;
        break;
      case '6':
        setSpeed(200);
        MAX_SPEED = 175;
        break;
      case '7':
        setSpeed(210);
        MAX_SPEED = 190;
        break;
      case '8':
        setSpeed(220);
        MAX_SPEED = 200;
        break;
      case '9':
        setSpeed(240);
        MAX_SPEED = 210;
        break;
      case 'q':
        setSpeed(255);
        MAX_SPEED = 220;
        break;
      default:
        stop();
    }
  }

}

double kalmanFilter(double error) {
  // Prediction update
  P = P + Q;

  // Measurement update
  K = P / (P + R);
  x = x + K * (error - x);
  P = (1 - K) * P;

  return x;
}

void forward(int speed)
{
  digitalWrite(in1Pin, HIGH);
  digitalWrite(in2Pin, LOW);
  digitalWrite(in3Pin, HIGH);
  digitalWrite(in4Pin, LOW);  
  analogWrite(ena1, speed);
  analogWrite(ena2, speed);
}

void back(int speed)
{
  digitalWrite(in1Pin, LOW);
  digitalWrite(in2Pin, HIGH);
  digitalWrite(in3Pin, LOW);
  digitalWrite(in4Pin, HIGH);    
  analogWrite(ena1, speed);
  analogWrite(ena2, speed);
}

void left(int speed) {
  digitalWrite(in1Pin, HIGH);
  digitalWrite(in2Pin, LOW);
  digitalWrite(in3Pin, LOW);
  digitalWrite(in4Pin, HIGH);    
  analogWrite(ena1, speed);
  analogWrite(ena2, speed);
}

void right(int speed) {
  digitalWrite(in1Pin, LOW);
  digitalWrite(in2Pin, HIGH);
  digitalWrite(in3Pin, HIGH);
  digitalWrite(in4Pin, LOW);    
  analogWrite(ena1, speed);
  analogWrite(ena2, speed);
}

void forwardRight(int speed, int turnSpeed) {
  digitalWrite(in1Pin, HIGH);
  digitalWrite(in2Pin, LOW);
  digitalWrite(in3Pin, HIGH);
  digitalWrite(in4Pin, LOW);  
  analogWrite(ena1, speed);
  analogWrite(ena2, turnSpeed);
}

void forwardLeft(int speed, int turnSpeed) {
  digitalWrite(in1Pin, HIGH);
  digitalWrite(in2Pin, LOW);
  digitalWrite(in3Pin, HIGH);
  digitalWrite(in4Pin, LOW);  
  analogWrite(ena1, turnSpeed);
  analogWrite(ena2, speed);
}

void forwardTurn(int speedLeft, int speedRight) {
  digitalWrite(in1Pin, HIGH);
  digitalWrite(in2Pin, LOW);
  digitalWrite(in3Pin, HIGH);
  digitalWrite(in4Pin, LOW);  
  analogWrite(ena1, speedLeft);
  analogWrite(ena2, speedRight);
}

void backRight(int speed, int turnSpeed) {
  digitalWrite(in1Pin, LOW);
  digitalWrite(in2Pin, HIGH);
  digitalWrite(in3Pin, LOW);
  digitalWrite(in4Pin, HIGH);
  analogWrite(ena1, speed);
  analogWrite(ena2, turnSpeed);
}

void backLeft(int speed, int turnSpeed) {
  digitalWrite(in1Pin, LOW);
  digitalWrite(in2Pin, HIGH);
  digitalWrite(in3Pin, LOW);
  digitalWrite(in4Pin, HIGH);    
  analogWrite(ena1, turnSpeed);
  analogWrite(ena2, speed);
}

void setSpeed(int s) {
  speed = s;
}

void stop() {
  digitalWrite(in1Pin, LOW);
  digitalWrite(in2Pin, LOW); 
  digitalWrite(in3Pin, LOW);
  digitalWrite(in4Pin, LOW); 
}
