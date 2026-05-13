import streamlit as st
import json

st.set_page_config(page_title="Etkinlik Puanlama - ClubSpace ITU", page_icon="⭐", layout="wide")

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Bu sayfayi gormek icin giris yapmaniz gerekiyor.")
    st.stop()

if "reservations" not in st.session_state:
    with open("data/reservations.json", "r", encoding="utf-8") as f:
        st.session_state.reservations = json.load(f)

if "ratings" not in st.session_state:
    st.session_state.ratings = {}

role_labels = {"club_admin": "Kulup Yoneticisi", "advisor": "Danisman", "coordinator": "Koordinator", "building_mgr": "Bina Sorumlusu", "student": "Ogrenci"}

with st.sidebar:
    st.markdown(f"### 👤 {st.session_state.user_name}")
    st.caption(role_labels.get(st.session_state.user_role, ""))
    st.divider()
    if st.button("Cikis Yap", use_container_width=True):
        st.session_state.logged_in = False
        st.rerun()

st.title("⭐ Etkinlik Puanlama")
st.caption("Katıldığınız etkinlikleri değerlendirin.")
st.divider()

# Onaylanan etkinlikler
onaylanan = [r for r in st.session_state.reservations if r["status"] == "approved"]

if not onaylanan:
    st.info("Henüz onaylanmış etkinlik bulunmuyor.")
else:
    st.markdown(f"**{len(onaylanan)}** etkinlik puanlanabilir.")
    st.divider()

    for r in onaylanan:
        rating_key = f"rating_{r['id']}"
        mevcut_puan = st.session_state.ratings.get(rating_key, {}).get("score", 0)
        mevcut_yorum = st.session_state.ratings.get(rating_key, {}).get("comment", "")

        with st.container(border=True):
            col1, col2 = st.columns([3, 2])
            with col1:
                st.markdown(f"### 🟢 {r['event_title']}")
                st.caption(f"📅 {r['event_date']} | ⏰ {r['start_time']}-{r['end_time']} | 👤 {r['requested_by']}")

            with col2:
                if mevcut_puan > 0:
                    yildiz = "⭐" * mevcut_puan
                    st.success(f"Puaniniz: {yildiz} ({mevcut_puan}/5)")
                    if mevcut_yorum:
                        st.caption(f"Yorumunuz: {mevcut_yorum}")
                else:
                    puan = st.select_slider(
                        "Puan Ver",
                        options=[1, 2, 3, 4, 5],
                        value=3,
                        key=f"slider_{r['id']}",
                        format_func=lambda x: "⭐" * x
                    )
                    yorum = st.text_input("Yorum (opsiyonel)", key=f"yorum_{r['id']}", placeholder="Etkinlik hakkinda ne dusunuyorsunuz?")

                    if st.button("Puanla", key=f"btn_{r['id']}", type="primary", use_container_width=True):
                        st.session_state.ratings[rating_key] = {
                            "score": puan,
                            "comment": yorum,
                            "user": st.session_state.user_name
                        }
                        st.rerun()

    st.divider()
    st.subheader("📊 Puan Özeti")
    if st.session_state.ratings:
        toplam = sum(v["score"] for v in st.session_state.ratings.values())
        ortalama = toplam / len(st.session_state.ratings)
        col1, col2, col3 = st.columns(3)
        col1.metric("Toplam Puanlanan", len(st.session_state.ratings))
        col2.metric("Ortalama Puan", f"{ortalama:.1f}/5")
        col3.metric("En Yüksek Puan", max(v["score"] for v in st.session_state.ratings.values()))
    else:
        st.info("Henüz puan verilmedi.")
