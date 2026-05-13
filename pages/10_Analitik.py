import streamlit as st
import json
from datetime import date, datetime
from collections import Counter

st.set_page_config(page_title="Analitik - ClubSpace ITU", page_icon="📊", layout="wide")

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Bu sayfayi gormek icin giris yapmaniz gerekiyor.")
    st.stop()

if "reservations" not in st.session_state:
    with open("data/reservations.json", "r", encoding="utf-8") as f:
        st.session_state.reservations = json.load(f)

with open("data/clubs.json", "r", encoding="utf-8") as f:
    clubs = json.load(f)
with open("data/classrooms.json", "r", encoding="utf-8") as f:
    classrooms = json.load(f)

role_labels = {"club_admin": "Kulup Yoneticisi", "advisor": "Danisman", "coordinator": "Koordinator", "building_mgr": "Bina Sorumlusu", "student": "Ogrenci"}

with st.sidebar:
    st.markdown(f"### 👤 {st.session_state.user_name}")
    st.caption(role_labels.get(st.session_state.user_role, ""))
    st.divider()
    if st.button("Cikis Yap", use_container_width=True):
        st.session_state.logged_in = False
        st.rerun()

st.title("📊 Analitik Dashboard")
st.caption("Kampüs geneli etkinlik ve rezervasyon istatistikleri.")
st.divider()

reservations = st.session_state.reservations

# Genel istatistikler
toplam = len(reservations)
onaylanan = len([r for r in reservations if r["status"] == "approved"])
bekleyen = len([r for r in reservations if r["status"] == "pending"])
reddedilen = len([r for r in reservations if r["status"] == "rejected"])
onay_orani = round((onaylanan / toplam * 100) if toplam > 0 else 0, 1)

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Toplam Rezervasyon", toplam)
col2.metric("Onaylanan", onaylanan, delta=f"+{onaylanan}")
col3.metric("Bekleyen", bekleyen)
col4.metric("Reddedilen", reddedilen)
col5.metric("Onay Oranı", f"%{onay_orani}")

st.divider()

col_left, col_right = st.columns(2)

with col_left:
    st.subheader("🏆 En Aktif Kulüpler")
    kulup_sayac = Counter([r.get("club_id", 0) for r in reservations])
    kulup_listesi = []
    for club_id, sayi in kulup_sayac.most_common(10):
        kulup = next((c for c in clubs if c["id"] == club_id), None)
        if kulup:
            kulup_listesi.append({"Kulüp": kulup["name"], "Etkinlik": sayi})

    if kulup_listesi:
        for i, k in enumerate(kulup_listesi[:5], 1):
            medal = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣"][i-1]
            col_a, col_b = st.columns([4, 1])
            col_a.markdown(f"{medal} {k['Kulüp']}")
            col_b.markdown(f"**{k['Etkinlik']}**")

with col_right:
    st.subheader("🏛️ En Çok Kullanılan Sınıflar")
    sinif_sayac = Counter([r.get("classroom_id", 0) for r in reservations if r["status"] == "approved"])
    for i, (sinif_id, sayi) in enumerate(sinif_sayac.most_common(5), 1):
        sinif = next((c for c in classrooms if c["id"] == sinif_id), None)
        if sinif:
            medal = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣"][i-1]
            col_a, col_b = st.columns([4, 1])
            col_a.markdown(f"{medal} {sinif['building']} {sinif['room_no']}")
            col_b.markdown(f"**{sayi}**")

st.divider()

col_left2, col_right2 = st.columns(2)

with col_left2:
    st.subheader("📅 Aylık Etkinlik Dağılımı")
    ay_sayac = Counter()
    for r in reservations:
        if r["status"] == "approved":
            try:
                ay = r["event_date"][:7]
                ay_sayac[ay] += 1
            except Exception:
                pass
    for ay, sayi in sorted(ay_sayac.items()):
        bar = "█" * sayi
        st.markdown(f"**{ay}** — {bar} ({sayi})")

with col_right2:
    st.subheader("📋 Durum Dağılımı")
    durum_sayac = Counter([r["status"] for r in reservations])
    durum_labels = {
        "approved": "✅ Onaylanan",
        "pending": "🟡 Bekleyen",
        "rejected": "🔴 Reddedilen",
        "advisor_approved": "🔵 Danışman Onayı",
        "coord_approved": "🔵 Koordinatör Onayı",
        "cancelled": "⚫ İptal"
    }
    for durum, sayi in durum_sayac.most_common():
        label = durum_labels.get(durum, durum)
        yuzde = round(sayi / toplam * 100, 1) if toplam > 0 else 0
        col_a, col_b = st.columns([4, 1])
        col_a.markdown(f"{label}")
        col_b.markdown(f"**{sayi}** (%{yuzde})")

st.divider()

st.subheader("🏢 Bina Kullanım İstatistikleri")
bina_sayac = Counter()
for r in reservations:
    if r["status"] == "approved":
        sinif = next((c for c in classrooms if c["id"] == r.get("classroom_id")), None)
        if sinif:
            bina_sayac[sinif["building"]] += 1

cols = st.columns(4)
for i, (bina, sayi) in enumerate(bina_sayac.most_common(8)):
    with cols[i % 4]:
        with st.container(border=True):
            st.markdown(f"**{bina}**")
            st.metric("Etkinlik", sayi)
