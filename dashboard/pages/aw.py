import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import mysql.connector
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

engine = None

def open_connection():
    global engine
    load_dotenv()
    db_url = os.getenv('DATABASE_URL')
    print(f'DATABASE_URL: {db_url}')  # Debug line
    engine = create_engine(f'{db_url}')
    print(f'Engine: {engine}')
    return engine

def load_data():
    global engine
    if engine is None:
        engine = open_connection()
    global fact_finance_df
    fact_finance_df = pd.read_sql("SELECT * FROM factfinance", engine)
    print(fact_finance_df.head()) 
    global fact_internet_sales
    fact_internet_sales = pd.read_sql("SELECT * FROM factinternetsales", engine)
    print(fact_internet_sales.head())
    global dimention_time_df 
    dimention_time_df = pd.read_sql("SELECT * FROM dimtime", engine)
    print(dimention_time_df.head())
    global dimention_reseller_df 
    dimention_reseller_df = pd.read_sql("SELECT * FROM dimreseller", engine)
    print(dimention_reseller_df.head())
    global dimention_product_df 
    dimention_product_df = pd.read_sql("SELECT * FROM dimproduct", engine)
    print(dimention_product_df.head())
    global dimention_product_category_df 
    dimention_product_category_df = pd.read_sql("SELECT * FROM dimproductcategory", engine)
    print(dimention_product_category_df.head())
    global dimention_product_subcategory_df 
    dimention_product_subcategory_df = pd.read_sql("SELECT * FROM dimproductsubcategory", engine)
    print(dimention_product_subcategory_df.head())
    global dimention_customer_df 
    dimention_customer_df = pd.read_sql("SELECT * FROM dimcustomer", engine)
    print(dimention_customer_df.head())
    return fact_finance_df, fact_internet_sales, dimention_time_df, dimention_reseller_df, dimention_product_df, dimention_product_category_df, dimention_product_subcategory_df, dimention_customer_df

def comparison():
    st.header('Comparison')
    st.subheader('Perbandingan Penjualan Sepanjang Tahun')
    tren_penjualan = fact_internet_sales.merge(dimention_time_df, left_on='OrderDateKey', right_on='TimeKey')
    tren_penjualan = tren_penjualan.groupby('CalendarYear').agg({'SalesAmount': 'sum'}).reset_index()
    plt.figure(figsize=(10, 5))
    sns.lineplot(data=tren_penjualan, x='CalendarYear', y='SalesAmount')
    plt.title('Tren Penjualan Adventure Works')
    plt.xlabel('Tahun')
    plt.ylabel('Total Penjualan')
    st.pyplot()

def show_aw():
    st.title('Data Visualization Dashboard')
    st.write('This is the Adventure Works page.')
    load_data()
    comparison()
    

    

   
