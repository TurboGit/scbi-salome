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

# A simple tutorial to build SALOME

  To build SALOME master just run:

```
$ scbi --env=xdev --deps --update --safe s-salome
```

  To build SALOME master and create an installer:

```
$ scbi --env=xdev --deps --update --safe --enable-installer s-salome
```

# OS Specific Instructions

## CentOS

For now on CentOS and Debian-9 the documentation cannot be built. The
compilation must be done with the `--enable-no-doc` option:

```
$ scbi --env=xdev --deps --update --enable-no-doc --safe s-salome
```
