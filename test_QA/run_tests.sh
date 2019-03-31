#!/usr/bin/env bash


echo "*****************************"
echo "*** Running tests         ***"
echo "*****************************"

#pytest -s -v
pytest -s -v --ignore utils/slack
#pytest -s -v test_Update_Lambda_Functions.py