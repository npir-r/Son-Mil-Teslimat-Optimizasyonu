"""
Son-Mil Teslimat Optimizasyonu — Mini Vaka Çözümü
----------------------------------------------------
1) NetworkX ile tam bağlantılı (complete) mesafe grafiği kurar.
2) 'Mevcut durum' senaryosu: noktalar veri girildiği sırayla ziyaret edilir.
3) 'Optimize' senaryo: en yakın komşu (nearest neighbor) sezgiseliyle rota kurulur,
   ardından 2-opt ile küçük iyileştirmeler yapılır.
4) İki senaryoyu mesafe / süre / maliyet açısından karşılaştırır.
5) Sonucu tek bir PNG üzerinde görselleştirir.
"""

import math
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

from data_generator import DEPOT, DELIVERY_POINTS, ASSUMPTIONS

POINTS = [DEPOT] + DELIVERY_POINTS
NAMES = [p["name"] for p in POINTS]


def haversine_km(p1, p2):
    """İki koordinat arası kuş uçuşu mesafe (km)."""
    R = 6371.0
    lat1, lon1 = math.radians(p1["lat"]), math.radians(p1["lon"])
    lat2, lon2 = math.radians(p2["lat"]), math.radians(p2["lon"])
    dlat, dlon = lat2 - lat1, lon2 - lon1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    return 2 * R * math.asin(math.sqrt(a)) * 1.3  # +%30 kentsel yol düzeltme katsayısı


def build_graph():
    G = nx.complete_graph(len(POINTS))
    mapping = {i: POINTS[i]["name"] for i in range(len(POINTS))}
    G = nx.relabel_nodes(G, mapping)
    for i, p1 in enumerate(POINTS):
        for j, p2 in enumerate(POINTS):
            if i < j:
                d = haversine_km(p1, p2)
                G[p1["name"]][p2["name"]]["weight"] = d
    return G


def route_distance(G, route):
    return sum(G[route[i]][route[i + 1]]["weight"] for i in range(len(route) - 1))


def baseline_route(G):
    """Mevcut durum: veri girildiği sırayla, planlama yapılmadan ziyaret."""
    route = [DEPOT["name"]] + [p["name"] for p in DELIVERY_POINTS] + [DEPOT["name"]]
    return route


def nearest_neighbor_route(G):
    unvisited = set(p["name"] for p in DELIVERY_POINTS)
    route = [DEPOT["name"]]
    current = DEPOT["name"]
    while unvisited:
        nxt = min(unvisited, key=lambda n: G[current][n]["weight"])
        route.append(nxt)
        unvisited.remove(nxt)
        current = nxt
    route.append(DEPOT["name"])
    return route


def two_opt(G, route):
    """Basit 2-opt iyileştirmesi: kesişen rota segmentlerini düzeltir."""
    best = route[:]
    improved = True
    while improved:
        improved = False
        for i in range(1, len(best) - 2):
            for j in range(i + 1, len(best) - 1):
                new_route = best[:i] + best[i:j + 1][::-1] + best[j + 1:]
                if route_distance(G, new_route) < route_distance(G, best):
                    best = new_route
                    improved = True
    return best


def summarize(G, route, label):
    dist = route_distance(G, route)
    time_h = dist / ASSUMPTIONS["avg_speed_kmh"]
    cost = dist * ASSUMPTIONS["fuel_cost_per_km_tl"]
    print(f"\n--- {label} ---")
    print(" -> ".join(route))
    print(f"Toplam mesafe : {dist:.1f} km")
    print(f"Tahmini süre  : {time_h:.2f} saat ({time_h * 60:.0f} dk)")
    print(f"Tahmini maliyet: {cost:.0f} TL")
    return {"label": label, "distance_km": dist, "time_h": time_h, "cost_tl": cost, "route": route}


def plot_routes(base_route, opt_route, savepath):
    coord = {p["name"]: (p["lon"], p["lat"]) for p in POINTS}
    fig, axes = plt.subplots(1, 2, figsize=(13, 6))

    for ax, route, title, color in [
        (axes[0], base_route, "Mevcut Durum (Planlanmamış Sıra)", "#c0392b"),
        (axes[1], opt_route, "Optimize Rota (NN + 2-opt)", "#1f6f43"),
    ]:
        xs = [coord[n][0] for n in route]
        ys = [coord[n][1] for n in route]
        ax.plot(xs, ys, "-o", color=color, linewidth=1.8, markersize=5, zorder=2)
        depot_x, depot_y = coord[DEPOT["name"]]
        ax.scatter([depot_x], [depot_y], color="black", s=110, marker="s", zorder=3, label="Depo")
        for n in route:
            if n != DEPOT["name"]:
                x, y = coord[n]
                ax.annotate(n, (x, y), fontsize=7, xytext=(3, 3), textcoords="offset points")
        ax.set_title(title, fontsize=12, fontweight="bold")
        ax.set_xlabel("Boylam")
        ax.set_ylabel("Enlem")
        ax.legend(loc="lower right", fontsize=8)
        ax.grid(alpha=0.25)

    fig.suptitle("İstanbul Son-Mil Teslimat Ağı — Mevcut vs. Optimize Rota", fontsize=14, fontweight="bold")
    fig.tight_layout(rect=[0, 0, 1, 0.94])
    fig.savefig(savepath, dpi=150)
    print(f"\nGrafik kaydedildi: {savepath}")


if __name__ == "__main__":
    G = build_graph()

    base = baseline_route(G)
    nn = nearest_neighbor_route(G)
    opt = two_opt(G, nn)

    res_base = summarize(G, base, "Mevcut Durum (planlanmamış sıra)")
    res_nn = summarize(G, nn, "En Yakın Komşu (Nearest Neighbor)")
    res_opt = summarize(G, opt, "Optimize Rota (NN + 2-opt)")

    improvement_pct = (res_base["distance_km"] - res_opt["distance_km"]) / res_base["distance_km"] * 100
    time_saved_min = (res_base["time_h"] - res_opt["time_h"]) * 60
    cost_saved = res_base["cost_tl"] - res_opt["cost_tl"]

    print("\n=== KARŞILAŞTIRMA ÖZETİ ===")
    print(f"Mesafe azalışı : %{improvement_pct:.1f}")
    print(f"Süre kazancı   : {time_saved_min:.0f} dakika/tur")
    print(f"Maliyet kazancı: {cost_saved:.0f} TL/tur")

    # Sonuçları CSV'e kaydet
    summary_df = pd.DataFrame([res_base, res_nn, res_opt])[["label", "distance_km", "time_h", "cost_tl"]]
    summary_df.to_csv("output/route_comparison.csv", index=False, encoding="utf-8-sig")

    plot_routes(base, opt, "output/route_comparison.png")
