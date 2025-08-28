#!/usr/bin/env python3
"""Write a PyInstaller-compatible version_info.py file safely.

This script writes a small Python file (`version_info.py`) that can be
passed to PyInstaller with `--version-file` to embed file metadata.

Usage:
  python tools/write_version_info.py --tag v1.2.3 --sha abcdef --out version_info.py
"""
import argparse
import textwrap


def main():
    parser = argparse.ArgumentParser(description='Write version_info.py for PyInstaller')
    parser.add_argument('--tag', default='v0.0.0')
    parser.add_argument('--sha', default='')
    parser.add_argument('--out', default='version_info.py', help='Output path for version_info.py')
    args = parser.parse_args()

    tag = args.tag
    sha = args.sha
    out_path = args.out

    content = textwrap.dedent(f"""
    # -*- coding: utf-8 -*-
    from PyInstaller.utils.win32.versioninfo import VSVersionInfo, FixedFileInfo, StringFileInfo, StringTable, StringStruct, VarFileInfo, VarStruct

    version_info = VSVersionInfo(
      ffi=FixedFileInfo(
        filevers=(1,0,0,0),
        prodvers=(1,0,0,0),
        mask=0x3f,
        flags=0x0,
        OS=0x40004,
        fileType=0x1,
        subtype=0x0,
        date=(0, 0)
      ),
      kids=[
        StringFileInfo(
          [
            StringTable(
              u'040904B0',
              [
                StringStruct(u'CompanyName', u'Palia Garden Optimizer'),
                StringStruct(u'FileDescription', u'Palia Garden Optimizer'),
                StringStruct(u'FileVersion', u'{tag}'),
                StringStruct(u'InternalName', u'PaliaGardenOptimizer'),
                StringStruct(u'LegalCopyright', u'Open Source'),
                StringStruct(u'OriginalFilename', u'PaliaGardenOptimizer.exe'),
                StringStruct(u'ProductName', u'Palia Garden Optimizer'),
                StringStruct(u'ProductVersion', u'{tag}'),
              ]
            )
          ]
        ),
        VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
      ]
    )
    """).strip()

    if sha:
        content = f"# commit: {sha}\n" + content

    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f'Wrote {out_path} with tag {tag}')


if __name__ == '__main__':
    main()
