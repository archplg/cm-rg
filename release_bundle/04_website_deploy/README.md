# crossmodelrg.org - сайт CM-RG

Статический сайт-визитка проекта Cross-Model Repertory Grid в фирменной стилистике лаборатории Archipelago. Три языка (RU, EN, ZH), переключаются капсульным переключателем в шапке. Никакого build-step, никаких зависимостей.

## Файлы

```
site_crossmodelrg/
├── index.html        - разметка (~7 KB)
├── styles.css        - дизайн-система Archipelago (~12 KB)
├── app.js            - i18n-контроллер (~5 KB)
├── translations.json - контент на 3 языках (~16 KB)
└── README.md         - этот файл
```

Итого: ~40 KB, без внешних зависимостей кроме Google Fonts (Unbounded + Manrope).

## Что соответствует стайлгайду

Реализованы все 6 паттернов из раздела «Веб-блоки и UI-паттерны»:

| Паттерн стайлгайда | Где применён |
|---|---|
| #1 Главный баннер | Hero-секция на синем фоне (#3848DD) с белыми Unbounded-заголовками |
| #2 Облако блоков | Секция «Главные открытия» - 10 разноцветных карточек на чёрном фоне |
| #3 Заголовок + акцентный блок | Контактная секция - один центрированный серый блок |
| #4 Овальные лейблы-капсулы | Используются как .pill в .what-card и .data-card |
| #5 Лейблы внутри блоков | What-секция и Data-секция - капсулы внутри серых карточек |
| #6 Нумерованные колонки | Methodology (4 колонки) и Team (3 колонки) |

Цвета строго из палитры: `#3848DD`, `#38DD98`, `#FF4D00`, `#D9D9D9`, `#000`, `#FFF`. Все радиусы - 16px (карточки) или 9999px (капсулы и кнопки).

## Шрифты

- **Unbounded** (заголовки) - доступен на Google Fonts, импортируется в index.html.
- **TT Firs Text** (основной) - **коммерческий шрифт от TypeType**, не свободен. В CSS прописан fallback на **Manrope** (близкий по характеру геометрический гротеск, доступен на Google Fonts). Если у Archipelago есть лицензия на TT Firs Text - просто положите файлы шрифта в папку `fonts/` и подключите через `@font-face` в начале `styles.css`.

## Запуск локально

Просто откройте `index.html` в браузере? **Не сработает** - `fetch('translations.json')` в `app.js` блокируется CORS-политикой для `file://` протокола. Нужен локальный HTTP-сервер:

```powershell
# Python (есть на большинстве систем):
cd C:\Users\Sergey\archipelago_cross_model\site_crossmodelrg
python -m http.server 8000
# Откройте http://localhost:8000
```

Альтернативно (если стоит Node):
```powershell
npx serve .
```

## Деплой

Поскольку всё статическое, подойдёт любой статический хостинг. Рекомендуемые опции в порядке простоты:

### Вариант 1: Vercel (рекомендую)
1. `cd site_crossmodelrg && npx vercel`
2. Привязать домен crossmodelrg.org в дашборде Vercel (Project Settings → Domains).
3. Указать у регистратора домена DNS-записи, которые покажет Vercel (обычно A или CNAME).

### Вариант 2: Netlify
1. Перетащить папку `site_crossmodelrg/` в дашборд https://app.netlify.com/drop.
2. Domains → Add custom domain → crossmodelrg.org → следовать инструкциям.

### Вариант 3: Cloudflare Pages
1. `wrangler pages deploy site_crossmodelrg/` (после авторизации).
2. Привязать домен в Cloudflare Dashboard.

### Вариант 4: GitHub Pages
1. Закоммитить папку как репо `archipelago-research/crossmodelrg-site`.
2. Settings → Pages → Source: main branch → Save.
3. CNAME-файл с содержимым `crossmodelrg.org` + DNS-настройка.

## Что нужно подкрутить перед запуском в прод

1. **Заменить URL'ы в `translations.json`**: сейчас стоят гипотетические `huggingface.co/datasets/archipelago-research/cm-rg-v2` и `github.com/archipelago-research/cm-rg` - подставить реальные после регистрации.
2. **arxiv и Zenodo ссылки**: сейчас `#` (пустые). Заполнить после публикации препринта.
3. **Дать вычитать ZH-перевод носителю**: машинный перевод на упрощённый китайский корректен по смыслу, но для финального запуска лучше проверить тон и терминологию (особенно «构念网格» и «评价多样性»).
4. **Email и контактные данные**: проверить, что `sergey@archplg.co.uk` актуален.
5. **OG-image**: добавить файл `og-image.png` (1200×630px) для красивого preview в соцсетях и twitter cards. Сейчас preview без картинки.
6. **Analytics** (опционально): добавить Plausible / Umami / Fathom через `<script>` перед `</head>`. Я бы не ставил GA - не вписывается в дух open research.
7. **robots.txt и sitemap.xml**: добавить простые файлы для SEO. Шаблоны:

```
# robots.txt
User-agent: *
Allow: /
Sitemap: https://crossmodelrg.org/sitemap.xml
```

```xml
<!-- sitemap.xml -->
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://crossmodelrg.org/</loc>
    <changefreq>monthly</changefreq>
    <priority>1.0</priority>
  </url>
</urlset>
```

## Как добавить ещё языки

В `translations.json` добавить новый ключ верхнего уровня (например, `"ja"`) с тем же набором полей. В `index.html` в `.lang-switch` добавить кнопку `<button data-lang="ja">日</button>`. В `app.js` обновить `SUPPORTED_LANGS = ["ru", "en", "zh", "ja"]`. Всё.

## Что НЕ реализовано (намеренно)

- Тёмная тема - стайлгайд не упоминает её, и hero уже на тёмном (синем) фоне.
- Анимации появления секций при скролле - можно добавить через `IntersectionObserver` за 30 строк, если хочется.
- Cookie-banner - нет аналитики и трекеров, поэтому не нужен по GDPR.

---

Уверенность: 8/10. Снимаю до 8 потому что: a) визуальный рендер графической решётки логотипа я делал по описанию из стайлгайда («треугольная форма из пересекающихся синего, зелёного и чёрного элементов»), точная геометрия из reference могла отличаться - стоит сверить с дизайн-файлом; b) китайский перевод сделан мной, не носителем - желательно вычитать.
