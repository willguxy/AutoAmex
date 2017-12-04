#!/bin/bash
# get login_id with given offer from log_files, support argument expansions
# Example: ./getOffer.sh staples tmp/*
if [ "$2" = '' ]; then
  grep -i -C 1 "$1" *.log | grep ID | grep -oE '[^ ]+$'
else
  for n in "${@:2}"; do
    grep -i -C 1 "$1" "$n" | grep ID | grep -oE '[^ ]+$'
  done
fi
