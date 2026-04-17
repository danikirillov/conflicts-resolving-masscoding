# Задание: Лимит результатов движка рекомендаций

**Файл:** `backend/python/recommendation_engine.py`

## Тип конфликта: Сохранить оба

### Задание A: Добавить метод трендовых товаров по категории
**Расчетное время:** 9 минут

Добавьте метод для получения трендовых товаров в определенной категории.

**Необходимые изменения:**
- после метода `get_trending_products`), добавить:
```python
    def get_trending_by_category(self, category: str, limit: int = 5) -> List[int]:
        """Получить трендовые товары в определенной категории"""
        category_products = [pid for pid, cat in self.product_categories.items() 
                            if cat == category]
        return category_products[:limit]
```

**Обоснование:** Показывать трендовые товары по категориям для лучшего таргетинга.

**Инструкции по выполнению:**
```bash
git checkout -b <твой ник или имя>/recommendation_engine/a
git add backend/python/recommendation_engine.py
git commit -m "Добавить метод трендовых товаров по категории"
git push origin <твой ник или имя>/recommendation_engine/a
```

---

### Задание B: Добавить рекомендации на основе цены
**Расчетное время:** 9 минут

Добавьте метод для рекомендации товаров в аналогичном ценовом диапазоне.

**Необходимые изменения:**
- после метода `get_trending_products`), добавить:
```python
    def get_price_range_recommendations(self, product_id: int, 
                                       tolerance: float = 0.2, limit: int = 5) -> List[int]:
        """Получить товары в аналогичном ценовом диапазоне"""
        # В реальной реализации потребуются данные о ценах
        return self.get_similar_products(product_id, limit)
```

**Обоснование:** Помочь клиентам найти альтернативы в рамках их бюджета.

**Инструкции по выполнению:**
```bash
git checkout -b <твой ник или имя>/recommendation_engine/b
git add backend/python/recommendation_engine.py
git commit -m "Добавить рекомендации на основе цены"
git push origin <твой ник или имя>/recommendation_engine/b
```

---

## Ожидаемый конфликт
Оба задания добавляют новые методы рекомендаций. Оба улучшают систему рекомендаций.

## Стратегия разрешения
**Сохраните оба** метода - они предоставляют дополняющие стратегии рекомендаций.
