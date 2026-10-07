import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle

OUT = "/workspace/course/images"

def box(ax, x, y, w, h, text, fc="#e3f2fd", ec="#1565c0", fs=10, lw=1.5):
    p = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.02",
                       fc=fc, ec=ec, lw=lw)
    ax.add_patch(p)
    ax.text(x + w/2, y + h/2, text, ha="center", va="center", fontsize=fs, wrap=True)

def arrow(ax, x1, y1, x2, y2, color="#424242", style="-|>", ls="-", lw=1.8, label=None, lx=0, ly=0, lfs=9, lcolor=None):
    a = FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=style, mutation_scale=15,
                        color=color, lw=lw, linestyle=ls)
    ax.add_patch(a)
    if label:
        ax.text((x1+x2)/2 + lx, (y1+y2)/2 + ly, label, fontsize=lfs,
                color=lcolor or color, ha="center", va="bottom")

def new_ax(figsize=(10, 6)):
    fig, ax = plt.subplots(figsize=figsize)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.axis("off")
    return fig, ax

def save(fig, name):
    fig.savefig(f"{OUT}/{name}", dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)

# ---------- 1. Monolith vs Microservices ----------
fig, ax = new_ax((12, 6))
ax.text(0.25, 0.95, "МОНОЛИТ", ha="center", fontsize=13, weight="bold")
box(ax, 0.05, 0.25, 0.4, 0.6, "", fc="#fff3e0", ec="#e65100")
for i, t in enumerate(["UI", "Бизнес-логика", "Доступ к данным"]):
    box(ax, 0.08, 0.72 - i*0.16, 0.34, 0.13, t, fc="#ffe0b2", ec="#e65100", fs=10)
box(ax, 0.13, 0.1, 0.24, 0.1, "Единая БД", fc="#ffcdd2", ec="#b71c1c", fs=10)
arrow(ax, 0.25, 0.25, 0.25, 0.2, color="#b71c1c")
ax.text(0.25, 0.04, "Один деплой, один сбой = падает всё", ha="center", fontsize=9, style="italic")

