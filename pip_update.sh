#!/usr/bin/env bash
python3 setup.py sdist bdist_wheel
python3 -m twine upload --repository-url https://upload.pypi.org/legacy/ --username diniscruz dist/*
rm -rf dist
rm -rf build
rm -rd pbx_gs_python_utils.egg-info
