import streamlit as st

st.title("📊 Yönetim Paneli (Dashboard)")

col1, col2, col3 = st.columns(3)
col1.metric(label="Toplam Etkinlik", value="12")
col2.metric(label="Onay Bekleyen Rezervasyon", value="3")
col3.metric(label="Bu Ayki Aktif Kulüp", value="8")

st.write("---")
st.subheader("🔔 Son Bildirimler")
st.info("İTÜ Robotik Kulübü'nün rezervasyonu Danışman tarafından onaylandı.")
