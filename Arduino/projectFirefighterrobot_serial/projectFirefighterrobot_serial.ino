#include <SoftwareSerial.h>
#define LeftSensor 2
#define RightSensor 10
#define ForwardSensor 11

SoftwareSerial bluetoothSerial(12, 13);
int ena = 3, in1 = 4, in2 = 5, enb = 6, in3 = 7, in4 = 8;
int pump = 9;
int autoMode = 0;
int fire = 0;
char command;
int speed = 255;
int workingOnFire = 0;
void setup() {
	pinMode(ena, OUTPUT);
	pinMode(in1, OUTPUT);
	pinMode(in2, OUTPUT);
	pinMode(enb, OUTPUT);
	pinMode(in3, OUTPUT);
	pinMode(in4, OUTPUT);
	pinMode(pump, OUTPUT);
	pinMode(LeftSensor, INPUT);
	pinMode(RightSensor, INPUT);
	pinMode(ForwardSensor, INPUT);
	analogWrite(ena, 200);
	analogWrite(enb, 200);

  Serial.begin(115200);
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
	digitalWrite(4, LOW);
	digitalWrite(5, HIGH);
	digitalWrite(7, HIGH);
	digitalWrite(8, LOW);
}

void Left() {
	digitalWrite(4, HIGH);
	digitalWrite(5, LOW);
	digitalWrite(7, LOW);
	digitalWrite(8, HIGH);
}

void loop() {
  if(autoMode > 0) {
    if (Serial.available() > 0) {
      String firework = Serial.readStringUntil('\n');
      if(firework == "working_on_fire_out") {
        workingOnFire = 1;
      }
    }
    if (digitalRead(LeftSensor) == 1 && digitalRead(RightSensor) == 1 && digitalRead(ForwardSensor) == 1) 
    {
      fire = 0;    
      stop();
    }
    
    else if (digitalRead(ForwardSensor) == 0) 
    {
      fire = 1;
      while(digitalRead(ForwardSensor) == 0){
        // Print the "Fire Dectected" command to Raspberry Pi
        if(!workingOnFire) {
          Serial.println("fire_start");
        }
      }
      stop();
    }
    
    else if (digitalRead(LeftSensor) == 0)
    {
      speed = 220;
      analogWrite(ena, speed);
	    analogWrite(enb, speed);
      Left();
    }
    
    else if (digitalRead(RightSensor) == 0) 
    {
      speed = 220;
      analogWrite(ena, speed);
	    analogWrite(enb, speed);
      Right();
    }
    
    delay(320);//change this value to increase the distance
 
  }

  if (Serial.available() > 0) {
    String cmd = Serial.readStringUntil('\n');
    command = cmd.charAt(0);
  }

  if (bluetoothSerial.available() > 0) {
    command = bluetoothSerial.read();
  }
  
  switch(command) {
    case 'X':
      autoMode = 1;
      break;
    case 'x':
      autoMode = 0;
      speed = 0;
      break;
    case 'F':
      analogWrite(ena, speed);
      analogWrite(enb, speed);
      Forward();
      break;
    case 'B':
      analogWrite(ena, speed);
      analogWrite(enb, speed);
      Backward();
      break;
    case 'R':
      analogWrite(ena, speed);
      analogWrite(enb, speed);
      Right();
      break;
    case 'L':
      analogWrite(ena, speed);
      analogWrite(enb, speed);
      Left();
      break;
    case 'I':
      analogWrite(ena, 0.28*speed);
      analogWrite(enb, speed);
      Forward();
      break;
    case 'G':
      analogWrite(ena, speed);
      analogWrite(enb, 0.28*speed);
      Forward();
      break;
    case 'J':
      analogWrite(ena, speed);
      analogWrite(enb, 0.28*speed);
      Backward();
      break;
    case 'H':
      analogWrite(ena, 0.28*speed);
      analogWrite(enb, speed);
      Backward();
      break;
    case 'W':
      startPump();
      break;
    case 'w':
      stopPump();
      break;
    case '1':
      speed = 100;
      break;
    case '2':
      speed = 120;
      break;
    case '3':
      speed = 140;
      break;
    case '4':
      speed = 150;
      break;
    case '5':
      speed = 165;
      break;
    case '6':
      speed = 175;
      break;
    case '7':
      speed = 190;
      break;
    case '8':
      speed = 200;
      break;
    case '9':
      speed = 210;
      break;
    case 'q':
      speed = 220;
      break;
    default:
      stop();
      break;
  }
  
}
