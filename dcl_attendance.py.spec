# -*- mode: python -*-

block_cipher = None


a = Analysis(['dcl_attendance.py.py'],
             pathex=['C:\\Users\\Administrator\\Documents\\Attendance_Dont_Delete'],
             binaries=[],
             datas=[],
             hiddenimports=['babel.numbers'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='dcl_attendance.py',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True )
