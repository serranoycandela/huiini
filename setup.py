# -*- coding: utf-8 -*-
from distutils.core import setup
import py2exe, sys

sys.argv.append('py2exe')
#C:\Python34\python.exe setup.py
setup(
    windows=[
            {
                "script": "huiini.py",
                "icon_resources": [(1, "myicon.ico")]
            }
        ],


    options={
               "py2exe":{
                       "unbuffered": True,
                       "optimize": 2,
                       "includes":["PySide2.QtCore","PySide2.QtGui"]
               }
       },

)
