import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle

OUT = "/workspace/course/images"

plt.rcParams["font.family"] = "DejaVu Sans"

# ---- Modern flat palette ----
BG      = "#ffffff"
INK     = "#1e293b"   # main text
MUTED   = "#64748b"   # secondary text
LINE    = "#94a3b8"   # neutral arrows

BLUE    = "#2563eb"; BLUE_F   = "#dbeafe"; BLUE_S   = "#bfdbfe"
GREEN   = "#059669"; GREEN_F  = "#d1fae5"; GREEN_S  = "#a7f3d0"
ORANGE  = "#ea580c"; ORANGE_F = "#ffedd5"; ORANGE_S = "#fed7aa"
RED     = "#dc2626"; RED_F    = "#fee2e2"; RED_S    = "#fecaca"
PURPLE  = "#7c3aed"; PURPLE_F = "#ede9fe"; PURPLE_S = "#ddd6fe"
TEAL    = "#0d9488"; TEAL_F   = "#ccfbf1"; TEAL_S   = "#99f6e4"
AMBER   = "#d97706"; AMBER_F  = "#fef3c7"; AMBER_S  = "#fde68a"
GRAY_F  = "#f1f5f9"; GRAY_S   = "#e2e8f0"


def box(ax, x, y, w, h, text="", fc="#dbeafe", ec="#2563eb", fs=10.5, lw=1.6,
        bold=False, r=0.018, tc=None, va="center"):
    p = FancyBboxPatch((x, y), w, h,
                       boxstyle=f"round,pad=0.006,rounding_size={r}",
                       fc=fc, ec=ec, lw=lw, mutation_scale=1)
    ax.add_patch(p)
    if text:
        ax.text(x + w/2, y + h/2, text, ha="center", va=va, fontsize=fs,
                color=tc or INK, weight="bold" if bold else "normal",
                linespacing=1.35)
    return p


def cyl(ax, cx, cy, w, h, label="", fc=GREEN_F, ec=GREEN, fs=9):
    """Small database cylinder."""
    from matplotlib.patches import Ellipse
    e1 = Ellipse((cx, cy + h/2), w, w*0.32, fc=fc, ec=ec, lw=1.6)
    e2 = Ellipse((cx, cy - h/2), w, w*0.32, fc=fc, ec=ec, lw=1.6)
    rect = plt.Rectangle((cx - w/2, cy - h/2), w, h, fc=fc, ec="none")
    ax.add_patch(rect); ax.add_patch(e2); ax.add_patch(e1)
    ax.plot([cx - w/2, cx - w/2], [cy - h/2, cy + h/2], color=ec, lw=1.6)
    ax.plot([cx + w/2, cx + w/2], [cy - h/2, cy + h/2], color=ec, lw=1.6)
    if label:
        ax.text(cx, cy - h/2 - 0.035, label, ha="center", va="top",
                fontsize=fs, color=MUTED)


def arrow(ax, x1, y1, x2, y2, color=LINE, style="-|>", ls="-", lw=1.8, ms=16):
    a = FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=style,
                        mutation_scale=ms, color=color, lw=lw, linestyle=ls,
                        shrinkA=2, shrinkB=2)
    ax.add_patch(a)
    return a


def lbl(ax, x, y, text, fs=9, color=MUTED, ha="center", style="normal", weight="normal"):
    ax.text(x, y, text, fontsize=fs, color=color, ha=ha, va="center",
            style=style, weight=weight)


def title(ax, x, y, text, fs=13, color=INK):
    ax.text(x, y, text, fontsize=fs, color=color, ha="center", va="center",
            weight="bold")


def new_ax(figsize=(11, 6)):
    fig, ax = plt.subplots(figsize=figsize)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.axis("off")
    fig.patch.set_facecolor(BG)
    return fig, ax


def save(fig, name):
    fig.savefig(f"{OUT}/{name}", dpi=180, bbox_inches="tight",
                facecolor=BG, pad_inches=0.15)
    plt.close(fig)


# ============================================================
# 1. Monolith vs Microservices
# ============================================================
fig, ax = new_ax((12, 6.2))

# Left: monolith
title(ax, 0.24, 0.94, "МОНОЛИТ", 14)
box(ax, 0.06, 0.16, 0.36, 0.72, "", fc="#fffbeb", ec=AMBER, lw=2)
mods = [("Presentation / UI", 0.70), ("Business logic", 0.535), ("Data access (ORM)", 0.37)]
for t, y in mods:
    box(ax, 0.10, y, 0.28, 0.115, t, fc=AMBER_F, ec=AMBER, fs=10)
