
kws = set(["name", "gender", "mother", "father", "spouse", "born",
           "birth_place", "died", "death_place", "buried" "married",
           "marriage_place", "place", "source", "notes", "tagline"])

class Person(object):

   def __init__(self, info):
       self.birth = '?'
       self.died = '?'
       self.idx = ''
       self.gen = None
       self.col = None
       self.birth_place = None
       self.death_place = None

       for key in kws:
           setattr(self, key, info[key] if key in info else None)

   def __str__(self):
       return "{0}\n{1}-{2}\n".format(self.name, self.birth, self.death)


class Family(dict):

    def __init__(self):
        pass

    def root():
        return self._root

def read_input(filename):
    fam = Family()
    with open(filename, 'r') as f:
        line = f.readline()
        while line != "":
            person = _get_person(f, line)
            line = f.readline()
            fam[person.name] = person

    for person in fam.values():
        if person.mother is not None:
            person.mother = fam[person.mother] if isinstance(person.mother, basestring) \
                                               else person.mother.name
        if person.father is not None:
            person.father = fam[person.father] if isinstance(person.father, basestring) \
                                               else person.father.name
    return fam


def _get_person(f, line):

    while(line.split() == ""):
        f = line.readline()

    info = {}
    while(len(line.split()) > 0):
        kw = line.split(":")[0]
        if kw in kws:
            info[kw] = "".join(line.split(":")[1:]).strip()
        line = f.readline()

    return Person(info)
