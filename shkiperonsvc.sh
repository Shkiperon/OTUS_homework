#!/bin/bash
if (( $# != 2 )); then
  echo "Need only two parameters (word for search and fullpath to logfile)."
  exit 1
fi
if [ ! -f "$2" ]; then
  echo "Looks like logfile does not exist. Stopping the service."
  exit 1
fi
echo "Starting Shkiperon Service. Will search $1 in $2 logfile"
while :
do
  if (( $(grep -c "$1" "$2") > 0 )); then
    echo "ALARM!!! Founded $1 in $2 logfile. Making rotation..."
    (mv "$2" "$2.rotated-$(date +'%Y%m%d-%H%M%S')"; touch "$2"; echo "Rotation done.") || (echo "Rotation has been FAILED. Stopping service."; exit 3)
  fi
  sleep 30s
done
