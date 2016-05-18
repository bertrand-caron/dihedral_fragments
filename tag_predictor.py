from API_client.api import API
from fragment_dihedrals.fragment_dihedral import re_pattern_matching_for
from fragment_dihedrals.chemistry import CHEMICAL_GROUPS

CHEMICAL_GROUPS_MATCHING_PATTERNS = [(moiety, re_pattern_matching_for(pattern, debug=True, metadata=moiety)) for (moiety, pattern) in CHEMICAL_GROUPS if pattern]

def dihedrals(molecule):
    return molecule.dihedral_fragments

def tags_for_dihedral(dihedral_string):
    tags = [moiety for (moiety, matching_function) in CHEMICAL_GROUPS_MATCHING_PATTERNS if matching_function(dihedral_string)]
    assert len(tags) <= 1, 'No dihedral should be matched by more than one rule: {0}'.format(tags)
    return tags

def tags_for_molecule(molecule):
    return set(
        reduce(
            lambda acc, e: acc + e,
            [tags_for_dihedral(dihedral) for dihedral in dihedrals(molecule)],
            [],
        ),
    )

def yes_or_no(query):
    choice = raw_input(query)
    if choice == 'y':
       return True
    elif choice == 'n':
       return False
    else:
       sys.stdout.write("Please respond with 'yes' or 'no'")

IGNORE_FILE = '.ignore'

def get_ignored_molids():
    from os.path import exists
    if exists(IGNORE_FILE):
        with open(IGNORE_FILE) as fh:
            return set([int(line) for line in fh.read().splitlines()])
    else:
        return set()

if __name__ == '__main__':
    print tags_for_dihedral("O,H|C|C|C,H")

    #print tags_for_dihedral('H,H,H|C|C|CL,CL,CL')
    #print tags_for_dihedral('CL,H|C|C|H,H')
    #print tags_for_dihedral('O,O,O|P|O|C')
    #print tags_for_dihedral('C|O|P|O,O,O')

    ignored_molids = get_ignored_molids()

    fh = open(IGNORE_FILE, 'a')

    DATA_SETS_TAGS = set(['Shivakumar et al.', 'Marenich et al.', 'Mobley et al.'])

    api = API(debug=True, api_format='pickle')
    molecules = api.Molecules.search(tag='Mobley et al.', max_atoms=15)
    for molecule in molecules:
        if molecule.molid in ignored_molids:
            continue

        print molecule
        new_tags = tags_for_molecule(molecule)
        old_tags = set(molecule.tags) - DATA_SETS_TAGS

        if old_tags != new_tags:
            print 'Old tags are: {0}'.format(list(old_tags))
            print 'New tags are: {0}'.format(list(new_tags))

            try:
                if yes_or_no('Add those ({0}) tags ?'.format(new_tags - old_tags)):
                    print 'Adding new tags ...'
                    for tag_name in new_tags - old_tags:
                        print molecule.tag(tag_name=tag_name)
                    print 'Successfully added new tags'
                else:
                    fh.write(str(molecule.molid) + '\n')
            except KeyboardInterrupt:
                fh.close()
                raise
        print
