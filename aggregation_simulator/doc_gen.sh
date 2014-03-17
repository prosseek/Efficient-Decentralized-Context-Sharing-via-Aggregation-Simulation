#!/bin/sh
PACKAGE_NAME=$(basename "$PWD")
SRCDIR="./$PACKAGE_NAME"
#sphinx-apidoc -F -o docs/sphinx $SRCDIR

cd docs/sphinx
make html
cd -