import streamlit as st
import requests
import pandas as pd
from io import BytesIO
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

# Konfigurasi halaman a
st.set_page_config(
    page_title="SSCASN Scraper",
    page_icon="📊",
    layout="wide"
)

# CSS untuk styling
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #1f77b4;
        color: white;
        font-weight: bold;
        border-radius: 5px;
        padding: 0.5rem 1rem;
    }
    .stButton>button:hover {
        background-color: #145a8c;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">📊 SSCASN Data Scraper 2025</div>', unsafe_allow_html=True)

# Fungsi untuk fetch data dengan retry mechanism
def fetch_data_page(url, headers, retries=3):
    for attempt in range(retries):
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 429:  # Rate limit
                time.sleep(2 ** attempt)  # Exponential backoff
                continue
        except Exception as e:
            if attempt == retries - 1:
                st.warning(f"Error fetching {url}: {str(e)}")
            time.sleep(1)
    return None

# Fungsi scraping dengan multithreading
def scrape_sscasn_data(tahun="2025", kode_ref_pend=None, max_workers=5):
    # Validasi tahun
    if not tahun or not tahun.strip():
        tahun = "2025"
    
    base_url = f'https://api-sscasn.bkn.go.id/{tahun.strip()}/portal/spf?'
    
    # Tambahkan parameter kode_ref_pend jika ada
    if kode_ref_pend and kode_ref_pend.strip():
        base_url += f'kode_ref_pend={kode_ref_pend.strip()}&'
    
    base_url += 'offset='
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Referer': 'https://sscasn.bkn.go.id/',
        'Origin': 'https://sscasn.bkn.go.id',
        'Accept': 'application/json',
    }
    
    # Fetch first page untuk mengetahui total data
    first_url = f'{base_url}0'
    first_response = fetch_data_page(first_url, headers)
    
    if not first_response or 'data' not in first_response:
        st.error("Gagal mengambil data. Pastikan koneksi internet stabil.")
        return pd.DataFrame()
    
    # Ambil total data
    total_data = first_response['data'].get('meta', {}).get('total', 0)
    
    if total_data == 0:
        st.warning("Tidak ada data yang ditemukan.")
        return pd.DataFrame()
    
    st.info(f"📝 Total data yang ditemukan: **{total_data}** formasi")
    
    # Setup progress bar
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    all_data = []
    items_per_page = 10
    
    # Hitung jumlah halaman
    total_pages = (total_data + items_per_page - 1) // items_per_page
    
    # Tambahkan data dari first page
    if 'data' in first_response['data']:
        all_data.extend(first_response['data']['data'])
    
    # Buat list URLs untuk halaman selanjutnya
    urls = [f'{base_url}{offset}' for offset in range(items_per_page, total_data, items_per_page)]
    
    # Fetch menggunakan ThreadPoolExecutor untuk kecepatan
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_url = {executor.submit(fetch_data_page, url, headers): url for url in urls}
        
        completed = 0
        for future in as_completed(future_to_url):
            completed += 1
            progress = (completed + 1) / total_pages  # +1 untuk first page
            progress_bar.progress(min(progress, 1.0))
            status_text.text(f"Mengambil data... {completed + 1}/{total_pages} halaman")
            
            result = future.result()
            if result and 'data' in result and 'data' in result['data']:
                all_data.extend(result['data']['data'])
    
    progress_bar.progress(1.0)
    status_text.text(f"✅ Selesai! Total {len(all_data)} data berhasil diambil.")
    
    return pd.DataFrame(all_data)

# Fungsi untuk convert DataFrame ke Excel
def convert_df_to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Data SSCASN')
        
        # Auto-adjust column width
        worksheet = writer.sheets['Data SSCASN']
        for idx, col in enumerate(df.columns):
            max_length = max(
                df[col].astype(str).apply(len).max(),
                len(str(col))
            )
            worksheet.column_dimensions[chr(65 + idx)].width = min(max_length + 2, 50)
    
    return output.getvalue()

