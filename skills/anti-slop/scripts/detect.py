#!/usr/bin/env python3
"""anti-slop detector: heuristic static checks for generated-looking design and text.

Flags suspicious patterns by rule ID (see references/*.md). It is a reviewer's
aid, not a judge: every finding needs a human or model decision.

Usage:
  detect.py [paths...] [--json] [--min-severity low|medium|high]
            [--fail-on low|medium|high|none] [--lang auto|ca|es|en]
            [--exclude GLOB] [--list-rules]

Inline control:
  anti-slop-ignore            on a line: ignore every finding on that line
  anti-slop-ignore D-14 W-10  on a line: ignore those rules on that line
  anti-slop-ignore-file       anywhere in a file: skip the file

Exit codes: 0 = nothing at or above --fail-on, 1 = findings at or above it,
2 = usage error. Standard library only.
"""
from __future__ import annotations

import argparse
import bisect
import fnmatch
import html
import json
import os
import re
import sys
from dataclasses import dataclass, asdict

SEV = {"low": 1, "medium": 2, "high": 3}

STYLE_EXT = {".css", ".scss", ".sass", ".less"}
MARKUP_EXT = {".html", ".htm", ".tsx", ".jsx", ".vue", ".svelte", ".astro"}
PROSE_EXT = {".md", ".mdx", ".txt"}
ALL_EXT = STYLE_EXT | MARKUP_EXT | PROSE_EXT
SKIP_DIRS = {"node_modules", ".git", "dist", "build", "vendor", ".next", ".nuxt",
             ".svelte-kit", "out", "coverage", "__pycache__", ".venv", "venv", "results"}

# --------------------------------------------------------------------------- rules

RULES = {
    # design
    "D-02": ("high", "Card inside a card"),
    "D-03": ("high", "Side-stripe border"),
    "D-06": ("low", "One radius everywhere"),
    "D-07": ("medium", "Glass and blur"),
    "D-08": ("low", "Hard offset shadow"),
    "D-10": ("low", "Default font without intent"),
    "D-11": ("medium", "Text below 12px"),
    "D-12": ("high", "Eyebrow above heading"),
    "D-13": ("medium", "Small tracked uppercase label"),
    "D-14": ("medium", "Letter-spacing added"),
    "D-16": ("medium", "Monospace as costume"),
    "D-20": ("high", "AI palette gradient"),
    "D-21": ("high", "Gradient text"),
    "D-22": ("medium", "Glow"),
    "D-23": ("low", "Pure black"),
    "D-24": ("low", "Default cream background"),
    "D-26": ("high", "Grey text on colour"),
    "D-28": ("medium", "Two-tone headline"),
    "D-41": ("medium", "Many one-off values"),
    "D-45": ("high", "Emoji as icon"),
    "D-46": ("medium", "Icon in a tinted circle"),
    "D-47": ("medium", "Badge and pill soup"),
    "D-50": ("high", "Entrance animation"),
    "D-51": ("medium", "Bounce or elastic easing"),
    "D-52": ("low", "Hover that moves or scales"),
    "D-53": ("low", "Animating layout properties"),
    "D-54": ("medium", "Infinite decorative motion"),
    "D-56": ("medium", "Motion without reduced-motion alternative"),
    "D-58": ("medium", "Cursor and scroll gimmicks"),
    "D-60": ("medium", "Broken basics"),
    # writing
    "W-01": ("high", "Comma splice"),
    "W-03": ("medium", "Choppy chain of short sentences"),
    "W-10": ("high", "Semicolon"),
    "W-11": ("high", "Em dash in prose"),
    "W-19": ("high", "Quotation marks as habit"),
    "W-12": ("medium", "Colon hinge"),
    "W-13": ("high", "Negative parallelism"),
    "W-18": ("medium", "Reflex caveat tail"),
    "W-14": ("medium", "Bold-label bullets"),
    "W-15": ("medium", "Question as heading"),
    "W-20": ("medium", "Repeated sentence"),
    "W-21": ("high", "Empty opener or closer"),
    "W-26": ("medium", "Signposting"),
    "W-29": ("medium", "Inflated vocabulary"),
    "W-30": ("medium", "Comma-tag heading"),
    "W-31": ("medium", "Slogan heading"),
    "W-32": ("medium", "Title Case heading"),
    "W-33": ("medium", "Numeral count"),
    "W-34": ("medium", "Generic heading"),
    "W-37": ("medium", "Scattered bold"),
    "W-38": ("medium", "Decorative emoji"),
    "W-43": ("medium", "Participle tail"),
    "W-44": ("high", "Chatbot residue"),
    "EN-02": ("high", "Marketing buzzword"),
    "EN-04": ("low", "Intensifier adverbs"),
    "EN-05": ("medium", "Significance inflation"),
    "EN-06": ("medium", "Vague attribution"),
    "EN-09": ("medium", "Generic UI string"),
    "CA-02": ("high", "Calque from English (ca)"),
    "CA-03": ("medium", "Calque from Spanish (ca)"),
    "CA-04": ("medium", "Gerund of posteriority (ca)"),
    "CA-08": ("medium", "Mixed action label forms (ca)"),
    "CA-11": ("low", "Bureaucratic verb (ca)"),
    "CA-13": ("low", "Anglicism in interface (ca)"),
    "ES-02": ("high", "Calque from English (es)"),
    "ES-03": ("medium", "Gerund of posteriority (es)"),
    "ES-04": ("medium", "Missing opening question mark (es)"),
    "ES-08": ("low", "Bureaucratic verb (es)"),
    # content
    "C-01": ("medium", "Unsourced number"),
    "C-02": ("high", "Placeholder person or company"),
    "C-04": ("medium", "Repeated generic CTA"),
    "C-07": ("high", "Internal note in public text"),
    "C-12": ("high", "Placeholder left in"),
}


@dataclass
class Finding:
    rule: str
    severity: str
    file: str
    line: int
    message: str
    excerpt: str


def I(p: str) -> re.Pattern:
    return re.compile(p, re.IGNORECASE)


STARS = re.compile(r"(?:^|[>\"'`])\s*[★☆]{3,}\s*(?:$|[<\"'`])")
TWO_TONE = re.compile(r"<h([1-3])\b[^>]*>\s*[^<>\s][^<>]{1,120}(?:<br\b[^>]*>\s*)?<(span|em|strong)\b[^>]*>[^<>]*\w[^<>]*\s[^<>]*\w[^<>]*</\2>\s*</h\1>", re.I)
CA_INF = re.compile(r"^(?:veure|entrar|acceptar|rebutjar|enviar|desar|guardar|tancar|crear|cancel·lar|descarregar|baixar|cercar|buscar|continuar|començar|editar|esborrar|eliminar|afegir|obrir|mostrar|demanar|contactar|llegir|descobrir|comprar|reservar|sol·licitar|registrar|iniciar|accedir|configurar|tornar|compartir|copiar|publicar|pagar|confirmar|seleccionar|filtrar|explorar|provar|consultar|conèixer|trobar|escriure|mirar|parlar|subscriure|inscriure)(?![\w·])", re.I)
CA_IMP = re.compile(r"^(?:mira|entra|accepta|rebutja|envia|desa|guarda|tanca|crea|cancel·la|descarrega|baixa|cerca|continua|comença|edita|esborra|elimina|afegeix|obre|mostra|demana|contacta|llegeix|descobreix|compra|reserva|sol·licita|registra|inicia|accedeix|configura|torna|comparteix|copia|publica|paga|confirma|selecciona|filtra|explora|prova|consulta|coneix|troba|escriu|parla|subscriu|inscriu|vine|truca|segueix|fes|uneix)(?![\w·])", re.I)


