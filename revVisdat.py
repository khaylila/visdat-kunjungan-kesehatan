import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import warnings

warnings.filterwarnings("ignore")

# Configure the page
st.set_page_config(page_title="Kunjungan Faskes Indonesia 📌", layout="wide")

# Set title and custom styles
# st.title(":bar_chart: ANALISIS DATA STATUS KESEHATAN DI INDONESIA 👩‍⚕️")
st.markdown(
    '<h1 style="text-align:center;"> ANALISIS KUNJUNGAN FASILITAS KESEHATAN DI INDONESIA 👩‍⚕️</h1>',
    unsafe_allow_html=True,
)

# Load data
df = pd.read_csv("C:/Users/izza/OneDrive/Documents/milea/visdat/train.csv")
# Convert Tanggal Datang to datetime format
df["Tanggal Datang"] = pd.to_datetime(df["Tanggal Datang"], format="%Y-%m-%d")
df["Nomor peserta"] = df["Nomor peserta"].astype(str)

# st.write(df[df["Kepemilikan Faskes"]=="Vertikal"])

monthStr = [
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "Mei",
    "Jun",
    "Jul",
    "Agu",
    "Sep",
    "Okt",
    "Nov",
    "Des",
]

monthYear = []
for tanggalDatang in df["Tanggal Datang"].sort_values(ascending=True):
    tempPeriod = monthStr[tanggalDatang.month - 1] + " " + str(tanggalDatang.year)
    if tempPeriod not in monthYear:
        monthYear.append(tempPeriod)

col_period_start, col_period_end = st.columns(2)
with col_period_start:
    periodStart = st.selectbox("Period Start", monthYear)
with col_period_end:
    periodEnd = st.selectbox("Period End", monthYear)

monthStart, yearStart = periodStart.split(" ")
monthEnd, yearEnd = periodEnd.split(" ")
monthStartIndex = monthStr.index(monthStart) + 1
monthEndIndex = monthStr.index(monthEnd) + 1
# Filter dataframe based on selections
filtered_df = df[
    (df["Tanggal Datang"].dt.year >= int(yearStart))
    & (df["Tanggal Datang"].dt.month >= monthStartIndex)
    & (df["Tanggal Datang"].dt.year <= int(yearEnd))
    & (df["Tanggal Datang"].dt.month <= monthEndIndex)
]


# st.write(filtered_df.tail(5))

# Create tabs for different charts
tab0, tab1= st.tabs(["Summary","Provinces"])

