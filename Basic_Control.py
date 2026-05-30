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

#Time to spend in each jar in seconds
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
BASE_MIN, BASE_MAX = 500, 2500 # MIN=Left, MAX=Right
SHOULDER_MIN, SHOULDER_MAX = 1250, 1800 # MIN=Down, MAX=Up
ELBOW_MIN, ELBOW_MAX = 1950, 2150 # MIN=Up, MAX=Down
WRIST_MIN, WRIST_MAX = 500, 1500 # MIN=Down, MAX=Up
CLAW_MIN, CLAW_MAX = 1100, 1400 # Fully open and closed positions

class BasicControl:
  def __init__(self):
    self.centers = [BASE_CENTER, SHOULDER_CENTER, ELBOW_CENTER, WRIST_CENTER, CLAW_CENTER]
    self.ssc = serial.Serial('COM5', 9600)

  # Defines the entire sequence that the robot arm will follow for the procedure
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

  # Resets all servo postions to center
  def center(self):
    for joint in JOINTS:
      self.write_position(self.centers[joint], joint)

  def close_claw(self):
    self.write_position(CLAW_MAX, CLAW)

  # Completes one cycle of the procedure. 
  # If half is True, then perform the first half
  def cycle(self, half : bool):
    print(f"Cycling with Half = {half}...")
    cycle_jars, cycle_times = JARS, TIMES
    if half:
      cycle_jars, cycle_times = JARS[:3], TIMES[:3]

    for jar, t in zip(cycle_jars, cycle_times):
      self.dip(jar, dip_time=t)
    print(f"Cycle Complete")

  # Move to the specified jar, dip for dip_time
  def dip(self, jar : int, dip_time : int):
    self.raise_arm()
    self.write_position(jar, BASE)
    print("Dipping...")
    self.lower_arm()
    time.sleep(dip_time)
    print("Dip Complete")

  # Hang slide over center of setup indefinitely
  def dry(self):
    print("Drying...")
    self.raise_arm()
    self.write_position(BASE_CENTER, BASE)
    print("Dry Complete")

  # Allow user to load slide to claw
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

  # Writes the position to move the specified joint to
  def write_position(self, servo_position : int, joint : int):
    self.ssc.write(bytes(f"#{joint}P{servo_position} T1000\r", encoding='utf8'))
    time.sleep(2)

controller = BasicControl()
controller.sequence()
