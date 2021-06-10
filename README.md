# scbi-salome

Setup Configure Build Install - Scripts for building SALOME

# Pre-requisite

  First you need to install the scbi driver.

  https://github.com/TurboGit/scbi

# Install

```
$ git clone https://github.com/TurboGit/scbi-salome.git
$ cd ./scbi-salome
$ make
```

# A simple tutorial to build SALOME

  To build SALOME master just run:

```
$ scbi --env=xdev --deps --update --safe salome
```

  To build SALOME master and create an installer:

```
$ scbi --env=xdev --deps --update --safe --enable-installer salome
```
