import os, shutil, string
import re
import pandas as pd
# import numpy as np
# import time
# import warnings

def readXMPfiles(XMPdirectory):
    XMPdictionary = {}
    for XMPfile in os.listdir(XMPdirectory):
        if XMPfile.endswith('.xmp'):
            XMPfullpath = os.path.join(XMPdirectory, XMPfile)
            XMPbase = os.path.splitext(os.path.basename(XMPfile))[0]
            print('Reading ' + XMPbase)
            with open(XMPfullpath, 'r') as f:
                XMPdictionary[XMPbase] = f.read()

    first_xmp = XMPdictionary[next(iter(XMPdictionary))]
    search_exif = r'(?<=exif:)[a-zA-Z\d]+(?==)'
    search_crs = r'(?<=crs:)[a-zA-Z\d]+(?==)'
    exif_list = re.findall(search_exif, first_xmp)
    exif_list = ['exif ' + s for s in exif_list]
    crs_list = re.findall(search_crs, first_xmp)
    crs_list = ['crs ' + s for s in crs_list]

    all_columns = list(set(exif_list + crs_list))
    xmp_snapshot = pd.DataFrame([], columns=all_columns)
    
    row_index = 0
    row_values = []
    for key, value in XMPdictionary.items():
        for column in xmp_snapshot:
            search_values = column.split(' ')
            # search_re = r'(?<=' + search_values[0] + r':' + search_values[1] + r'=\")' + r'[a-zA-Z\d/:-]'
            search_re = r'(?<=' + search_values[0] + r':' + search_values[1] + '=)\"([^\"]*)\"'
            single_value = re.search(search_re, value)
            if single_value:
                row_values += single_value.group(0)
            else:
                row_values += 'No Value Found'

    print('finished reading text')