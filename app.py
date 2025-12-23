import streamlit as st
import google.generativeai as genai
from PIL import Image
import time

# --- SAYFA VE MARKA AYARLARI ---
st.set_page_config(page_title="By Ezgi Studios", page_icon="🌿", layout="wide")

# --- TASARIM (BEJ & LAWN GREEN) ---
st.markdown("""
<style>
    /* 1. ANA ARKA PLAN: BEJ */
    .stApp {
        background-color: #F5F5DC;
        color: #333333;
    }

    /* 2. BAŞLIKLAR */
    h1 {
        color: #2E8B57 !important;
        font-family: 'Helvetica Neue', sans-serif;
        text-align: center;
        padding-bottom: 10px;
    }
    
    h2, h3, p, label, .stMarkdown, .stRadio label {
        color: #333333 !important;
        font-weight: 500;
    }

    /* 3. BUTONLAR: LAWN YEŞİLİ */
    div.stButton > button { 
        background-color: #7CFC00; 
        color: #006400; 
        border: 2px solid #32CD32;
        border-radius: 12px; 
        height: 55px; 
        width: 100%;
        font-size: 18px;
        font-weight: bold;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    div.stButton > button:hover {
        background-color: #32CD32;
        color: white;
        transform: translateY(-2px);
    }
    
    /* 4. GÖRSEL ÇERÇEVELERİ */
    .stImage > img {
        border: 4px solid #7CFC00;
        border-radius: 15px; 
        transition: transform 0.3s; 
        box-shadow: 0 5px 15px rgba(0,0,0,0.1); 
    }
    .stImage > img:hover { transform: scale(1.03); z-index: 10; }

    /* 5. SIDEBAR */
    section[data-testid="stSidebar"] {
        background-color: #FFFFFF;
        border-right: 1px solid #ddd;
    }
    section[data-testid="stSidebar"] h1, section[data-testid="stSidebar"] label {
        color: #333333 !important;
    }
</style>
""", unsafe_allow_html=True)

# --- DİL SÖZLÜĞÜ ---
languages = {
    "Türkçe": {
        "title": "🌿 By Ezgi Studios 🌿",
        "subtitle": "AI Destekli Natural & Profesyonel Moda Stüdyosu",
        "sector_label": "Çekim Sektörünü Seçiniz:",
        "sectors": ["Aksesuar (Jewelry/Watch)", "Gelinlik (Wedding)", "Abiye (Evening)", "Günlük Giyim (Casual)", "Çanta (Bags)", "Ayakkabı (Shoes)"], 
        "upload_label": " Referans Fotoğrafı",
        "button_start": "✦ Çekimi Başlat ✦",
        "model_design": "👤 Model Seçimi",
        "bg_label": "Arka Plan Konsepti",
        "vid_title": "🎬 By Ezgi Video Production",
        "vid_select": "Videoya dönüştürülecek pozu seçin:",
        "vid_motion_label": "A) Hazır Hareket Seçimi:",
        "vid_custom_label": "B) Özel Hareket Talimatı (İsteğe Bağlı):",
        "vid_custom_placeholder": "Örn: Saçlar hafifçe rüzgarda uçuşsun, kamera yavaşça yüze yaklaşsın...",
        "btn_preset": "🎬 Seçili Hareketi Uygula",
        "btn_custom": "✨ Özel Talimatı Uygula",
        "vid_success": "By Ezgi Studios prodüksiyonu tamamlandı!",
        "motions": ["Podyum Yürüyüşü", "360 Derece Dönüş", "Hafif Rüzgar/Dalgalanma", "Sinematik Zoom"]
    },
    "English": {
        "title": "🌿 By Ezgi Studios 🌿",
        "subtitle": "AI Powered Natural & Professional Fashion Hub",
        "sector_label": "Select Shooting Sector:",
        "sectors": ["Accessories", "Wedding Dress", "Evening Wear", "Casual Wear", "Bags", "Shoes"],
        "upload_label": " Reference Photo",
        "button_start": "✦ Start Shoot ✦",
        "model_design": "👤 Model Selection",
        "bg_label": "Background Concept",
        "vid_title": "🎬 By Ezgi Video Production",
        "vid_select": "Select pose to animate:",
        "vid_motion_label": "A) Select Preset Motion:",
        "vid_custom_label": "B) Custom Motion Instruction (Optional):",
        "vid_custom_placeholder": "E.g., Hair blowing in wind, slow zoom to face...",
        "btn_preset": "🎬 Apply Preset Motion",
        "btn_custom": "✨ Apply Custom Instruction",
        "vid_success": "By Ezgi Studios production completed!",
        "motions": ["Runway Walk", "360 Spin", "Wind/Fabric Detail", "Cinematic Zoom"]
    }
}

