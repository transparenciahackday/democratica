#!/bin/sh

rm media/mp-photos/*
python manage.py reset deputados --noinput
python manage.py reset dar --noinput
cd scripts
python insert_data.py
python insert_transcripts.py
cd ..
