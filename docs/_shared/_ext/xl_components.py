"""Data-driven page components for the XLeRobot docs.

Each directive takes a YAML body and renders plain HTML. The English and
Chinese pages share the same structure and differ only in text. Styling lives
in ``docs/_shared/static/css/xl-theme.css``; the only script is the price
calculator in ``xl.js``. Text in the output stays selectable and is indexed by
Sphinx search, because raw HTML nodes are included in the search index.

Links in YAML may use ``doc:path/to/page`` (optionally ``#anchor``) for pages
in the same project. They are resolved to relative URLs, and a warning is
emitted when the page does not exist.

Inline text supports ``**bold**``, ```code``` and ``[label](url)`` only.
"""

from __future__ import annotations

import html
import json
import os
import re

import yaml
from docutils import nodes
from docutils.parsers.rst import Directive, directives
from sphinx.transforms import SphinxTransform
from sphinx.util import logging
from sphinx.util.osutil import relative_uri

logger = logging.getLogger(__name__)

_LINK = re.compile(r"\[([^\]]+)\]\(([^)\s]+)\)")
_BOLD = re.compile(r"\*\*(.+?)\*\*")
_CODE = re.compile(r"`([^`]+)`")


def _e(value) -> str:
    return html.escape("" if value is None else str(value), quote=True)


class _XlDirective(Directive):
    has_content = True
    option_spec = {"class": directives.class_option}

    @property
    def env(self):
        return self.state.document.settings.env

    def data(self):
        try:
            return yaml.safe_load("\n".join(self.content)) or {}
        except yaml.YAMLError as exc:  # pragma: no cover - reported to the author
            raise self.error(f"{self.name}: invalid YAML: {exc}")

    def url(self, target: str) -> str:
        if not target:
            return ""
        if not target.startswith("doc:"):
            return target
        doc, _, anchor = target[4:].partition("#")
        if doc not in self.env.found_docs:
            logger.warning(
                "%s: unknown document %r", self.name, doc,
                location=(self.env.docname, self.lineno),
            )
        builder = self.env.app.builder
        here = builder.get_target_uri(self.env.docname)
        uri = relative_uri(here, builder.get_target_uri(doc))
        return uri + ("#" + anchor if anchor else "")

    def inline(self, text) -> str:
        if text is None:
            return ""
        out = html.escape(str(text), quote=False)

        def link(match):
            href = _e(self.url(html.unescape(match.group(2))))
            return f'<a href="{href}">{match.group(1)}</a>'

        out = _CODE.sub(r"<code>\1</code>", out)
        out = _LINK.sub(link, out)
        return _BOLD.sub(r"<strong>\1</strong>", out)

    @staticmethod
    def icon(name) -> str:
        """``cart`` -> Font Awesome solid icon; non-ASCII text -> emoji."""
        if not name:
            return ""
        name = str(name)
        if not name.isascii():
            return f'<span class="xl-icon xl-icon--emoji" aria-hidden="true">{_e(name)}</span>'
        family = "fa-solid"
        if name.startswith("brands:"):
            family, name = "fa-brands", name.split(":", 1)[1]
        return f'<span class="xl-icon" aria-hidden="true"><i class="{family} fa-{_e(name)}"></i></span>'

    def chips(self, items) -> str:
        if not items:
            return ""
        inner = "".join(f'<span class="xl-chip">{self.inline(c)}</span>' for c in items)
        return f'<span class="xl-chips">{inner}</span>'

    def classes(self, *base) -> str:
        return " ".join([*base, *self.options.get("class", [])])

    def raw(self, markup: str):
        return [nodes.raw("", markup, format="html")]


class XlStats(_XlDirective):
    """Row of big numbers: ``- {value, label}``."""

    def run(self):
        items = self.data()
        cells = "".join(
            '<div class="xl-stat">'
            f'<p class="xl-stat__value">{self.inline(i.get("value"))}</p>'
            f'<p class="xl-stat__label">{self.inline(i.get("label"))}</p>'
            "</div>"
            for i in items
        )
        return self.raw(f'<div class="{self.classes("xl-stats")}" style="--xl-n:{len(items)}">{cells}</div>')


