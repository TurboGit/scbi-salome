from datetime import datetime
from pathlib import Path
import os.path
import subprocess
import hashlib

# get the pid for the current process
PID = os.getpid()
UID = os.getuid()

WEB_SERVER = "__WEB_SERVER__"
SALOME_VERSION = "__SALOME_VERSION__"
EDF_DIRECTION = "__DIRECTION__"
USER_ID = "__USERID__"
LOG_FILENAME = "/tmp/%s-salome.log" % UID
SESSION_ID = datetime.now().strftime("%Y%m%d%H%M%S")
# set GUI_LOG_FILE which is used in KERNEL to enable logging
os.environ["GUI_LOG_FILE"] = LOG_FILENAME

def create_uid():
    #  Initialize in case check_output below fails
    sha_1 = hashlib.sha1()
    try:
        #  Get 64 random bytes from /dev/urandom
        #  TODO: We may want to specialize this for Windows when supported
        out = check_output(["od", "-t", "x8", "-N", "64", "/dev/urandom"])
        sha_1.update(out)
    except:
        #  If the above fails use a timestamp
        dt = datetime.today()
        seconds = dt.timestamp()
        sha_1.update(b"%d" % seconds)

    return sha_1.hexdigest()

def get_uid():
    #  User ID is stored in $HOME/.config/salome/user.id
    salome_dir = os.path.join(Path.home(), ".config", "salome")
    if(not os.path.isdir(salome_dir)):
        os.mkdir(salome_dir)
    salome_id = os.path.join(salome_dir, "user.id")

    if(os.path.isfile(salome_id)):
        #  File exists get id
        with open(salome_id) as f:
            id = f.readlines()
            return id[0]
    else:
        #  File not present generate id
        id = create_uid()
        with open(salome_id, "w") as f:
            f.write(id)
            return id

def init(context, root_dir):
    # start the SALOME logger process in charge of sending the data
    # to the web server. Note that this process will automatically
    # terminate when the given process id will quit.

    USER_ID = get_uid()

    SALOME_VERSION = os.environ["SALOME_VERSION"]
    SALOME_LOGGER = os.environ["LOGGER_ROOT_DIR"]

    L_BIN = os.path.join(SALOME_LOGGER, "bin", "SalomeLogger")
    L_PLG = os.path.join(SALOME_LOGGER, "bin", "libFilterPlugin.so")

    PFX = USER_ID + ',' + SESSION_ID + ',' \
        + EDF_DIRECTION + ',' + SALOME_VERSION

    subprocess.Popen([L_BIN,
                      "--prefix", PFX,
                      "--server", WEB_SERVER,
                      "--lib-path", L_PLG,
                      "--pid", str(PID),
                      "--file-name", LOG_FILENAME])
