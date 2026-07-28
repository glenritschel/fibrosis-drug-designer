# Adverse-effect & target reference

Grounding for the target biology and adverse-effect assignments in the tool.
Effects are tagged by the **tissue** in which they arise (which is what makes
them removable by localization or not).

## Therapeutic / anti-fibrotic targets

| Target | Anti-fibrotic rationale | Key liability (tissue) |
|---|---|---|
| SRC-family | Myofibroblast mechanotransduction | Bleeding (platelets); **PAH & pleural effusion (pulmonary endothelium)** |
| MEK1/2 | MAPK/ERK in fibrotic signaling | Retinopathy (retina), rash (skin), ↓LVEF (heart), CK (muscle), diarrhea (GI), neuro (CNS) — all on-target in normal tissue |
| DDR1 | Collagen-sensing RTK; pro-fibrotic | Comparatively clean; mild epithelial (GI) |
| PDGFR | Anti-fibrotic | Fluid retention / edema (vasculature) |
| FAK (PTK2) | Focal-adhesion mechanotransduction; antifibrotic in IPF models | GI toxicity; hematologic (marrow) |
| ROCK2 | Rho-kinase mechanotransduction + Th17/Treg | Infection / immunosuppression; GI. ROCK1 cross-inhibition adds cardiovascular effects |
| YAP/TAZ | Master mechanotransduction output | GI epithelial toxicity, immunosuppression, impaired wound healing (in fibrotic tissue) |

## Anti-targets (no anti-fibrotic rationale here)

| Target | Adverse effect (tissue) |
|---|---|
| KIT | Myelosuppression / cytopenias (marrow) |
| BTK | Bleeding (platelets); immunosuppression (immune) |
| LCK | Immunosuppression (T cells) |
| TYK2 / HCK | Immunosuppression / infection (immune) |
| EPH (EPHB/EPHA) | Vascular remodeling (pulmonary endothelium) |
| KCNH2 (hERG) | QT prolongation (cardiac) |
| ROCK1 | Hypotension / cardiovascular (cardiac) |

## Selected sources

- Rix U et al. *Chemical proteomic profiles of the BCR-ABL inhibitors imatinib,
  nilotinib, and dasatinib.* Blood 2007;110(12):4055. — dasatinib off-target kinome.
- Hantschel O et al. *The Btk tyrosine kinase is a major target of dasatinib.* PNAS 2007.
- Dasatinib-induced pulmonary arterial hypertension: case series & population
  studies (Eur Respir J 2017;50:1700217; and reviews) — SRC-mediated pulmonary
  endothelial dysfunction; ~0.45–5% incidence; often reversible.
- MEK-inhibitor ocular toxicity reviews (retinal vein occlusion, serous
  retinopathy) — on-target MEK/ERK in retinal pigment epithelium.
- Belumosudil (ROCK2 inhibitor, ~100× ROCK2/ROCK1 selective): FDA-approved for
  chronic GVHD; Th17/Treg + antifibrotic; adverse events predominantly infection,
  asthenia, nausea, diarrhea.
- Focal adhesion kinase (FAK/PTK2) in fibrosis: antifibrotic in bleomycin
  pulmonary fibrosis models; FAK inhibitor development literature.
- YAP/TAZ–TEAD (Hippo pathway) inhibition: mechanotransduction master node in
  fibrosis; systemic inhibition toxicity-limited (intestinal/epithelial
  homeostasis, immune, tumor-suppressive roles).

> Assignments are simplified to one primary tissue per effect for the model's
> logic. Real target pharmacology is richer; treat this as a teaching scaffold.
