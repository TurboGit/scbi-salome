#!/usr/bin/env python
import getpass
import io
import os
import readline
import subprocess
import sys


readline.parse_and_bind("tab:complete")
eole = "eole.hpc.edf.fr"
gaia = "gaia.hpc.edf.fr"
nameOfEntriesToKill = ["porthospv431mpi"]

templateFile = "servers.pvsc"


def ping(nameOfHost):
    p = subprocess.Popen(["ping", "-c1", "-w1", nameOfHost],
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p.communicate()
    return p.returncode


def checkEDFRD():
    """
    To test connections
    """
    nni = getpass.getuser()
    if ping(eole) != 0 and ping(gaia) != 0:
        sys.exit('Cluster Eole and Gaia unavailable')
    return nni


def writeFromScratchXMLFile(fileName, nni):
    """
    To create xml file if it does not exist yet.
    """
    xmlC = io.open(templateFile, 'r').read()
    a = xmlC.replace("%s", nni)
    with io.open(fileName, "w") as f:
        f.write(prettyPrintXml(a))
        f.flush()
    pass


def tryToAddServersInXMLFile(userFileName, nni):
    """
    If the xml file exists, we try to add new servers in it.
    """
    import xml.etree.ElementTree as ET
    import re

    tree = ET.parse(userFileName)
    userFileRoot = tree.getroot()
    if userFileRoot.tag != "Servers":
        return
    for child in userFileRoot:
        if child.tag != "Server":
            return
    writeNeeded = False

    # REMOVE the server if it's the nameOfEntriesToKill list
    for nameOfEntryToKill in nameOfEntriesToKill:
        elts = [child for child in userFileRoot if child.attrib["name"] == nameOfEntryToKill]
        for elt in elts:
            writeNeeded = True
            userFileRoot.remove(elt)
        pass

    xmlTemplate = ET.parse(templateFile)

    for entry in xmlTemplate.getroot():
        # name of the server we want to add
        nameOfEntry = entry.attrib['name']

        entryStr = ET.tostring(entry).decode()
        # if the server is already in the user's server.pvsc file we are going to update it
        elts = [child for child in userFileRoot if child.attrib["name"] == nameOfEntry]

        # UPDATE the server if it was already in the config file of the user
        for elt in elts:
            eltStr = ET.tostring(elt).decode()
            if "%s" in entryStr:
                elt2 = ET.fromstring(entryStr % (nni))
            else:
                elt2 = ET.fromstring(entryStr)

            if re.sub("[\s]+", "", eltStr) != re.sub("[\s]+", "", ET.tostring(elt2).decode()):
                writeNeeded = True
                userFileRoot.remove(elt)
                userFileRoot.append(elt2)
            pass

        # ADD the server if it's not in the user config file
        if len(elts) == 0:
            writeNeeded = True
            if "%s" in entryStr:
                elt = ET.fromstring(entryStr % (nni))
            else:
                elt = ET.fromstring(entryStr)

            userFileRoot.append(elt)

    if writeNeeded:
        # before overloading it store the old one
        import tempfile
        dn = os.path.dirname(userFileName)
        bn = os.path.splitext(os.path.basename(userFileName))
        f = tempfile.mkstemp(suffix=bn[1], prefix='%s_' % (bn[0],), dir=dn)
        with io.open(userFileName, 'r') as userfile:
            os.write(f[0], userfile.read().encode())
        os.close(f[0])
        #
        st = ET.tostring(userFileRoot)
        with io.open(userFileName, "w") as f:
            f.write(prettyPrintXml(st))
            f.flush()
    else:
        return  # entry nameOfEntry already present -> do not touch anything
    pass


def prettyPrintXml(string):
    """
    To write xml files without extra empty lines
    """
    from xml.dom.minidom import parseString

    # from : http://stackoverflow.com/questions/14479656/empty-lines-while-using-minidom-toprettyxml
    return '\n'.join([line for line in parseString(string).toprettyxml(indent=' ' * 2).split('\n') if line.strip()])


if __name__ == '__main__':
    """
    We install server.psvc file in ~/.config/ParaView
    """
    nni = checkEDFRD()
    configPath = os.path.expanduser(os.path.join("~", ".config", "ParaView"))
    if not os.path.exists(configPath):
        os.makedirs(configPath)
    userServersPvsc = os.path.join(configPath, "servers.pvsc")
    if not os.path.exists(userServersPvsc) or os.stat(userServersPvsc).st_size == 0:
        writeFromScratchXMLFile(userServersPvsc, nni)
    else:
        tryToAddServersInXMLFile(userServersPvsc, nni)