cyl(ax, 0.24, 0.245, 0.16, 0.06, "единая БД", fc=RED_F, ec=RED, fs=9)
lbl(ax, 0.24, 0.075, "один деплой • один сбой роняет всё\nкоманда из 50 человек в одном коде", 9.5)

# Right: microservices
title(ax, 0.72, 0.94, "МИКРОСЕРВИСЫ", 14)
svcs = [("users", BLUE, BLUE_F), ("orders", GREEN, GREEN_F),
        ("payments", PURPLE, PURPLE_F), ("catalog", ORANGE, ORANGE_F)]
pos = [(0.52, 0.62), (0.70, 0.62), (0.52, 0.34), (0.70, 0.34)]
for (name, ec, fc), (x, y) in zip(svcs, pos):
    box(ax, x, y, 0.145, 0.16, name, fc=fc, ec=ec, fs=11, bold=True)
    cyl(ax, x + 0.0725, y - 0.055, 0.09, 0.035, "своя БД", fc=GRAY_F, ec=MUTED, fs=8)
    arrow(ax, x + 0.0725, y, x + 0.0725, y - 0.032, color=ec, lw=1.4)
# client on top
box(ax, 0.585, 0.86, 0.215, 0.075, "клиент", fc=GRAY_F, ec=MUTED, fs=10)
for x, y in pos:
    arrow(ax, 0.6925, 0.86, x + 0.0725, y + 0.16, color=LINE, lw=1.2, ls=(0,(3,2)))
lbl(ax, 0.72, 0.075, "независимые деплои • изоляция сбоев\nмаленькие команды вокруг сервисов", 9.5)

arrow(ax, 0.445, 0.52, 0.485, 0.52, color=INK, lw=2.5, ms=22)
save(fig, "01_monolith_vs_microservices.png")

# ============================================================
# 2. Sync vs Async communication
# ============================================================
fig, ax = new_ax((12, 6))

title(ax, 0.25, 0.93, "СИНХРОННЫЙ REST/gRPC", 12)
box(ax, 0.06, 0.60, 0.13, 0.11, "Order", fc=GREEN_F, ec=GREEN, bold=True)
box(ax, 0.24, 0.60, 0.13, 0.11, "Payment", fc=PURPLE_F, ec=PURPLE, bold=True)
box(ax, 0.06, 0.34, 0.13, 0.11, "Inventory", fc=BLUE_F, ec=BLUE, bold=True)
arrow(ax, 0.19, 0.675, 0.24, 0.675, color=INK)
lbl(ax, 0.215, 0.72, "POST /pay", 8.5)
arrow(ax, 0.125, 0.60, 0.125, 0.45, color=INK)
lbl(ax, 0.155, 0.53, "GET stock", 8.5, ha="left")
lbl(ax, 0.185, 0.20, "отвечает только когда все ответы получены\nзадержка = сумма задержек цепочки", 9)

title(ax, 0.74, 0.93, "АСИНХРОННЫЙ БРОКЕР СООБЩЕНИЙ", 12)
box(ax, 0.52, 0.62, 0.12, 0.11, "Order\n(producer)", fc=GREEN_F, ec=GREEN, fs=9, bold=True)
box(ax, 0.68, 0.55, 0.17, 0.25, "брокер\n(Kafka / RabbitMQ)", fc=AMBER_F, ec=AMBER, fs=9.5, bold=True)
box(ax, 0.90, 0.70, 0.085, 0.09, "Payment", fc=PURPLE_F, ec=PURPLE, fs=8)
box(ax, 0.90, 0.57, 0.085, 0.09, "Shipping", fc=BLUE_F, ec=BLUE, fs=8)
box(ax, 0.90, 0.44, 0.085, 0.09, "Email", fc=ORANGE_F, ec=ORANGE, fs=8)
arrow(ax, 0.64, 0.675, 0.68, 0.675, color=INK)
lbl(ax, 0.66, 0.715, "event:", 8); lbl(ax, 0.66, 0.645, "order.created", 7.5, color=GREEN)
for yy in (0.745, 0.615, 0.485):
    arrow(ax, 0.85, 0.675 if yy==0.745 else (0.675 if yy==0.615 else 0.675), 0.90, yy, color=LINE, lw=1.3)
lbl(ax, 0.735, 0.20, "producer не ждёт consumers\nкаждый подписчик читает сам, темп свой", 9)

