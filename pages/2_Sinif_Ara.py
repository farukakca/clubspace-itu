import streamlit as st
import json

st.set_page_config(page_title="Sinif Ara - ClubSpace ITU", page_icon="🔍", layout="wide")

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Bu sayfayi gormek icin giris yapmaniz gerekiyor.")
    st.stop()

with open("data/classrooms.json", "r", encoding="utf-8") as f:
    classrooms = json.load(f)

role_labels = {"club_admin": "Kulup Yoneticisi", "advisor": "Danisman", "coordinator": "Koordinator", "building_mgr": "Bina Sorumlusu", "student": "Ogrenci"}

with st.sidebar:
    st.markdown(f"### 👤 {st.session_state.user_name}")
    st.caption(role_labels.get(st.session_state.user_role, ""))
    st.divider()

    st.header("🔎 Filtreler")

    # Bina listesini JSON'dan dinamik al
    binalar = sorted(list(set(r["building"] for r in classrooms)))
    bina = st.selectbox("Bina", ["Hepsi"] + binalar)

    # Kampus filtresi
    kampusler = sorted(list(set(r["campus"] for r in classrooms)))
    kampus = st.selectbox("Kampus", ["Hepsi"] + kampusler)

    min_kapasite = st.number_input("Min. Kapasite (kisi)", min_value=0, value=0, step=10)
    max_kapasite = st.number_input("Max. Kapasite (kisi)", min_value=0, value=500, step=10)

    st.markdown("**Ekipman**")
    projektor = st.checkbox("Projektor")
    ses_sistemi = st.checkbox("Ses Sistemi")
    beyaz_tahta = st.checkbox("Beyaz Tahta")

    if st.button("Cikis Yap", use_container_width=True):
        st.session_state.logged_in = False
        st.rerun()

st.title("🔍 Sinif Arama")
st.caption("Kriterlerinize gore uygun siniflari filtreleyin.")
st.divider()

# Filtreleme
filtered = []
for room in classrooms:
    if bina != "Hepsi" and room["building"] != bina:
        continue
    if kampus != "Hepsi" and room["campus"] != kampus:
        continue
    if room["capacity"] < min_kapasite:
        continue
    if max_kapasite > 0 and room["capacity"] > max_kapasite:
        continue
    if projektor and not room["has_projector"]:
        continue
    if ses_sistemi and not room["has_sound_system"]:
        continue
    if beyaz_tahta and not room["has_whiteboard"]:
        continue
    filtered.append(room)

st.markdown(f"**{len(filtered)}** sinif bulundu.")
st.divider()

if not filtered:
    st.warning("Sectiginiz kriterlere uygun sinif bulunamadi. Filtreleri gevsetin.")
else:
    # Kart seklinde goster
    cols = st.columns(3)
    for i, room in enumerate(filtered):
        with cols[i % 3]:
            ekipman = []
            if room["has_projector"]: ekipman.append("📽️ Projektor")
            if room["has_sound_system"]: ekipman.append("🔊 Ses")
            if room["has_whiteboard"]: ekipman.append("📋 Tahta")

            with st.container(border=True):
                st.markdown(f"### 🏛️ {room['building']} - {room['room_no']}")
                st.caption(f"{room['building_name']} | {room['campus']} Kampusu")
                st.markdown(f"👥 **Kapasite:** {room['capacity']} kisi")
                st.markdown(f"🏢 **Kat:** {room['floor']}")
                st.markdown(f"🛠️ {' · '.join(ekipman) if ekipman else 'Ekipman bilgisi yok'}")
                if st.button("Rezervasyon Yap", key=f"res_{room['id']}", use_container_width=True):
                    st.session_state["secilen_sinif"] = f"{room['building']} - {room['room_no']}"
                    st.success(f"{room['building']} {room['room_no']} secildi! Rezervasyon sayfasina gidin.")
