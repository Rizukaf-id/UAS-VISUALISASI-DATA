import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Fungsi untuk visualisasi Comparison
def visualize_comparison(data):
    plt.figure(figsize=(10,6))
    sns.lineplot(data=data, x='CalendarYear', y='SalesAmount')
    plt.figure(figsize=(10, 5))
    sns.barplot(data=data, x='SalesAmount', y='EnglishProductSubcategoryName', palette='viridis')
    st.pyplot()

# Fungsi untuk visualisasi Relationship
def visualize_relationship(data):
    plt.figure(figsize=(10,6))
    sns.scatterplot(data=data, x='YearlyIncome', y='SalesAmount', palette='rocket')
    st.pyplot()

# Fungsi untuk visualisasi Composition
def visualize_composition(data):
    fig, ax = plt.subplots(1, 2, figsize=(15, 5))

    # Plot untuk kategori
    ax[0].pie(data['SalesAmount'], labels=data['EnglishProductCategoryName'], autopct='%1.1f%%', startangle=140)
    ax[0].set_title('Persentase Penjualan Berdasarkan Kategori Produk')

    # Plot untuk subkategori
    sns.barplot(data=data, y='EnglishProductSubcategoryName', x='SalesAmount', ax=ax[1])
    ax[1].set_title('Penjualan Berdasarkan Subkategori Produk')
    ax[1].tick_params(axis='x', rotation=90)  # Rotate x-axis labels for readability

    plt.tight_layout()
    st.pyplot()

# Fungsi untuk visualisasi Distribution
def visualize_distribution(data):
    plt.figure(figsize=(10,6))
    plt.figure(figsize=(10, 5))
    sns.histplot(data=data, x='MonthNumberOfYear', bins=12, kde=True, color='blue')
    st.pyplot()

# Fungsi untuk membaca data
def load_data():
    data = pd.read_csv('data/all_data.csv')  # Ganti dengan path file data Anda
    return data

# Main function
def main():
    st.title('Data Visualization Dashboard')

    data = load_data()

    option = st.sidebar.selectbox(
        'Pilih visualisasi',
        ('Comparison', 'Relationship', 'Composition', 'Distribution')
    )

    if option == 'Comparison':
        # Tampilkan visualisasi Comparison
        visualize_comparison(data)
    elif option == 'Relationship':
        # Tampilkan visualisasi Relationship
        visualize_relationship(data)
    elif option == 'Composition':
        # Tampilkan visualisasi Composition
        visualize_composition(data)
    elif option == 'Distribution':
        # Tampilkan visualisasi Distribution
        visualize_distribution(data)

if __name__ == "__main__":
    main()