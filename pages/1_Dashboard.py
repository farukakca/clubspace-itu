import streamlit as st
import json

st.set_page_config(page_title="Dashboard - ClubSpace ITU", page_icon="📊", layout="wide")

# Giris kontrolu
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Bu sayfayi gormek icin giris yapmaniz gerekiyor.")
    st.stop()

# Mock veri yukle
with open("data/reservations.json", "r", encoding="utf-8") as f:
    reservations = json.load(f)
with open("data/clubs.json", "r", encoding="utf-8") as f:
    clubs = json.load(f)

# Rol etiketi
role_labels = {
    "club_admin": "Kulup Yoneticisi",
    "advisor": "Danisman",
    "coordinator": "Koordinator",
    "building_mgr": "Bina Sorumlusu",
    "student": "Ogrenci"
}

# Sidebar kullanici bilgisi
with st.sidebar:
    st.markdown(f"### 👤 {st.session_state.user_name}")
    st.caption(role_labels.get(st.session_state.user_role, ""))
    if st.session_state.get("user_club"):
        st.caption(f"🏢 {st.session_state.user_club}")
    st.divider()
    if st.button("Cikis Yap", use_container_width=True):
        st.session_state.logged_in = False
        st.rerun()

st.title("📊 Dashboard")
st.caption(f"Hos geldiniz, {st.session_state.user_name}")
st.divider()

# Istatistikler
approved = [r for r in reservations if r["status"] == "approved"]
pending = [r for r in reservations if r["status"] == "pending"]
rejected = [r for r in reservations if r["status"] == "rejected"]

col1, col2, col3, col4 = st.columns(4)
col1.metric("Toplam Rezervasyon", len(reservations))
col2.metric("Onaylanan", len(approved), delta=f"+{len(approved)}")
col3.metric("Onay Bekleyen", len(pending))
col4.metric("Reddedilen", len(rejected))

st.divider()

# Role gore farkli icerik
if st.session_state.user_role == "club_admin":
    st.subheader("📋 Kulubunuzun Rezervasyonlari")
    club_reservations = [r for r in reservations if r.get("club_id") == 1]
    if club_reservations:
        for r in club_reservations:
            status_color = {"approved": "🟢", "pending": "🟡", "rejected": "🔴", "advisor_approved": "🔵", "coord_approved": "🔵"}.get(r["status"], "⚪")
            st.markdown(f"{status_color} **{r['event_title']}** — {r['event_date']} {r['start_time']}-{r['end_time']} | Durum: `{r['status']}`")
    else:
        st.info("Henuz rezervasyon bulunmuyor.")

elif st.session_state.user_role in ["advisor", "coordinator", "building_mgr"]:
    st.subheader("🔔 Onay Bekleyen Talepler")
    if pending:
        for r in pending:
            with st.container():
                st.markdown(f"🟡 **{r['event_title']}** — {r['event_date']} | Talep Eden: {r['requested_by']}")
    else:
        st.success("Onay bekleyen talep yok.")

else:
    st.subheader("📅 Yaklasan Onaylanan Etkinlikler")
    if approved:
        for r in approved:
            st.markdown(f"🟢 **{r['event_title']}** — {r['event_date']} {r['start_time']}-{r['end_time']}")
    else:
        st.info("Yaklasan etkinlik bulunamadi.")

st.divider()
st.subheader("🔔 Son Bildirimler")
st.info("ITU Robotik Kulubu'nun 'Arduino Egitimi' rezervasyonu onay bekliyor.")
st.info("IEEE Ogrenci Kolu'nun 'Teknik Seminer' etkinligi onaylandi.")
st.success("Python Bootcamp etkinligi basariyla tamamlandi.")
