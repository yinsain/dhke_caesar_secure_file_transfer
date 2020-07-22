#!/bin/sh
if [ ! -d "uploads" ];then
	mkdir uploads/
fi
python3 server.py
