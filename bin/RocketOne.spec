# -*- mode: python -*-
a = Analysis(['RocketOne\\RocketOne.py'],
             pathex=['C:\\Python27', 'C:\\Python27\\Lib', 'C:\\Python27\\Lib\\site-packages', 'C:\\Python27\\Lib\\site-packages\\PySide', 'F:\\Aptana\\RocketOne'],
             hiddenimports=['PySide.QtNetwork'],
             hookspath=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=1,
          name=os.path.join('build\\pyi.win32\\RocketOne', 'RocketOne.exe'),
          debug=True,
          strip=None,
          upx=True,
          console=True , icon='QML\\images\\RocketOne_512px_clear.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=None,
               upx=True,
               name=os.path.join('dist', 'RocketOne'))
