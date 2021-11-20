#!/bin/bash

SHOW_SOL=""

#reading the arguments. 
POSITIONAL=()
while [[ $# -gt 0 ]]; do
  key="$1"

  case $key in
    -e)
      EX="$2"
      shift # past argument
      shift # past value
      ;;
    -p)
      SHOW_SOL="-p"
      shift # past argument
      ;;
  esac
done

set -- "${POSITIONAL[@]}"


python3 main.py -e ${EX} ${SHOW_SOL}