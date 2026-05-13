import streamlit as st
import json

st.title("🔍 Sınıf Arama ve Filtreleme")

st.sidebar.header("Filtreleme Seçenekleri")
bina = st.sidebar.selectbox("Bina Seçin", ["Hepsi", "EEB"])
min_kapasite = st.sidebar.number_input("Minimum Kapasite (Kişi)", min_value=0, value=30)
projektor = st.sidebar.checkbox("Projektör Olsun mu?")

with open("data/classrooms.json", "r", encoding="utf-8") as f:
    classrooms = json.load(f)

filtered_rooms = []
for room in classrooms:
    if bina != "Hepsi" and room["building"] != bina:
        continue
    if room["capacity"] < min_kapasite:
        continue
    if projektor and not room["has_projector"]:
        continue
    filtered_rooms.append(room)

st.write(f"İTÜ kampüsünde kriterlerinize uygun **{len(filtered_rooms)}** sınıf bulundu.")
st.dataframe(filtered_rooms)
