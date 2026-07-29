# How to populate candidates.csv with verified SMILES

The developability screen needs **PubChem-verified** SMILES. This environment
can't reach PubChem, so retrieve them on your side — two easy options:

## Option A — one click per compound (REST, returns a CSV)
Open the `lookup_url` in each row of `candidates.csv`. It returns a small CSV
containing the PubChem **CID** and the **IsomericSMILES**. Paste the SMILES into
the `smiles` column and the CID into `pubchem_cid`.

> If a `lookup_url` returns an error about property names (PubChem renamed some
> properties in 2025), replace `IsomericSMILES,CanonicalSMILES` in the URL with
> `SMILES,ConnectivitySMILES`, or just use Option B.

## Option B — the compound page
Go to `https://pubchem.ncbi.nlm.nih.gov/#query=<name>`, open the compound,
confirm the name matches, and copy the **Isomeric SMILES** (now labeled
"SMILES") from *Names and Identifiers → Canonical/Isomeric SMILES*.

## Notes
- `zelasudil` (RXC007) and any clinical-code compounds (e.g., GNS-3595) may not
  resolve by name — search the code or the developer's structure, and confirm.
- Use the **isomeric** SMILES (includes stereochemistry) where available.
- Then run:  `python developability_screen.py`  (it auto-detects candidates.csv).

## Fastest path
Paste the SMILES back to me (or upload the CSV PubChem gives you) and I'll fill
`candidates.csv`, run the screen, and drop the results into the dossier for you.
