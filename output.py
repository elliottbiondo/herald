from os import system
import numpy as np

page_margin = 0.5
box_height = 2.5
box_width = 6.5
box_margin = 0.2
row_spacing = 7.
col_spacing = box_width + 1.5
shift = 3

PX_TO_CM = 35.43307

def _birth_lines(person):
    line_style = '\t<path style="stroke:#000000;fill:none"\n'
    s = ''

    if person.mother or person.father:
        child_x = person.child_x*PX_TO_CM
        child_y = person.child_y*PX_TO_CM
        parent = person.mother if person.mother else person.father
        parent_x = parent.parent_x*PX_TO_CM
        parent_y = parent.parent_y*PX_TO_CM
        if parent.gender == "male":
            mpx = parent_x + (col_spacing - box_width)/2.*PX_TO_CM
        else:
            mpx = parent_x - (col_spacing - box_width)/2.*PX_TO_CM
        mpy = parent_y
        mpx2 = mpx
        mpy2 = mpy + box_height/2.*PX_TO_CM
        s = line_style
        s += 'd="M {0:.5} {1} L {2} {3} L {4} {5}"/>\n'.format(
              child_x, child_y, mpx2, mpy2, mpx, mpy)

    if person.mother:
        s += line_style
        s += 'd="M {0:.5} {1:.5} L {2:.5} {3:.5}"/>\n'.format(
              mpx, mpy, person.mother.parent_x*PX_TO_CM - shift,
              person.mother.parent_y*PX_TO_CM)
    if person.father:
        s += line_style
        s += 'd="M {0:.5} {1:.5} L {2:.5} {3:.5}"/>\n'.format(
              mpx, mpy, person.father.parent_x*PX_TO_CM - shift,
              person.father.parent_y*PX_TO_CM)
    return s

def _person_text(person, width, height, people_per_gen, gen_ranks):

    x = width/2. - people_per_gen[person.gen]*col_spacing/2. \
                 + gen_ranks[person.gen].index(person.col)*col_spacing \
                 + (col_spacing - box_width)/2.0
    y = height - person.gen*row_spacing - page_margin - box_height/2. \
        - (row_spacing - box_height)/2.0
    person.x = x
    person.y = y
    person.child_x = x + box_width/2.
    person.child_y = y - box_height/2
    person.parent_y = y
    if person.gender == 'male':
        person.parent_x = x + box_width
    else:
        person.parent_x = x

    s = '\t<text \n\t style="font-size:12px;line-height:125%;fill:#000000;"\n'
    s += '\t\tx="{0}cm"\n'.format(x)
    s += '\t\ty="{0}cm">\n'.format(y)
    s += '\t\t<tspan x="={0}cm" y="{1}cm"> {2} </tspan>\n'.format(x, y-0.5, person.name)
    if person.born is not None and person.died is not None:
        s += '\t\t<tspan x="{0}cm" y="{1}cm" > {2} - {3}</tspan>\n'.format(x, y, person.born, person.died)
    elif person.born is not None or person.died is not None:
        if person.born is None:
            person.born = "?"
        if person.died is None:
            person.died = "?"
        s += '\t\t<tspan x="{0}cm" y="{1}cm" > {2} - {3}</tspan>\n'.format(x, y, person.born, person.died)
    if person.birth_place is not None or person.place is not None:
        if person.birth_place is not None:
            place = person.birth_place
        else:
            place = person.place
        s += '\t\t<tspan x="{0}cm" y="{1}cm" > {2} </tspan>\n'.format(x, y+0.5, place)
    if person.tagline is not None:
        s += '\t\t<tspan x="{0}cm" y="{1}cm" > {2} </tspan>\n'.format(x, y+1, person.tagline)
    s += '\t</text>\n'

    s += '\t<rect style="fill:none;stroke-width:1;stroke:#000000;"\n'
    s += '\t\twidth="{0}cm"\n'.format(box_width)
    s += '\t\theight="{0}cm"\n'.format(box_height)
    s += '\t\tx="{0}cm"\n'.format(x-0.1)
    s += '\t\ty="{0}cm" />\n'.format(y-box_height/2.)
    return s

def assign(person, idx):
    person.idx = idx
    if person.mother is not None:
        assign(person.mother, person.idx +'1')
    if person.father is not None:
        assign(person.father, person.idx + '0')

def write_output(fam, person):
    assign(person, '')
    person.gen = 0
    max_gen = 0
    subfam = [person]

    for ps in fam.itervalues():
        if ps.idx != '':
            print ps.idx, ps.name, int(ps.idx, 2)
            ps.gen = len(ps.idx)
            ps.col = int(ps.idx, 2)
            subfam.append(ps)
            if ps.gen > max_gen:
                max_gen = len(ps.idx)

    people_per_gen = {x:0 for x in range(max_gen + 1)}
    gen_ranks = {x:[] for x in range(max_gen+1)}
    for ps in subfam:
        people_per_gen[ps.gen] += 1
        gen_ranks[ps.gen].append(ps.col)

    for x in range(max_gen+1):
        gen_ranks[x].sort()

    height = (max_gen + 1)*row_spacing + 2*page_margin
    width = max(people_per_gen.values())*col_spacing + 2*page_margin

    s = '<svg\nwidth="{0}cm"\nheight="{1}cm"\nviewbox="0 0 {0} {1}">\n<g>\n'.format(width, height)

    for p in subfam:
        s += _person_text(p, width, height, people_per_gen, gen_ranks)

    for p in subfam:
        s += _birth_lines(p)

    s += "</g>\n</svg>"

    tempfile = "fam.svg"
    with open(tempfile, 'w') as f:
        f.write(s)
    system("inkscape {0} --export-pdf {1}".format(tempfile, "fam.pdf"))