# Sidebar untuk input
with st.sidebar:
    st.header("⚙️ Pengaturan")
    
    tahun = st.text_input(
        "Tahun",
        value="2025",
        placeholder="Contoh: 2025",
        help="Masukkan tahun SSCASN"
    )
    
    kode_ref_pend = st.text_input(
        "Kode Referensi Pendidikan",
        placeholder="Contoh: 5109751 (opsional)",
        help="Kosongkan untuk mengambil semua data"
    )
    
    st.markdown("---")
    st.markdown("### 📌 Panduan:")
    st.markdown("""
    - **Tahun**: Masukkan tahun (2024, 2025, 2026, dll)
    - **Kosongkan** kode untuk scrape semua formasi
    - **Isi kode** untuk filter formasi tertentu
    - Proses akan berjalan otomatis setelah klik tombol
    """)
    
    scrape_button = st.button("🚀 Mulai Scraping", type="primary")

# Main content
if scrape_button:
    if not tahun or not tahun.strip():
        st.error("❌ Tahun tidak boleh kosong!")
    else:
        with st.spinner("Memproses data..."):
            df = scrape_sscasn_data(tahun, kode_ref_pend)
            
            if not df.empty:
                # Simpan di session state
                st.session_state['df'] = df
                st.session_state['tahun'] = tahun
                st.success(f"✅ Berhasil mengambil {len(df)} data!")
            else:
                st.error("❌ Tidak ada data yang berhasil diambil.")

# Tampilkan data jika ada di session state
if 'df' in st.session_state and not st.session_state['df'].empty:
    df = st.session_state['df']
    
    st.markdown("---")
    
    # Metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Formasi", len(df))
    with col2:
        if 'ins_nm' in df.columns:
            st.metric("Total Instansi", df['ins_nm'].nunique())
    with col3:
        if 'lokasi_nm' in df.columns:
            st.metric("Total Lokasi", df['lokasi_nm'].nunique())
    
    st.markdown("---")
    
    # Search dan filter
    col1, col2 = st.columns([3, 1])
    with col1:
        search_term = st.text_input("🔍 Cari data", placeholder="Ketik untuk mencari...")
    with col2:
        items_per_page = st.selectbox("Tampilkan per halaman", [10, 25, 50, 100], index=1)
    
    # Filter data berdasarkan search
    if search_term:
        mask = df.astype(str).apply(lambda x: x.str.contains(search_term, case=False, na=False)).any(axis=1)
        filtered_df = df[mask]
    else:
        filtered_df = df
    
    # Pagination
    total_rows = len(filtered_df)
    total_pages = (total_rows + items_per_page - 1) // items_per_page
    
    if total_pages > 0:
        page = st.number_input("Halaman", min_value=1, max_value=total_pages, value=1)
        
        start_idx = (page - 1) * items_per_page
        end_idx = min(start_idx + items_per_page, total_rows)
        
        st.info(f"Menampilkan {start_idx + 1}-{end_idx} dari {total_rows} data")
        
        # Tampilkan tabel
        st.dataframe(
            filtered_df.iloc[start_idx:end_idx],
            use_container_width=True,
            height=500
        )
        
        # Pagination info
        st.caption(f"Halaman {page} dari {total_pages}")
    
    # Tombol download
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        excel_data = convert_df_to_excel(filtered_df if search_term else df)
        st.download_button(
            label="📥 Download Excel",
            data=excel_data,
            file_name=f"data_sscasn_{time.strftime('%Y%m%d_%H%M%S')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
    with col2:
        csv_data = (filtered_df if search_term else df).to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download CSV",
            data=csv_data,
            file_name=f"data_sscasn_{time.strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
        )

else:
    # Tampilan awal
    st.info("👈 Silakan masukkan tahun dan kode referensi pendidikan (opsional), lalu klik tombol **Mulai Scraping** di sidebar untuk memulai.")
    
    st.markdown("---")
    st.markdown("### 📖 Cara Penggunaan:")
    st.markdown("""
    1. Masukkan **tahun** (contoh: 2025, 2026, 2024)
    2. **(Opsional)** Masukkan kode referensi pendidikan di sidebar
    3. Klik tombol **Mulai Scraping**
    4. Tunggu proses selesai
    5. Data akan ditampilkan dalam tabel interaktif
    6. Gunakan fitur pencarian untuk filter data
    7. Download hasil dalam format Excel atau CSV
    """)
