# uncompyle6 version 3.9.0
# Python bytecode version base 3.6 (3379)
# Decompiled from: Python 3.8.1 (tags/v3.8.1:1b293b6, Dec 18 2019, 23:11:46) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/niltech/Downloads/train delay/systemcheck.py
# Compiled at: 2019-01-28 19:50:50
# Size of source mod 2**32: 615 bytes
import os
lst = list(os.listdir())
if 'model.json' not in lst or 'model.h5' not in lst:
    print('File not Found')
    raise SystemError
read = "\nimport os\nlst = list(os.listdir())\n#print(lst)\nif(not 'model.json' in lst or not 'model.h5' in lst):\n    print('File not Found')\n    raise(SystemError)\nelse:\n    pass\n    #print('Everything is fine')\n\n"