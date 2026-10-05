# scbi-salome

Setup Configure Build Install - Scripts for building SALOME

Those are based on the SCBI build driver. See project
and documentation here: https://github.com/TurboGit/scbi

# Install

First some prerequisites for the SCBI driver itself:

```
 apt install -y git rsync gcc lsb-release
```

The SCBI driver is integrated as sub-module.

```
 git clone --recurse-submodule https://github.com/TurboGit/scbi-salome.git
 cd ./scbi-salome
 make
```

The SCBI driver is installed into $HOME/.local/bin, if not already in
your PATH you need to add it:

```
 export PATH=$HOME/.local/bin:$PATH
```

# Install some prerequisites

  This is to ensure that some natives modules are used instead of building
  them. The list above is for Debian-13:

```
 apt install g++ wget ftp libyaml-dev python3-pippython3-yaml python3-toml \
     python3-zipp python3-scipy libnlopt-dev libnlopt-cxx-dev \
     python3-distutils-extra python3-nlopt python3-h5py python3-netcdf4 \
     libproj-dev libgdal-dev libqwt-qt5-dev python3-meshio \
     libhdf5-openmpi-dev libopenmpi-dev qtbase5-dev qttools5-dev \
     libqt5help5 libqt5x11extras5-dev libqt5opengl5-dev libqt5svg5-dev \
     qtxmlpatterns5-dev-tools pyqt5-dev pyqt5-dev-tools python3-pyqt5 \
     python3-pyqt5.sip libboost-filesystem-dev libboost-regex-dev \
     libboost-thread-dev libboost-chrono-dev libboost-date-time-dev \
     libboost-serialization-dev sphinx-common sphinx-intl doxygen \
     graphviz libcppunit-dev chrpath libgraphviz-dev python3-psutil \
     libfmt-dev libgl2ps-dev git-lfs libxt-dev libeigen3-dev \
     libxml2-utils libbz2-dev python3-matplotlib libcminpack-dev \
     libxrandr-dev libxinerama-dev libxcursor-dev libtbb-dev libglfw3-dev \
     tcl-dev tk-dev libfreetype-dev libfreeimage-dev rapidjson-dev \
     libxi-dev libxmu-dev
```

# A simple tutorial to build SALOME

  To build SALOME master just run:

```
 scbi --env=dev --deps --update --safe s-salome
```

  To build SALOME master and create an installer:

```
 scbi --env=dev --deps --update --safe --enable-installer s-salome
```
