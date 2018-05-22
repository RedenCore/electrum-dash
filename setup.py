#!/usr/bin/env python3

# python setup.py sdist --format=zip,gztar

from setuptools import setup
import os
import sys
import platform
import imp
import argparse

version = imp.load_source('version', 'lib/version.py')

if sys.version_info[:3] < (3, 4, 0):
    sys.exit("Error: Electrum-REDEN requires Python version >= 3.4.0...")

data_files = []

if platform.system() in ['Linux', 'FreeBSD', 'DragonFly']:
    parser = argparse.ArgumentParser()
    parser.add_argument('--root=', dest='root_path', metavar='dir', default='/')
    opts, _ = parser.parse_known_args(sys.argv[1:])
    usr_share = os.path.join(sys.prefix, "share")
    if not os.access(opts.root_path + usr_share, os.W_OK) and \
       not os.access(opts.root_path, os.W_OK):
        if 'XDG_DATA_HOME' in os.environ.keys():
            usr_share = os.environ['XDG_DATA_HOME']
        else:
            usr_share = os.path.expanduser('~/.local/share')
    data_files += [
        (os.path.join(usr_share, 'applications/'), ['electrum-reden.desktop']),
        (os.path.join(usr_share, 'pixmaps/'), ['icons/electrum-reden.png'])
    ]

setup(
    name="Electrum-REDEN",
    version=version.ELECTRUM_VERSION,
    install_requires=[
        'pyaes>=0.1a1',
        'ecdsa>=0.9',
        'pbkdf2',
        'requests',
        'qrcode',
        'protobuf',
        'dnspython',
        'jsonrpclib-pelix',
        'PySocks>=1.6.6',
        'x11_hash>=1.4',
    ],
    packages=[
        'electrum_reden',
        'electrum_reden_gui',
        'electrum_reden_gui.qt',
        'electrum_reden_plugins',
        'electrum_reden_plugins.audio_modem',
        'electrum_reden_plugins.cosigner_pool',
        'electrum_reden_plugins.email_requests',
        'electrum_reden_plugins.hw_wallet',
        'electrum_reden_plugins.keepkey',
        'electrum_reden_plugins.labels',
        'electrum_reden_plugins.ledger',
        'electrum_reden_plugins.trezor',
        'electrum_reden_plugins.digitalbitbox',
        'electrum_reden_plugins.virtualkeyboard',
    ],
    package_dir={
        'electrum_reden': 'lib',
        'electrum_reden_gui': 'gui',
        'electrum_reden_plugins': 'plugins',
    },
    package_data={
        'electrum_reden': [
            'servers.json',
            'servers_testnet.json',
            'currencies.json',
            'www/index.html',
            'wordlist/*.txt',
            'locale/*/LC_MESSAGES/electrum.mo',
        ]
    },
    scripts=['electrum-reden'],
    data_files=data_files,
    description="Lightweight Redenpay Wallet",
    maintainer="akhavr",
    maintainer_email="akhavr@khavr.com",
    license="MIT License",
    url="https://electrum.reden.org",
    long_description="""Lightweight Redenpay Wallet"""
)
