import json
from chembl_webresource_client.new_client import new_client

lotus_inchikeys_path = r'lotus_compounds_inchikeys.json'
lotus_inchikeys_list = json.load(open(lotus_inchikeys_path))
lotus_inchikeys_length = str(len(lotus_inchikeys_list))

chemblids = []
count = 1
for inchikey in lotus_inchikeys_list:
    molecule = new_client.molecule
    mol = molecule.filter(molecule_structures__standard_inchi_key=inchikey).only(['molecule_chembl_id'])
    print('processed ' + str(count) + ' of ' + lotus_inchikeys_length)
    count = count + 1
    if mol:
        chemblid = mol[0]['molecule_chembl_id']
        chemblids.append(chemblid)

print(len(chemblids))
with open('lotus_chemblids.json', 'w') as outfile:
    outfile.write(json.dumps(chemblids))