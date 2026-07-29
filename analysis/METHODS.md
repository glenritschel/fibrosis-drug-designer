# In-silico support dossier
### Computational basis for a provisional patent — fibrosis-localized multikinase inhibition (SSc)

**Purpose.** This dossier assembles the computational evidence and reproducible protocols supporting the invention, for inclusion in / reference by a provisional patent specification. It is organized so that the parts that are *executed and rigorous* (the target-profile optimization; the developability pipeline) are distinguished from the parts specified as *reproducible protocols* for a licensee with laboratory or larger compute resources to run (target-activity QSAR, docking, wet-lab).

**Honest scope.** Efficacy/severity weights in the optimization are illustrative design heuristics, not measured pharmacology; the *structure* of the conclusions is the finding. No wet-lab data is asserted. This supports a provisional (priority + enabled method + credible computational utility); experimental reduction to practice is expected downstream.

---

## 1. Method — target-profile optimization  *(executed)*

**Model.** A causal map `drug → molecular target → tissue → outcome` scores a candidate drug by (i) predicted anti-fibrotic efficacy = sum of per-target weights (capped 100) and (ii) an adverse-effect penalty = severity-weighted sum of active adverse effects, where an adverse effect is "active" only if its tissue is reachable by the chosen delivery localization. Design score = efficacy − penalty. Therapeutic targets: SRC-family, MEK1/2, FAK(PTK2), ROCK2, PDGFR, DDR1, YAP/TAZ. Delivery routes: systemic, lung/inhaled, skin/topical, fibrotic-tissue-targeted.

**Reproducibility.** Full enumeration of every target subset × delivery route. Script: `optimization_analysis.py`; machine-readable output: `optimization_results.json`. **508 designs evaluated.**

## 2. Result — optimal design per delivery route

| Delivery route | Optimal target set | Efficacy | Adverse effects | Design score |
|---|---|---|---|---|
| **Fibrotic-targeted** *(global best)* | SRC + MEK + FAK + ROCK2 | 100 | 0 | 100 |
| **Inhaled** | MEK + FAK + ROCK2 + PDGFR | 100 | 0 | 100 |
| **Topical** | SRC + FAK + ROCK2 + PDGFR | 100 | 0 | 100 |
| **Systemic (oral)** | FAK + ROCK2 + PDGFR + DDR1 | 95 | 6 (0 serious) | 56 |

**Structural findings (robust to the exact weights):**
- **No systemic design reaches zero adverse effects** — confirmed by exhaustive search. Every targeted route can.
- **Each targeted route drops exactly one high-value target** — the one whose harm lands in the tissue that route cannot avoid: fibrotic-targeted drops YAP (its harm is *in* fibrotic tissue); inhaled drops SRC (reaches pulmonary endothelium → PAH); topical drops MEK (reaches skin → rash).
- **FAK + ROCK2 appear in every optimum** — their liabilities sit in tissues no targeted route reaches.

See `optimization_figure.png`.

## 3. Method — developability screen  *(executed pipeline; demonstration)*

**Pipeline.** `developability_screen.py` (RDKit) computes, per candidate: MW, cLogP (Crippen), TPSA, HBD, HBA, rotatable bonds, aromatic rings, QED, Lipinski (Ro5) violations, Veber oral pass, PAINS+Brenk structural-alert count, and a lipophilicity/basic-center **hERG-risk heuristic**. Output: `developability_results.csv`.

**Verification.** SMILES were retrieved from PubChem (PUG-REST, by name → CID) and each was validated in RDKit: the RDKit-computed molecular formula and weight matched the PubChem-stated values for **all ten** candidates (`validate_and_screen.py`), and the structures were rendered for visual confirmation (`candidate_structures.png`). This confirms the structures are correct, not merely parseable.

**Executed results — PubChem-verified candidates.** (`developability_results.csv`)

| Candidate (CID) | Target | MW | cLogP | TPSA | HBD | HBA | QED | Ro5 viol. | Veber | alerts | hERG (heur.) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| saracatinib (10302451) | SRC-fam | 542.0 | 3.94 | 90.4 | 1 | 10 | 0.45 | 1 | pass | 0 | **flag** |
| mirdametinib (9826528) | MEK1/2 | 482.2 | 2.47 | 90.8 | 4 | 5 | 0.36 | 0 | pass | 2 | no |
| selumetinib (10127622) | MEK1/2 | 457.7 | 3.53 | 88.4 | 3 | 5 | 0.39 | 0 | pass | 2 | no |
| trametinib (11707110) | MEK1/2 | 615.4 | 3.94 | 107.1 | 2 | 5 | 0.33 | 1 | pass | 1 | no |
| defactinib (25117126) | FAK | 510.5 | 2.40 | 142.1 | 3 | 9 | 0.42 | 1 | **fail** | 0 | no |
| belumosudil (11950170) | ROCK2 | 452.5 | 4.82 | 104.8 | 3 | 6 | 0.33 | 0 | pass | 0 | **flag** |
| zelasudil (155792249) | ROCK2 | 437.5 | 3.97 | 100.5 | 3 | 5 | 0.41 | 0 | pass | 0 | **flag** |
| bosutinib (5328940) | SRC-fam | 530.5 | 5.19 | 82.9 | 1 | 8 | 0.38 | 2 | pass | 1 | **flag** |
| nintedanib (135423438) | PDGFR | 539.6 | 4.04 | 101.5 | 2 | 7 | 0.27 | 1 | pass | 1 | **flag** |
| imatinib (5291) | DDR1/PDGFR | 493.6 | 4.59 | 86.3 | 2 | 7 | 0.39 | 0 | pass | 0 | **flag** |

