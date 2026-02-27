import numpy as np

def gaussian_envelope(t, t0, sigma, amplitude=1.0):
    return amplitude * np.exp(-(t - t0)**2 / (2 * sigma**2))

def gaussian_pulse(t, t0, sigma, omega, amplitude=1.0):
    envelope = gaussian_envelope(t, t0, sigma, amplitude)
    return envelope * np.cos(omega * t)

def drag_pulse(t, t0, sigma, omega, alpha, amplitude=1.0):
    envelope = gaussian_envelope(t, t0, sigma, amplitude)
    d_envelope = -(t - t0) / sigma**2 * envelope

    I = envelope * np.cos(omega * t)
    Q = -alpha * d_envelope * np.sin(omega * t)

    return I + Q

def gaussian_fft(signal, t):
    dt = t[1] - t[0]
    fft_signal = np.fft.fft(signal)
    freq = np.fft.fftfreq(len(signal), dt)
    return freq, fft_signal

def calculate_leakage(fft_signal, freq, target_freq_hz):
    bandwidth = 0.5e9  # 500 MHz
    mask = np.abs(freq - target_freq_hz) < bandwidth

    energy_target = np.sum(np.abs(fft_signal[mask])**2)
    energy_total = np.sum(np.abs(fft_signal)**2)

    return 1 - energy_target / energy_total

def analyze_drag_performance():
    t = np.linspace(0, 20e-9, 2000)
    t0 = 10e-9
    sigma = 2e-9

    f0 = 4e9
    omega = 2 * np.pi * f0
    alpha = 0.5

    gaussian = gaussian_pulse(t, t0, sigma, omega)
    drag = drag_pulse(t, t0, sigma, omega, alpha)

    freq, fft_gaussian = gaussian_fft(gaussian, t)
    _, fft_drag = gaussian_fft(drag, t)

    leakage_gaussian = calculate_leakage(fft_gaussian, freq, f0)
    leakage_drag = calculate_leakage(fft_drag, freq, f0)

    return leakage_gaussian, leakage_drag
