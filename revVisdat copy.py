import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import json
import os
import warnings

warnings.filterwarnings("ignore")

# Configure the page
st.set_page_config(page_title="Info Sehat Indonesia 📌", layout="wide")

# Set title and custom styles
# st.title(":bar_chart: ANALYSIS DATA STATUS KESEHATAN DI INDONESIA 👩‍⚕️")
st.markdown(
    '<h1 style="text-align:center;"> ANALYSIS DATA STATUS KESEHATAN DI INDONESIA 👩‍⚕️</h1>',
    unsafe_allow_html=True,
)
    

# st.markdown(
#     "<style>div.block-container{padding-top:1rem; text-align: center; background-color: #ccffcc;}</style>",
#     unsafe_allow_html=True,
# )
# st.markdown(
#     "<style>section.main > div {background-color: #ccffcc;}</style>",
#     unsafe_allow_html=True,
# )

# Change directory to the path containing the CSV file
# os.chdir(r"D:\winphyton\WPy64-31180")

# Load data
df = pd.read_csv("C:/Users/izza/OneDrive/Documents/milea/visdat/train.csv")
# Convert Tanggal Datang to datetime format
df["Tanggal Datang"] = pd.to_datetime(df["Tanggal Datang"], format="%Y-%m-%d")
df["Nomor peserta"] = df["Nomor peserta"].astype(str)

# Muat file GeoJSON
geojson_path = "C:/Users/izza/OneDrive/Documents/milea/visdat/indonesia-prov.geojson"
with open(geojson_path) as f:
    geojson = json.load(f)

# Fungsi untuk memperbarui progress bar
# def update_progress(progress):
#     progress_bar.progress(progress)
    
    
    
# Fungsi untuk menghitung total 
def calculate_total_patients(df):
    return df['Nomor peserta'].count()

# Fungsi untuk menghitung total pasien
def calculate_total_patients(df):
    return df['Nomor peserta'].nunique()

# df.columns = [
#     "index",
#     "Nomor peserta",
#     "Nomor keluarga",
#     "Bobot",
#     "ID Kunjungan FKTP",
#     "Tanggal Datang",
#     "Tanggal Pulang",
#     "Provinsi Faskes",
#     "Kepemilikan Faskes",
#     "Jenis Faskes",
#     "Tipe Faskes",
#     "Tingkat Pelayanan Faskes",
#     "Jenis Poli",
#     "Segmen Peserta",
#     "Diagnosis",
#     "Provinsi Faskes Rujukan",
#     "Kepemilikan Faskes Rujukan",
#     "Jenis Faskes Rujukan",
#     "Tipe Faskes Rujukan",
#     "Jenis Poli Rujukan",
#     "Jenis Kunjungan Faskes",
#     "Status Peserta",
#     # "Keterangan",
# ]

# 1. Display total number of unique patients
# total_patients = df["Nomor peserta"].nunique()
# st.markdown(f"### Total Patients: {total_patients}")

# Sidebar filters
# st.sidebar.header("Filter Data")

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


# def getDate(month, year):
#     date = 30
#     if month in [1, 3, 5, 7, 8, 10, 12]:
#         date = 31
#     else:
#         if month in [4, 6, 9, 11]:
#             date = 30
#         else:
#             if year % 4 == 0:
#                 date = 29
#             else:
#                 date = 28
#     return date


monthYear = []
for tanggalDatang in df["Tanggal Datang"].sort_values(ascending=True):
    tempPeriod = monthStr[tanggalDatang.month - 1] + " " + str(tanggalDatang.year)
    if tempPeriod not in monthYear:
        monthYear.append(tempPeriod)

# Filter by year and month
# years = df["Tanggal Datang"].dt.year.unique()
# selected_year = st.sidebar.selectbox("Year", years, index=len(years) - 1)
# months = df[df["Tanggal Datang"].dt.year == selected_year][
#     "Tanggal Datang"
# ].dt.month.unique()
# Move period start and end filters to main page
col_period_start, col_period_end = st.columns(2)
with col_period_start:
    periodStart = st.selectbox("Period Start", monthYear)
with col_period_end:
    periodEnd = st.selectbox("Period End", monthYear)

monthStart, yearStart = periodStart.split(" ")
monthEnd, yearEnd = periodEnd.split(" ")
monthStartIndex = monthStr.index(monthStart) + 1
monthEndIndex = monthStr.index(monthEnd) + 1
# dateEnd = getDate(monthEndIndex, int(yearEnd))
# rangePeriod = [
#     pd.to_datetime(f"{yearStart}-{monthStartIndex:02d}-01"),
#     pd.to_datetime(f"{yearEnd}-{monthEndIndex:02d}-{dateEnd}"),
# ]



