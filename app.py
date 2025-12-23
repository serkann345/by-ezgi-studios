import streamlit as st
import google.generativeai as genai
from PIL import Image
import urllib.parse
import random

# ---------------------------------------------------------
# 1. TASARIM (BY EZGI PRESTIGE)
# ---------------------------------------------------------
st.set_page_config(layout="wide", page_title="By Ezgi - AI Studio", page_icon="✨")

st.markdown("""
<style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .main-header { 
        font-family: 'Helvetica Neue', sans-serif; 
        color: #FFD700; /* Altın Rengi */
        text-align: center; 
        font-weight: 300;
        letter-spacing: 2px;
        margin-bottom: 30px;
    }
    .stButton>button {
        background-color: #FFD700;
        color: #000000;
        border-radius: 0px;
        width: 100%;
        height: 60px;
        font-weight: bold;
        border: none;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .stButton>button:hover {
        background-color: #ffffff;
        color: #000000;
    }
    .uploaded-img { border: 1px solid #333; }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. GÜVENLİK
# ---------------------------------------------------------
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

def check_password():
    password = st.sidebar.text_input("🔑 GİRİŞ ŞİFRESİ", type="password")
    if password == 'EZGIVIP':
        st.session_state.authenticated = True
        st.rerun()
    elif password:
        st.sidebar.error("Erişim Reddedildi")

if not st.session_state.authenticated:
    st.title("🔒 BY EZGI STUDIOS")
    check_password()
    st.stop()

# ---------------------------------------------------------
# 3. GOOGLE STUDIO MANTIK MOTORU
# ---------------------------------------------------------

def create_high_end_prompt(api_key, image, model_pref, scene_pref):
    """Google AI Studio'daki gibi detaylı prompt oluşturur"""
    genai.configure(api_key=api_key)
    
    # En güçlü modelini kullanıyoruz
    model = genai.GenerativeModel('gemini-1.5-pro') 
    
    # Bu prompt, Google Studio'nun çalışma mantığını simüle eder
    system_prompt = f"""
    Sen dünyanın en iyi moda editörüsün (Vogue/Harper's Bazaar seviyesi).
    GÖREV: Yüklenen fotoğraftaki kıyafeti (kumaş, kesim, desen, yaka) en küçük dikişine kadar analiz et.
    
    HEDEF: Bu kıyafeti şu modele giydireceğiz: {model_pref}.
    MEKAN: {scene_pref}.
    
    KRİTİK: Bana görüntü oluşturma motoru için İngilizce bir "Master Prompt" yaz.
    
    Kurallar:
    1. Asla "resimdeki kıyafet" deme, kıyafeti sıfırdan detaylıca tarif et (örn: "A crimson silk dress with lace sleeves...").
    2. Işıklandırmayı "Cinematic, softbox lighting, 8k, unreal engine 5 render" olarak ayarla.
    3. Modelin yüz hatlarını, cilt dokusunu ve duruşunu detaylandır.
    4. Sadece İngilizce prompt metnini ver.
    """
    
    try:
        response = model.generate_content([system_prompt, image])
        return response.text
    except Exception as e:
        return None

def generate_visual(prompt):
    """Görüntüyü oluşturur"""
    # Google Studio kalitesine en yakın sonucu veren 'Flux-Realism' motorunu kullanıyoruz
    # Seed'i rastgele yaparak her seferinde farklı bir sonuç almanı sağlıyoruz
    seed = random.randint(1, 1000000)
    encoded = urllib.parse.quote(prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded}?width=1080&height=1350&model=flux-realism&seed={seed}&nologo=true&enhance=true"
    return url

# ---------------------------------------------------------
# 4. ARAYÜZ
# ---------------------------------------------------------
with st.sidebar:
    st.header("AYARLAR")
    api_key = st.text_input("Google API Key", type="password")
    
    st.divider()
    
    st.subheader("MODEL SEÇİMİ")
    model_choice = st.radio("", [
        "Turkish Hijab Model (Modern)",
        "European Fashion Model",
        "Asian Fashion Model",
        "Classic Hijab Model"
    ])
    
    st.subheader("MEKAN")
    scene_choice = st.selectbox("", [
        "Luxury Studio (Gold/Beige)",
        "Paris Street Style",
        "Minimalist White",
        "Nature / Sunset"
    ])

st.markdown("<h1 class='main-header'>BY EZGI STUDIOS</h1>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.caption("REFERANS FOTOĞRAF")
    uploaded_file = st.file_uploader("", type=["jpg", "png", "jpeg"])
    if uploaded_file:
        st.image(uploaded_file, use_container_width=True)

with col2:
    st.caption("SONUÇ")
    
    if st.button("PRODÜKSİYONU BAŞLAT"):
        if uploaded_file and api_key:
            input_image = Image.open(uploaded_file)
            
            with st.spinner("1/2: Moda Editörü Analiz Ediyor (Gemini Pro)..."):
                # Önce Google'ın zekasını kullanıp mükemmel tarifi alıyoruz
                master_prompt = create_high_end_prompt(api_key, input_image, model_choice, scene_choice)
            
            if master_prompt:
                with st.spinner("2/2: Fotoğraf Stüdyoda Çekiliyor..."):
                    # Sonra bu tarifi görselleştiriyoruz
                    result_url = generate_visual(master_prompt)
                    
                    # Resmi Göster
                    st.image(result_url, use_container_width=True)
                    st.success("Çekim Tamamlandı.")
                    st.markdown(f"[Yüksek Kalite İndir]({result_url})", unsafe_allow_html=True)
            else:
                st.error("API Anahtarını kontrol et veya tekrar dene.")
        else:
            st.warning("Lütfen fotoğraf yükleyin ve API Anahtarını girin.")
