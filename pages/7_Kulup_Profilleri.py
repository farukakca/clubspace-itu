import streamlit as st
import json

st.set_page_config(page_title="Kulüp Profilleri - ClubSpace ITU", page_icon="🏢", layout="wide")

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Bu sayfayi gormek icin giris yapmaniz gerekiyor.")
    st.stop()

with open("data/clubs.json", "r", encoding="utf-8") as f:
    clubs = json.load(f)

if "reservations" not in st.session_state:
    with open("data/reservations.json", "r", encoding="utf-8") as f:
        st.session_state.reservations = json.load(f)

role_labels = {"club_admin": "Kulup Yoneticisi", "advisor": "Danisman", "coordinator": "Koordinator", "building_mgr": "Bina Sorumlusu", "student": "Ogrenci"}

with st.sidebar:
    st.markdown(f"### 👤 {st.session_state.user_name}")
    st.caption(role_labels.get(st.session_state.user_role, ""))
    st.divider()
    kategori_filtre = st.selectbox("Kategori", ["Hepsi", "Uzmanlik", "Spor", "Kultur Sanat"])
    arama = st.text_input("Kulup Ara", placeholder="Kulup adi...")
    if st.button("Cikis Yap", use_container_width=True):
        st.session_state.logged_in = False
        st.rerun()

st.title("🏢 Kulüp Profilleri")
st.caption("ITU öğrenci kulüplerini keşfedin.")
st.divider()

# Filtrele
gosterilen = clubs
if kategori_filtre != "Hepsi":
    gosterilen = [c for c in gosterilen if c.get("category") == kategori_filtre]
if arama:
    gosterilen = [c for c in gosterilen if arama.lower() in c["name"].lower()]

st.markdown(f"**{len(gosterilen)}** kulüp listeleniyor.")
st.divider()

cols = st.columns(3)
for i, club in enumerate(gosterilen):
    with cols[i % 3]:
        # Bu kulubun etkinlik sayisi
        etkinlik_sayisi = len([r for r in st.session_state.reservations if r.get("club_id") == club["id"] and r["status"] == "approved"])

        with st.container(border=True):
            st.markdown(f"### 🏛️ {club['name']}")
            st.caption(f"📂 {club.get('category', 'Diger')}")

            if club.get("bio"):
                st.markdown(club["bio"])

            st.markdown(f"✅ **{etkinlik_sayisi}** onaylı etkinlik")

            col_a, col_b = st.columns(2)
            if club.get("instagram_url"):
                col_a.markdown(f"[📸 Instagram]({club['instagram_url']})")
            if club.get("whatsapp_url"):
                col_b.markdown(f"[💬 WhatsApp]({club['whatsapp_url']})")