# # Filter by Jenis Poli
# jenis_poli = df["Jenis Poli"].unique()
# selected_jenis_poli = st.sidebar.multiselect("Jenis Poli", jenis_poli)

# # Filter by Tipe Faskes
# tipe_faskes = df["Tipe Faskes"].unique()
# selected_tipe_faskes = st.sidebar.multiselect("Tipe Faskes", tipe_faskes)

# # Filter by Provinsi Faskes
# provinsi_faskes = df["Provinsi Faskes"].unique()
# selected_provinsi_faskes = st.sidebar.multiselect("Provinsi Faskes", provinsi_faskes)

# # Filter by Kepemilikan Faskes
# kepemilikan_faskes = df["Kepemilikan Faskes"].unique()
# selected_kepemilikan_faskes = st.sidebar.multiselect(
#     "Kepemilikan Faskes", kepemilikan_faskes
# )

# Filter dataframe based on selections
filtered_df = df[
    (df["Tanggal Datang"].dt.year >= int(yearStart))
    & (df["Tanggal Datang"].dt.month >= monthStartIndex)
    & (df["Tanggal Datang"].dt.year <= int(yearEnd))
    & (df["Tanggal Datang"].dt.month <= monthEndIndex)
    # & (
    #     df["Jenis Poli"].isin(selected_jenis_poli)
    #     if selected_jenis_poli
    #     else df["Jenis Poli"].notna()
    # )
    # & (
    #     df["Tipe Faskes"].isin(selected_tipe_faskes)
    #     if selected_tipe_faskes
    #     else df["Tipe Faskes"].notna()
    # )
    # & (
    #     df["Provinsi Faskes"].isin(selected_provinsi_faskes)
    #     if selected_provinsi_faskes
    #     else df["Provinsi Faskes"].notna()
    # )
    # & (
    #     df["Kepemilikan Faskes"].isin(selected_kepemilikan_faskes)
    #     if selected_kepemilikan_faskes
    #     else df["Kepemilikan Faskes"].notna()
    # )
]


# total_patients = filtered_df["Nomor peserta"].nunique()
# total_patients = filtered_df["Nomor peserta"].count()
# st.markdown(f"### Total Pasien: {total_patients}")

# with colTotalKunjungan:
#     total_kunjungan = filtered_df["Nomor peserta"].count()
#     st.markdown(f"### Total Kunjungan: {total_kunjungan}")


# with colTotalPasien:
#     total_patients = filtered_df["Nomor peserta"].nunique()
#     st.markdown(f"### Total Pasien: {total_patients}")

# chartLineTrend = filtered_df.groupby(pd.Grouper(key="Tanggal Pulang", freq="1M"))
# ["Tanggal Pulang", freq="1M"].value_counts()
# df = px.data.gapminder().query("country=='Canada'")
# figTrendPengunjung = px.line(
#     df, x=chartLineTrend, y="index", title="Trend Kunjungan Faskes"
# )
# # figTrendPengunjung.show()
# figTrendPengunjung.update_layout(mrgin=dict(t=20, b=20, l=20, r=20), height=500)
# st.plotly_chart(figTrendPengunjung)

# st.write(trendByMonth)
# st.write(trendByMonth["Tanggal Datang"].dt.strftime("%b %Y"))
# trendByMonth["Tanggal Datang"] = trendByMonth["Tanggal Datang"].dt.strftime("%b %Y")

# Calculate total patients and total visits
total_kunjungan = filtered_df["Nomor peserta"].count()
total_pasien = filtered_df["Nomor peserta"].nunique()
pasienSehat = filtered_df[filtered_df['Status Peserta']=="Sehat"]["Status Peserta"].value_counts()
pasienSakit = filtered_df[filtered_df['Status Peserta']!="Sehat"]["Status Peserta"].value_counts()

# Define maximum values for progress bars
max_kunjungan = 1000  # Adjust this value as needed
max_pasien = 500  # Adjust this value as needed

# Normalize the progress values to be between 0.0 and 1.0
progress_kunjungan = min(total_kunjungan / max_kunjungan, 1.0)
progress_pasien = min(total_pasien / max_pasien, 1.0)

# Display total patients and total visits with progress bars
# colHead = st.columns(1)
# colHead.