class XlFlow(_XlDirective):
    """Step diagram. ``items`` for one track, or ``lanes`` for several.

    Step: ``{title, text, icon, link, chips}``. Optional ``branch`` (one step
    shown under the track) and per-lane ``note``.
    """

    option_spec = {**_XlDirective.option_spec, "numbered": directives.flag}

    def step(self, item, index) -> str:
        num = f'<span class="xl-flow__num">{index:02d}</span>' if "numbered" in self.options else ""
        body = (
            f'{num}{self.icon(item.get("icon"))}'
            f'<span class="xl-flow__title">{self.inline(item.get("title"))}</span>'
            f'<span class="xl-flow__text">{self.inline(item.get("text"))}</span>'
            f'{self.chips(item.get("chips"))}'
        )
        link = item.get("link")
        card = (
            f'<a class="xl-flow__card" href="{_e(self.url(link))}">{body}</a>'
            if link else f'<div class="xl-flow__card">{body}</div>'
        )
        return f'<li class="xl-flow__step">{card}</li>'

    def track(self, items) -> str:
        steps = "".join(self.step(it, n) for n, it in enumerate(items, 1))
        return f'<ol class="xl-flow__track" style="--xl-n:{len(items)}">{steps}</ol>'

    def run(self):
        data = self.data()
        parts = []
        if "lanes" in data:
            for lane in data["lanes"]:
                note = lane.get("note")
                note_html = f'<span class="xl-lane__note">{self.inline(note)}</span>' if note else ""
                parts.append(
                    '<div class="xl-lane">'
                    f'<p class="xl-lane__label">{self.inline(lane.get("label"))}{note_html}</p>'
                    f'{self.track(lane.get("items", []))}</div>'
                )
            kind = "xl-flow--lanes"
        else:
            parts.append(self.track(data.get("items", [])))
            kind = "xl-flow--journey"
        branch = data.get("branch")
        if branch:
            parts.append(
                f'<a class="xl-flow__branch" href="{_e(self.url(branch.get("link")))}">'
                f'{self.icon(branch.get("icon"))}'
                f'<span><strong>{self.inline(branch.get("title"))}</strong> '
                f'{self.inline(branch.get("text"))}</span>'
                '<span class="xl-flow__go" aria-hidden="true">›</span></a>'
            )
        return self.raw(f'<div class="{self.classes("xl-flow", kind)}">{"".join(parts)}</div>')


class XlCompose(_XlDirective):
    """``groups`` joined by "+", then "=" and a ``result`` tile."""

    def run(self):
        data = self.data()
        blocks = []
        for n, group in enumerate(data.get("groups", [])):
            if n:
                blocks.append('<div class="xl-compose__op" aria-hidden="true">+</div>')
            items = "".join(
                f'<li>{self.icon(it.get("icon"))}<span><strong>{self.inline(it.get("label"))}</strong>'
                f'<small>{self.inline(it.get("note"))}</small></span></li>'
                for it in group.get("items", [])
            )
            blocks.append(
                '<div class="xl-compose__group">'
                f'<p class="xl-compose__eyebrow">{self.inline(group.get("eyebrow"))}</p>'
                f'<p class="xl-compose__title">{self.inline(group.get("title"))}</p>'
                f'<ul>{items}</ul></div>'
            )
        result = data.get("result") or {}
        blocks.append('<div class="xl-compose__op" aria-hidden="true">=</div>')
        blocks.append(
            '<div class="xl-compose__result">'
            f'<p class="xl-compose__eyebrow">{self.inline(result.get("eyebrow"))}</p>'
            f'<p class="xl-compose__title">{self.inline(result.get("title"))}</p>'
            f'<p class="xl-compose__text">{self.inline(result.get("text"))}</p>'
            f'{self.chips(result.get("chips"))}</div>'
        )
        return self.raw(f'<div class="{self.classes("xl-compose")}">{"".join(blocks)}</div>')


