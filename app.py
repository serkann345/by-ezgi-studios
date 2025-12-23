import streamlit as st
import google.generativeai as genai
from PIL import Image

# ---------------------------------------------------------
# 1. AYARLAR VE TASARIM
# ---------------------------------------------------------
st.set_page_config(layout="wide", page_title="By Ezgi Studios", page_icon="🌿")

# Özel CSS Tasarımı (Bej Rengi ve Fontlar)
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
# 2. GÜVENLİK SİSTEMİ (EZGIVIP)
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

# Eğer giriş yapılmadıysa KİLİTLİ EKRANI göster
if not st.session_state.authenticated:
    st.markdown("<h1 style='text-align: center; color: #d32f2f;'>🔒 KİLİTLİ / LOCKED</h1>", unsafe_allow_html=True)
    st.markdown("""
        <div class='locked-box'>
            <h3>Bu stüdyo özel davetle çalışmaktadır.</h3>
            <p>Erişim sağlamak için lütfen sol menüden şifre giriniz.</p>
        </div>
    """, unsafe_allow_html=True)
    check_password()
    st.stop()  # Uygulamanın geri kalanını durdur

# ---------------------------------------------------------
# 3. ANA UYGULAMA (Giriş Yapıldıysa Burası Çalışır)
# ---------------------------------------------------------

# Sol Menü Ayarları
with st.sidebar:
    st.success("✅ Giriş Başarılı / Logged In")
    st.markdown("---")
    
    # --- API KEY GİRİŞİ (HATAYI ÇÖZEN KISIM) ---
    api_key = st.text_input("Google AI Studio Key:", type="password", help="aistudio.google.com adresinden alacağınız AIza ile başlayan anahtar.")
    
    if not api_key:
        st.warning("⚠️ Lütfen kullanmak için Google API Anahtarınızı girin.")

# Ana Başlık
st.markdown("<h1 class='main-header'>🌿 By Ezgi Studios 🌿</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>AI Destekli Profesyonel Moda & Prodüksiyon Stüdyosu</p>", unsafe_allow_html=True)
st.markdown("---")

# İki Sütunlu Yapı
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("1. Ayarlarınızı Yapın")
    sector = st.selectbox("Sektör Seçimi:", ["Aksesuar", "Gelinlik", "Abiye", "Günlük Giyim", "Ayakkabı"])
    model_type = st.selectbox("Model Tipi:", ["Türk Tesettürlü Model", "Avrupalı Model", "Asyalı Model", "Siyahi Model"])
    uploaded_file = st.file_uploader("Ürün/Kıyafet Fotoğrafı Yükle", type=["jpg", "png", "jpeg"])

with col2:
    st.subheader("2. Stüdyo Sonucu")
    
    if uploaded_file and api_key:
        # Resmi Göster
        image = Image.open(uploaded_file)
        st.image(image, caption="Yüklenen Tasarım", use_container_width=True)
        
        # Buton
        if st.button("✨ Çekimi Başlat (Generate)"):
            try:
                # Modeli Yapılandır
                genai.configure(api_key=api_key)
                
                # Model Seçimi (En garantisi flash modelidir)
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                with st.spinner("Model hazırlanıyor, ışıklar ayarlanıyor..."):
                    # Prompt Mantığı
                    prompt = f"""
                    Sen profesyonel bir moda fotoğrafçısısın.
                    Bu görseldeki ürünü al ve {model_type} üzerinde, {sector} konseptine uygun olarak
                    ultra gerçekçi, sinematik ışıklandırma ile yeniden hayal et.
                    Yüz hatları net olsun. 8k çözünürlük, moda dergisi kapağı kalitesinde olsun.
                    """
                    
                    # Üretim
                    response = model.generate_content([prompt, image])
                    st.image(response.text, caption="Oluşturulan Görsel (Not: Metin tabanlı model görsel linki veremeyebilir, görsel yeteneği için Pro sürüm gerekebilir)", use_container_width=True)
                    
                    # Eğer görsel gelmezse metin çıktısını yazdır (Hata ayıklama için)
                    st.write(response.text)
                    
                    st.success("Çekim Tamamlandı!")
            except Exception as e:
                st.error(f"Bir hata oluştu: {e}")
                st.info("İpucu: API Key'inizin doğru olduğundan ve başında/sonunda boşluk olmadığından emin olun.")
                
    elif not uploaded_file:
        st.info("Lütfen önce bir fotoğraf yükleyin.")
    elif not api_key:
        st.error("Lütfen sol menüden API Anahtarınızı girin.")