def action_label_forms(text: str, line_of, add):
    """CA-08: buttons and links that mix the infinitive and the imperative."""
    inf, imp = [], []
    for m in re.finditer(r"<(a|button)\b[^>]*>(.*?)</\1>", text, re.S | re.I):
        label = html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", m.group(2)))).strip()
        if not label or len(label.split()) > 5:
            continue
        if CA_INF.match(label):
            inf.append((line_of(m.start()), label))
        elif CA_IMP.match(label):
            imp.append((line_of(m.start()), label))
    if inf and imp:
        add("CA-08", inf[0][0], f"Action labels mix the infinitive («{inf[0][1]}») and the imperative («{imp[0][1]}»)", inf[0][1])


EMOJI = re.compile("[\U0001F300-\U0001FAFF\U00002600-\U000027BF\U0001F000-\U0001F02F⭐⬆✅❌]")

# ------------------------------------------------------------------ design rules

SIDE = r"(?:left|right|inline-start|inline-end)"
DESIGN_LINE_RULES = [
    ("D-03", None, re.compile(r"border-" + SIDE + r"\s*:\s*(?:[2-9]|\d{2,})(?:\.\d+)?px"), "Thick border on one side only"),
    ("D-03", None, re.compile(r"border-" + SIDE + r"-width\s*:\s*(?:[2-9]|\d{2,})px"), "Thick border on one side only"),
    ("D-03", None, re.compile(r"(?<![\w-])border-(?:l|r|s|e)-(?:2|4|8|\[\d+px\])(?![\w-])"), "Tailwind side stripe"),
    ("D-03", "low", re.compile(r"(?<![\w:-])border-(?:t|b)-(?:4|8|\[\d+px\])(?![\w-])"), "Thick top or bottom accent border"),
    ("D-20", None, re.compile(r"from-(?:purple|violet|indigo|fuchsia)-\d{2,3}.*?to-(?:blue|cyan|sky|pink|indigo|violet|purple|fuchsia)-\d{2,3}"), "Purple/blue/pink gradient"),
    ("D-20", None, I(r"(?:linear|radial)-gradient\([^)]*#(?:8b5cf6|7c3aed|6366f1|a855f7|9333ea|4f46e5|ec4899|d946ef|6d28d9)"), "Purple/indigo gradient"),
    ("D-21", None, re.compile(r"^(?=.*\bbg-clip-text\b)(?=.*\btext-transparent\b)"), "Gradient text"),
    ("D-21", None, I(r"background-clip\s*:\s*text"), "Gradient text"),
    ("D-07", None, re.compile(r"(?<![\w-])backdrop-blur(?:-\w+)?(?![\w-])|backdrop-filter\s*:\s*blur"), "Backdrop blur"),
    ("D-08", None, re.compile(r"box-shadow\s*:\s*-?[1-9]\d*px\s+-?[1-9]\d*px\s+0(?:px)?\s"), "Hard offset shadow"),
    ("D-08", None, re.compile(r"shadow-\[-?[1-9]\d*px_-?[1-9]\d*px_0"), "Hard offset shadow"),
    ("D-22", None, re.compile(r"shadow-(?:purple|violet|indigo|cyan|blue|pink|fuchsia|emerald|sky)-\d{3}"), "Coloured glow shadow"),
    ("D-22", None, re.compile(r"shadow-\[0_0_\d{2,}px"), "Glow shadow"),
    ("D-22", None, I(r"box-shadow\s*:\s*0(?:px)?\s+0(?:px)?\s+[1-9]\d+px[^;]*(?:rgba?\((?!0,\s*0,\s*0)|#(?!000))"), "Glow shadow"),
    ("D-12", None, I(r"""class(?:Name)?\s*=\s*["'{`][^"'`]*\b(?:eyebrow|kicker|overline|pre-?title|supertitle|tagline)\b"""), "Eyebrow class"),
    ("D-12", None, I(r"\.(?:eyebrow|kicker|overline|pre-?title|supertitle)\b"), "Eyebrow selector"),
    ("D-13", None, re.compile(r"^(?=.*(?<![\w-])uppercase(?![\w-]))(?=.*(?<![\w-])tracking-(?:wide|wider|widest|\[))(?=.*(?<![\w-])text-(?:xs|\[1[01]px\]|\[0\.[67]\d*rem\])(?![\w-]))"), "Small tracked uppercase label"),
    ("D-14", None, I(r"letter-spacing\s*:\s*(?!normal|0(?:px|em|rem)?\s*[;}!]|0\s*$|inherit|initial|unset)[-\d.]"), "Letter-spacing set"),
    ("D-14", None, re.compile(r"(?<![\w-])tracking-(?:tighter|tight|wide|wider|widest|\[[^\]]+\])(?![\w-])"), "Tailwind tracking"),
    ("D-16", None, re.compile(r"^(?=.*(?<![\w-])font-mono(?![\w-]))(?=.*(?<![\w-])(?:uppercase|text-xs)(?![\w-]))"), "Monospace small label"),
    ("D-23", None, I(r"(?:^|[;{\s])(?:color|background(?:-color)?)\s*:\s*#000(?:000)?\b"), "Pure black"),
    ("D-24", None, I(r"#(?:f4f1ea|faf7f2|f5f0e8|fdfbf7|f7f3ed|fbf8f3|f5f1e8|faf6f0)\b"), "Cream background preset"),
    ("D-26", None, re.compile(r"^(?=.*(?<![\w-])text-(?:gray|slate|zinc|neutral)-(?:300|400|500)(?![\w-]))(?=.*(?<![\w:-])bg-(?:blue|indigo|violet|purple|red|green|emerald|teal|sky|pink|rose|orange|amber)-(?:5|6|7|8)00(?![\w-]))"), "Grey text on coloured background"),
    ("D-46", None, re.compile(r"^(?=.*(?<![\w-])rounded-(?:full|xl|lg)(?![\w-]))(?=.*(?<![\w:-])bg-\w+-(?:50|100)(?:/\d+)?(?![\w-]))(?=.*(?<![\w-])(?:w-1[0-4]|size-1[0-4]|h-1[0-4])(?![\w-]))(?=.*(?:items-center|place-items-center|justify-center))"), "Icon in a tinted circle"),
    ("D-50", None, re.compile(r"data-aos=|\bwhileInView\b|initial=\{\{\s*opacity:\s*0\s*,\s*(?:y|x|scale)\s*:|\bAOS\.init\b|animate__fadeIn|\bfade-?(?:in-)?up\b|\banimate-fade-?in(?:-up)?\b"), "Entrance animation"),
    ("D-51", None, re.compile(r"(?<![\w-])animate-bounce(?![\w-])|\b(?:easeOutBack|easeInOutBack|easeOutElastic|easeInOutElastic|easeOutBounce)\b|ease-(?:elastic|bounce|spring)\b"), "Bounce or elastic easing"),
    ("D-52", None, re.compile(r"hover:(?:scale-1(?:0[2-9]|[1-9]\d)|-translate-y-\d)"), "Hover scale or lift"),
    ("D-53", None, I(r"transition(?:-property)?\s*:[^;]*\b(?:width|height|top|left|right|bottom|margin|padding)\b"), "Transition on layout property"),
    ("D-53", None, re.compile(r"(?<![\w-])transition-all(?![\w-])"), "transition-all"),
    ("D-54", None, re.compile(r"(?<![\w-])animate-(?:pulse|ping)(?![\w-])"), "Infinite pulse"),
    ("D-54", None, I(r"^(?!.*(?:spin|rotate|loader|loading|skeleton|shimmer|progress)).*animation(?:-iteration-count)?\s*:[^;]*\binfinite\b"), "Infinite animation"),
    ("D-50", None, I(r"animation-timeline\s*:\s*view\(|\bdata-(?:split|reveal|view-reveal|scroll-reveal)\b|\bSplitText\b"), "Scroll reveal or split text"),
    ("D-58", None, I(r"(?<![\w-])cursor\s*:\s*none"), "System cursor hidden for a custom one"),
    ("D-58", None, I(r"animation-timeline\s*:\s*scroll\("), "Scroll-linked progress animation"),
    ("D-58", None, I(r"(?:\.|class(?:Name)?\s*=\s*[\"'][^\"']*?)(?<![\w-])(?:custom-cursor|cursor-(?:dot|follower|ring|outline)|scroll-progress|reading-progress)(?![\w-])"), "Custom cursor or progress bar"),
    ("D-58", None, re.compile(r"(?:^|[}\s,])\.cursor\s*\{[^}]*position\s*:\s*fixed"), "Custom cursor element"),
    ("D-60", None, I(r"user-scalable\s*=\s*no|maximum-scale\s*=\s*1(?:\.0)?\b"), "Zoom disabled"),
]

