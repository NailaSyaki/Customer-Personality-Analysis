import streamlit as st
import pandas as pd
import plotly.express as px # Kita pakai Plotly agar lebih interaktif dibanding Seaborn

st.set_page_config(page_title="Customer Insight Tool", layout="wide")

# 1. Load Data
@st.cache_data
def load_data():
    df = pd.read_csv('data_clean.csv')
    # Memberi nama Cluster agar lebih mudah dibaca orang awam
    cluster_names = {
        1: "💎 The Prime Affluents (Sultan)",
        3: "👴 The Golden Seniors",
        0: "🏠 The Frugal Elders",
        2: "🌱 The Budget Aspirants"
    }
    df['Segment_Name'] = df['Cluster'].map(cluster_names)
    return df

df = load_data()

# --- SIDEBAR ---
st.sidebar.title("🔍 Filter Dashboard")
selected_segments = st.sidebar.multiselect(
    "Pilih Kelompok Pelanggan:",
    options=df['Segment_Name'].unique(),
    default=df['Segment_Name'].unique()
)

filtered_df = df[df['Segment_Name'].isin(selected_segments)]

# --- HEADER ---
st.title("🎯 Strategi Pemasaran Berdasarkan Segmen")
st.markdown(f"Saat ini menganalisis **{len(filtered_df)}** profil pelanggan.")

# --- ROW 1: SUMMARY CARDS ---
col1, col2, col3, col4 = st.columns(4)
col1.metric("💰 Rata-rata Pendapatan", f"${filtered_df['Income'].mean():,.0f}")
col2.metric("🛒 Rata-rata Belanja", f"${filtered_df['Total_Spend'].mean():,.0f}")
col3.metric("🎂 Rata-rata Usia", f"{filtered_df['Age'].mean():.0f} Tahun")
col4.metric("📈 Respon Promo", f"{filtered_df['Response'].mean()*100:.1f}%")

st.divider()

# --- ROW 2: BUSINESS INSIGHTS (The "Storytelling" Part) ---
st.subheader("💡 Apa yang Harus Dilakukan?")
c1, c2 = st.columns([2, 1])

with c1:
    # Grafik Interaktif menggunakan Plotly (bisa di-zoom dan hover)
    fig = px.scatter(filtered_df, x='Income', y='Total_Spend', 
                     color='Segment_Name', size='Total_Spend',
                     hover_data=['Age', 'Education'],
                     title="Hubungan Pendapatan vs Total Belanja")
    st.plotly_chart(fig, use_container_width=True)

with c2:
    st.info("**Rekomendasi Bisnis:**")
    if "💎 The Prime Affluents (Sultan)" in selected_segments:
        st.write("- **Sultan:** Fokus pada produk Wine dan Meat premium. Jangan beri terlalu banyak diskon, mereka lebih suka eksklusivitas.")
    if "👴 The Golden Seniors" in selected_segments:
        st.write("- **Seniors:** Gunakan katalog fisik. Mereka punya daya beli tinggi tapi lebih suka cara belanja tradisional.")
    if "🌱 The Budget Aspirants" in selected_segments:
        st.write("- **Budget Aspirants:** Fokus pada promo 'Buy 1 Get 1' dan kampanye via website.")

# --- ROW 3: PRODUCT ANALYSIS ---
st.divider()
st.subheader("🍷 Produk Apa yang Paling Laku?")
products = {'MntWines': 'Wine', 'MntFruits': 'Buah', 'MntMeatProducts': 'Daging', 
            'MntFishProducts': 'Ikan', 'MntSweetProducts': 'Permen', 'MntGoldProds': 'Emas'}

# Mengubah data untuk grafik bar yang lebih cantik
df_melted = filtered_df.groupby('Segment_Name')[list(products.keys())].mean().reset_index()
df_melted = df_melted.melt(id_vars='Segment_Name', var_name='Produk', value_name='Rata-rata Belanja')
df_melted['Produk'] = df_melted['Produk'].map(products)

fig_bar = px.bar(df_melted, x='Segment_Name', y='Rata-rata Belanja', color='Produk', barmode='group')
st.plotly_chart(fig_bar, use_container_width=True)
