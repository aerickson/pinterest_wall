import os.path
import subprocess
from appscript import mactypes

SCRIPT = """/usr/bin/osascript<<END
tell application "Finder"
set desktop picture to POSIX file "%s"
end tell
END"""

def set_wallpaper(filename):
  filepath = os.path.abspath(filename)
  #filepathmactypes.File(filepath)
  subprocess.Popen(SCRIPT%filename, shell=True)