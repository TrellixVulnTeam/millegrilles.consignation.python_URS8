#!/bin/bash

# Fichier de setup pour container Docker (doit etre execute dans le container via Dockerfile)

GIT_NAME=MilleGrilles.consignation.python
GIT_FOLDER=$SRC_FOLDER/$GIT_NAME

REQ_FILE=$GIT_FOLDER/requirements.txt
if [ ! -f $REQ_FILE ]; then
    echo Fichier $REQ_FILE introuvable

    echo Repertoire git: $GIT_FOLDER
    echo Repertoire src: $SRC_FOLDER

    ls -la $SRC_FOLDER
    ls -la $GIT_FOLDER
    exit 1
fi

echo "Installer dependances Python avec pip: fichier $REQ_FILE"
# http_proxy=http://192.168.1.28:8000 pip3 install --no-cache-dir -r $REQ_FILE
pip3 install --no-cache-dir -r $REQ_FILE

# Fix pymongo, erreur cannot import abc (issue #305)
pip3 uninstall -y bson
pip3 uninstall -y pymongo
pip3 install pymongo

echo Installer package MilleGrilles.consignation
cd $GIT_FOLDER
python3 setup.py install

echo "Copier script demarrer dans $BUNDLE_FOLDER"
mkdir -p $BUNDLE_FOLDER
cp $GIT_FOLDER/scripts/demarrer*.py $BUNDLE_FOLDER
# Copier fichier de reference pour la configuration de tous les domaines
cp $GIT_FOLDER/scripts/domaines.json $BUNDLE_FOLDER

cd $BUNDLE_FOLDER
rm -rf $BUILD_FOLDER
