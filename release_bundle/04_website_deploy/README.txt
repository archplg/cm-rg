WEBSITE DEPLOY (crossmodelrg.org)

Содержимое:
- index.html - one-page структура
- styles.css - Archipelago design system (#3848DD синий, #38DD98 мятный)
- app.js - i18n controller
- translations.json - RU/EN/ZH контент
- README.md - подробная инструкция по деплою

ДЕПЛОЙ ВАРИАНТЫ:

Vercel (рекомендую):
  cd 04_website_deploy
  npx vercel

Netlify (drag-n-drop):
  https://app.netlify.com/drop
  Перетащить эту папку целиком

Cloudflare Pages:
  npx wrangler pages deploy . --project-name=cm-rg

После деплоя - добавить crossmodelrg.org как custom domain в дашборде хостинга.

См. 00_DEPLOY_GUIDE.md в корне для полной инструкции.
