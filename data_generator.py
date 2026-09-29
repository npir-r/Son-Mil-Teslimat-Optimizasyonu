"""
Vaka Verisi Üretici — İstanbul Son-Mil Teslimat Ağı
-----------------------------------------------------
Depo: Hadımköy (Mars Logistics'in gerçek hub bölgelerinden biri)
Teslimat noktaları: İstanbul'un farklı ilçelerinden 18 nokta,
her biri yaklaşık koordinat ve varsayımsal günlük sipariş hacmiyle.
"""

import pandas as pd

# Depo (dağıtım merkezi) — Hadımköy
DEPOT = {"name": "Depo - Hadımköy", "lat": 41.1122, "lon": 28.6797, "demand": 0}

# 18 teslimat noktası (ilçe merkezine yakın yaklaşık koordinatlar)
DELIVERY_POINTS = [
    {"name": "Kadıköy",       "lat": 40.9906, "lon": 29.0274, "demand": 14},
    {"name": "Üsküdar",       "lat": 41.0225, "lon": 29.0150, "demand": 11},
    {"name": "Beşiktaş",      "lat": 41.0422, "lon": 29.0080, "demand": 9},
    {"name": "Şişli",         "lat": 41.0602, "lon": 28.9877, "demand": 16},
    {"name": "Bakırköy",      "lat": 40.9819, "lon": 28.8772, "demand": 10},
    {"name": "Maltepe",       "lat": 40.9354, "lon": 29.1305, "demand": 8},
    {"name": "Pendik",        "lat": 40.8776, "lon": 29.2339, "demand": 7},
    {"name": "Kartal",        "lat": 40.9053, "lon": 29.1899, "demand": 6},
    {"name": "Ümraniye",      "lat": 41.0165, "lon": 29.1247, "demand": 13},
    {"name": "Sarıyer",       "lat": 41.1670, "lon": 29.0563, "demand": 5},
    {"name": "Beylikdüzü",    "lat": 41.0016, "lon": 28.6403, "demand": 9},
    {"name": "Avcılar",       "lat": 40.9793, "lon": 28.7212, "demand": 8},
    {"name": "Bahçelievler",  "lat": 41.0022, "lon": 28.8589, "demand": 12},
    {"name": "Zeytinburnu",   "lat": 40.9950, "lon": 28.9020, "demand": 10},
    {"name": "Fatih",         "lat": 41.0192, "lon": 28.9494, "demand": 15},
    {"name": "Bağcılar",      "lat": 41.0390, "lon": 28.8565, "demand": 11},
    {"name": "Esenler",       "lat": 41.0446, "lon": 28.8797, "demand": 9},
    {"name": "Sultangazi",    "lat": 41.1075, "lon": 28.8676, "demand": 7},
]

# Varsayımlar (rapor için)
ASSUMPTIONS = {
    "avg_speed_kmh": 25,          # şehir içi ortalama hız
    "fuel_cost_per_km_tl": 3.5,   # km başına yakıt maliyeti
    "vehicle_capacity": 120,      # araç başına toplam kapasite (varsayımsal birim)
}

if __name__ == "__main__":
    df = pd.DataFrame([DEPOT] + DELIVERY_POINTS)
    df.to_csv("data/points.csv", index=False, encoding="utf-8-sig")
    print(df)
    print("\nToplam günlük talep:", df["demand"].sum())
    print("Varsayımlar:", ASSUMPTIONS)
