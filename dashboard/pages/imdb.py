import streamlit as st
import pandas as pd
import plotly.express as px

# st.set_page_config(initial_sidebar_state="collapsed", page_title="052-Rizka F")

data = pd.read_csv('./data/imdb_combined.csv', sep=';', encoding='ISO-8859-1')
data = data.dropna()

def filter_data():
    st.header('Filter Data')
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        min_year = st.selectbox('Min Year', options=[None] + list(data['Year'].sort_values(ascending=True).unique()), index=0)
    with col2:
        max_year = st.selectbox('Max Year', options=[None] + list(data['Year'].sort_values(ascending=False).unique()), index=0)
    with col3:
        rating_data = st.selectbox('Rating', options=[None] + list(data['Rating'].unique()), index=0)
    with col4:
        color_data = st.selectbox('Color', options=[None] + list(data['Color'].unique()), index=0)

    global filtered_data
    filtered_data = data.copy()
    if min_year is not None:
        filtered_data = filtered_data[filtered_data['Year'] >= min_year]
    if max_year is not None:
        filtered_data = filtered_data[filtered_data['Year'] <= max_year]
    if rating_data is not None:
        filtered_data = filtered_data[filtered_data['Rating'] == rating_data]
    if color_data is not None:
        filtered_data = filtered_data[filtered_data['Color'] == color_data]
    st.divider()
    return filtered_data

def comparison():
    st.header('Comparison')
    st.subheader('Perbandingan Budget dan Rating per Tahun')

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.write('Max Budget')
        st.write(filtered_data['Budget'].max())
    with col2:
        st.write('Min Budget')
        st.write(filtered_data['Budget'].min())
    with col3:
        st.write('Max Rating')
        st.write(filtered_data['Rating'].max())
    with col4:
        st.write('Min Rating')
        st.write(filtered_data['Rating'].min())

    tab1, tab2 = st.tabs(['Budget', 'Rating'])
    with tab1:
        budget = filtered_data.groupby('Year')['Budget'].sum().reset_index()
        fig = px.line(budget, x='Year', y='Budget', title='Budget per Year')
        st.plotly_chart(fig)
        with st.expander('Penjelasan'):
            st.write('Total budget film dalam daftar 250 film teratas menunjukkan tren meningkat dari tahun 1940 hingga 2020. Hal ini berarti film-film semakin mahal. Terdapat fluktuasi dari tahun ke tahun, dengan 2016 sebagai tahun termahal dan 1940 sebagai tahun termurah. Faktor-faktor yang mungkin menyebabkan fluktuasi ini termasuk inflasi, kondisi ekonomi, dan tren industri film. Tren ini memiliki dampak signifikan pada industri film dan dapat digunakan untuk membuat keputusan tentang produksi film.')
    with tab2:
        rating = filtered_data.groupby('Year')['Rating'].mean().reset_index()
        fig = px.line(rating, x='Year', y='Rating', title='Average Rating per Year')
        st.plotly_chart(fig)
        with st.expander('Penjelasan'):
            st.write('Rata-rata rating film pada TOP 250 menunjukkan grafik yang fluktuatif. Rating tertinggi terjadi pada tahun 1972. Hal ini menunjukkan bahwa kualitas film tidak selalu meningkat dari waktu ke waktu.')

