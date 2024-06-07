import os, shutil, string
# import pandas as pd
# import re
# import numpy as np
# import time
# import warnings

def readXMPfiles(XMPdirectory):
    XMPdictionary = {}
    for XMPfile in os.listdir(XMPdirectory):
        if XMPfile.endswith('.xmp'):
            XMPfullpath = os.path.join(XMPdirectory, XMPfile)
            XMPbase = os.path.basename(XMPfile)
            print('Reading ' + XMPbase)
            with open(XMPfullpath, 'r') as f:
                XMPdictionary[XMPbase] = f.read()

    print('finished reading text')