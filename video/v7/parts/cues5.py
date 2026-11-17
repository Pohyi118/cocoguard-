
def at(t, sig, g, pan=0.0): add(SFX, t, sig, g, pan)
def sc(i, x): return S[i] + x
for k in (2, 5, 7): at(S[k] - 0.4, whoosh(0.8), 0.20, -0.2)           # act wipes
# ACT 1: thunder after each flash, loss count-up ticks, the 30-minute clock ticking, "?" pops
for f, seed, g in ((1.6, 0.3, 0.34), (3.4, 1.1, 0.26), (9.6, 1.9, 0.3)): at(f + 0.35, thunder(seed), g, -0.3 if f < 5 else 0.3)
for k in range(10): at(5.7 + 1.6 * (k / 10) ** 0.8, tick(), 0.06, -0.3)
at(7.4, pop(820), 0.08, -0.3)
for k in range(int(S[2] - S[1] - 1.0)): at(S[1] + 1.0 + k, tick(), 0.07 + 0.01 * (k % 2), 0.4)
for d in (3.0, 5.5, 9.8): at(S[1] + d, pop(560), 0.08, -0.4)
at(S[1] + 1.4, whoosh(0.5), 0.06, -0.4)
# ACT 2: cut to silence, a single ding, gauge count-up, activation hit, drone hum, drips, input checks, route draw, chime
at(S[2] + 0.05, bell(1760, 0.5), 0.10); at(S[2] + 0.2, sweep(2.6, 300, 1400), 0.05)
for k in range(12): at(S[2] + 0.5 + 2.2 * (k / 12) ** 0.9, tick(), 0.06, 0.3)
at(S[2] + 2.75, bell(1318, 0.4), 0.09, 0.4); at(S[2] + 2.9, bell(1760, 0.4), 0.08, 0.4)
at(S[2] + 5.0, thud(), 0.16); at(S[2] + 5.02, chime(74), 0.12)
at(S[3] + 0.8, drone_hum(2.6), 0.10, -0.1)
for uu, f in ((1.75, 1500), (2.3, 1300), (2.9, 1150)): at(S[3] + uu, drip(f), 0.11, -0.2)
for i in range(4): at(S[3] + 1.15 + 0.6 * i, pop(640 + 70 * i), 0.08, 0.5)
at(S[3] + 3.6, sweep(1.4, 400, 1300), 0.05, -0.2)
for n in range(1, 5): at(S[3] + 3.5 + n * 0.3, pop(700 + 80 * n), 0.07, -0.2)
at(S[3] + 4.95, chime(76), 0.08); at(S[3] + 6.0, whoosh(0.6), 0.08)
for rt in (10.2, 11.75, 12.9, 15.6): at(S[3] + 6.0 + rt - 6.5, click(), 0.12, 0.3)
at(S[3] + 6.0 + 11.8 - 6.5, sweep(0.5, 600, 1100), 0.04, 0.3); at(S[3] + 6.0 + 15.65 - 6.5, chime(76), 0.06)
# ACT 3: heartbeat under the race, lock-on finds, clock ticks, finish bell, phone shutter, lock sting
r0, r1 = sc(5, 1.0), sc(5, 9.6)
for k in range(int((r1 - r0) / 0.6)):
    at(r0 + k * 0.6, thud(), 0.07 + 0.02 * (k % 2), 0); at(r0 + k * 0.6 + 0.18, thud(), 0.045, 0)
for k in range(15): at(r0 + k * (r1 - r0) / 15, tick(), 0.045, 0.6)
for i, m in enumerate((1.75, 3.5, 5.25, 9.67, 12.33, 19.0, 26.5)): at(r0 + (r1 - r0) * m / 30, blip(1760 + 60 * (i % 3)), 0.09, 0.35)
for m in (4.0, 26.5): at(r0 + (r1 - r0) * m / 30 + 0.05, bell(784, 0.25), 0.06, -0.35)
at(r1 + 0.05, bell(523, 1.1), 0.08)
at(sc(6, 3.2), whoosh(0.5), 0.08, 0.6)
for d in (1.0, 1.95, 2.4, 3.25): at(sc(6, 3.2 + d), click(), 0.12, 0.6)
at(sc(6, 3.2 + 1.05), blip(1480), 0.08, 0.6); at(sc(6, 3.2 + 3.3), chime(79), 0.06, 0.6)
at(sc(6, 8.6), whoosh(0.5), 0.07)
for d in (1.3, 3.15): at(sc(6, 8.5 + d), click(), 0.12, 0.2); at(sc(6, 8.5 + d + 0.08), pop(880), 0.06, 0.2)
at(sc(6, 10.4), chime(79), 0.07)
# ACT 4: gentle whooshes, check-ins, match-cut whoosh, ask hit, closing chime
at(sc(7, 2.6), whoosh(0.5), 0.07, -0.3)
for i in range(3): at(sc(7, 3.1 + 0.9 * i), pop(700 + 50 * i), 0.07, -0.3)
at(sc(7, 8.0), whoosh(0.9), 0.10)
at(sc(8, 0.6), thud(), 0.14); at(sc(8, 0.62), chime(74), 0.10)
at(sc(8, 9.4), chime(74), 0.08); at(sc(8, 9.45), bell(587, 1.4), 0.06)

# ACT 2b: Field Node 3D beat: servo-like whir on the explode, clicks on reassembly, pops on callouts
at(S[4] + 0.2, whoosh(0.6), 0.07); at(S[4] + 1.8, sweep(1.6, 500, 1600), 0.05, 0.2)
for i, d in enumerate((1.8, 2.6, 3.4, 4.4)): at(S[4] + d, pop(700 + 70 * i), 0.07, 0.5)
at(S[4] + 5.6, click(), 0.12); at(S[4] + 6.1, click(), 0.12); at(S[4] + 6.3, chime(76), 0.06)
# v6: real-footage entries
at(S[2] + 6.0, whoosh(0.7), 0.09)                  # laptop arrives with the alert
at(S[4] + 7.0, whoosh(0.5), 0.07); at(S[4] + 8.1, click(), 0.12, 0.3)   # sensor node page, Exploded
at(S[5] + 10.0, whoosh(0.6), 0.08)                  # Compare screen
