#!/bin/bash
cd kinematics
python setup.py build_ext --inplace
cd ..
mv kinematics/kinematics_c.so .
