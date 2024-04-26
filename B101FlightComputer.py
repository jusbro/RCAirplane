/*
This software is designed to fly a simple RC airplane
The main hardware is an Arduino Nano RP2040 Connect

The Wifi Chip was flashed with Bluepad32 firmware for NINA
https://gitlab.com/ricardoquesada/bluepad32/-/blob/main/docs/plat_nina.md

This program pairs the RP2040 with an Xbox Controller
https://gitlab.com/ricardoquesada/bluepad32/-/blob/main/docs/supported_gamepads.md



AIR CRAFT DESIGN
The following site is being utilized to research and design a prototype:
https://www.airfieldmodels.com/information_source/math_and_science_of_model_aircraft/rc_aircraft_design/step_by_step_model_aircraft_design.htm

*/
#include <Bluepad32.h>
#include <Servo.h>

#define THROTTLE_LED_PIN 13
#define AILERON_SERVO_PIN A3
//When using analog pins for the 2040, some pins cannot be used do to them being controlled by the Wifi chip. 
//The flashing of that chip has removed their functionality
//These pins WILL NOT WORK as a result: 

ControllerPtr myControllers[BP32_MAX_CONTROLLERS];

Servo aileronServo;

void setup() {
  Serial.begin(9600);

  pinMode(THROTTLE_LED_PIN, OUTPUT);
  pinMode(AILERON_SERVO_PIN, OUTPUT);

  aileronServo.attach(AILERON_SERVO_PIN);

  BP32.setup(&onConnectedController, &onDisconnectedController);

  //Add forgetBluetoothKeys here if needed
}

// This callback gets called any time a new gamepad is connected.
// Up to 4 gamepads can be connected at the same time.
void onConnectedController(ControllerPtr ctl) {
  bool foundEmptySlot = false;
  for (int i = 0; i < BP32_MAX_GAMEPADS; i++) {
    if (myControllers[i] == nullptr) {
      Serial.print("CALLBACK: Controller is connected, index=");
      Serial.println(i);
      myControllers[i] = ctl;
      foundEmptySlot = true;

      // Optional, once the gamepad is connected, request further info about the
      // gamepad.
      ControllerProperties properties = ctl->getProperties();
      char buf[80];
      sprintf(buf,
              "BTAddr: %02x:%02x:%02x:%02x:%02x:%02x, VID/PID: %04x:%04x, "
              "flags: 0x%02x",
              properties.btaddr[0], properties.btaddr[1], properties.btaddr[2],
              properties.btaddr[3], properties.btaddr[4], properties.btaddr[5],
              properties.vendor_id, properties.product_id, properties.flags);
      Serial.println(buf);
      break;
    }
  }
  if (!foundEmptySlot) {
    Serial.println(
        "CALLBACK: Controller connected, but could not found empty slot");
  }
}

void onDisconnectedController(ControllerPtr ctl) {
  bool foundGamepad = false;

  for (int i = 0; i < BP32_MAX_GAMEPADS; i++) {
    if (myControllers[i] == ctl) {
      Serial.print("CALLBACK: Controller is disconnected from index=");
      Serial.println(i);
      myControllers[i] = nullptr;
      foundGamepad = true;
      break;
    }
  }

  if (!foundGamepad) {
    Serial.println(
        "CALLBACK: Controller disconnected, but not found in myControllers");
  }
}

void controllerAction(ControllerPrt gamepad){
  int count = gamepad->throttle();
  int servoCount = gamepad->axisX();
  int servoPos = map(servoCount, -511, 511, 0, 180);
  myservo.write(servoPos);
  int brightness = map(count, 0, 1023, 0, 255);
  analogWrite(LED_PIN, brightness);
  
}



void loop() {
  BP32.update();
  for (int i = 0; i < BP32_MAX_CONTROLLERS; i++) {
    ControllerPtr myController = myControllers[i];
    if (myController && myController->isConnected()) 
  controllerAction(myController);
  delay(100);

}
