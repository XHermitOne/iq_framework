#!/bin/sh

pygettext --output-dir=./locale/ --output=iq.pot ./
pygettext --output-dir=./locale/ --output=iq_scanner.pot ./iq_scanner/ 
pygettext --output-dir=./locale/ --output=iq_report.pot ./iq_report/ 