colTotalKunjungan, colTotalPasien, colPasienSehat, colPasienSakit = st.columns(4)

colTotalKunjungan.metric(
    label="Total Kunjungan",
    value=total_kunjungan
)

# Progress bar for total kunjungan
# colTotalKunjungan.progress(progress_kunjungan)

colTotalPasien.metric(
    label="Total Pasien",
    value=total_pasien
)

# Progress bar for total pasien
# colTotalPasien.progress(progress_pasien)

colPasienSehat.metric(
    label="Kunjungan Sembuh",
    value=pasienSehat
)

colPasienSakit.metric(
    label="Kunjungan Sakit",
    value=pasienSakit
)

st.write(filtered_df.tail(5))

# Create tabs for different charts
tab0, tab1= st.tabs(["Summary","Provinces"])
# tab0, tab1, tab2, tab3, tab4, tab5, tab6, tab7= st.tabs(["Summary","Provinces", "Status Pasien", "Status Rujukan", "Jenis Faskes dan Segmen", "Jenis Poli", "Provinsi Faskes", "Kepemilikan Akses"])

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
                            #    color='index', 
                               orientation='h',
        #  height=400,
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
            title='Kunjugan Fasilitas Kesehatan Berdasarkan Waktu',
            markers=True,
        )
        st.plotly_chart(chartLineTrend)
    else:
        st.write("No data available for the selected period.")

    
    # top 3 fakses yang dipilih pengunjung
    countTopThreeKunjunganFaskesByJenisFaskes = (
        filtered_df.groupby("Jenis Faskes")["index"].count().nlargest(3).reset_index()
    )
    chartTopJenisFaskes = px.bar(countTopThreeKunjunganFaskesByJenisFaskes, x="Jenis Faskes", y="index",
                                #  color='index', 
                                 orientation='v',
        #  height=400,
        labels={"index": "Banyaknya Pasien"},
        title='Top 3 Jenis Faskes dengan Kunjungan Terbanyak'
    )
    st.plotly_chart(chartTopJenisFaskes)

    # top 3 segmen pengunjung
    countTopThreeKunjunganFaskesBySegmenPeserta = (
        filtered_df.groupby("Segmen Peserta")["index"].count().nlargest(3).reset_index()
    )
    chartTopSegmenPeserta = px.bar(countTopThreeKunjunganFaskesBySegmenPeserta, x="Segmen Peserta", y="index",
                                #    color='index',
                                   orientation='v',
        #  height=400,
        labels={"index": "Banyaknya Pasien"},
        title='Top 3 Segmen Peserta dengan Kunjungan Terbanyak'
    )
    st.plotly_chart(chartTopSegmenPeserta)

