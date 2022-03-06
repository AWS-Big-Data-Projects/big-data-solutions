import re
import io
import sys
import boto3
import pandas as pd
import numpy as np
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from awsglue.context import GlueContext
from awsglue.job import Job
from io import StringIO
from botocore.exceptions import ClientError
import datetime
from collections import OrderedDict
import json
from urllib.parse import unquote_plus
from itertools import chain, starmap
from pandas import DataFrame, ExcelWriter
import xlrd
import xlsxwriter
import configparser
from zipfile import ZipFile
from io import BytesIO
import zipfile
import openpyxl
from openpyxl import Workbook
#########################################################################
"""
# create Workbook object
wb=Workbook()
# set file path
filepath="s3://mybucket/test1.xlsx"
# save workbook
wb.save(filepath)
"""
bucket = 'theegc'
filepath = 'demo1.xlsx'
df = pd.read_csv('s3://mybucket/test1.csv')
df2 = pd.read_csv('s3://mybucket/test2.csv')
for colname in df:
    if (  colname == 'originaltid'  ):
        df.rename(columns={'originaltid': 'tid'}, inplace=True, errors = 'raise')#new
for colname in df2:
    if (  colname == 'originaltid'  ):
        df2.rename(columns={'originaltid': 'tid'}, inplace=True, errors = 'raise')#new
convert_dict = {  'tid': str, 'zip': str  }
df = df.astype(convert_dict)
df2 = df2.astype(convert_dict)
df['ZIP_length'] = df.zip.str.len()
df['TID_length'] = df.tid.str.len()
print('Padding ZIP and TID columns')
df['tid'] = np.where( (df['TID_length'] > 1) & (df['TID_length'] < 9) ,df['tid'].apply(lambda x: str(x).rjust(9,"0")),df['tid'] )
df['zip'] = np.where( (df['ZIP_length'] > 1) & (df['ZIP_length'] < 5) ,df['zip'].apply(lambda x: str(x).rjust(5,"0")),df['zip'] )
df.drop(['TID_length', 'ZIP_length'], axis = 1,inplace= True)
df2['ZIP_length'] = df2.zip.str.len()
df2['TID_length'] = df2.tid.str.len()
print('Padding ZIP and TID columns')
df2['tid'] = np.where( (df2['TID_length'] > 1) & (df2['TID_length'] < 9) ,df2['tid'].apply(lambda x: str(x).rjust(9,"0")),df2['tid'] )
df2['zip'] = np.where( (df2['ZIP_length'] > 1) & (df2['ZIP_length'] < 5) ,df2['zip'].apply(lambda x: str(x).rjust(5,"0")),df2['zip'] )
df2.drop(['TID_length', 'ZIP_length'], axis = 1,inplace= True)

with io.BytesIO() as output:
    with ExcelWriter(output,engine='xlsxwriter', mode='w') as writer:
        df.to_excel(writer, sheet_name="Sheet1",index= False)
        df2.to_excel(writer, sheet_name="Sheet2",index= False)
    data = output.getvalue()
s3 = boto3.resource('s3')
s3.Bucket(bucket).put_object(Key=filepath, Body=data)
