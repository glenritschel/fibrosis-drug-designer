"""
Reproducible physicochemical / developability screen (RDKit).

This is a runnable PIPELINE + demonstration. It computes drug-likeness,
physicochemical properties, structural-alert flags, and a lipophilicity/hERG
risk heuristic for any set of candidate structures.

IMPORTANT: to screen the actual candidate agents for a filing, create
`candidates.csv` with columns  name,smiles,pubchem_cid  using SMILES VERIFIED
against PubChem — do not trust hand-entered drug SMILES. RDKit will parse an
incorrect SMILES silently, so parse success is NOT an identity check.

Below it runs on a few reference molecules with unambiguous SMILES so the exact
metric definitions and outputs are demonstrated.
"""
import csv, os
from rdkit import Chem
from rdkit.Chem import Descriptors, QED, Crippen, rdMolDescriptors
from rdkit.Chem import FilterCatalog

# --- structural-alert catalogs (PAINS + Brenk) ---
params = FilterCatalog.FilterCatalogParams()
params.AddCatalog(FilterCatalog.FilterCatalogParams.FilterCatalogs.PAINS)
params.AddCatalog(FilterCatalog.FilterCatalogParams.FilterCatalogs.BRENK)
catalog = FilterCatalog.FilterCatalog(params)

BASIC_N = Chem.MolFromSmarts("[NX3;!$(N=*);!$(N-[#6]=[O,N,S])]")  # rough basic amine

def screen(name, smiles, cid=""):
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return {"name": name, "error": "unparseable SMILES"}
    mw   = Descriptors.MolWt(mol)
    clogp= Crippen.MolLogP(mol)
    tpsa = rdMolDescriptors.CalcTPSA(mol)
    hbd  = rdMolDescriptors.CalcNumHBD(mol)
    hba  = rdMolDescriptors.CalcNumHBA(mol)
    rotb = rdMolDescriptors.CalcNumRotatableBonds(mol)
    arom = rdMolDescriptors.CalcNumAromaticRings(mol)
    qed  = QED.qed(mol)
    ro5  = sum([mw > 500, clogp > 5, hbd > 5, hba > 10])          # Lipinski violations
    veber= (rotb <= 10) and (tpsa <= 140)                        # Veber oral pass
    alerts = [e.GetDescription() for e in catalog.GetMatches(mol)]
    herg_risk = (clogp >= 3.7) and mol.HasSubstructMatch(BASIC_N) and (250 <= mw <= 600)
    return {"name": name, "cid": cid, "MW": round(mw,1), "cLogP": round(clogp,2),
            "TPSA": round(tpsa,1), "HBD": hbd, "HBA": hba, "RotB": rotb, "ArRings": arom,
            "QED": round(qed,3), "Ro5_viol": ro5, "Veber_pass": veber,
            "n_alerts": len(alerts), "hERG_flag(heuristic)": herg_risk}

# use candidates.csv if provided, else a DEMONSTRATION set (SMILES are certain)
rows = []
if os.path.exists(os.path.join(os.path.dirname(__file__), "candidates.csv")):
    with open(os.path.join(os.path.dirname(__file__), "candidates.csv")) as f:
        for r in csv.DictReader(f):
            rows.append(screen(r["name"], r["smiles"], r.get("pubchem_cid","")))
    src = "candidates.csv (user-supplied, verify vs PubChem)"
else:
    demo = [  # unambiguous reference SMILES — DEMONSTRATION ONLY
        ("Aspirin (ref)",   "CC(=O)Oc1ccccc1C(=O)O"),
        ("Ibuprofen (ref)", "CC(C)Cc1ccc(cc1)C(C)C(=O)O"),
        ("Caffeine (ref)",  "Cn1cnc2c1c(=O)n(C)c(=O)n2C"),
        ("Nilotinib-like fragment (ref)", "Cc1ccc(cc1Nc1nccc(n1)-c1cccnc1)C(=O)N"),
    ]
    rows = [screen(n, s) for n, s in demo]
    src = "DEMONSTRATION reference set (replace with candidates.csv for filing)"

cols = ["name","cid","MW","cLogP","TPSA","HBD","HBA","RotB","ArRings","QED",
        "Ro5_viol","Veber_pass","n_alerts","hERG_flag(heuristic)"]
print(f"Developability screen — source: {src}\n")
print(" | ".join(cols))
for r in rows:
    print(" | ".join(str(r.get(c,"")) for c in cols))

with open("results/developability_results.csv","w",newline="") as f:
    w = csv.DictWriter(f, fieldnames=cols); w.writeheader()
    for r in rows: w.writerow({c: r.get(c,"") for c in cols})
print("\nSaved developability_results.csv")
print("Metric key: Ro5_viol = Lipinski violations (>=2 flags oral-drug-likeness concern);",
      "Veber_pass = RotB<=10 & TPSA<=140; hERG_flag = lipophilic (cLogP>=3.7) + basic center heuristic.")
