#!/usr/bin/env python3
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
    for i in range(50):  # Generate 500 records
        for item in demo_data:
            new_item = item.copy()
            new_item['jumlah_formasi'] = item['jumlah_formasi'] + i
            extended_data.append(new_item)
    
    return extended_data


class SSCASNScraper:
    """
    Class untuk scraping data SSCASN
    Menggunakan API yang sudah terbukti berhasil dari GitHub repositories
    """
    
    def __init__(self, year: str = '2024'):
        """
        Initialize scraper dengan konfigurasi yang sudah terbukti bekerja
        
        Note: API 2024 lebih stabil, untuk 2025 mungkin struktur berubah
        """
        self.base_url = f"https://api-sscasn.bkn.go.id/{year}/portal/spf"
        self.year = year
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
            'Referer': 'https://sscasn.bkn.go.id/',
            'Origin': 'https://sscasn.bkn.go.id'
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
    
    def get_page(self, offset: int, kode_ref_pend: str = '') -> Optional[Dict]:
        """
        Ambil satu halaman data dari API
        
        Args:
            offset: Position offset untuk pagination
            kode_ref_pend: Kode referensi pendidikan (optional)
            
        Returns:
            Dictionary response atau None jika gagal
        """
        # Build URL dengan parameter
        params = {
            'kode_ref_pend': kode_ref_pend,
            'offset': offset
        }
        
        try:
            response = self.session.get(
                self.base_url,
                params=params,
                timeout=30
            )
            
            if response.status_code == 200:
                try:
                    return response.json()
                except:
                    return None
            else:
                return None
                
        except Exception as e:
            return None
    
    def scrape_all(self, 
                   kode_ref_pend: str = '', 
                   max_records: Optional[int] = None,
                   progress_callback=None,
                   status_callback=None) -> List[Dict]:
        """
        Scrape semua data dengan progress tracking
        
        Args:
            kode_ref_pend: Kode referensi pendidikan
            max_records: Maksimal records yang akan di-scrape
            progress_callback: Function untuk update progress bar
            status_callback: Function untuk update status text
            
        Returns:
            List of dictionaries berisi data formasi
        """
        all_data = []
        offset = 0
        items_per_page = 10  # SSCASN API returns 10 items per page
        consecutive_failures = 0
        max_consecutive_failures = 3
        
        while True:
            # Update status
            if status_callback:
                status_callback(f"📥 Mengambil data offset {offset}...")
            
            # Get data
            response_data = self.get_page(offset, kode_ref_pend)
            
            if not response_data:
                consecutive_failures += 1
                if status_callback:
                    status_callback(f"⚠️ Gagal mengambil data (attempt {consecutive_failures}/{max_consecutive_failures})")
                
                if consecutive_failures >= max_consecutive_failures:
                    if status_callback:
                        status_callback(f"❌ Terlalu banyak kegagalan, berhenti di offset {offset}")
                    break
                
                time.sleep(2)  # Wait before retry
                continue
            
            # Reset failure counter
            consecutive_failures = 0
            
            # Extract items dari response
            # API SSCASN bisa mengembalikan berbagai struktur
            items = []
            
            if isinstance(response_data, dict):
                # Coba berbagai kemungkinan key
                items = (response_data.get('data') or 
                        response_data.get('results') or 
                        response_data.get('items') or
                        response_data.get('formasi') or
                        [])
            elif isinstance(response_data, list):
                items = response_data
            
            # Jika tidak ada items, selesai
            if not items or len(items) == 0:
                if status_callback:
                    status_callback(f"✅ Tidak ada data lagi di offset {offset}")
                break
            
            # Add items to all_data
            all_data.extend(items)
            
            if status_callback:
                status_callback(f"✅ Berhasil: {len(items)} items | Total: {len(all_data)}")
            
            # Update progress bar
            if progress_callback and max_records:
                progress = min(100, int((len(all_data) / max_records) * 100))
                progress_callback(progress)
            
            # Check if reached max_records
            if max_records and len(all_data) >= max_records:
                all_data = all_data[:max_records]
                if status_callback:
                    status_callback(f"✅ Mencapai batas maksimal: {max_records} records")
                break
            
            # Move to next page
            offset += items_per_page
            
            # Rate limiting - jangan overload server
            time.sleep(1)
        
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


