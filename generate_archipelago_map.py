"""
Phase 2L · Archipelago Map - vintage nautical chart visualization.

Models are islands; their position reflects mutual similarity
(distance = 1 - mean Pearson r). Output: results_phase2l/archplg_phase2l_map.html

Cost: $0.
Usage: python generate_archipelago_map.py
"""
from __future__ import annotations

import json
import math
import random
import sys
from collections import defaultdict
from pathlib import Path

RESULTS_DIR = Path("./results_phase2l")
ANALYSIS_JSON = RESULTS_DIR / "analysis_results.json"
OUTPUT_HTML = RESULTS_DIR / "archplg_phase2l_map.html"

MODEL_META_SHORT_NAMES = {
    "A_C": "claude haiku 4.5", "A_M": "claude sonnet 4.6", "A_F": "claude opus 4.8",
    "O_C": "gpt-5 mini", "O_M": "gpt-5.4", "O_F": "gpt-5.5",
    "G_C": "gemini 2.5 flash lite", "G_M": "gemini 3 flash", "G_F": "gemini 3.1 pro",
    "M_C": "ministral 3b", "M_M": "mistral small 4", "M_F": "mistral medium 3.5",
    "D_C": "deepseek v4 flash", "D_M": "deepseek v3.1", "D_F": "deepseek r1",
    "X_C": "grok build 0.1", "X_M": "grok 4.3", "X_F": "grok 4.20",
    "Q_C": "qwen 2.5 7b", "Q_M": "qwen plus", "Q_F": "qwen 3.7 max",
    "K_C": "kimi k2.5", "K_M": "kimi k2 thinking", "K_F": "kimi k2.6",
    "Z_C": "glm 4.7 flash", "Z_M": "glm 4.5 air", "Z_F": "glm 5.1",
    "N_C": "nemotron nano 9b", "N_M": "nemotron super 49b", "N_F": "nemotron ultra 550b",
    "L_C": "llama 4 scout", "L_M": "llama 3.3 70b", "L_F": "llama 4 maverick",
    "C_C": "command r7b", "C_M": "command r", "C_F": "command a",
}

FAMILY_COLORS = {
    "anthropic": "#c97645", "openai": "#1e7a5f", "google": "#3a5fa8",
    "mistral": "#a85530", "deepseek": "#5040a0", "xai": "#2c2c2c",
    "qwen": "#5848d0", "moonshot": "#3a78c0", "zhipu": "#c08020",
    "nvidia": "#5a8a30", "meta": "#3a6fc0", "cohere": "#c05848",
}
FAMILY_MAP = {
    "A": "anthropic", "O": "openai", "G": "google", "M": "mistral",
    "D": "deepseek", "X": "xai", "Q": "qwen", "K": "moonshot",
    "Z": "zhipu", "N": "nvidia", "L": "meta", "C": "cohere",
}
# Tasks с описаниями
TASKS_INFO = {
    "K": {
        "title": "M&A под регуляторной неопределённостью",
        "industry": "Корпоративные финансы / право",
        "context": "Покупка fintech компании в Сингапуре. 4 юрисдикции (US, EU, Singapore, UAE) с разными правилами AI compliance. Что выбрать: спешить с deal до новых регуляций или ждать ясности?",
        "icon": "⚖️",
    },
    "L": {
        "title": "Передача семейного бизнеса по наследству",
        "industry": "Wealth management / family business",
        "context": "Основатель уходит на пенсию, 3 наследника с разными взглядами и компетенциями. Как распределить контроль и какой governance построить?",
        "icon": "👪",
    },
    "M": {
        "title": "Стратегия ответа на пандемию",
        "industry": "Public health / government",
        "context": "Правительство страны должно решить: $5 млрд на vaccine program, lockdown strategy, или экономическую поддержку. Trade-offs здоровье vs экономика.",
        "icon": "🦠",
    },
    "N_task": {
        "title": "Распределение R&D бюджета",
        "industry": "Tech / venture capital",
        "context": "$1.2 млрд на 8 emerging technologies (quantum, gene editing, AI hardware и др.). Какие приоритеты, какая структура bet'ов?",
        "icon": "🔬",
    },
    "O": {
        "title": "Кризисные коммуникации после взлома",
        "industry": "PR / cybersecurity",
        "context": "Утечка данных 50М пользователей. 24 часа на reaction strategy: что говорить, кому, в каком порядке, как минимизировать ущерб.",
        "icon": "🚨",
    },
    "P": {
        "title": "Конституционная реформа",
        "industry": "Legal / political",
        "context": "Демократическая страна обсуждает amendments к Constitution. Как balance individual rights, institutional stability, evolving values.",
        "icon": "📜",
    },
    "Q": {
        "title": "Регулирование ИИ - cross-jurisdiction",
        "industry": "Tech policy / international law",
        "context": "G7 пытаются coordinated framework для AI. EU AI Act, US executive orders, China regulations - как найти common ground.",
        "icon": "🌐",
    },
}

# Sample models to show as response examples (diverse perspectives)
SAMPLE_MODELS_PER_TASK = ["A_F", "O_F", "Q_F"]  # Anthropic, OpenAI, Qwen flagships

def load_sample_responses(results_dir):
    """Load 3 sample responses per task from Phase 1 files."""
    samples = {}
    phase1_dir = results_dir / "phase1_free_response"
    if not phase1_dir.exists():
        return samples
    for task_id in TASKS_INFO.keys():
        samples[task_id] = []
        for model_short in SAMPLE_MODELS_PER_TASK:
            cell_path = phase1_dir / task_id / "N" / f"{model_short}.json"
            if cell_path.exists():
                try:
                    data = json.loads(cell_path.read_text(encoding="utf-8"))
                    response = data.get("response", "")[:2000]
                    samples[task_id].append({
                        "model": model_short,
                        "name": MODEL_META_SHORT_NAMES.get(model_short, model_short),
                        "response": response,
                    })
                except Exception:
                    pass
    return samples


FAMILY_LEGEND = [
    ("anthropic", "Anthropic (Claude)"),
    ("openai", "OpenAI (GPT)"),
    ("google", "Google (Gemini)"),
    ("xai", "xAI (Grok)"),
    ("meta", "Meta (Llama)"),
    ("mistral", "Mistral"),
    ("deepseek", "DeepSeek"),
    ("qwen", "Qwen (Alibaba)"),
    ("moonshot", "Moonshot (Kimi)"),
    ("zhipu", "Zhipu (GLM)"),
    ("nvidia", "NVIDIA (Nemotron)"),
    ("cohere", "Cohere (Command)"),
]

# Ensemble bundles - подходящие комбинации моделей для разных индустрий/задач
# Каждый bundle = 3 модели + объяснение почему именно эти
ENSEMBLE_BUNDLES = [
    {
        "id": "corporate-legal",
        "title": "Корпоративное право и M&A",
        "subtitle": "Задачи K (M&A regulatory), P (constitutional reform), Q (AI regulation)",
        "models": ["A_F", "O_F", "G_F"],
        "rationale": "Три топ-flagship Western cluster с самым высоким взаимным consensus (r 0.32-0.38). Нужны для precision в юридических задачах где интерпретация важнее скорости.",
    },
    {
        "id": "strategy-analytics",
        "title": "Бизнес-стратегия и аналитика",
        "subtitle": "Задачи M (pandemic strategy), N (R&D portfolio)",
        "models": ["A_M", "O_M", "G_M"],
        "rationale": "Mid-tier sweet spot - дают развёрнутые аргументы за разумную цену, имеют high consensus (~0.37). Подходят для глубокого анализа без overkill.",
    },
    {
        "id": "crisis-fast",
        "title": "Кризисные коммуникации",
        "subtitle": "Задачи O (crisis comms post-breach), быстрые judgment calls",
        "models": ["G_C", "A_C", "X_C"],
        "rationale": "Самые быстрые модели (3-9 секунд на ответ) с достаточной consensus (~0.30). Когда нужно решение за минуту, а не за десять.",
    },
    {
        "id": "ethics-deep",
        "title": "Этические/значимые решения",
        "subtitle": "Задачи L (family succession), P (constitutional)",
        "models": ["A_F", "K_M", "D_F"],
        "rationale": "Reasoning-heavy модели - тратят больше времени на цепочку рассуждений. Подходят для nuanced judgment где нужна моральная глубина.",
    },
    {
        "id": "diversity-check",
        "title": "Проверка bias - кросс-кластерный ансамбль",
        "subtitle": "Любая задача где важно избежать Western-bias",
        "models": ["O_F", "Q_F", "L_F"],
        "rationale": "Один Western flagship + один Chinese flagship + один open-weights flagship. Если все три согласны - результат robust. Если расходятся - есть bias.",
    },
    {
        "id": "budget",
        "title": "Бюджетный ансамбль",
        "subtitle": "Когда нужна оценка но дорого",
        "models": ["A_C", "O_C", "G_C"],
        "rationale": "Три самых дешёвых Western cheap-tier модели. Сэкономит ~10x по сравнению с flagship ансамблем, но требует поправки на калибровку (cheap занижает).",
    },
    {
        "id": "deep-reasoning",
        "title": "Глубокий reasoning",
        "subtitle": "Когда есть время и нужно подробное обоснование",
        "models": ["D_F", "K_M", "A_F"],
        "rationale": "Три reasoning-специалиста: DeepSeek R1, Kimi Thinking, Claude Opus. Тратят 30-300 секунд но дают chains of thought. Для финальных решений.",
    },
]

