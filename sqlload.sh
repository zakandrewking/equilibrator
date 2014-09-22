#!/bin/bash

gunzip -c data/sqldump.txt.gz | mysql -u zaking -D equilibrator
