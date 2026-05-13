import streamlit as st
import json
from datetime import date, time

st.set_page_config(page_title="Rezervasyon - ClubSpace ITU", page_icon="📅", layout="wide")

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Bu sayfayi gormek icin giris yapmaniz gerekiyor.")
    st.stop()

if st.session_state.user_role not in ["club_admin"]:
    st.error("Bu sayfaya sadece Kulup Yoneticileri erisebilir.")
    st.stop()

with open("data/classrooms.json", "r", encoding="utf-8") as f:
    classrooms = json.load(f)

# Session'da rezervasyon listesi yoksa JSON'dan yukle
if "reservations" not in st.session_state:
    with open("data/reservations.json", "r", encoding="utf-8") as f:
        st.session_state.reservations = json.load(f)

role_labels = {"club_admin": "Kulup Yoneticisi", "advisor": "Danisman", "coordinator": "Koordinator", "building_mgr": "Bina Sorumlusu", "student": "Ogrenci"}

with st.sidebar:
    st.markdown(f"### 👤 {st.session_state.user_name}")
    st.caption(role_labels.get(st.session_state.user_role, ""))
    if st.session_state.get("user_club"):
        st.caption(f"🏢 {st.session_state.user_club}")
    st.divider()
    if st.button("Cikis Yap", use_container_width=True):
        st.session_state.logged_in = False
        st.rerun()

st.title("📅 Yeni Rezervasyon Talebi")
st.caption("Etkinliginiz icin derslik rezervasyon formunu doldurun.")
st.divider()

st.info("📌 Onay Sureci: **Kulup** → **Danisman** → **Koordinator** → **Bina Sorumlusu** → ✅ Onaylandi")
st.divider()

secilen = st.session_state.get("secilen_sinif", "")

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Etkinlik Bilgileri")
    event_title = st.text_input("Etkinlik Adi *", placeholder="Ornek: Robot Gunleri Workshop")
    event_description = st.text_area("Etkinlik Aciklamasi", placeholder="Etkinlik hakkinda kisa bilgi verin...")
    expected_attendees = st.number_input("Tahmini Katilimci Sayisi *", min_value=1, value=30, step=5)

    st.subheader("Tarih ve Saat")
    event_date = st.date_input("Etkinlik Tarihi *", min_value=date.today())
    col_s, col_e = st.columns(2)
    with col_s:
        start_time = st.time_input("Baslangic Saati *", value=time(10, 0))
    with col_e:
        end_time = st.time_input("Bitis Saati *", value=time(12, 0))

    st.subheader("Sinif Secimi")
    sinif_listesi = [f"{r['building']} - {r['room_no']} (Kapasite: {r['capacity']})" for r in classrooms]
    default_idx = 0
    if secilen:
        for i, s in enumerate(sinif_listesi):
            if secilen in s:
                default_idx = i
                break
    secilen_sinif_str = st.selectbox("Sinif Sec *", sinif_listesi, index=default_idx)
    gerekli_ekipman = st.multiselect("Gerekli Ekipman", ["Projektor", "Ses Sistemi", "Beyaz Tahta"])
    ek_not = st.text_area("Ek Notlar (opsiyonel)", placeholder="Varsa ozel isteklerinizi belirtin...")

with col2:
    st.subheader("📋 Ozet")
    with st.container(border=True):
        st.markdown(f"**Kulup:** {st.session_state.get('user_club', 'Belirtilmedi')}")
        st.markdown(f"**Etkinlik:** {event_title if event_title else '—'}")
        st.markdown(f"**Tarih:** {event_date}")
        st.markdown(f"**Saat:** {start_time} - {end_time}")
        st.markdown(f"**Katilimci:** {expected_attendees} kisi")
        st.markdown(f"**Sinif:** {secilen_sinif_str.split(' (')[0]}")
        if gerekli_ekipman:
            st.markdown(f"**Ekipman:** {', '.join(gerekli_ekipman)}")

    st.divider()

    if st.button("📨 Talebi Gonder", type="primary", use_container_width=True):
        if not event_title:
            st.error("Etkinlik adi zorunludur!")
        elif start_time >= end_time:
            st.error("Bitis saati baslangic saatinden sonra olmalidir!")
        else:
            # Sinif ID bul
            sinif_building = secilen_sinif_str.split(" - ")[0]
            sinif_room = secilen_sinif_str.split(" - ")[1].split(" (")[0]
            sinif = next((c for c in classrooms if c["building"] == sinif_building and c["room_no"] == sinif_room), None)
            sinif_id = sinif["id"] if sinif else 1

            # Yeni rezervasyon olustur
            yeni_id = max([r["id"] for r in st.session_state.reservations], default=0) + 1
            yeni_rezervasyon = {
                "id": yeni_id,
                "club_id": 1,
                "classroom_id": sinif_id,
                "requested_by": st.session_state.user_name,
                "event_title": event_title,
                "event_date": str(event_date),
                "start_time": str(start_time)[:5],
                "end_time": str(end_time)[:5],
                "expected_attendees": expected_attendees,
                "status": "pending",
                "created_at": str(date.today())
            }

            # Session state'e ekle
            st.session_state.reservations.append(yeni_rezervasyon)

            st.success(f"✅ '{event_title}' talebiniz basariyla olusturuldu!")
            st.info("**Durum:** Onay Bekliyor (pending)\n\nDanismaniniz onay icin bilgilendirildi.")
            st.balloons()

            if "secilen_sinif" in st.session_state:
                del st.session_state["secilen_sinif"]
