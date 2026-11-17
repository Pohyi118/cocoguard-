
def drone_hum(dur):
    n = int(dur * SR); t = tt(n); f = 205 + 6 * np.sin(2 * np.pi * 0.7 * t)
    ph = 2 * np.pi * np.cumsum(f) / SR
    y = 0.6 * np.sin(ph) + 0.35 * np.sin(2 * ph + 0.3) + 0.2 * np.sin(3 * ph + 1.1) + 0.25 * shaped(n, 2500, 7000)
    return y * (0.75 + 0.25 * np.sin(2 * np.pi * 31 * t)) * np.minimum(sm(t / 0.4), 1 - sm((t - dur + 0.5) / 0.5))
def drip(f=1300):
    n = int(0.35 * SR); t = tt(n); fr = f * (1 + 0.8 * np.exp(-t / 0.02))
    return np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-t / 0.07)
def click():
    n = int(0.06 * SR); t = tt(n)
    return 0.7 * shaped(n, 1500, 8000) * np.exp(-t / 0.004) + 0.5 * np.sin(2 * np.pi * 180 * t) * np.exp(-t / 0.02)
def shutter():
    a = click(); y = np.zeros(int(0.25 * SR)); y[:len(a)] += a; i = int(0.09 * SR); y[i:i + len(a)] += 0.8 * a; return y