def relationship():
    st.header('Relationship')
    st.subheader('Hubungan antara Rating, Durasi, Budget, dan Gross')

    tab1, tab2, tab3 = st.tabs(['Rating vs Duration', 'Rating vs Budget', 'Budget vs Gross'])
    with tab1:
        duration_rating = filtered_data[['Durasi(Menit)', 'Rating']]
        fig = px.scatter(duration_rating, x='Durasi(Menit)', y='Rating', title='Duration vs Rating')
        max_rating = duration_rating['Rating'].idxmax()
        min_rating = duration_rating['Rating'].idxmin()
        fig.add_annotation(x=duration_rating.loc[max_rating, 'Durasi(Menit)'], y=duration_rating.loc[max_rating, 'Rating'], text="Max")
        fig.add_annotation(x=duration_rating.loc[min_rating, 'Durasi(Menit)'], y=duration_rating.loc[min_rating, 'Rating'], text="Min")
        st.plotly_chart(fig)

        with st.expander('Penjelasan'):
            st.write('Durasi film berkorelasi positif dengan rating film. Hal ini menunjukkan bahwa film dengan durasi yang lebih lama cenderung memiliki rating yang lebih tinggi. Namun, terdapat beberapa film dengan durasi yang sangat pendek yang memiliki rating tinggi, dan sebaliknya. Faktor-faktor lain seperti plot, akting, dan pengarahan juga mempengaruhi rating film.')

    with tab2:
        rating_budget = filtered_data[['Rating', 'Budget']]
        fig = px.scatter(rating_budget, x='Budget', y='Rating', title='Rating vs Budget')
        max_budget = rating_budget['Budget'].idxmax()
        min_budget = rating_budget['Budget'].idxmin()
        fig.add_annotation(x=rating_budget.loc[max_budget, 'Budget'], y=rating_budget.loc[max_budget, 'Rating'], text="Max")
        fig.add_annotation(x=rating_budget.loc[min_budget, 'Budget'], y=rating_budget.loc[min_budget, 'Rating'], text="Min")
        st.plotly_chart(fig)

        with st.expander('Penjelasan'):
            st.write('Budget film tidak berkorelasi secara signifikan terhadap Rating. Terdapat film dengan budget tinggi namun memiliki rating yang rendah.')

    with tab3:
        budget_gross = filtered_data[['Budget', 'Gross_World']]
        fig = px.scatter(budget_gross, x='Budget', y='Gross_World', title='Budget vs Gross')
        max_gross = budget_gross['Gross_World'].idxmax()
        min_gross = budget_gross['Gross_World'].idxmin()
        fig.add_annotation(x=budget_gross.loc[max_gross, 'Budget'], y=budget_gross.loc[max_gross, 'Gross_World'], text="Max")
        fig.add_annotation(x=budget_gross.loc[min_gross, 'Budget'], y=budget_gross.loc[min_gross, 'Gross_World'], text="Min")
        st.plotly_chart(fig)

        with st.expander('Penjelasan'):
            st.write('Budget film tidak berkorelasi secara signifikan terhadap Gross World. Terdapat film dengan budget tinggi namun memiliki pendapatan yang rendah.')

def composition():
    st.header('Composition')
    st.subheader('Komposisi Data Rated dan Color')
    tab1, tab2, = st.tabs(['Rated', 'Color'])
    with tab1:
        rated = filtered_data.groupby('Rated').agg({
            'Rated': 'count'
        })
        rated = rated.rename(columns={'Rated': 'Total'}).reset_index()
        fig = px.pie(rated, values='Total', names='Rated', title='Rated Composition')
        st.plotly_chart(fig)

        st.bar_chart(rated.set_index('Rated'))

        with st.expander('Penjelasan'):
            st.write('Film-film dalam daftar 250 film teratas memiliki berbagai Rated. Rated 15 adalah yang paling banyak, diikuti oleh rating 18 dan PG. Rating lainnya seperti 12A, U, dan yang lainnya memiliki jumlah yang lebih sedikit.')

    with tab2:
        color = filtered_data.groupby('Color').agg({
            'Color': 'count'
        })
        color = color.rename(columns={'Color': 'Total'}).reset_index()
        fig = px.pie(color, values='Total', names='Color', title='Color Composition')
        st.plotly_chart(fig)

        with st.expander('Penjelasan'):
            st.write('Film-film dalam daftar 250 film teratas memiliki berbagai warna. Film yang diproduksi berwarna lebih banyak diminati dibandingkan yang lainnya.')

def distribution():
    st.header('Distribution')
    st.subheader('Persebaran data Budget per Tahun')
    trend_budget = filtered_data.groupby('Year').agg({
        'Budget': 'sum'
    })
    trend_budget = trend_budget[trend_budget['Budget'] != 0]
    trend_budget.reset_index(inplace=True)
    fig = px.histogram(trend_budget, x='Year', y='Budget', title='Budget Distribution')
    st.plotly_chart(fig)

    with st.expander('Penjelasan'):
        st.write('Distribusi budget film dalam daftar 250 film teratas menunjukkan bahwa sebagian besar film memiliki budget di bawah 4 miliar. Terdapat beberapa film dengan budget yang sangat tinggi, yang rilis antara tahun 2010 hingga 2020.')


def show_imdb():
    st.title('IMDB Data Visualization Dashboard')
    st.subheader('Konteks')
    st.write('IMDb, atau Internet Movie Database, adalah basis data online yang menyediakan informasi tentang film, acara televisi, aktor, sutradara, penulis skenario, dan lainnya yang berkaitan dengan industri hiburan.')
    st.divider()
    filter_data()
    comparison()
    relationship()
    composition()
    distribution()