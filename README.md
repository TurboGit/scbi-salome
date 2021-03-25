# scbi-salome

Setup Configure Build Install - Scripts for building SALOME

# Pre-requisite

  First you need to install the scbi driver.

  https://github.com/TurboGit/scbi

# Install

```
$ git clone https://github.com/TurboGit/scbi-salome
$ cd ./scbi-salome
$ make
```

# A simple tutorial to build SALOME

  To build SALOME just run:

```
$ scbi --env=v96 --deps --update --safe salome
```

  To build SALOME and create an installer:

```
$ scbi --env=v96 --deps --update --safe --enable-installer salome
```
