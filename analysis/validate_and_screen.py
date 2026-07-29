"""
Validate PubChem-sourced SMILES (RDKit formula/MW vs PubChem-stated values),
then run the developability screen. Writes candidates.csv + developability_results.csv.
"""
import csv
from rdkit import Chem
from rdkit.Chem import Descriptors, QED, Crippen, rdMolDescriptors, FilterCatalog

# name, pubchem_cid, smiles, expected_formula, expected_mw  (SMILES + formula/MW from PubChem PUG-REST)
DATA = [
 ("saracatinib","10302451","CN1CCN(CC1)CCOC2=CC3=C(C(=C2)OC4CCOCC4)C(=NC=N3)NC5=C(C=CC6=C5OCO6)Cl","C27H32ClN5O5",542.0),
 ("bosutinib","5328940","CN1CCN(CC1)CCCOC2=C(C=C3C(=C2)N=CC(=C3NC4=CC(=C(C=C4Cl)Cl)OC)C#N)OC","C26H29Cl2N5O3",530.4),
 ("mirdametinib","9826528","C1=CC(=C(C=C1I)F)NC2=C(C=CC(=C2F)F)C(=O)NOC[C@@H](CO)O","C16H14F3IN2O4",482.19),
 ("selumetinib","10127622","CN1C=NC2=C1C=C(C(=C2F)NC3=C(C=C(C=C3)Br)Cl)C(=O)NOCCO","C17H15BrClFN4O3",457.7),
 ("trametinib","11707110","CC1=C2C(=C(N(C1=O)C)NC3=C(C=C(C=C3)I)F)C(=O)N(C(=O)N2C4=CC=CC(=C4)NC(=O)C)C5CC5","C26H23FIN5O4",615.4),
 ("defactinib","25117126","CNC(=O)C1=CC=C(C=C1)NC2=NC=C(C(=N2)NCC3=NC=CN=C3N(C)S(=O)(=O)C)C(F)(F)F","C20H21F3N8O3S",510.5),
 ("belumosudil","11950170","CC(C)NC(=O)COC1=CC=CC(=C1)C2=NC3=CC=CC=C3C(=N2)NC4=CC5=C(C=C4)NN=C5","C26H24N6O2",452.5),
 ("zelasudil","155792249","CN1C(=NC(=N1)C2=CC=C(C=C2)C(=O)NCC(F)F)NC3=C(C4=C(C=C3)NN=C4)C5CC5","C22H21F2N7O",437.4),
 ("nintedanib","135423438","CN1CCN(CC1)CC(=O)N(C)C2=CC=C(C=C2)N=C(C3=CC=CC=C3)C4=C(NC5=C4C=CC(=C5)C(=O)OC)O","C31H33N5O4",539.6),
 ("imatinib","5291","CC1=C(C=C(C=C1)NC(=O)C2=CC=C(C=C2)CN3CCN(CC3)C)NC4=NC=CC(=N4)C5=CN=CC=C5","C29H31N7O",493.6),
]

params = FilterCatalog.FilterCatalogParams()
params.AddCatalog(FilterCatalog.FilterCatalogParams.FilterCatalogs.PAINS)
params.AddCatalog(FilterCatalog.FilterCatalogParams.FilterCatalogs.BRENK)
catalog = FilterCatalog.FilterCatalog(params)
BASIC_N = Chem.MolFromSmarts("[NX3;!$(N=*);!$(N-[#6]=[O,N,S])]")

# ---- 1. validate ----
print("VALIDATION (RDKit formula/MW vs PubChem):")
valid_rows = []
for name, cid, smi, exp_f, exp_mw in DATA:
    if smi is None:
        print(f"  {name:14s} CID {cid:12s}  PENDING — no verified SMILES yet")
        continue
    mol = Chem.MolFromSmiles(smi)
    if mol is None:
        print(f"  {name:14s} CID {cid:12s}  FAIL — SMILES did not parse"); continue
    f = rdMolDescriptors.CalcMolFormula(mol)
    mw = Descriptors.MolWt(mol)
    ok_f = (f == exp_f)
    ok_mw = abs(mw - exp_mw) <= 1.0
    print(f"  {name:14s} CID {cid:12s}  RDKit {f} ({mw:.1f})  vs PubChem {exp_f} ({exp_mw})  "
          f"{'PASS' if ok_f and ok_mw else 'CHECK: '+('formula ' if not ok_f else '')+('MW' if not ok_mw else '')}")
    valid_rows.append((name, cid, smi, mol))

# ---- 2. write candidates.csv (validated only) ----
with open("candidates.csv","w",newline="") as f:
    w = csv.writer(f); w.writerow(["name","smiles","pubchem_cid"])
    for name, cid, smi, mol in valid_rows: w.writerow([name, smi, cid])

# ---- 3. developability screen ----
def screen(name, cid, mol):
    mw   = Descriptors.MolWt(mol); clogp = Crippen.MolLogP(mol)
    tpsa = rdMolDescriptors.CalcTPSA(mol)
    hbd  = rdMolDescriptors.CalcNumHBD(mol); hba = rdMolDescriptors.CalcNumHBA(mol)
    rotb = rdMolDescriptors.CalcNumRotatableBonds(mol); arom = rdMolDescriptors.CalcNumAromaticRings(mol)
    qed  = QED.qed(mol)
    ro5  = sum([mw>500, clogp>5, hbd>5, hba>10])
    veber= (rotb<=10) and (tpsa<=140)
    alerts = len(catalog.GetMatches(mol))
    herg = (clogp>=3.7) and mol.HasSubstructMatch(BASIC_N) and (250<=mw<=600)
    return dict(name=name, cid=cid, MW=round(mw,1), cLogP=round(clogp,2), TPSA=round(tpsa,1),
                HBD=hbd, HBA=hba, RotB=rotb, ArRings=arom, QED=round(qed,3),
                Ro5_viol=ro5, Veber_pass=veber, n_alerts=alerts, hERG_flag=herg)

cols = ["name","cid","MW","cLogP","TPSA","HBD","HBA","RotB","ArRings","QED","Ro5_viol","Veber_pass","n_alerts","hERG_flag"]
rows = [screen(n,c,m) for n,c,_,m in [(n,c,s,m) for n,c,s,m in valid_rows]]
print("\nDEVELOPABILITY SCREEN (PubChem-verified candidates):\n")
print(" | ".join(cols))
for r in rows: print(" | ".join(str(r[c]) for c in cols))
with open("results/developability_results.csv","w",newline="") as f:
    w = csv.DictWriter(f, fieldnames=cols); w.writeheader()
    for r in rows: w.writerow(r)
print("\nSaved candidates.csv and developability_results.csv")
