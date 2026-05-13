import streamlit as st
import json
import os
import time
from dotenv import load_dotenv

st.set_page_config(page_title="AI Sinif Onerisi - ClubSpace ITU", page_icon="🤖", layout="wide")

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Bu sayfayi gormek icin giris yapmaniz gerekiyor.")
    st.stop()

load_dotenv()
api_key = os.getenv("GOOGLE_AI_KEY")

role_labels = {
    "club_admin": "Kulup Yoneticisi",
    "advisor": "Danisman",
    "coordinator": "Koordinator",
    "building_mgr": "Bina Sorumlusu",
    "student": "Ogrenci"
}

with st.sidebar:
    st.markdown(f"### 👤 {st.session_state.user_name}")
    st.caption(role_labels.get(st.session_state.user_role, ""))
    st.divider()
    if st.button("Cikis Yap", use_container_width=True):
        st.session_state.logged_in = False
        st.rerun()

st.title("🤖 Akilli Sinif Onerisi")
st.caption("Etkinlik bilgilerinizi girin, AI size en uygun siniflari onerir.")
st.divider()

with open("data/classrooms.json", "r", encoding="utf-8") as f:
    classrooms = json.load(f)

def akilli_oneri(katilimci, tercih_bina, ekipman_ihtiyac, etkinlik_turu):
    skorlar = []
    for c in classrooms:
        skor = 0

        # 1. Kapasite skoru (max 35 puan)
        kapasite_fark = c["capacity"] - katilimci
        if kapasite_fark < 0:
            continue  # Yetersiz kapasite, elendi
        elif kapasite_fark == 0:
            skor += 35
        elif kapasite_fark <= 10:
            skor += 33
        elif kapasite_fark <= 20:
            skor += 30
        elif kapasite_fark <= 40:
            skor += 24
        elif kapasite_fark <= 80:
            skor += 16
        elif kapasite_fark <= 150:
            skor += 9
        else:
            skor += 3

        # 2. Ekipman skoru (max 30 puan)
        ekipman_puan = 0
        ekipman_toplam = len(ekipman_ihtiyac)
        if ekipman_toplam > 0:
            if "Projektor" in ekipman_ihtiyac:
                ekipman_puan += 12 if c["has_projector"] else -10
            if "Ses Sistemi" in ekipman_ihtiyac:
                ekipman_puan += 12 if c["has_sound_system"] else -10
            if "Beyaz Tahta" in ekipman_ihtiyac:
                ekipman_puan += 6 if c["has_whiteboard"] else -4
        else:
            # Ekipman istenmemis, var olan ekipman hafif bonus
            if c["has_projector"]: ekipman_puan += 4
            if c["has_sound_system"]: ekipman_puan += 3
            if c["has_whiteboard"]: ekipman_puan += 2
        skor += ekipman_puan

        # 3. Bina tercihi skoru (max 20 puan)
        if tercih_bina != "Fark Etmez":
            if c["building"] == tercih_bina:
                skor += 20
            else:
                skor += 0
        else:
            skor += 10  # Fark etmez ise orta puan

        # 4. Kat skoru (max 8 puan) - erisim kolayligi
        if c["floor"] == 0:
            skor += 8
        elif c["floor"] == 1:
            skor += 7
        elif c["floor"] == 2:
            skor += 5
        elif c["floor"] == 3:
            skor += 3
        else:
            skor += 1

        # 5. Etkinlik turune gore bonus (max 7 puan)
        if etkinlik_turu in ["Konser / Gosteri"] and c["has_sound_system"]:
            skor += 7
        elif etkinlik_turu in ["Workshop / Egitim", "Konferans / Seminer"] and c["has_projector"]:
            skor += 5
        elif etkinlik_turu == "Toplanti" and c["capacity"] <= katilimci + 30:
            skor += 4
        elif etkinlik_turu == "Genel Kurul" and c["capacity"] >= katilimci:
            skor += 3

        skorlar.append((skor, c))

    skorlar.sort(key=lambda x: x[0], reverse=True)
    return skorlar[:3]