# Риски моделей - простыми словами для людей не-инженеров
MODEL_RISKS = [
    {
        "id": "token-burn",
        "severity": "high",
        "title": "Долго думают, дорого",
        "models": ["D_F", "K_M", "Q_F"],
        "description": "Эти модели сначала &laquo;размышляют вслух&raquo; - пишут длинные внутренние монологи перед ответом. Один ответ может стоить в 3-5 раз дороже чем у обычной модели. Если важна цена - бери модели подешевле из той же семьи. Если важна вдумчивость и есть бюджет - используй.",
    },
    {
        "id": "empty-content",
        "severity": "critical",
        "title": "Иногда не отвечают вообще",
        "models": ["Z_F", "N_C", "N_M"],
        "description": "Эти модели иногда возвращают пустое сообщение вместо ответа. В нашем эксперименте провалились на сложных задачах. Если используешь в продукте - обязательно нужен запасной вариант (если первая модель промолчала - вызвать вторую). Без запасного плана продукт сломается.",
    },
    {
        "id": "high-latency",
        "severity": "high",
        "title": "Очень медленные",
        "models": ["K_M", "K_F", "D_F", "Q_F"],
        "description": "Отвечают 30 секунд - 5 минут. Kimi Thinking в нашем эксперименте однажды думал 75 минут над одной задачей. Не подходят для чата где пользователь ждёт ответ в реальном времени. Подходят для отчётов и аналитики, которую можно подождать.",
    },
    {
        "id": "anti-consensus",
        "severity": "medium",
        "title": "Оценивают наоборот",
        "models": ["Q_C", "N_C", "N_M", "L_M"],
        "description": "Эти модели систематически ставят низкие оценки там, где большинство других моделей ставит высокие, и наоборот. Не подходят для оценки кандидатов на работу или contentа - дадут странные результаты. Зато полезны как &laquo;адвокат дьявола&raquo; - чтобы проверить нет ли у других моделей слепых пятен.",
    },
    {
        "id": "mid-overrate",
        "severity": "medium",
        "title": "Mid-модели всё хвалят",
        "models": ["A_M", "O_M", "G_M", "M_M", "X_M", "Q_M", "K_M", "Z_M", "N_M", "L_M", "C_M"],
        "description": "Средние по цене модели (Sonnet, GPT-5.4, Llama 3.3 и др.) дают завышенные оценки - в среднем 3.89 из 7 на любое задание. Если оцениваешь кандидатов или резюме - все покажутся &laquo;хорошими&raquo;. Решение: либо отнимай 0.10 от их оценки, либо используй flagship для калибровки.",
    },
    {
        "id": "cheap-underrate",
        "severity": "medium",
        "title": "Дешёвые модели всё ругают",
        "models": ["A_C", "O_C", "G_C", "M_C", "X_C", "Q_C", "K_C", "Z_C", "N_C", "L_C", "C_C", "D_C"],
        "description": "Дешёвые модели (Haiku, GPT-5 mini и др.) дают заниженные оценки - в среднем 3.65 из 7. Если используешь для скрининга кандидатов - можешь отбраковать хороших. Решение: либо прибавляй 0.15 к их оценке, либо комбинируй с flagship.",
    },
    {
        "id": "deprecated-slug",
        "severity": "low",
        "title": "Может пропасть из доступа",
        "models": ["Z_C"],
        "description": "Изначальная версия Z_C (GLM 4 32B) была убрана провайдером прямо во время нашего эксперимента. Заменили на GLM 4.7 Flash. Урок: китайские модели меняются часто. Перед production - проверь что модель ещё доступна, и держи запасной slug.",
    },
    {
        "id": "single-language",
        "severity": "info",
        "title": "Лучше работают на родном языке",
        "models": ["Q_F", "K_F", "Z_F", "Q_M", "K_M"],
        "description": "Китайские модели Qwen и Kimi показывают лучшие результаты в задачах с китайским контекстом. Не значит что они плохи на английском или русском - но если делаешь multi-language продукт, тестируй качество отдельно на каждом языке. Не предполагай что Western flagships везде лучше.",
    },
]


def compute_distance_matrix(corrs_by_key):
    pair_corrs = defaultdict(list)
    all_models = set()
    for key, corr_dict in corrs_by_key.items():
        for pair_str, r in corr_dict.items():
            a, b = pair_str.split("|")
            if a == b:
                continue
            all_models.add(a)
            all_models.add(b)
            canonical = tuple(sorted([a, b]))
            pair_corrs[canonical].append(r)
    keys_list = list(MODEL_META_SHORT_NAMES.keys())
    models = sorted(all_models, key=lambda m: keys_list.index(m) if m in keys_list else 99)
    pair_avg = {p: sum(rs) / len(rs) for p, rs in pair_corrs.items()}
    n = len(models)
    D = [[0.0] * n for _ in range(n)]
    for i, a in enumerate(models):
        for j, b in enumerate(models):
            if i == j:
                D[i][j] = 0
            else:
                pair = tuple(sorted([a, b]))
                r = pair_avg.get(pair)
                D[i][j] = 1.5 if r is None else max(0.05, 1.0 - r)
    return models, D


def simple_mds(D, dim=2, iterations=1500, lr=0.02, seed=42):
    rng = random.Random(seed)
    n = len(D)
    positions = []
    for i in range(n):
        angle = 2 * math.pi * i / n + rng.gauss(0, 0.3)
        radius = 1.0 + rng.gauss(0, 0.1)
        positions.append([radius * math.cos(angle), radius * math.sin(angle)])

    for it in range(iterations):
        cur_lr = lr * (1 - it / iterations) ** 1.5 + 0.001
        for i in range(n):
            for j in range(n):
                if i == j:
                    continue
                dx = positions[i][0] - positions[j][0]
                dy = positions[i][1] - positions[j][1]
                cur_dist = math.sqrt(dx * dx + dy * dy) + 1e-6
                error = cur_dist - D[i][j]
                grad_x = error * dx / cur_dist
                grad_y = error * dy / cur_dist
                positions[i][0] -= cur_lr * grad_x
                positions[i][1] -= cur_lr * grad_y
                positions[j][0] += cur_lr * grad_x
                positions[j][1] += cur_lr * grad_y
    return positions


def normalize_to_canvas(positions, canvas_w=1200, canvas_h=800, margin=80):
    xs = [p[0] for p in positions]
    ys = [p[1] for p in positions]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    range_x = max_x - min_x + 1e-6
    range_y = max_y - min_y + 1e-6
    scale = min((canvas_w - 2 * margin) / range_x, (canvas_h - 2 * margin) / range_y)
    cx, cy = canvas_w / 2, canvas_h / 2
    px_center = (min_x + max_x) / 2
    py_center = (min_y + max_y) / 2
    return [(cx + (p[0] - px_center) * scale, cy + (p[1] - py_center) * scale)
            for p in positions]


