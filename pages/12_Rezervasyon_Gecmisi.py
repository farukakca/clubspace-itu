import streamlit as st
import json

st.set_page_config(page_title="Rezervasyon Geçmişi - ClubSpace ITU", page_icon="📜", layout="wide")

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Bu sayfayi gormek icin giris yapmaniz gerekiyor.")
    st.stop()

if "reservations" not in st.session_state:
    with open("data/reservations.json", "r", encoding="utf-8") as f:
        st.session_state.reservations = json.load(f)

with open("data/classrooms.json", "r", encoding="utf-8") as f:
    classrooms = json.load(f)

role_labels = {"club_admin": "Kulup Yoneticisi", "advisor": "Danisman", "coordinator": "Koordinator", "building_mgr": "Bina Sorumlusu", "student": "Ogrenci"}

with st.sidebar:
    st.markdown(f"### 👤 {st.session_state.user_name}")
    st.caption(role_labels.get(st.session_state.user_role, ""))
    st.divider()
    durum_filtre = st.selectbox("Durum Filtrele", ["Tümü", "Onaylanan", "Bekleyen", "Reddedilen"])
    if st.button("Cikis Yap", use_container_width=True):
        st.session_state.logged_in = False
        st.rerun()

st.title("📜 Rezervasyon Geçmişi")
st.caption("Tüm rezervasyon taleplerinin geçmişi.")
st.divider()

durum_map = {
    "Tümü": None,
    "Onaylanan": "approved",
    "Bekleyen": "pending",
    "Reddedilen": "rejected"
}

reservations = st.session_state.reservations
if durum_map[durum_filtre]:
    reservations = [r for r in reservations if r["status"] == durum_map[durum_filtre]]

reservations = sorted(reservations, key=lambda x: x["event_date"], reverse=True)

onaylanan = len([r for r in st.session_state.reservations if r["status"] == "approved"])
bekleyen = len([r for r in st.session_state.reservations if r["status"] == "pending"])
reddedilen = len([r for r in st.session_state.reservations if r["status"] == "rejected"])

col1, col2, col3, col4 = st.columns(4)
col1.metric("Toplam", len(st.session_state.reservations))
col2.metric("✅ Onaylanan", onaylanan)
col3.metric("🟡 Bekleyen", bekleyen)
col4.metric("🔴 Reddedilen", reddedilen)

st.divider()
st.markdown(f"**{len(reservations)}** rezervasyon listeleniyor.")
st.divider()

for r in reservations:
    sinif = next((c for c in classrooms if c["id"] == r["classroom_id"]), None)
    sinif_str = f"{sinif['building']} {sinif['room_no']}" if sinif else "?"

    durum_renk = {
        "approved": "🟢", "pending": "🟡", "rejected": "🔴",
        "advisor_approved": "🔵", "coord_approved": "🔵", "cancelled": "⚫"
    }.get(r["status"], "⚪")

    durum_aciklama = {
        "approved": "Onaylandı",
        "pending": "Onay Bekliyor",
        "rejected": "Reddedildi",
        "advisor_approved": "Danışman Onayladı",
        "coord_approved": "Koordinatör Onayladı",
        "cancelled": "İptal Edildi"
    }.get(r["status"], r["status"])

    with st.container(border=True):
        col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
        col1.markdown(f"{durum_renk} **{r['event_title']}**")
        col1.caption(f"👤 {r['requested_by']}")
        col2.markdown(f"📅 {r['event_date']}")
        col2.caption(f"⏰ {r['start_time']}-{r['end_time']}")
        col3.markdown(f"📍 {sinif_str}")
        col3.caption(f"👥 {r['expected_attendees']} kişi")
        col4.markdown(f"`{durum_aciklama}`")
