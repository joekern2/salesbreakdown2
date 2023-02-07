# -*- coding: utf-8 -*-
"""
Created on Wed Dec 14 11:23:11 2022

@author: jkern
"""

import numpy as np
import pandas as pd
import streamlit as st
import os

### read excel functions
def getFiles():
    dtot = 0
    dCharles = 0
    dEric = 0
    dRyan = 0
    dShane = 0
    dSales = 0
    check = 0
    mcheck = 0
    c1check = 0
    c2check = 0
    c3check = 0
    c4check = 0
    c5check = 0
    
    
    
    st.header('In first box, upload the MasterPL file or a Salesman\'s PL file - the file that will hold the updated data.\n')
    
    st.header('In the remaining columns, upload the salesman\'s Entries file - the files that have the data to be loaded into the first file.\n If uploading data for the masterPL, make sure to load all four salesmen\'s entry files.')

    uploaded_filem = st.file_uploader("Upload Master File")
    if uploaded_filem is not None:
        mcheck = 1
        #read xls or xlsx
        filem=pd.ExcelFile(uploaded_filem)
        dtot = {sheet_name: filem.parse(sheet_name) 
                    for sheet_name in filem.sheet_names} 
    else:
        st.warning("MasterPL or NamePL if for one Salesman")

    st.write('\n========================================================================================')
    st.write('\n')

    uploaded_filec = st.file_uploader("Upload Entries sheet for Charles")
    if uploaded_filec is not None:
        c1check = 1
        #read xls or xlsx
        filec=pd.ExcelFile(uploaded_filec)
        dCharles = {sheet_name: filec.parse(sheet_name) 
                    for sheet_name in filec.sheet_names} 
    else:
        st.warning("NamePLEntries File for Salesman 1")       
        
    st.write('\n========================================================================================')
    st.write('\n')

    uploaded_filee = st.file_uploader("Upload Entries sheet for Eric")
    if uploaded_filee is not None:
        c2check = 1
        #read xls or xlsx
        filee=pd.ExcelFile(uploaded_filee)
        dEric = {sheet_name: filee.parse(sheet_name) 
                    for sheet_name in filee.sheet_names} 
    else:
        st.warning("NamePLEntries File for Salesman 2")
        
    st.write('\n========================================================================================')
    st.write('\n')

    uploaded_filer = st.file_uploader("Upload Entries sheet for Ryan")
    if uploaded_filer is not None:
        c3check = 1
        #read xls or xlsx
        filer=pd.ExcelFile(uploaded_filer)
        dRyan = {sheet_name: filer.parse(sheet_name) 
                    for sheet_name in filer.sheet_names} 
    else:
        st.warning("NamePLEntries File for Salesman 3")
        
    st.write('\n========================================================================================')
    st.write('\n')
  
    uploaded_files = st.file_uploader("Upload Entries sheet for Shane")
    if uploaded_files is not None:
        c4check = 1
        #read xls or xlsx
        files=pd.ExcelFile(uploaded_files)
        dShane = {sheet_name: files.parse(sheet_name) 
                    for sheet_name in files.sheet_names} 
    else:
        st.warning("NamePLEntries File for Salesman 4")
        
    st.write('\n========================================================================================')
    st.write('\n')
    
    uploaded_files = st.file_uploader("Upload Entries sheet for Salesman 5")
    if uploaded_files is not None:
        c5check = 1
        #read xls or xlsx
        file5=pd.ExcelFile(uploaded_files)
        dSales = {sheet_name: file5.parse(sheet_name) 
                    for sheet_name in file5.sheet_names} 
    else:
        st.warning("NamePLEntries File for Salesman 5")
        
    st.write('\n========================================================================================')
    st.write('\n')
    
    

    selection = st.radio(
    "Who\'s P&L would you like to update?",
    ('Master', 'Charles', 'Eric', 'Ryan', 'Shane', 'Salesman 5'))
    
    check = 100
    
    if selection == 'Master':
        check = 0
    elif selection == 'Charles':
        check = 1
    elif selection == 'Eric':
        check = 2
    elif selection == 'Ryan':
        check = 3
    elif selection == 'Shane':
        check = 4
    elif selection == 'Salesman 5':
        check = 5



    
    return dtot, dCharles, dEric, dRyan, dShane, dSales, check, mcheck, c1check, c2check, c3check, c4check, c5check