**Reading.** All ten are drug-like small molecules (as expected — most are approved or clinical), so developability is not the program risk; the risks are target-profile assembly and delivery. The screen flags the expected, manageable liabilities: defactinib's high polar surface area (TPSA 142, marginal Veber), bosutinib's two Lipinski flags (MW/cLogP), and a lipophilicity/basic-center hERG heuristic flag on the basic-amine kinase inhibitors (saracatinib, bosutinib, belumosudil, zelasudil, nintedanib, imatinib) — each warrants a dedicated hERG assay, consistent with these being real drugs whose cardiac profiles are already managed clinically. The heuristic is crude and over-flags basic lipophilic scaffolds; treat as "check", not "fail".

## 4. Protocol — off-target / selectivity prediction  *(to run on verified structures)*

For each candidate, enumerate predicted targets and confirm the anti-targets are spared:
1. Submit canonical SMILES to **SwissTargetPrediction**, **SEA** (Similarity Ensemble Approach), and **Polypharmacology Browser (PPB3)**.
2. **Pass criterion:** none of KIT, BTK, LCK, EPH among top predicted targets; and a predicted-selectivity margin (on-target pIC50 − max anti-target pIC50) ≥ 2 log units.
3. **hERG** is checked independently with a dedicated model (ADMET-AI / pkCSM) in addition to the heuristic above — non-negotiable, as QT is the model's serious cardiac node.

## 5. Protocol — molecular docking  *(method disclosure)*

Dock each candidate into the ATP site of each on-target and representative anti-targets; compare binding poses/scores as a physics-based cross-check on QSAR.
- **Tool:** AutoDock Vina (open source) or equivalent; ligands prepared with RDKit/Meeko, exhaustiveness ≥ 16, 3 replicates.
- **Structures (representative — select best co-crystal per series from the PDB):** c-Src (e.g., 2SRC), MEK1 (e.g., 3EQH), FAK (e.g., 2ETM), ROCK2 (verify current best), PDGFR/DDR1 (verify), and anti-targets KIT (1T46) and hERG (cryo-EM 5VA1) for liability checks.
- **Readout:** favorable, consistent poses in on-target ATP pockets; weak/absent binding in anti-target pockets.

## 6. Localization rationale — FAP targeting  *(literature-grounded)*

The optimization shows the serious toxicities are on-target/off-tissue, removable only by localization. **Fibroblast activation protein (FAP)** is selectively expressed on activated (myo)fibroblasts in fibrotic skin and lung and near-absent in normal adult tissue; it is validated as a fibrosis marker via **FAPI-PET imaging of interstitial lung disease** and implicated in skin fibrosis. This supports FAP as the molecular address for fibrotic-tissue localization, via: FAP-activated prodrug (Gly-Pro–capped payload cleaved locally by FAP protease), FAP-binding conjugate/nanocarrier, or FAPI-ligand–guided delivery. FAPI-PET additionally provides a companion-diagnostic / stratification readout.

## 7. De novo generative design  *(specified)*

For novel single-molecule composition-of-matter realizing the fibrotic-targeted profile, the scoring specification for REINVENT4 (open-source RL generative design) is provided separately (`reinvent4_fibrotic_scoring.toml`): rewards predicted potency on SRC/MEK/FAK/ROCK2, penalizes KIT/BTK/hERG, constrains QED/SA/MW/logP.

## 8. Reproducibility & limitations

Executed scripts (`optimization_analysis.py`, `developability_screen.py`, `make_figure.py`) run on standard Python + RDKit + matplotlib and regenerate all executed results. Limitations: heuristic efficacy weights; developability ≠ target activity; off-target/docking/QSAR require verified structures and are specified as protocols; FAP-targeted small-molecule delivery is emerging. None of this substitutes for wet-lab validation.

## 9. Artifact manifest
- `optimization_analysis.py`, `optimization_results.json`, `optimization_figure.png` — target-profile optimization (executed)
- `developability_screen.py`, `developability_results.csv` — developability pipeline (executed demo; template for verified candidates)
- `make_figure.py` — figure generation
- `reinvent4_fibrotic_scoring.toml` — de-novo scoring spec (delivered previously)

## 10. Sources
- Saracatinib in pulmonary fibrosis: https://www.atsjournals.org/doi/10.1164/rccm.202010-3832OC
- Nintedanib targets & SSc-ILD approval: https://pubs.acs.org/doi/10.1021/jm501562a
- Zelasudil (ROCK2, Ph2a IPF): https://www.redxpharma.com/our-pipeline/zelasudil/
- Belumosudil DDI/transporters: https://accp1.onlinelibrary.wiley.com/doi/10.1002/jcph.70018
- Kinase-inhibitor combinations for selectivity (eLife): https://elifesciences.org/articles/86189
- FAP / FAPI-PET in fibrotic ILD: https://jnm.snmjournals.org/content/63/1/125
- FAPα in fibrosis (review): https://pmc.ncbi.nlm.nih.gov/articles/PMC10742035/
- REINVENT4: https://github.com/MolecularAI/REINVENT4 ; SwissTargetPrediction: https://www.expasy.org/resources/swisstargetprediction

*Prepared 2026-07-28 · Ritschel Research, in collaboration with Claude (Anthropic). Discovery-stage computational support; not legal advice.*
