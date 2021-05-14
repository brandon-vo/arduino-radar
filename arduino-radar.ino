#include <Servo.h>

// Define ultrasonic sensor and motor pins
#define trigPin 5
#define echoPin 6
#define servoPin 8

float duration; // Travel time in microseconds
float distance; // Distance in centimeters
int angle; // Position of the servo motor

Servo servoMotor; // Create servoMotor object

void setup() {
  pinMode(trigPin, OUTPUT); // Trig
  pinMode(echoPin, INPUT); // Echo
  servoMotor.attach(servoPin); // Servo motor
  Serial.begin(9600);
}

void loop() {

  // Rotate 0 to 180 degrees
  for (angle = 0; angle <= 180; angle++) { // Increase by 1 degree
    servoMotor.write(angle);
    delay(30);
    calculateDistance(angle);
    if (angle % 2 == 0) // Display data for angles in increments of 2
      displayData();
  }
  // Rotate 180 to 0 degrees
  for (angle = 180; angle >= 0; angle--) { // Decrease by 1 degree
    servoMotor.write(angle);
    delay(30);
    calculateDistance(angle);
    if (angle % 2 == 0) // Display data for angles in increments of 2
      displayData();
  }

}

// Calculate distance
float calculateDistance(int angle) {

  // Clear trigPin
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);

  // Turn on trigPin for 10 microseconds
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  // Duration in microseconds
  duration = pulseIn(echoPin, HIGH);

  // Calculate distance
  distance = duration * (0.0343) / 2; // Duration in microseconds multiplied by speed of sound in cm/μs divided by 2

  // Distance is set to 0 when the sensor is unreadable
  if (distance >= 400 || distance <= 3) {
    distance = 0;
  }

}

// Display data
void displayData() {
  Serial.print(angle); // Display angle
  Serial.print(",");
  Serial.println(distance); // Display distance (cm)
}
