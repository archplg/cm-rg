/* ============================================================
   crossmodelrg.org · i18n controller
   Loads translations.json, swaps content by data-i18n keys,
   persists user choice in localStorage.
   ============================================================ */

const SUPPORTED_LANGS = ["ru", "en", "zh"];
const DEFAULT_LANG = "ru";
const STORAGE_KEY = "cmrg.lang";

let TRANSLATIONS = null;

function detectInitialLang() {
  const saved = localStorage.getItem(STORAGE_KEY);
  if (saved && SUPPORTED_LANGS.includes(saved)) return saved;
  const browser = (navigator.language || "ru").toLowerCase().slice(0, 2);
  if (SUPPORTED_LANGS.includes(browser)) return browser;
  return DEFAULT_LANG;
}

function setLang(lang) {
  if (!SUPPORTED_LANGS.includes(lang)) lang = DEFAULT_LANG;
  document.documentElement.lang = lang;
  localStorage.setItem(STORAGE_KEY, lang);

  // Highlight active button
  document.querySelectorAll(".lang-switch button").forEach((b) => {
    b.classList.toggle("active", b.dataset.lang === lang);
  });

  if (!TRANSLATIONS) return;
  applyTranslations(TRANSLATIONS[lang]);
}

function get(path, root) {
  return path.split(".").reduce((o, k) => (o == null ? o : o[k]), root);
}

function applyTranslations(t) {
  if (!t) return;

  // Meta
  document.title = t.meta.title;
  const md = document.querySelector('meta[name="description"]');
  if (md) md.setAttribute("content", t.meta.description);

  // Walk all [data-i18n] elements with simple key path
  document.querySelectorAll("[data-i18n]").forEach((el) => {
    const key = el.getAttribute("data-i18n");
    const value = get(key, t);
    if (typeof value === "string") el.textContent = value;
  });

  // Hero stats
  const statsRoot = document.getElementById("hero-stats");
  if (statsRoot && Array.isArray(t.hero.stats)) {
    statsRoot.innerHTML = t.hero.stats
      .map(
        (s) =>
          `<div class="hero-stat"><span class="n">${escapeHtml(
            s.n
          )}</span><span class="label">${escapeHtml(s.label)}</span></div>`
      )
      .join("");
  }

  // What cards
  const whatRoot = document.getElementById("what-grid");
  if (whatRoot && Array.isArray(t.what.points)) {
    whatRoot.innerHTML = t.what.points
      .map(
        (p) => `
        <article class="what-card">
          <span class="pill">${escapeHtml(p.label)}</span>
          <h3>${escapeHtml(p.title)}</h3>
          <p>${escapeHtml(p.text)}</p>
        </article>`
      )
      .join("");
  }

  // Findings
  const findingsRoot = document.getElementById("findings-grid");
  if (findingsRoot && Array.isArray(t.findings.items)) {
    findingsRoot.innerHTML = t.findings.items
      .map(
        (f) => `
        <article class="finding">
          <span class="tag">${escapeHtml(f.tag)}</span>
          <h3>${escapeHtml(f.title)}</h3>
          <p>${escapeHtml(f.text)}</p>
        </article>`
      )
      .join("");
  }

  // Methodology steps
  const stepsRoot = document.getElementById("steps-grid");
  if (stepsRoot && Array.isArray(t.methodology.steps)) {
    stepsRoot.innerHTML = t.methodology.steps
      .map(
        (s) => `
        <article class="step">
          <span class="num">${escapeHtml(s.num)}</span>
          <h3>${escapeHtml(s.title)}</h3>
          <p>${escapeHtml(s.text)}</p>
        </article>`
      )
      .join("");
  }

  // Data cards
  const dataRoot = document.getElementById("data-grid");
  if (dataRoot && Array.isArray(t.data.blocks)) {
    dataRoot.innerHTML = t.data.blocks
      .map((b) => {
        const isLive = b.url && b.url !== "#";
        const linkAttr = isLive
          ? `href="${escapeHtml(b.url)}" target="_blank" rel="noopener"`
          : `href="#" aria-disabled="true" style="opacity:0.5;cursor:default;pointer-events:none"`;
        return `
          <article class="data-card">
            <span class="pill">${escapeHtml(b.label)}</span>
            <h3>${escapeHtml(b.name)}</h3>
            <p>${escapeHtml(b.desc)}</p>
            <a class="link" ${linkAttr}>${isLive ? "Open" : "Soon"}</a>
          </article>`;
      })
      .join("");
  }

  // Team
  const teamRoot = document.getElementById("team-grid");
  if (teamRoot && Array.isArray(t.team.blocks)) {
    teamRoot.innerHTML = t.team.blocks
      .map(
        (b) => `
        <article class="team-block">
          <span class="num">${escapeHtml(b.num)}</span>
          <h3>${escapeHtml(b.title)}</h3>
          <p>${escapeHtml(b.text)}</p>
        </article>`
      )
      .join("");
  }
}

function escapeHtml(s) {
  if (s == null) return "";
  return String(s)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");
}

async function init() {
  // Lang switcher binding
  document.querySelectorAll(".lang-switch button").forEach((b) => {
    b.addEventListener("click", () => setLang(b.dataset.lang));
  });

  // Load translations
  try {
    const res = await fetch("translations.json");
    if (!res.ok) throw new Error("HTTP " + res.status);
    TRANSLATIONS = await res.json();
  } catch (err) {
    console.error("Failed to load translations:", err);
    // Fallback: keep what's in HTML
    return;
  }

  setLang(detectInitialLang());
}

document.addEventListener("DOMContentLoaded", init);
