import streamlit as st
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

# Read CSV files into dataframes
df = pd.read_csv('imdb_combined_data2.csv')
# df.astype("string")

# df.keys()

df['Rating'] = df['Rating'].astype("string")
# df['Rating']

df['Name'] = df['Name'].astype("string")
# df['Name']

df['Year'] = pd.to_numeric(df['Year'])
# df['Year']


# 1. COMPARISON CHART - BAR CHART
# Raw Data Preparation
# Take 3 columns from panda dataframe, sorted by Rating
st.write("1. COMPARISON CHART - BAR CHART")
df_sel = df[['Rating','Gross_US', 'Gross_World']].sort_values(by=['Rating'])

# Drop rows with all zeros
hsl = df_sel.loc[(df_sel[['Gross_US', 'Gross_World']] != 0).all(axis=1)]
# df_sel

# Prepare the chart data from panda dataframe for BAR CHART
# X axis = Rating
# Y1 axis= Gross US, Y2 axis = Gross World
chart_data = pd.DataFrame(
    {
        "Rating": hsl['Rating'], "Gross US": hsl['Gross_US'], "Gross World":hsl['Gross_World']}
)

# BAR CHART (call the bar_chart using the chart_data, while defining label)
st.bar_chart(
   chart_data, x="Rating", y=["Gross US", "Gross World"], color=["#FF0000", "#0000FF"]  # Optional
)

# 2. RELATIONSHIP CHART - SCATTER PLOT
# Raw Data Preparation
# Take 4 columns from panda dataframe, sorted by Rating
st.write("2. RELATIONSHIP CHART - SCATTER PLOT")
df_sel2 = df[['Gross_US','Gross_World','Durasi(Menit)','Budget','Rating']].sort_values(by=['Durasi(Menit)'])

# Drop rows with all zeros
hsl = df_sel2.loc[(df_sel2[['Gross_US', 'Gross_World']] != 0).all(axis=1)]
hsl
# df_sel

# Scale down the numbers in 3 columns, dividing it by 1 million
# df_sel2['Gross_US'] = df_sel2['Gross_US']/1000000
# df_sel2['Gross_World'] = df_sel2['Gross_World']/1000000
# df_sel2['Budget'] = df_sel2['Budget']/1000000

hsl['Gross_US'] = hsl['Gross_US']/1000000
hsl['Gross_World'] = hsl['Gross_World']/1000000
hsl['Budget'] = hsl['Budget']/1000000

# Prepare the data for plotting
chart_data2 = pd.DataFrame(hsl, columns=["Gross_US", "Gross_World", "Durasi(Menit)", "Budget", "Rating"])

# In this case, I wanted to know the relation between X = Durasi(Menit) and Y = (Budget and Gross Sales in US). Sementara Gross_World digunakan untuk ukuran lingkaran yang akan ditampilkan
st.scatter_chart(
    chart_data2, 
    x='Durasi(Menit)',
    y=['Budget','Gross_US'],
    size='Gross_World',
    color=['#FF0000', '#0000FF'],  # Optional
    # color = ['Rating']
)


# 3. COMPOSITION CHART - DONUT CHART
# Raw Data Preparation
# Take 4 columns from panda dataframe, sorted by Rating
st.write("3. COMPOSITION CHART - DONUT CHART")

df_sel3 = df[['Gross_US','Gross_World','Budget','Rating']].sort_values(by=['Rating'])

# Drop rows with all zeros
hsl = df_sel3.loc[(df_sel3[['Gross_US', 'Gross_World']] != 0).all(axis=1)]
# df_sel
hsl = hsl.groupby(['Rating']).sum()
hsl

 
label = df_sel3.Rating.unique()
# label
# Creating plot
fig = plt.figure(figsize=(10, 7))
explode = [0,0.1,0,0.1]
plt.pie(hsl['Gross_US'], labels = hsl.index, explode = explode, autopct='%1.1f%%',
        shadow=False, startangle=90)
plt.axis('equal')
 
# show plot
st.pyplot(fig)


# 4. DISTRIBUTION - LINE CHART


chart_data2
st.line_chart(
    chart_data2, 
    x='Durasi(Menit)',
    y=['Budget','Gross_US'],
    color=['#FF0000', '#0000FF'],  # Optional
    # color = ['Rating']
)



# labels = 'Frogs', 'Hogs', 'Dogs', 'Logs'
# sizes = [15, 30, 45, 10]
# explode = (0, 0.1, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

# fig1, ax1 = plt.subplots()
# ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
#         shadow=True, startangle=90)
# ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.


# plt.show()


# st.bar_chart(df_sel)
# df_sorted
# sorting