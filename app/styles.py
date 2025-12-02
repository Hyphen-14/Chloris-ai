import streamlit as st

def load_css():
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Montserrat:wght@300;400;600&display=swap');

            /* BACKGROUND: Deep Jungle Night */
            .stApp {
                background-color: #0a0f0d;
                background-image: radial-gradient(circle at 50% 0%, #1a2f23 0%, #0a0f0d 80%);
                color: #e0f2f1;
            }

            /* TYPOGRAPHY */
            h1, h2, h3 {
                font-family: 'Playfair Display', serif;
                color: #A8E890 !important; /* Mint Neon */
                text-shadow: 0 0 10px rgba(168, 232, 144, 0.3);
            }
            p, div, label, span {
                font-family: 'Montserrat', sans-serif;
                color: #d1e7dd;
            }

            /* GLASS CARD (Kotak Kaca) */
            .glass-card {
                background: rgba(20, 30, 25, 0.6);
                backdrop-filter: blur(12px);
                border-radius: 20px;
                border: 1px solid rgba(168, 232, 144, 0.15);
                padding: 20px;
                margin-bottom: 20px;
                box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.5);
                transition: transform 0.3s ease, box-shadow 0.3s ease, border-color 0.3s;
            }
            .glass-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 0 25px rgba(168, 232, 144, 0.2);
                border-color: rgba(168, 232, 144, 0.6);
            }

            /* INFO BOX */
            .info-box {
                background: rgba(255, 255, 255, 0.05);
                border-radius: 12px;
                padding: 10px;
                text-align: center;
                border: 1px solid rgba(255,255,255,0.1);
                transition: 0.3s;
            }
            .info-box:hover {
                background: rgba(168, 232, 144, 0.1);
                border-color: #A8E890;
            }

            /* METRIC BOX */
            .metric-box {
                text-align: center;
                padding: 15px;
                border-radius: 15px;
                background: linear-gradient(145deg, rgba(255, 255, 255, 0.05), rgba(255, 255, 255, 0.02));
                border: 1px solid rgba(255, 182, 193, 0.2);
                margin-bottom: 10px;
            }
            .metric-value {
                font-family: 'Montserrat', sans-serif;
                font-size: 26px;
                font-weight: bold;
                color: #FFB7B2;
                text-shadow: 0 0 8px rgba(255, 183, 178, 0.4);
            }
            .metric-label {
                font-size: 12px; color: #a3b1a8; letter-spacing: 1px; text-transform: uppercase;
            }

            /* SIDEBAR */
            section[data-testid="stSidebar"] {
                background-color: #050806;
                border-right: 1px solid rgba(168, 232, 144, 0.1);
            }
            
            /* TOMBOL */
            .stButton button {
                background: linear-gradient(90deg, #4A6B5A, #2F5242);
                color: #A8E890;
                font-weight: 600;
                border: 1px solid #4A6B5A;
                border-radius: 12px;
                padding: 0.5rem 1rem;
                transition: 0.3s;
            }
            .stButton button:hover {
                background: linear-gradient(90deg, #A8E890, #4A6B5A);
                color: #0a0f0d;
                box-shadow: 0 0 20px rgba(168, 232, 144, 0.6);
                border-color: #A8E890;
            }
        </style>
    """, unsafe_allow_html=True)