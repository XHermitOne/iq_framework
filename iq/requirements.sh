# !/bin/sh

# Packages necessary for working on projects in Python:
# Tested on Ubuntu 18.04.LTS

sudo apt install --assume-yes python3-pip

# Code analyzers
sudo apt install --assume-yes pylint3
sudo apt install --assume-yes python3-pep8

# Operating system
sudo apt install --assume-yes smbfs-utils
sudo apt install --assume-yes cifs-utils
sudo apt install --assume-yes smbclient 
sudo apt install --assume-yes indicator-applet-complete
sudo apt install --assume-yes ttf-mscorefonts-installer
sudo apt install --assume-yes python3-apt

# Work with the console
sudo apt install --assume-yes python3-dialog
sudo apt install --assume-yes python3-urwid
sudo apt install --assume-yes curl

# wxPython

# Needful
sudo apt install --assume-yes libsdl1.2debian
sudo apt install --assume-yes libsdl2-2.0-0
sudo apt install --assume-yes build-essential libgtk-3-dev

# Web in wxPython
sudo apt install --assume-yes libwebkit2gtk-4.0-dev

# For Ubuntu 16.04
pip3 install -U -f https://extras.wxpython.org/wxPython4/extras/linux/gtk3/ubuntu-16.04 wxPython

# Upgrade:
# pip3 install wxPython --upgrade
# Remove:
# pip3 uninstall wxPython

# For Ubuntu 18.04
# pip3 install -U -f https://extras.wxpython.org/wxPython4/extras/linux/gtk3/ubuntu-18.04 wxPython

# Altered installation
# pip3 download wxPython
# pip3 wheel -v wxPython-4.0.1.tar.gz  2>&1 | tee build.log
# pip3 install wxPython-4.0.1-cp35-cp35m-linux_x86_64.whl

# Additionally
pip3 install objectlistview
sudo apt install --assume-yes python3-six
sudo apt install --assume-yes python3-matplotlib
# sudo apt install --assume-yes python3-wxmpl

# Database
sudo apt install --assume-yes python3-psycopg2
sudo apt install --assume-yes python3-sqlalchemy
sudo apt install --assume-yes unixodbc unixodbc-dev freetds-bin freetds-dev tdsodbc python3-pyodbc

# For Ubuntu 16.04
pip3 install JayDeBeApi
# For Ubuntu 18.04
# pip3 install JayDeBeApi3

# DBase
# pip3 install dbfpy
pip3 install dbfread


# Office
sudo apt install --assume-yes unoconv
sudo apt install --assume-yes python3-sane
sudo apt install --assume-yes python3-reportlab
sudo apt install --assume-yes python3-pypdf2
sudo apt install --assume-yes python3-odf python-odf-doc
sudo apt install --assume-yes libreoffice-java-common

pip3 install mtranslate

# 
sudo apt --fix-broken install --assume-yes

echo
echo  _     _____                                 _   
echo |_|___|   __|___ ___ _____ ___ _ _ _ ___ ___| |_ 
echo | | . |   __|  _| .'|     | -_| | | | . |  _| '_|
echo |_|_  |__|  |_| |__,|_|_|_|___|_____|___|_| |_,_|
echo     |_|     
echo

