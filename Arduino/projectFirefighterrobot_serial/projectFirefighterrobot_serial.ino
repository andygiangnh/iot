#include <SoftwareSerial.h>
#define LeftSen 2
#define RightSen 10
#define FrontSen 11

SoftwareSerial bluetoothSerial(12, 13);
int ena = 3, in1 = 4, in2 = 5, enb = 6, in3 = 7, in4 = 8, pump = 9;
char command;
int speed = 255;
void setup() {
	pinMode(ena, OUTPUT);
	pinMode(in1, OUTPUT);
	pinMode(in2, OUTPUT);
	pinMode(enb, OUTPUT);
	pinMode(in3, OUTPUT);
	pinMode(in4, OUTPUT);
	pinMode(pump, OUTPUT);
	pinMode(LeftSen, INPUT);
	pinMode(RightSen, INPUT);
	pinMode(FrontSen, INPUT);
	analogWrite(ena, 200);
	analogWrite(enb, 200);

  Serial.begin(9600);
  bluetoothSerial.begin(9600);

}
void stop() {
  digitalWrite(4, LOW);
	digitalWrite(5, LOW);
	digitalWrite(7, LOW);
	digitalWrite(8, LOW);
}
void startPump(){
  digitalWrite(pump, HIGH);
}
void stopPump(){
  digitalWrite(pump, LOW);
}
void Forward() {
	digitalWrite(4, HIGH);
	digitalWrite(5, LOW);
	digitalWrite(7, HIGH);
	digitalWrite(8, LOW);

}
void Backward() {
	digitalWrite(4, LOW);
	digitalWrite(5, HIGH);
	digitalWrite(7, LOW);
	digitalWrite(8, HIGH);

}void Right() {
	digitalWrite(4, HIGH);
	digitalWrite(5, LOW);
	digitalWrite(7, LOW);
	digitalWrite(8, HIGH);
}

void Left() {
	digitalWrite(4, LOW);
	digitalWrite(5, HIGH);
	digitalWrite(7, HIGH);
	digitalWrite(8, LOW);
}

void loop() {
  if (Serial.available() > 0) {
    command = Serial.readStringUntil('\n');
  }

  if (bluetoothSerial.available() > 0) {
    command = bluetoothSerial.read();
  }
  
  switch(command) {      
    case 'F':
      analogWrite(3, speed);
      analogWrite(6, speed);
      Forward();
      break;
    case 'B':
      analogWrite(3, speed);
      analogWrite(6, speed);
      Backward();
      break;
    case 'R':
      analogWrite(3, speed);
      analogWrite(6, speed);
      Right();
      break;
    case 'L':
      analogWrite(3, speed);
      analogWrite(6, speed);
      Left();
      break;
    case 'I':
      analogWrite(3, 0.28*speed);
      analogWrite(6, speed);
      Forward();
      break;
    case 'G':
      analogWrite(3, speed);
      analogWrite(6, 0.28*speed);
      Forward();
      break;
    case 'J':
      analogWrite(3, speed);
      analogWrite(6, 0.28*speed);
      Backward();
      break;
    case 'H':
      analogWrite(3, 0.28*speed);
      analogWrite(6, speed);
      Backward();
      break;
    case 'W':
      startPump();
      break;
    case 'w':
      stopPump();
      break;
    default:
      stop();
      break;
  }
  
}