def format_dataframe_display(df: pd.DataFrame) -> pd.DataFrame:
    """
    Format DataFrame untuk display dengan column mapping sesuai screenshot SSCASN
    """
    display_df = df.copy()
    
    # Column mapping ke Bahasa Indonesia (sesuai screenshot)
    column_mapping = {
        'jabatan_nm': 'Jabatan',
        'ins_nm': 'Instansi',
        'lokasi_nm': 'Unit Kerja',
        'formasi_nm': 'Formasi',
        'disable': '(CPNS)Dapat Diisi Disabilitas?',
        'penghasilan': 'Penghasilan (juta)',
        'jumlah_formasi': 'Jumlah Kebutuhan',
        'pendidikan_nm': 'Pendidikan',
        'status': 'Status',
        'jp_nama': 'Jenis Jabatan',
        'lokasi_kerja': 'Lokasi Kerja'
    }
    
    # Rename columns yang ada
    for old, new in column_mapping.items():
        if old in display_df.columns:
            display_df = display_df.rename(columns={old: new})
    
    # Reorder columns sesuai urutan screenshot
    preferred_order = [
        'Jabatan', 'Instansi', 'Unit Kerja', 'Formasi',
        '(CPNS)Dapat Diisi Disabilitas?', 'Penghasilan (juta)',
        'Jumlah Kebutuhan', 'Pendidikan', 'Status'
    ]
    
    # Build final column order
    display_columns = [col for col in preferred_order if col in display_df.columns]
    # Add remaining columns yang tidak ada di preferred order
    display_columns.extend([col for col in display_df.columns if col not in display_columns])
    
    return display_df[display_columns]


