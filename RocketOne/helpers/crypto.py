# -*- coding: UTF-8 -*-
'''
Created on 05.10.2012

@author: APartilov
'''

import hashlib


m = hashlib.sha256()

m.update("Alex")
m.update("13112002")

stri = m.hexdigest()
print stri
