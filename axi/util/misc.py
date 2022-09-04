
# Previous to-port-in-code
def writeTextToFile(txt, wt):
  subprocess.call(["rm", "../gcodes/tmp.gcode"]);
  cmd = "node ../textPlotter.js "+str(wt)+" "+str(txt)+" >> ../gcodes/tmp.gcode"
  subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