def main():
    # Header
    st.markdown('<div class="main-header">🔍 SSCASN Formasi Scraper</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Cari dan ekspor data formasi CPNS/PPPK</div>', unsafe_allow_html=True)
    
    # Initialize session state
    if 'scraped_data' not in st.session_state:
        st.session_state.scraped_data = None
    if 'df' not in st.session_state:
        st.session_state.df = None
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 0
    if 'search_term' not in st.session_state:
        st.session_state.search_term = ""
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Konfigurasi")
        
        # Mode selection
        mode = st.radio(
            "Mode",
            options=['📊 Demo Mode', '🚀 Live Scraping'],
            index=0,
            help="Demo mode untuk testing, Live scraping untuk data real"
        )
        
        if mode == '🚀 Live Scraping':
            st.warning("⚠️ **Catatan Penting:**\n\n"
                      "API SSCASN 2025 mungkin belum tersedia atau strukturnya berbeda. "
                      "Gunakan tahun 2024 untuk hasil yang lebih stabil.")
            
            year = st.selectbox(
                "Tahun",
                options=['2024', '2025'],
                index=0,
                help="2024 lebih stabil, 2025 mungkin belum tersedia"
            )
            
            kode_ref_pend = st.text_input(
                "Kode Ref Pendidikan",
                value="",
                help="Kosongkan untuk semua. Contoh: 5109751 untuk S1 Teknik Geomatika"
            )
            
            max_records = st.number_input(
                "Max Records",
                min_value=10,
                max_value=10000,
                value=500,
                step=10,
                help="Batasi jumlah data untuk mencegah timeout"
            )
        
        st.markdown("---")
        
        # Action button
        button_label = "📊 Load Demo Data" if mode == '📊 Demo Mode' else "🚀 Mulai Scraping"
        
        if st.button(button_label, type="primary", use_container_width=True):
            if mode == '📊 Demo Mode':
                # Demo mode
                with st.spinner('Loading demo data...'):
                    time.sleep(1)
                    data = get_demo_data()
                    
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
                
                def update_progress(progress):
                    progress_bar.progress(progress)
                
                def update_status(message):
                    status_text.text(message)
                
                try:
                    data = scraper.scrape_all(
                        kode_ref_pend=kode_ref_pend,
                        max_records=max_records,
                        progress_callback=update_progress,
                        status_callback=update_status
                    )
                    
                    if data and len(data) > 0:
                        st.session_state.scraped_data = data
                        st.session_state.df = pd.DataFrame(data)
                        st.session_state.current_page = 0
                        progress_bar.progress(100)
                        status_text.empty()
                        st.success(f"✅ Berhasil scraping {len(data)} records!")
                        st.balloons()
                    else:
                        st.error("❌ Tidak ada data yang berhasil di-scrape.\n\n"
                                "Kemungkinan:\n"
                                "- API sedang down\n"
                                "- Kode referensi pendidikan salah\n"
                                "- Tahun yang dipilih tidak tersedia\n\n"
                                "Coba gunakan **Demo Mode** untuk testing fitur aplikasi.")
                        progress_bar.empty()
                        status_text.empty()
                        
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}\n\nGunakan Demo Mode untuk testing.")
                    progress_bar.empty()
                    status_text.empty()
        
        # Info section
        st.markdown("---")
        st.markdown("### 📋 Info")
        
        if mode == '📊 Demo Mode':
            st.info("💡 **Demo Mode**\n\n"
                   "- 500 sample records\n"
                   "- Data mirip dengan SSCASN asli\n"
                   "- Semua fitur berfungsi normal\n"
                   "- Perfect untuk testing & learning")
        else:
            st.markdown("""
            **Cara Mencari Kode:**
            1. Buka [sscasn.bkn.go.id](https://sscasn.bkn.go.id)
            2. Filter pendidikan
            3. F12 → Network tab
            4. Lihat `kode_ref_pend`
            
            **Contoh Kode:**
            - `5201101` = S1 TI
            - `5109751` = S1 Geomatika
            - Kosongkan = Semua
            
            **Tips:**
            - Mulai dengan max 100-500 records
            - Gunakan tahun 2024 untuk stabilitas
            - Jika gagal, coba Demo Mode dulu
            """)
    
    # Main content
    if st.session_state.df is not None:
        df = st.session_state.df
        
        # Metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("📊 Total Records", f"{len(df):,}")
        with col2:
            st.metric("📝 Kolom", len(df.columns))
        with col3:
            if 'ins_nm' in df.columns:
                st.metric("🏢 Instansi", df['ins_nm'].nunique())
            else:
                st.metric("🏢 Instansi", "-")
        with col4:
            current_time = datetime.now().strftime("%H:%M:%S")
            st.metric("🕐 Waktu", current_time)
        
        st.markdown("---")
        
        # Search
        col1, col2 = st.columns([3, 1])
        with col1:
            search_input = st.text_input(
                "🔍 Cari formasi",
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
        
        # Filter
        filtered_df = search_dataframe(df, st.session_state.search_term)
        
        if st.session_state.search_term:
            st.info(f"🔍 Ditemukan **{len(filtered_df):,}** hasil dari **{len(df):,}** total records")
        
        # Pagination
        items_per_page = 20
        total_pages = max(1, (len(filtered_df) - 1) // items_per_page + 1)
        
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
            paginated_df = paginate_dataframe(filtered_df, st.session_state.current_page, items_per_page)
            display_df = format_dataframe_display(paginated_df)
            
            st.dataframe(
                display_df,
                use_container_width=True,
                height=600,
                hide_index=True
            )
            
            start_record = st.session_state.current_page * items_per_page + 1
            end_record = min(start_record + items_per_page - 1, len(filtered_df))
            st.caption(f"Menampilkan record {start_record:,}-{end_record:,} dari {len(filtered_df):,}")
        else:
            st.warning("⚠️ Tidak ada data yang sesuai dengan pencarian")
        
        # Export
        st.markdown("---")
        st.subheader("📥 Export Data")
        
        col1, col2, col3 = st.columns(3)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        with col1:
            csv_all = convert_df_to_csv(df)
            st.download_button(
                label=f"📊 Export Semua ({len(df):,} records)",
                data=csv_all,
                file_name=f"sscasn_all_{timestamp}.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        with col2:
            if st.session_state.search_term and len(filtered_df) > 0:
                csv_filtered = convert_df_to_csv(filtered_df)
                st.download_button(
                    label=f"🔍 Export Filtered ({len(filtered_df):,} records)",
                    data=csv_filtered,
                    file_name=f"sscasn_filtered_{timestamp}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            else:
                st.button(f"🔍 Export Filtered", disabled=True, use_container_width=True)
        
        with col3:
            if len(paginated_df) > 0:
                csv_page = convert_df_to_csv(paginated_df)
                st.download_button(
                    label=f"📄 Export Page ({len(paginated_df)} records)",
                    data=csv_page,
                    file_name=f"sscasn_page_{st.session_state.current_page + 1}_{timestamp}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            else:
                st.button(f"📄 Export Page", disabled=True, use_container_width=True)
        
        # Data info
        with st.expander("📋 Info Data"):
            st.write("**Kolom:**", ", ".join(df.columns))
            st.write("\n**Sample (5 baris pertama):**")
            st.dataframe(df.head(), use_container_width=True)
    
    else:
        # Landing page
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.info("""
            ### 👋 Selamat Datang!
            
            **Pilih mode di sidebar:**
            
            📊 **Demo Mode** (Recommended)
            - Testing tanpa internet
            - 500 sample records
            - Semua fitur aktif
            
            🚀 **Live Scraping**
            - Data real dari SSCASN API
            - Perlu koneksi internet
            - Gunakan tahun 2024 untuk stabilitas
            
            **Cara pakai:**
            1. Pilih mode
            2. Klik tombol
            3. Search & Export!
            """)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 1rem;'>
        <p><b>SSCASN Scraper v2.1</b> | Production Ready</p>
        <p><small>⚠️ Gunakan secara bertanggung jawab | Data untuk keperluan pribadi/edukasi</small></p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
