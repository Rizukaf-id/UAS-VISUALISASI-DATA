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
    # engine = create_engine("mysql+mysqlconnector://root:@localhost/adventureworks_dw")
    return engine

def load_data():
    global engine
    if engine is None:
        engine = open_connection()
    global fact_finance_df
    fact_finance_df = pd.read_sql("SELECT * FROM factfinance", engine)
    # print(fact_finance_df.head()) 
    global fact_internet_sales
    fact_internet_sales = pd.read_sql("SELECT * FROM factinternetsales", engine)
    # print(fact_internet_sales.head())
    global dimention_time_df 
    dimention_time_df = pd.read_sql("SELECT * FROM dimtime", engine)
    # print(dimention_time_df.head())
    global dimention_reseller_df 
    dimention_reseller_df = pd.read_sql("SELECT * FROM dimreseller", engine)
    # print(dimention_reseller_df.head())
    global dimention_product_df 
    dimention_product_df = pd.read_sql("SELECT * FROM dimproduct", engine)
    # print(dimention_product_df.head())
    global dimention_product_category_df 
    dimention_product_category_df = pd.read_sql("SELECT * FROM dimproductcategory", engine)
    # print(dimention_product_category_df.head())
    global dimention_product_subcategory_df 
    dimention_product_subcategory_df = pd.read_sql("SELECT * FROM dimproductsubcategory", engine)
    # print(dimention_product_subcategory_df.head())
    global dimention_customer_df 
    dimention_customer_df = pd.read_sql("SELECT * FROM dimcustomer", engine)
    # print(dimention_customer_df.head())
    return fact_finance_df, fact_internet_sales, dimention_time_df, dimention_reseller_df, dimention_product_df, dimention_product_category_df, dimention_product_subcategory_df, dimention_customer_df

def comparison():
    st.header('Comparison')
    st.subheader('Perbandingan Penjualan Sepanjang Tahun')
    tren_penjualan = fact_internet_sales.merge(dimention_time_df, left_on='OrderDateKey', right_on='TimeKey')
    tren_penjualan = tren_penjualan.groupby('CalendarYear').agg({'SalesAmount': 'sum'}).reset_index()
    top_product = fact_internet_sales.merge(dimention_product_df, left_on='ProductKey', right_on='ProductKey')
    top_subcategory = top_product.merge(dimention_product_subcategory_df, left_on='ProductSubcategoryKey', right_on='ProductSubcategoryKey')
    top_subcategory = top_subcategory.groupby('EnglishProductSubcategoryName').agg({'SalesAmount': 'sum'}).reset_index()
    top_subcategory = top_subcategory.sort_values('SalesAmount', ascending=False)
    top_subcategory['EnglishProductSubcategoryName'] = np.where(top_subcategory['SalesAmount'] < 300000, 'others', top_subcategory['EnglishProductSubcategoryName'])
    top_subcategory = top_subcategory.groupby('EnglishProductSubcategoryName').agg({'SalesAmount': 'sum'}).reset_index()
    top_subcategory = top_subcategory.sort_values('SalesAmount', ascending=False)


    col1, col2, col3 = st.columns(3)
    with col1:
        total_sold = tren_penjualan['SalesAmount'].sum()
        st.metric(label='Total Penjualan', value=total_sold)
    with col2:
        avg_sold = tren_penjualan['SalesAmount'].mean()
        st.metric(label='Rata-rata Penjualan', value=avg_sold)
    with col3:
        total_product = top_product['ProductKey'].count()
        st.metric(label='Total Produk Terjual', value=total_product)
    

    fig, ax = plt.subplots(figsize=(16, 8))
    ax.plot(tren_penjualan['CalendarYear'], tren_penjualan['SalesAmount'], marker='o')
    plt.title('Tren Penjualan Adventure Works', fontsize=32)
    plt.xlabel('Tahun', fontsize=16)
    plt.ylabel('Total Penjualan', fontsize=16)
    st.pyplot(fig)

    fig, ax = plt.subplots(figsize=(16, 8))
    ax.bar(top_subcategory['EnglishProductSubcategoryName'], top_subcategory['SalesAmount'])
    plt.title('Penjualan per Sub Kategori Produk', fontsize=32)
    plt.xlabel('Sub Kategori Produk', fontsize=16)
    plt.ylabel('Total Penjualan', fontsize=16)
    plt.xticks(rotation=45)
    st.pyplot(fig)

