#!/bin/sh
PACKAGE_NAME=context
# The package `context` is in current directory.
PYTHONPATH=.:$PYTHONPATH python tests/test_context.py
python -m $PACKAGE_NAME.context

PYTHONPATH=.:$PYTHONPATH python tests/test_utils.py
python -m $PACKAGE_NAME.utils