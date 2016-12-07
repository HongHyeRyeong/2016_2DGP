# -*- mode: python -*-

block_cipher = None


a = Analysis(['mygame.py'],
             pathex=['C:\\2DGP\\2015182045\\2016_2DGP\\plants_vs_zombies'],
             binaries=None,
             datas=None,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='mygame',
          debug=False,
          strip=False,
          upx=True,
          console=True )
