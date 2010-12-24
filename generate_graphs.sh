rm deputados.dot deputados.png
python modelviz.py deputados >| deputados.dot
dot deputados.dot -Tpng -o deputados.png