class XlPricing(_XlDirective):
    """Price calculator. Works without JS: it then shows the base price.

    ``currencies: [{code, symbol}]``, ``base: {label, prices}``,
    ``choices: [{legend, type: radio|checkbox, options: [{label, prices}]}]``,
    plus ``labels: {currency, total, included}`` and an optional ``note``.
    """

    def run(self):
        data = self.data()
        serial = self.env.new_serialno("xl-pricing")
        currencies = data["currencies"]
        labels = data.get("labels", {})
        first = currencies[0]["code"]
        symbols = {c["code"]: c["symbol"] for c in currencies}

        def money(prices, mode):
            value = prices.get(first, 0)
            if mode == "option" and not value:
                return _e(labels.get("included", "Included"))
            sign = "+" if mode == "option" else "~"
            return f"{sign}{_e(symbols[first])}{value:,}"

        seg = "".join(
            f'<label><input type="radio" name="xl-cur-{serial}" value="{_e(c["code"])}" data-currency'
            f'{" checked" if i == 0 else ""}><span>{_e(c.get("label", c["code"]))}</span></label>'
            for i, c in enumerate(currencies)
        )
        base = data["base"]
        rows = [
            '<div class="xl-pricing__base">'
            f'<span>{self.inline(base["label"])}</span>'
            f'<span class="xl-price" data-mode="base" data-prices="{_e(json.dumps(base["prices"]))}">'
            f'{money(base["prices"], "base")}</span></div>'
        ]
        for c_index, choice in enumerate(data.get("choices", [])):
            kind = "radio" if choice.get("type") == "radio" else "checkbox"
            opts = []
            for o_index, opt in enumerate(choice["options"]):
                checked = " checked" if kind == "radio" and o_index == 0 else ""
                prices = _e(json.dumps(opt["prices"]))
                opts.append(
                    f'<label class="xl-opt"><input type="{kind}" name="xl-opt-{serial}-{c_index}" '
                    f'data-prices="{prices}"{checked}>'
                    f'<span class="xl-opt__label">{self.inline(opt["label"])}</span>'
                    f'<span class="xl-price" data-mode="option" data-prices="{prices}">'
                    f'{money(opt["prices"], "option")}</span></label>'
                )
            rows.append(f'<fieldset><legend>{self.inline(choice["legend"])}</legend>{"".join(opts)}</fieldset>')
        note = data.get("note")
        note_html = f'<p class="xl-pricing__note">{self.inline(note)}</p>' if note else ""
        markup = (
            f'<div class="{self.classes("xl-pricing")}" data-xl-pricing '
            f'data-symbols="{_e(json.dumps(symbols, ensure_ascii=False))}" '
            f'data-included="{_e(labels.get("included", "Included"))}">'
            f'<div class="xl-pricing__options">'
            f'<div class="xl-seg" role="radiogroup" aria-label="{_e(labels.get("currency", "Currency"))}">{seg}</div>'
            f'{"".join(rows)}</div>'
            '<div class="xl-pricing__total">'
            f'<p class="xl-pricing__label">{self.inline(labels.get("total", "Estimated total"))}</p>'
            f'<p class="xl-pricing__sum" aria-live="polite">{money(base["prices"], "base")}</p>'
            f"{note_html}</div></div>"
        )
        return self.raw(markup)


class XlTimeline(_XlDirective):
    """``- {version, date, text, state: done|current|next, badge}``."""

    def run(self):
        items = self.data()
        lis = []
        for it in items:
            state = it.get("state", "done")
            badge = f' <span class="xl-badge">{_e(it["badge"])}</span>' if it.get("badge") else ""
            lis.append(
                f'<li class="xl-timeline__item is-{_e(state)}"><span class="xl-timeline__dot"></span>'
                f'<p class="xl-timeline__version">{self.inline(it.get("version"))}{badge}</p>'
                f'<p class="xl-timeline__date">{self.inline(it.get("date"))}</p>'
                f'<p class="xl-timeline__text">{self.inline(it.get("text"))}</p></li>'
            )
        return self.raw(
            f'<ol class="{self.classes("xl-timeline")}" style="--xl-n:{len(items)}">{"".join(lis)}</ol>'
        )


