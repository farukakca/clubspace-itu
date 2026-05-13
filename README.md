# 🏫 ClubSpace ITU

**ITU Öğrenci Kulübü Derslik Rezervasyon Platformu**

ClubSpace ITU, İstanbul Teknik Üniversitesi öğrenci kulüplerinin derslik rezervasyon sürecini dijitalleştiren bir web platformudur. Mevcut kağıt bazlı, çok adımlı onay sürecini tek bir platforma taşıyarak süreci hızlandırmayı, şeffaflaştırmayı ve kullanıcı deneyimini iyileştirmeyi hedefler.

---

## 🚀 Canlı Uygulama

**[clubspace-itu.streamlit.app](https://clubspace-itu.streamlit.app)**

---

## 📋 Özellikler

- 🔐 **ITU E-posta ile Giriş** — @itu.edu.tr uzantılı hesaplarla rol bazlı erişim
- 🔍 **Akıllı Sınıf Arama** — Bina, kapasite ve ekipman filtresiyle 140 derslik
- 📅 **Rezervasyon Formu** — Dijital başvuru ve otomatik onay akışı
- ✅ **Onay Paneli** — Danışman → Koordinatör → Bina Sorumlusu onay süreci
- 🤖 **AI Sınıf Önerisi** — Kapasite, ekipman, bina ve etkinlik türüne göre akıllı öneri
- 📆 **Etkinlik Takvimi** — Haftalık ve aylık etkinlik görünümü

---

## 🗂️ Proje Yapısı

```
clubspace-itu/
├── app.py                  # Ana uygulama - giriş sayfası
├── pages/
│   ├── 1_Dashboard.py      # Kullanıcı paneli
│   ├── 2_Sinif_Ara.py      # Sınıf arama ve filtreleme
│   ├── 3_Rezervasyon.py    # Rezervasyon formu
│   ├── 4_Onay_Paneli.py    # Onay yönetimi
│   ├── 5_AI_Oneri.py       # AI destekli sınıf önerisi
│   └── 6_Takvim.py         # Etkinlik takvimi
├── data/
│   ├── classrooms.json     # 140 ITU dersliği (EEB, MDB, MED, MEDB, MEDC, FEB, ISB)
│   ├── clubs.json          # 74 gerçek ITU kulübü
│   └── reservations.json   # Örnek rezervasyon verileri
├── requirements.txt
└── .env                    # API key (GitHub'a yüklenmez)
```

---

## 🧪 Test Hesapları

| Rol | E-posta | Şifre |
|-----|---------|-------|
| Kulüp Yöneticisi | kulup@itu.edu.tr | 1234 |
| Danışman | danisman@itu.edu.tr | 1234 |
| Koordinatör | koordinator@itu.edu.tr | 1234 |
| Bina Sorumlusu | bina@itu.edu.tr | 1234 |
| Öğrenci | ogrenci@itu.edu.tr | 1234 |

---

## ⚙️ Kurulum (Lokal)

```bash
# Repoyu klonla
git clone https://github.com/farukakca/clubspace-itu.git
cd clubspace-itu

# Bağımlılıkları yükle
pip3 install -r requirements.txt

# API key'i ayarla
echo "GOOGLE_AI_KEY=your_api_key_here" > .env

# Uygulamayı başlat
python3 -m streamlit run app.py
```

---

## 🛠️ Kullanılan Teknolojiler

- **Frontend/Backend:** Streamlit (Python)
- **AI Entegrasyonu:** Google Gemini API (google-genai)
- **Veri:** JSON mock veri (140 derslik, 74 kulüp)
- **Deployment:** Streamlit Community Cloud
- **Versiyon Kontrolü:** GitHub

---

## 👥 Ekip

**ISL 343E Management Information Systems — Grup 9**

| İsim | Takım | Görev |
|------|-------|-------|
| Ömer Faruk Yıldız | Takım A | Analiz & Diyagramlar |
| Yusuf Çalık | Takım A | Analiz & Diyagramlar |
| Oğuzhan Çal | Takım A | Analiz & Diyagramlar |
| Hakan Şeker | Takım B | Veritabanı & Tasarım |
| Yiğitkan Doğan | Takım B | Veritabanı & Tasarım |
| Mehmet Kartal | Takım B | Veritabanı & Tasarım |
| Alpkaan Çeliksüngü | Takım C | App & Rapor |
| Ömer Faruk Akça | Takım C | App & Rapor |
| Ahmet Hazineli | Takım C | App & Rapor |

---

## 📊 Veritabanı

Veritabanı şeması ve örnek veriler Takım B tarafından hazırlanmıştır:
- `schema.sql` — Tüm tablo tanımları
- `sample_data.sql` — Örnek veri
- `clubspace.db` — SQLite veritabanı dosyası

Uygulama şu an JSON mock veri kullanmaktadır. SQLite entegrasyonu için `sqlite3.connect("clubspace.db")` ile bağlantı kurulabilir.

---

## 📄 Lisans

Bu proje ISL 343E Management Information Systems dersi kapsamında geliştirilmiştir.