# --- AYARLAR ---
st.sidebar.title("🌐 Language / Dil")
selected_lang = st.sidebar.selectbox("", ["Türkçe", "English"])
T = languages[selected_lang]

st.sidebar.divider()
st.sidebar.title("🔐 Studio Key")
st.sidebar.info("Uygulamayı kullanmak için kendi Google AI Studio anahtarınızı giriniz.")
user_api_key = st.sidebar.text_input("Google AI API Key:", type="password")

if user_api_key:
    genai.configure(api_key=user_api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.sidebar.warning("Giriş Anahtarı Bekleniyor...")
    st.stop()

# --- ANA EKRAN ---
st.title(T["title"])
st.markdown(f"<h3 style='text-align: center;'>{T['subtitle']}</h3>", unsafe_allow_html=True)
st.write("") 

if 'generated_images' not in st.session_state:
    st.session_state.generated_images = []

# --- SOL PANEL: RESİM ÜRETİMİ ---
with st.container():
    sektor = st.selectbox(T["sector_label"], T["sectors"])
    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        urun_file = st.file_uploader(f"{sektor} {T['upload_label']}", type=['jpg', 'png', 'jpeg'])
        if urun_file: st.image(urun_file, width=250)

    with col2:
        is_shoes = "Ayakkabı" in sektor or "Shoes" in sektor
        karakter_tipi = "AI"
        char_file = None
        
        if not is_shoes:
            karakter_tipi = st.radio(T["model_design"], ["AI Oluştursun", "Kendi Modelimi Yükle"])
            if karakter_tipi == "AI Oluştursun":
                 c1, c2 = st.columns(2)
                 with c1:
                     ethnic = st.selectbox("Köken", ["Avrupalı", "Asyalı", "Latin", "Afrikalı"])
                 with c2:
                     gender = st.selectbox("Cinsiyet", ["Kadın", "Erkek"])
            else:
                char_file = st.file_uploader("Model Fotoğrafı", type=['jpg', 'png'])

    st.markdown("---")
    arka_plan = st.selectbox(T["bg_label"], ["Stüdyo (Beyaz)", "Bej Minimal", "Doğa/Garden", "Lüks Salon", "Sokak/Street"])

    st.write("")
    if st.button(T["button_start"]):
        if urun_file:
            with st.spinner("By Ezgi Studios: Görüntüler İşleniyor..."):
                
                input_images = [Image.open(urun_file)]
                if char_file: input_images.append(Image.open(char_file))

                # --- PROMPT MANTIĞI ---
                
                # 1. AYAKKABI
                if is_shoes:
                    prompt_logic = f"""
                    TASK: Professional Shoe Photography.
                    Action: Place the shoe on a professional surface suitable for {arka_plan}.
                    Angles: Side profile, Top view, Back detail, Angled.
                    NO FACES. Product Focus only.
                    """
                
                # 2. SADECE AKSESUAR (KATI KORUMA)
                elif "Aksesuar" in sektor or "Accessories" in sektor:
                     if karakter_tipi == "AI Oluştursun":
                        target_model = f"{ethnic} kökenli, {gender} model."
                     else:
                        target_model = "Referans görseldeki kişinin kimliğini koru."

                     prompt_logic = f"""
                     GÖREV: Ultra-Gerçekçi Ürün Yerleştirme.
                     MODEL: {target_model}
                     [KRİTİK: AKSESUAR KORUMA]
                     Referans görseldeki takıyı (Kolye/Saat/Küpe) al ve modelin üzerine yerleştir.
                     KURALLAR:
                     1. GEOMETRİ KİLİDİ: Ürünün şeklini, boyutunu ASLA değiştirme.
                     2. DOKU KİLİDİ: Metal rengi ve taşlar %100 aynı kalmalı.
                     3. YARATICILIK YASAK: Olduğu gibi kopyala.
                     SAHNE: {arka_plan}. ODAK: Close-up.
                     """

                # 3. GELİNLİK/ABİYE (KIYAFET KORUMALI)
                else:
                    if karakter_tipi == "AI Oluştursun":
                        target_model = f"{ethnic} kökenli {gender} model."
                    else:
                        target_model = "Referans görseldeki kişinin yüzünü koru."

                    prompt_logic = f"""
                    GÖREV: {target_model} referans kıyafeti giyiyor.
                    [1. KIYAFET KİLİDİ]
                    Kumaş dokusu, desen, dikişler, iplik izleri, boncuklar %100 aynı kalıyor.
                    [2. AKSESUAR KİLİDİ]
                    Modelin üzerindeki mevcut aksesuarlara (Taç, Duvak, Kolye) dokunma, çıkarma veya değiştirme.
                    SAHNE: {arka_plan}
                    """

                # API Çağrısı
                response = model.generate_content([prompt_logic] + input_images)
                
                # Demo Sonuçlar
                st.session_state.generated_images = [
                    "https://via.placeholder.com/600x800?text=By+Ezgi+Poz+1",
                    "https://via.placeholder.com/600x800?text=By+Ezgi+Poz+2",
                    "https://via.placeholder.com/600x800?text=By+Ezgi+Poz+3",
                    "https://via.placeholder.com/600x800?text=By+Ezgi+Poz+4"
                ]
                st.success("Çekim Tamamlandı! Aşağıdan Video Prodüksiyonuna geçebilirsiniz.")

# --- VİDEO BÖLÜMÜ ---
if st.session_state.generated_images:
    st.markdown("---")
    st.markdown(f"<h2 style='text-align: center; color: #2E8B57;'>{T['vid_title']}</h2>", unsafe_allow_html=True)
    
    cols = st.columns(4)
    for i, img in enumerate(st.session_state.generated_images):
        with cols[i]:
            st.image(img, caption=f"Poz {i+1}")

    st.write("")
    
    video_container = st.container()
    with video_container:
        v1, v2 = st.columns([1, 1])
        
        with v1:
            st.info("1. Ayarlar / Settings")
            selected_index = st.selectbox(T["vid_select"], range(1, len(st.session_state.generated_images)+1))
            source_image = st.session_state.generated_images[selected_index-1]
            
            preset_motion = st.selectbox(T["vid_motion_label"], T["motions"])
            custom_text = st.text_area(T["vid_custom_label"], placeholder=T["vid_custom_placeholder"])

        with v2:
            st.info("2. Motor / Action")
            
            lighting_guard = "CRITICAL: DO NOT add extra lights. Preserve source lighting 100%. No brightening filters."
            
            if st.button(T["btn_preset"]):
                with st.spinner("By Ezgi Studios: Video Render Alınıyor..."):
                    final_video_prompt = f"Action: {preset_motion}. {lighting_guard}"
                    time.sleep(3)
                    st.success(f"{T['vid_success']}")
                    st.video("https://www.w3schools.com/html/mov_bbb.mp4")
            
            st.write("")
            
            if st.button(T["btn_custom"]):
                if custom_text:
                    with st.spinner("By Ezgi Studios: Özel Video İşleniyor..."):
                        final_video_prompt = f"Action: {custom_text}. {lighting_guard}"
                        time.sleep(3)
                        st.success(f"{T['vid_success']}")
                        st.video("https://www.w3schools.com/html/mov_bbb.mp4")
                else:
                    st.warning("Lütfen bir talimat yazınız.")