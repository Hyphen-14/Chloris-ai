import streamlit as st
import pandas as pd
import plotly.express as px
import os
from config import COLORS, PLANT_COLORS # Import warna tanaman
from utils import get_history_dataframe, delete_single_record

def render_reports_page():
    """Render halaman laporan dengan Visualisasi Native & Warna Spesifik"""
    
    # --- HEADER ---
    st.markdown(f"""
    <div class="page-header-box">
        <h2 style="color: {COLORS['text_main']}; margin-top: 0;">📊 Laporan & Analisis</h2>
        <p style="color: {COLORS['text_body']}; margin-bottom: 0;">
            Pantau kesehatan tanamanmu secara mendetail berdasarkan riwayat scan.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # 1. LOAD DATA
    df = get_history_dataframe()
    
    if df.empty:
        st.info("👋 Belum ada data riwayat. Silakan lakukan scan tanaman dan klik tombol 'Simpan'.")
        return

    # --- PRE-PROCESSING ---
    def extract_plant_type(disease_name):
        name = str(disease_name).lower()
        if 'tomato' in name or 'tomat' in name: return '🍅 Tomat'
        if 'potato' in name or 'kentang' in name: return '🥔 Kentang'
        if 'corn' in name or 'jagung' in name: return '🌽 Jagung'
        if 'lettuce' in name or 'selada' in name: return '🥬 Selada'
        if 'pepper' in name or 'cabai' in name or 'cabe' in name: return '🌶️ Cabai/Paprika'
        if 'strawberry' in name or 'stroberi' in name: return '🍓 Stroberi'
        if 'cucumber' in name or 'mentimun' in name: return '🥒 Mentimun'
        return '🌿 Tanaman Lain'

    df['plant_type'] = df['disease_name'].apply(extract_plant_type)
    df['status_kesehatan'] = df['disease_name'].apply(lambda x: 'Sehat' if 'Sehat' in str(x) or 'Healthy' in str(x) else 'Sakit')

    # --- 2. SUMMARY METRICS ---
    total_scan = len(df)
    total_sakit = len(df[df['status_kesehatan'] == 'Sakit'])
    rasio_sehat = ((total_scan - total_sakit) / total_scan) * 100 if total_scan > 0 else 0
    
    col1, col2, col3 = st.columns(3)
    metrics = [
        ("Total Aktivitas", f"{total_scan}", "📷"),
        ("Tanaman Sakit", f"{total_sakit}", "⚠️"),
        ("Rasio Kesehatan", f"{rasio_sehat:.1f}%", "🛡️")
    ]
    
    for col, (label, val, icon) in zip([col1, col2, col3], metrics):
        with col:
            st.markdown(f"""
            <div style="background: {COLORS['white']}; padding: 15px; border-radius: 10px; border: 1px solid {COLORS['border']}; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
                <div style="font-size: 2rem; margin-bottom: 5px;">{icon}</div>
                <div style="color: {COLORS['text_light']}; font-size: 0.9rem;">{label}</div>
                <div style="color: {COLORS['primary']}; font-size: 1.5rem; font-weight: 700;">{val}</div>
            </div>
            """, unsafe_allow_html=True)
            
    st.markdown("---")
    
    # --- 3. VISUALISASI (METODE NATIVE CONTAINER) ---
    c1, c2 = st.columns(2)
    
    with c1:
        # Peta Persebaran (Sunburst)
        # WARNA: Berdasarkan JENIS TANAMAN (PLANT_COLORS) agar mudah dibedakan
        fig_sun = px.sunburst(
            df, 
            path=['plant_type', 'disease_name'],
            color='plant_type', # Warnai berdasarkan jenis tanaman
            color_discrete_map=PLANT_COLORS # Gunakan palet warna kita
        )
        
        # Bungkus dalam Container CSS Native
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">🗺️ Persebaran Jenis Tanaman</div>', unsafe_allow_html=True)
        
        fig_sun.update_layout(
            margin=dict(t=0, l=0, r=0, b=0), 
            height=300,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_sun, use_container_width=True, config={'displayModeBar': True}) # Interaktivitas ON
        st.markdown('</div>', unsafe_allow_html=True)
        
    with c2:
        # Statistik per Tanaman (Bar Chart)
        # WARNA: Berdasarkan STATUS KESEHATAN (Hijau/Oranye)
        plant_stats = df.groupby(['plant_type', 'status_kesehatan']).size().reset_index(name='count')
        
        fig_bar = px.bar(
            plant_stats, 
            x='plant_type', 
            y='count', 
            color='status_kesehatan', # Warnai berdasarkan Sehat/Sakit
            color_discrete_map={'Sehat': COLORS['success'], 'Sakit': COLORS['warning']},
            barmode='stack'
        )
        
        # Bungkus dalam Container CSS Native
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">📊 Status Sehat vs Sakit</div>', unsafe_allow_html=True)
        
        fig_bar.update_layout(
            xaxis_title=None, 
            yaxis_title="Jumlah Scan",
            legend_title=None,
            margin=dict(t=0, l=0, r=0, b=0),
            height=300,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font={'color': COLORS['text_body']}
        )
        st.plotly_chart(fig_bar, use_container_width=True, config={'displayModeBar': True}) # Interaktivitas ON
        st.markdown('</div>', unsafe_allow_html=True)

    # --- 4. GALERI RIWAYAT ---
    st.markdown("---")
    st.markdown(f"<h4 style='color:{COLORS['text_main']};'>🖼️ Galeri Riwayat</h4>", unsafe_allow_html=True)
    
    recent_df = df.sort_values(by='timestamp', ascending=False).head(4)
    cols = st.columns(4)
    for idx, (index, row) in enumerate(recent_df.iterrows()):
        col = cols[idx % 4]
        with col:
            if os.path.exists(row['image_path']):
                st.image(row['image_path'], use_container_width=True)
                status_color = COLORS['success'] if row['status_kesehatan'] == 'Sehat' else COLORS['warning']
                st.markdown(f"""
                <div style="font-size: 0.75rem; background: white; padding: 5px; border: 1px solid {COLORS['border']}; border-radius: 0 0 8px 8px; border-top: none;">
                    <div style="font-weight: bold; color: {COLORS['text_main']}; overflow: hidden; white-space: nowrap; text-overflow: ellipsis;">{row['disease_name']}</div>
                    <div style="color: {status_color}; font-weight: 600;">{row['confidence']}%</div>
                </div>
                """, unsafe_allow_html=True)

    # --- 5. DELETE FEATURE ---
    st.markdown("---")
    with st.expander("🗑️ Kelola / Hapus Data"):
        if df.empty:
            st.info("Tidak ada data.")
        else:
            df['label_option'] = df['timestamp'] + " - " + df['disease_name']
            selected_items = st.multiselect("Pilih data yang ingin dihapus:", options=df['label_option'].tolist())
            
            if selected_items and st.button("Hapus Terpilih", type="primary"):
                success_count = 0
                for item in selected_items:
                    ts = item.split(" - ")[0]
                    res, msg = delete_single_record(ts)
                    if res: success_count += 1
                
                if success_count:
                    st.success(f"Berhasil menghapus {success_count} data!")
                    st.rerun()

    # --- 6. TABEL ---
    with st.expander("📄 Data Mentah"):
        st.dataframe(df, use_container_width=True)