import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

# Parameters
s = 0.5e-3  # slit separation (m)
a = s / 4   # slit width (m)
L = 2.0     # screen distance (m)
lambda_ = 550e-9  # wavelength (m)

# Horizontal screen positions (in meters)
y = np.linspace(-0.021, 0.021, 2000)
theta = np.arctan(y / L)

#Interference 
alpha = np.pi * s * np.sin(theta) / lambda_  # for interference
beta = np.pi * a * np.sin(theta) / lambda_   # for diffraction

# Patterns
interference = np.cos(alpha)**2
# Avoid division by zero for envelope
envelope = np.ones_like(beta)
nonzero = beta != 0
envelope[nonzero] = (np.sin(beta[nonzero]) / beta[nonzero])**2
total = envelope * interference

y_mm = y * 1e3  # convert to mm for plotting

# Find and plot interference maxima (orders m)
m_orders = np.arange(-8, 9)
# y_m = m * lambda * L / s
maxima_y = m_orders * lambda_ * L / s
maxima_y_mm = maxima_y * 1e3

# Find and plot diffraction minima (envelope zeros, except at center)
n_orders = np.array([-4, -3, -2, -1, 1, 2, 3, 4])
minima_y = n_orders * lambda_ * L / a
minima_y_mm = minima_y * 1e3

# Create figure with only one subplot for the main pattern
fig, ax1 = plt.subplots(figsize=(14, 7))

# Plot total pattern
ax1.plot(y_mm, total / total.max(), label='Double-Slit Pattern', color='blue')
# Plot interference only (solid)
ax1.plot(y_mm, interference, label='Interference Only', color='purple', alpha=0.5, linestyle='-')
# Plot envelope only (solid)
ax1.plot(y_mm, envelope, label='Diffraction Envelope', color='orange', alpha=0.7, linestyle='-')

# Only label m = 0 and the orders where envelope minima occur
m_label_orders = [-8, -4, 0, 4, 8]
order_label_added = False
minima_label_added = False
for m, y_m in zip(m_orders, maxima_y_mm):
    if np.abs(y_m) <= y_mm[-1]:
        # Add legend label
        if not order_label_added:
            ax1.axvline(y_m, color='gray', linestyle='--', alpha=0.3, label='Interference Maxima (order $m$)')
            order_label_added = True
        else:
            ax1.axvline(y_m, color='gray', linestyle='--', alpha=0.3)
        # Only label selected m values
        if m in m_label_orders:
            ax1.text(y_m, 1.08, f'$m={m}$', ha='center', va='bottom', fontsize=12, color='gray', rotation=0)

# Vertical lines for envelope minima
for n, y_n in zip(n_orders, minima_y_mm):
    if np.abs(y_n) <= y_mm[-1]:
        if not minima_label_added:
            ax1.axvline(y_n, color='red', linestyle=':', alpha=0.8, label='Envelope Minima')
            minima_label_added = True
        else:
            ax1.axvline(y_n, color='red', linestyle=':', alpha=0.8)

ax1.set_xlabel('Position on Screen y (mm)')
ax1.set_ylabel('Relative Intensity')
ax1.set_title(r'Double-Slit Interference Pattern ($\lambda$ = 550 nm, s = 0.5 mm, L = 2.0 m)', fontsize=22, pad=40)
ax1.grid(True, which='both', linestyle=':', alpha=0.3)
ax1.legend()
ax1.set_ylim(-0.05, 1.15)

plt.tight_layout(rect=[0, 0, 1, 0.93])  # leave space for title and m labels
plt.savefig('double_slit_pattern.png', dpi=300, bbox_inches='tight')
plt.show()
