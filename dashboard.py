import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='dark')

# Title untuk Streamlit app
st.title('Proyek Akhir Dicoding')
st.header('Bike Sharing Dashboard')

# Membaca dataset day.csv dan hour.csv
day_df = pd.read_csv('day_clean.csv')
day_df['dteday'] = pd.to_datetime(day_df['dteday'])  # Correct conversion to datetime

hour_df = pd.read_csv('hour_clean.csv')
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])  # Correct conversion to datetime

# Filter numeric columns untuk correlation
numeric_columns_day = day_df.select_dtypes(include=['float64', 'int64'])
numeric_columns_hour = hour_df.select_dtypes(include=['float64', 'int64'])

# Korelasi antara variabel-variabel (Day)
correlation_matrix = numeric_columns_day.corr()
correlation_matrix_hour = numeric_columns_hour.corr()

# Korelasi antara suhu, kelembapan, dan jumlah penyewa
correlation_temp_hum_cnt = hour_df[['temp', 'hum', 'cnt']].corr()

# Visualisasi korelasi antara variabel-variabel
st.header('Korelasi Variabel Day dan Hour')

with st.expander("Penjelasan"):
    st.write(
        """Ini merupakan heatmap korelasi antara variabel-variabel (Day) dan (Hour).
        Dan bisa dilihat bahwa terdapat korelasi yang cukup tinggi antara variabel temp, hum, dan cnt.
        Tetapi kedua variabel tersebut tidak memiliki korelasi yang signifikan. 
        
        """
    )


fig, axes = plt.subplots(2, 1, figsize=(18, 18))

sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', ax=axes[0])
axes[0].set_title('Korelasi antara Variabel Day')

sns.heatmap(correlation_matrix_hour, annot=True, cmap='coolwarm', ax=axes[1])
axes[1].set_title('Korelasi antara Variabel Hour')

st.pyplot(fig)

# Visualisasi distribusi penyewa sepeda berdasarkan hari kerja
st.header('Distribusi Penyewa Sepeda Berdasarkan Hari Kerja')

with st.expander("Penjelasan"):
    st.write(
        """Dapat dilihat pada 2 grafik ini, bahwa tidak memiliki perbedaan yang signifikan 
        antara distribusi penyewa sepeda pada setiap hari dan juga jamnya. Dan juga memang banyak
        orang yang menyewa sepeda pada hari kerja dibandingkan pada hari libur. 
        Hal ini terbukti karena lebih banyak penyewa di hari kerja dibandingkan pada hari libur.
        
        """
    )

fig, axes = plt.subplots(1, 2, figsize=(12, 6))

workingday_counts_day = day_df.groupby(day_df['workingday'].replace([1,0],['Yes','No']))['cnt'].sum()
workingday_counts_hour = hour_df.groupby(hour_df['workingday'].replace([1,0],['Yes','No']))['cnt'].sum()

sns.barplot(x=workingday_counts_day.index, y=workingday_counts_day.values, ax=axes[0])
axes[0].set_title('Distribusi Penyewa (Hari Kerja)')

sns.barplot(x=workingday_counts_hour.index, y=workingday_counts_hour.values, ax=axes[1])
axes[1].set_title('Distribusi Penyewa (Jam Kerja)')

st.pyplot(fig)

# Visualisasi tren penyewaan sepeda berdasarkan bulan
st.header('Tren Penyewaan Sepeda Berdasarkan Bulan')
with st.expander("Penjelasan"):
    st.write(
        """Dari grafik garis ini bisa disimpulkan, bahwa terdapat peningkatan 
        penyewaan sepeda di bulan tertentu, yang dimana bulan-bulan itu bisa dinikmati 
        suasananya dengan bersepeda.
        
        """
    )

monthly_rentals_hour = hour_df.groupby(hour_df['dteday'].dt.month)['cnt'].sum()

plt.figure(figsize=(10, 6))
sns.lineplot(x=monthly_rentals_hour.index, y=monthly_rentals_hour.values)
plt.title('Tren Penyewaan Sepeda Berdasarkan Bulan')
st.pyplot(plt.gcf())

# Visualisasi korelasi antara suhu, kelembapan, dan jumlah penyewa
st.header('Korelasi Suhu, Kelembapan, dan Jumlah Penyewa')

plt.figure(figsize=(8, 6))
sns.heatmap(correlation_temp_hum_cnt, annot=True, cmap='coolwarm')
plt.title('Korelasi antara Suhu, Kelembapan, dan Jumlah Penyewa')
st.pyplot(plt.gcf())

# Visualisasi scatter plot antara suhu dan jumlah penyewa
st.header('Hubungan antara Suhu dan Jumlah Penyewa')
plt.figure(figsize=(8, 6))
sns.scatterplot(x='temp', y='cnt', data=day_df)
plt.title('Hubungan antara Suhu dan Jumlah Penyewa')
st.pyplot(plt.gcf())

# Visualisasi scatter plot antara kelembapan dan jumlah penyewa
st.header('Hubungan antara Kelembapan dan Jumlah Penyewa')
plt.figure(figsize=(8, 6))
sns.scatterplot(x='hum', y='cnt', data=day_df)
plt.title('Hubungan antara Kelembapan dan Jumlah Penyewa')
st.pyplot(plt.gcf()) 

st.header('PERTANYAAN 1')
st.subheader('Bagaimana pengaruh cuaca terhadap jumlah penyewa sepeda pada jam-jam sibuk?')

with st.expander("Penjelasan"):
    st.write(
        """Dari grafik ini bisa disimpulkan, banyak penyewa sepeda 
        menyewa pada cuaca tertentu, seperti cuaca cerah, dan mungkin mendung.
        Karena di cuaca tersebut masih mendukung untuk bersepeda. 
        
        """
    )

busy_hours_df = hour_df[(hour_df['hr'] >= 7) & (hour_df['hr'] <= 9) | (hour_df['hr'] >= 17) & (hour_df['hr'] <= 19)]
weather_rentals = busy_hours_df.groupby(busy_hours_df['weathersit'].replace([1,2,3,4],['Cerah','Mendung','Hujan Ringan','Hujan Lebat']))['cnt'].mean()

plt.figure(figsize=(8, 6))
sns.barplot(x=weather_rentals.index, y=weather_rentals.values)
plt.title('Pengaruh Cuaca terhadap Jumlah Penyewa pada Jam-Jam Sibuk')
st.pyplot(plt.gcf())


st.header('PERTANYAAN 2')
st.subheader('Bagaimana hubungan antara musim dan jumlah penyewa sepeda pada hari kerja?')

with st.expander("Penjelasan"):
    st.write(
        """Dari grafik ini bisa disimpulkan, banyak penyewa sepeda 
        di musim musim tertentu, seperti musim gugur, musim panas. 
        Hal itu terjadi karena dimusim tersebut suasananya sangat mendukung 
        untuk bersepeda.
        
        """
    )

workingday_df = day_df[day_df['workingday'] == 0]
season_rentals_workingday = workingday_df.groupby(workingday_df['season'].replace([1,2,3,4],['Musim Semi','Musim Panas','Musim gugur','Musim Dingin']))['cnt'].mean()

plt.figure(figsize=(8, 6))
sns.barplot(x=season_rentals_workingday.index, y=season_rentals_workingday.values)
plt.title('Hubungan Musim dan Jumlah Penyewa pada Hari Kerja')
st.pyplot(plt.gcf())