# latency comparison bars
ax.text(0.06, 0.155, "СРАВНЕНИЕ ЗАДЕРЖКИ", fontsize=9.5, color=MUTED, weight="bold", ha="left")
# sync: sequential chain of colored segments
xb = 0.06
for lab, d, c in [("order", 0.05, GREEN), ("payment", 0.13, PURPLE), ("stock", 0.08, BLUE)]:
    ax.add_patch(FancyBboxPatch((xb, 0.10), d, 0.028, boxstyle="round,pad=0.002",
                                fc=c, ec=c, alpha=0.9))
    xb += d + 0.004
lbl(ax, 0.36, 0.114, "= 320 мс до ответа клиенту", 8.5, color=INK, ha="left")
# async: short publish + parallel background
ax.add_patch(FancyBboxPatch((0.06, 0.045), 0.03, 0.028, boxstyle="round,pad=0.002",
                            fc=GREEN, ec=GREEN, alpha=0.9))
for i, (d, c) in enumerate([(0.10, PURPLE), (0.07, BLUE)]):
    ax.add_patch(FancyBboxPatch((0.098, 0.055 - i*0.012), d, 0.009,
                                boxstyle="round,pad=0.001", fc=c, ec=c, alpha=0.75))
lbl(ax, 0.215, 0.058, "= 60 мс до ответа, остальное — в фоне", 8.5, color=INK, ha="left")
save(fig, "02_sync_async_communication.png")

# ============================================================
# 3. API Gateway
# ============================================================
fig, ax = new_ax((11, 6.5))
box(ax, 0.05, 0.78, 0.13, 0.09, "Web", fc=GRAY_F, ec=MUTED, bold=True)
box(ax, 0.05, 0.66, 0.13, 0.09, "Mobile", fc=GRAY_F, ec=MUTED, bold=True)
box(ax, 0.05, 0.54, 0.13, 0.09, "Партнёры", fc=GRAY_F, ec=MUTED, bold=True)

gw_x, gw_y, gw_w, gw_h = 0.30, 0.40, 0.26, 0.48
box(ax, gw_x, gw_y, gw_w, gw_h, "", fc=BLUE_F, ec=BLUE, lw=2.2)
title(ax, gw_x + gw_w/2, 0.855, "API GATEWAY", 12, BLUE)
steps = ["аутентификация (JWT)", "rate limiting", "роутинг /path → сервис", "ретраи, таймауты", "логирование запросов"]
for i, s in enumerate(steps):
    box(ax, gw_x+0.025, 0.755 - i*0.075, gw_w-0.05, 0.055, s, fc="white", ec=BLUE, fs=9)

for yy in (0.825, 0.705, 0.585):
    arrow(ax, 0.18, yy, gw_x, (yy+0.62)/2 if yy!=0.585 else 0.52, color=LINE, lw=1.5)

backends = [("users", GREEN, GREEN_F, 0.78), ("orders", PURPLE, PURPLE_F, 0.62),
            ("payments", ORANGE, ORANGE_S, 0.46), ("catalog", TEAL, TEAL_F, 0.30)]
for name, ec, fc, y in backends:
    box(ax, 0.72, y, 0.16, 0.09, name, fc=fc, ec=ec, bold=True)
    arrow(ax, gw_x+gw_w, 0.64, 0.72, y+0.045, color=ec, lw=1.6)

box(ax, 0.72, 0.10, 0.16, 0.09, "лицензионный /\nвнутренний API", fc=GRAY_F, ec=MUTED, fs=8.5)
lbl(ax, 0.43, 0.16, "single entry point:\nклиенты не знают топологию внутри", 9.5, ha="left")
lbl(ax, 0.30, 0.05, "минус: gateway может стать «умным» монолитом — держите в нём только сетевые функции", 9, color=RED)
save(fig, "03_api_gateway.png")

# ============================================================
# 4. Service Discovery
# ============================================================
fig, ax = new_ax((11, 6.2))
box(ax, 0.38, 0.74, 0.24, 0.14, "", fc=PURPLE_F, ec=PURPLE, lw=2)
title(ax, 0.50, 0.845, "РЕЕСТР (registry)", 11, PURPLE)
reg = ["users-svc → 10.0.1.4:8080", "users-svc → 10.0.2.9:8080", "orders-svc → 10.0.3.2:8080"]
for i, r in enumerate(reg):
    lbl(ax, 0.50, 0.80 - i*0.028, r, 8.5, color=INK)

