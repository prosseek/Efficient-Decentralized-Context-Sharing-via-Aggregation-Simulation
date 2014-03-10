#!/bin/sh
#SRCDIR="./context"
#sphinx-apidoc -F -o docs/sphinx $SRCDIR

cd docs/sphinx
make html
cd -