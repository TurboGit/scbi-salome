#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Generates a new catalog of resources (file CatalogResources.xml) and configures
SALOME for the current user on the main HPC ressources used at EDF R&D.
You need acces rights to the remote resources in order to perform the
configuration.
If you don't have the required rights for a resource, it will not be added to
the catalog."""

from collections import defaultdict
import getpass
import logging
import optparse
import os
import subprocess
import sys

# lxml module is not always available
try:
    import lxml.etree as ET
except ImportError:
    import xml.etree.ElementTree as ET


SALOME_VERSION = "<salome_version>"


class Resource(object):
    def __init__(self, name, version, logger, nni_user):        
        self.name = name
        self.version = version
        self.logger = logger
        self.nni_user = nni_user       
        self.set_defaults()

    def set_defaults(self):
        if not self.nni_user:
            self.hostname = "%s.hpc.edf.fr" % self.name
        else:
            self.hostname = "%s@%s.hpc.edf.fr" % (self.nni_user,self.name)

        remote_salome_dir = self.get_remote_salome_dir()
        self.remote_appligen = os.path.join(remote_salome_dir, 'modules',
                                            'install',
                                            'KERNEL_%s' % self.version,
                                            'bin', 'salome', 'appli_gen.py')
        self.remote_salome_appli = os.path.join(remote_salome_dir,
                                                "appli_%s" % self.version)
        if not self.nni_user:
            username = getpass.getuser()
        else:
            username = self.nni_user
        if self.name == "cronos":
            scratch="/scratch/users"
        else:
            scratch="/scratch"
        self.remote_virtual_appli = os.path.join(scratch, username,
                                                 "appli_%s" % self.version)
        self.working_dir = os.path.join("/scratch", username, "workingdir")

# Attention à bien modifier à nouveau le répertoire en dur pour version officielle une fois les tests terminés :
#  /projets/salome/logiciels/salome/
    def get_remote_salome_dir(self):
        if self.name == "cronos":
            return "/software/rd/salome/logiciels/salome/%s" % self.version
        else:
            return "/projets/salome/logiciels/salome/%s" % self.version


    def prepare(self):
        stdout = sys.stdout
        stderr = sys.stderr
        if not self.logger.isEnabledFor(logging.INFO):
            FNULL = open(os.devnull, 'w')
            stdout = FNULL
            stderr = FNULL
        ret = subprocess.call(["ssh", "-oStrictHostKeyChecking=no",
                               "-oBatchMode=yes",
                               self.hostname,
                               self.remote_appligen,
                               '--prefix=' + self.remote_virtual_appli,
                               '--config=' + self.remote_salome_appli + "/config_appli.xml"],
                              stdout=stdout, stderr=stderr)
        if not self.logger.isEnabledFor(logging.INFO):
            FNULL.close()
        return ret

    def addToCatalog(self, catalog):
        print("Your virtual application on %s is available on %s "%(self.name,self.remote_virtual_appli))
        m = ET.Element('machine')
        m.set("name", self.name)
        m.set("hostname", self.hostname)
        m.set("appliPath", self.remote_virtual_appli)
        m.set("type", "cluster")
        m.set("protocol", "ssh")
        m.set("iprotocol", "srun")
        m.set("workingDirectory", self.working_dir)
        m.set("canLaunchBatchJobs", "true")
        m.set("canRunContainers", "false")
        m.set("batch", "slurm")
        m.set("mpi", "no mpi")
        catalog.getroot().append(m)


def addLocalhost(catalog):
  """ Localhost settings.
      Leave default values. Only nbOfNodes is changed.
  """
  m = ET.Element('machine')
  import socket
  m.set("hostname", socket.gethostname())
  import multiprocessing
  m.set("nbOfNodes", str(multiprocessing.cpu_count()))
  catalog.getroot().append(m)

if __name__ == '__main__':
    usage = """usage: %prog [options]
Generates a new catalog of resources (file CatalogResources.xml) and configures
SALOME for the current user on the main HPC ressources used at EDF R&D.
You need acces rights to the remote resources in order to perform the
configuration.
If you don't have the required rights for a resource, it will not be added to
the catalog."""
    parser = optparse.OptionParser(usage=usage)
    parser.add_option("-v", "--version", help="SALOME version (default: %default)",
                      default=SALOME_VERSION)
    parser.add_option("-q", "--quiet", action="store_true",
                      help="Quiet mode")
    parser.add_option("-b", "--verbose", action="store_true",
                      help="Verbose mode")
    parser.add_option("-f", "--file", dest="filename",
                      help="Catalog Resources file path (default: %default).",
                      default="CatalogResources.xml")
    parser.add_option("-i", "--interactiv", dest="interactiv",
                      action="store_true",
                      help="Interactiv mode - ask confirmation before adding a resource.",
                      default=False)
    parser.add_option("-a", "--always-add", dest="always", action="store_true",
                      help="Add the resource to the catalog even if the remote\
                      configuration fails.",
                      default=False)
    parser.add_option("-n", "--no-remote", dest="noremote", action="store_true",
                      help="Do not try to execute the configuration on the \
                      remote resource.",
                      default=False)
    parser.add_option("-u", "--user_nni", default='')

    (options, args) = parser.parse_args()

    logger = logging.getLogger('CREATE_CATALOG')
    formatter = logging.Formatter('%(asctime)s - %(name)s - '
                                  '%(levelname)s - %(message)s')
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.WARNING)
    if options.verbose:
        logger.setLevel(logging.DEBUG)
    if options.quiet:
        logger.setLevel(logging.ERROR)

    catalog = ET.ElementTree(ET.Element('resources'))

    # Ce dictionnaire relie un cluster à une classe
    # Par défaut la classe Resource est renvoyée
    cluster_to_resource = defaultdict(lambda: Resource)

    for cluster in ["gaia", "cronos"]:
        r = cluster_to_resource[cluster](cluster, options.version, logger, options.user_nni)
        logger.debug("Processing resource %s." % r.name)
        rep = "y"
        if options.interactiv:
            rep = input("Configure %s? (y|n)" % r.name)
            while rep not in ("y", "n"):
                rep = input("Configure %s? (y|n)" % r.name)
        if rep == "y":
            if options.noremote:
                ok = 0
            else:
                ok = r.prepare()
            logger.debug("Adding resource %s to the catalog." % r.name)
            if ok == 0:
                r.addToCatalog(catalog)
            else:
                logger.warning("%s configuration failed! "
                               "Verify your acces rights to %s and try again."
                               % (r.name, r.hostname))
                if options.always:
                    r.addToCatalog(catalog)
                else:
                    logger.info("%s was not added to the resource catalog."
                                % r.name)
    addLocalhost(catalog)
    # pretty_print works only with lxml
    try:
      catalog.write(options.filename, pretty_print=True)
    except:
      catalog.write(options.filename)