def getTotals(master, c1, c2, c3, c4, c5, c, c1c, c2c, c3c, c4c, c5c):
    master['Salesman P&L']['Unnamed: 4'][10] = 0
    master['Salesman P&L']['Unnamed: 5'][10] = 0
    master['Salesman P&L']['Unnamed: 8'][10] = 0
    master['Salesman P&L']['Unnamed: 9'][10] = 0
    master['Salesman P&L']['Unnamed: 12'][10] = 0
    master['Salesman P&L']['Unnamed: 13'][10] = 0
    #commission
    master['Salesman P&L']['Unnamed: 13'][2] = 0
    for i in range(12):
        month = master['Salesman P&L']['SALESMAN P&L'][14:26].iloc[i]
        x, y = sumNewTrucks(c1, c2, c3, c4, c5, month, c, c1c, c2c, c3c, c4c, c5c)
        master['Salesman P&L']['Unnamed: 4'][14 + i] = x
        master['Salesman P&L']['Unnamed: 4'][10] += x
        master['Salesman P&L']['Unnamed: 5'][14 + i] = y
        master['Salesman P&L']['Unnamed: 5'][10] += y
        
        a, b = sumOldTrucks(c1, c2, c3, c4, c5, month, c, c1c, c2c, c3c, c4c, c5c)
        master['Salesman P&L']['Unnamed: 8'][14 + i] = a
        master['Salesman P&L']['Unnamed: 8'][10] += a
        master['Salesman P&L']['Unnamed: 9'][14 + i] = b
        master['Salesman P&L']['Unnamed: 9'][10] += b
        
        master['Salesman P&L']['Unnamed: 12'][14 + i] = x + a
        master['Salesman P&L']['Unnamed: 12'][10] += x + a
        master['Salesman P&L']['Unnamed: 13'][14 + i] = y + b
        master['Salesman P&L']['Unnamed: 13'][10] += y + b
        
        z = sumCommission(c1, c2, c3, c4, c5, month, c, c1c, c2c, c3c, c4c, c5c)
        master['Salesman P&L']['Unnamed: 13'][2] += z
    
    master['Salesman P&L']['Unnamed: 4'][11] = master['Salesman P&L']['Unnamed: 4'][10]
    master['Salesman P&L']['Unnamed: 5'][11] = master['Salesman P&L']['Unnamed: 5'][10]
    master['Salesman P&L']['Unnamed: 8'][11] = master['Salesman P&L']['Unnamed: 8'][10]
    master['Salesman P&L']['Unnamed: 9'][11] = master['Salesman P&L']['Unnamed: 9'][10]
    master['Salesman P&L']['Unnamed: 12'][11] = master['Salesman P&L']['Unnamed: 6'][10]
    master['Salesman P&L']['Unnamed: 13'][11] = master['Salesman P&L']['Unnamed: 13'][10]
    
    return master


def sumNewTrucks(c1, c2, c3, c4, c5, month, c, c1c, c2c, c3c, c4c, c5c):
    x = 0
    y = 0
    
    if c == 0 or c == 1:
        if c1c == 1:
            x = c1[month]['Unnamed: 4'][25]
            y = c1[month]['Unnamed: 5'][25]
    if c == 0 or c == 2:
        if c2c == 1:
            x += c2[month]['Unnamed: 4'][25]
            y += c2[month]['Unnamed: 5'][25]
    if c == 0 or c == 3:
        if c3c == 1:
            x += c3[month]['Unnamed: 4'][25]
            y += c3[month]['Unnamed: 5'][25]
    if c == 0 or c == 4:
        if c4c == 1:
            x += c4[month]['Unnamed: 4'][25]
            y += c4[month]['Unnamed: 5'][25]
    if c == 0 or c == 5:
        if c5c == 1:
            x += c5[month]['Unnamed: 4'][25]
            y += c5[month]['Unnamed: 5'][25]
    
    return x, y
    
    
def sumOldTrucks(c1, c2, c3, c4, c5, month, c, c1c, c2c, c3c, c4c, c5c):
    x = 0
    y = 0
    
    if c == 0 or c == 1:
        if c1c == 1:
            x = c1[month]['Unnamed: 8'][25]
            y = c1[month]['Unnamed: 9'][25]
    if c == 0 or c == 2:
        if c2c == 1:
            x += c2[month]['Unnamed: 8'][25]
            y += c2[month]['Unnamed: 9'][25]
    if c == 0 or c == 3:
        if c3c == 1:
            x += c3[month]['Unnamed: 8'][25]
            y += c3[month]['Unnamed: 9'][25]
    if c == 0 or c == 4:
        if c4c == 1:
            x += c4[month]['Unnamed: 8'][25]
            y += c4[month]['Unnamed: 9'][25]
    if c == 0 or c == 5:
        if c5c == 1:
            x += c5[month]['Unnamed: 8'][25]
            y += c5[month]['Unnamed: 9'][25]
        
    return x, y


def sumCommission(c1, c2, c3, c4, c5, month, c, c1c, c2c, c3c, c4c, c5c):
    x = 0
    if c == 0 or c == 1:
        if c1c == 1:
            x = c1[month]['Unnamed: 14'][25]
    if c == 0 or c == 2:
        if c2c == 1:
            x += c2[month]['Unnamed: 14'][25]
    if c == 0 or c == 3:
        if c3c == 1:
            x += c3[month]['Unnamed: 14'][25]
    if c == 0 or c == 4:
        if c4c == 1:
            x += c4[month]['Unnamed: 14'][25]
    if c == 0 or c == 5:
        if c5c == 1:
            x += c5[month]['Unnamed: 14'][25]

    
    return x


@st.cache
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

