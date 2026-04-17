# Задание: Сервис питомцев - методы фильтрации

**Файл:** `backend/java/PetService.java`

## Тип конфликта: Сохранить оба

### Задание A: Добавить метод фильтрации по нескольким видам
**Расчетное время:** 8 минут

Добавьте метод для фильтрации питомцев по нескольким видам одновременно.

**Необходимые изменения:**
- После строки 62 (после метода `searchBySpecies`), добавить:
```java
    /**
     * Фильтр питомцев по нескольким видам
     */
    public List<Pet> filterBySpecies(List<String> speciesList) {
        List<Pet> results = new ArrayList<>();
        for (Pet pet : pets) {
            if (speciesList.contains(pet.getSpecies())) {
                results.add(pet);
            }
        }
        return results;
    }
```

**Обоснование:** Поддержка одновременной фильтрации по нескольким видам.

**Инструкции по выполнению:**
```bash
git checkout -b yourname/PetService/a
git add backend/java/PetService.java
git commit -m "Добавить фильтрацию по нескольким видам"
git push origin yourname/PetService/a
```

---

### Задание B: Добавить метод фильтрации по возрастному диапазону
**Расчетное время:** 8 минут

Добавьте метод для фильтрации питомцев по возрастному диапазону.

**Необходимые изменения:**
- После строки 62 (после метода `searchBySpecies`), добавить:
```java
    /**
     * Фильтр питомцев по возрастному диапазону
     */
    public List<Pet> filterByAgeRange(int minAge, int maxAge) {
        List<Pet> results = new ArrayList<>();
        for (Pet pet : pets) {
            if (pet.getAge() >= minAge && pet.getAge() <= maxAge) {
                results.add(pet);
            }
        }
        return results;
    }
```

**Обоснование:** Позволить клиентам находить питомцев в определенных возрастных диапазонах.

**Инструкции по выполнению:**
```bash
git checkout -b yourname/PetService/b
git add backend/java/PetService.java
git commit -m "Добавить фильтрацию по возрастному диапазону"
git push origin yourname/PetService/b
```

---

## Ожидаемый конфликт
Оба задания добавляют новые методы после одного и того же метода. Обе возможности фильтрации полезны.

## Стратегия разрешения
**Сохраните оба** метода - они предоставляют разные возможности фильтрации, которые могут работать вместе.