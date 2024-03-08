import seaborn as sb
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# Load data
jam_df = pd.read_csv("https://raw.githubusercontent.com/NazwaChantika/dashboard-dicoding-streamlit/main/Dashboard/jam.csv")
hari_df = pd.read_csv("https://raw.githubusercontent.com/NazwaChantika/dashboard-dicoding-streamlit/main/Dashboard/hari.csv")

# Function to plot bike rental count by weather situation
def plot_bike_rental_by_weather(df, title):
    musim_df = df.groupby(by="weathersit").cnt.nunique().reset_index()
    musim_df.rename(columns={"cnt": "count_sewa"}, inplace=True)

    colors = ["#FFA500", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
    fig, ax = plt.subplots(figsize=(10, 5))
    sb.barplot(
        y="count_sewa",
        x="weathersit",
        hue="weathersit",
        data=musim_df.sort_values(by="count_sewa", ascending=False),
        palette=colors,
        ax=ax,
        legend = False
    )
    ax.set_title(title, loc="center", fontsize=15)
    ax.set_xlabel("Musim")
    ax.set_ylabel("Banyak Sepeda disewa")
    st.pyplot(fig)

# Function to display statistics of bike usage by weekday and holiday
def display_bike_usage_statistics(df, title):
    statistik_penggunaan = df.groupby(['weekday', 'holiday']).agg({
        "registered": ["sum", "max", "min"],
        "casual": ["sum", "max", "min"]
    }).reset_index()

    st.write(title)
    st.write(statistik_penggunaan)

    # Visualisasi untuk statistik penggunaan registered
    fig_registered, axes_registered = plt.subplots(nrows=1, ncols=3, figsize=(15, 5))

    for i, (stat, color) in enumerate(zip(["sum", "max", "min"], ['b', 'g', 'r'])):
        ax = axes_registered[i]
        ax.bar(statistik_penggunaan.index, statistik_penggunaan["registered"][stat], color=color)
        ax.set_xticks(statistik_penggunaan.index)
        ax.set_xticklabels(statistik_penggunaan['weekday'])
        ax.set_title(f"Registered {stat.capitalize()}")

    st.pyplot(fig_registered)

    # Visualisasi untuk statistik penggunaan casual
    fig_casual, axes_casual = plt.subplots(nrows=1, ncols=3, figsize=(15, 5))

    for i, (stat, color) in enumerate(zip(["sum", "max", "min"], ['b', 'g', 'r'])):
        ax = axes_casual[i]
        ax.bar(statistik_penggunaan.index, statistik_penggunaan["casual"][stat], color=color)
        ax.set_xticks(statistik_penggunaan.index)
        ax.set_xticklabels(statistik_penggunaan['weekday'])
        ax.set_title(f"Casual {stat.capitalize()}")

    st.pyplot(fig_casual)

# Main part of the Streamlit app
st.title("Bike Rental Dashboard")
st.header("Banyaknya Jumlah Sepeda yang disewa pada setiap Musim")
st.subheader("Jam")
plot_bike_rental_by_weather(jam_df, "Jumlah Sepeda yang Disewa Berdasarkan Musim (Jam)")
st.subheader("Hari")
plot_bike_rental_by_weather(hari_df, "Jumlah Sepeda yang Disewa Berdasarkan Musim (Hari)")

st.header("Statistik Penggunaan Sepeda")
st.subheader("Statistik Penggunaan Sepeda di Weekday dan Holiday (Jam)")
display_bike_usage_statistics(jam_df, "Statistik Penggunaan Sepeda di Weekday dan Holiday (Jam)")
st.subheader("Statistik Penggunaan Sepeda di Weekday dan Holiday(Hari)")
display_bike_usage_statistics(hari_df, "Statistik Penggunaan Sepeda di Weekday dan Holiday(Hari)")


