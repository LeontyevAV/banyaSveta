#!/usr/bin/env bash
set -e
cd /home/leontyevav/work/bots/banyaSveta
for f in services_check inline_check prev_check menu_check; do
  echo "=== $f ==="
  sed 's#/home/sasha#/home/leontyevav#g' "tmp/$f.py" > /tmp/_chk.py
  python3 /tmp/_chk.py
done
