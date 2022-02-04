# Image pour scripts python millegrilles.transactionet certains domaines.
# Note: les fichiers doivent avoir ete copies dans le repertoire courant sous src/

FROM docker.maceroc.com/millegrilles_python_base:2022.0.0

ENV SRC_FOLDER=/opt/millegrilles/build/src

COPY scripts/ $BUILD_FOLDER/scripts
COPY ./ $SRC_FOLDER/millegrilles.consignation.python/

RUN $BUILD_FOLDER/scripts/setup.sh

USER mg_python