def relationship():
    st.header('Relationship')
    st.subheader('Hubungan antara Pendapatan Tahunan dengan Total Pembelian')
    customer_buy = fact_internet_sales.merge(dimention_customer_df, left_on='CustomerKey', right_on='CustomerKey')
    customer_buy = customer_buy.groupby('FirstName').agg({
        'SalesAmount': 'sum',
        'YearlyIncome': 'mean',
        }).reset_index()
    
    col1, col2 = st.columns(2)
    with col1:
        top_customer = customer_buy.sort_values('SalesAmount', ascending=False).iloc[0]
        # top_customer = top_customer['YearlyIncome']
        st.metric(label='Gaji Pelanggan dengan Pembelian Terbanyak', value=round(top_customer['YearlyIncome']))
    with col2:
        bottom_customer = customer_buy.sort_values('SalesAmount', ascending=True).iloc[0]
        # bottom_customer = bottom_customer['YearlyIncome']
        st.metric(label='Gaji Pelanggan dengan Pembelian Paling Sedikit', value=bottom_customer['YearlyIncome'])

    fig, ax = plt.subplots(figsize=(16, 8))
    ax.scatter(customer_buy['YearlyIncome'], customer_buy['SalesAmount'])

    plt.scatter(top_customer['YearlyIncome'], top_customer['SalesAmount'], color='red', s=100, label='Max Income')
    plt.scatter(bottom_customer['YearlyIncome'], bottom_customer['SalesAmount'], color='black', s=100, label='Min Income')
    
    plt.title('Hubungan antara Pendapatan Tahunan dengan Total Pembelian', fontsize=32)
    plt.xlabel('Pendapatan Tahunan', fontsize=16)
    plt.ylabel('Total Pembelian', fontsize=16)
    st.pyplot(fig)

def composition():
    st.header('Composition')
    st.subheader('Komposisi Penjualan per Kategori Produk dan sub Kategori Produk')
    penjualan_product = fact_internet_sales.merge(dimention_product_df, left_on='ProductKey', right_on='ProductKey')
    penjualan_subkategori = penjualan_product.merge(dimention_product_subcategory_df, left_on='ProductSubcategoryKey', right_on='ProductSubcategoryKey')
    penjualan_kategori = penjualan_subkategori.merge(dimention_product_category_df, left_on='ProductCategoryKey', right_on='ProductCategoryKey')
    penjualan_kategori = penjualan_kategori.groupby('EnglishProductCategoryName').agg({'SalesAmount': 'sum'}).reset_index()
    penjualan_subkategori = penjualan_subkategori.groupby('EnglishProductSubcategoryName').agg({'SalesAmount': 'sum'}).reset_index()
    penjualan_subkategori['EnglishProductSubcategoryName'] = np.where(penjualan_subkategori['SalesAmount'] < 300000, 'others', penjualan_subkategori['EnglishProductSubcategoryName'])
    penjualan_subkategori = penjualan_subkategori.groupby('EnglishProductSubcategoryName').agg({'SalesAmount': 'sum'}).reset_index()
    penjualan_subkategori = penjualan_subkategori.sort_values('SalesAmount', ascending=False)
    
    col1, col2 = st.columns(2)
    with col1:
        top_category = penjualan_kategori.sort_values('SalesAmount', ascending=False)
        top_category = top_category['EnglishProductCategoryName'].iloc[0]
        st.metric(label='Kategori Terlaris', value=top_category)
    with col2:
        top_subcategory = penjualan_subkategori['EnglishProductSubcategoryName'].iloc[0]
        st.metric(label='Sub Kategori Terlaris', value=top_subcategory)
   
    fig, ax = plt.subplots(1, 2, figsize=(16, 8))
    ax[0].pie(penjualan_kategori['SalesAmount'], labels=penjualan_kategori['EnglishProductCategoryName'], autopct='%1.1f%%')
    ax[0].set_title('Komposisi Penjualan per Kategori Produk', fontsize=18)
    ax[1].pie(penjualan_subkategori['SalesAmount'], labels=penjualan_subkategori['EnglishProductSubcategoryName'], autopct='%1.1f%%')
    ax[1].set_title('Komposisi Penjualan per Sub Kategori Produk', fontsize=18)
    st.pyplot(fig)

def distribution():
    st.header('Distribution')
    st.subheader('Distribusi Penjualan per Bulan')
    tren_penjualan = fact_internet_sales.merge(dimention_time_df, left_on='OrderDateKey', right_on='TimeKey')
    
    fig, ax = plt.subplots(figsize=(16, 8))
    sns.histplot(tren_penjualan['MonthNumberOfYear'], bins=12, kde=True, ax=ax)
    plt.title('Distribusi Penjualan per Bulan', fontsize=32)
    plt.xlabel('Bulan', fontsize=16)
    plt.ylabel('Total Penjualan', fontsize=16)
    st.pyplot(fig)
    
def show_aw():
    st.title('Adventure Works Data Visualization Dashboard')
    st.subheader('Konteks')
    st.write('Adventure Works adalah perusahaan manufaktur yang berlokasi di daerah Pacific Northwest di Amerika Serikat. Perusahaan ini berfokus pada pembuatan dan penjualan sepeda, serta berbagai komponen dan aksesori terkait sepeda.')
    st.divider()
    load_data()
    comparison()
    relationship()
    composition()
    distribution()