svc_data = [("users A", 0.06, 0.45, GREEN), ("users B", 0.06, 0.28, GREEN),
            ("orders C", 0.86, 0.45, BLUE), ("caller", 0.44, 0.10, ORANGE)]
for name, x, y, c in svc_data:
    box(ax, x, y, 0.12, 0.09, name, fc="white", ec=c, lw=2, bold=True)
    arrow(ax, x+0.06, y+0.09, 0.50 if x < 0.3 else (0.44 if x>0.5 else 0.50), 0.74,
          color=c, ls=(0,(4,2)), lw=1.3)
lbl(ax, 0.10, 0.56, "heartbeat каждые 5 с", 8.5, color=MUTED)
lbl(ax, 0.90, 0.56, "registration", 8.5, color=MUTED)

arrow(ax, 0.56, 0.145, 0.86, 0.25, color=ORANGE, lw=2)
lbl(ax, 0.74, 0.22, "lookup + балансировка", 9, color=ORANGE)
arrow(ax, 0.44, 0.145, 0.18, 0.30, color=INK, lw=2)
lbl(ax, 0.24, 0.20, "прямой вызов 10.0.1.4:8080", 9)

lbl(ax, 0.50, 0.02, "вышел users B → heartbeat пропал → реестр исключил инстанс → новые запросы идут только на A", 9, color=RED)
save(fig, "04_service_discovery.png")

# ============================================================
# 5. Saga orchestration
# ============================================================
fig, ax = new_ax((12, 6.2))
box(ax, 0.38, 0.78, 0.24, 0.12, "SAGA ORCHESTRATOR", fc=AMBER_F, ec=AMBER, bold=True, fs=11)
steps = [("1. create order", GREEN, 0.05), ("2. reserve stock", BLUE, 0.27),
         ("3. charge card", PURPLE, 0.49), ("4. ship", ORANGE, 0.71)]
for name, c, x in steps:
    box(ax, x, 0.45, 0.19, 0.10, name.split(". ",1)[1], fc="white", ec=c, lw=2, bold=True, fs=10)
    lbl(ax, x+0.095, 0.575, name.split(".")[0], 9, color=c, weight="bold")
    arrow(ax, x+0.095, 0.78, x+0.095, 0.55, color=AMBER, lw=1.4)
    arrow(ax, x+0.095, 0.45, x+0.095, 0.38, color=c, lw=1.4, style="-|>")
    lbl(ax, x+0.095, 0.345, "ok", 8.5, color=GREEN)

# failure path
box(ax, 0.49, 0.17, 0.19, 0.09, "ОТКАЗ оплаты", fc=RED_F, ec=RED, bold=True, fs=9.5)
arrow(ax, 0.585, 0.38, 0.585, 0.26, color=RED, lw=2)
comp = [("C1: отменить заказ", 0.05), ("C2: вернуть stock", 0.27)]
for name, x in comp:
    box(ax, x, 0.17, 0.19, 0.09, name, fc=GRAY_F, ec=RED, fs=8.5)
    arrow(ax, 0.49, 0.215, x+0.19, 0.215, color=RED, ls=(0,(3,2)), lw=1.3)
lbl(ax, 0.60, 0.09, "компенсации выполняются в обратном порядке;\nитоговое состояние согласовано eventual consistency", 9, color=MUTED)
save(fig, "05_saga_orchestration.png")

# ============================================================
# 6. Circuit breaker states
# ============================================================
fig, ax = new_ax((10.5, 6))
nodes = {"CLOSED": (0.14, 0.55, GREEN, GREEN_F),
         "OPEN":   (0.55, 0.82, RED, RED_F),
         "HALF-\nOPEN": (0.55, 0.30, AMBER, AMBER_F)}
for name, (x, y, c, fc) in nodes.items():
    box(ax, x, y, 0.20, 0.14, name, fc=fc, ec=c, lw=2.5, bold=True, fs=11)

arrow(ax, 0.34, 0.66, 0.55, 0.84, color=RED, lw=2)
lbl(ax, 0.40, 0.79, "fail% > порога", 8.5, color=RED)
arrow(ax, 0.65, 0.82, 0.65, 0.44, color=AMBER, lw=2)
lbl(ax, 0.70, 0.63, "таймер истёк", 8.5, color=AMBER, ha="left")
arrow(ax, 0.55, 0.34, 0.24, 0.55, color=GREEN, lw=2)
lbl(ax, 0.33, 0.40, "тест прошёл", 8.5, color=GREEN)
arrow(ax, 0.65, 0.30, 0.65, 0.18, color=RED, lw=1.6)
lbl(ax, 0.70, 0.15, "тест упал → снова OPEN", 8.5, color=RED, ha="left")

