import streamlit as st
import pandas as pd

# ==========================
# CONFIG & CSS
# ==========================
st.set_page_config(page_title="Aplikasi Ledger Keuangan", layout="centered")

st.markdown("""
<style>
/* Card Style */
.card {
    background: #ffffff;
    padding: 20px;
    border-radius: 18px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.08);
    margin-bottom: 20px;
    border: 1px solid #e6e6e6;
}

/* Judul utama */
h1 {
    text-align: center;
    font-weight: 700;
}

/* Tombol */
div.stButton > button {
    width: 100%;
    border-radius: 10px;
    font-size: 18px;
    padding: 8px 0px;
}
</style>
""", unsafe_allow_html=True)

# ==========================
# STATE
# ==========================
if "ledger" not in st.session_state:
    st.session_state.ledger = []

# ==========================
# HEADER
# ==========================
st.markdown("<h1>💳 Aplikasi Ledger Keuangan</h1>", unsafe_allow_html=True)
st.write("Masukkan transaksi pemasukan atau pengeluaran, lalu lihat ringkasannya.")

# ==========================
# INPUT FORM
# ==========================
with st.container():
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    jenis = st.selectbox("Jenis Transaksi", ["in", "out"])
    nominal = st.number_input("Nominal", min_value=1, step=1000)

    tambah = st.button("➕ Tambah Transaksi")

    if tambah:
        if jenis == "in":
            st.session_state.ledger.append(nominal)
        else:
            st.session_state.ledger.append(-nominal)

        st.success("Transaksi berhasil ditambahkan!")

    st.markdown("</div>", unsafe_allow_html=True)

# ==========================
# UNDO BUTTON
# ==========================
with st.container():
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    undo = st.button("↩️ Undo Transaksi Terakhir", type="secondary")

    if undo:
        if len(st.session_state.ledger) > 0:
            st.session_state.ledger.pop()
            st.warning("Transaksi terakhir dihapus.")
        else:
            st.error("Ledger masih kosong.")

    st.markdown("</div>", unsafe_allow_html=True)

# ==========================
# TAMPILKAN TABEL LEDGER
# ==========================
if len(st.session_state.ledger) > 0:
    df = pd.DataFrame({
        "Nominal": st.session_state.ledger,
        "Jenis": ["Pemasukan" if x > 0 else "Pengeluaran" for x in st.session_state.ledger]
    })

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("📘 Daftar Transaksi")
    st.dataframe(df, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ==========================
# HITUNG RINGKASAN
# ==========================
ledger = st.session_state.ledger
saldo_akhir = sum(ledger)
total_pemasukan = sum(x for x in ledger if x > 0)
total_pengeluaran = sum(-x for x in ledger if x < 0)

# ==========================
# TAMPILKAN RINGKASAN
# ==========================
with st.container():
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    st.subheader("📊 Ringkasan Keuangan")
    
    col1, col2 = st.columns(2)
    
    col1.metric("Total Pemasukan", f"Rp {total_pemasukan:,}")
    col2.metric("Total Pengeluaran", f"Rp {total_pengeluaran:,}")

    st.metric("Saldo Akhir", f"Rp {saldo_akhir:,}")

    if len(ledger) > 0:
        st.write(f"**Transaksi Pertama:** {ledger[0]}")
        st.write(f"**Transaksi Terakhir:** {ledger[-1]}")

    st.markdown("</div>", unsafe_allow_html=True)