# CSS to center-align content within tabs
st.markdown(
    """
    <style>
    .css-1v3fvcr, .css-12w0qpk {
        justify-content: center;
    }
    .element-container {
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

with tab0:
    # Calculate total patients and total visits
    total_kunjungan = filtered_df["Nomor peserta"].count()
    total_pasien = filtered_df["Nomor peserta"].nunique()
    pasienSehat = filtered_df[filtered_df['Status Peserta']=="Sehat"]["Status Peserta"].value_counts()
    pasienSakit = filtered_df[filtered_df['Status Peserta']!="Sehat"]["Status Peserta"].value_counts()

    colTotalKunjungan, colTotalPasien, colPasienSehat, colPasienSakit = st.columns(4)
    colTotalKunjungan.metric(
        label="Total Kunjungan",
        value=total_kunjungan
    )

    colTotalPasien.metric(
        label="Total Pasien",
        value=total_pasien
    )

    colPasienSehat.metric(
        label="Kunjungan Sembuh",
        value=pasienSehat
    )

    colPasienSakit.metric(
        label="Kunjungan Sakit",
        value=pasienSakit
    )

    st.markdown(
        "<h3 style='font-align:center;'>Summary Data</h3>",
        unsafe_allow_html=True,
    )

    countTopFiceKunjunganFaskesByProvince = (
        filtered_df.groupby("Provinsi Faskes")["index"].count().nlargest(5).sort_values(ascending=True).reset_index()
    )
    chartTopProvinces = px.bar(countTopFiceKunjunganFaskesByProvince,
                               x="index",
                               y="Provinsi Faskes",
                               color='index', 
                               orientation='h',
        text_auto=True,
        labels={"index": "Banyaknya Pasien"},
        title='Top 5 Provinsi dengan Kunjungan Terbanyak'
    )
    st.plotly_chart(chartTopProvinces)


    trendByMonth = (
        filtered_df.groupby(pd.Grouper(key="Tanggal Datang", freq="M"))
        .count()
        .reset_index()
    )

    if not trendByMonth.empty:
        chartLineTrend = px.line(
            trendByMonth,
            x="Tanggal Datang",
            y="index",
            labels={
                "Tanggal Datang": "Bulan",
                "index": "Jumlah Pengunjung",
            },
            # color='index',
            title='Kunjugan Fasilitas Kesehatan Berdasarkan Waktu',
            markers=True,
        )
        st.plotly_chart(chartLineTrend)
    else:
        st.write("No data available for the selected period.")

    
    # top 3 fakses yang dipilih pengunjung
    countTopThreeKunjunganFaskesByJenisFaskes = (
        filtered_df.groupby("Jenis Faskes")["index"].count().reset_index()
    )
    chartTopJenisFaskes = px.bar(countTopThreeKunjunganFaskesByJenisFaskes, x="Jenis Faskes", y="index",
                                 color='index', 
                                 orientation='v',
        #  height=400,
        labels={"index": "Banyaknya Pasien"},
        text_auto=True,
        title='Top 3 Jenis Faskes dengan Kunjungan Terbanyak'
    )
    st.plotly_chart(chartTopJenisFaskes)

    # top 3 segmen pengunjung
    countTopThreeKunjunganFaskesBySegmenPeserta = (
        filtered_df.groupby("Segmen Peserta")["index"].count().reset_index()
    )
    chartTopSegmenPeserta = px.bar(countTopThreeKunjunganFaskesBySegmenPeserta, x="Segmen Peserta", y="index",
                                   color='index',
                                   orientation='v',
        #  height=400,
        labels={"index": "Banyaknya Pasien"},
        text_auto=True,
        title='Top 3 Segmen Peserta dengan Kunjungan Terbanyak'
    )
    st.plotly_chart(chartTopSegmenPeserta)

with tab1:
    selectProvince = st.selectbox("Pilih provinsi", df["Provinsi Faskes"].unique(),index=None)

    if selectProvince is not None:
        # Calculate total patients and total visits
        total_kunjungan = filtered_df[(filtered_df["Provinsi Faskes"]==selectProvince)]["Nomor peserta"].count()
        total_pasien = filtered_df[(filtered_df["Provinsi Faskes"]==selectProvince)]["Nomor peserta"].nunique()
        pasienSehat = filtered_df[(filtered_df["Provinsi Faskes"]==selectProvince)&(filtered_df['Status Peserta']=="Sehat")]["Status Peserta"].count()
        pasienSakit = filtered_df[(filtered_df["Provinsi Faskes"]==selectProvince)&(filtered_df['Status Peserta']!="Sehat")]["Status Peserta"].count()

        df_filter_provinceFaskes = (
            filtered_df[filtered_df["Provinsi Faskes"]==selectProvince].groupby("Kepemilikan Faskes")["Jenis Faskes"]
            .value_counts()
            .reset_index()
        )
    else:
        # Calculate total patients and total visits
        total_kunjungan = filtered_df["Nomor peserta"].count()
        total_pasien = filtered_df["Nomor peserta"].nunique()
        pasienSehat = filtered_df[filtered_df['Status Peserta']=="Sehat"]["Status Peserta"].value_counts()
        pasienSakit = filtered_df[filtered_df['Status Peserta']!="Sehat"]["Status Peserta"].value_counts()

        df_filter_provinceFaskes = (
            filtered_df.groupby("Kepemilikan Faskes")["Jenis Faskes"]
            .value_counts()
            .reset_index()
        )

    colTotalKunjungan, colTotalPasien, colPasienSehat, colPasienSakit = st.columns(4)
    colTotalKunjungan.metric(
        label="Total Kunjungan",
        value=total_kunjungan
    )

    colTotalPasien.metric(
        label="Total Pasien",
        value=total_pasien
    )

    colPasienSehat.metric(
        label="Kunjungan Sembuh",
        value=pasienSehat
    )

    colPasienSakit.metric(
        label="Kunjungan Sakit",
        value=pasienSakit
    )

    # st.write(df_filter_provinceFaskes.groupby("Kepemilikan Faskes").value_counts())

    figKepemilikanFaskesJenisFaskes = px.bar(
        df_filter_provinceFaskes,
        x="count",
        y="Kepemilikan Faskes",
        orientation="h",
        title="Kunjungan Berdasarkan Kepemilikan Faskes",
        labels={"count":"Banyaknya Kunjungan"},
        # text_auto=True,
        # color="count"
    )
    # fig.show()
    figKepemilikanFaskesJenisFaskes.update_layout(
        margin=dict(t=20, b=20, l=20, r=20), height=500
    )
    st.plotly_chart(figKepemilikanFaskesJenisFaskes)

    if selectProvince is not None:
        chartJenisFaskes = (
        filtered_df[filtered_df["Provinsi Faskes"]==selectProvince].groupby("Jenis Faskes")["index"].count().reset_index()
    )
    else:
        chartJenisFaskes = (
        filtered_df.groupby("Jenis Faskes")["index"].count().reset_index()
    )

    chartTopJenisFaskes = px.bar(chartJenisFaskes,
                                 x="Jenis Faskes",
                                 y="index",
                                 orientation='v',
                                 labels={"index": "Banyaknya Pasien"},
                                 title='Kunjungan Berasarkan Jenis Faskes',
                                 text_auto=True,
                                 color="index"
    )
    st.plotly_chart(chartTopJenisFaskes)



    if selectProvince is not None:
        chartJenisPoliProvinsi = (
        filtered_df[filtered_df["Provinsi Faskes"]==selectProvince].groupby("Jenis Poli")["index"].count().reset_index()
    )
    else:
        chartJenisPoliProvinsi = (
        filtered_df.groupby("Jenis Poli")["index"].count().reset_index()
    )

    jenisPoliProvinsi = px.bar(chartJenisPoliProvinsi,
                                 x="index",
                                 y="Jenis Poli",
                                 orientation='h',
                                 labels={"index": "Banyaknya Pasien"},
                                 title='Kunjungan Berdasarkan Jenis Poli',
                                 text_auto=True,
                                 color="index"
    )
    st.plotly_chart(jenisPoliProvinsi)

    if selectProvince is not None:
        chartJenisSegmenProvinsi = (
        filtered_df[filtered_df["Provinsi Faskes"]==selectProvince].groupby("Segmen Peserta")["index"].count().reset_index()
        )
    else:
        chartJenisSegmenProvinsi = (
        filtered_df.groupby("Segmen Peserta")["index"].count().reset_index()
        )
    jenisSegmenProvinsi = px.bar(chartJenisSegmenProvinsi,
                                 x="Segmen Peserta",
                                 y="index",
                                 orientation='v',
                                 labels={"index": "Banyaknya Pasien"},
                                 title='Kunjungan Berasarkan Segmen Peserta',
                                 text_auto=True,
                                 color="index"
    )
    st.plotly_chart(jenisSegmenProvinsi)

    if selectProvince is not None:
        countTopKunjunganFaskesByNumber = (
        filtered_df[filtered_df["Provinsi Faskes"]==selectProvince].groupby("Nomor peserta")["index"].count().reset_index()
        )
    else:
        countTopKunjunganFaskesByNumber = (
        filtered_df.groupby("Nomor peserta")["index"].count().reset_index()
        )

    chartHistogramKunjunganFaskesByNumber = px.histogram(countTopKunjunganFaskesByNumber,x="index",
                            labels={"index": "Frekuensi kunjungan pasien",
                                    "count":"Banyaknya pasien"},
                                    title="Frekuensi Kunjungan")
    st.plotly_chart(chartHistogramKunjunganFaskesByNumber)
    
    