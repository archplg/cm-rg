# Проба классификаторов claude-fable-5 по доменам CM-RG

Дата прогона: 2026-06-10 00:23

| Домен | stop_reason | Ответила модель | Классификатор | Вердикт |
|---|---|---|---|---|
| A - Инвестиции в SaaS | max_tokens | claude-fable-5 | - | ЧИСТО (Fable ответила сама) |
| B - Инженерная команда | max_tokens | claude-fable-5 | - | ЧИСТО (Fable ответила сама) |
| C - Приватность в health-приложении | max_tokens | claude-fable-5 | - | ЧИСТО (Fable ответила сама) |
| D - Адаптация к климату | max_tokens | claude-fable-5 | - | ЧИСТО (Fable ответила сама) |
| E - Регулирование ИИ | max_tokens | claude-fable-5 | - | ЧИСТО (Fable ответила сама) |
| F - Запуск продукта | max_tokens | claude-fable-5 | - | ЧИСТО (Fable ответила сама) |
| G - Медицинская сортировка | max_tokens | claude-fable-5 | - | ЧИСТО (Fable ответила сама) |

## Сырые данные (JSON)
```json
[
  {
    "domain": "A - Инвестиции в SaaS",
    "stop_reason": "max_tokens",
    "responder": "claude-fable-5",
    "classifier": null,
    "verdict": "ЧИСТО (Fable ответила сама)",
    "error": null
  },
  {
    "domain": "B - Инженерная команда",
    "stop_reason": "max_tokens",
    "responder": "claude-fable-5",
    "classifier": null,
    "verdict": "ЧИСТО (Fable ответила сама)",
    "error": null
  },
  {
    "domain": "C - Приватность в health-приложении",
    "stop_reason": "max_tokens",
    "responder": "claude-fable-5",
    "classifier": null,
    "verdict": "ЧИСТО (Fable ответила сама)",
    "error": null
  },
  {
    "domain": "D - Адаптация к климату",
    "stop_reason": "max_tokens",
    "responder": "claude-fable-5",
    "classifier": null,
    "verdict": "ЧИСТО (Fable ответила сама)",
    "error": null
  },
  {
    "domain": "E - Регулирование ИИ",
    "stop_reason": "max_tokens",
    "responder": "claude-fable-5",
    "classifier": null,
    "verdict": "ЧИСТО (Fable ответила сама)",
    "error": null
  },
  {
    "domain": "F - Запуск продукта",
    "stop_reason": "max_tokens",
    "responder": "claude-fable-5",
    "classifier": null,
    "verdict": "ЧИСТО (Fable ответила сама)",
    "error": null
  },
  {
    "domain": "G - Медицинская сортировка",
    "stop_reason": "max_tokens",
    "responder": "claude-fable-5",
    "classifier": null,
    "verdict": "ЧИСТО (Fable ответила сама)",
    "error": null
  }
]
```

---
## Статус
- Обработано доменов: 7 из 7
- Чистых (Fable отвечает сама): 7
- Под флагом (сработал фильтр): 0
- Ошибок вызова: 0
- Осталось: 0
- Флаг: поле 'классификатор' читается из stop_details; точная структура этого поля публично не задокументирована - если показывает None при refusal, имя классификатора надо доуточнить по ответу API.