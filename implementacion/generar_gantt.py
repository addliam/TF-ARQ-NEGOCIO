"""Genera el cronograma (diagrama de Gantt) del capítulo 4.

Uso: python implementacion/generar_gantt.py  ->  implementacion/G1_cronograma.png
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))

# (paquete, actividad, mes inicio, duración en meses, transición)
ACT = [
    ("PQ-E", "Aprobación, comité y plan de cambio", 1, 1, "T1"),
    ("PQ-A", "Firewall, switches, VLAN y VPN", 1, 2, "T1"),
    ("PQ-A", "Suscripción Azure, identidad y respaldo", 2, 1, "T1"),
    ("PQ-B", "Sistema de citas y turnos (desarrollo)", 2, 3, "T1"),
    ("PQ-B", "Integración caja–ESB y pantallas", 4, 1, "T1"),
    ("PQ-B", "Piloto en 3 especialidades y despliegue", 5, 1, "T1"),
    ("PQ-C", "Clúster local y migración de bases", 6, 2, "T2"),
    ("PQ-C", "Adaptador de historias clínicas", 7, 2, "T2"),
    ("PQ-C", "WhatsApp Business API y motor de IA (reglas)", 8, 2, "T2"),
    ("PQ-D", "ETL, repositorio y tablero", 10, 2, "T3"),
    ("PQ-D", "Portal web de citas y WAF", 10, 2, "T3"),
    ("PQ-D", "Entrenamiento de la IA con histórico", 12, 1, "T3"),
    ("PQ-E", "Capacitación y acompañamiento", 3, 10, "T1–T3"),
]
COL = {"T1": "#4C78A8", "T2": "#F58518", "T3": "#54A24B", "T1–T3": "#9D9D9D"}

fig, ax = plt.subplots(figsize=(11, 5.2), dpi=150)
for i, (pq, act, ini, dur, tr) in enumerate(ACT):
    y = len(ACT) - 1 - i
    ax.barh(y, dur, left=ini - 0.5, height=0.6, color=COL[tr], edgecolor="white")
    ax.text(-0.2, y, f"{pq}  {act}", ha="right", va="center", fontsize=8.5)
ax.set_yticks([])
ax.set_xticks(range(1, 13)); ax.set_xticklabels([f"M{m}" for m in range(1, 13)], fontsize=8.5)
ax.set_xlim(0.5, 12.5)
for m in (5.5, 9.5):
    ax.axvline(m, color="#555", lw=0.8, ls="--")
for x, t in ((3, "Transición 1: turno digital"), (7.5, "Transición 2: aviso y estimación"), (11, "Transición 3: analítica")):
    ax.text(x, len(ACT) - 0.2, t, ha="center", fontsize=8.5, weight="bold")
for s in ("top", "right", "left"):
    ax.spines[s].set_visible(False)
ax.grid(axis="x", color="#ddd", lw=0.5); ax.set_axisbelow(True)
handles = [plt.Rectangle((0, 0), 1, 1, color=c) for c in COL.values()]
ax.legend(handles, ["T1", "T2", "T3", "Transversal"], loc="upper center", bbox_to_anchor=(0.5, -0.08), fontsize=8, frameon=False, ncol=4)
plt.tight_layout()
plt.savefig(os.path.join(HERE, "G1_cronograma.png"), bbox_inches="tight")
print("OK G1_cronograma.png")
