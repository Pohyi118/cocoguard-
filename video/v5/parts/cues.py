
def at(t, sig, g, pan=0.0): add(SFX, t, sig, g, pan)
def sc(i, x): return S[i] + x
for k in range(1, len(S) - 1): at(S[k] - 0.4, whoosh(0.8), 0.20, -0.2)          # brand wipe between scenes
# 1 hook: clock ticks, rain-gauge trigger chime, shot changes, pod labels
for k in range(8): at(1.0 + k * 0.25, tick(), 0.09, 0.2)
at(3.85, bell(988, 0.35), 0.10, 0.5); at(3.99, bell(1318, 0.35), 0.09, 0.5)
at(3.3, whoosh(0.5), 0.05); at(6.5, whoosh(0.5), 0.05)
at(sc(0, 7.2), pop(820), 0.09, -0.3); at(sc(0, 7.7), pop(560), 0.10, 0.3); at(sc(0, 7.72), thud(), 0.10, 0.3)
# 2 climate risk: three cards, count-ups, country chips
for c0 in (sc(1, 1.6), sc(1, 6.9), sc(1, 13.1)): at(c0, whoosh(0.45), 0.08, -0.4)
for k in range(10): at(sc(1, 1.85) + 1.5 * (k / 10) ** 0.8, tick(), 0.06, -0.4)
at(sc(1, 3.4), pop(820), 0.09, -0.4)
for k in range(3): at(sc(1, 7.3 + k * 0.5), pop(640 + 90 * k), 0.08, -0.3 + 0.2 * k)
for k in range(14): at(sc(1, 13.55) + 1.9 * (k / 14) ** 0.8, tick(), 0.06, -0.4)
at(sc(1, 15.5), pop(900), 0.09, -0.4)
# 3 market gap: axes, tool dots, empty corner, KokoShield lands
at(sc(2, 0.7), sweep(1.0, 400, 700), 0.05, 0.4)
for k, d in enumerate([2.0, 2.7, 3.4, 4.1, 4.8]): at(sc(2, d), pop(560 + 70 * k), 0.08, 0.5)
at(sc(2, 6.0), sweep(1.2, 900, 1600), 0.04, 0.6)
at(sc(2, 8.6), thud(), 0.16, 0.6); at(sc(2, 8.62), chime(74), 0.11, 0.6)
# 4 drone survey (two flights, standing water drips) + Field Node callouts
at(sc(3, 2.4), drone_hum(2.3), 0.10, -0.2); at(sc(3, 4.5), drone_hum(2.3), 0.10, 0.2)
at(sc(3, 4.5), bell(1175, 0.4), 0.07)
for d, f in ((5.33, 1500), (5.79, 1300), (6.22, 1150)): at(sc(3, d), drip(f), 0.12, -0.2)
at(sc(3, 6.65), chime(79), 0.06)
at(sc(3, 7.7), whoosh(0.5), 0.08)
for k in range(4): at(sc(3, 8.4 + 0.4 * k), pop(700 + 80 * k), 0.07, -0.3)
# 5 ranked route on the real app: two clicks, route changes, zoom, phone + print
at(sc(4, 0.2), whoosh(0.5), 0.08)
at(sc(4, 1.55), click(), 0.16); at(sc(4, 2.65), click(), 0.16); at(sc(4, 2.9), chime(76), 0.07)
at(sc(4, 3.7), whoosh(0.6), 0.06); at(sc(4, 7.0), whoosh(0.5), 0.08)
# 6 record and confirm: camera shutter, confirm dings, rule-out thud
at(sc(5, 0.4), whoosh(0.5), 0.08, 0.6); at(sc(5, 1.2), shutter(), 0.14, 0.6)
at(sc(5, 3.0), whoosh(0.5), 0.07)
at(sc(5, 4.6), click(), 0.12); at(sc(5, 4.62), bell(1318, 0.45), 0.10)
at(sc(5, 5.6), click(), 0.12); at(sc(5, 5.62), bell(1480, 0.45), 0.10)
at(sc(5, 6.6), click(), 0.12); at(sc(5, 6.62), thud(), 0.16)
at(sc(5, 7.4), chime(79), 0.06)
# 7 pilot race: start beeps, clock, finds, finish, misses, facts
r0, r1 = sc(6, 1.4), sc(6, 11.4)
at(r0 - 0.5, bell(660, 0.18), 0.08); at(r0, bell(880, 0.25), 0.09)
for k in range(15): at(r0 + k * (r1 - r0) / 15, tick(), 0.05, 0.6)
for m, pods in ((7, 3), (14, 2), (22, 1), (30, 1)):
    for p in range(pods): at(r0 + (r1 - r0) * m / 30 + p * 0.09, bell(1568 + 120 * p, 0.3), 0.08, -0.3)
for m in (8, 30): at(r0 + (r1 - r0) * m / 30 + 0.05, bell(784, 0.25), 0.07, -0.3)
at(r1 + 0.05, bell(523, 1.1), 0.08)
at(r1 + 0.15, buzz(), 0.09, -0.4); at(r1 + 0.4, buzz(), 0.08, -0.4)
at(sc(6, 12.0), whoosh(0.5), 0.08, 0.6)
for k in range(5): at(sc(6, 12.45 + 0.6 * k), pop(700 + 50 * k), 0.07, 0.6)
# 8 impact and market
at(sc(7, 0.9), whoosh(0.5), 0.08); at(sc(7, 5.6), whoosh(0.5), 0.08)
for k in range(3): at(sc(7, 6.0 + 1.6 * k), blip(1320), 0.03, -0.3); at(sc(7, 6.7 + 1.6 * k), blip(1480), 0.03, 0.3)
at(sc(7, 10.7), whoosh(0.45), 0.07)
for k in range(20): at(sc(7, 11.2) + 1.6 * k / 20, tick(), 0.05, -0.2)
for k in range(20): at(sc(7, 13.2) + 1.8 * k / 20, tick(), 0.05, 0.2)
at(sc(7, 15.1), chime(76), 0.07)
# 9 close + end card
at(sc(8, 0.65), chime(74), 0.09, -0.3)
at(END - 2.2, chime(74), 0.08); at(END - 2.15, bell(587, 1.4), 0.06)

