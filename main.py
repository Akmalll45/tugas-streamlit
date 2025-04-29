# app.py

import streamlit as st
import pandas as pd
import plotly.express as px

# Setup halaman
st.set_page_config(page_title="Dashboard Saham BEI", layout="wide", page_icon="📈")

# CSS Kustom
st.markdown("""
<style>
body {
    background-color: #f5f7fa;
}
.main-container {
    background-color: #ffffff;
    padding: 2rem;
    border-radius: 1.25rem;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.1);
}
h1, h2, h3, h4 {
    color: #1f3b57;
}
footer {
    text-align: center;
    color: #999;
    font-size: 0.85rem;
    margin-top: 2rem;
}
.metric-title {
    color: #555;
    font-size: 0.85rem;
}
</style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("saham.txt", sep="\t")
    df['listingDate'] = pd.to_datetime(df['listingDate'])
    df['TahunListing'] = df['listingDate'].dt.year
    return df

df = load_data()

# =============================
# HEADER
# =============================
st.markdown("<div class='main-container'>", unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center;'>📊 Dashboard Saham Bursa Efek Indonesia</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size:1.1rem;'>Dibuat dengan oleh <strong style='color:#0e76a8;'>Muhammad Akmal</strong></p>", unsafe_allow_html=True)
st.markdown("---")

# =============================
# SIDEBAR FILTER
# =============================
st.sidebar.header("🔎 Filter")
board_list = df['listingBoard'].unique()
selected_board = st.sidebar.multiselect("Pilih Listing Board", board_list, default=list(board_list))

search_keyword = st.sidebar.text_input("Cari Nama atau Kode Saham")

# Filter data
filtered_df = df[df['listingBoard'].isin(selected_board)]
if search_keyword:
    filtered_df = filtered_df[
        filtered_df['name'].str.contains(search_keyword, case=False, na=False) |
        filtered_df['code'].str.contains(search_keyword, case=False, na=False)
    ]

# =============================
# DASHBOARD METRIK
# =============================
col1, col2, col3 = st.columns(3)
col1.metric(label="📈 Total Emiten", value=f"{filtered_df.shape[0]:,}")
col2.metric(label="🏆 Saham Terbanyak", value=filtered_df.loc[filtered_df['shares'].idxmax()]['code'])
col3.metric(label="📅 Tahun Listing Tertua", value=int(filtered_df['TahunListing'].min()))

# =============================
# TABEL DATA
# =============================
st.subheader("📋 Tabel Saham Terfilter")
st.dataframe(filtered_df, use_container_width=True)

# =============================
# GRAFIK INTERAKTIF
# =============================
st.subheader("📊 Visualisasi Data Saham")

tab1, tab2, tab3 = st.tabs(["📦 Distribusi Saham", "📅 Tahun Listing", "🏷️ Listing Board"])

with tab1:
    fig1 = px.histogram(filtered_df, x='shares', nbins=50, title="Distribusi Jumlah Saham Beredar", color_discrete_sequence=["#0e76a8"])
    st.plotly_chart(fig1, use_container_width=True)

with tab2:
    fig2 = px.histogram(filtered_df, x='TahunListing', title="Jumlah Emiten per Tahun Listing", color_discrete_sequence=["#ff6361"])
    st.plotly_chart(fig2, use_container_width=True)

with tab3:
    board_count = filtered_df['listingBoard'].value_counts().reset_index()
    board_count.columns = ['ListingBoard', 'Jumlah']
    fig3 = px.pie(board_count, names='ListingBoard', values='Jumlah', title="Komposisi Listing Board", color_discrete_sequence=px.colors.sequential.Blues)
    st.plotly_chart(fig3, use_container_width=True)

# =============================
# FOOTER
# =============================
st.markdown("""
<hr>
<footer>© 2025 Dibuat oleh <strong>Muhammad Akmal</strong>. Dashboard ini dibuat berdasarkan data dari BEI.</footer>
</div>
""", unsafe_allow_html=True)
