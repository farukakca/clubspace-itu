import streamlit as st
import json

st.set_page_config(page_title="Onay Paneli - ClubSpace ITU", page_icon="📋", layout="wide")

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Bu sayfayi gormek icin giris yapmaniz gerekiyor.")
    st.stop()

if st.session_state.user_role not in ["advisor", "coordinator", "building_mgr"]:
    st.error("Bu sayfaya sadece Danisman, Koordinator ve Bina Sorumlusu erisebilir.")
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

role_filter = {
    "advisor": "pending",
    "coordinator": "advisor_approved",
    "building_mgr": "coord_approved"
}

with st.sidebar:
    st.markdown(f"### 👤 {st.session_state.user_name}")
    st.caption(role_labels.get(st.session_state.user_role, ""))
    st.divider()
    show_all = st.checkbox("Tum rezervasyonlari goster", value=False)
    if st.button("Cikis Yap", use_container_width=True):
        st.session_state.logged_in = False
        st.rerun()

st.title("📋 Onay Paneli")
st.caption(f"Rol: {role_labels.get(st.session_state.user_role, '')}")
st.divider()

st.info("📌 Onay Sureci: **Kulup** → **Danisman** → **Koordinator** → **Bina Sorumlusu** → ✅")
st.divider()

beklenen_status = role_filter.get(st.session_state.user_role, "pending")
gorunecek = reservations if show_all else [r for r in reservations if r["status"] == beklenen_status]

if not gorunecek:
    st.success("✅ Onay bekleyen talep yok!")
else:
    st.markdown(f"**{len(gorunecek)}** talep listeleniyor.")
    st.divider()

    for r in gorunecek:
        sinif = next((c for c in classrooms if c["id"] == r["classroom_id"]), None)
        sinif_str = f"{sinif['building']} - {sinif['room_no']}" if sinif else "Bilinmiyor"

        status_color = {
            "approved": "🟢", "pending": "🟡", "rejected": "🔴",
            "advisor_approved": "🔵", "coord_approved": "🔵", "cancelled": "⚫"
        }.get(r["status"], "⚪")

        with st.container(border=True):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"### {status_color} {r['event_title']}")
                st.markdown(f"**Talep Eden:** {r['requested_by']}")
                st.markdown(f"**Sinif:** {sinif_str} &nbsp;|&nbsp; **Tarih:** {r['event_date']} &nbsp;|&nbsp; **Saat:** {r['start_time']} - {r['end_time']}")
                st.markdown(f"**Katilimci:** {r['expected_attendees']} kisi &nbsp;|&nbsp; **Durum:** `{r['status']}`")
            with col2:
                st.markdown("**Karar Ver:**")
                yorum = st.text_input("Yorum", key=f"yorum_{r['id']}", placeholder="Opsiyonel not...")
                col_a, col_r = st.columns(2)
                with col_a:
                    if st.button("✅ Onayla", key=f"onayla_{r['id']}", use_container_width=True, type="primary"):
                        st.success(f"'{r['event_title']}' onaylandi!")
                with col_r:
                    if st.button("❌ Reddet", key=f"reddet_{r['id']}", use_container_width=True):
                        st.error(f"'{r['event_title']}' reddedildi.")