class LineIndex:
    def __init__(self, text: str):
        self.nl = [i for i, c in enumerate(text) if c == "\n"]

    def __call__(self, pos: int) -> int:
        return bisect.bisect_left(self.nl, pos) + 1


CARD_CLASS = re.compile(r"(?:^|\s)(?:card|panel|tile)(?:$|\s|-)")


def is_card_like(tag: str, attrs: str) -> bool:
    if re.match(r"(?:\w+\.)?Card$", tag):
        return True
    m = re.search(r"""class(?:Name)?\s*=\s*(?:"([^"]*)"|'([^']*)'|\{`([^`]*)`\}|\{"([^"]*)"\})""", attrs)
    if not m:
        return False
    cls = next(g for g in m.groups() if g is not None)
    if CARD_CLASS.search(cls):
        return True
    has_round = re.search(r"(?<![\w-])rounded(?:-(?:md|lg|xl|2xl|3xl))?(?![\w-])", cls)
    has_frame = re.search(r"(?<![\w:-])(?:border|shadow(?:-(?:sm|md|lg|xl))?)(?![\w-])", cls)
    has_pad = re.search(r"(?<![\w:-])p[xy]?-(?:[3-9]|1\d)(?![\w-])", cls)
    has_bg = re.search(r"(?<![\w:-])bg-", cls)
    return bool(has_round and has_pad and (has_frame or has_bg))


VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}
TAG = re.compile(r"<(/?)([A-Za-z][\w.:-]*)((?:[^<>\"'{}]|\"[^\"]*\"|'[^']*'|\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\})*?)(/?)>")


def nested_cards(text: str):
    stack = []  # (name, card, line)
    out = []
    line_of = LineIndex(text)
    for m in TAG.finditer(text):
        closing, name, attrs, selfclose = m.groups()
        line = line_of(m.start())
        if closing:
            for i in range(len(stack) - 1, -1, -1):
                if stack[i][0] == name:
                    del stack[i:]
                    break
            continue
        if selfclose or name.lower() in VOID:
            continue
        card = is_card_like(name, attrs)
        if card and any(c for _, c, _ in stack):
            out.append(line)
        stack.append((name, card, line))
    return out


def design_checks(path: str, text: str, lines: list[str], is_style: bool, add):
    in_comment = False
    tw_arbitrary = 0
    radius_big = 0
    clip_shapes = 0
    badges = 0
    for no, raw in enumerate(lines, 1):
        s = raw.strip()
        if is_style:
            if in_comment:
                if "*/" in s:
                    in_comment = False
                continue
            if s.startswith("/*") and "*/" not in s:
                in_comment = True
                continue
            if s.startswith(("/*", "//", "*")):
                continue
        for rid, sev, rx, msg in DESIGN_LINE_RULES:
            if rx.search(raw):
                add(rid, no, msg, raw, sev)
        # cubic-bezier overshoot
        for m in re.finditer(r"cubic-bezier\(\s*([-\d.]+)\s*,\s*([-\d.]+)\s*,\s*([-\d.]+)\s*,\s*([-\d.]+)\s*\)", raw):
            try:
                y1, y2 = float(m.group(2)), float(m.group(4))
            except ValueError:
                continue
            if y1 < 0 or y1 > 1 or y2 < 0 or y2 > 1:
                add("D-51", no, "Overshooting cubic-bezier", raw)
        # tiny text
        for m in re.finditer(r"font-size\s*:\s*([\d.]+)(px|rem|em)\b", raw):
            v = float(m.group(1)) * (16 if m.group(2) != "px" else 1)
            if 0 < v < 12:
                add("D-11", no, f"Text at {v:g}px", raw)
        for m in re.finditer(r"text-\[([\d.]+)(px|rem)\]", raw):
            v = float(m.group(1)) * (16 if m.group(2) == "rem" else 1)
            if v < 12:
                add("D-11", no, f"Text at {v:g}px", raw)
        # default fonts declared as the first family
        m = re.search(r"font-family\s*:\s*['\"]?(Inter|Roboto|Arial|Helvetica|Open Sans|Poppins|Montserrat|Lato)\b", raw, re.I)
        if m and is_style:
            add("D-10", no, f"{m.group(1)} as the main face: is it a choice?", raw)
        if not is_style and STARS.search(raw):
            add("D-45", no, "Star row: does the rating vary and have a source?", raw, "low")
        elif not is_style and EMOJI.search(raw) and re.search(r"[>\"'`]\s*" + EMOJI.pattern, raw):
            add("D-45", no, "Emoji used as an icon", raw)
        if not is_style and re.search(r"<img\b(?![^>]*\balt\s*=)", raw):
            add("D-60", no, "Image without alt", raw)
        tw_arbitrary += len(re.findall(r"(?<![\w-])-?[a-z]+(?:-[a-z]+)*-\[\d+(?:\.\d+)?px\]", raw))
        radius_big += len(re.findall(r"(?<![\w-])rounded-(?:2xl|3xl)(?![\w-])", raw))
        clip_shapes += len(re.findall(r"clip-path\s*:\s*polygon\(", raw, re.I))
        if re.search(r"^(?=.*(?<![\w-])rounded-full(?![\w-]))(?=.*(?<![\w:-])px-(?:2|2\.5|3)(?![\w-]))(?=.*(?<![\w-])text-xs(?![\w-]))", raw):
            badges += 1
    if tw_arbitrary > 8:
        add("D-41", 1, f"{tw_arbitrary} arbitrary pixel values: use the scale", "")
    if radius_big > 12:
        add("D-06", 1, f"{radius_big} large radii: one radius on everything", "")
    if clip_shapes > 12:
        add("D-06", 1, f"{clip_shapes} clip-path shapes: one signature shape on everything", "")
    if badges > 6:
        add("D-47", 1, f"{badges} pill badges in one file", "")
    if is_style:
        if re.search(r"@keyframes|animation\s*:", text) and "prefers-reduced-motion" not in text:
            line = next((i for i, l in enumerate(lines, 1) if re.search(r"@keyframes|animation\s*:", l)), 1)
            add("D-56", line, "Animation without a prefers-reduced-motion rule", lines[line - 1])
        if re.search(r"outline\s*:\s*(?:none|0)\b", text) and not re.search(r":focus-visible|:focus\b", text):
            line = next(i for i, l in enumerate(lines, 1) if re.search(r"outline\s*:\s*(?:none|0)\b", l))
            add("D-60", line, "Focus outline removed with no replacement", lines[line - 1])
    else:
        for line in nested_cards(text):
            add("D-02", line, "Card-like box inside another card-like box", lines[line - 1])
        line_of = LineIndex(text)
        for m in TWO_TONE.finditer(text):
            add("D-28", line_of(m.start()), "Heading split into two tones: one colour, one weight", re.sub(r"<[^>]+>", " ", m.group(0)))
        action_label_forms(text, line_of, add)


# ------------------------------------------------------------------- prose units

@dataclass
class Unit:
    kind: str   # para | bullet | heading
    text: str
    line: int
    level: int = 0


