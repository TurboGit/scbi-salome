from datetime import datetime
from pathlib import Path
import os
import subprocess
import hashlib
import platform, getpass, tempfile
import sys

from PyQt5 import QtCore
from PyQt5.QtWidgets import QRadioButton, QVBoxLayout
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QApplication
from PyQt5.QtCore import QSettings

# check if window
is_window = any(platform.win32_ver())

def get_hashuid():
    if is_window:
        return 2**15 + 2**14 + hash(getpass.getuser())%2**14
    else:
        return os.getuid()

# get the pid for the current process
PID = os.getpid()
UID = get_hashuid()

WEB_SERVER = "__WEB_SERVER__"
SALOME_VERSION = "__SALOME_VERSION__"
EDF_DIRECTION = "__DIRECTION__"
USER_ID = "__USERID__"
temp_dir = tempfile.gettempdir()
LOG_FILENAME = os.path.join(temp_dir, "%s-salome.log" % UID)

SESSION_ID = datetime.now().strftime("%Y%m%d%H%M%S")
# set GUI_LOG_FILE which is used in KERNEL to enable logging
os.environ["GUI_LOG_FILE"] = LOG_FILENAME

#  Resource file for SALOME
settings = QtCore.QSettings('salome', 'salomerc')

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
    #  Get or create User ID
    if not settings.contains("user_id"):
        settings.setValue("user_id", create_uid())
    return settings.value("user_id")

#  Dialog box to ask for the direction
class MainWindow(QWidget):

    def __init__(self, app):
        super().__init__()

        self.app = app

        self.button = QPushButton("Ok")

        self.choices = [
            QRadioButton(text="CEIDRE"),
            QRadioButton(text="CIH"),
            QRadioButton(text="CNEPE"),
            QRadioButton(text="DIPDE"),
            QRadioButton(text="DT"),
            QRadioButton(text="Edvance"),
            QRadioButton(text="RetD")
        ]

        self.label = QLabel("Lors de l'utilisation de SALOME des informations sont remontées\n"
                            + "vers un serveur à des fin de statistiques :\n"
                            + "  - Les informations sont anonymes\n"
                            + "  - Les modules utilisés sont reportés\n"
                            + "  - Des informations plus détaillées sont récupérées pour SHAPER et GEOM\n"
                            + "\n"
                            + "Ces informations permettront de mieux connaître les usages\n"
                            + "de SALOME et de porter plus d'attention aux modules\n"
                            + "correspondants.\n\n"
                            + "Merci de sélectionner votre direction :\n")

        self.button.pressed.connect(self.press_ok)

        layout = QVBoxLayout()
        layout.addWidget(self.label)

        for c in self.choices:
            layout.addWidget(c)

        layout.addWidget(self.button)
        self.setLayout(layout)

    def press_ok(self):
        for c in self.choices:
            if c.isChecked():
                settings.setValue("direction", c.text())
                self.app.quit()

def init(context, root_dir):
    # Start the SALOME logger process in charge of sending the data
    # to the web server. Note that this process will automatically
    # terminate when the given process id will quit.

    # Never enable the logger when run on GitLab-CI
    if os.getenv('CI_PROJECT_DIR') != None:
        return

    # Make sure the logger module has been compiled and
    # is available.
    if os.getenv('LOGGER_ROOT_DIR') == None:
        return

    # We only support salome logger in GUI mode
    if "shell" in sys.argv:
        return

    SALOME_VERSION = os.environ["SALOME_VERSION"]
    SALOME_LOGGER = os.environ["LOGGER_ROOT_DIR"]

    # Ask for the direction if there is not yet a version registered
    force_ask = not settings.contains("version")

    # Record version now
    settings.setValue("version", SALOME_VERSION)

    # If we don't yet have the direction set or if a new SALOME version
    # ask for the direction now.
    if force_ask or not settings.contains("direction"):
        app = QApplication([])
        w = MainWindow(app)
        w.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)
        w.show()
        app.exec()

    # Now set EDF_DIRECTION has defined
    EDF_DIRECTION = settings.value("direction")

    # Get USER_ID, fully random and either recorded in settings or
    # generated if not yet set.
    USER_ID = get_uid()

    settings.sync()

    L_BIN = os.path.join(SALOME_LOGGER, "bin", "SalomeLogger")
    L_PLG = os.path.join(SALOME_LOGGER, "bin", "libFilterPlugin.so") \
        if not is_window else os.path.join(SALOME_LOGGER, "bin", "FilterPlugin.dll")

    PFX = USER_ID + ',' + SESSION_ID + ',' \
        + EDF_DIRECTION + ',' + SALOME_VERSION

    CMDLINE=[L_BIN,
             "--prefix", PFX,
             "--server", WEB_SERVER,
             "--pid", str(PID),
             "--file-name", LOG_FILENAME ]

    if not is_window:
        CMDLINE+=[ "--lib-path", L_PLG ]

    subprocess.Popen(CMDLINE, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