box(ax, 0.83, 0.55, 0.15, 0.14, "fallback:\nкэш /\nнейтральное\nзначение", fc=GRAY_F, ec=MUTED, fs=8.5)
arrow(ax, 0.75, 0.86, 0.90, 0.69, color=MUTED, lw=1.5)
lbl(ax, 0.85, 0.80, "пока OPEN", 8.5)

lbl(ax, 0.5, 0.04, "CLOSED — идёт трафик и сбор статистики • OPEN — вызовы блокируются мгновенно,\n downstream отдыхает • HALF-OPEN — пропускаем несколько тестовых запросов", 9, color=MUTED)
save(fig, "06_circuit_breaker.png")

# ============================================================
# 7. Event-driven with outbox
# ============================================================
fig, ax = new_ax((12, 6.2))
box(ax, 0.05, 0.55, 0.22, 0.30, "", fc=GREEN_F, ec=GREEN, lw=2)
title(ax, 0.16, 0.82, "orders-service", 10.5, GREEN)
box(ax, 0.07, 0.60, 0.085, 0.12, "таблица\norders", fc="white", ec=GREEN, fs=8.5)
box(ax, 0.17, 0.60, 0.085, 0.12, "outbox\ntable", fc=AMBER_F, ec=AMBER, fs=8.5)
lbl(ax, 0.16, 0.50, "один local ACID-транзакт", 8.5)

box(ax, 0.34, 0.60, 0.13, 0.11, "relay /\ndebezium", fc=GRAY_F, ec=MUTED, fs=8.5)
arrow(ax, 0.27, 0.655, 0.34, 0.655, color=AMBER, lw=2)

box(ax, 0.53, 0.55, 0.20, 0.22, "Kafka topic\norder-events", fc=PURPLE_F, ec=PURPLE, lw=2, bold=True, fs=10)
arrow(ax, 0.47, 0.655, 0.53, 0.655, color=INK, lw=2)

subs = [("payments", 0.78, BLUE), ("shipping", 0.62, TEAL), ("analytics", 0.46, ORANGE)]
for name, y, c in subs:
    box(ax, 0.80, y, 0.15, 0.09, name, fc="white", ec=c, lw=2, bold=True, fs=9.5)
    arrow(ax, 0.73, 0.66, 0.80, y+0.045, color=c, lw=1.6)
lbl(ax, 0.875, 0.40, "consumer groups", 8.5)

box(ax, 0.53, 0.18, 0.20, 0.12, "DLQ\norder-events.dead", fc=RED_F, ec=RED, fs=8.5)
arrow(ax, 0.875, 0.62, 0.73, 0.26, color=RED, ls=(0,(3,2)), lw=1.4)
lbl(ax, 0.84, 0.33, "после N ретраев", 8.5, color=RED)

lbl(ax, 0.16, 0.06, "почему outbox: запись в БД и в брокер — разные системы,\nбез outbox событие может «потеряться» при падении между commit и publish", 9, color=MUTED)
save(fig, "07_event_driven.png")

# ============================================================
# 8. Strangler Fig migration
# ============================================================
fig, ax = new_ax((11.5, 6))
box(ax, 0.05, 0.30, 0.30, 0.45, "ЛЕГАСИ-МОНОЛИТ", fc=GRAY_F, ec=MUTED, lw=2, bold=True, fs=11)
inner = ["users", "orders", "payments", "catalog", "search"]
for i, m in enumerate(inner):
    fade = i >= 3
    box(ax, 0.08, 0.62 - i*0.075, 0.24, 0.055, m + (" ✓ вынесен" if fade else ""),
        fc=RED_F if not fade else "white", ec=RED if not fade else GREEN, fs=8.5)

box(ax, 0.42, 0.44, 0.14, 0.18, "ROUTER /\ngateway", fc=BLUE_F, ec=BLUE, lw=2.2, bold=True, fs=9.5)
box(ax, 0.68, 0.66, 0.16, 0.09, "catalog-svc", fc=GREEN_F, ec=GREEN, bold=True, fs=9.5)
box(ax, 0.68, 0.50, 0.16, 0.09, "search-svc", fc=GREEN_F, ec=GREEN, bold=True, fs=9.5)
box(ax, 0.68, 0.34, 0.16, 0.09, "users-svc", fc=TEAL_F, ec=TEAL, bold=True, fs=9.5)

