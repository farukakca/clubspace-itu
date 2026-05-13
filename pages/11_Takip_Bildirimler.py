import streamlit as st
import json

st.set_page_config(page_title="Takip & Bildirimler - ClubSpace ITU", page_icon="🔔", layout="wide")

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Bu sayfayi gormek icin giris yapmaniz gerekiyor.")
    st.stop()

with open("data/clubs.json", "r", encoding="utf-8") as f:
    clubs = json.load(f)

if "reservations" not in st.session_state:
    with open("data/reservations.json", "r", encoding="utf-8") as f:
        st.session_state.reservations = json.load(f)

if "takip_edilen" not in st.session_state:
    st.session_state.takip_edilen = set()

if "bildirimler" not in st.session_state:
    st.session_state.bildirimler = [
        {"mesaj": "ITU Robotik Kulubu yeni etkinlik olusturdu: Arduino Egitimi", "okundu": False, "tur": "yeni_etkinlik"},
        {"mesaj": "Bahar Konseri rezervasyonunuz danisman tarafindan onaylandi", "okundu": False, "tur": "onay"},
        {"mesaj": "Python Bootcamp etkinligi yarindan itibaren basliyor!", "okundu": True, "tur": "hatirlatma"},
    ]

role_labels = {"club_admin": "Kulup Yoneticisi", "advisor": "Danisman", "coordinator": "Koordinator", "building_mgr": "Bina Sorumlusu", "student": "Ogrenci"}

with st.sidebar:
    st.markdown(f"### 👤 {st.session_state.user_name}")
    st.caption(role_labels.get(st.session_state.user_role, ""))
    st.divider()
    okunmamis = len([b for b in st.session_state.bildirimler if not b["okundu"]])
    if okunmamis > 0:
        st.markdown(f"🔔 **{okunmamis} okunmamış bildirim**")
    if st.button("Cikis Yap", use_container_width=True):
        st.session_state.logged_in = False
        st.rerun()

st.title("🔔 Takip & Bildirimler")
st.divider()

tab1, tab2 = st.tabs(["🔔 Bildirimler", "➕ Kulüp Takip Et"])

with tab1:
    st.subheader("Bildirimlerim")

    okunmamis_sayisi = len([b for b in st.session_state.bildirimler if not b["okundu"]])
    col_a, col_b = st.columns([4, 1])
    col_a.markdown(f"**{okunmamis_sayisi}** okunmamış bildirim")
    with col_b:
        if st.button("Tümünü Okundu İşaretle", use_container_width=True):
            for b in st.session_state.bildirimler:
                b["okundu"] = True
            st.rerun()

    st.divider()

    tur_ikonlar = {
        "yeni_etkinlik": "🆕",
        "onay": "✅",
        "red": "❌",
        "hatirlatma": "⏰",
        "rezervasyon": "📅"
    }

    for i, bildirim in enumerate(reversed(st.session_state.bildirimler)):
        ikon = tur_ikonlar.get(bildirim["tur"], "🔔")
        bg = "" if bildirim["okundu"] else "**"
        bg_end = "" if bildirim["okundu"] else "**"

        with st.container(border=True):
            col1, col2 = st.columns([5, 1])
            col1.markdown(f"{ikon} {bg}{bildirim['mesaj']}{bg_end}")
            if not bildirim["okundu"]:
                col1.caption("🔵 Yeni")
            if col2.button("✓", key=f"oku_{i}", help="Okundu işaretle"):
                idx = len(st.session_state.bildirimler) - 1 - i
                st.session_state.bildirimler[idx]["okundu"] = True
                st.rerun()

with tab2:
    st.subheader("Kulüpleri Takip Et")
    st.caption("Takip ettiğiniz kulüplerin etkinliklerinden haberdar olun.")
    st.divider()

    arama = st.text_input("Kulüp Ara", placeholder="Kulüp adı yazın...")
    filtreli = [c for c in clubs if arama.lower() in c["name"].lower()] if arama else clubs

    cols = st.columns(3)
    for i, club in enumerate(filtreli[:15]):
        with cols[i % 3]:
            with st.container(border=True):
                takip_ediyor = club["id"] in st.session_state.takip_edilen
                st.markdown(f"**{club['name']}**")
                st.caption(f"📂 {club.get('category', 'Diger')}")

                if takip_ediyor:
                    if st.button("✅ Takip Ediliyor", key=f"takip_{club['id']}", use_container_width=True):
                        st.session_state.takip_edilen.discard(club["id"])
                        st.rerun()
                else:
                    if st.button("➕ Takip Et", key=f"takip_{club['id']}", use_container_width=True, type="primary"):
                        st.session_state.takip_edilen.add(club["id"])
                        yeni_bildirim = {
                            "mesaj": f"{club['name']} kulübünü takip etmeye başladınız!",
                            "okundu": False,
                            "tur": "yeni_etkinlik"
                        }
                        st.session_state.bildirimler.append(yeni_bildirim)
                        st.rerun()

    st.divider()
    st.subheader(f"Takip Ettiğim Kulüpler ({len(st.session_state.takip_edilen)})")
    if st.session_state.takip_edilen:
        for club_id in st.session_state.takip_edilen:
            kulup = next((c for c in clubs if c["id"] == club_id), None)
            if kulup:
                col1, col2 = st.columns([4, 1])
                col1.markdown(f"✅ **{kulup['name']}** — {kulup.get('category', '')}")
                if col2.button("Bırak", key=f"birak_{club_id}"):
                    st.session_state.takip_edilen.discard(club_id)
                    st.rerun()
    else:
        st.info("Henüz kulüp takip etmiyorsunuz.")
