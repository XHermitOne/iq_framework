# !/bin/sh

# Packages necessary for working on projects in Python:
# Tested on Ubuntu 18.04.LTS

# [NOTE] For automatic password entry for sudo, you can use
# command construction:
# echo "password" | sudo --stdin command

# Git
sudo apt install --assume-yes git
# [NOTE] For create files by git with access 777:
umask 000

sudo apt install --assume-yes python3-pip

# Code analyzers
sudo apt install --assume-yes pylint3
sudo apt install --assume-yes python3-pep8

# Operating system
sudo apt install --assume-yes smbfs-utils
sudo apt install --assume-yes cifs-utils
sudo apt install --assume-yes nfs-common
sudo apt install --assume-yes indicator-applet-complete
sudo apt install --assume-yes ttf-mscorefonts-installer
sudo apt install --assume-yes python3-apt
sudo apt install --assume-yes smbclient
pip3 install pysmb

# Net
pip3 install ping3

# Work with the console
sudo apt install --assume-yes python3-dialog
sudo apt install --assume-yes python3-urwid
sudo apt install --assume-yes curl

# Color console
sudo apt install --assume-yes python3-termcolor
sudo apt install --assume-yes python3-colorama
pip3 install rich

# wxPython

# Needful
sudo apt install --assume-yes libsdl1.2debian
sudo apt install --assume-yes libsdl2-2.0-0
sudo apt install --assume-yes build-essential libgtk-3-dev

# Web in wxPython
sudo apt install --assume-yes libwebkit2gtk-4.0-dev

# For Ubuntu 16.04
# pip3 install -U -f https://extras.wxpython.org/wxPython4/extras/linux/gtk3/ubuntu-16.04 wxPython==4.0.7.post2 Pillow==7.0.0 numpy==1.16.6

# For Ubuntu 18.04
# pip3 install -U -f https://extras.wxpython.org/wxPython4/extras/linux/gtk3/ubuntu-18.04 wxPython==4.0.7.post2

# For Ubuntu 20.04
# pip3 install -U -f https://extras.wxpython.org/wxPython4/extras/linux/gtk3/ubuntu-20.04 wxPython==4.1.1

# For Ubuntu 22.04
pip3 install -U -f https://extras.wxpython.org/wxPython4/extras/linux/gtk3/ubuntu-22.04 wxPython==4.2.0


# Upgrade:
# pip3 install wxPython --upgrade
# Remove:
# pip3 uninstall wxPython

# Altered installation
# pip3 download wxPython
# pip3 wheel -v wxPython-4.0.1.tar.gz  2>&1 | tee build.log
# pip3 install wxPython-4.0.1-cp35-cp35m-linux_x86_64.whl

pip3 install pysvg-py3
sudo apt install --assume-yes imagemagick
sudo apt install --assume-yes inkscape

# Additionally
pip3 install objectlistview
sudo apt install --assume-yes python3-six
sudo apt install --assume-yes python3-matplotlib
# sudo apt install --assume-yes python3-wxmpl

# GTK+
sudo apt install --assume-yes python3-gi
sudo apt install --assume-yes python3-gi-cairo
sudo apt install --assume-yes gir1.2-gtk-3.0
sudo apt install --assume-yes glade
sudo apt install --assume-yes gir1.2-appindicator3-0.1 
sudo apt install --assume-yes libappindicator3-0.1-cil 
#sudo apt install --assume-yes libappindicator3-1
sudo apt install --assume-yes libayatana-appindicator3-1
sudo apt install --assume-yes gnome-shell-extension-appindicator

# JSONRPC (Ubuntu 20.04)
sudo apt install python3-jsonrpclib-pelix

# JSONRPC (Ubuntu 16.04)
# pip3 install jsonrpclib-pelix

# Database
sudo apt install --assume-yes python3-psycopg2
sudo apt install --assume-yes python3-sqlalchemy
sudo apt install --assume-yes unixodbc unixodbc-dev freetds-bin freetds-dev tdsodbc python3-pyodbc
sudo apt install --assume-yes python3-pymysql
sudo apt install --assume-yes sqlite3
sudo apt install --assume-yes sqlitebrowser

# For Ubuntu 16.04
# pip3 install JayDeBeApi
# For Ubuntu 18.04
# pip3 install JayDeBeApi3
# For Ubuntu 20.04
pip3 install jaydebeapi jpype1

# DBase
# pip3 install dbfpy
pip3 install dbfread
pip3 install dbfpy3

# xmltodict
pip3 install xmltodict

# Office
sudo apt install --assume-yes unoconv
sudo apt install --assume-yes python3-sane
sudo apt install --assume-yes python3-reportlab
sudo apt install --assume-yes python3-pypdf2
sudo apt install --assume-yes python3-odf python-odf-doc
sudo apt install --assume-yes libreoffice-java-common
sudo apt install --assume-yes python3-xlrd
sudo apt install --assume-yes python3-xlwt
sudo apt install --assume-yes python3-xlsxwriter
sudo apt install --assume-yes python3-openpyxl
sudo apt install --assume-yes pdf2svg
pip3 install pygal
pip3 install PyMuPDF
pip3 install img2pdf

pip3 install mtranslate

sudo apt install --assume-yes python3-jinja2

# IDE
sudo apt install --assume-yes poedit

# SCADA
sudo apt install --assume-yes gnuplot

# Data tables
# sudo apt install --assume-yes python3-pandas
pip3 install pandas
pip3 install plotly_express

# Maps
pip3 install folium
pip3 install yandex-maps
pip3 install dadata==20.7.0

# Java
pip3 install py4j

# 
sudo apt --fix-broken install --assume-yes

# iq
export IQ_PATH="$(dirname "$PWD")"

# Ubuntu 16.04
rm ~/.local/lib/python3.5/site-packages/iq.pth
echo $IQ_PATH >> ~/.local/lib/python3.5/site-packages/iq.pth

# Ubuntu 18.04
rm ~/.local/lib/python3.6/site-packages/iq.pth
echo $IQ_PATH >> ~/.local/lib/python3.6/site-packages/iq.pth

# Ubuntu 20.04
rm ~/.local/lib/python3.8/site-packages/iq.pth
echo $IQ_PATH >> ~/.local/lib/python3.8/site-packages/iq.pth

# Ubuntu 22.04
rm ~/.local/lib/python3.10/site-packages/iq.pth
echo $IQ_PATH >> ~/.local/lib/python3.10/site-packages/iq.pth

echo
echo " _     _____                                 _"
echo "|_|___|   __|___ ___ _____ ___ _ _ _ ___ ___| |_"
echo "| | . |   __|  _| .'|     | -_| | | | . |  _| '_|"
echo "|_|_  |__|  |_| |__,|_|_|_|___|_____|___|_| |_,_|"
echo "    |_|"
echo
