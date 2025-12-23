import streamlit as st
import google.generativeai as genai
from PIL import Image

# ---------------------------------------------------------
# 1. AYARLAR VE TASARIM
# ---------------------------------------------------------
st.set_page_config(layout="wide", page_title="By Ezgi Studios", page_icon="🌿")

# Özel Tasarım (Bej Rengi)
st.markdown("""
<style>
    .stApp {
        background-color: #f5f5dc;
    }
    .main-header {
        font-family: 'Helvetica Neue', sans-serif;
        color: #4a4a4a;
        text-align: center;
        font-weight: bold;
    }
    .stButton>button {
        background-color: #8b5a2b;
        color: white;
        border-radius: 20px;
        width: 100%;
        border: none;
    }
    .stButton>button:hover {
        background-color: #6d4621;
    }
    .locked-box {
        border: 2px solid #ff4b4b;
        padding: 20px;
        border-radius: 10px;
        background-color: #ffe6e6;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. GÜVENLİK SİSTEMİ (Şifre: EZGIVIP)
# ---------------------------------------------------------
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

def check_password():
    password = st.sidebar.text_input("🔑 Stüdyo Şifresi / Password", type="password")
    if password == 'EZGIVIP':
        st.session_state.authenticated = True
        st.rerun()
    elif password:
        st.sidebar.error("Hatalı Şifre!")

if not st.session_state.authenticated:
    st.markdown("<h1 style='text-align: center; color: #d32f2f;'>🔒 KİLİTLİ / LOCKED</h1>", unsafe_allow_html=True)
    st.markdown("""
        <div class='locked-box'>
            <h3>Bu stüdyo özel davetle çalışmaktadır.</h3>
            <p>Erişim sağlamak için lütfen sol menüden şifre giriniz.</p>
        </div>
    """, unsafe_allow_html=True)
    check_password()
    st.stop()

# ---------------------------------------------------------
# 3. ANA UYGULAMA
# ---------------------------------------------------------
with st.sidebar:
    st.success("✅ Giriş Başarılı")
    st.markdown("---")
    # API Key Kutusu
    api_key = st.text_input("Google AI Studio Key:", type="password")
    if not api_key:
        st.warning("⚠️ Lütfen API Anahtarınızı girin.")

st.markdown("<h1 class='main-header'>🌿 By Ezgi Studios 🌿</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>AI Destekli Profesyonel Moda Stüdyosu (v2.5 Pro)</p>", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("1. Ayarlar")
    sector = st.selectbox("Sektör:", ["Aksesuar", "Gelinlik", "Abiye", "Günlük Giyim", "Ayakkabı"])
    model_type = st.selectbox("Model:", ["Türk Tesettürlü Model", "Avrupalı Model", "Asyalı Model"])
    uploaded_file = st.file_uploader("Fotoğraf Yükle", type=["jpg", "png", "jpeg"])

with col2:
    st.subheader("2. Sonuç")
    
    if uploaded_file and api_key:
        image = Image.open(uploaded_file)
        st.image(image, caption="Yüklenen Görsel", use_container_width=True)
        
        if st.button("✨ Çekimi Başlat"):
            try:
                genai.configure(api_key=api_key)
                
                # SENİN LİSTENDEKİ EN İYİ MODEL BURADA!
                model = genai.GenerativeModel('models/gemini-2.5-pro')
                
                with st.spinner("Gemini 2.5 Pro işleniyor..."):
                    prompt = f"""
                    Sen dünyanın en iyi moda fotoğrafçısısın.
                    Görev: Bu görseldeki ürünü analiz et.
                    Konsept: {sector}
                    Model: {model_type} (Yüz hatları ve detaylar ultra gerçekçi olsun).
                    Bu ürünü kullanarak moda dergisi kapağı kalitesinde bir sahne hayal et ve detaylıca anlat.
                    """
                    
                    response = model.generate_content([prompt, image])
                    st.write(response.text)
                    st.success("İşlem Başarılı! 🌿")
                    
            except Exception as e:
                st.error(f"Hata: {e}")
    
    elif not uploaded_file:
        st.info("Lütfen fotoğraf yükleyin.")
