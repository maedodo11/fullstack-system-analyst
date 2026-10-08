# Модуль 6. Безопасность и аутентификация

## Маршрут урока

| Режим | Что делать |
|---|---|
| База · 20–30 мин | Вход, роль и право на конкретный объект. Прочитайте [основу](#lesson-base) и объясните один пример своими словами. |
| Практика · 30–45 мин | Выполните [задание](#lesson-practice), затем сравните с [критериями](../practice/assessment.md). |
| Углубление · 20–40 мин | OAuth/OIDC, JWT и threat model. Возвращайтесь после первой практики. |

**Артефакт в портфолио:** [шаг сквозного проекта](../project/04_api.md). Время ориентировочное; один урок можно разделить на несколько занятий.

> **Результат модуля:** роль не заменяет проверку владельца. Начинающему: сначала [маршрут](../START_HERE.md), затем теория → упражнение → самопроверка.

Аналитик закладывает требования безопасности на старте — дешевле, чем латать потом.

<a id="lesson-base"></a>

## База и разборы

### 1. Аутентификация vs авторизация
- **AuthN** — кто ты (логин/пароль, токен, biometrics).
- **AuthZ** — что тебе можно (RBAC, ABAC, ReBAC).

### 2. OAuth 2.0 / OIDC — main flow Authorization Code + PKCE

![OAuth PKCE flow](../images_fullstack/04_oauth_code_pkce.png)

*Авторизационный код обменивается с code_verifier. PKCE связывает запрос авторизации с обменом кода; параметры безопасности проверяются отдельно.*
```
1. Клиент → /authorize?response_type=code&client_id=...&redirect_uri=...&code_challenge=...&code_challenge_method=S256&state=...
2. Пользователь логинится у Auth Server
3. Redirect с ?code=xyz
4. Клиент → /token (code + code_verifier) → access_token (JWT или opaque), при разрешённом сценарии refresh_token
5. Запросы к API: Authorization: Bearer <access_token>
```
PKCE связывает обмен кода с клиентом, создавшим code_verifier; используем S256 и точное сопоставление redirect_uri. Для OIDC дополнительно проверяем ID Token и nonce. В браузере возможен BFF: токены остаются на сервере, браузер получает HttpOnly+Secure cookie сессии и защиту от CSRF. Native-клиент хранит секреты в защищённом хранилище ОС. Cookie нельзя читать из JavaScript для формирования Bearer-заголовка; это разные архитектуры. Сроки жизни и ротация токенов — согласованные настройки, а не универсальные 5–15 минут.

### 3. JWT анатомия и ловушки
`header.payload.signature`. Типовые дыры: `alg: none`, подмена RS→HS, отсутствие проверки `aud/iss/exp`, секрет в клиенте. Проверяем подпись доверенным ключом, allowlist алгоритмов, iss/aud/exp и применимые nbf; не доверяем алгоритму из токена без проверки. Выбор asymmetric/HMAC зависит от границ доверия. JWT не шифрует payload. jti сам по себе не отзывает токен — требуется механизм отзыва и политика проверки. Claims минимальны.

### 4. RBAC модель для админки
```
roles: admin | manager | support
support: orders:read, orders:comment          ← запрет refund
manager: +orders:refund(limit 50k), users:read
admin:   *
Проверка на gateway И внутри сервиса (defense in depth).
```
Разбор инцидента: фронт скрывал кнопку «рефанд», но эндпоинт не проверял роль → любой support мог вернуть деньги через curl. Урок: проверка прав только на сервере.

### 5. OWASP Top-10 (то, что требует аналитик в ТЗ)
Injection (параметризованные запросы), Broken Access Control, Failures of Authentication, Sensitive Data Exposure (TLS, шифрование at-rest, маскирование логов), XXE, Security Misconfiguration (дефолтные пароли, открытые minio/actuator), XSS (экранирование, CSP), Insecure Design (угрозы бизнес-логики: перебор SMS-лимитов, накопление бонусов).

### 6. Хранение секретов и паролей
Пароли: bcrypt/scrypt/argon2 + salt. Секреты: Vault/SOPS или Secret с настроенными RBAC и шифрованием хранилища; base64 в Kubernetes Secret не является шифрованием. Ротация, никаких ключей в git. Не логируем карточные данные, токены и пароли; Luhn проверяет контрольную сумму, а не выполняет маскирование.

### 7. Threat modeling (STRIDE) на практике
Для «перевод между клиентами»: Spoofing (поддельная сессия) → MFA; Tampering (подмена суммы в теле) → подпись + серверный расчёт; Repudiation → аудит действий; Information Disclosure → шифрование; DoS → rate limit 10 rps/user; Elevation → RBAC-проверки. Результат — список требований, которые аналитик вносит в бэклог.

## Ссылки
- OAuth 2.0 — базовый RFC 6749: https://datatracker.ietf.org/doc/html/rfc6749
- OAuth Security BCP: https://www.rfc-editor.org/rfc/rfc9700.html
- JWT.io разбор токена (используйте только учебные токены): https://jwt.io/
- OWASP Top 10 (2021): https://owasp.org/www-project-top-ten/
- OWASP ASVS — чеклист требований безопасности: https://owasp.org/www-project-application-security-verification-standard/
- Cheatsheets: https://cheatsheetseries.owasp.org/

<a id="lesson-practice"></a>

## Практика
- [ ] Нарисуйте sequence Authorization Code + PKCE и покажите точку перехвата без PKCE.
- [ ] Проведите STRIDE для «загрузки документов пользователем» — минимум 6 угроз с мерами.
- [ ] Составьте матрицу RBAC для CRM (роли: agent, teamlead, compliance) × 10 операций.

Задание 9 практикума: [tasks](../practice/tasks.md) · [разбор RBAC+JWT](../practice/solutions/sol09_rbac_jwt.md) · шаблон [threat model](../templates/threat-model.md)
Дальше: [Модуль 7 — Тестирование и качество](../07_testing_quality/README.md)

## Закрепление: Роль не заменяет проверку владельца

**Простыми словами.** Аутентификация определяет пользователя; авторизация проверяет разрешение на конкретное действие и объект. Подписанный токен не означает, что любая операция допустима.

**Разобранный пример.** Покупатель B с валидным токеном запрашивает GET /payments/P9 покупателя A. Сервер проверяет владельца и возвращает согласованный 403 или 404 без раскрытия деталей чужого платежа.

**Самостоятельно (20–30 минут).** Составьте матрицу buyer/support/admin × просмотр, charge, refund; добавьте ограничения владельца и суммы.

**Критерии проверки.** Есть серверные проверки каждой операции, негативные сценарии чужого объекта, нет карточных данных и токенов в логах.

<details>
<summary>Самопроверка: Достаточно скрыть кнопку возврата на фронтенде?</summary>

Нет. API обязан проверить полномочия, владение/область доступа и лимит. UI помогает пользователю, но не обеспечивает запрет.

</details>

[Сквозной пример оплаты](../examples/payment/README.md) · [Первоисточники](../SOURCES.md)
