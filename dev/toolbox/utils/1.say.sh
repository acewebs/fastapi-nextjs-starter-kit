#!/bin/bash

if [ -t 1 ] && [ -z "${NO_COLOR:-}" ]; then
  RED='\033[0;31m'
  GREEN='\033[0;32m'
  YELLOW='\033[0;33m'
  BLUE='\033[0;34m'
  GRAY='\033[0;90m'
  NC='\033[0m'
else
  RED='' GREEN='' YELLOW='' BLUE='' GRAY='' NC=''
fi

info()    { echo -e "${BLUE}[i]${NC} $*"; }
success() { echo -e "${GREEN}[✓]${NC} $*"; }
warn()    { echo -e "${YELLOW}[!]${NC} $*"; }
error()   { echo -e "${RED}[✗]${NC} $*"; }
debug()   { [[ "${LOG_LEVEL:-}" == "debug" ]] && echo -e "${GRAY}[d]${NC} $*"; }
step()    { echo -e "${BLUE}→${NC} $*"; }
