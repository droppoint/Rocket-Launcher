# -*- mode: python -*-
a = Analysis(['F:\\Aptana\\RocketOne\\RocketOne\\qml.py'],
             pathex=['F:\\Aptana\\RocketOne\\bin'],
             hiddenimports=[],
             hookspath=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name=os.path.join('dist', 'qml.exe'),
          debug=False,
          strip=None,
          upx=True,
          console=True )
