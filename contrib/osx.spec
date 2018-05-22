# -*- mode: python -*-
import os
import os.path
import sys


for i, x in enumerate(sys.argv):
    if x == '--name':
        cmdline_name = sys.argv[i+1]
        break
else:
    raise BaseException('no name')

PY36BINDIR =  os.environ.get('PY36BINDIR')

hiddenimports = [
    'lib',
    'lib.base_wizard',
    'lib.plot',
    'lib.qrscanner',
    'lib.websockets',
    'gui.qt',

    'mnemonic',  # required by python-trezor

    'plugins',

    'plugins.hw_wallet.qt',

    'plugins.audio_modem.qt',
    'plugins.cosigner_pool.qt',
    'plugins.digitalbitbox.qt',
    'plugins.email_requests.qt',
    'plugins.keepkey.qt',
    'plugins.labels.qt',
    'plugins.trezor.qt',
    'plugins.ledger.qt',
    'plugins.virtualkeyboard.qt',
]

datas = [
    ('lib/servers.json', 'electrum_reden'),
    ('lib/servers_testnet.json', 'electrum_reden'),
    ('lib/currencies.json', 'electrum_reden'),
    ('lib/locale', 'electrum_reden/locale'),
    ('lib/wordlist', 'electrum_reden/wordlist'),
]

# https://github.com/pyinstaller/pyinstaller/wiki/Recipe-remove-tkinter-tcl
sys.modules['FixTk'] = None
excludes = ['FixTk', 'tcl', 'tk', '_tkinter', 'tkinter', 'Tkinter']

a = Analysis(['electrum-reden'],
             pathex=['plugins'],
             hiddenimports=hiddenimports,
             datas=datas,
             excludes=excludes,
             runtime_hooks=['pyi_runtimehook.py'])

# http://stackoverflow.com/questions/19055089/
for d in a.datas:
    if 'pyconfig' in d[0]:
        a.datas.remove(d)
        break

# Add TOC to electrum_reden, electrum_reden_gui, electrum_reden_plugins
for p in sorted(a.pure):
    if p[0].startswith('lib') and p[2] == 'PYMODULE':
        a.pure += [('electrum_reden%s' % p[0][3:] , p[1], p[2])]
    if p[0].startswith('gui') and p[2] == 'PYMODULE':
        a.pure += [('electrum_reden_gui%s' % p[0][3:] , p[1], p[2])]
    if p[0].startswith('plugins') and p[2] == 'PYMODULE':
        a.pure += [('electrum_reden_plugins%s' % p[0][7:] , p[1], p[2])]

pyz = PYZ(a.pure)

exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          debug=False,
          strip=False,
          upx=False,
          console=False,
          icon='icons/electrum-reden.ico',
          name=os.path.join('build/electrum-reden/electrum-reden', cmdline_name))

# trezorctl separate bin
tctl_a = Analysis([os.path.join(PY36BINDIR, 'trezorctl')],
                  hiddenimports=['pkgutil'],
                  excludes=excludes,
                  runtime_hooks=['pyi_tctl_runtimehook.py'])

tctl_pyz = PYZ(tctl_a.pure)

tctl_exe = EXE(tctl_pyz,
           tctl_a.scripts,
           exclude_binaries=True,
           debug=False,
           strip=False,
           upx=False,
           console=True,
           name=os.path.join('build/electrum-reden/electrum-reden', 'trezorctl.bin'))

coll = COLLECT(exe, tctl_exe,
               a.binaries,
               a.datas,
               strip=False,
               upx=False,
               name=os.path.join('dist', 'electrum-reden'))

app = BUNDLE(coll,
             name=os.path.join('dist', 'Electrum-REDEN.app'),
             appname="Electrum-REDEN",
	         icon='electrum-reden.icns',
             version = 'ELECTRUM_VERSION')
