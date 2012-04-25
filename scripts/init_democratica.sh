#!/bin/sh

python import_mps.py
python determine_mp_gender.py
python import_mp_photos.py
python import_legislatures.py
python import_linksets.py
python import_parties.py
python import_governments.py
python import_elections.py

echo 'Deputados OK, agora é importar as transcrições.'
echo
echo '  python import_transcripts.py -i <directório das transcrições>' 