CODE_HINT = re.compile(r"=>|&&|\|\||\bconst\s|\breturn\b|\bimport\s|\bfunction\b|\(\)|=\{|\bclassName\b|^\s*[})\]]")
TW_TOKEN = re.compile(r"^(?:[a-z]+:)*-?[a-z]+(?:-[\w./\[\]#%]+)+$|^(?:flex|grid|block|inline|hidden|relative|absolute|fixed|sticky|uppercase|italic|truncate|container|group|peer|underline|border|rounded|shadow|transition|antialiased)$")


def looks_like_code_or_classes(t: str) -> bool:
    if CODE_HINT.search(t):
        return True
    toks = t.split()
    if not toks:
        return True
    cls = sum(1 for x in toks if TW_TOKEN.match(x) or "/" in x and "." in x)
    return cls / len(toks) > 0.4


def words(t: str):
    return re.findall(r"[A-Za-zÀ-ÿ·'’-]+", t)


def prose_units_md(lines: list[str]):
    units = []
    in_fence = False
    in_front = False
    in_comment = False
    para: list[tuple[int, str]] = []

    def flush():
        if para:
            units.append(Unit("para", " ".join(t for _, t in para), para[0][0]))
            para.clear()

    for no, raw in enumerate(lines, 1):
        s = raw.strip()
        if no == 1 and s == "---":
            in_front = True
            continue
        if in_front:
            if s in ("---", "..."):
                in_front = False
            continue
        if s.startswith(("```", "~~~")):
            flush()
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if in_comment:
            if "-->" in s:
                in_comment = False
            continue
        if s.startswith("<!--"):
            flush()
            if "-->" not in s:
                in_comment = True
            continue
        if not s:
            flush()
            continue
        if s.startswith(("import ", "export ")) or (s.startswith("<") and s.endswith(">") and not re.search(r">[^<]{3,}<", s)):
            flush()
            continue
        if s.startswith("|") or re.match(r"^[-=]{3,}$", s) or s.startswith("    "):
            flush()
            continue
        m = re.match(r"^(#{1,6})\s+(.*?)\s*#*$", s)
        if m:
            flush()
            units.append(Unit("heading", m.group(2), no, len(m.group(1))))
            continue
        m = re.match(r"^(?:[-*+]|\d+[.)])\s+(.*)$", s)
        if m:
            flush()
            units.append(Unit("bullet", m.group(1), no))
            continue
        if raw.startswith(("  ", "\t")) and units and units[-1].kind == "bullet" and not para:
            units[-1].text += " " + s
            continue
        para.append((no, s))
    flush()
    return units


def blank_block(text: str, rx: re.Pattern) -> str:
    return rx.sub(lambda m: re.sub(r"[^\n]", " ", m.group(0)), text)


def prose_units_markup(text: str):
    t = blank_block(text, re.compile(r"<(script|style)\b[^>]*>.*?</\1>", re.S | re.I))
    t = blank_block(t, re.compile(r"<!--.*?-->", re.S))
    t = blank_block(t, re.compile(r"\{/\*.*?\*/\}", re.S))
    units = []
    spans = []
    line_of = LineIndex(t)
    for m in re.finditer(r"<h([1-6])\b[^>]*>(.*?)</h\1>", t, re.S | re.I):
        inner = re.sub(r"<[^>]+>|\{[^{}]*\}", " ", m.group(2))
        inner = html.unescape(re.sub(r"\s+", " ", inner)).strip()
        if inner:
            units.append(Unit("heading", inner, line_of(m.start()), int(m.group(1))))
        spans.append((m.start(), m.end()))
    for m in re.finditer(r">([^<>]+)<", t):
        if any(a <= m.start() < b for a, b in spans):
            continue
        chunk = re.sub(r"\{[^{}]*\}", " ", m.group(1))
        chunk = html.unescape(re.sub(r"\s+", " ", chunk)).strip()
        if not words(chunk) or looks_like_code_or_classes(chunk):
            continue
        if len(words(chunk)) < 3:
            units.append(Unit("short", chunk, line_of(m.start())))
            continue
        line = line_of(m.start(1) + len(m.group(1)) - len(m.group(1).lstrip()))
        units.append(Unit("para", chunk, line))
    # copy held in JS string literals (feature lists, CTA data)
    for m in re.finditer(r"""(?<![\w$])(?:title|label|heading|subtitle|description|desc|text|body|cta|caption|eyebrow|name|question|answer)\s*:\s*(["'`])((?:(?!\1)[^\\\n]|\\.){6,})\1""", t):
        s = html.unescape(m.group(2)).strip()
        if len(words(s)) >= 2 and not looks_like_code_or_classes(s):
            kind = "heading" if m.group(0).lstrip().startswith(("title", "heading")) else "para"
            units.append(Unit(kind, s, line_of(m.start()), 3))
    units.sort(key=lambda u: u.line)
    return units


# ---------------------------------------------------------------- language

STOP = {
    "ca": set("i els les amb per és són però també aquest aquesta això hi ho perquè quan molt més seu seva dels als pel pels l d de la el que una un en no ja".split()),
    "es": set("y los las con por es son pero también este esta esto muy más su sus porque cuando del al de la el que una un en no ya para se lo".split()),
    "en": set("the and of to is are that with for this was were it on be you we not but as have has an at by from or".split()),
}
STRONG = {
    "ca": set("i els amb per és però aquest aquesta això hi ho perquè molt dels pel pels va van tot està més seva seu cal fins".split()),
    "es": set("y los con por pero este esta esto muy para lo porque está más hay sus todo".split()),
    "en": set("the and of to is are that with for this was it".split()),
}


def detect_lang(t: str):
    toks = [w.lower() for w in re.findall(r"[A-Za-zÀ-ÿ]+", t)]
    toks += ["l", "d"] * len(re.findall(r"\b[ldLD]['’][a-zà-ÿ]", t))
    if len(toks) < 3:
        return None
    score = {k: sum(1 for w in toks if w in STRONG[k]) * 2 + sum(1 for w in toks if w in STOP[k]) for k in STOP}
    score["ca"] += 3 * len(re.findall(r"[àèò]|l·l|\b[ld]['’]\w|-(?:se|nos|vos|ho|hi|ne|lo|la|los|les)\b", t, re.I))
    score["es"] += 3 * len(re.findall(r"[áñ¿¡]|ción\b", t, re.I))
    best = max(score, key=score.get)
    if score[best] < 2:
        return None
    return best


# ------------------------------------------------------------------ prose rules

def L(*alts: str) -> re.Pattern:
    return re.compile(r"(?<![\w])(?:" + "|".join(alts) + r")(?![\w])", re.IGNORECASE)


