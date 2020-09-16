"""
    setup.py file for SWIG example
"""
from setuptools import setup, Extension
import os

polyiou_module = Extension('dotadev.polyiou._polyiou',
                           sources=['./dotadev/polyiou/polyiou.i', './dotadev/polyiou/polyiou.cpp'],
                           include_dirs=["./dotadev/polyiou"],
                           language='c++',
                           swig_opts=['-c++'])


setup(name='dotadev',
      version='0.1',
      packages=['dotadev'],
      package_dir={'dotadev': 'dotadev'},
      ext_modules=[polyiou_module],
      license="MIT",
      author="SWIG Docs",
      description="""Simple swig example from docs""",
      long_description=open("README.md").read(),
      )
