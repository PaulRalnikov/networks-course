import matplotlib.pyplot as plt
import numpy as np

F = 15_000_000 #kbit
U_s = 30_000 #kbit/s
D_i = 2_000 #kbit/s

N = [10, 100, 1000]
U = [300, 700, 2_000] # kb\s

sz = len(N)
fig, axs = plt.subplots(1, sz, figsize=(15 * sz, 25))

for i in range(len(N)):
    n = N[i]

    ax = axs[i]
    x = np.array(U)
    y_client_server = [max(n * F / U_s, F / D_i) for _ in U]
    y_p2p = np.array([max(F / U_s, F / D_i, n * F / (U_s + u* n)) for u in U])

    width = 150.0
    ax.bar(x - width / 2, y_client_server, width=width, label="Client-server")
    ax.bar(x + width / 2, y_p2p, width=width, label="P2P")

    for container in ax.containers:
        ax.bar_label(container, rotation=90)

    ax.set_xlabel('U, kbit/s')
    ax.set_ylabel('Time (s)')
    ax.set_title(f'N = {n}')
    ax.set_xticks(x)
    ax.set_xticklabels(x)
    ax.legend(  fontsize='medium', title='Legend', title_fontsize='large', shadow=True)
plt.subplots_adjust(wspace=0.25)
plt.savefig("task2.pdf")
plt.show()
