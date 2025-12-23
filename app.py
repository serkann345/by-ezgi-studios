import streamlit as st
import google.generativeai as genai
from PIL import Image
import urllib.parse
import time

# ---------------------------------------------------------
# 1. AYARLAR VE TASARIM (By Ezgi Teması)
# ---------------------------------------------------------
st.set_page_config(layout="wide", page_title="By Ezgi Studios", page_icon="🌿")

# Özel CSS: Bej Arka Plan, Yeşil Butonlar
st.markdown("""
<style>
    /* Ana Arka Plan */
    .stApp {
        background-color: #F5F5DC; /* Bej */
        color: #333333;
    }
    /* Başlık */
    .main-header {
        font-family: 'Helvetica Neue', sans-serif;
        color: #2E8B57; /* Koyu Yeşil */
        text-align: center;
        font-weight: bold;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }
    /* Butonlar */
    .stButton>button {
        background-color: #7CFC00; /* Çim Yeşili */
        color: #006400; /* Koyu Yeşil Yazı */
        border: 2px solid #32CD32;
        border-radius: 12px;
        width: 100%;
        height: 50px;
        font-weight: bold;
        font-size: 18px;
    }
    .stButton>button:hover {
        background-color: #32CD32;
        color: white;
        transform: scale(1.02);
    }
    /* Kilit Ekranı */
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
    password = st.sidebar.text_input("🔑 Stüdyo Giriş Şifresi", type="password")
    if password == 'EZGIVIP':
        st.session_state.authenticated = True
        st.rerun()
    elif password:
        st.sidebar.error("Hatalı Şifre!")

if not st.session_state.authenticated:
    st.markdown("<h1 style='text-align: center; margin-top: 50px; color: #d32f2f;'>🔒 STÜDYO KİLİTLİ</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Lütfen sol menüden şifreyi giriniz.</p>", unsafe_allow_html=True)
    check_password()
    st.stop()

# ---------------------------------------------------------
# 3. FONKSİYONLAR (Gemini 2.5 + Görsel Üretim)
# ---------------------------------------------------------

def analyze_and_create_prompt(api_key, image, model_type, sector, background):
    """Gemini 2.5 Pro kullanarak kıyafeti analiz eder ve prompt yazar."""
    genai.configure(api_key=api_key)
    
    # SENİN BULDUĞUN EN GÜÇLÜ MODEL
    model = genai.GenerativeModel('models/gemini-2.5-pro') 
    
    prompt = f"""
    Sen uzman bir moda fotoğrafçısısın.
    GÖREV: Bu fotoğraftaki kıyafeti (kesimi, rengi, kumaşı, deseni) çok detaylı analiz et.
    AMAÇ: Bu kıyafeti şu özelliklerdeki bir modele giydireceğiz: {model_type}.
    ORTAM: {sector} konsepti, {background} arka planı.
    
    ÇIKTI FORMATI (Sadece İngilizce Prompt Yaz):
    "A photorealistic shot of a {model_type} wearing a [kıyafetin detaylı tarifi], in a {background} setting, {sector} concept, cinematic lighting, 8k, highly detailed texture, fashion magazine style."
    
    Lütfen sadece İngilizce promptu ver, başka açıklama yapma.
    """
    
    try:
        response = model.generate_content([prompt, image])
        return response.text
    except Exception as e:
        return f"Hata: {e}"

def generate_image_url(prompt_text):
    """Metni görsele çeviren motor (Flux Modeli - Ücretsiz)."""
    # Promptu URL'ye uygun hale getir
    encoded_prompt = urllib.parse.quote(prompt_text)
    # Flux Realism modelini kullan
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1280&model=flux&nologo=true&seed={int(time.time())}"
    return url

# ---------------------------------------------------------
# 4. ANA UYGULAMA
# ---------------------------------------------------------
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3050/3050253.png", width=60)
    st.title("Ayarlar")
    api_key = st.text_input("Google API Key:", type="password", help="AIza ile başlayan anahtarınız.")
    st.info("Bu stüdyo Gemini 2.5 Pro teknolojisini kullanır.")

st.markdown("<h1 class='main-header'>🌿 By Ezgi Studios 🌿</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Yapay Zeka Destekli Moda & Prodüksiyon Merkezi</p>", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("1. Yükle & Seç")
    uploaded_file = st.file_uploader("Kıyafet Fotoğrafı Yükle", type=["jpg", "png", "jpeg"])
    
    sector = st.selectbox("Sektör:", ["Gelinlik", "Abiye", "Günlük Giyim", "Tesettür Giyim", "Çanta & Aksesuar"])
    
    model_type = st.selectbox("Model Tercihi:", 
                              ["Turkish Hijab Fashion Model", 
                               "European Fashion Model", 
                               "Asian Fashion Model",
                               "African American Fashion Model"])
    
    bg_choice = st.selectbox("Arka Plan:", 
                             ["Luxury Studio (Gold/Beige)", 
                              "Parisian Street with Flowers", 
                              "Minimalist White Studio", 
                              "Nature / Garden Sunset"])

with col2:
    st.subheader("2. Sonuç")
    
    if uploaded_file and api_key:
        input_image = Image.open(uploaded_file)
        st.image(input_image, caption="Orijinal Fotoğraf", width=200)
        
        if st.button("✨ Çekimi Başlat (Generate)"):
            with st.spinner("Gemini 2.5 Pro kıyafeti inceliyor..."):
                # 1. Adım: Gemini Analizi
                description_prompt = analyze_and_create_prompt(api_key, input_image, model_type, sector, bg_choice)
                
                if "Hata" in description_prompt:
                    st.error("API Hatası: Lütfen anahtarınızı kontrol edin.")
                    st.error(description_prompt)
                else:
                    st.success("Kıyafet Analiz Edildi! Fotoğraf basılıyor...")
                    # st.write(description_prompt) # İstersen promptu görmek için açabilirsin
                    
                    # 2. Adım: Fotoğraf Üretimi
                    with st.spinner("Stüdyo ışıkları ayarlanıyor..."):
                        final_url = generate_image_url(description_prompt)
                        time.sleep(2) # Yüklenmesi için kısa bekleme
                        
                        # Resmi Göster
                        st.image(final_url, caption="By Ezgi AI Design", use_container_width=True)
                        st.balloons()
                        
                        st.markdown(f"[📥 Resmi İndir]({final_url})", unsafe_allow_html=True)
    
    elif not uploaded_file:
        st.info("👈 Lütfen sol taraftan bir fotoğraf yükleyin.")
    elif not api_key:
        st.warning("👈 Lütfen API Anahtarınızı girin.")
