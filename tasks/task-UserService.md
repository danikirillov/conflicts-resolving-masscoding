# Задание: Валидация в сервисе пользователей

**Файл:** `backend/java/UserService.java`

## Тип конфликта: Сохранить оба

### Задание A: Добавить валидацию домена email
**Расчетное время:** 8 минут

Добавьте валидацию для проверки бизнес-доменов email.

**Необходимые изменения:**
- После строки 29 (после проверки существования email), добавить:
```java
        // Валидация домена email
        if (email.endsWith("@tempmail.com") || email.endsWith("@disposable.com")) {
            throw new IllegalArgumentException("Disposable email addresses not allowed");
        }
```

**Обоснование:** Предотвратить спам-аккаунты, использующие одноразовые email-сервисы.

**Инструкции по выполнению:**
```bash
git checkout -b yourname/UserService/a
git add backend/java/UserService.java
git commit -m "Добавить валидацию домена email"
git push origin yourname/UserService/a
```

---

### Задание B: Добавить валидацию силы пароля
**Расчетное время:** 8 минут

Добавьте валидацию для требований к сложности пароля.

**Необходимые изменения:**
- После строки 29 (после проверки существования email), добавить:
```java
        // Валидация силы пароля
        if (!password.matches(".*[A-Z].*") || !password.matches(".*[0-9].*")) {
            throw new IllegalArgumentException("Password must contain uppercase and numbers");
        }
```

**Обоснование:** Обеспечить более строгие требования к безопасности паролей.

**Инструкции по выполнению:**
```bash
git checkout -b yourname/UserService/b
git add backend/java/UserService.java
git commit -m "Добавить валидацию силы пароля"
git push origin yourname/UserService/b
```

---

## Ожидаемый конфликт
Оба задания добавляют логику валидации в одном месте. Обе улучшают безопасность.

## Стратегия разрешения
**Сохраните обе** валидации - они решают разные проблемы безопасности и обе должны применяться.
