import json
from chembl_webresource_client.new_client import new_client


def getchembllotusold():
    lotus_inchikeys_path = r'lotus_inchikeys.json'
    lotus_inchikeys_list = json.load(open(lotus_inchikeys_path))
    lotus_inchikeys_length = str(len(lotus_inchikeys_list))

    count = 0
    # get the inichkeys that have been checked in a previous run
    done = open('lotus_checked.txt', 'r')
    done = done.read()
    # open text files to append data - needed if the code has to be restarted
    checked = open('lotus_checked.txt', 'a')
    chemblids = open('lotus_chemblids.txt', 'a')
    # instantiate chembl client
    molecule = new_client.molecule
    # iterate through the inchikeys
    for inchikey in lotus_inchikeys_list:
        count = count + 1
        if done.find(inchikey) != -1:
            print(inchikey + " done")
            continue
        # check unchecked data
        # time.sleep(1)
        mol = molecule.filter(molecule_structures__standard_inchi_key=inchikey).only(['molecule_chembl_id'])
        print('processed ' + str(count) + ' of ' + lotus_inchikeys_length)
        if mol:
            chemblid = mol[0]['molecule_chembl_id']
            chemblids.write(chemblid + '\n')
        checked.write(inchikey + '\n')

    checked.close()
    chemblids.close()


def getchembllotus():
    # work out which inchikeys are in lotus and chembl (v34) and save to json file
    # open the inchikey files
    ljsn = open('lotus_inchikeys.json', 'r')
    cjsn = open('chembl_inchikeys.json', 'r')

    # open json file to store the inchikey intersection set
    ijsn = open('chembl__lotus_inchikeys.json', 'w')

    # import the data into variables (Python lists)
    lkeys = json.load(ljsn)
    ckeys = json.load(cjsn)

    # check to see if each lotus inchikey is in the chembl set
    both = []
    lkeys.sort()
    for key in lkeys:
        print(key)
        if key in ckeys:
            both.append(key)

    # write out the set of inchikeys in both
    ijsn.write(json.dumps(both))
    print(str(len(both)) + " inchikeys found...")
    ljsn.close()
    cjsn.close()
    ijsn.close()
    return True


def raw2newckeys():
    # quick code to convert mysql output of inchikey dump to JSON array (half the size)
    ojsn = open('chembl_inchikeys_old.json', 'r')
    okeys = json.load(ojsn)
    ojsn.close()

    njsn = open('chembl_inchikeys.json', 'w')
    data = okeys[0]['data']
    nkeys = []
    count = 1
    for key in data:
        nkeys.append(key['standard_inchi_key'])
        count += 1
        print(count)

    print(len(nkeys))
    njsn.write(json.dumps(nkeys))
    njsn.close()
    return True
