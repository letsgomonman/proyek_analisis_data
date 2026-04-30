\# Proyek Analisis Data: E-Commerce Public Dataset



Proyek ini merupakan tugas akhir dari kelas Belajar Fundamental Analisis Data. Tujuan dari proyek ini adalah untuk menganalisis dataset E-Commerce untuk mendapatkan \*insight\* bisnis dan memvisualisasikannya melalui sebuah \*dashboard\* interaktif.



\## Pertanyaan Bisnis

Proyek ini dibuat untuk menjawab dua pertanyaan bisnis utama:

1\. Apa saja kategori produk yang menghasilkan total pendapatan (\*revenue\*) tertinggi dan terendah selama periode tahun 2018?

2\. Bagaimana segmentasi pelanggan berdasarkan tingkat RFM (\*Recency, Frequency, Monetary\*) selama periode transaksi terakhir, dan kelompok pelanggan mana yang paling bernilai (\*Best Customers\*)?



\## Setup Environment



\### Anaconda:

```bash

conda create --name main-ds python=3.9

conda activate main-ds

pip install -r requirements.txt



\### Shell-Terminal

```

mkdir proyek\_analisis\_data

cd proyek\_analisis\_data

pipenv install

pipenv shell

pip install -r requirements.txt

```



\### Run steamlit app

```

streamlit run dashboard.py

```

