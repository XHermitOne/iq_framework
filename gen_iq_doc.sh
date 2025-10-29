#!/bin/sh

# Install:
# sudo apt install python3-sphinx python3-sphinxcontrib.apidoc

cd ~/dev/prj/work/iq_framework/
sphinx-apidoc --separate --full --output-dir ./ide/help/iq_documentation ./iq
make -C ./ide/help/iq_documentation html
