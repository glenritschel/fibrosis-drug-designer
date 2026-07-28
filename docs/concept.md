# The concept: on-target ≠ off-tissue

Anti-fibrotic drug programs keep running into the same wall: a compound that
convincingly quiets scar-forming myofibroblasts also does something harmful
elsewhere. The reflex is to make the molecule *more selective*. This tool exists
to show, concretely, when that helps and when it can't.

## Two kinds of adverse effect

Model the biology as a directed map:

```
drug → molecular target → organ / tissue → outcome
```

Every adverse effect then falls into one of two classes:

**Off-target.** The drug binds a gene that has no part in the therapeutic
mechanism. Dasatinib, for example, is a promiscuous kinase inhibitor: beyond its
intended targets it hits KIT (→ cytopenias), the hERG channel (→ QT
prolongation), and BTK (→ bleeding), among ~100 others. These harms are
*removable by selectivity* — a cleaner molecule that spares those genes simply
loses those effects, at no cost to efficacy.

**On-target, wrong tissue.** The harm comes from the *therapeutic* target doing
its job in a tissue where you didn't want it. SRC-family inhibition is a
legitimate anti-fibrotic mechanism in the myofibroblast — but the identical
inhibition in the pulmonary endothelium contributes to pulmonary arterial
hypertension, and in platelets to bleeding. MEK inhibition reverses fibrotic
signaling, but the same MAPK/ERK blockade in the retina, skin, heart, and gut
produces retinopathy, rash, reduced cardiac function, and diarrhea. **No amount
of target selectivity removes these**, because there is no wrong target to
remove — only a wrong location.

## The lever is localization, not selectivity

If the second class is the dominant safety problem — and for the kinase
inhibitors studied here it is — then the design axis that matters is *where the
drug is allowed to act*, not *what it binds*. Restrict exposure to fibrotic
tissue (targeted delivery, local administration, a prodrug activated in the
fibrotic compartment) and the off-tissue harms fall away while efficacy at the
disease site is preserved.

The tool makes this literal: switch a design from *systemic* to
*fibrotic-tissue-targeted* and the serious adverse effects disappear from the
map, with efficacy unchanged.

## What an exhaustive search of the model finds

Searching every target combination against every delivery route (with the tool's
illustrative weights) yields a clean pattern:

- **Every delivery route can reach the efficacy ceiling with zero adverse
  effects** — *except systemic*, which never does. The best a systemic (oral)
  design achieves is to give up the three strongest targets (SRC, MEK, YAP) and
  settle for FAK + ROCK2 + PDGFR + DDR1: high efficacy, but a handful of
  non-serious effects.
- **Each targeted route forces you to drop exactly one high-value target** — the
  one whose harm lands in the tissue that route can't avoid:
  - *fibrotic-targeted* drops **YAP/TAZ** (its wound-healing liability is in
    fibrotic tissue itself — the one place you can't localize away from);
  - *inhaled* drops **SRC** (inhaled delivery still reaches pulmonary
    endothelium → PAH);
  - *topical* drops **MEK** (topical reaches skin → rash).
- **FAK and ROCK2 appear in every optimum** — their liabilities sit in tissues
  none of the targeted routes reach, so they are "free" mechanotransduction
  targets.

The deepest version of the lesson is YAP/TAZ: the single most potent node in the
model is excluded from the best targeted design *because its benefit and its harm
occur in the same tissue.* When benefit and harm co-localize, even perfect
targeting can't separate them — the clearest possible statement that this is a
localization problem, not a selectivity one.

## Caveat

The efficacy weights and severity scores in the tool are **illustrative
heuristics for exploring trade-offs, not validated pharmacology.** The structure
of these findings is robust to the exact numbers; the numbers themselves are not
a basis for any real program decision.
