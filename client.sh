#!/bin/sh
if [ -z "$1" ];then
echo "[!] Provide server ip as argument"
exit
fi
python3 client.py "$1"
