#!/usr/bin/env python3
"""
SSCASN Scraper - Streamlit App (WITH DEMO DATA)
================================================
Aplikasi web untuk scraping dan mencari formasi SSCASN
+ Demo data sesuai screenshot untuk testing

Author: Claude
Date: 2026-01-30
"""

import streamlit as st
import requests
import pandas as pd
import time
from datetime import datetime
from typing import List, Dict, Optional
import io

# Konfigurasi halaman
st.set_page_config(
    page_title="SSCASN Scraper",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stButton>button {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)


def get_demo_data() -> List[Dict]:
    """Generate demo data sesuai dengan screenshot SSCASN"""
    demo_data = [
        {
            "jabatan_nm": "PENATA LAYANAN OPERASIONAL",
            "ins_nm": "Badan Gizi Nasional",
            "lokasi_nm": "Direktorat Penyediaan dan Penyaluran Wilayah I - Deputi Bidang Penyediaan dan Penyaluran",
            "formasi_nm": "PPPK Teknis Khusus",
            "disable": "Ya",
            "penghasilan": "0 - 0",
            "jumlah_formasi": 10081,
            "status": "DITUTUP"
        },
        {
            "jabatan_nm": "PENATA LAYANAN OPERASIONAL",
            "ins_nm": "Badan Gizi Nasional",
            "lokasi_nm": "Direktorat Penyediaan dan Penyaluran Wilayah II - Deputi Bidang Penyediaan dan Penyaluran",
            "formasi_nm": "PPPK Teknis Khusus",
            "disable": "Ya",
            "penghasilan": "0 - 0",
            "jumlah_formasi": 12493,
            "status": "DITUTUP"
        },
        {
            "jabatan_nm": "PENATA LAYANAN OPERASIONAL",
            "ins_nm": "Badan Gizi Nasional",
            "lokasi_nm": "Direktorat Penyediaan dan Penyaluran Wilayah III | Deputi Bidang Penyediaan dan Penyaluran",
            "formasi_nm": "PPPK Teknis Khusus",
            "disable": "Ya",
            "penghasilan": "0 - 0",
            "jumlah_formasi": 8444,
            "status": "DITUTUP"
        },
        {
            "jabatan_nm": "PENATA LAYANAN OPERASIONAL",
            "ins_nm": "Badan Gizi Nasional",
            "lokasi_nm": "Biro Umum dan Keuangan - Sekretariat Utama",
            "formasi_nm": "PPPK Teknis Khusus",
            "disable": "Ya",
            "penghasilan": "0 - 0",
            "jumlah_formasi": 10,
            "status": "DITUTUP"
        },
        {
            "jabatan_nm": "PENATA LAYANAN OPERASIONAL",
            "ins_nm": "Badan Gizi Nasional",
            "lokasi_nm": "Biro Hukum dan Hubungan Masyarakat - Sekretariat Utama",
            "formasi_nm": "PPPK Teknis Khusus",
            "disable": "Ya",
            "penghasilan": "0 - 0",
            "jumlah_formasi": 10,
            "status": "DITUTUP"
        },
        {
            "jabatan_nm": "PROGRAMMER",
            "ins_nm": "Kementerian Komunikasi dan Informatika",
            "lokasi_nm": "Direktorat Jenderal Aplikasi Informatika",
            "formasi_nm": "CPNS",
            "disable": "Tidak",
            "penghasilan": "4.5 - 6.0",
            "jumlah_formasi": 15,
            "pendidikan_nm": "S1 TEKNIK INFORMATIKA/ILMU KOMPUTER/SISTEM INFORMASI",
            "status": "BUKA"
        },
        {
            "jabatan_nm": "ANALIS KEBIJAKAN AHLI PERTAMA",
            "ins_nm": "Kementerian Komunikasi dan Informatika",
            "lokasi_nm": "Sekretariat Jenderal",
            "formasi_nm": "CPNS",
            "disable": "Tidak",
            "penghasilan": "4.2 - 5.8",
            "jumlah_formasi": 8,
            "pendidikan_nm": "S1 ADMINISTRASI NEGARA/ADMINISTRASI PUBLIK",
            "status": "BUKA"
        },
        {
            "jabatan_nm": "STATISTISI AHLI PERTAMA",
            "ins_nm": "Badan Pusat Statistik",
            "lokasi_nm": "Direktorat Statistik Kependudukan dan Ketenagakerjaan",
            "formasi_nm": "CPNS",
            "disable": "Ya",
            "penghasilan": "4.0 - 5.5",
            "jumlah_formasi": 25,
            "pendidikan_nm": "S1 STATISTIKA/MATEMATIKA",
            "status": "BUKA"
        },
        {
            "jabatan_nm": "PENELITI AHLI PERTAMA",
            "ins_nm": "Badan Riset dan Inovasi Nasional",
            "lokasi_nm": "Organisasi Riset Ilmu Pengetahuan Alam",
            "formasi_nm": "CPNS",
            "disable": "Tidak",
            "penghasilan": "5.0 - 7.0",
            "jumlah_formasi": 12,
            "pendidikan_nm": "S2 FISIKA/KIMIA/BIOLOGI",
            "status": "BUKA"
        },
        {
            "jabatan_nm": "AUDITOR AHLI PERTAMA",
            "ins_nm": "Badan Pengawasan Keuangan dan Pembangunan",
            "lokasi_nm": "Deputi Bidang Pengawasan Penyelenggaraan Keuangan Daerah",
            "formasi_nm": "CPNS",
            "disable": "Tidak",
            "penghasilan": "4.8 - 6.5",
            "jumlah_formasi": 20,
            "pendidikan_nm": "S1 AKUNTANSI/EKONOMI",
            "status": "BUKA"
        },
    ]
    
    # Duplicate data untuk simulasi banyak records
    extended_data = []
    for i in range(50):  # Generate 500 records (50 * 10)
        for item in demo_data:
            new_item = item.copy()
            new_item['jumlah_formasi'] = item['jumlah_formasi'] + i
            extended_data.append(new_item)
    
    return extended_data


class SSCASNScraper:
    """Class untuk scraping data SSCASN"""
    
    def __init__(self, year: str = '2025'):
        self.base_url = f"https://api-sscasn.bkn.go.id/{year}/portal/spf"
        self.year = year
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Referer': 'https://sscasn.bkn.go.id/',
            'Origin': 'https://sscasn.bkn.go.id',
            'Accept': 'application/json',
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
    
    def get_page(self, offset: int, kode_ref_pend: str = '') -> Optional[Dict]:
        """Ambil satu halaman data"""
        params = {
            'kode_ref_pend': kode_ref_pend,
            'offset': offset
        }
        
        try:
            response = self.session.get(self.base_url, params=params, timeout=30)
            if response.status_code == 200:
                return response.json()
            return None
        except:
            return None
    
    def scrape_all(self, kode_ref_pend: str = '', max_records: Optional[int] = None, 
                   progress_callback=None) -> List[Dict]:
        """Scrape semua data dengan progress tracking"""
        all_data = []
        offset = 0
        items_per_page = 10
        
        while True:
            if progress_callback:
                progress_callback(f"Mengambil data offset {offset}...")
            
            data = self.get_page(offset, kode_ref_pend)
            
            if not data:
                break
            
            # Ekstrak items
            items = (data.get('data') or data.get('results') or 
                    data.get('items') or data.get('formasi') or [])
            
            if isinstance(data, list):
                items = data
            
            if not items or len(items) == 0:
                break
            
            all_data.extend(items)
            
            if max_records and len(all_data) >= max_records:
                all_data = all_data[:max_records]
                break
            
            offset += items_per_page
            time.sleep(0.5)
        
        return all_data


def search_dataframe(df: pd.DataFrame, search_term: str) -> pd.DataFrame:
    """Search di seluruh kolom DataFrame"""
    if not search_term:
        return df
    
    search_term = search_term.lower()
    mask = df.astype(str).apply(lambda x: x.str.lower().str.contains(search_term, na=False)).any(axis=1)
    return df[mask]


def paginate_dataframe(df: pd.DataFrame, page: int, items_per_page: int) -> pd.DataFrame:
    """Pagination untuk DataFrame"""
    start_idx = page * items_per_page
    end_idx = start_idx + items_per_page
    return df.iloc[start_idx:end_idx]


def convert_df_to_csv(df: pd.DataFrame) -> bytes:
    """Convert DataFrame ke CSV bytes untuk download"""
    return df.to_csv(index=False, encoding='utf-8-sig').encode('utf-8-sig')


def main():
    # Header
    st.markdown('<div class="main-header">🔍 SSCASN Formasi Scraper</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Cari dan ekspor data formasi CPNS/PPPK 2025</div>', unsafe_allow_html=True)
    
    # Initialize session state
    if 'scraped_data' not in st.session_state:
        st.session_state.scraped_data = None
    if 'df' not in st.session_state:
        st.session_state.df = None
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 0
    if 'search_term' not in st.session_state:
        st.session_state.search_term = ""
    
    # Sidebar - Konfigurasi Scraping
    with st.sidebar:
        st.header("⚙️ Konfigurasi Scraping")
        
        # Mode selection
        mode = st.radio(
            "Mode",
            options=['Demo Mode (Test)', 'Live Scraping'],
            index=0,
            help="Demo mode menggunakan data contoh, Live scraping mengambil data asli dari API"
        )
        
        if mode == 'Live Scraping':
            year = st.selectbox(
                "Tahun",
                options=['2025', '2024'],
                index=0
            )
            
            kode_ref_pend = st.text_input(
                "Kode Ref Pendidikan",
                value="",
                help="Kosongkan untuk semua formasi"
            )
            
            max_records = st.number_input(
                "Max Records",
                min_value=10,
                max_value=10000,
                value=500,
                step=10
            )
        
        st.markdown("---")
        
        # Tombol Scrape/Load
        button_label = "📊 Load Demo Data" if mode == 'Demo Mode (Test)' else "🚀 Mulai Scraping"
        
        if st.button(button_label, type="primary", use_container_width=True):
            if mode == 'Demo Mode (Test)':
                # Load demo data
                with st.spinner('Loading demo data...'):
                    time.sleep(1)  # Simulate loading
                    data = get_demo_data()
                    
                    if data:
                        st.session_state.scraped_data = data
                        st.session_state.df = pd.DataFrame(data)
                        st.session_state.current_page = 0
                        st.success(f"✅ Demo data loaded: {len(data)} records!")
                        st.balloons()
            else:
                # Live scraping
                scraper = SSCASNScraper(year=year)
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                def update_progress(message):
                    status_text.text(message)
                
                with st.spinner('Scraping data...'):
                    try:
                        data = scraper.scrape_all(
                            kode_ref_pend=kode_ref_pend,
                            max_records=max_records,
                            progress_callback=update_progress
                        )
                        
                        if data:
                            st.session_state.scraped_data = data
                            st.session_state.df = pd.DataFrame(data)
                            st.session_state.current_page = 0
                            progress_bar.progress(100)
                            status_text.empty()
                            st.success(f"✅ Berhasil scraping {len(data)} records!")
                            st.balloons()
                        else:
                            st.error("❌ Tidak ada data yang berhasil di-scrape")
                            
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
                        progress_bar.empty()
                        status_text.empty()
        
        # Info
        st.markdown("---")
        st.markdown("### 📋 Info")
        if mode == 'Demo Mode (Test)':
            st.info("💡 Demo mode menampilkan data contoh untuk testing fitur aplikasi")
        else:
            st.markdown("""
            **Cara Mencari Kode:**
            1. Buka [SSCASN](https://sscasn.bkn.go.id)
            2. Filter pendidikan
            3. Buka DevTools (F12)
            4. Lihat `kode_ref_pend`
            
            **Contoh kode:**
            - `5201101` = S1 TI
            - `5109751` = S1 Geomatika
            - Kosongkan = Semua
            """)
    
    # Main content
    if st.session_state.df is not None:
        df = st.session_state.df
        
        # Metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("📊 Total Records", len(df))
        with col2:
            st.metric("📝 Total Kolom", len(df.columns))
        with col3:
            if 'ins_nm' in df.columns:
                st.metric("🏢 Instansi", df['ins_nm'].nunique())
            else:
                st.metric("🏢 Instansi", "-")
        with col4:
            scrape_time = datetime.now().strftime("%H:%M:%S")
            st.metric("🕐 Waktu", scrape_time)
        
        st.markdown("---")
        
        # Search Bar
        col1, col2 = st.columns([3, 1])
        with col1:
            search_input = st.text_input(
                "🔍 Cari formasi (jabatan, instansi, lokasi, dll)",
                value=st.session_state.search_term,
                placeholder="Ketik untuk mencari...",
                key="search_box"
            )
            if search_input != st.session_state.search_term:
                st.session_state.search_term = search_input
                st.session_state.current_page = 0
        
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🔄 Reset", use_container_width=True):
                st.session_state.search_term = ""
                st.session_state.current_page = 0
                st.rerun()
        
        # Filter data
        filtered_df = search_dataframe(df, st.session_state.search_term)
        
        if st.session_state.search_term:
            st.info(f"🔍 Ditemukan {len(filtered_df)} hasil dari {len(df)} total records")
        
        # Pagination
        items_per_page = 20
        total_pages = (len(filtered_df) - 1) // items_per_page + 1 if len(filtered_df) > 0 else 1
        
        # Pagination controls
        col1, col2, col3, col4, col5 = st.columns([1, 1, 2, 1, 1])
        
        with col1:
            if st.button("⏮️ First", disabled=st.session_state.current_page == 0):
                st.session_state.current_page = 0
                st.rerun()
        
        with col2:
            if st.button("◀️ Prev", disabled=st.session_state.current_page == 0):
                st.session_state.current_page -= 1
                st.rerun()
        
        with col3:
            st.markdown(f"<div style='text-align: center; padding: 0.5rem;'>"
                       f"<b>Halaman {st.session_state.current_page + 1} dari {total_pages}</b>"
                       f"</div>", unsafe_allow_html=True)
        
        with col4:
            if st.button("Next ▶️", disabled=st.session_state.current_page >= total_pages - 1):
                st.session_state.current_page += 1
                st.rerun()
        
        with col5:
            if st.button("Last ⏭️", disabled=st.session_state.current_page >= total_pages - 1):
                st.session_state.current_page = total_pages - 1
                st.rerun()
        
        # Display data
        if len(filtered_df) > 0:
            paginated_df = paginate_dataframe(
                filtered_df, 
                st.session_state.current_page, 
                items_per_page
            )
            
            # Prepare display with column mapping (sesuai screenshot)
            display_df = paginated_df.copy()
            
            column_mapping = {
                'jabatan_nm': 'Jabatan',
                'ins_nm': 'Instansi',
                'lokasi_nm': 'Unit Kerja',
                'formasi_nm': 'Formasi',
                'disable': '(CPNS)Dapat Diisi Disabilitas?',
                'penghasilan': 'Penghasilan (juta)',
                'jumlah_formasi': 'Jumlah Kebutuhan',
                'pendidikan_nm': 'Pendidikan',
                'status': 'Status'
            }
            
            for old, new in column_mapping.items():
                if old in display_df.columns:
                    display_df = display_df.rename(columns={old: new})
            
            # Reorder columns sesuai screenshot
            preferred_order = [
                'Jabatan', 'Instansi', 'Unit Kerja', 'Formasi',
                '(CPNS)Dapat Diisi Disabilitas?', 'Penghasilan (juta)',
                'Jumlah Kebutuhan', 'Status'
            ]
            
            display_columns = [col for col in preferred_order if col in display_df.columns]
            display_columns.extend([col for col in display_df.columns if col not in display_columns])
            
            display_df = display_df[display_columns]
            
            # Display table
            st.dataframe(
                display_df,
                use_container_width=True,
                height=600,
                hide_index=True
            )
            
            # Record info
            start_record = st.session_state.current_page * items_per_page + 1
            end_record = min(start_record + items_per_page - 1, len(filtered_df))
            st.caption(f"Menampilkan record {start_record}-{end_record} dari {len(filtered_df)}")
            
        else:
            st.warning("⚠️ Tidak ada data yang sesuai dengan pencarian")
        
        # Export buttons
        st.markdown("---")
        st.subheader("📥 Export Data")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            csv_all = convert_df_to_csv(df)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            st.download_button(
                label="📊 Export Semua Data (CSV)",
                data=csv_all,
                file_name=f"sscasn_all_{timestamp}.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        with col2:
            if st.session_state.search_term and len(filtered_df) > 0:
                csv_filtered = convert_df_to_csv(filtered_df)
                st.download_button(
                    label="🔍 Export Hasil Pencarian (CSV)",
                    data=csv_filtered,
                    file_name=f"sscasn_filtered_{timestamp}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            else:
                st.button("🔍 Export Hasil Pencarian (CSV)", disabled=True, use_container_width=True)
        
        with col3:
            if len(paginated_df) > 0:
                csv_page = convert_df_to_csv(paginated_df)
                st.download_button(
                    label="📄 Export Halaman Ini (CSV)",
                    data=csv_page,
                    file_name=f"sscasn_page_{st.session_state.current_page + 1}_{timestamp}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            else:
                st.button("📄 Export Halaman Ini (CSV)", disabled=True, use_container_width=True)
        
        # Data Preview
        with st.expander("📋 Preview Struktur Data"):
            st.write("**Kolom yang tersedia:**")
            st.write(list(df.columns))
            st.write("\n**Contoh data (5 baris pertama):**")
            st.dataframe(df.head(), use_container_width=True)
    
    else:
        # Landing page
        st.markdown("---")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.info("""
            ### 👋 Selamat Datang!
            
            **Cara menggunakan:**
            1. Pilih mode di sidebar (Demo/Live)
            2. Klik tombol untuk load/scrape data
            3. Gunakan search untuk mencari formasi
            4. Export data sesuai kebutuhan
            
            **Mode Demo** cocok untuk testing tanpa perlu koneksi API.
            **Mode Live** untuk scraping data real dari SSCASN.
            """)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 1rem;'>
        <p><b>SSCASN Scraper v2.0</b> | Made with ❤️ using Streamlit</p>
        <p><small>⚠️ Gunakan secara bertanggung jawab</small></p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
