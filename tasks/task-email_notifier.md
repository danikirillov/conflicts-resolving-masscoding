# Задание: Конфигурация SMTP в Email Notifier

**Файл:** `backend/python/email_notifier.py`

## Тип конфликта: Выбрать одно значение

### Задание A: Обновить SMTP порт на 465
**Расчетное время:** 5 минут

Измените SMTP порт на 465 для SSL/TLS соединения.

**Необходимые изменения:**
- Строка 13: Изменить `self.smtp_port = 587` на `self.smtp_port = 465`

**Обоснование:** Использовать SSL порт для лучшей безопасности.

**Инструкции по выполнению:**
```bash
git checkout -b yourname/email_notifier/a
git add backend/python/email_notifier.py
git commit -m "Обновить SMTP порт на 465"
git push origin yourname/email_notifier/a
```

---

### Задание B: Обновить SMTP порт на 25
**Расчетное время:** 5 минут

Измените SMTP порт на 25 для внутреннего почтового сервера.

**Необходимые изменения:**
- Строка 13: Изменить `self.smtp_port = 587` на `self.smtp_port = 25`

**Обоснование:** Внутренний почтовый сервер использует стандартный SMTP порт.

**Инструкции по выполнению:**
```bash
git checkout -b yourname/email_notifier/b
git add backend/python/email_notifier.py
git commit -m "Обновить SMTP порт на 25"
git push origin yourname/email_notifier/b
```

---

## Ожидаемый конфликт
Оба задания изменяют SMTP порт. Правильный порт зависит от конфигурации почтового сервера.

## Стратегия разрешения
**Выберите одно** на основе:
- Спецификаций почтового сервера
- Требований безопасности
- Конфигурации сети
