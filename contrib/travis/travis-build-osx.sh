#!/bin/bash
set -ev

if [[ -z $TRAVIS_TAG ]]; then
  echo TRAVIS_TAG unset, exiting
  exit 1
fi

BUILD_REPO_URL=https://github.com/akhavr/electrum-reden.git

cd build

git clone --branch $TRAVIS_TAG $BUILD_REPO_URL electrum-reden

cd electrum-reden

export PY36BINDIR=/Library/Frameworks/Python.framework/Versions/3.6/bin/
export PATH=$PATH:$PY36BINDIR
source ./contrib/travis/electrum_reden_version_env.sh;
echo wine build version is $ELECTRUM_REDEN_VERSION

sudo pip3 install -r contrib/requirements.txt
sudo pip3 install \
    x11_hash>=1.4 \
    btchip-python==0.1.24 \
    keepkey==4.0.2 \
    trezor==0.7.16

pyrcc5 icons.qrc -o gui/qt/icons_rc.py

export PATH="/usr/local/opt/gettext/bin:$PATH"
./contrib/make_locale
find . -name '*.po' -delete
find . -name '*.pot' -delete

cp contrib/osx.spec .
cp contrib/pyi_runtimehook.py .
cp contrib/pyi_tctl_runtimehook.py .

pyinstaller \
    -y \
    --name electrum-reden-$ELECTRUM_REDEN_VERSION.bin \
    osx.spec

sudo hdiutil create -fs HFS+ -volname "Electrum-REDEN" \
    -srcfolder dist/Electrum-REDEN.app \
    dist/electrum-reden-$ELECTRUM_REDEN_VERSION-macosx.dmg
