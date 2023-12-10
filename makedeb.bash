#!/usr/bin/env bash

rm -f *.deb

rm -rf deb/opt/
rm -rf deb/debian/cctv-manager/

mkdir -p deb/opt/cctv-manager/accounts/
rm -r deb/opt/cctv-manager/accounts/*

mkdir -p deb/opt/cctv-manager/cameras/
rm -r deb/opt/cctv-manager/cameras/*

mkdir -p deb/opt/cctv-manager/cctv_manager/
rm -r deb/opt/cctv-manager/cctv_manager/*

mkdir -p deb/opt/cctv-manager/design/
rm -r deb/opt/cctv-manager/design/*

mkdir -p deb/opt/cctv-manager/fixtures/
rm -r deb/opt/cctv-manager/fixtures/*

mkdir -p deb/opt/cctv-manager/records/
rm -r deb/opt/cctv-manager/records/*

mkdir -p deb/opt/cctv-manager/utils/
rm -r deb/opt/cctv-manager/utils/*

cp -r cctv_manager/accounts/* deb/opt/cctv-manager/accounts/
cp -r cctv_manager/cameras/* deb/opt/cctv-manager/cameras/
cp -r cctv_manager/cctv_manager/* deb/opt/cctv-manager/cctv_manager/
cp -r cctv_manager/design/* deb/opt/cctv-manager/design/
cp -r cctv_manager/fixtures/* deb/opt/cctv-manager/fixtures/
cp -r cctv_manager/records/* deb/opt/cctv-manager/records/
cp -r cctv_manager/utils/* deb/opt/cctv-manager/utils/
cp cctv_manager/manage.py deb/opt/cctv-manager/

cd deb || exit
dpkg-buildpackage  -us -uc -b
cd - || exit

rm -rf deb/opt/
rm -rf deb/debian/cctv-manager/