def render_svg(models, coords, consensus, canvas_w=1200, canvas_h=800):
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {canvas_w} {canvas_h}" class="archipelago-svg">']
    parts.append('<defs>')
    parts.append(
        '<filter id="paperTexture" x="0" y="0" width="100%" height="100%">'
        '<feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="2" seed="3"/>'
        '<feColorMatrix values="0 0 0 0 0.85  0 0 0 0 0.78  0 0 0 0 0.6  0 0 0 0.04 0"/>'
        '<feComposite in2="SourceGraphic" operator="in"/>'
        '</filter>'
        '<radialGradient id="islandGrad">'
        '<stop offset="0%" stop-color="#fef9ee"/>'
        '<stop offset="100%" stop-color="#e8dcc0"/>'
        '</radialGradient>'
    )
    parts.append('</defs>')
    parts.append(f'<rect width="{canvas_w}" height="{canvas_h}" fill="#f0e5cf"/>')
    parts.append(f'<rect width="{canvas_w}" height="{canvas_h}" fill="url(#paperTexture)" opacity="0.7"/>')

    grid_step = 100
    for x in range(grid_step, canvas_w, grid_step):
        parts.append(f'<line x1="{x}" y1="0" x2="{x}" y2="{canvas_h}" stroke="#a8c3d0" stroke-width="0.5" opacity="0.6"/>')
    for y in range(grid_step, canvas_h, grid_step):
        parts.append(f'<line x1="0" y1="{y}" x2="{canvas_w}" y2="{y}" stroke="#a8c3d0" stroke-width="0.5" opacity="0.6"/>')

    longitudes = []
    for x in range(grid_step, canvas_w, grid_step):
        if abs(x - canvas_w / 2) > 10:
            deg = (x - canvas_w / 2) // grid_step * 4
            longitudes.append((x, f"{abs(deg):.0f}°{'W' if x < canvas_w / 2 else 'E'}"))
    longitudes.append((canvas_w / 2, "0°"))
    for x, label in longitudes:
        parts.append(
            f'<text x="{x}" y="22" text-anchor="middle" fill="#1e3a5f" '
            f'font-family="Cormorant Garamond, serif" font-size="13" letter-spacing="2">{label}</text>'
        )
    for y in range(grid_step, canvas_h, grid_step):
        parts.append(
            f'<text x="20" y="{y + 5}" text-anchor="start" fill="#1e3a5f" '
            f'font-family="Cormorant Garamond, serif" font-size="13" letter-spacing="2">'
            f'{38 + (canvas_h - y) // grid_step:.0f}°N</text>'
        )

    cx, cy = canvas_w - 70, 80
    parts.append(
        f'<g transform="translate({cx},{cy})">'
        f'<circle r="30" fill="none" stroke="#1e3a5f" stroke-width="0.8"/>'
        f'<text x="0" y="-22" text-anchor="middle" fill="#1e3a5f" font-family="Cormorant Garamond, serif" font-size="11">N</text>'
        f'<text x="22" y="3" text-anchor="middle" fill="#1e3a5f" font-family="Cormorant Garamond, serif" font-size="11">E</text>'
        f'<text x="0" y="28" text-anchor="middle" fill="#1e3a5f" font-family="Cormorant Garamond, serif" font-size="11">S</text>'
        f'<text x="-22" y="3" text-anchor="middle" fill="#1e3a5f" font-family="Cormorant Garamond, serif" font-size="11">W</text>'
        f'<line x1="0" y1="-18" x2="0" y2="18" stroke="#1e3a5f" stroke-width="0.5"/>'
        f'<line x1="-18" y1="0" x2="18" y2="0" stroke="#1e3a5f" stroke-width="0.5"/>'
        f'<polygon points="0,-18 -3,-6 0,-10 3,-6" fill="#1e3a5f"/>'
        f'</g>'
    )

    parts.append(
        '<g transform="translate(40, 50)">'
        '<rect width="280" height="125" fill="#f7eed8" stroke="#c97645" stroke-width="1.5" rx="2"/>'
        '<rect x="3" y="3" width="274" height="119" fill="none" stroke="#c97645" stroke-width="0.4" rx="1"/>'
        '<text x="14" y="28" fill="#1e3a5f" font-family="Cormorant Garamond, serif" font-size="13" letter-spacing="3.5" font-weight="600">КАРТА ТРИДЦАТИ ШЕСТИ</text>'
        '<text x="14" y="50" fill="#5a4a3a" font-family="Cormorant Garamond, serif" font-style="italic" font-size="11">Архипелаг моделей · CM-RG Phase 2L</text>'
        '<line x1="14" y1="58" x2="266" y2="58" stroke="#c97645" stroke-width="0.4"/>'
        '<text x="14" y="76" fill="#1e3a5f" font-family="Cormorant Garamond, serif" font-size="11">Остров - модель.</text>'
        '<text x="14" y="91" fill="#1e3a5f" font-family="Cormorant Garamond, serif" font-size="11">Расстояние - измеренное расхождение</text>'
        '<text x="14" y="106" fill="#1e3a5f" font-family="Cormorant Garamond, serif" font-size="11">в оценках на 7 advisory задачах.</text>'
        '</g>'
    )

    sx, sy = canvas_w // 2 - 100, canvas_h - 50
    parts.append(
        f'<g transform="translate({sx},{sy})">'
        f'<rect x="0" y="0" width="50" height="6" fill="#1e3a5f"/>'
        f'<rect x="50" y="0" width="50" height="6" fill="#f0e5cf" stroke="#1e3a5f" stroke-width="0.5"/>'
        f'<rect x="100" y="0" width="50" height="6" fill="#1e3a5f"/>'
        f'<rect x="150" y="0" width="50" height="6" fill="#f0e5cf" stroke="#1e3a5f" stroke-width="0.5"/>'
        f'<text x="100" y="22" text-anchor="middle" fill="#c97645" font-family="Cormorant Garamond, serif" font-size="10" letter-spacing="3">ЕДИНИЦЫ РАСХОЖДЕНИЯ</text>'
        f'</g>'
    )

    parts.append(
        f'<text x="{canvas_w // 2}" y="{canvas_h - 18}" text-anchor="middle" fill="#1e3a5f" '
        f'font-family="Cormorant Garamond, serif" font-style="italic" font-size="11">'
        f'Лист I - MDS-проекция усреднённых корреляций 14 (task × condition) комбинаций.</text>'
    )

    # Concentric "consensus radius" guides - subtle dashed circles, horizontal labels on right
    map_cx, map_cy = canvas_w // 2, canvas_h // 2
    for r, label, op in [(80, "ядро", 0.75), (180, "переходная", 0.6), (280, "периферия", 0.5)]:
        parts.append(
            f'<circle cx="{map_cx}" cy="{map_cy}" r="{r}" fill="none" '
            f'stroke="#c97645" stroke-width="1.2" stroke-dasharray="6 5" opacity="{op}"/>'
        )
        # Horizontal label to the right of each ring
        parts.append(
            f'<text x="{map_cx + r + 8}" y="{map_cy + 4}" text-anchor="start" '
            f'fill="#c97645" font-family="Cormorant Garamond, serif" '
            f'font-size="11" letter-spacing="2" font-style="italic" font-weight="600" '
            f'opacity="{min(op + 0.15, 1.0)}">{label}</text>'
        )

    # Center marker - небольшой но заметный
    parts.append(
        f'<g>'
        f'<circle cx="{map_cx}" cy="{map_cy}" r="5" fill="#c97645" opacity="0.85"/>'
        f'<circle cx="{map_cx}" cy="{map_cy}" r="10" fill="none" stroke="#c97645" stroke-width="1.2" opacity="0.6"/>'
        f'<text x="{map_cx}" y="{map_cy - 18}" text-anchor="middle" '
        f'fill="#c97645" font-family="Cormorant Garamond, serif" '
        f'font-size="11" letter-spacing="3" font-weight="600" font-style="italic">ядро консенсуса</text>'
        f'</g>'
    )

    # Axis labels - объяснение что значит расстояние
    parts.append(
        f'<g opacity="0.6">'
        # Top axis - "ПЕРИФЕРИЯ ←"
        f'<text x="{map_cx}" y="50" text-anchor="middle" '
        f'fill="#1e3a5f" font-family="Cormorant Garamond, serif" '
        f'font-size="10" letter-spacing="4" font-style="italic">↑ ПЕРИФЕРИЯ</text>'
        # Bottom axis label
        f'<text x="{map_cx}" y="{canvas_h - 65}" text-anchor="middle" '
        f'fill="#1e3a5f" font-family="Cormorant Garamond, serif" '
        f'font-size="10" letter-spacing="4" font-style="italic">↓ ПЕРИФЕРИЯ</text>'
        # Left axis
        f'<text x="50" y="{map_cy}" text-anchor="middle" transform="rotate(-90, 50, {map_cy})" '
        f'fill="#1e3a5f" font-family="Cormorant Garamond, serif" '
        f'font-size="10" letter-spacing="4" font-style="italic">← ПЕРИФЕРИЯ</text>'
        # Right axis
        f'<text x="{canvas_w - 50}" y="{map_cy}" text-anchor="middle" transform="rotate(90, {canvas_w - 50}, {map_cy})" '
        f'fill="#1e3a5f" font-family="Cormorant Garamond, serif" '
        f'font-size="10" letter-spacing="4" font-style="italic">ПЕРИФЕРИЯ →</text>'
        f'</g>'
    )

    indexed = sorted(enumerate(models), key=lambda iy: -consensus.get(iy[1], 0))
    for idx, model_id in indexed:
        x, y = coords[idx]
        c = consensus.get(model_id, 0)
        radius = 6 + max(0, c) * 30
        family = FAMILY_MAP.get(model_id[0], "unknown")
        color = FAMILY_COLORS.get(family, "#1e3a5f")
        # Multiple event handlers for maximum compatibility - mousedown is most reliable
        click_attr = 'onclick="window.openModalFor(this); return false;" onmousedown="window.openModalFor(this); return false;" onpointerdown="window.openModalFor(this); return false;"'
        parts.append(
            f'<g class="island" data-id="{model_id}" '
            f'data-name="{MODEL_META_SHORT_NAMES.get(model_id, model_id)}" '
            f'data-family="{family}" data-consensus="{c:.3f}" '
            f'{click_attr} '
            f'style="cursor: pointer; pointer-events: all;">'
            # INVISIBLE BIG hit target with multiple event types
            f'<rect x="{x - 50:.1f}" y="{y - 25:.1f}" width="100" height="55" '
            f'fill="white" fill-opacity="0.001" pointer-events="all" {click_attr}/>'
            # Outer dashed ring (visual only)
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{radius + 2:.1f}" fill="none" '
            f'stroke="{color}" stroke-width="0.8" stroke-dasharray="2 2" opacity="0.5" '
            f'pointer-events="none"/>'
            # Visible filled circle - also clickable
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{radius:.1f}" fill="url(#islandGrad)" '
            f'stroke="{color}" stroke-width="1.4" pointer-events="all" {click_attr}/>'
        )
        label = MODEL_META_SHORT_NAMES.get(model_id, model_id).upper()
        label_y = y + radius + 14
        if y > canvas_h * 0.85:
            label_y = y - radius - 6
        parts.append(
            f'<text x="{x:.1f}" y="{label_y:.1f}" text-anchor="middle" fill="#1e3a5f" '
            f'font-family="Cormorant Garamond, serif" font-size="11" letter-spacing="1.5">{label}</text>'
            f'</g>'
        )

    parts.append('</svg>')
    return "".join(parts)


def build_model_descriptions(consensus):
    family_descriptions = {
        "anthropic": "Anthropic - известна осторожным RLHF, ориентирована на безопасность и nuance в judgment задачах.",
        "openai": "OpenAI - центральный игрок Western alignment cluster, эталон калибровки.",
        "google": "Google DeepMind - сильна в многошаговом reasoning, иногда смещена в академическую формальность.",
        "mistral": "Mistral AI - европейский игрок, баланс эффективности и качества, более лёгкая калибровка.",
        "deepseek": "DeepSeek - сильна в reasoning через цепочку мысли, R1 - reasoning-flagship не chat-flagship.",
        "xai": "xAI - сравнительно молодая семья, ориентация на live data и провокационный стиль.",
        "qwen": "Alibaba Qwen - крупный китайский игрок, переходит от open-weights традиции к Western alignment.",
        "moonshot": "Moonshot Kimi - долгий контекст и reasoning, фокус на китайском рынке.",
        "zhipu": "Zhipu GLM - академический китайский проект, более sober оценки.",
        "nvidia": "NVIDIA Nemotron - модели обученные NVIDIA на foundation Llama, технически-инженерный уклон.",
        "meta": "Meta Llama - open-weights флагман, mid использовал Llama 3.3 (предыдущее поколение).",
        "cohere": "Cohere - корпоративный игрок, фокус на enterprise tasks, осторожная калибровка.",
    }
    tier_descriptions = {
        "cheap": "Cheap-tier модель. Cheap raters систематически дают **более низкие** оценки (средний 3.65 из 7).",
        "mid": "Mid-tier модель. Mid raters систематически дают **более высокие** оценки (средний 3.89 из 7).",
        "flagship": "Flagship модель. Сбалансированная калибровка (средняя оценка 3.80 из 7).",
    }
    tier_map = {"C": "cheap", "M": "mid", "F": "flagship"}
    descriptions = {}
    sorted_by_c = sorted(consensus.items(), key=lambda kv: -kv[1])
    ranks = {m: rank for rank, (m, _) in enumerate(sorted_by_c)}
    n = len(sorted_by_c)
    tier_simple = {
        "cheap": "Это **дешёвая** модель - быстрая и недорогая, но обычно строже оценивает (даёт более низкие баллы в среднем 3.65 из 7).",
        "mid": "Это **средняя** модель - баланс цены и качества, но систематически даёт более высокие оценки (в среднем 3.89 из 7) - может казаться 'слишком доброй'.",
        "flagship": "Это **флагман** - самая дорогая, обычно даёт самые сбалансированные оценки (3.80 из 7).",
    }
    for short, c in consensus.items():
        family = FAMILY_MAP.get(short[0], "unknown")
        tier = tier_map.get(short[1], "")
        rank = ranks.get(short, 99) + 1
        tier_extra = tier_simple.get(tier, "")
        if c >= 0.30:
            position = (
                f"**Эта модель в центре карты - в ядре согласия.** "
                f"Её оценки очень похожи на оценки GPT-5.5, Claude Opus, Gemini 3.1 Pro и других топ-моделей "
                f"Западного кластера. Можно сказать что она говорит на 'общем языке' современных ИИ-судей. "
                f"{tier_extra}"
            )
        elif c >= 0.15:
            position = (
                f"**Промежуточная позиция между центром и периферией.** "
                f"Эта модель частично согласна с большинством, но имеет собственный взгляд на оценки. "
                f"Полезна когда хочешь проверить mainstream выводы альтернативной перспективой. "
                f"{tier_extra}"
            )
        elif c >= 0.0:
            position = (
                f"**На периферии карты - слабое согласие с большинством.** "
                f"Эта модель оценивает довольно иначе чем mainstream. Не обязательно неправильно - "
                f"просто использует другие критерии. Полезна как 'второе мнение'. "
                f"{tier_extra}"
            )
        else:
            position = (
                f"**Антипод консенсуса - на дальней периферии.** "
                f"Эта модель часто оценивает **противоположно** большинству - где другие ставят высокий балл, "
                f"она ставит низкий, и наоборот. Это не баг - это альтернативная система ценностей. "
                f"Полезна как red team для проверки слепых пятен mainstream моделей. "
                f"{tier_extra}"
            )
        descriptions[short] = {
            "family_text": family_descriptions.get(family, ""),
            "tier_text": tier_descriptions.get(tier, ""),
            "position_text": position,
            "consensus_rank": f"{rank} из {n}",
            "consensus_score": c,
        }
    return descriptions


def build_html(svg, models, descriptions, task_samples=None):
    task_samples = task_samples or {}
    legend_html = ""
    for fam_id, name in FAMILY_LEGEND:
        color = FAMILY_COLORS[fam_id]
        legend_html += (
            f'<div class="legend-item" data-family="{fam_id}">'
            f'<span class="legend-swatch" style="background: {color}"></span>'
            f'<span class="legend-name">{name}</span></div>'
        )
    # Ensemble bundles - кликабельные ансамбли для индустрий
    bundles_html = ""
    for b in ENSEMBLE_BUNDLES:
        models_str = " · ".join(b["models"])
        bundles_html += (
            f'<div class="bundle-item" data-bundle="{b["id"]}">'
            f'<div class="bundle-title">{b["title"]}</div>'
            f'<div class="bundle-subtitle">{b["subtitle"]}</div>'
            f'<div class="bundle-models">{models_str}</div>'
            f'<div class="bundle-rationale">{b["rationale"]}</div>'
            f'</div>'
        )
    # Render risks block
    risks_html = ""
    severity_colors = {"critical": "#ef4444", "high": "#f97316", "medium": "#fbbf24", "low": "#84cc16", "info": "#60a5fa"}
    severity_labels = {"critical": "КРИТИЧНО", "high": "ВЫСОКИЙ", "medium": "СРЕДНИЙ", "low": "НИЗКИЙ", "info": "К СВЕДЕНИЮ"}
    for r in MODEL_RISKS:
        sev_color = severity_colors.get(r["severity"], "#888")
        sev_label = severity_labels.get(r["severity"], r["severity"])
        models_str = " · ".join(r["models"])
        risks_html += (
            f'<div class="risk-item" data-risk="{r["id"]}" style="border-left-color: {sev_color};">'
            f'<div class="risk-header">'
            f'<span class="risk-severity" style="background: {sev_color};">{sev_label}</span>'
            f'<span class="risk-title">{r["title"]}</span>'
            f'</div>'
            f'<div class="risk-models">{models_str}</div>'
            f'<div class="risk-description">{r["description"]}</div>'
            f'</div>'
        )

    # Build task cards grid
    tasks_grid_html = ""
    for task_id, info in TASKS_INFO.items():
        tasks_grid_html += (
            f'<div class="task-card" data-task="{task_id}" onclick="window.openTaskModalFor(\'{task_id}\')">'
            f'<div class="task-icon">{info["icon"]}</div>'
            f'<div class="task-card-title">{info["title"]}</div>'
            f'<div class="task-card-industry">{info["industry"]}</div>'
            f'</div>'
        )
    # Build tasks data with samples for JS
    tasks_data = {}
    for tid, info in TASKS_INFO.items():
        tasks_data[tid] = {
            "title": info["title"],
            "industry": info["industry"],
            "context": info["context"],
            "icon": info["icon"],
            "samples": task_samples.get(tid, []),
        }
    tasks_json = json.dumps(tasks_data, ensure_ascii=False)

    descriptions_json = json.dumps(descriptions, ensure_ascii=False)
    bundles_json = json.dumps({b["id"]: b for b in ENSEMBLE_BUNDLES}, ensure_ascii=False)
    risks_json = json.dumps({r["id"]: r for r in MODEL_RISKS}, ensure_ascii=False)
    n_models = len(models)

    css = """
  body { margin: 0; padding: 30px; background: #2c2519; min-height: 100vh; font-family: 'Cormorant Garamond', serif; color: #f0e5cf; }
  .container { max-width: 1280px; margin: 0 auto; }
  .header { text-align: center; padding: 20px 0; }
  .header h1 { margin: 0 0 6px; font-size: 26px; letter-spacing: 4px; font-weight: 400; }
  .header p { margin: 0; font-style: italic; opacity: 0.7; font-size: 14px; }
  .tasks-section { margin: 30px 0; padding: 24px; background: #1e1a14; border-radius: 4px; border-left: 3px solid #c97645; }
  .tasks-section h3 { margin: 0 0 6px; font-size: 14px; color: #c97645; letter-spacing: 2px; text-transform: uppercase; font-weight: 600; }
  .tasks-section .subtitle { margin: 0 0 16px; font-size: 12px; color: #8a7d6a; font-style: italic; }
  .tasks-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 10px; }
  .task-card { background: #2c2519; padding: 14px 16px; border-radius: 4px; cursor: pointer; transition: all 0.2s; border-left: 3px solid #c97645; }
  .task-card:hover { background: #3a3024; border-left-color: #f0c79a; transform: translateY(-2px); }
  .task-icon { font-size: 20px; margin-bottom: 6px; }
  .task-card-title { font-size: 13px; font-weight: 600; color: #f0e5cf; margin-bottom: 4px; line-height: 1.3; }
  .task-card-industry { font-size: 11px; color: #c97645; font-style: italic; letter-spacing: 1px; }

  /* Task modal - full page overlay */
  .task-modal-overlay { position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(20, 15, 10, 0.92); display: none; align-items: center; justify-content: center; z-index: 10000; padding: 20px; box-sizing: border-box; overflow-y: auto; }
  .task-modal-overlay.open { display: flex; }
  .task-modal { background: #f0e5cf; color: #1e3a5f; max-width: 880px; width: 92%; border: 4px solid #c97645; box-shadow: 0 0 0 8px #2c2519, 0 30px 60px rgba(0,0,0,0.8); padding: 32px 36px; max-height: 90vh; overflow-y: auto; font-family: 'Cormorant Garamond', serif; position: relative; }
  .task-modal h2 { margin: 0 0 6px; font-size: 22px; color: #1e3a5f; letter-spacing: 1px; }
  .task-modal .task-modal-industry { font-style: italic; color: #c97645; margin-bottom: 14px; font-size: 13px; letter-spacing: 1.5px; text-transform: uppercase; }
  .task-modal .task-modal-context { background: #f7eed8; border-left: 3px solid #c97645; padding: 14px 18px; margin: 14px 0 24px; font-size: 14px; line-height: 1.6; color: #1e3a5f; }
  .task-modal h3 { margin: 22px 0 12px; font-size: 14px; color: #c97645; letter-spacing: 2px; text-transform: uppercase; font-weight: 600; }
  .task-response { background: #fff8e7; border: 1px solid #d4c8b0; padding: 14px 18px; margin: 12px 0; border-radius: 3px; }
  .task-response-author { font-size: 12px; color: #c97645; font-weight: 600; letter-spacing: 1px; margin-bottom: 8px; text-transform: uppercase; }
  .task-response-text { font-size: 13px; line-height: 1.6; color: #2c2519; white-space: pre-wrap; }

  .map-container { position: relative; }
  .map-frame { background: #f0e5cf; box-shadow: 0 10px 40px rgba(0,0,0,0.6), 0 0 0 4px #2c2519, 0 0 0 8px #c97645, 0 0 0 12px #2c2519; padding: 8px; }
  /* Map-only modal overlay - covers only the map, not the whole page */
  .map-modal-overlay { position: absolute; top: 0; left: 0; right: 0; bottom: 0; background: rgba(20, 15, 10, 0.85); display: none; align-items: center; justify-content: center; z-index: 100; padding: 20px; box-sizing: border-box; backdrop-filter: blur(2px); }
  .map-modal-overlay.open { display: flex; }
  .map-modal-overlay .modal { max-height: 90%; }
  .archipelago-svg { display: block; width: 100%; height: auto; }
  .island { cursor: pointer; transition: opacity 0.2s; }
  .island.dim { opacity: 0.15; }
  .island:hover circle:last-of-type { stroke-width: 2.8; }
  .legend { margin: 30px 0; padding: 24px; background: #1e1a14; border: 1px solid #3a3024; border-radius: 4px; }
  .legend h3 { margin: 0 0 12px; font-size: 13px; letter-spacing: 3px; color: #c97645; text-transform: uppercase; font-weight: 400; }
  .legend-row { display: flex; flex-wrap: wrap; gap: 12px; margin-bottom: 18px; }
  .legend-item { display: flex; align-items: center; gap: 8px; cursor: pointer; padding: 6px 12px; background: #2c2519; border-radius: 4px; transition: background 0.15s; }
  .legend-item:hover { background: #3a3024; }
  .legend-item.active { background: #c97645; color: #2c2519; }
  .legend-item.active .legend-name { color: #2c2519; }
  .legend-swatch { width: 14px; height: 14px; border-radius: 50%; flex-shrink: 0; border: 1.5px solid #f0e5cf; }
  .legend-name { font-size: 13px; color: #f0e5cf; font-family: 'Cormorant Garamond', serif; }
  .legend-section-title { font-size: 11px; color: #8a7d6a; letter-spacing: 2px; margin: 8px 0 6px; text-transform: uppercase; }
  .size-scale { display: flex; gap: 24px; align-items: end; padding: 12px 0; }
  .size-scale-item { text-align: center; }
  .size-scale-circle { background: #f0e5cf; border: 2px solid #c97645; border-radius: 50%; margin: 0 auto 6px; }
  .size-scale-label { font-size: 11px; color: #c0b5a0; font-style: italic; }
  .narrative { margin: 30px 0; padding: 30px; background: #1e1a14; border-left: 4px solid #c97645; border-radius: 4px; line-height: 1.7; }
  .narrative h2 { margin: 0 0 16px; font-size: 22px; letter-spacing: 2px; color: #c97645; font-weight: 400; }
  .narrative h3 { margin: 24px 0 10px; font-size: 16px; color: #f0e5cf; font-weight: 600; letter-spacing: 1px; }
  .narrative p { margin: 12px 0; color: #d4c8b0; font-size: 15px; }
  .narrative strong { color: #f0e5cf; }
  .narrative .finding { border-left: 2px solid #5a4a3a; padding-left: 16px; margin: 16px 0; }
  .narrative .finding-num { color: #c97645; font-weight: 600; font-size: 13px; letter-spacing: 2px; }
  .footer { text-align: center; color: #c97645; padding: 24px 0; font-style: italic; font-size: 13px; opacity: 0.8; }
  /* Modal - works as standalone div (not dialog) */
  .modal { background: #f0e5cf; color: #1e3a5f; max-width: 540px; width: 90%; border: 4px solid #c97645; box-shadow: 0 0 0 8px #2c2519, 0 30px 60px rgba(0,0,0,0.8); padding: 32px; max-height: 85vh; overflow-y: auto; font-family: 'Cormorant Garamond', serif; line-height: 1.6; position: relative; }
  .modal-backdrop { display: none; } /* legacy, no longer used */
  .modal h2 { margin: 0 0 8px; font-size: 22px; color: #1e3a5f; letter-spacing: 1px; }
  .modal .subtitle { font-style: italic; color: #5a4a3a; margin-bottom: 18px; font-size: 14px; }
  .modal h3 { margin: 20px 0 8px; font-size: 14px; color: #c97645; letter-spacing: 2px; text-transform: uppercase; font-weight: 600; }
  .modal p { margin: 8px 0; font-size: 14px; }
  .modal strong { color: #c97645; }
  .modal-close { position: absolute; top: 16px; right: 20px; background: #c97645; border: none; color: #2c2519; font-size: 24px; cursor: pointer; width: 32px; height: 32px; border-radius: 50%; line-height: 0; display: flex; align-items: center; justify-content: center; font-weight: bold; }
  .modal-close:hover { background: #1e3a5f; color: #f0e5cf; }
  .modal-hint { position: absolute; bottom: 12px; left: 32px; right: 32px; text-align: center; font-size: 11px; color: #8a7d6a; font-style: italic; letter-spacing: 1px; }
  .modal-rank { display: inline-block; background: #1e3a5f; color: #f0e5cf; padding: 2px 10px; border-radius: 3px; font-size: 12px; letter-spacing: 1px; }
  .bundles { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 12px; margin-top: 8px; }
  .bundle-item { padding: 14px 16px; background: #2c2519; border-left: 3px solid #c97645; border-radius: 4px; cursor: pointer; transition: all 0.2s; }
  .bundle-item:hover { background: #3a3024; border-left-color: #f0c79a; }
  .bundle-item.active { background: #c97645; border-left-color: #f0e5cf; }
  .bundle-item.active .bundle-title, .bundle-item.active .bundle-subtitle, .bundle-item.active .bundle-models, .bundle-item.active .bundle-rationale { color: #2c2519; }
  .bundle-title { font-size: 14px; font-weight: 600; color: #c97645; letter-spacing: 1px; margin-bottom: 4px; }
  .bundle-subtitle { font-size: 11px; color: #8a7d6a; font-style: italic; margin-bottom: 8px; }
  .bundle-models { font-size: 13px; color: #f0e5cf; font-family: 'SF Mono', monospace; letter-spacing: 2px; margin-bottom: 6px; }
  .bundle-rationale { font-size: 12px; color: #c0b5a0; line-height: 1.5; }
  .risks { display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 10px; margin-top: 8px; }
  .risk-item { padding: 12px 14px; background: #2c2519; border-left: 4px solid #888; border-radius: 4px; cursor: pointer; transition: all 0.2s; }
  .risk-item:hover { background: #3a3024; }
  .risk-item.active { background: #c97645; }
  .risk-item.active .risk-title, .risk-item.active .risk-models, .risk-item.active .risk-description { color: #2c2519; }
  .risk-header { display: flex; align-items: center; gap: 8px; margin-bottom: 6px; }
  .risk-severity { display: inline-block; padding: 2px 6px; font-size: 9px; font-weight: 700; color: #2c2519; border-radius: 3px; letter-spacing: 1.5px; font-family: SF Mono, monospace; }
  .risk-title { font-size: 13px; font-weight: 600; color: #f0e5cf; letter-spacing: 0.5px; }
  .risk-models { font-size: 12px; color: #c0b5a0; font-family: SF Mono, monospace; letter-spacing: 2px; margin-bottom: 6px; }
  .risk-description { font-size: 11px; color: #a89c80; line-height: 1.5; }
"""

    narrative = """
    <h2>Что мы увидели</h2>

    <p>Мы попросили 36 ИИ оценить ответы друг друга на 7 сложных бизнес-задач. Получилось 2.6 миллиона оценок. Вот три главные находки.</p>

    <div class="finding">
      <div class="finding-num">1. ИИ НЕ СОГЛАСНЫ ДРУГ С ДРУГОМ</div>
      <p style="font-size: 16px;">Если десять моделей оценят один и тот же ответ - они дадут <strong>совершенно разные числа</strong>. Корреляция между ними всего 0.21. Это значит: <strong>миф об объективном ИИ-судье - это миф</strong>.</p>
    </div>

    <div class="finding">
      <div class="finding-num">2. ЕСТЬ "ЗАПАДНЫЙ КЛУБ"</div>
      <p style="font-size: 16px;">GPT-5.5, Claude, Gemini, Grok - <strong>оценивают похоже друг на друга</strong>. Они в центре карты, в одном кластере. Это самые крупные острова. Их объединяет схожее обучение - они говорят на одном языке оценок.</p>
    </div>

    <div class="finding">
      <div class="finding-num">3. ЕСТЬ "ПРОТИВОПОЛОЖНЫЕ"</div>
      <p style="font-size: 16px;">Qwen 2.5 7B, Nemotron, Llama 3.3 - <strong>оценивают наоборот</strong>. Где Западный клуб видит сильный ответ, эти модели видят слабый. Они <strong>не сломаны</strong> - у них просто другая система ценностей.</p>
    </div>

    <h3>Что это значит на практике</h3>

    <p>
      <strong>Выбираешь ИИ для оценки кандидатов?</strong> Cheap-модель будет занижать,
      mid-модель завышать, только flagship даёт балансированную оценку (3.65 / 3.89 / 3.80
      в среднем по шкале 1-7).
    </p>
    <p>
      <strong>Делаешь ансамбль из нескольких ИИ?</strong> Anthropic + OpenAI + Google ≈
      один голос. Это всё Западный клуб. Для реального разнообразия нужны модели из
      <strong>разных кластеров</strong>.
    </p>
    <p>
      <strong>Думаешь &laquo;ИИ объективнее людей&raquo;?</strong> Не объективнее. Просто
      у разных ИИ разные субъективности - и они расходятся между собой ничуть не меньше
      чем разные группы людей.
    </p>

    <h3>Как читать карту</h3>
    <ul style="color: #d4c8b0; font-size: 15px; line-height: 1.8;">
      <li><strong>Близкие острова</strong> - модели согласны в оценках</li>
      <li><strong>Далёкие острова</strong> - разные системы судей</li>
      <li><strong>Большой остров</strong> - модель в центре консенсуса (с ней многие согласны)</li>
      <li><strong>Маленький остров</strong> - модель на периферии (с ней мало кто согласен)</li>
      <li><strong>Цвет</strong> - семья производителя (Anthropic оранжевый, OpenAI зелёный, etc.)</li>
      <li><strong>Кликни на остров</strong> - откроется детальная карточка модели</li>
      <li><strong>Кликни на семью в легенде</strong> - другие острова потускнеют</li>
    </ul>
"""

    js_template = r"""
window.addEventListener('error', function(e) {
  console.error('GLOBAL ERROR:', e.message, 'at', e.filename, ':', e.lineno);
  var bar = document.getElementById('debug-bar');
  if (bar) bar.textContent = 'JS ERROR: ' + e.message;
});

// GLOBAL functions - called from inline onclick attributes on islands
window.DESCRIPTIONS = {};
window.BUNDLES = {};
window.RISKS = {};

window.openModalFor = function(el) {
  try {
    var id = el.getAttribute('data-id') || '';
    var name = el.getAttribute('data-name') || id;
    var cAttr = el.getAttribute('data-consensus') || '0';
    var c = parseFloat(cAttr) || 0;
    var desc = window.DESCRIPTIONS[id] || {};
    var tierMap = {C: 'Cheap-tier', M: 'Mid-tier', F: 'Flagship'};
    var tier = tierMap[id[1]] || '';

    function md(s) {
      if (s == null) return '';
      return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
    }

    document.getElementById('modal-title').textContent = (name || id).toUpperCase();
    document.getElementById('modal-subtitle').textContent = id + ' | ' + tier + ' | ранг ' + (desc.consensus_rank || '-');
    document.getElementById('modal-rank').textContent = 'Согласие с другими: ' + c.toFixed(3);
    document.getElementById('modal-position').innerHTML = md(desc.position_text || 'Нет данных');
    document.getElementById('modal-tier').innerHTML = md(desc.tier_text || 'Нет данных');
    document.getElementById('modal-family').textContent = desc.family_text || 'Нет данных';

    // Show map-only overlay (covers only map area, not whole viewport)
    var overlay = document.getElementById('map-modal-overlay');
    if (overlay) {
      overlay.classList.add('open');
      overlay.style.display = 'flex';
      // Scroll map into view if needed
      overlay.scrollIntoView({behavior: 'smooth', block: 'nearest'});
    }

    var bar = document.getElementById('debug-bar');
    if (bar) bar.textContent = 'Modal opened for ' + id;
  } catch (err) {
    console.error('openModalFor failed:', err);
    alert('Click registered on ' + (el.getAttribute('data-id') || 'unknown') + '\nError: ' + err.message);
  }
  return false;
};

window.closeModal = function() {
  var overlay = document.getElementById('map-modal-overlay');
  if (overlay) {
    overlay.classList.remove('open');
    overlay.style.display = 'none';
  }
};

// Task modal - shows full task context + 3 example responses
window.TASKS_DATA = {};
window.openTaskModalFor = function(taskId) {
  var t = window.TASKS_DATA[taskId];
  if (!t) { console.error('No task data for', taskId); return; }
  document.getElementById('task-modal-icon').textContent = t.icon || '';
  document.getElementById('task-modal-title').textContent = t.title || taskId;
  document.getElementById('task-modal-industry').textContent = t.industry || '';
  document.getElementById('task-modal-context').textContent = t.context || '';
  var respHtml = '';
  var samples = t.samples || [];
  if (samples.length === 0) {
    respHtml = '<p style="color: #5a4a3a; font-style: italic;">Примеры ответов не загружены. Возможно Phase 1 данные не сгенерированы.</p>';
  } else {
    samples.forEach(function(s) {
      respHtml += '<div class="task-response">';
      respHtml += '<div class="task-response-author">' + (s.name || s.model).toUpperCase() + ' (' + s.model + ')</div>';
      respHtml += '<div class="task-response-text">' + (s.response || '(пустой ответ)').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;') + '</div>';
      respHtml += '</div>';
    });
  }
  document.getElementById('task-modal-responses').innerHTML = respHtml;
  var overlay = document.getElementById('task-modal-overlay');
  overlay.classList.add('open');
  overlay.style.display = 'flex';
};

window.closeTaskModal = function() {
  var overlay = document.getElementById('task-modal-overlay');
  if (overlay) {
    overlay.classList.remove('open');
    overlay.style.display = 'none';
  }
};

// CRITICAL: Universal click handler ATTACHED BEFORE IIFE so it runs even if IIFE has error
document.addEventListener('click', function(e) {
  // Show what was clicked in debug-bar
  var t = e.target;
  var tag = t.tagName || '?';
  var cls = (t.getAttribute && t.getAttribute('class')) || '';
  var id = t.id || '';
  var closestIsland = (t.closest && t.closest('.island')) ? t.closest('.island') : null;
  var msg = 'CLICK -> ' + tag + ' class="' + cls + '" id="' + id + '" island=' + (closestIsland ? closestIsland.getAttribute('data-id') : 'NONE');
  var bar = document.getElementById('debug-bar');
  if (bar) bar.textContent = msg;
  console.log(msg);

  // If click was on an island - open modal
  if (closestIsland) {
    window.openModalFor(closestIsland);
  }
}, true);  // capture=true catches click BEFORE any other handler

// Close modal handlers - attached outside IIFE
document.addEventListener('keydown', function(e) {
  if (e.key === 'Escape') window.closeModal();
});

// Close on click on backdrop (but not on modal content)
document.addEventListener('click', function(e) {
  if (e.target && (e.target.id === 'map-modal-overlay' || e.target.id === 'modal-backdrop')) {
    window.closeModal();
  }
});

(function() {
  'use strict';

  function setDebug(msg) {
    var bar = document.getElementById('debug-bar');
    if (bar) bar.textContent = msg;
    console.log('[DEBUG]', msg);
  }

  // EXTRA SAFETY: 4 redundant click delegates - one of them MUST work
  function setupAllClickHandlers() {
    // Method 1: per-element direct listener
    var islands = document.querySelectorAll('.island');
    islands.forEach(function(el) {
      el.style.cursor = 'pointer';
      el.style.pointerEvents = 'all';
      el.addEventListener('click', function(e) {
        if (e.stopPropagation) e.stopPropagation();
        if (e.preventDefault) e.preventDefault();
        window.openModalFor(el);
      });
    });

    // Method 2: SVG-level delegation
    var svg = document.querySelector('.archipelago-svg');
    if (svg) {
      svg.addEventListener('click', function(e) {
        var node = e.target;
        while (node && node.tagName !== 'svg' && node !== document.body) {
          if (node.classList && node.classList.contains('island')) {
            if (e.stopPropagation) e.stopPropagation();
            window.openModalFor(node);
            return;
          }
          node = node.parentNode;
        }
      });
    }

    // Method 3: document.body delegation
    document.body.addEventListener('click', function(e) {
      var node = e.target;
      while (node && node !== document.body) {
        if (node.classList && node.classList.contains('island')) {
          window.openModalFor(node);
          return;
        }
        node = node.parentNode;
      }
    });

    setDebug('Click handlers attached to ' + islands.length + ' islands (4 methods).');
  }

  // Load data into GLOBAL window vars (so window.openModalFor can use them)
  try {
    var descEl = document.getElementById('model-descriptions-data');
    if (descEl) window.DESCRIPTIONS = JSON.parse(descEl.textContent);
    setDebug('Descriptions loaded: ' + Object.keys(window.DESCRIPTIONS).length + ' models. Click any island.');
  } catch (e) {
    console.error('Failed to parse descriptions JSON', e);
    setDebug('FAILED to parse descriptions: ' + e.message);
  }
  try {
    var bundlesEl = document.getElementById('bundles-data');
    if (bundlesEl) window.BUNDLES = JSON.parse(bundlesEl.textContent);
  } catch (e) { console.error('Failed to parse bundles JSON', e); }
  try {
    var risksEl = document.getElementById('risks-data');
    if (risksEl) window.RISKS = JSON.parse(risksEl.textContent);
  } catch (e) { console.error('Failed to parse risks JSON', e); }
  try {
    var tasksEl = document.getElementById('tasks-data');
    if (tasksEl) window.TASKS_DATA = JSON.parse(tasksEl.textContent);
  } catch (e) { console.error('Failed to parse tasks JSON', e); }
  var DESCRIPTIONS = window.DESCRIPTIONS;
  var BUNDLES = window.BUNDLES;
  var RISKS = window.RISKS;

  var TIER_RU = {C: "Cheap-tier", M: "Mid-tier", F: "Flagship"};

  // Local refs for short access - globals already defined outside IIFE
  var openModalFor = window.openModalFor;
  var closeModal = window.closeModal;
  window.closeModal = closeModal;

  // Expose for manual testing in DevTools console
  window.openModalFor = openModalFor;
  window.closeModal = closeModal;
  window.DESCRIPTIONS = DESCRIPTIONS;
  window.BUNDLES = BUNDLES;
  window.testModal = function(id) {
    // Manual test: call window.testModal('A_F') in console
    var fake = document.createElement('div');
    fake.setAttribute('data-id', id || 'A_F');
    fake.setAttribute('data-name', (DESCRIPTIONS[id] && id) || 'Test Model');
    fake.setAttribute('data-consensus', '0.321');
    openModalFor(fake);
    return 'Modal opened for ' + id;
  };

  // Island click via EVENT DELEGATION on document.body
  // (no per-element listeners - one delegated handler catches all clicks)
  var islands = document.querySelectorAll('.island');
  setDebug('Islands found: ' + islands.length + '. Descriptions: ' + Object.keys(DESCRIPTIONS).length + '. Click any island.');

  // Mark all islands as visually clickable
  islands.forEach(function(el) {
    el.style.cursor = 'pointer';
    el.style.pointerEvents = 'all';
    el.addEventListener('mouseenter', function() {
      if (el.parentNode) el.parentNode.appendChild(el);
    });
  });

  // ONE delegated click handler on body - catches click on island or any of its children
  function findIslandFromEvent(target) {
    var node = target;
    while (node && node !== document.body) {
      if (node.classList && node.classList.contains('island')) return node;
      node = node.parentNode;
    }
    return null;
  }

  document.body.addEventListener('click', function(e) {
    var island = findIslandFromEvent(e.target);
    if (!island) return;
    if (e.stopPropagation) e.stopPropagation();
    try {
      openModalFor(island);
      setDebug('Modal opened for ' + island.getAttribute('data-id'));
    } catch (err) {
      console.error('Modal open failed', err);
      setDebug('Modal failed: ' + err.message);
      alert('Click registered on ' + (island.getAttribute('data-id') || 'unknown') + ' but modal failed:\n' + err.message);
    }
  }, true);  // useCapture=true - catch before any other handler

  // Test helper: window.testIsland() programmatically clicks first island
  window.testIsland = function(id) {
    var target = id ? document.querySelector('.island[data-id="' + id + '"]') : islands[0];
    if (!target) return 'Island not found';
    openModalFor(target);
    return 'Modal opened for ' + target.getAttribute('data-id');
  };

  // Modal close - HTML5 dialog supports Escape natively, but also bind click on backdrop
  var dlg = document.getElementById('modal-dialog');
  if (dlg) {
    dlg.addEventListener('click', function(e) {
      // click on dialog itself (not children) = click on backdrop
      if (e.target === dlg) window.closeModal();
    });
    // Native dialog Escape already works, but our custom listener for redundancy
    dlg.addEventListener('cancel', function(e) {
      e.preventDefault();
      window.closeModal();
    });
  }

  // Family legend - click to highlight family
  var activeFamily = null;
  var activeBundle = null;

  function clearHighlights() {
    document.querySelectorAll('.legend-item').forEach(function(i) { i.classList.remove('active'); });
    document.querySelectorAll('.bundle-item').forEach(function(i) { i.classList.remove('active'); });
    document.querySelectorAll('.risk-item').forEach(function(i) { i.classList.remove('active'); });
    document.querySelectorAll('.island').forEach(function(i) { i.classList.remove('dim'); });
    activeFamily = null;
    activeBundle = null;
  }

  document.querySelectorAll('.legend-item').forEach(function(item) {
    item.addEventListener('click', function() {
      var fam = item.getAttribute('data-family');
      if (activeFamily === fam) {
        clearHighlights();
      } else {
        clearHighlights();
        activeFamily = fam;
        item.classList.add('active');
        document.querySelectorAll('.island').forEach(function(i) {
          i.classList.toggle('dim', i.getAttribute('data-family') !== fam);
        });
      }
    });
  });

  // Bundle click - highlight 3 models from bundle
  document.querySelectorAll('.bundle-item').forEach(function(item) {
    item.addEventListener('click', function() {
      var bid = item.getAttribute('data-bundle');
      if (activeBundle === bid) {
        clearHighlights();
      } else {
        clearHighlights();
        activeBundle = bid;
        item.classList.add('active');
        var bundle = BUNDLES[bid] || {};
        var bundleModels = bundle.models || [];
        document.querySelectorAll('.island').forEach(function(i) {
          var id = i.getAttribute('data-id');
          i.classList.toggle('dim', bundleModels.indexOf(id) === -1);
        });
      }
    });
  });

  // Risk click - highlight models affected by this risk
  var activeRisk = null;
  document.querySelectorAll('.risk-item').forEach(function(item) {
    item.addEventListener('click', function() {
      var rid = item.getAttribute('data-risk');
      if (activeRisk === rid) {
        clearHighlights();
        activeRisk = null;
      } else {
        clearHighlights();
        activeRisk = rid;
        item.classList.add('active');
        var risk = RISKS[rid] || {};
        var affectedModels = risk.models || [];
        document.querySelectorAll('.island').forEach(function(i) {
          var id = i.getAttribute('data-id');
          i.classList.toggle('dim', affectedModels.indexOf(id) === -1);
        });
      }
    });
  });

  // Setup ALL click handlers (4 methods)
  setupAllClickHandlers();

  // GUARANTEED FALLBACK: Generate HTML buttons for each model under the map
  // HTML buttons WILL work since user confirmed HTML clicks fire
  function generateModelButtons() {
    var container = document.getElementById('model-buttons');
    if (!container) return;
    var models = Object.keys(DESCRIPTIONS).sort(function(a, b) {
      return (DESCRIPTIONS[b].consensus_score || 0) - (DESCRIPTIONS[a].consensus_score || 0);
    });
    var families = {anthropic: '#c97645', openai: '#1e7a5f', google: '#3a5fa8', mistral: '#a85530', deepseek: '#5040a0', xai: '#2c2c2c', qwen: '#5848d0', moonshot: '#3a78c0', zhipu: '#c08020', nvidia: '#5a8a30', meta: '#3a6fc0', cohere: '#c05848'};
    var famMap = {A: 'anthropic', O: 'openai', G: 'google', M: 'mistral', D: 'deepseek', X: 'xai', Q: 'qwen', K: 'moonshot', Z: 'zhipu', N: 'nvidia', L: 'meta', C: 'cohere'};
    var html = '';
    models.forEach(function(id) {
      var d = DESCRIPTIONS[id];
      var fam = famMap[id[0]] || 'unknown';
      var color = families[fam] || '#666';
      var c = d.consensus_score || 0;
      var name = id;  // short id - find full name from island element
      var island = document.querySelector('.island[data-id="' + id + '"]');
      if (island) name = (island.getAttribute('data-name') || id).toUpperCase();
      html += '<button data-id="' + id + '" style="background: #2c2519; color: #f0e5cf; border: 2px solid ' + color + '; padding: 8px 4px; font-family: \'Cormorant Garamond\', serif; font-size: 11px; letter-spacing: 1px; cursor: pointer; border-radius: 3px; text-align: left; line-height: 1.3;" onmouseover="this.style.background=\'' + color + '\'; this.style.color=\'#2c2519\';" onmouseout="this.style.background=\'#2c2519\'; this.style.color=\'#f0e5cf\';"><div style="font-weight: 600;">' + id + '</div><div style="font-size: 9px; opacity: 0.7;">' + name + '</div></button>';
    });
    container.innerHTML = html;
    // Bind clicks
    container.querySelectorAll('button').forEach(function(btn) {
      btn.addEventListener('click', function() {
        var id = btn.getAttribute('data-id');
        var island = document.querySelector('.island[data-id="' + id + '"]');
        if (island) window.openModalFor(island);
      });
    });
  }
  generateModelButtons();

  // DIAGNOSTIC: log EVERY click on the page - shows what's actually being clicked
  document.addEventListener('click', function(e) {
    var t = e.target;
    var tag = t.tagName || '?';
    var cls = t.getAttribute ? (t.getAttribute('class') || '') : '';
    var id = t.id || '';
    var closestIsland = (t.closest && t.closest('.island')) ? t.closest('.island').getAttribute('data-id') : 'NONE';
    var msg = 'CLICK -> ' + tag + ' class="' + cls + '" id="' + id + '" closestIsland=' + closestIsland;
    var bar = document.getElementById('debug-bar');
    if (bar) bar.textContent = msg;
    console.log(msg);
  }, true);

  console.log('Archipelago map ready.');
})();

// Backup: also setup after window.load (in case DOM not ready when IIFE ran)
window.addEventListener('load', function() {
  var islands = document.querySelectorAll('.island');
  islands.forEach(function(el) {
    if (!el._clickAttached) {
      el._clickAttached = true;
      el.style.cursor = 'pointer';
      el.style.pointerEvents = 'all';
      el.addEventListener('click', function(e) {
        if (e.stopPropagation) e.stopPropagation();
        window.openModalFor(el);
      });
    }
  });
  console.log('Backup click handlers added on window.load');
});
"""
    js = js_template

    # Build the head/body parts as f-string, THEN concat the script tags safely
    body_html = f"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<title>Архипелаг тридцати шести · CM-RG Phase 2L</title>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;1,400&display=swap" rel="stylesheet">
<style>{css}</style>
</head>
<body>
<div id="debug-bar" style="position: fixed; top: 0; left: 0; right: 0; background: #c97645; color: #2c2519; padding: 6px 16px; font-family: monospace; font-size: 11px; z-index: 100; letter-spacing: 1px;">Loading...</div>
<div class="container" style="padding-top: 30px;">
  <div class="header">
    <h1>АРХИПЕЛАГ ТРИДЦАТИ ШЕСТИ</h1>
    <p>Phase 2L · Cross-Model Repertory Grid · {n_models} моделей · 2.6 млн оценок · средний r = 0.21</p>
  </div>

  <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 24px; margin: 30px 0; padding: 24px; background: #1e1a14; border-radius: 4px; border-left: 3px solid #c97645;">
    <div>
      <h3 style="margin: 0 0 10px; font-size: 13px; color: #c97645; letter-spacing: 2px; text-transform: uppercase;">Что мы сделали</h3>
      <p style="margin: 0; line-height: 1.7; color: #d4c8b0; font-size: 15px;">Мы взяли <strong style="color: #f0e5cf;">36 топовых ИИ-моделей</strong> от 12 разных производителей (Anthropic, OpenAI, Google, Meta, Mistral и других) и попросили каждую написать совет на <strong style="color: #f0e5cf;">7 сложных бизнес-задач</strong>: слияние и поглощение, передача семейного бизнеса, реагирование на пандемию, распределение R&amp;D бюджета, кризисные коммуникации после взлома, конституционная реформа, регулирование ИИ. Потом каждая модель прочитала <strong style="color: #f0e5cf;">35 анонимных ответов</strong> от других ИИ и оценила их. Итого <strong style="color: #f0e5cf;">2.6 миллиона оценок</strong>.</p>
    </div>
    <div>
      <h3 style="margin: 0 0 10px; font-size: 13px; color: #c97645; letter-spacing: 2px; text-transform: uppercase;">Что обнаружили</h3>
      <p style="margin: 0; line-height: 1.7; color: #d4c8b0; font-size: 15px;">ИИ-модели <strong style="color: #f0e5cf;">слабо согласны</strong> друг с другом (корреляция 0.21 из 1.0). Миф об "объективном ИИ-судье" - это миф. Есть <strong style="color: #f0e5cf;">Западный кластер согласия</strong> (GPT, Claude, Gemini, Grok) - модели обучены похожим способом и оценивают похоже. Есть <strong style="color: #f0e5cf;">периферия противоположных мнений</strong> (Qwen 7B, Nemotron, Llama 3.3). И есть <strong style="color: #f0e5cf;">переходная зона</strong> (Qwen Max, Kimi) - китайские флагманы постепенно сближаются. Карта показывает кластеры пространственно: близко = модели похоже оценивают.</p>
    </div>
  </div>

  <div class="tasks-section">
    <h3>7 задач эксперимента (кликабельно)</h3>
    <p class="subtitle">Каждая модель ответила на эти 7 советующих вопросов. Кликни карточку чтобы увидеть 3 примера ответов от разных flagship моделей.</p>
    <div class="tasks-grid" id="tasks-grid">
      {tasks_grid_html}
    </div>
  </div>

  <div class="map-container">
    <div class="map-frame">{svg}</div>
    <!-- Modal overlay - covers ONLY the map area, not entire page -->
    <div class="map-modal-overlay" id="map-modal-overlay">
      <div class="modal" id="modal" style="position: relative; max-width: 540px; width: 90%;">
        <button class="modal-close" onclick="window.closeModal()" title="Закрыть (Escape)">×</button>
        <h2 id="modal-title">-</h2>
        <div class="subtitle" id="modal-subtitle">-</div>

        <div style="background: #f7eed8; border-left: 3px solid #c97645; padding: 12px 16px; margin: 14px 0;">
          <div style="margin-bottom: 8px;"><span class="modal-rank" id="modal-rank">-</span></div>
          <div style="font-size: 12px; color: #5a4a3a; line-height: 1.5;">
            <strong>Ранг</strong> = место в рейтинге согласия с другими ИИ (1 = больше всего совпадает).<br>
            <strong>Индекс согласия</strong> = от -1 до +1: близко к 1 = почти полное согласие, около 0 = слабое, ниже 0 = противоположные оценки.
          </div>
        </div>

        <h3>Поведение в эксперименте</h3>
        <p id="modal-position">-</p>

        <h3>Семья и провайдер</h3>
        <p id="modal-family">-</p>

        <p id="modal-tier" style="display: none;">-</p>
        <div class="modal-hint">× сверху · Escape · клик мимо</div>
      </div>
    </div>
  </div>

  <div style="background: #1e1a14; padding: 16px; margin: 16px 0; border-radius: 4px; border-left: 3px solid #c97645;">
    <h3 style="margin: 0 0 12px; font-size: 13px; color: #c97645; letter-spacing: 2px; text-transform: uppercase;">Карточки моделей (если клик на остров не работает)</h3>
    <p style="margin: 0 0 12px; font-size: 12px; color: #8a7d6a; font-style: italic;">Кликни любую кнопку - откроется детальная карточка модели.</p>
    <div id="model-buttons" style="display: grid; grid-template-columns: repeat(auto-fill, minmax(140px, 1fr)); gap: 6px;">
      <!-- Buttons generated by JS for guaranteed click functionality -->
    </div>
  </div>

  <div class="legend">
    <h3>Условные обозначения</h3>

    <div class="legend-section-title">Как читать карту</div>
    <p style="margin: 6px 0 14px; font-size: 13px; color: #d4c8b0; font-style: italic; line-height: 1.6;">
      Направление осей не имеет смысла (MDS rotation arbitrary). Важно <strong style="color: #f0e5cf;">только расстояние</strong>.
      Чем ближе остров к <strong style="color: #c97645;">ЯДРУ КОНСЕНСУСА</strong> (центру карты), тем сильнее модель согласна с другими.
      Чем дальше к <strong style="color: #f0e5cf;">ПЕРИФЕРИИ</strong> - тем больше модель оценивает иначе чем большинство.
      Пунктирные круги показывают уровни consensus (core / transitional / periphery).
    </p>

    <div class="legend-section-title" style="margin-top: 18px;">Семьи моделей (кликабельно - выделить семью)</div>
    <div class="legend-row">{legend_html}</div>

    <div class="legend-section-title" style="margin-top: 18px;">Размер острова - уровень consensus</div>
    <div class="size-scale">
      <div class="size-scale-item">
        <div class="size-scale-circle" style="width: 14px; height: 14px;"></div>
        <div class="size-scale-label">consensus &le; 0</div>
        <div class="size-scale-label" style="color: #8a7d6a;">divergent</div>
      </div>
      <div class="size-scale-item">
        <div class="size-scale-circle" style="width: 24px; height: 24px;"></div>
        <div class="size-scale-label">consensus ~ 0.15</div>
        <div class="size-scale-label" style="color: #8a7d6a;">промежуточная</div>
      </div>
      <div class="size-scale-item">
        <div class="size-scale-circle" style="width: 40px; height: 40px;"></div>
        <div class="size-scale-label">consensus ~ 0.30</div>
        <div class="size-scale-label" style="color: #8a7d6a;">в центре</div>
      </div>
      <div class="size-scale-item">
        <div class="size-scale-circle" style="width: 56px; height: 56px;"></div>
        <div class="size-scale-label">consensus 0.38+</div>
        <div class="size-scale-label" style="color: #8a7d6a;">ядро Western</div>
      </div>
    </div>

    <div class="legend-section-title" style="margin-top: 18px;">Расстояние между островами</div>
    <p style="margin: 6px 0 0; font-size: 13px; color: #d4c8b0; font-style: italic;">Близко = модели согласны в оценках. Далеко = разные системы судей. Точное расстояние = 1 - средняя корреляция Pearson между моделями по 14 (задача × условие) комбинациям.</p>
  </div>

  <div class="narrative">{narrative}</div>

  <div class="legend">
    <h3>Ансамбли для индустрий (кликабельно - подсветить рекомендованные модели)</h3>
    <p style="margin: 0 0 12px; font-size: 12px; color: #8a7d6a; font-style: italic;">Каждый ансамбль = 3 модели для конкретного типа задач. Клик подсвечивает их на карте.</p>
    <div class="bundles">{bundles_html}</div>

    <h3 style="margin-top: 28px;">Риски и особенности моделей (кликабельно)</h3>
    <p style="margin: 0 0 12px; font-size: 12px; color: #8a7d6a; font-style: italic;">Что нужно знать ДО того как использовать модель в production. Клик подсвечивает модели с этим риском на карте.</p>
    <div class="risks">{risks_html}</div>
  </div>

  <div class="footer">Archipelago Research · CM-RG Phase 2L · 2026 · $112.89 бюджет на 2,572 API calls</div>
</div>

<!-- Modal moved inside .map-container above (overlay only over map, not whole page) -->

<!-- Task modal - full page overlay -->
<div class="task-modal-overlay" id="task-modal-overlay" onclick="if(event.target === this) window.closeTaskModal()">
  <div class="task-modal">
    <button class="modal-close" onclick="window.closeTaskModal()" title="Закрыть (Escape)">×</button>
    <div class="task-icon" id="task-modal-icon" style="font-size: 32px; margin-bottom: 4px;">-</div>
    <h2 id="task-modal-title">-</h2>
    <div class="task-modal-industry" id="task-modal-industry">-</div>
    <div class="task-modal-context" id="task-modal-context">-</div>
    <h3>Примеры ответов от 3 разных flagship моделей</h3>
    <div id="task-modal-responses">Loading...</div>
  </div>
</div>

<!-- script tags appended via concat below -->
</body>
</html>
"""
    # Concatenate the script tags WITHOUT f-string interpolation
    # (this guarantees no `{}` in JSON or JS get re-parsed as f-string placeholders)
    parts = [body_html.replace("</body>\n</html>\n", "")]
    parts.append('<script type="application/json" id="model-descriptions-data">')
    parts.append(descriptions_json)
    parts.append('</script>\n')
    parts.append('<script type="application/json" id="bundles-data">')
    parts.append(bundles_json)
    parts.append('</script>\n')
    parts.append('<script type="application/json" id="risks-data">')
    parts.append(risks_json)
    parts.append('</script>\n')
    parts.append('<script type="application/json" id="tasks-data">')
    parts.append(tasks_json)
    parts.append('</script>\n')
    parts.append('<script>\n')
    parts.append(js)
    parts.append('\n</script>\n</body>\n</html>\n')
    html = "".join(parts)
    return html


def main():
    if not ANALYSIS_JSON.exists():
        print(f"ERROR: {ANALYSIS_JSON} not found. Run analyze_phase2l.py first.")
        return 2
    print(f"Loading analysis results from {ANALYSIS_JSON}...")
    data = json.loads(ANALYSIS_JSON.read_text(encoding="utf-8"))
    corrs = data.get("inter_rater_corrs", {})
    consensus = data.get("divergence_summary", {})
    if not corrs:
        print("ERROR: no inter_rater_corrs in analysis_results.json.")
        return 2
    print("Computing pairwise distances...")
    models, D = compute_distance_matrix(corrs)
    print(f"  {len(models)} models")
    print("Running MDS (15-30 seconds)...")
    positions = simple_mds(D, dim=2, iterations=1500, lr=0.02)
    canvas_w, canvas_h = 1200, 800
    coords = normalize_to_canvas(positions, canvas_w, canvas_h, margin=100)
    print("Rendering vintage SVG...")
    svg = render_svg(models, coords, consensus, canvas_w, canvas_h)
    descriptions = build_model_descriptions(consensus)
    print("Loading sample responses for task cards...")
    task_samples = load_sample_responses(RESULTS_DIR)
    print(f"  Loaded samples for {sum(1 for s in task_samples.values() if s)} tasks")
    print("Building HTML...")
    html = build_html(svg, models, descriptions, task_samples)
    OUTPUT_HTML.write_text(html, encoding="utf-8")
    print(f"\nSaved: {OUTPUT_HTML}")
    print(f"\nOpen: start {OUTPUT_HTML}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