OPENERS = {
    "en": L(r"I hope (?:this|my) (?:email|message|note) finds you well", r"I hope you(?:'re| are) (?:doing )?well", r"(?:I )?hope this helps", r"don't hesitate to", r"do not hesitate to",
            r"feel free to (?:reach out|contact|let me know|ask)", r"please let (?:me|us) know if you have any (?:other )?questions", r"thanks for reaching out", r"great question",
            r"in conclusion", r"to sum (?:it )?up", r"let's dive in", r"without further ado", r"I'd be (?:happy|glad) to help"),
    "ca": L(r"espero que (?:estiguis|estigueu|estigui|esteu) bé", r"disculpeu el silenci", r"perdona el silenci", r"no dubt(?:is|eu|i) (?:a|en)", r"rest(?:em|o) a (?:la )?(?:vostra|teva|seva) (?:entera )?disposició",
            r"quedo a l'espera", r"esperem que (?:tot )?(?:estigui|vagi) (?:tot )?bé", r"en resum,", r"en definitiva,", r"bona pregunta", r"sense més preàmbuls", r"som-hi!?", r"ja som aquí"),
    "es": L(r"espero que (?:te encuentres|estés|esté|se encuentre|estéis) bien", r"no dud(?:es|e|éis|en) en", r"qued(?:o|amos) a (?:tu|su|vuestra) (?:entera )?disposición", r"quedamos atentos",
            r"esperamos que todo (?:esté|vaya) bien", r"en resumen,", r"en definitiva,", r"buena pregunta", r"sin más preámbulos", r"¡claro!", r"¡por supuesto!"),
}
SIGNPOST = {
    "en": L(r"it'?s worth (?:noting|mentioning)", r"it is (?:worth|important to) not(?:e|ing)", r"it'?s important to (?:note|remember|understand)", r"let'?s (?:take a (?:closer )?look|explore|break (?:it|this) down|dive)",
            r"here'?s (?:the thing|what you need to know)", r"below,? you(?:'ll| will) find", r"in this (?:article|post|guide|section),? (?:we|you|I)", r"as (?:mentioned|discussed|noted) (?:above|earlier|before)",
            r"first and foremost", r"at the end of the day", r"when it comes to", r"in today'?s (?:fast-paced|digital|ever-changing|modern)", r"needless to say", r"the truth is", r"let me be clear", r"at its core"),
    "ca": L(r"cal (?:destacar|remarcar|tenir en compte|esmentar) que", r"val a dir que", r"és important (?:tenir en compte|destacar|remarcar|recordar) que", r"a continuació (?:us|t'|et|li) (?:expliquem|explico|detallem|presentem|mostrem)",
            r"tal com (?:hem|he) (?:dit|comentat|esmentat)", r"com (?:hem|he) (?:dit|comentat|esmentat) (?:abans|anteriorment)", r"anem a veure", r"a continuació (?:trobaràs|trobareu)", r"en aquest (?:article|apartat|document),? (?:us|t'|et)"),
    "es": L(r"cabe (?:destacar|señalar|mencionar|resaltar) que", r"es importante (?:tener en cuenta|destacar|señalar|recordar) que", r"a continuación (?:te|os|le) (?:explicamos|explico|detallamos|presentamos|mostramos)",
            r"como (?:hemos|he) (?:dicho|comentado|mencionado)", r"vamos a ver", r"veamos", r"a continuación (?:encontrarás|encontraréis)", r"en este (?:artículo|apartado|documento),? (?:te|os)"),
}
INFLATED = {
    "en": L(r"delve", r"delves", r"delving", r"tapestry", r"testament", r"pivotal", r"intricate", r"intricacies", r"interplay", r"meticulous(?:ly)?", r"underscores?", r"underscoring", r"realm",
            r"vibrant", r"bustling", r"boasts", r"garner(?:s|ed)?", r"bolster(?:s|ed)?", r"showcas(?:e|es|ing)", r"foster(?:s|ing)?", r"seamless(?:ly)?", r"leverag(?:e|es|ing)", r"holistic", r"synerg(?:y|ies)",
            r"multifaceted", r"embark(?:s|ing)?", r"elevate[sd]?", r"empower(?:s|ing)?", r"unlock(?:s|ing)?", r"harness(?:es|ing)?", r"transformative", r"cutting-edge", r"game-changer", r"ever-evolving",
            r"nestled", r"in the heart of", r"a myriad of", r"a plethora of", r"valuable insights", r"robust", r"crucial", r"navigat(?:e|ing) the"),
    "ca": L(r"potencia(?:r|m|t)?", r"impulsa(?:r|m)", r"apost(?:ar|em|a) per", r"posa(?:r|m) en valor", r"sense fissures", r"fonamental(?:s)?", r"crucial(?:s)?", r"holístic\w*", r"sinergi(?:a|es)",
            r"ecosistema", r"transformador\w*", r"revolucionari\w*", r"innovador\w*", r"d'avantguarda", r"de primer nivell", r"a un altre nivell", r"experiència immersiva", r"en l'era digital",
            r"en el panorama actual", r"endinsa(?:r-se|r-nos|m-nos)", r"testimoni de", r"un paper clau", r"aspecte clau", r"punts? clau", r"robust\w*"),
    "es": L(r"potencia(?:r|mos)", r"impulsa(?:r|mos)", r"apost(?:ar|amos) por", r"poner en valor", r"sin fisuras", r"fundamental(?:es)?", r"crucial(?:es)?", r"holístic\w*", r"sinergi(?:a|as)",
            r"ecosistema", r"transformador\w*", r"revolucionari\w*", r"innovador\w*", r"de vanguardia", r"de primer nivel", r"al siguiente nivel", r"experiencia inmersiva", r"en la era digital",
            r"en el panorama actual", r"sumérge(?:te|nos)", r"adentr(?:arse|arnos|émonos)", r"profundizar en", r"entramado", r"testimonio de", r"un papel (?:crucial|clave|fundamental)",
            r"cabe destacar", r"sin lugar a dudas", r"cautivador\w*", r"robust\w*"),
}
NEG_PARALLEL = {
    "en": [I(r"\bnot (?:just|only|merely|simply)\b[^.!?]{1,80}\bbut\b"), I(r"\b(?:it|this|that)(?:'s| is| isn't| is not) (?:not |n't )?(?:just|only|merely)?\s?(?:about )?[^.!?,;]{1,50}[,;:—–-]\s*(?:it|this|that)(?:'s| is)\b"),
           I(r"\bisn't (?:just|only|merely)\b"), I(r"\bno [a-z]+(?: [a-z]+)?\.\s+no [a-z]+(?: [a-z]+)?\.\s+just\b")],
    "ca": [I(r"\bno (?:és|són|era) (?:només|sols|solament|simplement)\b"), I(r"\bno només\b[^.!?]{1,100}\bsinó\b"), I(r"\bno (?:és|són) [^.!?,;]{1,50}[,;:—–]\s*(?:és|són)\b")],
    "es": [I(r"\bno (?:es|son|era) (?:solo|sólo|solamente|simplemente)\b"), I(r"\bno (?:solo|sólo|solamente)\b[^.!?]{1,100}\bsino\b"), I(r"\bno (?:es|son) [^.!?,;]{1,50}[,;:—–]\s*(?:es|son)\b")],
}
CAVEAT = {
    "ca": I(r",\s+(?:i\s+)?(?:no|mai)\s+(?:un|una|uns|unes|el|la|els|les|l['’]|de|del|dels|d['’]|com)\b\s*(?:[\w·'’-]+\s*){0,5}[.!]?$"),
    "es": I(r",\s+(?:y\s+)?(?:no|nunca)\s+(?:un|una|unos|unas|el|los|las|de|del|como)\b\s*(?:[\w'-]+\s*){0,5}[.!]?$"),
    "en": I(r",\s+(?:and\s+)?(?:not|never)\s+(?:a|an|the|by|from|as|in)\b\s*(?:[\w'-]+\s*){0,5}[.!]?$"),
}
SPLICE = {
    "en": I(r",\s+(?:it|this|that|they|we|you|he|she|there|these|those)\s?(?:is|are|was|were|has|have|had|will|can|could|should|does|do|did|isn't|aren't|wasn't|won't|can't|'s|'re|'ve|'ll)\b"),
    "ca": I(r",\s+(?:ens|us|hi ha|hi havia|tenim|teniu|tenen|hem|heu|han|farem|fem|fan|podem|poden|volem|volen|serà|seran|estem|està|estan|ara (?:volem|podem|tenim|hem)|ja (?:hem|tenim|podeu|pots|està))\b(?!\s+de\b)"),
    "es": I(r",\s+(?:nos|os|hay|había|tenemos|tenéis|tienen|hemos|habéis|han|haremos|hacemos|hacen|podemos|pueden|queremos|quieren|será|serán|estamos|está|están|ya (?:hemos|tenemos|está))\b"),
}
SUBORD = {
    "en": I(r"\b(?:if|when|whenever|because|although|though|while|as|since|after|before|once|unless|until|whether|so that|even|where|which|who|whose)\b"),
    "ca": I(r"\b(?:si|quan|perquè|encara que|tot i que|mentre|com que|ja que|un cop|després que|abans que|fins que|on|qui|que|els quals|la qual|el qual|sempre que|tant si)\b"),
    "es": I(r"\b(?:si|cuando|porque|aunque|mientras|como|ya que|una vez|después de que|antes de que|hasta que|donde|quien|que|los cuales|la cual|el cual|siempre que|tanto si)\b"),
}
TAILS = {
    "en": I(r",\s+(?:highlighting|underscoring|emphasizing|emphasising|reflecting|showcasing|ensuring|contributing to|fostering|solidifying|cementing|marking|signaling|signalling|paving the way)\b"),
}
CALQUES = {
    "ca": [("CA-02", None, L(r"a nivell (?:de|d')(?! mar)", r"en base a", r"jug\w* un (?:rol|paper)", r"(?:fa|fer|fan|feia|faria) sentit", r"eventualment", r"remarcable(?:s)?")),
           ("CA-02", None, re.compile(r"\ben lloc\s*(?:[.!»\"”)]|$)", re.I)),
           ("CA-02", "medium", L(r"(?:ha|han|has|hem|va|van) (?:estat|ser) \w+(?:at|ada|ats|ades|it|ida|its|ides|ut|uda|uts|udes) per")),
           ("CA-03", None, L(r"t(?:inc|ens|é|enim|eniu|enen|enir|enia|indré|indria|indries) que (?:\w+(?:ar|er|re|ir))", r"en quant a", r"a l'igual que", r"apart d[e']", r"al (?:arribar|sortir|entrar|fer|veure|tornar|acabar|començar|obrir|tancar)",
                                r"lo (?:important|millor|pitjor|més|bo|dolent|normal)", r"degut a", r"(?:envieu|enviar|envia|retorneu|retorna) el mateix")),
           ("CA-04", None, re.compile(r",\s*[a-zàèéíòóúïü]+(?:ant|ent|int)-se\b", re.I)),
           ("CA-11", None, L(r"realitz\w+", r"efectu\w+", r"procedir a", r"procedeix\w* a", r"dur a terme", r"comptar amb", r"compta amb", r"compten amb", r"disposa de", r"disposem de")),
           ("CA-13", None, L(r"e-?mail", r"online", r"click", r"login", r"log in", r"password"))],
    "es": [("ES-02", None, L(r"a nivel de(?! mar)", r"en base a", r"jug\w* un (?:rol|papel)", r"hac\w* sentido", r"eventualmente", r"remov(?:er|ido|ió|emos|emos)", r"este (?:correo|mensaje) (?:te|le) encuentre bien")),
           ("ES-02", None, re.compile(r"\ben su lugar\s*(?:[.!»\"”)]|$)", re.I)),
           ("ES-02", "medium", L(r"(?:fue|fueron|ha sido|han sido) \w+(?:ado|ada|ados|adas|ido|ida|idos|idas) por")),
           ("ES-03", None, re.compile(r",\s*\w+(?:ándose|iéndose)\b", re.I)),
           ("ES-08", None, L(r"realiz\w+", r"efectu\w+", r"proced\w+ a", r"llevar a cabo", r"lleva a cabo", r"cuenta con", r"contamos con", r"dispone de", r"disponemos de", r"(?:envíe|envíen|enviar|envía|rellene) (?:el|la) mism[oa]"))],
    "en": [("EN-02", None, L(r"empower(?:s)? your", r"supercharge\w*", r"unleash(?:es)? the power", r"transform your (?:business|workflow|team)", r"revolutioniz\w+", r"best-in-class", r"world-class",
                              r"industry-leading", r"enterprise-grade", r"next-generation", r"next-gen", r"future-proof", r"mission-critical", r"trusted by leading", r"built for the modern", r"drive growth",
                              r"(?:take|takes|taking) (?:it|your \w+) to the next level")),
           ("EN-05", None, L(r"stands? as a testament", r"plays? a (?:pivotal|crucial|key|vital) role", r"underscores? the importance", r"marks? a turning point", r"sets? the stage for",
                              r"indelible mark", r"deeply rooted in", r"reflects? a broader trend", r"a rich tapestry")),
           ("EN-06", None, L(r"experts (?:say|agree|believe)", r"studies (?:show|suggest|have shown)", r"research (?:shows|suggests)", r"industry reports suggest", r"observers have noted", r"many believe"))],
}
RESIDUE = L(r"as an AI(?: language model)?", r"as a large language model", r"(?:I )?hope this helps", r"certainly!", r"great question!?", r"knowledge cutoff", r"\[insert [^\]]+\]",
            r"com a model de llenguatge", r"espero que (?:t'|us )?(?:sigui útil|ajudi)", r"com a intel·ligència artificial", r"como modelo de lenguaje", r"espero que (?:te|os) (?:sirva|ayude)",
            r"como (?:una )?inteligencia artificial", r"let me know if you(?:'d)? (?:like|want|need)", r"here is (?:a|the) (?:revised|updated|rewritten) version", r"aquí tens (?:una|la) versió (?:revisada|actualitzada)",
            r"aquí tienes (?:una|la) versión (?:revisada|actualizada)")
