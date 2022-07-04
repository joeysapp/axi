def writeTextToFile(txt, wt):
  subprocess.call(["rm", "../gcodes/tmp.gcode"]);
  cmd = "node ../textPlotter.js "+str(wt)+" "+str(txt)+" >> ../gcodes/tmp.gcode"
  subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)

def map(val, min1, max1, min2, max2):
  return min2+(max2-min2)*((val-min1)/(max1-min1))
