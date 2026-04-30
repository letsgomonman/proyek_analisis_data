import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

sns.set(style='dark')

def create_revenue_2018_df(df):
    year_2018_df = df[df['order_year'] == 2018]
    revenue_per_category_df = year_2018_df.groupby('product_category_name_english')['price'].sum().reset_index()
    revenue_per_category_df = revenue_per_category_df.sort_values(by='price', ascending=False)
    return revenue_per_category_df

def create_rfm_df(df):
    rfm_df = df.groupby(by="customer_unique_id", as_index=False).agg({
        "order_purchase_timestamp": "max",
        "order_id": "nunique",
        "price": "sum"
    })
    rfm_df.columns = ["customer_unique_id", "max_order_timestamp", "frequency", "monetary"]
    
    rfm_df["max_order_timestamp"] = rfm_df["max_order_timestamp"].dt.date
    recent_date = df["order_purchase_timestamp"].dt.date.max() + pd.Timedelta(days=1)
    rfm_df["recency"] = rfm_df["max_order_timestamp"].apply(lambda x: (recent_date - x).days)
    rfm_df.drop("max_order_timestamp", axis=1, inplace=True)
    
    return rfm_df

all_df = pd.read_csv("dashboard/main_data.csv")

datetime_columns = ["order_purchase_timestamp", "order_delivered_customer_date"]
all_df.sort_values(by="order_purchase_timestamp", inplace=True)
all_df.reset_index(drop=True, inplace=True)

for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column])

revenue_2018_df = create_revenue_2018_df(all_df)
rfm_df = create_rfm_df(all_df)

st.header('E-Commerce Dashboard :sparkles:')

st.subheader("Performa Pendapatan Kategori Produk (Tahun 2018)")

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(24, 6))
colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

sns.barplot(x="price", y="product_category_name_english", data=revenue_2018_df.head(5), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("Total Pendapatan (BRL)", fontsize=12)
ax[0].set_title("Kategori Produk dengan Pendapatan Tertinggi", loc="center", fontsize=15)
ax[0].tick_params(axis='y', labelsize=12)

sns.barplot(x="price", y="product_category_name_english", data=revenue_2018_df.sort_values(by="price", ascending=True).head(5), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("Total Pendapatan (BRL)", fontsize=12)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Kategori Produk dengan Pendapatan Terendah", loc="center", fontsize=15)
ax[1].tick_params(axis='y', labelsize=12)

st.pyplot(fig)

with st.expander("Lihat Insight Performa Produk"):
    st.write(
        """
         Berdasarkan analisis performa produk di tahun 2018, kategori health_beauty merupakan penyumbang pendapatan (revenue) tertinggi bagi perusahaan. 
         Sebaliknya, kategori cd_dvds_musicals menghasilkan pendapatan paling rendah, yang mengindikasikan kurangnya minat pasar atau nilai jual barang yang sangat kecil di kategori tersebut.
        """
    )

st.subheader("Best Customer Based on RFM Parameters")

col1, col2, col3 = st.columns(3)
with col1:
    avg_recency = round(rfm_df.recency.mean(), 1)
    st.metric("Average Recency (days)", value=avg_recency)
with col2:
    avg_frequency = round(rfm_df.frequency.mean(), 2)
    st.metric("Average Frequency", value=avg_frequency)
with col3:
    avg_monetary = format_currency(rfm_df.monetary.mean(), "BRL", locale='pt_BR')
    st.metric("Average Monetary", value=avg_monetary)

fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(30, 6))
colors = ["#72BCD4", "#72BCD4", "#72BCD4", "#72BCD4", "#72BCD4"]

sns.barplot(y="recency", x="customer_unique_id", data=rfm_df.sort_values(by="recency", ascending=True).head(5), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("Customer ID", fontsize=12)
ax[0].set_title("By Recency (days)", loc="center", fontsize=18)
ax[0].tick_params(axis ='x', labelsize=10, rotation=45)
ax[0].set_xticklabels([val[:5]+'...' for val in rfm_df.sort_values(by="recency", ascending=True).head(5)['customer_unique_id']])

sns.barplot(y="frequency", x="customer_unique_id", data=rfm_df.sort_values(by="frequency", ascending=False).head(5), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("Customer ID", fontsize=12)
ax[1].set_title("By Frequency", loc="center", fontsize=18)
ax[1].tick_params(axis='x', labelsize=10, rotation=45)
ax[1].set_xticklabels([val[:5]+'...' for val in rfm_df.sort_values(by="frequency", ascending=False).head(5)['customer_unique_id']])

sns.barplot(y="monetary", x="customer_unique_id", data=rfm_df.sort_values(by="monetary", ascending=False).head(5), palette=colors, ax=ax[2])
ax[2].set_ylabel(None)
ax[2].set_xlabel("Customer ID", fontsize=12)
ax[2].set_title("By Monetary", loc="center", fontsize=18)
ax[2].tick_params(axis='x', labelsize=10, rotation=45)
ax[2].set_xticklabels([val[:5]+'...' for val in rfm_df.sort_values(by="monetary", ascending=False).head(5)['customer_unique_id']])

st.pyplot(fig)

with st.expander("Lihat Insight RFM Analysis"):
    st.write(
        """
        Melalui Analisis RFM dan Clustering (Binning), berhasil memetakan segmentasi pelanggan. 
        Terdapat kelompok pelanggan Best Customers yang rutin berbelanja dengan total pengeluaran yang tinggi. 
        Namun, porsi terbesar pelanggan saat ini mungkin berada di segmen "Cold" (tidak bertransaksi lebih dari 90 hari terakhir).
        """
    )

st.caption('Copyright © Abdurrahman Muhaddits 2026')
