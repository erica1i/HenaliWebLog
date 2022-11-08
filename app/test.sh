#!bin/#!/usr/bin/env bash
rm test.db
python build_db.py
python db_testing_code.py

python __init__.py
