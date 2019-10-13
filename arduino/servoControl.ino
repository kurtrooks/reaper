/*
 * rosserial Servo Control Example
 *
 * This sketch demonstrates the control of hobby R/C servos
 * using ROS and the arduiono
 * 
 * For the full tutorial write up, visit
 * www.ros.org/wiki/rosserial_arduino_demos
 *
 * For more information on the Arduino Servo Library
 * Checkout :
 * http://www.arduino.cc/en/Reference/Servo
 */


#if (ARDUINO >= 100)
 #include <Arduino.h>
#else
 #include <WProgram.h>
#endif

#include <Servo.h> 
#include <ros.h>
#include <std_msgs/UInt16.h>

ros::NodeHandle  nh;

Servo hip_servo;
Servo shoulder_servo;

void hip_servo_cb( const std_msgs::UInt16& cmd_msg){
  //hip_servo.write(cmd_msg.data); //set servo angle, should be from 0-180  
  digitalWrite(13, HIGH-digitalRead(13));  //toggle led  
}

void hip_servo_cb2( const std_msgs::UInt16& cmd_msg){
  hip_servo.writeMicroseconds(cmd_msg.data); 
  digitalWrite(13, HIGH-digitalRead(13));  //toggle led  
}

void shoulder_servo_cb( const std_msgs::UInt16& cmd_msg){
  //shoulder_servo.write(cmd_msg.data); //set servo angle, should be from 0-180  
  digitalWrite(13, HIGH-digitalRead(13));  //toggle led  
}

ros::Subscriber<std_msgs::UInt16> hip_sub("hip_servo", hip_servo_cb);
ros::Subscriber<std_msgs::UInt16> hip_sub2("hip_servo2", hip_servo_cb2);
ros::Subscriber<std_msgs::UInt16> shoulder_sub("shoulder_servo", shoulder_servo_cb);


void setup(){
  pinMode(13, OUTPUT);

  nh.initNode();
  nh.subscribe(hip_sub);
  nh.subscribe(shoulder_sub);
  nh.subscribe(hip_sub2);
  
  
  hip_servo.attach(9); //attach it to pin 9
  shoulder_servo.attach(10); //attach it to pin 10
}

void loop(){
  nh.spinOnce();
  delay(1);
}