class XlCards(_XlDirective):
    """Card grid. ``- {title, eyebrow, badge, text, notes, bullets, links,
    image, image_alt, icon, link}``. ``:visible: N`` puts the remaining cards
    in a collapsed "more" block labelled with ``:more:``.
    """

    option_spec = {
        **_XlDirective.option_spec,
        "columns": directives.positive_int,
        "visible": directives.nonnegative_int,
        "more": directives.unchanged,
        "variant": directives.unchanged,
    }

    def card(self, it) -> str:
        parts = []
        if it.get("image"):
            src = _e(self.url(it["image"]))
            parts.append(
                f'<a class="xl-card__media" href="{src}">'
                f'<img src="{src}" alt="{_e(it.get("image_alt", ""))}" loading="lazy"></a>'
            )
        body = [self.icon(it.get("icon"))]
        eyebrow = self.inline(it.get("eyebrow"))
        if it.get("badge"):
            eyebrow += f' <span class="xl-badge">{_e(it["badge"])}</span>'
        if eyebrow:
            body.append(f'<p class="xl-card__eyebrow">{eyebrow}</p>')
        title = self.inline(it.get("title"))
        if it.get("link"):
            title = f'<a href="{_e(self.url(it["link"]))}">{title}</a>'
        body.append(f'<p class="xl-card__title">{title}</p>')
        if it.get("text"):
            body.append(f'<p class="xl-card__text">{self.inline(it["text"])}</p>')
        for key in ("bullets", "notes"):
            if it.get(key):
                lis = "".join(f"<li>{self.inline(x)}</li>" for x in it[key])
                body.append(f'<ul class="xl-card__{key}">{lis}</ul>')
        if it.get("links"):
            links = "".join(
                f'<a href="{_e(self.url(l["url"]))}">{self.inline(l["label"])}</a>' for l in it["links"]
            )
            body.append(f'<p class="xl-card__links">{links}</p>')
        parts.append(f'<div class="xl-card__body">{"".join(body)}</div>')
        return f'<article class="xl-card">{"".join(parts)}</article>'

    def grid(self, items) -> str:
        cols = self.options.get("columns", 3)
        variant = self.options.get("variant")
        cls = self.classes("xl-cards", f"xl-cards--{variant}" if variant else "")
        return f'<div class="{cls}" style="--xl-cols:{cols}">{"".join(self.card(i) for i in items)}</div>'

    def run(self):
        items = self.data()
        visible = self.options.get("visible")
        if visible is None or visible >= len(items):
            return self.raw(self.grid(items))
        rest = items[visible:]
        label = _e(self.options.get("more", "More")).replace("{n}", str(len(rest)))
        return self.raw(
            self.grid(items[:visible])
            + f'<details class="xl-more"><summary>{label}</summary>{self.grid(rest)}</details>'
        )


class xl_section_marker(nodes.Element):
    """Placeholder that adds classes to its enclosing section."""


class XlSection(Directive):
    """Add classes to the enclosing section: ``:band: gray`` and ``:class:``."""

    option_spec = {"band": directives.unchanged, "class": directives.class_option}

    def run(self):
        classes = list(self.options.get("class", []))
        if self.options.get("band"):
            classes.append(f"xl-band-{self.options['band']}")
        return [xl_section_marker(classes=classes)]


class XlSectionTransform(SphinxTransform):
    default_priority = 200

    def apply(self, **kwargs):
        for marker in list(self.document.findall(xl_section_marker)):
            section = marker.parent
            while section is not None and not isinstance(section, nodes.section):
                section = section.parent
            if section is not None:
                section["classes"].extend(marker["classes"])
            marker.parent.remove(marker)


def _page_context(app, pagename, templatename, context, doctree):
    """Link to the same page in the other language (or its home page)."""
    is_zh = (app.config.language or "en").lower().startswith("zh")
    other = "en" if is_zh else "zh"
    default = "https://xlerobot.readthedocs.io/{}/latest/".format("en" if is_zh else "zh-cn")
    base = os.environ.get("XL_ALT_LANG_BASE", default)
    other_src = os.path.normpath(os.path.join(app.confdir, "..", "..", other, "source"))
    exists = any(os.path.exists(os.path.join(other_src, pagename + ext)) for ext in (".md", ".rst"))
    context["xl_is_zh"] = is_zh
    context["xl_alt_lang_url"] = base + (pagename + ".html" if exists else "index.html")
    context["xl_alt_lang_label"] = "English" if is_zh else "中文"


def setup(app):
    for name, cls in {
        "xl-stats": XlStats,
        "xl-flow": XlFlow,
        "xl-compose": XlCompose,
        "xl-pricing": XlPricing,
        "xl-timeline": XlTimeline,
        "xl-cards": XlCards,
        "xl-section": XlSection,
    }.items():
        app.add_directive(name, cls)
    app.add_node(xl_section_marker)
    app.add_transform(XlSectionTransform)
    app.connect("html-page-context", _page_context)
    return {"version": "1.0", "parallel_read_safe": True, "parallel_write_safe": True}
