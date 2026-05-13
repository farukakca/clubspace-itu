import streamlit as st
import json
from datetime import date

st.set_page_config(page_title="Sorun Bildir - ClubSpace ITU", page_icon="🔧", layout="wide")

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Bu sayfayi gormek icin giris yapmaniz gerekiyor.")
    st.stop()

with open("data/classrooms.json", "r", encoding="utf-8") as f:
    classrooms = json.load(f)

if "issues" not in st.session_state:
    st.session_state.issues = []

role_labels = {"club_admin": "Kulup Yoneticisi", "advisor": "Danisman", "coordinator": "Koordinator", "building_mgr": "Bina Sorumlusu", "student": "Ogrenci"}

with st.sidebar:
    st.markdown(f"### 👤 {st.session_state.user_name}")
    st.caption(role_labels.get(st.session_state.user_role, ""))
    st.divider()
    if st.button("Cikis Yap", use_container_width=True):
        st.session_state.logged_in = False
        st.rerun()

st.title("🔧 Sınıf Sorun Bildirimi")
st.caption("Sınıflarda karşılaştığınız sorunları teknik ekibe bildirin.")
st.divider()

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Sorun Bildir")

    sinif_listesi = [f"{c['building']} - {c['room_no']} ({c['building_name']})" for c in classrooms]
    secilen_sinif = st.selectbox("Sınıf Seç *", sinif_listesi)

    sorun_turu = st.selectbox("Sorun Türü *", [
        "Projektör arızası",
        "Ses sistemi arızası",
        "Temizlik sorunu",
        "Klima / Isıtma sorunu",
        "Beyaz tahta sorunu",
        "Ekipman eksikliği",
        "Diğer"
    ])

    aciklama = st.text_area("Açıklama *", placeholder="Sorunu detaylıca açıklayın...")
    oncelik = st.select_slider("Öncelik", options=["Düşük", "Orta", "Yüksek", "Acil"], value="Orta")

    if st.button("📨 Bildir", type="primary", use_container_width=True):
        if not aciklama:
            st.error("Açıklama zorunludur!")
        else:
            yeni_id = len(st.session_state.issues) + 1
            yeni_sorun = {
                "id": yeni_id,
                "classroom": secilen_sinif,
                "type": sorun_turu,
                "description": aciklama,
                "priority": oncelik,
                "reported_by": st.session_state.user_name,
                "status": "open",
                "reported_at": str(date.today())
            }
            st.session_state.issues.append(yeni_sorun)
            st.success("✅ Sorun bildiriminiz teknik ekibe iletildi!")
            st.balloons()

with col2:
    st.subheader("📋 Bildirilen Sorunlar")

    if not st.session_state.issues:
        st.info("Henüz bildirilmiş sorun yok.")
    else:
        for issue in sorted(st.session_state.issues, key=lambda x: x["id"], reverse=True):
            oncelik_renk = {"Dusuk": "⚪", "Orta": "🟡", "Yuksek": "🟠", "Acil": "🔴"}.get(issue["priority"], "⚪")
            durum_renk = {"open": "🔴", "in_progress": "🟡", "resolved": "🟢"}.get(issue["status"], "⚪")

            with st.container(border=True):
                st.markdown(f"**{durum_renk} #{issue['id']} — {issue['type']}**")
                st.caption(f"📍 {issue['classroom']}")
                st.caption(f"📝 {issue['description']}")
                st.caption(f"{oncelik_renk} Öncelik: {issue['priority']} | 👤 {issue['reported_by']} | 📅 {issue['reported_at']} | Durum: `{issue['status']}`")
