#!/bin/bash
set -ev

if [[ -z $TRAVIS_TAG ]]; then
  echo TRAVIS_TAG unset, exiting
  exit 1
fi

BUILD_REPO_URL=https://github.com/akhavr/electrum-reden.git

cd build

git clone --branch $TRAVIS_TAG $BUILD_REPO_URL electrum-reden

docker run --rm \
    -v $(pwd):/opt \
    -w /opt/electrum-reden \
    -t zebralucky/electrum-reden-winebuild:Linux /opt/build_linux.sh

sudo find . -name '*.po' -delete
sudo find . -name '*.pot' -delete

sudo chown -R 1000 electrum-reden

docker run --rm \
    -v $(pwd)/electrum-reden:/home/buildozer/build \
    -t zebralucky/electrum-reden-winebuild:Kivy bash -c \
    'rm -rf packages && ./contrib/make_packages && mv ./contrib/packages . && ./contrib/make_apk'
