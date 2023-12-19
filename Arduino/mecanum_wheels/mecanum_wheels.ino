#include <SoftwareSerial.h>
SoftwareSerial bluetoothSerial(12, 13);
int in1 = 22, in2 = 24, in3 = 28, in4 = 26;
int in5 = 49, in6 = 47, in7 = 53, in8 = 51;

char command;
int speed = 255;

void setup() {
	pinMode(in1, OUTPUT);
	pinMode(in2, OUTPUT);
	pinMode(in3, OUTPUT);
	pinMode(in4, OUTPUT);
  pinMode(in5, OUTPUT);
	pinMode(in6, OUTPUT);
	pinMode(in7, OUTPUT);
	pinMode(in8, OUTPUT);

  Serial.begin(115200);
  bluetoothSerial.begin(9600);
}

void stop() {
  digitalWrite(in1, LOW);
	digitalWrite(in2, LOW);
	digitalWrite(in3, LOW);
	digitalWrite(in4, LOW);
  digitalWrite(in5, LOW);
	digitalWrite(in6, LOW);
	digitalWrite(in7, LOW);
	digitalWrite(in8, LOW);
}

void forward() {
	digitalWrite(in1, HIGH);
	digitalWrite(in2, LOW);
	digitalWrite(in3, HIGH);
	digitalWrite(in4, LOW);

  digitalWrite(in5, HIGH);
	digitalWrite(in6, LOW);
	digitalWrite(in7, HIGH);
	digitalWrite(in8, LOW);
}

void backward() {
	digitalWrite(in1, LOW);
	digitalWrite(in2, HIGH);
	digitalWrite(in3, LOW);
	digitalWrite(in4, HIGH);

  digitalWrite(in5, LOW);
	digitalWrite(in6, HIGH);
	digitalWrite(in7, LOW);
	digitalWrite(in8, HIGH);
}

void right() {
	digitalWrite(in1, LOW);
	digitalWrite(in2, HIGH);
	digitalWrite(in3, HIGH);
	digitalWrite(in4, LOW);

  digitalWrite(in5, HIGH);
	digitalWrite(in6, LOW);
	digitalWrite(in7, LOW);
	digitalWrite(in8, HIGH);
}

void left() {
	digitalWrite(in1, HIGH);
	digitalWrite(in2, LOW);
	digitalWrite(in3, LOW);
	digitalWrite(in4, HIGH);

  digitalWrite(in5, LOW);
	digitalWrite(in6, HIGH);
	digitalWrite(in7, HIGH);
	digitalWrite(in8, LOW);
}

void forwardRight() {
	// digitalWrite(in1, HIGH);
	// digitalWrite(in2, LOW);
	digitalWrite(in3, HIGH);
	digitalWrite(in4, LOW);

  digitalWrite(in5, HIGH);
	digitalWrite(in6, LOW);
	// digitalWrite(in7, HIGH);
	// digitalWrite(in8, LOW);
}

void forwardLeft() {
	digitalWrite(in1, HIGH);
	digitalWrite(in2, LOW);
	// digitalWrite(in3, HIGH);
	// digitalWrite(in4, LOW);

  // digitalWrite(in5, HIGH);
	// digitalWrite(in6, LOW);
	digitalWrite(in7, HIGH);
	digitalWrite(in8, LOW);
}

void backwardRight() {
  digitalWrite(in1, LOW);
	digitalWrite(in2, HIGH);
	// digitalWrite(in3, LOW);
	// digitalWrite(in4, HIGH);

  // digitalWrite(in5, LOW);
	// digitalWrite(in6, HIGH);
	digitalWrite(in7, LOW);
	digitalWrite(in8, HIGH);
}

void backwardLeft() {
  // digitalWrite(in1, LOW);
	// digitalWrite(in2, HIGH);
	digitalWrite(in3, LOW);
	digitalWrite(in4, HIGH);

  digitalWrite(in5, LOW);
	digitalWrite(in6, HIGH);
	// digitalWrite(in7, LOW);
	// digitalWrite(in8, HIGH);
}

void loop() {
  if (Serial.available() > 0) {
    String cmd = Serial.readStringUntil('\n');
    command = cmd.charAt(0);
  }

  if (bluetoothSerial.available() > 0) {
    command = bluetoothSerial.read();
    Serial.println(command);
  }
  
  switch(command) {
    case 'X':
      break;
    case 'x':      
      stop();
      break;
    case 'F':
      forward();
      break;
    case 'B':
      backward();
      break;
    case 'R':
      right();
      break;
    case 'L':
      left();
      break;
    case 'I':
      stop();
      forwardRight();
      break;
    case 'G':
      stop();
      forwardLeft();
      break;
    case 'J':
      stop();
      backwardRight();
      break;
    case 'H':
      stop();
      backwardLeft();
      break;
    case 'W':
      break;
    case 'w':
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
      speed = 200;
      break;
    case '8':
      speed = 220;
      break;
    case '9':
      speed = 235;
      break;
    case 'q':
      speed = 250;
      break;
    default:
      stop();
      break;
  }
  
}
