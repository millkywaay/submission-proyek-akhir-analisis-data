import streamlit as st
import pandas as pd
import plotly.express as px
from babel.numbers import format_currency

day_df = pd.read_csv("https://raw.githubusercontent.com/millkywaay/Dataset-Proyek-Analisi-Data/refs/heads/main/day.csv")
day_df.rename(columns={"dteday": "date", "cnt": "total_rentals"}, inplace=True)
day_df["date"] = pd.to_datetime(day_df["date"])

hour_df = pd.read_csv("https://raw.githubusercontent.com/millkywaay/Dataset-Proyek-Analisi-Data/refs/heads/main/hour.csv")
hour_df.rename(columns={"dteday": "date", "cnt": "total_rentals"}, inplace=True)
hour_df["date"] = pd.to_datetime(hour_df["date"])

workingday_map = {0: "Hari Libur", 1: "Hari Kerja"}
day_df["workingday"] = day_df["workingday"].map(workingday_map)
def create_daily_rentals_df(df):
    daily_rentals_df = df.resample(rule='D', on='date').agg({
        "total_rentals": "sum"
    })
    daily_rentals_df = daily_rentals_df.reset_index()
    return daily_rentals_df

def create_by_season_df(df):
    season_map = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
    df["season"] = df["season"].map(season_map)
    by_season_df = df.groupby("season")["total_rentals"].sum().reset_index()
    return by_season_df

def create_by_weekday_df(df):
    day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    df["weekday"] = pd.to_datetime(df["date"]).dt.day_name()
    df["weekday"] = pd.Categorical(df["weekday"], categories=day_order, ordered=True)
    by_weekday_df = df.groupby("weekday")["total_rentals"].sum().reset_index()
    return by_weekday_df

def create_by_workingday_df(df):
    by_workingday_df = df.groupby("workingday")["total_rentals"].sum().reset_index()
    return by_workingday_df

def create_peak_hour_df(df):
    peak_hour_df = df.groupby("hr")["total_rentals"].sum().reset_index()
    return peak_hour_df

st.sidebar.image("https://cdn.dribbble.com/userupload/24267094/file/original-26f849135f2b9a640e09626ea596e474.jpg?resize=752x&vertical=center", use_container_width=True)
st.sidebar.header("Filter Data")
start_date, end_date = st.sidebar.date_input(
    "Pilih Rentang Waktu", [day_df["date"].min(), day_df["date"].max()],
    min_value=day_df["date"].min(),
    max_value=day_df["date"].max()
)

day_df = day_df[(day_df["date"] >= pd.to_datetime(start_date)) & (day_df["date"] <= pd.to_datetime(end_date))]
hour_df = hour_df[(hour_df["date"] >= pd.to_datetime(start_date)) & (hour_df["date"] <= pd.to_datetime(end_date))]

daily_rentals_df = create_daily_rentals_df(day_df)
by_season_df = create_by_season_df(day_df)
by_weekday_df = create_by_weekday_df(day_df)
by_workingday_df = create_by_workingday_df(day_df)
peak_hour_df = create_peak_hour_df(hour_df)

st.title("🚴 Bike Sharing Dashboard")
st.markdown("Menampilkan analisis penyewaan sepeda berdasarkan dataset historis.")

# KPI Metrics
col1, col2 = st.columns(2)
col1.metric("Total Penyewaan", value=f"{day_df['total_rentals'].sum():,}")
col2.metric("Rata-rata Harian", value=f"{day_df['total_rentals'].mean():,.2f}")

# Tren Penyewaan Harian
st.subheader("Tren Penyewaan Sepeda Harian")
fig_trend = px.line(daily_rentals_df, x="date", y="total_rentals",
                    labels={"total_rentals": "Jumlah Penyewaan", "date": "Tanggal"}, markers=True,
                    color_discrete_sequence=["#2E86C1"])
st.plotly_chart(fig_trend)

# Peak Hour Penyewaan
st.subheader("Peak Hour Penyewaan Sepeda")
fig_peak_hour = px.line(peak_hour_df, x="hr", y="total_rentals",
                        labels={"total_rentals": "Jumlah Penyewaan", "hr": "Jam"}, markers=True,
                        color_discrete_sequence=["#E74C3C"])
st.plotly_chart(fig_peak_hour)

# Penyewaan Berdasarkan Musim
st.subheader("Penyewaan Sepeda Berdasarkan Musim")
fig_season = px.bar(by_season_df, x="season", y="total_rentals", color="season",
                    labels={"total_rentals": "Jumlah Penyewaan", "season": "Musim"},
                    color_discrete_sequence=["#16A085", "#2E86C1", "#8E44AD", "#D35400"])
st.plotly_chart(fig_season)

# Penyewaan Berdasarkan Hari dalam Seminggu
st.subheader("Penyewaan Sepeda Berdasarkan Hari")
fig_weekday = px.bar(by_weekday_df, x="weekday", y="total_rentals", color="weekday",
                     labels={"total_rentals": "Jumlah Penyewaan", "weekday": "Hari"},
                     color_discrete_sequence=["#16A085", "#2E86C1", "#8E44AD", "#D35400", "#E74C3C", "#F1C40F", "#7F8C8D"])
st.plotly_chart(fig_weekday)

# Penyewaan Berdasarkan Hari Kerja
st.subheader("Penyewaan Sepeda pada Hari Kerja")
fig_workingday = px.bar(by_workingday_df, x="workingday", y="total_rentals", color="workingday",
                        labels={"total_rentals": "Jumlah Penyewaan", "workingday": "Kategori Hari"},
                        color_discrete_sequence=["#16A085", "#D35400"])
st.plotly_chart(fig_workingday)

st.caption("© 2025 Khoirunnisa - Bike Sharing Analytics Dashboard")
