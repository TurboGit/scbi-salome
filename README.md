# scbi-salome

Setup Configure Build Install - Scripts for building SALOME

# Pre-requisite

  First you need to install the scbi driver.

  https://github.com/TurboGit/scbi

# Install

```
$ git clone https://gitlab.pleiade.edf.fr/pascal.obry/scbi-salome.git
$ cd ./scbi-salome.git
$ make
```

# A simple tutorial to build SALOME

  To build SALOME just run:

```
$ scbi --env=v95 --deps --update --safe salome
```

  To build SALOME and create an installer:

```
$ scbi --env=v95 --deps --update --safe --enable-installer salome
```
