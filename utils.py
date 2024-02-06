from scipy.fft import rfft, rfftfreq
import matplotlib.pyplot as plt
import numpy as np

def normalize(s):
    return s / np.max(s)

def remove_dc(s):
    return s - np.mean(s)

def calc_real_fft(s, fd=1, w=np.zeros(0)):
    if len(w) != 0:
        s = s * w

    n = len(s)

    sf = rfft(s) * 2 / n
    xf = rfftfreq(n, 1 / fd)

    return xf, sf

def calc_real_fft_without_dc(s, fd, w=np.zeros(0)):
    s = s - np.mean(s)
    
    if len(w) != 0:
        s = s * w

    n = len(s)

    sf = rfft(s) * 2 / n
    xf = rfftfreq(n, 1 / fd)

    return xf, sf

def plot_real_fft(s, fd, w=np.zeros(0)):
    if len(w) != 0:
        s = s * w

    n = len(s)

    sf = rfft(s) * 2 / n
    xf = rfftfreq(n, 1 / fd)

    plt.yscale('symlog')
    plt.plot(xf, 20 * np.log10(np.abs(sf)))
    plt.grid()
    plt.show()

def generate_noise(len, power=1, r=1):
    # P = U^2 / R
    return np.random.normal(0, np.sqrt(power/r), len)