import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import streamlit as st

st.set_page_config(
    page_title="Bike Sharing Analysis Dashboard",
    page_icon="🚲",
    layout="wide",
)

# Load data
DAY_PATH = "data/bike-sharing-dataset/day.csv"
HOUR_PATH = "data/bike-sharing-dataset/hour.csv"
MAIN_DATA_PATH = "dashboard/main_data.csv"


@st.cache_data
def load_data():
  hour_df = pd.read_csv(HOUR_PATH)
  hour_df["dteday"] = pd.to_datetime(hour_df["dteday"])

  season_map = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
  yr_map = {0: 2011, 1: 2012}
  mnth_map = {
      1: "Jan",
      2: "Feb",
      3: "Mar",
      4: "Apr",
      5: "May",
      6: "Jun",
      7: "Jul",
      8: "Aug",
      9: "Sep",
      10: "Oct",
      11: "Nov",
      12: "Dec",
  }
  workingday_map = {0: "Weekend/Holiday", 1: "Working Day"}
  weathersit_map = {
      1: "Clear/Few Clouds",
      2: "Mist/Cloudy",
      3: "Light Rain/Snow",
      4: "Heavy Rain/Ice Pallets",
  }

  hour_df["season_label"] = hour_df["season"].map(season_map)
  hour_df["year_label"] = hour_df["yr"].map(yr_map)
  hour_df["month_label"] = hour_df["mnth"].map(mnth_map)
  hour_df["workingday_label"] = hour_df["workingday"].map(workingday_map)
  hour_df["weather_label"] = hour_df["weathersit"].map(weathersit_map)

  try:
    day_df = pd.read_csv(MAIN_DATA_PATH)
    day_df["dteday"] = pd.to_datetime(day_df["dteday"])
  except FileNotFoundError:
    day_df = pd.read_csv(DAY_PATH)
    day_df["dteday"] = pd.to_datetime(day_df["dteday"])
    day_df["season_label"] = day_df["season"].map(season_map)
    day_df["year_label"] = day_df["yr"].map(yr_map)
    day_df["month_label"] = day_df["mnth"].map(mnth_map)
    day_df["workingday_label"] = day_df["workingday"].map(workingday_map)
    day_df["weather_label"] = day_df["weathersit"].map(weathersit_map)

  return day_df, hour_df


day_df, hour_df = load_data()

# Sidebar - Filter Rentang Tanggal
st.sidebar.title("Filter Data")
min_date = day_df["dteday"].min().date()
max_date = day_df["dteday"].max().date()

date_range = st.sidebar.date_input(
    "Pilih Rentang Tanggal",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
)

if isinstance(date_range, tuple) and len(date_range) == 2:
  start_date, end_date = pd.to_datetime(date_range[0]), pd.to_datetime(
      date_range[1]
  )
else:
  start_date, end_date = pd.to_datetime(min_date), pd.to_datetime(max_date)

filtered_day = day_df[
    (day_df["dteday"] >= start_date) & (day_df["dteday"] <= end_date)
]
filtered_hour = hour_df[
    (hour_df["dteday"] >= start_date) & (hour_df["dteday"] <= end_date)
]

# Judul & KPI Utama
st.title("🚲 Bike Sharing Analysis Dashboard (2011–2012)")
st.markdown(
    "Dashboard interaktif untuk memantau pola penyewaan sepeda berdasarkan"
    " waktu, musim, cuaca, dan segmen pengguna."
)

col1, col2, col3 = st.columns(3)
col1.metric("Total Penyewaan", f"{filtered_day['cnt'].sum():,}")
col2.metric("Pengguna Registered", f"{filtered_day['registered'].sum():,}")
col3.metric("Pengguna Casual", f"{filtered_day['casual'].sum():,}")

st.divider()

# Visualisasi 1: Pola Penyewaan per Jam
st.subheader("1. Rata-rata Penyewaan per Jam: Working Day vs Weekend/Holiday")
hourly_avg = (
    filtered_hour.groupby(["workingday_label", "hr"], observed=False)["cnt"]
    .mean()
    .reset_index()
)

fig1, ax1 = plt.subplots(figsize=(11, 4))
sns.lineplot(
    data=hourly_avg,
    x="hr",
    y="cnt",
    hue="workingday_label",
    marker="o",
    ax=ax1,
)
ax1.set_xlabel("Jam (hr)")
ax1.set_ylabel("Rata-rata Penyewaan (cnt)")
ax1.set_xticks(range(0, 24))
ax1.set_ylim(bottom=0)
ax1.grid(axis="y", linestyle="--", alpha=0.4)
st.pyplot(fig1)

# Visualisasi 2: Musim & Cuaca
st.subheader("2. Rata-rata Penyewaan Harian per Musim & Kondisi Cuaca")
c_left, c_right = st.columns(2)

season_order = ["Spring", "Summer", "Fall", "Winter"]
season_avg = (
    filtered_day.groupby("season_label", observed=False)["cnt"]
    .mean()
    .reindex(season_order)
    .reset_index()
)
weather_avg = (
    filtered_day.groupby("weather_label", observed=False)["cnt"]
    .mean()
    .sort_values(ascending=False)
    .reset_index()
)

with c_left:
  fig2a, ax2a = plt.subplots(figsize=(6, 4))
  sns.barplot(
      data=season_avg,
      x="season_label",
      y="cnt",
      hue="season_label",
      palette="viridis",
      legend=False,
      ax=ax2a,
  )
  ax2a.set_title("Per Musim")
  ax2a.set_xlabel("Musim")
  ax2a.set_ylabel("Rata-rata cnt")
  ax2a.set_ylim(bottom=0)
  st.pyplot(fig2a)

with c_right:
  fig2b, ax2b = plt.subplots(figsize=(6, 4))
  sns.barplot(
      data=weather_avg,
      y="weather_label",
      x="cnt",
      hue="weather_label",
      palette="coolwarm",
      legend=False,
      ax=ax2b,
  )
  ax2b.set_title("Per Kondisi Cuaca")
  ax2b.set_xlabel("Rata-rata cnt")
  ax2b.set_ylabel("Kondisi Cuaca")
  ax2b.set_xlim(left=0)
  st.pyplot(fig2b)

# Visualisasi 3: Tren Bulanan
st.subheader("3. Tren Penyewaan Bulanan: Total vs Registered vs Casual")
monthly_df = (
    filtered_day.assign(month_start=filtered_day["dteday"].dt.to_period("M"))
    .groupby("month_start", observed=False)[["casual", "registered", "cnt"]]
    .sum()
    .reset_index()
)
monthly_df["month_start"] = monthly_df["month_start"].dt.to_timestamp()

fig3, ax3 = plt.subplots(figsize=(11, 4))
ax3.plot(
    monthly_df["month_start"],
    monthly_df["cnt"],
    marker="o",
    label="Total (cnt)",
)
ax3.plot(
    monthly_df["month_start"],
    monthly_df["registered"],
    marker="s",
    linestyle="--",
    label="Registered",
)
ax3.plot(
    monthly_df["month_start"],
    monthly_df["casual"],
    marker="^",
    linestyle=":",
    label="Casual",
)
ax3.set_xlabel("Bulan")
ax3.set_ylabel("Total Penyewaan")
ax3.set_ylim(bottom=0)
ax3.grid(True, linestyle="--", alpha=0.4)
ax3.legend()
st.pyplot(fig3)