INTERNAL_CS = re.compile(r"(?<![\w])(?:TODO|TBD|FIXME|XXX)(?![\w])")
INTERNAL = L(r"to be confirmed", r"subject to validation", r"pendent de validar", r"pendent de validació", r"per confirmar", r"sujet[oa]s? a validación", r"por confirmar", r"pendiente de validar")
PLACEHOLDER = L(r"lorem ipsum", r"\[(?:your|tu|el teu|la teva|insert|inserta|insereix|nom|name|company|empresa)[^\]]*\]", r"555-01\d\d", r"\(555\)", r"123 Main St(?:reet)?", r"dolor sit amet")
FAKE_NAMES = L(r"Acme(?: Corp| Inc)?", r"Globex", r"Initech", r"John Doe", r"Jane Doe", r"Jane Smith", r"John Smith", r"Sarah Chen", r"Alex Johnson", r"Lorem Corp", r"Emily Chen", r"Michael Chen")
NUMBERS = L(r"\d{1,3}(?:[.,]\d{3})*\s?\+\s+(?:happy |satisfied )?(?:customers|users|teams|clients|companies|businesses|clientes|usuarios|empresas|usuaris|empreses)",
            r"\d{2,3}\s?%\s+(?:satisfaction|satisfacción|satisfacció|of (?:our )?(?:customers|users))", r"\d+(?:\.\d+)?x (?:faster|more|better|más|més)", r"trusted by \d")
COUNT_TITLE = L(r"[1-9]\d?\s+(?:more\s+|més\s+|más\s+)?(?:things?|tips?|ways?|reasons?|keys?|secrets|facts|coses?|cosa|consells?|maneres|motius|claus|cosas?|consejos?|formas|razones|claves?)",
                r"1 cosa més", r"1 more thing", r"una cosa més")
GENERIC_HEAD = re.compile(r"^(?:key takeaways|key points|key features|things to (?:keep in mind|consider|know)|final thoughts|additional considerations|important information|why choose us|our values|the bottom line|in a nutshell|"
                          r"coses a tenir en compte|aspectes clau|punts clau|conclusions finals|consideracions addicionals|informació important|per què triar-nos|els nostres valors|en poques paraules|"
                          r"cosas a tener en cuenta|aspectos clave|puntos clave|conclusiones finales|consideraciones adicionales|información importante|por qué elegirnos|nuestros valores|en pocas palabras)\b", re.I)
