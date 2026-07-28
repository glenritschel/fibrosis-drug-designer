# LinkedIn post — draft

> Educational / thought-leadership angle. Copy the body below; attach the rendered
> video; swap in your repo URL. Suggested variants and posting notes follow.

---

## Post body

A more selective drug won't fix fibrosis. I built a little tool to show why — and the reason surprised me enough that I animated it.

The instinct, when a drug has bad side effects, is always the same: make it cleaner. More selective. Hit only the target you want.

For fibrosis — I've been deep in scleroderma — that instinct is only half right.

Some side effects are **off-target**: the drug hits genes it was never meant to. Those you really can engineer away by making the molecule more selective.

But the worst effects often come from the **right target in the wrong tissue.** The same kinase that quiets a scar-forming cell can, in the blood vessels of the lung, help drive pulmonary hypertension. No amount of target selectivity separates those two outcomes — it's the *same target*, just in the wrong place.

So the lever that actually works isn't selectivity. It's **localization** — where the drug is allowed to act.

I turned the whole causal map (drug → targets → tissues → outcomes) into an interactive designer. Pick your targets and a delivery route, and watch which harms you can design out and which stubbornly remain. Run it forward from a molecule, or backward from the outcome you want. It's in the browser, and the code is open.

(It's a conceptual model — illustrative weights, not validated potencies — built to make the trade-off *legible*, not to rank real compounds.)

▶️ [video]
🔗 Tool + code: github.com/<your-handle>/fibrosis-drug-designer

Curious what the drug-delivery and translational crowd thinks: is localization an underrated design axis?

#DrugDiscovery #Fibrosis #Scleroderma #ComputationalBiology #Pharmacology #DrugDelivery

---

## Alternate opening hooks

- "Everyone says: make the drug more selective. For fibrosis, that advice quietly fails — here's the 40-second version."
- "The same enzyme that heals a scar can wreck a lung. That one fact reshapes how you'd design an anti-fibrotic. I made it interactive."
- "I spent a while convinced target selectivity was the answer to drug side effects. Then I mapped it out and changed my mind."

## Posting notes

- **First line is everything** on LinkedIn — it's the only thing shown before "…see more." Keep the hook on line 1, then a blank line.
- **Native video beats a link.** Upload the MP4 directly to the post rather than linking it; LinkedIn suppresses reach on posts whose main payload is an outbound link. Put the GitHub URL in the body and/or the first comment.
- **Put the repo link in the first comment** too — some report better reach when the post body has no external link. Test what works for your audience.
- **Aspect ratio:** render a square (1:1) or vertical (4:5) version for mobile feed if you can; the default 16:9 works but is smaller in-feed. See manim/README.md for the crop/format flags.
- **Length:** ~150–220 words performs well. This draft is ~230; trim the parenthetical if you want it tighter.
- **Tag** a couple of people or a lab working in fibrosis / drug delivery to seed engagement (only if genuine).
- **IP check first:** confirm with counsel that nothing here is new, unprotected disclosure before it goes public.
