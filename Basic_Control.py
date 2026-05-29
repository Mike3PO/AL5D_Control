import serial
import time

# Indices of each joint
BASE, SHOULDER, ELBOW, WRIST, CLAW = 0, 1, 2, 3, 4

# Array containing all joints
JOINTS = [BASE, SHOULDER, ELBOW, WRIST, CLAW]

# BASE servo positions for each jar
# 1 2 3 4 5 6
# JARS = [680, 1030, 1380, 1730, 2110, 2500]
# 1 2 3 6 5 4
JARS = [680, 1030, 1380, 2500, 2110, 1730]

#Time to spend in each jar
TIMES = [1, 1, 1, 1, 1, 1]

#Cycle Iterations
CYCLES = 10

#Centered servo positions for each joint
BASE_CENTER = 1500
SHOULDER_CENTER = 1550
ELBOW_CENTER = 2000
WRIST_CENTER = 700
CLAW_CENTER = 1500

# All max and min values for servos when all other servos are centered
BASE_MIN, BASE_MAX = 500, 2500
SHOULDER_MIN, SHOULDER_MAX = 1250, 1800
ELBOW_MIN, ELBOW_MAX = 1950, 2150 # The elbow gets erratic very quickly
WRIST_MIN, WRIST_MAX = 500, 1500
CLAW_MIN, CLAW_MAX = 1100, 1400 # Fully open and closed positions

class BasicControl:
  def __init__(self):
    self.centers = [BASE_CENTER, SHOULDER_CENTER, ELBOW_CENTER, WRIST_CENTER, CLAW_CENTER]
    self.ssc = serial.Serial('COM5', 9600)

  def sequence(self):
    self.load()

    cur_cycle = 0
    while cur_cycle <= CYCLES:
      if cur_cycle == CYCLES:
        self.cycle(half=True)
        break
      self.cycle(half=False)
      cur_cycle+= 1

    self.dry()

    self.ssc.close()

  def center(self):
    for joint in JOINTS:
      self.ssc.write(bytes(f"#{joint}P{self.centers[joint]} T1000\r", encoding='utf8'))
    time.sleep(2)

  def close_claw(self):
    self.write_position(CLAW_MAX, CLAW)

  def cycle(self, half : bool):
    print(f"Cycling with Half = {half}...")
    cycle_jars, cycle_times = JARS, TIMES
    if half:
      cycle_jars, cycle_times = JARS[:3], TIMES[:3]

    for jar, t in zip(cycle_jars, cycle_times):
      self.dip(jar, dip_time=t)
    print(f"Cycle Complete")

  def dip(self, jar : int, dip_time : int):
    self.raise_arm()
    self.write_position(jar, BASE)
    print("Dipping...")
    self.lower_arm()
    time.sleep(dip_time)
    print("Dip Complete")

  def dry(self):
    print("Drying...")
    self.raise_arm()
    self.write_position(BASE_CENTER, BASE)
    print("Dry Complete")

  def load(self):
    print("Beginning load sequence...")
    self.center()
    self.raise_arm()
    self.open_claw()
    print("Load slides now")
    time.sleep(5)
    self.close_claw()
    print("Slides Loaded")

  def lower_arm(self):
    self.write_position(SHOULDER_CENTER, SHOULDER)
    self.write_position(ELBOW_CENTER, ELBOW)

  def open_claw(self):
    self.write_position(CLAW_MIN, CLAW)

  def raise_arm(self):
    self.write_position(ELBOW_MIN, ELBOW)
    self.write_position(SHOULDER_MAX, SHOULDER)

  def write_position(self, servo_position : int, joint : int):
    self.ssc.write(bytes(f"#{joint}P{servo_position} T1000\r", encoding='utf8'))
    time.sleep(2)

controller = BasicControl()
controller.sequence()