DISTRIBUTIVE = re.compile(r"\b(?:cadascun|cadascuna|cadascú|each|cada uno|cada una|cada un)\b|\b(\w+) (?:by|a|per|rere|tras) \1\b|\b(?:step by step|one by one|una per una|un per un|pas a pas|paso a paso|uno a uno|una a una|uno por uno|una por una)\b", re.I)
GENERIC_UI = re.compile(r"^(?:submit|click here|learn more|read more|oops!?.*|uh-oh!?.*|something went wrong!?)$", re.I)
CTA = re.compile(r"^(?:learn more|get started|read more|find out more|discover more|saber más|leer más|descubre más|més informació|llegir més|descobreix-ho|descobreix més|veure més|ver más)\s*[→›>]?$", re.I)
LOWER_OK = {
    "ca": set("i o a e de del dels d en el la els les l al als per amb que un una uns unes sobre entre sense fins com".split()),
    "es": set("y o a e u de del en el la los las al por para con que un una unos unas sobre entre sin hasta como".split()),
}
INTENS = L(r"really", r"literally", r"genuinely", r"honestly", r"truly", r"deeply", r"fundamentally", r"inherently", r"incredibly", r"importantly", r"crucially", r"interestingly", r"actually", r"simply")


def sentences(t: str):
    parts = re.split(r"(?<=[.!?…])[\"»”)]*\s+(?=[\"«“(¿¡]?[A-ZÀ-Ý0-9])", t)
    return [p.strip() for p in parts if p.strip()]


def check_heading(u: Unit, lang, add):
    t = re.sub(r"[*_`]", "", u.text).strip()
    tl = t.rstrip(".:")
    if not tl:
        return
    if EMOJI.match(tl):
        add("W-38", u.line, "Heading starts with an emoji", t)
    if "," in tl:
        head, tail = tl.rsplit(",", 1)
        tw = words(tail)
        if 0 < len(tw) <= (6 if DISTRIBUTIVE.search(tail) else 4) and len(words(head)) >= 1 and not re.search(r"\d", tail) \
                and not re.search(r"(?<!\w)(?:i|y|and|o|or|e|u|&)(?!\w)", tail, re.I):
            if DISTRIBUTIVE.search(tail):
                add("W-30", u.line, "Comma-tag heading with a distributive tag", t, "high")
            else:
                add("W-30", u.line, "Comma-tag heading: say what the section contains", t)
    if tl.endswith("?") and u.level and u.level <= 3:
        add("W-15", u.line, "Question used as a heading", t)
    wc = len(words(tl))
    if wc >= 9 and not tl.endswith("?"):
        add("W-31", u.line, f"{wc}-word heading reads as a sentence or slogan", t)
    elif re.match(r"^(?:qué|què|per què|por qué|what|why|how|cómo|com)\s+\w+", tl, re.I) and not tl.endswith("?") and wc >= 4:
        add("W-31", u.line, "Question-shaped slogan heading", t)
    if GENERIC_HEAD.match(tl):
        add("W-34", u.line, "Generic heading", t)
    if COUNT_TITLE.search(tl):
        add("W-33", u.line, "Count used as a heading", t)
    if lang in ("ca", "es"):
        ms = list(re.finditer(r"[A-Za-zÀ-ÿ']+", tl))
        starts = {0} | {m.end() for m in re.finditer(r"[.!?]\s+[¿¡«\"(]*", tl)}
        ws = [m.group(0) for m in ms]
        rest = [m.group(0) for m in ms[1:] if m.start() not in starts]
        if len(ws) >= 3:
            later = [w for w in rest if w.lower() not in LOWER_OK[lang] and len(w) > 2]
            caps = [w for w in later if w[0].isupper() and not w.isupper()]
            func_caps = [w for w in rest if w.lower() in LOWER_OK[lang] and w[0].isupper() and not w.isupper()]
            if func_caps or (len(later) >= 3 and len(caps) == len(later)):
                add("W-32", u.line, "Title Case: this language uses sentence case", t)


def check_text(u: Unit, lang, add, file_lang):
    t = u.text
    lang = lang or file_lang
    plain = re.sub(r"\*\*|__|`", "", t)
    if ";" in plain and not re.search(r"&\w+;|&#\d+;", t):
        for s in sentences(plain):
            if re.search(r"\w\s*;\s+\w", s):
                add("W-10", u.line, "Semicolon in prose", s)
                break
    dashes = len(re.findall(r"—|\s–\s|\s--\s", plain))
    if dashes and not plain.lstrip().startswith(("—", "–")):
        add("W-11", u.line, f"{dashes} em dash(es) in prose", plain)
    quotes = len(re.findall(r"«[^»\n]{1,120}»|“[^”\n]{1,120}”", plain))
    if quotes:
        add("W-19", u.line, f"{quotes} pair(s) of « » or “ ” quotes", plain)
    for s in sentences(plain):
        m = re.search(r"([^:]{3,}):\s+([^:]+)$", s)
        if m and not re.search(r"https?$|\d$", m.group(1)):
            before, after = m.group(1), m.group(2)
            if len(words(before)) >= 4 and len(words(after)) >= 4 and after[:1].islower() and after.count(",") < 2 \
                    and not re.search(r"(?:following|example|e\.g|note|següents|exemple|nota|siguientes|ejemplo|per exemple|por ejemplo)$", before.strip(), re.I):
                add("W-12", u.line, "Colon used as a hinge between two clauses", s)
                break
    if lang in NEG_PARALLEL:
        for rx in NEG_PARALLEL[lang]:
            m = rx.search(plain)
            if m:
                add("W-13", u.line, "Negative parallelism", m.group(0))
                break
    if lang in OPENERS:
        m = OPENERS[lang].search(plain)
        if m:
            add("W-21", u.line, "Empty opener or closer", m.group(0))
        m = SIGNPOST[lang].search(plain)
        if m:
            add("W-26", u.line, "Signposting", m.group(0))
        hits = [m.group(0) for m in INFLATED[lang].finditer(plain)]
        if hits:
            add("W-29", u.line, "Inflated vocabulary: " + ", ".join(dict.fromkeys(h.lower() for h in hits)), plain,
                "medium" if len(hits) >= 2 or lang != "en" else "low")
        for rid, sev, rx in CALQUES.get(lang, []):
            m = rx.search(plain)
            if m:
                add(rid, u.line, RULES[rid][1], m.group(0), sev)
        for s in sentences(plain):
            m = SPLICE[lang].search(s)
            if not m:
                continue
            before = s[:m.start()]
            after = s[m.end():]
            if len(words(before)) >= 4 and len(words(after)) >= 2 and not SUBORD[lang].search(before) \
                    and not re.search(r"^\W*(?:and|but|or|so|then|i|o|però|y|pero|sino|també|también)\b", s[m.start() + 1:].strip(), re.I) \
                    and before.count(",") == 0:
                add("W-01", u.line, "Comma splice: two sentences joined by a comma", s)
                break
    if lang in TAILS:
        m = TAILS[lang].search(plain)
        if m:
            add("W-43", u.line, "Participle tail", m.group(0))
    if lang == "es":
        for s in sentences(plain):
            if s.endswith("?") and "¿" not in s and not (file_lang == "ca" and not re.search(r"[áñ¡]|ción\b", s, re.I)):
                add("ES-04", u.line, "Question without ¿", s)
                break
    if lang == "en" and len(INTENS.findall(plain)) >= 3:
        add("EN-04", u.line, "Three or more intensifier adverbs", plain)
    if len(re.findall(r"\*\*[^*]+\*\*", t)) >= 3 and u.kind == "para":
        add("W-37", u.line, "Bold scattered through a paragraph", t)
    if u.kind == "bullet" and EMOJI.match(plain.strip()):
        add("W-38", u.line, "Bullet starts with an emoji", plain)
    if u.kind == "para" and len(EMOJI.findall(plain)) >= 2:
        add("W-38", u.line, "Decorative emoji in prose", plain)
    if COUNT_TITLE.search(plain) and len(words(plain)) <= 12:
        add("W-33", u.line, "Numeral count in a short line", plain)
    m = RESIDUE.search(plain)
    if m:
        add("W-44", u.line, "Chatbot residue", m.group(0))
    m = INTERNAL_CS.search(t) or INTERNAL.search(t)
    if m:
        add("C-07", u.line, "Internal note in text", m.group(0))
    m = PLACEHOLDER.search(plain)
    if m:
        add("C-12", u.line, "Placeholder", m.group(0))
    m = FAKE_NAMES.search(plain)
    if m:
        add("C-02", u.line, "Placeholder name", m.group(0))
    m = NUMBERS.search(plain)
    if m:
        add("C-01", u.line, "Number that needs a source", m.group(0))
    if GENERIC_UI.match(plain.strip()):
        add("EN-09", u.line, "Generic UI string", plain)
    if u.kind == "para":
        ss = sentences(plain)
        run = 0
        for s in ss:
            run = run + 1 if len(words(s)) <= 6 else 0
            if run >= 3 and len(ss) >= 3:
                add("W-03", u.line, "Three or more very short sentences in a row", plain)
                break


