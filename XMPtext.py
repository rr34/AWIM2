import os, shutil, string
import re
import pandas as pd
# import numpy as np
# import time
# import warnings

def readXMPfiles(XMPdirectory):
    XMPdictionary = {}
    XMP_list = []
    # read all the XMP text into a dictionary of strings and also make a list for the rows index of the dataframe
    for XMPfile in os.listdir(XMPdirectory):
        if XMPfile.endswith('.xmp'):
            XMPfullpath = os.path.join(XMPdirectory, XMPfile)
            XMPbase = os.path.splitext(os.path.basename(XMPfile))[0]
            XMP_list.append(XMPbase)
            print('Reading ' + XMPbase)
            with open(XMPfullpath, 'r') as f:
                XMPdictionary[XMPbase] = f.read()


    # using one of the XMP files, get the names of all the columns of data contained in the XMPs
    first_xmp = XMPdictionary[next(iter(XMPdictionary))]
    search_exif = r'(?<=exif:)[a-zA-Z\d]+(?==)'
    search_crs = r'(?<=crs:)[a-zA-Z\d]+(?==)'
    exif_list = re.findall(search_exif, first_xmp)
    exif_list = ['exif ' + s for s in exif_list]
    crs_list = re.findall(search_crs, first_xmp)
    crs_list = ['crs ' + s for s in crs_list]
    awim_list = ['awim CommaSeparatedTags']

    all_columns = list(set(exif_list + crs_list + awim_list))
    xmp_snapshot = pd.DataFrame(columns=all_columns, index=XMP_list)
    
    for key, value in XMPdictionary.items():
        print('Scrubbing ' + key)
        for column in xmp_snapshot:
            search_values = column.split(' ')
            if search_values[0] == 'crs' or search_values[0] == 'exif':
                search_re = r'(?<=%s:%s=")([^"])*(?=")' % (search_values[0], search_values[1])
                single_value = re.search(search_re, value)
                if single_value:
                    single_value = single_value.group()
                else:
                    single_value = 'No value found.'
            elif search_values[0] == 'awim' and search_values[1] == 'CommaSeparatedTags':
                search_re = r'(?<=<dc:subject>).*(?=</dc:subject>)'
                tags_fulltext = re.search(search_re, value, re.DOTALL)
                if tags_fulltext:
                    search_re = r'(?<=rdf:li>)[a-zA-Z\d]+(?=</rdf:li>)'
                    tags = re.findall(search_re, tags_fulltext.group())
                    if tags:
                        single_value = ','.join(tags)
                    else: single_value = 'NoTags'
                else:
                    single_value = 'NoTags'

            xmp_snapshot.loc[key,column] = single_value

    xmp_snapshot = xmp_snapshot.sort_values('exif DateTimeOriginal')
    xmp_snapshot.insert(0, 'awim FrameNumber', range(1, 1 + len(xmp_snapshot)))

    latitude_txt_split = xmp_snapshot.iloc[0]['exif GPSLatitude'].split(',')
    latitude_hemisphere = latitude_txt_split[1][-1]
    latitude_txt_split[1] = latitude_txt_split[1][:-1]
    latitude_hemisphere_value = 1 if latitude_hemisphere == 'N' else -1
    latitude_value = latitude_hemisphere_value * (float(latitude_txt_split[0]) + float(latitude_txt_split[1])/60)
    longitude_txt_split = xmp_snapshot.iloc[0]['exif GPSLongitude'].split(',')
    longitude_hemisphere = longitude_txt_split[1][-1]
    longitude_txt_split[1] = longitude_txt_split[1][:-1]
    longitude_hemisphere_value = 1 if longitude_hemisphere == 'N' else -1
    longitude_value = longitude_hemisphere_value * (float(longitude_txt_split[0]) + float(longitude_txt_split[1])/60)

    latlng = [latitude_value, longitude_value]
    
    return xmp_snapshot, latlng


