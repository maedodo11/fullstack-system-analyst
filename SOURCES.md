# Первоисточники и границы учебных примеров

Проверено при редактуре 8 октября 2026 года. Числа нагрузки, TTL, лимитов и стоимости в примерах — учебные допущения. Они становятся требованиями только после согласования с владельцем продукта и проверки на целевом окружении.

| Тема | Первоисточник | Что уточняет |
|---|---|---|
| SPIDR | [Mike Cohn](https://www.mountaingoatsoftware.com/blog/five-simple-but-powerful-ways-to-split-user-stories) | Spike, Paths, Interfaces, Data, Rules |
| Scrum | [Scrum Guide](https://scrumguides.org/scrum-guide.html) | Scrum — framework; Sprint ≤1 месяца, не одна задача; DoR — возможная договорённость команды |
| Качество | [ISO/IEC 25010:2023](https://www.iso.org/standard/78176.html) | Указывать редакцию; учебный NFR-чеклист не является полной моделью стандарта |
| OAuth | [RFC 9700](https://www.rfc-editor.org/rfc/rfc9700.html) | PKCE, redirect URI и современные меры защиты OAuth |
| Индексы | [PostgreSQL multicolumn indexes](https://www.postgresql.org/docs/current/indexes-multicolumn.html) | Левый префикс — эвристика; планы зависят от версии и данных |
| Миграции | [PostgreSQL ALTER TABLE](https://www.postgresql.org/docs/17/ddl-alter.html) | ADD COLUMN, NOT NULL и изменение данных имеют разные издержки |
| Браузер | [MDN CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CORS) | Запрет чтения ответа не означает запрет отправки запроса |

Для углубления: [HTTP RFC 9110](https://www.rfc-editor.org/rfc/rfc9110.html), [JWT BCP RFC 8725](https://www.rfc-editor.org/rfc/rfc8725.html), [OpenAPI 3.1](https://spec.openapis.org/oas/v3.1.0), [WCAG 2.2](https://www.w3.org/TR/WCAG22/).

Юридические требования определяются применимой юрисдикцией и согласуются со специалистом. Название закона в учебном примере не заменяет анализ применимости. Фрагменты конфигураций с многоточиями иллюстрируют идею; для запуска используйте явно отмеченные исполняемые материалы в examples/.

## Дополнение: модели и SQL

- [OMG BPMN 2.0.2](https://www.omg.org/spec/BPMN/2.0.2/) — нотация, модель и XML-обмен.
- [OMG UML 2.5.1](https://www.omg.org/spec/UML/2.5.1/) — ассоциации акторов, include и extend.
- [PostgreSQL 17 ALTER TABLE](https://www.postgresql.org/docs/17/sql-altertable.html) — блокировки и условия переписывания таблицы.
- [PostgreSQL 17 Window Functions](https://www.postgresql.org/docs/17/tutorial-window.html) — оконные функции и рамки.
- [SQLite Window Functions](https://www.sqlite.org/windowfunctions.html) — синтаксис выполняемой лаборатории.
- [bpmn-js](https://github.com/bpmn-io/bpmn-js) — импорт и экспорт BPMN-схем; зависимости и их версии зафиксированы в tools/bpmn/package-lock.json.
