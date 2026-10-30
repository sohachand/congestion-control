import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import os

os.makedirs("evidence", exist_ok=True)  # charts get saved here

INK = "#1c1b19"
DIM = "#6b6558"
LINE = "#d8d3c7"
ACCENT = "#1d6f6a"
ACCENT2 = "#b5742a"
BAD = "#a8432f"
GOOD = "#2f7d4f"
BG = "#f3f1ec"
PANEL = "#ffffff"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "text.color": INK,
    "axes.edgecolor": LINE,
    "axes.labelcolor": INK,
    "xtick.color": DIM,
    "ytick.color": DIM,
    "figure.facecolor": BG,
    "axes.facecolor": PANEL,
})

# ---------- Figure 1: TCP Reno cwnd sawtooth ----------
rng = np.random.default_rng(7)
rounds = [0]
cwnd = [1]
ssthresh = [16]
states = ["slow start"]
c, st = 1, 16
for r in range(1, 46):
    state = "slow start" if c < st else "congestion avoidance"
    lost = state == "congestion avoidance" and rng.random() < 0.12
    if lost:
        st = max(2, c // 2)
        c = st  # Reno fast recovery
        state = "loss"
    else:
        c = c * 2 if state == "slow start" else c + 1
    c = min(c, 44)
    rounds.append(r); cwnd.append(c); ssthresh.append(st); states.append(state)

fig, ax = plt.subplots(figsize=(8.6, 4.2), dpi=200)
for i in range(1, len(rounds)):
    color = ACCENT if states[i] == "slow start" else (BAD if states[i] == "loss" else ACCENT2)
    ax.axvspan(rounds[i-1], rounds[i], color=color, alpha=0.08, lw=0)
ax.step(rounds, ssthresh, where="post", color=DIM, lw=1.2, ls="--", label="ssthresh")
ax.step(rounds, cwnd, where="post", color=ACCENT, lw=2.3, label="cwnd")
loss_r = [rounds[i] for i in range(len(states)) if states[i] == "loss"]
loss_c = [cwnd[i] for i in range(len(states)) if states[i] == "loss"]
ax.scatter(loss_r, loss_c, color=BAD, zorder=5, s=28, label="loss event")
ax.set_xlabel("RTT round")
ax.set_ylabel("cwnd (segments, MSS)")
ax.set_title("TCP Reno: congestion window vs. time", color=INK, fontsize=13, weight="bold")
ax.legend(frameon=False, loc="upper left", fontsize=9)
ax.spines[["top", "right"]].set_visible(False)
ax.grid(axis="y", color=LINE, lw=0.6, alpha=0.6)
fig.tight_layout()
fig.savefig("evidence/fig_cwnd_sawtooth.png", facecolor=BG)
plt.close(fig)

# ---------- Figure 2: Leaky bucket schematic ----------
fig, ax = plt.subplots(figsize=(8.6, 3.6), dpi=200)
ax.set_xlim(0, 10); ax.set_ylim(0, 5); ax.axis("off")
# bursty arrivals (left)
for i, x in enumerate([0.3, 0.55, 0.8, 0.95, 1.2]):
    ax.add_patch(patches.Circle((x, 2.5 + (0.3 if i % 2 else -0.3)), 0.12, color=ACCENT2))
ax.annotate("", xy=(2.1, 2.5), xytext=(1.4, 2.5), arrowprops=dict(arrowstyle="-|>", color=DIM, lw=1.6))
ax.text(0.7, 3.3, "bursty\narrivals", ha="center", fontsize=9, color=DIM)
# bucket (funnel)
bucket = patches.Polygon([[2.6, 4.4], [6.6, 4.4], [6.0, 0.9], [3.2, 0.9]], closed=True,
                          fill=True, facecolor=PANEL, edgecolor=DIM, lw=1.8)
ax.add_patch(bucket)
ax.add_patch(patches.Polygon([[3.35, 2.0], [5.85, 2.0], [5.5, 0.95], [3.7, 0.95]], closed=True,
                              facecolor=ACCENT, alpha=0.55, edgecolor="none"))
ax.text(4.6, 4.75, "leaky bucket (fixed capacity)", ha="center", fontsize=9.5, color=INK, weight="bold")
# leak hole + steady output
ax.annotate("", xy=(8.6, 0.95), xytext=(5.9, 0.95), arrowprops=dict(arrowstyle="-|>", color=GOOD, lw=2))
for x in [6.4, 7.1, 7.8]:
    ax.add_patch(patches.Circle((x, 0.95), 0.1, color=GOOD))
ax.text(7.5, 1.5, "fixed-rate\noutput", ha="center", fontsize=9, color=GOOD)
# overflow
ax.annotate("", xy=(4.6, 5.3), xytext=(4.6, 4.45), arrowprops=dict(arrowstyle="-|>", color=BAD, lw=2))
ax.text(4.6, 5.55, "overflow → dropped", ha="center", fontsize=9, color=BAD)
fig.tight_layout()
fig.savefig("evidence/fig_leaky_bucket.png", facecolor=BG)
plt.close(fig)

# ---------- Figure 3: Token bucket schematic ----------
fig, ax = plt.subplots(figsize=(8.6, 3.6), dpi=200)
ax.set_xlim(0, 10); ax.set_ylim(0, 5); ax.axis("off")
ax.add_patch(patches.FancyArrowPatch((1.0, 4.6), (1.0, 4.0), arrowstyle="-|>", color=ACCENT2, mutation_scale=16))
ax.text(1.0, 4.85, "token generator\n(fixed rate)", ha="center", fontsize=9, color=DIM)
bucket = patches.Rectangle((0.4, 1.0), 1.4, 3.0, fill=True, facecolor=PANEL, edgecolor=DIM, lw=1.8)
ax.add_patch(bucket)
ax.add_patch(patches.Rectangle((0.5, 1.1), 1.2, 1.8, facecolor=ACCENT2, alpha=0.6, edgecolor="none"))
for ty in [1.5, 1.9, 2.3, 2.7]:
    ax.add_patch(patches.Circle((1.1, ty), 0.12, color="#ffffff", ec=ACCENT2, lw=1))
ax.text(1.1, 0.6, "token bucket", ha="center", fontsize=9.5, color=INK, weight="bold")
# packets queue
for i, x in enumerate([2.6, 3.0, 3.4, 3.8]):
    ax.add_patch(patches.Rectangle((x, 2.2), 0.3, 0.3, color=DIM, alpha=0.7))
ax.text(3.2, 2.9, "packet queue", ha="center", fontsize=9, color=DIM)
# gate / check
ax.add_patch(patches.RegularPolygon((5.0, 2.35), numVertices=4, radius=0.55, orientation=np.pi/4,
                                     facecolor=PANEL, edgecolor=DIM, lw=1.6))
ax.text(5.0, 2.35, "token?", ha="center", va="center", fontsize=8.5, color=INK)
ax.annotate("", xy=(4.5, 2.35), xytext=(4.1, 2.35), arrowprops=dict(arrowstyle="-|>", color=DIM, lw=1.6))
# yes -> sent
ax.annotate("", xy=(8.4, 3.2), xytext=(5.55, 2.8), arrowprops=dict(arrowstyle="-|>", color=GOOD, lw=2))
ax.text(7.2, 3.55, "token available → sent\n(burst allowed)", ha="center", fontsize=8.8, color=GOOD)
# no -> dropped
ax.annotate("", xy=(8.4, 1.3), xytext=(5.55, 1.9), arrowprops=dict(arrowstyle="-|>", color=BAD, lw=2))
ax.text(7.2, 1.0, "no token → dropped\n(or queued)", ha="center", fontsize=8.8, color=BAD)
fig.tight_layout()
fig.savefig("evidence/fig_token_bucket.png", facecolor=BG)
plt.close(fig)

print("figures written")
