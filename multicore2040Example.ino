/*
This file acts as a simple demo of how to utilize two cores on the Arduino Nano 2040 Connect
There are apparently a few ways to go about doing this task. Below is one of the simplest methods I could create.
It uses only one library, which comes packaged with the board when installed through the Arduino IDE (tested on version 2.2.1 of the IDE)

SETUP
The board should have two LEDS; connected on pins 11 and 10


DEBUGGING:
In the event you send a program that the board doesn't like, it will drop connection, blink "SOS" with the builtin LED, and not reconnect to the computer
This is very easy to fix:
  1) Remove the change in your code, you'll need to figure out another way to do what you need
  2) While still plugged in, put the board into bootloader mode by pressing the builtin button twice
  3) Flash the board with a simple program you know works; I suggest the example blink.ino program
  4) When satisfied the board works, try your program again having reverted the changes


Nano RP2040 Connect Cheatsheet (Including Pinouts, Debugging, and Hard-resets)
https://docs.arduino.cc/tutorials/nano-rp2040-connect/rp2040-01-technical-reference/


*/

//This library seems to be included in the installation package of the board
#include <pico/multicore.h>

//Create two leds, one for each core to test the multicore functionality
#define CORE_0_LED 11
#define CORE_1_LED 10

//Give each led a different blink speed to easily see difference
int core0_LED_delay = 500;
int core1_LED_delay = 100;

void setup() {
  // One setup method is appropriate despite starting two cores. Some tutorials use a setup for each core. I found it to not be necessary.
  Serial.begin(9600);
  pinMode(CORE_0_LED, OUTPUT);
  pinMode(CORE_1_LED, OUTPUT);
  sleep_ms(500); //This line is 100% necessary to get the multicore to start. Why it comes before the multicore_launch, I have no idea... yet, it must.
  multicore_launch_core1(core1_loop);
  sleep_ms(500); //This one is not necessary but is a good idea regardless
}

void loop() {
  // This loops is what Core0 will run repeatedly. It does so natively:
  //As far as I understand with Arduino, this must be called "loop"
  while(true){
    //You must use while(true) in both loops for both cores to work 
    Serial.println("Core0 says Hello");
    digitalWrite(CORE_0_LED, HIGH);
    sleep_ms(core0_LED_delay);
    digitalWrite(CORE_0_LED, LOW);
    sleep_ms(core0_LED_delay);
  }
}

void core1_loop(){
  //This loop is what Core1 will run.
  //You may call this loop anything you like, as long as you specify it correctly in setup()
  while(true){
    //You must use a while(true) in both loops for both cores to work
    //Serial.println("Core1 also says Hello");
      //Core1 does not have a good time with Serial connections. This line of code if uncommented will cause the board to disconnnectI am looking into a work around. Both cores share memory so, that is a possible solution
    digitalWrite(CORE_1_LED, LOW);
    sleep_ms(core1_LED_delay);
    digitalWrite(CORE_1_LED, HIGH);
    sleep_ms(core1_LED_delay);
  }
}