arrow(ax, 0.20, 0.78, 0.42, 0.57, color=INK, lw=2)
lbl(ax, 0.27, 0.72, "весь трафик", 8.5)
arrow(ax, 0.49, 0.44, 0.35, 0.35, color=MUTED, lw=1.8)
lbl(ax, 0.40, 0.27, "остатки", 8.5)
for y in (0.705, 0.545, 0.385):
    arrow(ax, 0.56, 0.53, 0.68, y, color=GREEN, lw=1.6)

lbl(ax, 0.50, 0.90, "шаги: 1) router перед монолитом → 2) перенос функций по одной → 3) dual-write/миграция данных → 4) монолит гаснет", 9.5, color=MUTED)
lbl(ax, 0.50, 0.06, "главный риск: «вечная миграция» — фиксируйте критерий готовности каждого этапа до старта", 9.5, color=RED)
save(fig, "08_strangler_fig.png")

# ============================================================
# 9. Observability three pillars
# ============================================================
fig, ax = new_ax((12, 6))
pillars = [
    ("МЕТРИКИ", BLUE, BLUE_F, "числа во времени\nlatency P99, RPS, error rate\n→ Prometheus + Grafana"),
    ("ТРЕЙСЫ", PURPLE, PURPLE_F, "путь одного запроса\nсквозь все сервисы\n→ OpenTelemetry + Jaeger"),
    ("ЛОГИ", TEAL, TEAL_F, "события с context\ntrace_id в каждой строке\n→ Loki / ELK"),
]
for (t, c, fc, body), x in zip(pillars, (0.05, 0.38, 0.71)):
    box(ax, x, 0.55, 0.24, 0.30, "", fc=fc, ec=c, lw=2)
    title(ax, x+0.12, 0.80, t, 12, c)
    lbl(ax, x+0.12, 0.655, body, 9)

box(ax, 0.30, 0.18, 0.40, 0.16, "CORRELATION\ntrace_id склеивает три столпа:\nметрика аномальная → трейс нашёл сервис → лог дал причину",
    fc=AMBER_F, ec=AMBER, fs=9, bold=False)
for x in (0.17, 0.50, 0.83):
    arrow(ax, x, 0.55, 0.50, 0.34, color=AMBER, lw=1.6)

lbl(ax, 0.50, 0.05, "USE-методика для ресурсов (Utilization/Saturation/Errors) и RED для сервисов (Rate/Errors/Duration)", 9, color=MUTED)
save(fig, "09_observability.png")

# ============================================================
# 10. Kubernetes deployment
# ============================================================
fig, ax = new_ax((12, 6.2))
box(ax, 0.04, 0.42, 0.11, 0.10, "User", fc=GRAY_F, ec=MUTED, fs=9)
box(ax, 0.20, 0.42, 0.12, 0.10, "Ingress", fc=BLUE_F, ec=BLUE, bold=True, fs=9.5)
arrow(ax, 0.15, 0.47, 0.20, 0.47, color=INK)

box(ax, 0.39, 0.20, 0.58, 0.65, "", fc="#f8fafc", ec=INK, lw=2)
title(ax, 0.68, 0.81, "Kubernetes cluster", 11)
svc_defs = [("Service users", 0.66, GREEN, GREEN_F), ("Service orders", 0.45, PURPLE, PURPLE_F)]
for name, y, c, fc in svc_defs:
    box(ax, 0.42, y, 0.14, 0.08, name, fc="white", ec=c, fs=8.5, bold=True)
    for j in range(3):
        px = 0.60 + j*0.115
        box(ax, px, y-0.01, 0.09, 0.10, f"pod-{j+1}", fc=fc, ec=c, fs=8)
        arrow(ax, 0.56, y+0.04, px, y+0.04, color=c, lw=1.2)
arrow(ax, 0.32, 0.47, 0.42, 0.70, color=BLUE, lw=1.6)
arrow(ax, 0.32, 0.47, 0.42, 0.49, color=PURPLE, lw=1.6)

lbl(ax, 0.68, 0.27, "replicas + readiness/liveness probes\nrolling update: новый pod готов → старый получает SIGTERM", 9, color=MUTED)
box(ax, 0.39, 0.04, 0.58, 0.09, "CI/CD: build image → push registry → ArgoCD синхронизирует манифесты (GitOps)",
    fc=AMBER_F, ec=AMBER, fs=9)
save(fig, "10_kubernetes.png")

print("done")
