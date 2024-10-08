#!/usr/bin/env python
import getpass
import io
import os
import readline
import subprocess
import sys, platform


readline.parse_and_bind("tab:complete")
gaia = "gaia.hpc.edf.fr"
cronos = "cronos.hpc.edf.fr"
nameOfEntriesToKill = []

out_dir_Path=os.path.dirname(os.path.realpath(__file__))
templateFile = os.path.join(out_dir_Path,"servers.pvsc")


# check if window
is_window = any(platform.win32_ver())

def ping(nameOfHost):
    if not is_window:
        cmd = ["ping", "-c1", "-w1", nameOfHost]
    else:
        cmd = ["ping", "-n", "1", nameOfHost]
    p = subprocess.Popen(cmd,  stderr=subprocess.PIPE)
    p.communicate()
    return p.returncode


def checkEDFRD():
    """
    To test connections
    """
    nni = getpass.getuser().lower()
    if ping(gaia) != 0 and ping(cronos) != 0:
        sys.exit('Cluster Gaia and Cronos unavailable')
    return nni

def nni2port(nni):
    def chr2code(c):
        if c.isdigit():
            return c
        else:
            return str(ord(c.upper()))
    nni2 = "".join([chr2code(elt) for elt in nni])
    port = "1{}{}{}{}".format(nni2[0],nni2[1],nni2[2],nni2[-1])
    return port

def writeFromScratchXMLFile(fileName, nni):
    """
    To create xml file if it does not exist yet.
    """
    dico = {"nni":nni,"PORTID":nni2port(nni)}
    xmlC = io.open(templateFile, 'r').read()
    a = xmlC%dico
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

    dico = {"nni":nni,"PORTID":nni2port(nni)}
    templateFile_subst = templateFile+".subst"

    with open(templateFile_subst,"w") as f:
        f.write(open(templateFile).read()%dico)

    xmlTemplate = ET.parse(templateFile_subst)

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
                elt = ET.fromstring(entryStr % dico)
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

def check_permission_cronos(checking_dir = ""):
    """
    To check permission in restrited directory on cronos:
    """

    user = getpass.getuser().lower()
    hostname = "cronos"

    cmd = "ssh -o StrictHostKeyChecking=no {}@{}.hpc.edf.fr \"bash -c 'ls {} && echo OK'\"".format(user ,hostname, checking_dir)
    p = subprocess.Popen(cmd,
                        shell=True,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT)
    out = p.communicate()
    if p.returncode == 0:
        return True
    else:
        return False

def set_cronos_app_directory(pvsc_file_path):
    """
    Put salome directory on servers.pvsc according the user right.
    """
    rd_dir = "/software/rd/salome/logiciels/salome"
    restricted_dir = "/software/restricted/salome/logiciels/salome"
    orig_dir = rd_dir

    def patching_servers_pvsc(app_dir):
        with open(pvsc_file_path, 'r') as pvsc_file:
            pvsc_data = pvsc_file.read()
        pvsc_data = pvsc_data.replace(orig_dir,app_dir)

        with open(pvsc_file_path, 'w') as pvsc_file:
            pvsc_file.writelines(pvsc_data)

    if check_permission_cronos(rd_dir):
        pass
    elif check_permission_cronos(restricted_dir):
         patching_servers_pvsc(restricted_dir)
    else:
        print("ERROR: Vous n'avez pas les droits suffisants sur Cronos pour installer salome.")


if __name__ == '__main__':
    """
    We install server.psvc file in ~/.config/ParaView
    """
    nni = checkEDFRD()
    if not is_window:
        configPath = os.path.expanduser(os.path.join("~", ".config", "ParaView"))
    else:
        configPath = os.path.join(os.getenv("APPDATA"),"ParaView")
    if not os.path.exists(configPath):
        os.makedirs(configPath)
    userServersPvsc = os.path.join(configPath, "servers.pvsc")

    if not os.path.exists(userServersPvsc) or os.stat(userServersPvsc).st_size == 0:
        writeFromScratchXMLFile(userServersPvsc, nni)
    else:
        tryToAddServersInXMLFile(userServersPvsc, nni)

    # Rajoute salome_install_dir en vérifiant le droit d'utilisateur sur cronos

    set_cronos_app_directory(userServersPvsc)