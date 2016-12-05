#!/bin/bash
if [ "$2" = '' ]; then
  grep -i -C 1 "$1" *.log | grep ID | grep -oE '[^ ]+$'
else
  for n in "${@:2}"; do
    grep -i -C 1 "$1" "$n" | grep ID | grep -oE '[^ ]+$'
  done
fi
