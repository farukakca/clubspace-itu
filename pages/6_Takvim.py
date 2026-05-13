import streamlit as st
import json
from datetime import datetime, date, timedelta

st.set_page_config(page_title="Etkinlik Takvimi - ClubSpace ITU", page_icon="📅", layout="wide")

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Bu sayfayi gormek icin giris yapmaniz gerekiyor.")
    st.stop()

with open("data/reservations.json", "r", encoding="utf-8") as f:
    reservations = json.load(f)
with open("data/classrooms.json", "r", encoding="utf-8") as f:
    classrooms = json.load(f)

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
    st.markdown("**Filtrele**")
    sadece_onaylananlar = st.checkbox("Sadece onaylananlar", value=True)
    if st.button("Cikis Yap", use_container_width=True):
        st.session_state.logged_in = False
        st.rerun()

st.title("📅 Etkinlik Takvimi")
st.caption("Kampusteki onaylanan etkinlikleri goruntuleyin.")
st.divider()

# Hafta secimi
bugun = date.today()
haftanin_pazartesi = bugun - timedelta(days=bugun.weekday())

col_prev, col_title, col_next = st.columns([1, 4, 1])
with col_prev:
    if st.button("◀ Onceki Hafta"):
        if "hafta_offset" not in st.session_state:
            st.session_state.hafta_offset = 0
        st.session_state.hafta_offset -= 1

with col_next:
    if st.button("Sonraki Hafta ▶"):
        if "hafta_offset" not in st.session_state:
            st.session_state.hafta_offset = 0
        st.session_state.hafta_offset += 1

if "hafta_offset" not in st.session_state:
    st.session_state.hafta_offset = 0

gosterilen_pazartesi = haftanin_pazartesi + timedelta(weeks=st.session_state.hafta_offset)
gosterilen_pazar = gosterilen_pazartesi + timedelta(days=6)

with col_title:
    st.markdown(f"### {gosterilen_pazartesi.strftime('%d %B %Y')} — {gosterilen_pazar.strftime('%d %B %Y')}")

st.divider()

# Gunler
gun_isimleri = ["Pazartesi", "Sali", "Carsamba", "Persembe", "Cuma", "Cumartesi", "Pazar"]
kolonlar = st.columns(7)

for i, (kolon, gun_ismi) in enumerate(zip(kolonlar, gun_isimleri)):
    gun_tarihi = gosterilen_pazartesi + timedelta(days=i)
    gun_str = gun_tarihi.strftime("%Y-%m-%d")

    # O gune ait etkinlikler
    gun_etkinlikleri = []
    for r in reservations:
        if r["event_date"] == gun_str:
            if sadece_onaylananlar and r["status"] != "approved":
                continue
            gun_etkinlikleri.append(r)

    with kolon:
        # Bugun vurgula
        if gun_tarihi == bugun:
            st.markdown(f"**🔵 {gun_ismi}**")
            st.markdown(f"**{gun_tarihi.strftime('%d/%m')}**")
        else:
            st.markdown(f"**{gun_ismi}**")
            st.markdown(f"{gun_tarihi.strftime('%d/%m')}")

        st.divider()

        if gun_etkinlikleri:
            for e in gun_etkinlikleri:
                sinif = next((c for c in classrooms if c["id"] == e["classroom_id"]), None)
                sinif_str = f"{sinif['building']} {sinif['room_no']}" if sinif else "?"

                durum_renk = {
                    "approved": "🟢",
                    "pending": "🟡",
                    "rejected": "🔴",
                    "advisor_approved": "🔵",
                    "coord_approved": "🔵"
                }.get(e["status"], "⚪")

                with st.container(border=True):
                    st.markdown(f"{durum_renk} **{e['event_title']}**")
                    st.caption(f"⏰ {e['start_time']}-{e['end_time']}")
                    st.caption(f"📍 {sinif_str}")
        else:
            st.caption("Etkinlik yok")

st.divider()

# Ay gorunumu - liste olarak
st.subheader("📋 Bu Ayki Tum Etkinlikler")

ay_etkinlikleri = []
for r in reservations:
    try:
        etkinlik_tarihi = datetime.strptime(r["event_date"], "%Y-%m-%d").date()
        if etkinlik_tarihi.month == bugun.month and etkinlik_tarihi.year == bugun.year:
            if sadece_onaylananlar and r["status"] != "approved":
                continue
            ay_etkinlikleri.append(r)
    except Exception:
        continue

ay_etkinlikleri.sort(key=lambda x: x["event_date"])

if ay_etkinlikleri:
    for r in ay_etkinlikleri:
        sinif = next((c for c in classrooms if c["id"] == r["classroom_id"]), None)
        sinif_str = f"{sinif['building']} {sinif['room_no']}" if sinif else "?"
        durum_renk = {"approved": "🟢", "pending": "🟡", "rejected": "🔴", "advisor_approved": "🔵", "coord_approved": "🔵"}.get(r["status"], "⚪")

        col1, col2, col3, col4 = st.columns([2, 3, 2, 2])
        col1.markdown(f"**{r['event_date']}**")
        col2.markdown(f"{durum_renk} {r['event_title']}")
        col3.markdown(f"📍 {sinif_str}")
        col4.markdown(f"⏰ {r['start_time']}-{r['end_time']}")
else:
    st.info("Bu ay icin etkinlik bulunamadi.")
