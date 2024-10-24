#!/bin/bash
# set -xe

# dumb terminal stuff
CS=$(realpath .)
ln -sf "$CS/shell-fn" ~/.bash_aliases

# docs
mkdir -p ~/.man2pdf
ln -sf "$CS/man2pdf" ~/.man2pdf/man2pdf
