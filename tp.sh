#!/bin/bash

SHOW_SOL=""
SHOW_TIME=""

#reading the arguments. 
POSITIONAL=()
while [[ $# -gt 0 ]]; do
  key="$1"

  case $key in
    -a)
      ALGOTYPE="$2"
      shift # past argument
      shift # past value
      ;;
    -e)
      EX="$2"
      shift # past argument
      shift # past value
      ;;
    -p)
      SHOW_SOL="-p"
      shift # past argument
      ;;
    -t)
      SHOW_TIME="-t"
      shift # past argument
      ;;
  esac
done

set -- "${POSITIONAL[@]}"


python3 main.py -a ${ALGOTYPE} -e ${EX} ${SHOW_SOL} ${SHOW_TIME}