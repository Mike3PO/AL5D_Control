import serial
import time

BASE, SHOULDER, ELBOW, WRIST, CLAW = 0, 1, 2, 3, 4
JOINTS = [BASE, SHOULDER, ELBOW, WRIST, CLAW]
JARS = [1700, 1600, 1400, 1300, 1200, 1100]
BASE_CENTER = 1500
SHOULDER_CENTER = 1550
ELBOW_CENTER = 2050
WRIST_CENTER = 700
CLAW_CENTER = 1200

class BasicControl:
  def __init__(self):
    self.centers = [BASE_CENTER, SHOULDER_CENTER, ELBOW_CENTER, WRIST_CENTER, CLAW_CENTER]
    self.ssc = serial.Serial('COM5', 9600)

  def sequence(self):
    for joint in JOINTS:
      self.ssc.write(bytes(f"#{joint}P{self.centers[joint]} T1000\r", encoding='utf8'))

    time.sleep(2)

    # for jar in JARS:
    #   self.write_position(jar, BASE)

    self.ssc.close()

  def write_position(self, servo_position : int, joint : int):
    self.ssc.write(bytes(f"#{joint}P{servo_position} T1000\r", encoding='utf8'))
    time.sleep(2)

controller = BasicControl()

controller.sequence()
