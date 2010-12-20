#!/bin/sh

rm media/mp-photos/*
python manage.py reset deputados --noinput
cd scripts
python insert_data.py
cd ..