ax.text(0.75, 0.95, "МИКРОСЕРВИСЫ", ha="center", fontsize=13, weight="bold")
names = ["Сервис\nпользователей", "Сервис\nзаказов", "Сервис\nоплаты", "Сервис\nкаталога"]
dbs = ["БД users", "БД orders", "БД pay", "БД catalog"]
for i in range(4):
    x = 0.55 + (i % 2) * 0.22
    y = 0.55 - (i // 2) * 0.3
    box(ax, x, y, 0.18, 0.16, names[i], fc="#e1f5fe", ec="#0277bd", fs=9)
    box(ax, x + 0.02, y - 0.09, 0.14, 0.07, dbs[i], fc="#e8f5e9", ec="#2e7d32", fs=8)
    arrow(ax, x + 0.09, y, x + 0.09, y - 0.02, color="#2e7d32")
ax.text(0.75, 0.04, "Независимые деплой и БД, отказоустойчивость", ha="center", fontsize=9, style="italic")
save(fig, "01_monolith_vs_microservices.png")

# ---------- 2. Communication: sync vs async ----------
fig, ax = new_ax((12, 6))
ax.text(0.25, 0.95, "СИНХРОННО (HTTP/gRPC)", ha="center", fontsize=12, weight="bold")
box(ax, 0.05, 0.6, 0.12, 0.12, "Сервис A", fc="#e3f2fd", ec="#1565c0")
box(ax, 0.22, 0.6, 0.12, 0.12, "Сервис B", fc="#e3f2fd", ec="#1565c0")
box(ax, 0.22, 0.35, 0.12, 0.12, "Сервис C", fc="#e3f2fd", ec="#1565c0")
arrow(ax, 0.11, 0.6, 0.11, 0.5, color="#424242")
arrow(ax, 0.11, 0.5, 0.22, 0.45, label="1. запрос →", ly=-0.06)
arrow(ax, 0.28, 0.47, 0.28, 0.6, label="2. ответ ←", lx=0.06)
arrow(ax, 0.17, 0.63, 0.22, 0.63, label="→", )
ax.text(0.25, 0.2, "A ждёт B; B ждёт C.\nКаскадная задержка: 50+30+20 = 100 мс", ha="center", fontsize=9)
ax.text(0.75, 0.95, "АСИНХРОННО (брокер сообщений)", ha="center", fontsize=12, weight="bold")
box(ax, 0.52, 0.6, 0.12, 0.12, "Сервис A\n(продюсер)", fc="#e3f2fd", ec="#1565c0")
box(ax, 0.68, 0.45, 0.16, 0.12, "RabbitMQ / Kafka", fc="#fff9c4", ec="#f9a825")
box(ax, 0.52, 0.25, 0.12, 0.12, "Сервис B\n(консьюмер)", fc="#e3f2fd", ec="#1565c0")
box(ax, 0.82, 0.25, 0.12, 0.12, "Сервис C\n(консьюмер)", fc="#e3f2fd", ec="#1565c0")
arrow(ax, 0.60, 0.6, 0.72, 0.57, label="событие", lx=0.0, ly=0.02)
arrow(ax, 0.70, 0.45, 0.62, 0.37, label="получает", lx=-0.05)
arrow(ax, 0.80, 0.45, 0.86, 0.37, label="получает", lx=0.05)
ax.text(0.72, 0.12, "A не ждёт ответа. B и C обрабатывают в своём темпе", ha="center", fontsize=9)
save(fig, "02_sync_async_communication.png")

# ---------- 3. API Gateway ----------
fig, ax = new_ax((12, 6))
box(ax, 0.05, 0.65, 0.14, 0.12, "Клиент\n(Web/Mobile)", fc="#ede7f6", ec="#4527a0")
box(ax, 0.35, 0.55, 0.2, 0.25, "API Gateway\n\nАутентификация\nМаршрутизация\nRate limiting\nКэширование", fc="#fce4ec", ec="#ad1457", fs=9)
svcs = [("Сервис заказов", 0.72), ("Сервис каталога", 0.52), ("Сервис оплаты", 0.32)]
for name, y in svcs:
    box(ax, 0.72, y, 0.18, 0.1, name, fc="#e3f2fd", ec="#1565c0", fs=9)
    arrow(ax, 0.55, 0.68, 0.72, y + 0.05)
arrow(ax, 0.19, 0.71, 0.35, 0.68, label="/api/orders", ly=0.02)
ax.text(0.5, 0.1, "Клиент знает только адрес шлюза. Внутренняя топология сервисов скрыта.", ha="center", fontsize=10)
save(fig, "03_api_gateway.png")

# ---------- 4. Service Discovery ----------
fig, ax = new_ax((12, 6))
box(ax, 0.4, 0.75, 0.2, 0.15, "Реестр сервисов\n(Consul / Eureka / K8s)", fc="#fff9c4", ec="#f9a825", fs=9)
box(ax, 0.08, 0.4, 0.15, 0.12, "Сервис A", fc="#e3f2fd", ec="#1565c0")
box(ax, 0.42, 0.4, 0.15, 0.12, "Сервис B\n10.0.1.5:8080", fc="#e3f2fd", ec="#1565c0", fs=8)
box(ax, 0.75, 0.4, 0.15, 0.12, "Сервис B'\n10.0.2.9:8080", fc="#e3f2fd", ec="#1565c0", fs=8)
arrow(ax, 0.5, 0.52, 0.5, 0.75, label="2. найти все инстансы 'order-service'", lx=0.18, lfs=8)
arrow(ax, 0.16, 0.52, 0.44, 0.78, label="1. регистрация", lx=-0.05, lfs=8)
arrow(ax, 0.55, 0.78, 0.83, 0.52, label="1'. регистрация", lx=0.08, lfs=8)
arrow(ax, 0.23, 0.46, 0.42, 0.46, label="3. вызов напрямую", ly=0.02, lfs=8)
ax.text(0.5, 0.15, "Сервисы регистрируются при старте и «выживают» из реестра при остановке.\nКлиенты запрашивают адреса вместо жёсткой прописки хостов.", ha="center", fontsize=10)
save(fig, "04_service_discovery.png")

# ---------- 5. Saga orchestration ----------
fig, ax = new_ax((12, 6.5))
box(ax, 0.38, 0.8, 0.24, 0.12, "Сага-оркестратор", fc="#fce4ec", ec="#ad1457")
steps = [("1. Создать заказ", 0.05), ("2. Списать склад", 0.28), ("3. Оплата", 0.51), ("4. Отправка", 0.74)]
for name, x in steps:
    box(ax, x, 0.5, 0.2, 0.12, name, fc="#e3f2fd", ec="#1565c0", fs=9)
    arrow(ax, x + 0.1, 0.62, 0.42 + 0.16*min(x,0.3), 0.8, color="#ad1457", ls="--", lw=1)
for i in range(3):
    x1 = steps[i][1] + 0.2; x2 = steps[i+1][1]
    arrow(ax, x1, 0.56, x2, 0.56)
comp = [("Компенсация:\nотменить заказ", 0.05), ("Компенсация:\nвернуть товар", 0.28), ("Компенсация:\nвернуть деньги", 0.51)]
for name, x in comp:
    box(ax, x, 0.22, 0.2, 0.14, name, fc="#ffebee", ec="#c62828", fs=8)
for i in range(3):
    x = steps[i][1] + 0.1
    arrow(ax, x, 0.5, x, 0.36, color="#c62828", ls="--")
ax.text(0.75, 0.28, "Если шаг 3 упал —\nшаги 2 и 1 откатываются\nкомпенсирующими действиями", fontsize=9, ha="center", color="#c62828")
ax.text(0.5, 0.03, "Оркестрация: центральный координатор посылает команды каждому сервису", ha="center", fontsize=10)
save(fig, "05_saga_orchestration.png")

# ---------- 6. Circuit Breaker ----------
fig, ax = new_ax((12, 5.5))
box(ax, 0.05, 0.4, 0.18, 0.15, "ЗАКРЫТЫЙ\n(разрешён)", fc="#c8e6c9", ec="#2e7d32")
box(ax, 0.42, 0.4, 0.18, 0.15, "ПОЛУОТКРЫТЫЙ\n(проба)", fc="#fff9c4", ec="#f9a825")
box(ax, 0.78, 0.4, 0.18, 0.15, "ОТКРЫТЫЙ\n(блокирует)", fc="#ffcdd2", ec="#c62828")
arrow(ax, 0.23, 0.52, 0.42, 0.52, label="таймаут истёк", ly=0.02, lfs=8)
arrow(ax, 0.60, 0.48, 0.78, 0.48, label="порог ошибок превышен", ly=0.04, lfs=8)
arrow(ax, 0.78, 0.55, 0.60, 0.55, label="успешные ответы", ly=0.02, lfs=8)
arrow(ax, 0.42, 0.45, 0.23, 0.45, label="провал пробы", ly=-0.06, lfs=8)
arrow(ax, 0.14, 0.4, 0.14, 0.2, color="#2e7d32")
ax.text(0.14, 0.14, "запросы проходят", ha="center", fontsize=8)
arrow(ax, 0.87, 0.55, 0.87, 0.72, color="#c62828")
ax.text(0.87, 0.76, "Fallback: кэш /\nдеградация функции", ha="center", fontsize=8, color="#c62828")
ax.text(0.5, 0.9, "Паттерн Circuit Breaker (предохранитель)", ha="center", fontsize=12, weight="bold")
save(fig, "06_circuit_breaker.png")

# ---------- 7. Event-driven order flow ----------
fig, ax = new_ax((12, 6))
events = ["OrderCreated", "PaymentApproved", "InventoryReserved", "OrderShipped"]
svc_names = ["Сервис\nзаказов", "Сервис\nоплаты", "Сервис\nсклада", "Сервис\nдоставки"]
box(ax, 0.35, 0.75, 0.3, 0.12, "Шина событий (Kafka topic: events)", fc="#fff9c4", ec="#f9a825", fs=9)
for i, (ev, sn) in enumerate(zip(events, svc_names)):
    x = 0.05 + i * 0.24
    box(ax, x, 0.35, 0.18, 0.12, sn, fc="#e3f2fd", ec="#1565c0", fs=9)
    arrow(ax, x + 0.09, 0.47, x + 0.09, 0.75, color="#1565c0", label=ev, lfs=7, lx=0.0)
    arrow(ax, x + 0.14, 0.75, x + 0.14, 0.47, color="#f9a825", ls="--", lfs=7)
ax.text(0.5, 0.12, "Каждый сервис публикует события и подписывается на чужие.\nПрямых вызовов нет — связь только через шину.", ha="center", fontsize=10)
save(fig, "07_event_driven.png")

# ---------- 8. Strangler Fig ----------
fig, ax = new_ax((12, 6))
box(ax, 0.05, 0.4, 0.15, 0.15, "Клиенты", fc="#ede7f6", ec="#4527a0")
box(ax, 0.3, 0.4, 0.15, 0.15, "Прокси /\nGateway", fc="#fce4ec", ec="#ad1457", fs=9)
box(ax, 0.62, 0.62, 0.3, 0.18, "Монолит", fc="#fff3e0", ec="#e65100")
box(ax, 0.62, 0.36, 0.13, 0.13, "Новый\nсервис 1", fc="#e8f5e9", ec="#2e7d32", fs=8)
box(ax, 0.79, 0.36, 0.13, 0.13, "Новый\nсервис 2", fc="#e8f5e9", ec="#2e7d32", fs=8)
arrow(ax, 0.2, 0.48, 0.3, 0.48)
arrow(ax, 0.45, 0.52, 0.62, 0.7, label="старый трафик", lfs=8, ly=0.01)
arrow(ax, 0.45, 0.45, 0.62, 0.43, label="часть → новым", lfs=8, ly=0.02)
ax.text(0.5, 0.1, f"Этапы: 1) весь трафик в монолит  2) маршрутизация части функционала в новые сервисы\n3) монолит «задыхается» и удаляется по частям", ha="center", fontsize=10)
save(fig, "08_strangler_fig.png")

# ---------- 9. Observability ----------
fig, ax = new_ax((12, 6))
box(ax, 0.05, 0.45, 0.14, 0.12, "Trace ID", fc="#e1f5fe", ec="#0277bd")
spans = [("Сервис A", 0.25), ("Сервис B", 0.45), ("Сервис C", 0.65)]
for n, x in spans:
    box(ax, x, 0.6, 0.15, 0.08, n, fc="#e3f2fd", ec="#1565c0", fs=9)
arrow(ax, 0.19, 0.55, 0.28, 0.6)
arrow(ax, 0.4, 0.62, 0.45, 0.62)
arrow(ax, 0.6, 0.62, 0.65, 0.62)
ax.text(0.5, 0.75, "Распределённая трассировка: один TraceID проходит через все сервисы", ha="center", fontsize=10)
tri = [("МЕТРИКИ\n(Prometheus)", 0.1), ("ЛОГИ\n(Loki/ELK)", 0.42), ("ТРЕЙСЫ\n(Jaeger)", 0.74)]
for t, x in tri:
    box(ax, x, 0.15, 0.2, 0.15, t, fc="#f3e5f5", ec="#6a1b9a", fs=9)
ax.text(0.5, 0.4, "Три столпа наблюдаемости", ha="center", fontsize=11, weight="bold")
save(fig, "09_observability.png")

# ---------- 10. Container/K8s deployment ----------
fig, ax = new_ax((12, 6.5))
box(ax, 0.3, 0.8, 0.4, 0.12, "Kubernetes Cluster", fc="#e0f7fa", ec="#00695c", fs=11)
nodes = [("Node 1", 0.08), ("Node 2", 0.38), ("Node 3", 0.68)]
for n, x in nodes:
    box(ax, x, 0.45, 0.24, 0.3, "", fc="#eceff1", ec="#455a64")
    ax.text(x + 0.12, 0.72, n, ha="center", fontsize=10, weight="bold")
    for j in range(2):
        box(ax, x + 0.02 + j*0.115, 0.5, 0.1, 0.16, f"Pod\n{['order','pay'][j]}", fc="#c8e6c9", ec="#2e7d32", fs=7)
for x in [0.2, 0.5, 0.8]:
    arrow(ax, x, 0.8, x, 0.75, color="#00695c")
box(ax, 0.3, 0.15, 0.4, 0.12, "Docker-образ сервиса + CI/CD", fc="#fff9c4", ec="#f9a825", fs=10)
arrow(ax, 0.5, 0.27, 0.5, 0.45)
ax.text(0.5, 0.03, "Каждый микросервис упакован в контейнер; оркестратор раскладывает поды по нодам,\nвосстанавливает упавшие и масштабирует по нагрузке", ha="center", fontsize=9)
save(fig, "10_kubernetes.png")
print("done")
