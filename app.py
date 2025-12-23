import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="By Ezgi - Bağlantı Testi", page_icon="🔧")

st.title("🔧 By Ezgi Studios - Bağlantı Testi")
st.write("Bu ekran, API Anahtarınızın hangi modelleri görebildiğini test etmek içindir.")

# API Key Girişi
api_key = st.text_input("Google AI API Key:", type="password")

if st.button("📡 Bağlantıyı ve Modelleri Test Et"):
    if not api_key:
        st.error("Lütfen önce API Anahtarı girin.")
    else:
        try:
            # Yapılandırma
            genai.configure(api_key=api_key)
            
            st.info(f"Kullanılan Kütüphane Versiyonu: {genai.__version__}")
            
            # Modelleri Listele
            st.write("🔍 Google Sunucularına Bağlanılıyor...")
            models = list(genai.list_models())
            
            if not models:
                st.error("❌ HATA: Bağlantı kuruldu ama HİÇBİR model bulunamadı! Bu API Anahtarı yetkisiz veya hatalı proje ayarları var.")
            else:
                st.success(f"✅ BAŞARILI! Toplam {len(models)} model bulundu.")
                st.write("Aşağıdaki model isimlerinden birini kullanabiliriz:")
                
                # Bulunan modelleri ekrana yazdır
                for m in models:
                    if 'generateContent' in m.supported_generation_methods:
                        st.code(m.name)
                        
        except Exception as e:
            st.error(f"💥 KRİTİK HATA: {e}")
            st.warning("Bu hata, API anahtarının geçersiz olduğunu veya kütüphanenin çok eski olduğunu gösterir.")
