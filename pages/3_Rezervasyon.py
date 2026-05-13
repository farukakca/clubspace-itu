import streamlit as st

st.title("📅 Yeni Sınıf Rezervasyon Talebi")
st.write("Etkinliğiniz için rezervasyon formunu eksiksiz doldurun.")

# Takım B'nin Reservation tablosundaki resmi alan adları
event_title = st.text_input("Etkinlik Adı (event_title)")
event_description = st.text_area("Etkinlik Açıklaması (event_description)")
event_date = st.date_input("Etkinlik Tarihi (event_date)")
start_time = st.time_input("Başlangıç Saati (start_time)")
end_time = st.time_input("Bitiş Saati (end_time)")
expected_attendees = st.number_input("Tahmini Katılımcı Sayısı (expected_attendees)", min_value=1, value=10)

if st.button("Talebi Gönder"):
    if event_title:
        st.success(f"'{event_title}' talebiniz başarıyla oluşturuldu! Durumu: pending (Onay Bekliyor)")
        st.info("Süreç Başladı: Danışman Onayı -> Koordinatör Onayı -> Bina Sorumlusu Onayı")
    else:
        st.error("Lütfen etkinlik adını boş bırakmayın!")
