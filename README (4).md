# İstanbul Son-Mil Teslimat Ağı Optimizasyonu

İstanbul'daki tek bir dağıtım merkezinden 18 ilçeye yapılan teslimatları modelleyen ve rota planlamasıyla elde edilebilecek mesafe/süre/maliyet kazancını hesaplayan bir lojistik optimizasyon projesi.

**Sonuç:** Planlanmamış rotaya kıyasla **%28,4 daha kısa mesafe**, tur başına **~3 saat 17 dakika** ve **287 TL** tasarruf potansiyeli.

![Route Comparison](output/route_comparison.png)

---

## 📌 Proje Özeti

Bir e-ticaret/lojistik operasyonunun Hadımköy'deki dağıtım merkezinden 18 farklı İstanbul ilçesine günlük teslimat yaptığı varsayımsal bir senaryo kurgulanmıştır. Mevcut durumda teslimat sırası herhangi bir planlamaya dayanmazken, bu projede **Nearest Neighbor** sezgiseli ve **2-opt** iyileştirmesiyle rota optimize edilmiş ve iki senaryo karşılaştırılmıştır.

Detaylı problem tanımı, yöntem, bulgular ve iş etkisi için: [`EXECUTIVE_SUMMARY.md`](EXECUTIVE_SUMMARY.md)

## 🗂️ Proje Yapısı

```
├── data_generator.py          # Depo + 18 teslimat noktası verisi ve varsayımlar
├── optimize_routes.py         # Graf modeli, optimizasyon, karşılaştırma, görselleştirme
├── EXECUTIVE_SUMMARY.md       # Vaka raporu (problem, yöntem, bulgular, öneri)
├── data/
│   └── points.csv             # Depo ve teslimat noktaları (koordinat + talep)
└── output/
    ├── route_comparison.csv   # Senaryoların sayısal karşılaştırması
    └── route_comparison.png   # Mevcut vs. optimize rota görselleştirmesi
```

## ⚙️ Yöntem

1. **Ağ modeli:** Depo ve teslimat noktaları arasında `NetworkX` ile tam bağlantılı bir graf kuruldu; kenar ağırlıkları Haversine formülü + %30 kentsel yol düzeltme katsayısıyla hesaplanan tahmini yol mesafesidir.
2. **Referans senaryo:** Noktaların herhangi bir optimizasyon yapılmadan, kayıt sırasına göre ziyaret edildiği rota.
3. **Optimizasyon:** Önce **Nearest Neighbor** sezgiseliyle başlangıç rotası kuruldu, ardından **2-opt** algoritmasıyla çapraz/verimsiz segmentler iyileştirildi.

## 📊 Sonuçlar

| Senaryo | Mesafe | Süre | Maliyet |
|---|---|---|---|
| Mevcut durum (plansız) | 288,8 km | 11 sa 33 dk | 1.011 TL |
| Optimize rota (NN + 2-opt) | 206,7 km | 8 sa 16 dk | 723 TL |
| **İyileşme** | **%28,4 ↓** | **~3 sa 17 dk ↓** | **287 TL ↓** |

## 🚀 Çalıştırma

```bash
pip install pandas networkx matplotlib
python data_generator.py      # verinin CSV'ye yazılması
python optimize_routes.py     # optimizasyon, karşılaştırma ve grafik üretimi
```

## 🛠️ Kullanılan Teknolojiler

Python · NetworkX · Pandas · Matplotlib

## ⚠️ Sınırlılıklar

- Gerçek operasyonel veri değil, makul varsayımlarla kurgulanmış bir senaryo kullanılmıştır.
- Trafik yoğunluğu, teslimat zaman pencereleri ve araç kapasite kısıtları basitleştirilmiştir.
- Tek araçlı senaryo üzerinden analiz yapılmıştır; çok araçlı filo optimizasyonu (VRP) kapsam dışıdır.

## 👤 Hazırlayan

**Nazlı Pirim** — Marmara Üniversitesi, Yönetim Bilişim Sistemleri
[LinkedIn](https://linkedin.com/in/nazlı-pirim-) · [GitHub](https://github.com/npir-r)