file_kind_prose = [False]


def prose_checks(path: str, units: list[Unit], forced_lang, add):
    langs = {}
    for u in units:
        if u.kind != "heading":
            l = detect_lang(u.text)
            if l:
                langs[l] = langs.get(l, 0) + len(words(u.text))
    file_lang = forced_lang or (max(langs, key=langs.get) if langs else None)
    seen = {}
    bold_bullets = []
    ctas = []
    formula = [u for u in units if u.kind == "heading" and re.match(r"^\d[\d.,]*\s+\w+,\s", u.text)]
    if len(formula) >= 2:
        for u in formula:
            add("W-30", u.line, f"Count formula repeated in {len(formula)} headings", u.text, "high")
    caveats = []
    for u in units:
        if u.kind in ("para", "short", "heading"):
            ul = forced_lang or detect_lang(u.text) or file_lang
            if ul in CAVEAT:
                for s in sentences(u.text):
                    if CAVEAT[ul].search(s) and len(words(s)) <= 25:
                        caveats.append((u.line, s))
    if len(caveats) >= 3:
        add("W-18", caveats[0][0], f"{len(caveats)} sentences end in a caveat («…, no…»): keep the ones that matter", caveats[0][1])
        for line, s in caveats[1:]:
            add("W-18", line, "Caveat tail", s, "low")
    for u in units:
        if u.kind == "short":
            if CTA.match(u.text.strip()):
                ctas.append(u.line)
            elif GENERIC_UI.match(u.text.strip()):
                add("EN-09", u.line, "Generic UI string", u.text)
            continue
        lang = forced_lang or (detect_lang(u.text) if len(words(u.text)) >= 6 else None) or file_lang
        if u.kind == "heading":
            check_heading(u, lang, add)
        check_text(u, lang, add, file_lang)
        if u.kind == "bullet" and re.match(r"^\s*(?:\*\*|__)[^*_]{1,50}(?:\*\*|__)\s*[:.—–-]?\s*\S", u.text):
            bold_bullets.append(u.line)
        if CTA.match(u.text.strip()):
            ctas.append(u.line)
        if u.kind == "para":
            for s in sentences(u.text):
                key = re.sub(r"\W+", " ", s.lower()).strip()
                if len(key.split()) >= 8:
                    if key in seen:
                        add("W-20", u.line, f"Same sentence as line {seen[key]}", s)
                    else:
                        seen[key] = u.line
    if len(bold_bullets) >= 3:
        add("W-14", bold_bullets[0], f"{len(bold_bullets)} bullets that start with a bold label", "")
    if len(ctas) >= 3:
        add("C-04", ctas[0], f"Generic call to action repeated {len(ctas)} times", "")


# ------------------------------------------------------------------- driver

def scan_file(path: str, args) -> list[Finding]:
    try:
        with open(path, encoding="utf-8", errors="replace") as f:
            text = f.read()
    except OSError as e:
        print(f"detect.py: cannot read {path}: {e}", file=sys.stderr)
        return []
    if "anti-slop-ignore-file" in text:
        return []
    lines = text.split("\n")
    ext = os.path.splitext(path)[1].lower()
    findings: list[Finding] = []
    seen = set()

    def add(rule, line, msg, excerpt="", sev=None):
        sev = sev or RULES[rule][0]
        if SEV[sev] < SEV[args.min_severity]:
            return
        src = lines[line - 1] if 0 < line <= len(lines) else ""
        m = re.search(r"anti-slop-ignore(?!-file)((?:\s+[A-Z]{1,2}-\d{2})*)", src)
        if m and (not m.group(1).strip() or rule in m.group(1).split()):
            return
        key = (rule, line)
        if key in seen:
            return
        seen.add(key)
        ex = re.sub(r"\s+", " ", excerpt).strip()
        if len(ex) > 120:
            ex = ex[:117] + "..."
        findings.append(Finding(rule, sev, path, line, msg, ex))

    if ext in STYLE_EXT:
        design_checks(path, text, lines, True, add)
    elif ext in MARKUP_EXT:
        design_checks(path, text, lines, False, add)
        file_kind_prose[0] = False
        prose_checks(path, prose_units_markup(text), args.lang_forced, add)
    elif ext in PROSE_EXT:
        file_kind_prose[0] = True
        units = prose_units_md(lines) if ext != ".txt" else prose_units_txt(lines)
        prose_checks(path, units, args.lang_forced, add)
        if ext == ".mdx":
            design_checks(path, text, lines, False, add)
    return findings


def prose_units_txt(lines):
    units, para = [], []
    for no, raw in enumerate(lines + [""], 1):
        s = raw.strip()
        if s:
            para.append((no, s))
        elif para:
            units.append(Unit("para", " ".join(t for _, t in para), para[0][0]))
            para = []
    return units


def iter_files(paths, excludes):
    for p in paths:
        if os.path.isfile(p):
            yield p
            continue
        for root, dirs, files in os.walk(p):
            dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS and not d.startswith("."))
            for name in sorted(files):
                fp = os.path.join(root, name)
                if os.path.splitext(name)[1].lower() not in ALL_EXT:
                    continue
                if name.endswith((".min.css", ".min.js")):
                    continue
                if any(fnmatch.fnmatch(fp, g) or fnmatch.fnmatch(name, g) for g in excludes):
                    continue
                yield fp


def main(argv=None):
    ap = argparse.ArgumentParser(description="Heuristic detector for AI-slop patterns in design and text.")
    ap.add_argument("paths", nargs="*", default=["."])
    ap.add_argument("--json", action="store_true", help="JSON output")
    ap.add_argument("--min-severity", choices=list(SEV), default="low")
    ap.add_argument("--fail-on", choices=list(SEV) + ["none"], default="high")
    ap.add_argument("--lang", choices=["auto", "ca", "es", "en"], default="auto")
    ap.add_argument("--exclude", action="append", default=[], metavar="GLOB")
    ap.add_argument("--list-rules", action="store_true")
    args = ap.parse_args(argv)
    if args.list_rules:
        for rid, (sev, name) in RULES.items():
            print(f"{rid:6} {sev:7} {name}")
        return 0
    args.lang_forced = None if args.lang == "auto" else args.lang
    findings = []
    for fp in iter_files(args.paths, args.exclude):
        findings.extend(scan_file(fp, args))
    findings.sort(key=lambda f: (-SEV[f.severity], f.file, f.line))
    counts = {k: sum(1 for f in findings if f.severity == k) for k in SEV}
    if args.json:
        print(json.dumps({"findings": [asdict(f) for f in findings], "counts": counts}, ensure_ascii=False, indent=2))
    else:
        for f in findings:
            tail = f" | {f.excerpt}" if f.excerpt else ""
            print(f"{f.file}:{f.line}: {f.rule} [{f.severity}] {f.message}{tail}")
        print(f"\n{len(findings)} findings: {counts['high']} high, {counts['medium']} medium, {counts['low']} low", file=sys.stderr)
    if args.fail_on != "none" and any(SEV[f.severity] >= SEV[args.fail_on] for f in findings):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
