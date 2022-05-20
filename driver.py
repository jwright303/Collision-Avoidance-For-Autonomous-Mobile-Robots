import os
import readline

PCNUM = ["81", "184", "151", "84", "88", "71", "95"]

def pointCloudPrompt():
  print("\t[1] Simulated with cliff")
  print("\t[2] Simulated with pedestrian")
  print("\t[3] Simulated with object")
  print("\t[4] Camera generated object")
  print("\t[5] Camera generated two objects")
  print("\t[6] Camera generated rotated object")
  print("\t[7] Camera generated stairs scenario")
  return

def execProgram(program, data, pcNum="", extraArgs=""):
  if data == 1:
    #Exec simulated with a cliff
    pN = "81" if pcNum == "" else pcNum
    os.system("python3 " + program + " --pth=./ptclds/Cliff_Shifted/ --pref=pcd_ --pcNum=" + pN + " " + extraArgs)
  elif data == 2:
    #Esec simulated with a pedestrian
    pN = "184" if pcNum == "" else pcNum
    os.system("python3 " + program + " --pth=./ptclds/PreAct_3D_Person/ --pref=pcd_ --pcNum=" + pN + " " + extraArgs)
  elif data == 3:
    #Exec simulated with an object
    pN = "151" if pcNum == "" else pcNum
    os.system("python3 " + program + " --pth=./ptclds/PreAct_3D_F/ --pref=pcd_ --pcNum=" + pN + " " + extraArgs)
  elif data == 4:
    #Exec camera object
    pN = "84" if pcNum == "" else pcNum
    os.system("python3 " + program + " --pth=./ptclds/Cropped/Single/ --pref=pcd_ --pcNum=" + pN + " " + extraArgs)
  elif data == 5:
    #Exec camera two objects
    pN = "88" if pcNum == "" else pcNum
    os.system("python3 " + program + " --pth=./ptclds/Cropped/Two/ --pref=pcd_ --pcNum=" + pN + " " + extraArgs)
  elif data == 6:
    #Exec camera rotated object
    pN = "71" if pcNum == "" else pcNum
    os.system("python3 " + program + " --pth=./ptclds/Cropped/Rotated/ --pref=pcd_ --pcNum=" + pN + " " + extraArgs)
  elif data == 7:
    pN = "95" if pcNum == "" else pcNum
    os.system("python3 " + program + " --pth=./ptclds/Cropped/Stairs/ --pref=pcd_ --pcNum=" + pN + " " + extraArgs)
  else:
    return -1
  
  return 0


def getInput(prompt, pcPrompt=True):
  attempting = True
  cVal = 0
  while attempting:
    print(prompt)
    if pcPrompt:
      pointCloudPrompt()

    choice = input("Enter your choice: ")
    if (len(choice) == 1 and ord(choice) >= 48 and ord(choice) <= 57):
      cVal = int(choice)
      attempting = False
    else:
      print("Invalid input given, try again\n")

  return cVal


if __name__=="__main__":
  print("\nWelcome to the Collision Avoidance for Autonomous Mobile Robots driver")
  print("This program will allow you to run the most important programs our group developed\n")
  

  while True:
    print("You can run the programs below by entering their corresponding number")
    print("\t[1] Animate a point cloud scene")
    print("\t[2] View a specific point cloud")
    print("\t[3] Run object detection on a specific point cloud")
    print("\t[4] Simulate the object detection and rules on a point cloud scenario")
    print("\t[5] Run object detection on a point cloud scenario")
    print("\t[6] Run edge detection in real time")
    print("\t[7] Exit\n")

    cVal = getInput("", False)

    if cVal == 1:
      pVal = getInput("Choose the pointcloud scenario to animate")
      execProgram("pcldAnim.py", pVal)
    elif cVal == 2:
      pVal = getInput("Choose the pointcloud scenario to view from")
      pcNum = int(input("Enter the point cloud that you would like to view: (0-" + PCNUM[pVal-1] + "): "))
      execProgram("pcldView.py", pVal, str(pcNum))
    elif cVal == 3:
      pVal = getInput("Choose the pointcloud scenario to run object detection on")
      pcNum = int(input("Enter the point cloud that you would like to use: (0-" + PCNUM[pVal-1] + "): "))
      verb = input("Would you like to display the intermediate steps? (True or False): ")
      execProgram("pcCluster.py", pVal, str(pcNum), "--verbose=" + verb)
    elif cVal == 4:
      pVal = getInput("Choose the pointcloud scenario to run the simulation on")
      df = input("Would you like to filter out points that are too far? (True or False): ")
      execProgram("sim.py", pVal, extraArgs="--dF=" + df)
    elif cVal == 5:
      pVal = getInput("Choose the pointcloud scenario to run the object detection on")
      execProgram("objAnim.py", pVal)
    elif cVal == 6:
      print("Running program...")
      os.system("python3 EdgeDetRT.py")
    elif cVal == 7:
      break
    else:
      print("Invalid input given, try again")
    print("")
