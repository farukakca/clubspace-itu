import streamlit st

st.title("📋 Yönetici Onay Paneli")
st.write("Sistemdeki onay bekleyen aktif rezervasyon talepleri.")

st.info("**Talep Eden:** İTÜ Robotik Kulübü\n\n**Etkinlik:** Robot Günleri Hazırlığı\n\n**Sınıf:** EEB - 1101")

# Takım B'nin dökümanındaki resmi ENUM onay seviyeleri
onay_rolu = st.selectbox("Onay Yetkili Rolünüzü Seçin", ["advisor", "coordinator", "building_mgr"])
yorum = st.text_input("Onay/Ret Notu (Yorum ekleyin)")

col1, col2 = st.columns(2)
with col1:
    if st.button("👍 Onayla"):
        st.success(f"Talep {onay_rolu} seviyesinde ONAYLANDI. Bir sonraki aşamaya aktarılıyor.")
with col2:
    if st.button("👎 Reddet"):
        st.error(f"Talep {onay_rolu} tarafından REDDEDİLDİ. Kulübe bildirim gönderildi.")
