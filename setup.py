# -*- coding: utf-8 -*-
"""
Created on Wed Mar 18 09:27:59 2020

@author: ulipa
"""
from distutils.core import setup
setup(
  name = 'mdfaPy',
  install_requieres = ['matplotlib','numpy','pandas','pyqt5','sklearn','numba'],
  version = '1.5',
  description = 'A multifractal analysis interface',
  author = 'ulipaeh',
  author_email = '',
  url = 'https://github.com/Ulipaeh/mdfaPy',
  keywords = ['DFA', 'MFDFA'],
  classifiers = [],
)