with tab1:
    selectProvince = st.selectbox("Pilih provinsi", df["Provinsi Faskes"].unique(),index=None)

    # filtered_df[filtered_df['Status Peserta']=="Sehat"]["Status Peserta"].value_counts()

    # st.subheader("Kepemilikan Faskes Berdasarkan Jenis Faskes")
    if selectProvince is not None:
        df_filter_provinceFaskes = (
            filtered_df[filtered_df["Provinsi Faskes"]==selectProvince].groupby("Kepemilikan Faskes")["Jenis Faskes"]
            .value_counts()
            .reset_index()
        )
    else:
        df_filter_provinceFaskes = (
            filtered_df.groupby("Kepemilikan Faskes")["Jenis Faskes"]
            .value_counts()
            .reset_index()
        )

    figKepemilikanFaskesJenisFaskes = px.bar(
        df_filter_provinceFaskes,
        x="count",
        y="Kepemilikan Faskes",
        orientation="h",
        title="Kunjungan Berdasarkan Kepemilikan Faskes",
        labels={"count":"Banyaknya Kunjungan"}
    )
    # fig.show()
    figKepemilikanFaskesJenisFaskes.update_layout(
        margin=dict(t=20, b=20, l=20, r=20), height=500
    )
    st.plotly_chart(figKepemilikanFaskesJenisFaskes)

    # selectKepemilikanFaskes = st.selectbox("Kepemilikan Faskes", df["Kepemilikan Faskes"].unique(), index=None)

    # Kunjungan Berasarkan Jenis Faskes
    # if selectKepemilikanFaskes is not None:
    #     chartJenisFaskes = (
    #     filtered_df[filtered_df["Provinsi Faskes"]==selectProvince].groupby("Jenis Faskes")["index"].count().reset_index()
    # )
    # else:
    # chartJenisFaskes = filtered_df[(
    #     filtered_df[filtered_df["Provinsi Faskes"]==selectProvince]
    #     if selectProvince
    #     else filtered_df["Provinsi Faskes"].notna()
    # )
    # & (
    #     filtered_df[filtered_df["Jenis Faskes"]==selectKepemilikanFaskes]
    #     if selectKepemilikanFaskes
    #     else filtered_df["Jenis Faskes"].notna()
    # )]

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
                                 title='Kunjungan Berasarkan Jenis Faskes'
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

    # Kunjungan Berasarkan Jenis Poli
    # chartJenisPoliProvinsi = (
    #     filtered_df[filtered_df["Provinsi Faskes"]==selectProvince].groupby("Jenis Poli")["index"].count().reset_index()
    # )
    jenisPoliProvinsi = px.bar(chartJenisPoliProvinsi,
                                 x="index",
                                 y="Jenis Poli",
                                 orientation='h',
                                 labels={"index": "Banyaknya Pasien"},
                                 title='Kunjungan Berdasarkan Jenis Poli'
    )
    st.plotly_chart(jenisPoliProvinsi)

    # Kunjungan Berasarkan Segmen peserta
    # chartJenisSegmenProvinsi = (
    #     filtered_df[filtered_df["Provinsi Faskes"]==selectProvince].groupby("Segmen Peserta")["index"].count().reset_index()
    # )
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
                                 title='Kunjungan Berasarkan Segmen Peserta'
    )
    st.plotly_chart(jenisSegmenProvinsi)


    
    # countTopKunjunganFaskesByNumber = (
    #     filtered_df[filtered_df["Provinsi Faskes"]==selectProvince].groupby("Nomor peserta")["index"]
    #     .count()
    #     .reset_index()
    # )

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


# with tab2:
#     st.subheader("Status Pasien")
#     status_counts = filtered_df["Status Peserta"].value_counts()
#     fig1 = px.pie(
#         status_counts,
#         values=status_counts.values,
#         names=status_counts.index,
#         title=None,
#     )
#     fig1.update_layout(
#         margin=dict(t=20, b=20, l=20, r=20), width=500, height=500
#     )
#     st.plotly_chart(fig1)

# with tab3:
#     st.subheader("Status Rujukan")
#     referral_counts = filtered_df["Jenis Faskes Rujukan"].value_counts()
#     fig2 = px.pie(
#         referral_counts,
#         values=referral_counts.values,
#         names=referral_counts.index,
#         title=None,
#     )
#     fig2.update_layout(margin=dict(t=20, b=20, l=20, r=20), width=500, height=500)
#     st.plotly_chart(fig2)


#     # col3 = st.columns(1)

#     # with col3:

# # col4 = st.columns(1)

# # with col4:
# # st.subheader("Jumlah Nomor Peserta berdasarkan Segmen Peserta dan Jenis Faskes")
# # num_patients_by_segment_faskes = (
# #     filtered_df.groupby(["Segmen Peserta", "Jenis Faskes"])["Nomor peserta"]
# #     .nunique()
# #     .reset_index()
# # )
# # fig4 = px.bar(
# #     num_patients_by_segment_faskes,
# #     x="Jenis Faskes",
# #     y="Nomor peserta",
# #     color="Segmen Peserta",
# #     title=None,
# #     template="plotly_dark",
# #     barmode="group",
# # )  # Atur barmode='group' untuk membuat clustered bar chart
# # fig4.update_layout(margin=dict(t=20, b=20, l=20, r=20), height=500)
# # st.plotly_chart(fig4)

# with tab4:
#     st.markdown(
#         "<h3>Jumlah Pasien berdasarkan Jenis Faskes dan Segmen</h3>",
#         unsafe_allow_html=True,
#     )
#     col1, col2 = st.columns(2)
#     with col1:
#         st.markdown(
#             "<h4>Pasien Berdasarkan Faskes</h4>",
#             unsafe_allow_html=True,
#         )
#         status_counts = filtered_df["Jenis Faskes"].value_counts()
#         fig5 = px.pie(
#             status_counts,
#             values=status_counts.values,
#             names=status_counts.index,
#             title=None,
#         )
#         fig5.update_layout(
#             margin=dict(t=20, b=20, l=20, r=20), width=500, height=500
#         )
#         st.plotly_chart(fig5)

