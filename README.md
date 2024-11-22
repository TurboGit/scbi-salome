# scbi-salome

Setup Configure Build Install - Scripts for building SALOME

Those are based on the SCBI build driver. See project
and documentation here: https://github.com/TurboGit/scbi

# Install

The SCBI driver is integrated as sub-module.

```
$ git clone --recurse-submodule https://github.com/TurboGit/scbi-salome.git
$ cd ./scbi-salome
$ make
```

# Install some prerequisites

  This is to ensure that some natives modules are used instead of building
  them. The list above is for Debian-12:

```
  apt install libnlopt-dev libnlopt-cxx-dev
  apt install python3-nlopt python3-h5py python3-netcdf4
  apt install libproj-dev
  apt install libgdal-dev
  apt install libhdf5-openmpi-dev libopenmpi-dev

  apt install qtbase5-dev qttools5-dev libqt5help5 libqt5x11extras5-dev
  apt install libqt5opengl5-dev libqt5svg5-dev qtxmlpatterns5-dev-tools
  apt install libqwt-qt5-dev
  apt install python3-meshio
  apt install pyqt5-dev pyqt5-dev-tools python3-pyqt5 python3-pyqt5.sip
```

# A simple tutorial to build SALOME

  To build SALOME master just run:

```
$ scbi --env=xdev --deps --update --safe s-salome
```

  To build SALOME master and create an installer:

```
$ scbi --env=xdev --deps --update --safe --enable-installer s-salome
```
