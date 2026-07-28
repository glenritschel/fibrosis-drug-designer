# Anti-Fibrotic Placeholder Drug Designer

An interactive, browser-based tool for reasoning about **why anti-fibrotic drugs
cause the side effects they do — and which of those are actually fixable.**

It encodes a small causal map:

```
drug  →  molecular target  →  organ / tissue  →  outcome (efficacy or adverse effect)
```

and lets you design a hypothetical ("placeholder") drug **forward** — pick the
targets it hits and how it's delivered, and see the predicted efficacy and
adverse effects — or **backward** — state the outcome you want and let the tool
find a target set + delivery route that achieves it.

> **The one idea.** Some adverse effects are *off-target* (the drug hits a gene it
> shouldn't) and vanish when you make the molecule more selective. But the worst
> ones are *on-target in the wrong tissue* — the same target that helps in a
> myofibroblast harms elsewhere (e.g. SRC-family inhibition reversing fibrosis in
> the skin, but driving pulmonary hypertension in lung vessels). **Target
> selectivity cannot remove those. Tissue localization can.**

## Try it

Open [`index.html`](index.html) in any modern browser — it's a single
self-contained file, no build step, no dependencies.

- **Forward mode** — check the targets to hit (therapeutic) and spare
  (anti-targets), choose a delivery localization, and read off predicted
  efficacy, a fibrosis-reversal verdict, the active adverse effects, and a design
  score. Every adverse effect is labelled *off-target* (removable by sparing the
  gene) or *on-target / wrong tissue* (removable only by localization).
- **Backward mode** — set a goal ("achieve reversal, avoid all serious effects,
  systemic only") and the tool searches the design space and loads the best
  placeholder that satisfies it.
- **Optimized presets** — one-click, exhaustively-searched optima for each
  delivery route (fibrotic-targeted, inhaled, topical, systemic).

Also included in [`tools/`](tools/): a static layered **interaction network** of
the same map.

## What's in the model

Target universe (illustrative): SRC-family, MEK1/2, DDR1, PDGFR, FAK (PTK2),
ROCK2, YAP/TAZ as therapeutic mechanotransduction / anti-fibrotic nodes; KIT,
BTK, LCK, TYK2/HCK, EPH, hERG, ROCK1 as anti-targets. Delivery routes: systemic,
lung/inhaled, skin/topical, fibrotic-tissue-targeted.

See [`docs/concept.md`](docs/concept.md) for the biology and the design logic,
and [`docs/adverse_effect_reference.md`](docs/adverse_effect_reference.md) for
the per-target adverse-effect grounding and sources.

## The video

[`manim/fibrosis_selectivity.py`](manim/fibrosis_selectivity.py) is a
[Manim](https://www.manim.community/) scene that animates the core insight in
~45 seconds. See [`manim/README.md`](manim/README.md) to render it.

## ⚠️ Important — what this is and isn't

This is a **conceptual / educational instrument.** The efficacy weights and
severities are **illustrative design heuristics, not measured pharmacology.** The
*structure* of the conclusions (which target you must drop per delivery route;
that no systemic design reaches zero adverse effects) is robust; the specific
numbers are not. Do **not** use it to rank real compounds or predict real safety
margins. Swap in measured selectivity and potency data before drawing any
program decision.

## License

MIT — see [`LICENSE`](LICENSE).

Built by Glen Ritschel (Ritschel Research), 2026.