#     with col2:
#         st.markdown(
#             "<h4>Pasien Berdasarkan Segmen</h4>",
#             unsafe_allow_html=True,
#         )
#         referral_counts = filtered_df["Segmen Peserta"].value_counts()
#         fig6 = px.pie(
#             referral_counts,
#             values=referral_counts.values,
#             names=referral_counts.index,
#             title=None,
#         )
#         fig6.update_layout(margin=dict(t=20, b=20, l=20, r=20), width=500, height=500)
#         st.plotly_chart(fig6)

# with tab5:
#     st.subheader("Jumlah Pasien Berdasarkan Jenis Poli")
#     count_pasien_by_jenis_poli = (
#         filtered_df.groupby("Jenis Poli")["index"].count().reset_index()
#     )
#     fig8 = px.bar(
#         count_pasien_by_jenis_poli,
#         x="Jenis Poli",
#         y="index",
#         color="index",
#         title=None,
#         template="plotly_dark",
#         labels={"index": "Banyaknya Pasien"},
#     )
#     fig8.update_layout(margin=dict(t=20, b=20, l=20, r=20), height=500)
#     st.plotly_chart(fig8)
   
# with tab6:
#     st.subheader("Jumlah Pasien Berdasarkan Provinsi Faskes")
#     count_diagnosis_by_provinsi = (
#     filtered_df.groupby("Provinsi Faskes")["index"].count().reset_index()
#     )
#     fig7 = px.bar(
#         count_diagnosis_by_provinsi,
#         x="Provinsi Faskes",
#         y="index",
#         color="index",
#         title=None,
#         template="plotly_dark",
#         labels={"index": "Banyaknya Pasien"},
#     )
#     fig7.update_layout(margin=dict(t=20, b=20, l=20, r=20), height=500)
#     st.plotly_chart(fig7)  
    
# with tab7:
#     st.subheader("Jumlah Pasien Berdasarkan Kepemilikan Faskes")
#     count_diagnosis_by_provinsi = (
#     filtered_df.groupby("Kepemilikan Faskes")["index"].count().reset_index()
#     )
#     fig9 = px.bar(
#         count_diagnosis_by_provinsi,
#         x="Kepemilikan Faskes",
#         y="index",
#         color="index",
#         title=None,
#         template="plotly_dark",
#         labels={"index": "Banyaknya Pasien"},
#         )
#     fig9.update_layout(margin=dict(t=20, b=20, l=20, r=20), height=500)
#     st.plotly_chart(fig9)

#     st.subheader("Jumlah Pasien Berdasarkan Tipe Faskes")
#     count_pasien_by_tipe_faskes = (
#         filtered_df.groupby("Tipe Faskes")["index"].count().reset_index()
#     )
#     fig3 = px.bar(
#         count_pasien_by_tipe_faskes,
#         x="Tipe Faskes",
#         y="index",
#         color="index",
#         title=None,
#         template="plotly_dark",
#         labels={"index": "Banyaknya Pasien"},
#     )
#     fig3.update_layout(margin=dict(t=20, b=20, l=20, r=20), height=500)
#     st.plotly_chart(fig3)
    
#     # st.subheader("Kepemilikan Faskes Berdasarkan Jenis Faskes")
#     long_df = (
#     filtered_df.groupby("Kepemilikan Faskes")["Jenis Faskes"]
#     .value_counts()
#     .reset_index()
# )

#     figKepemilikanFaskesJenisFaskes = px.bar(
#         long_df,
#         x="Kepemilikan Faskes",
#         y="count",
#         color="Jenis Faskes",
#         title="Kepemilikan Faskes Berdasarkan Jenis Faskes",
#         labels={"count":"Banyaknya Faskes"}
#     )
#     # fig.show()
#     figKepemilikanFaskesJenisFaskes.update_layout(
#         margin=dict(t=20, b=20, l=20, r=20), height=500
#     )
#     st.plotly_chart(figKepemilikanFaskesJenisFaskes)




# with tab8:
#     st.subheader("Peta Pasien per Provinsi")
#     # Buat peta choropleth
#     fig = px.choropleth(
#         provinsi_counts,
#         geojson=geojson,
#         locations="Provinsi Faskes",
#         featureidkey="properties.state",  # Sesuaikan dengan kunci dalam file GeoJSON Anda
#         color="Jumlah Pasien",
#         color_continuous_scale="Viridis",
#         title="Jumlah Pasien Berdasarkan Provinsi",
#     )

#     fig.update_geos(fitbounds="locations", visible=False)
#     fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

#     st.plotly_chart(fig)
    
    