def oneri_metni_olustur(skor, sinif, katilimci, ekipman_ihtiyac):
    ekipman = []
    if sinif["has_projector"]: ekipman.append("projektor")
    if sinif["has_sound_system"]: ekipman.append("ses sistemi")
    if sinif["has_whiteboard"]: ekipman.append("beyaz tahta")

    kapasite_fark = sinif["capacity"] - katilimci
    if kapasite_fark == 0:
        kapasite_yorum = "Katilimci sayiniz icin tam kapasite."
    elif kapasite_fark <= 20:
        kapasite_yorum = "Katilimci sayiniz icin ideal kapasite."
    elif kapasite_fark <= 50:
        kapasite_yorum = "Katilimci sayiniz icin yeterli kapasite."
    else:
        kapasite_yorum = f"Katilimci sayinizdan {kapasite_fark} kisi fazla kapasiteli."

    eksik_ekipman = []
    if "Projektor" in ekipman_ihtiyac and not sinif["has_projector"]:
        eksik_ekipman.append("projektor")
    if "Ses Sistemi" in ekipman_ihtiyac and not sinif["has_sound_system"]:
        eksik_ekipman.append("ses sistemi")

    dezavantaj = ""
    if eksik_ekipman:
        dezavantaj = f"⚠️ **Dezavantaj:** {', '.join(eksik_ekipman)} bulunmuyor."

    return kapasite_yorum, ekipman, dezavantaj

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Etkinlik Bilgileri")
    etkinlik_turu = st.selectbox("Etkinlik Turu", [
        "Workshop / Egitim",
        "Konferans / Seminer",
        "Toplanti",
        "Konser / Gosteri",
        "Spor Etkinligi",
        "Sergi",
        "Genel Kurul",
        "Diger"
    ])
    katilimci = st.number_input("Tahmini Katilimci Sayisi", min_value=1, value=50, step=10)
    tercih_bina = st.selectbox(
        "Tercih Edilen Bina (opsiyonel)",
        ["Fark Etmez"] + sorted(list(set(c["building"] for c in classrooms)))
    )
    ekipman_ihtiyac = st.multiselect("Gerekli Ekipman", ["Projektor", "Ses Sistemi", "Beyaz Tahta"])
    ek_bilgi = st.text_area("Ek Bilgi (opsiyonel)", placeholder="Ornek: Sahne gerekiyor, karanlik ortam lazim...")

    if st.button("🤖 AI'dan Oneri Al", type="primary", use_container_width=True):
        with st.spinner("Siniflar analiz ediliyor..."):
            time.sleep(1.5)

            ai_basarili = False
            if api_key:
                try:
                    from google import genai
                    client = genai.Client(api_key=api_key)
                    sinif_ozet = []
                    for c in classrooms[:15]:
                        ekipman = []
                        if c["has_projector"]: ekipman.append("projektor")
                        if c["has_sound_system"]: ekipman.append("ses sistemi")
                        sinif_ozet.append(f"{c['building']} {c['room_no']} Kapasite:{c['capacity']} Ekipman:{','.join(ekipman) if ekipman else 'yok'}")
                    prompt = f"ITU sinif onerisi. Etkinlik:{etkinlik_turu}, {katilimci} kisi, Bina:{tercih_bina}, Ekipman:{', '.join(ekipman_ihtiyac) if ekipman_ihtiyac else 'yok'}. Siniflar:{chr(10).join(sinif_ozet)}. En uygun 3 sinifi oner, Turkce, kisa."
                    response = client.models.generate_content(model="gemini-2.0-flash-lite", contents=prompt)
                    st.session_state["ai_oneri"] = response.text
                    st.session_state["ai_mod"] = "gemini"
                    ai_basarili = True
                except Exception:
                    ai_basarili = False

            if not ai_basarili:
                oneriler = akilli_oneri(katilimci, tercih_bina, ekipman_ihtiyac, etkinlik_turu)
                if oneriler:
                    metin = f"**{etkinlik_turu}** etkinliginiz icin en uygun 3 sinif:\n\n"
                    for i, (skor, sinif) in enumerate(oneriler, 1):
                        kapasite_yorum, ekipman, dezavantaj = oneri_metni_olustur(skor, sinif, katilimci, ekipman_ihtiyac)
                        metin += f"### {i}. {sinif['building']} {sinif['room_no']} — {sinif['building_name']}\n"
                        metin += f"👥 Kapasite: **{sinif['capacity']} kisi** | 🏢 Kat: {sinif['floor']} | 🎯 Uygunluk: **{skor}/100**\n\n"
                        metin += f"✅ {kapasite_yorum}\n\n"
                        if ekipman:
                            metin += f"🛠️ Mevcut ekipman: {', '.join(ekipman)}\n\n"
                        if dezavantaj:
                            metin += f"{dezavantaj}\n\n"
                        metin += "---\n\n"
                    st.session_state["ai_oneri"] = metin
                    st.session_state["ai_mod"] = "algoritma"
                else:
                    st.session_state["ai_oneri"] = "Kriterlerinize uygun sinif bulunamadi. Filtreleri gevsetin."
                    st.session_state["ai_mod"] = "hata"

with col2:
    st.subheader("🎯 AI Onerisi")
    if "ai_oneri" in st.session_state and st.session_state["ai_oneri"]:
        if st.session_state.get("ai_mod") == "algoritma":
            st.caption("🔧 Akilli Oneri Algoritmasi ile olusturuldu")
        elif st.session_state.get("ai_mod") == "gemini":
            st.caption("✨ Google Gemini AI ile olusturuldu")
        st.markdown(st.session_state["ai_oneri"])
        st.divider()
        st.success("Rezervasyon icin 'Rezervasyon' sayfasina gidin.")
    else:
        st.info("Sol taraftaki formu doldurup 'AI'dan Oneri Al' butonuna basin.")
        st.markdown("""
        **Oneri sistemi nasil calisir?**
        - Kapasite uyumu: tam eslesme daha yuksek skor
        - Ekipman eslesmesi: gerekli ekipman varsa bonus
        - Bina tercihi: tercih edilen binaya oncelik
        - Kat erisimi: alt katlar daha yuksek skor
        - Etkinlik turu: konser icin ses sistemi, egitim icin projektor onceligi
        """)
