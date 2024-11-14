from collections import namedtuple

sputnik = namedtuple('sputnik', ['name', 'area', 'radius', 'gravity'])

phobos = sputnik(name='Phobos', area=1548.3, radius=11.26, gravity=0.0057)
deimos = sputnik(name='Deimos', area=495.15, radius=6.2, gravity=0.003)
print(phobos)
print(deimos)
# MarsSputnik(name='Phobos', area=1548.3, radius=11.26, gravity=0.0057)
# MarsSputnik(name='Deimos', area=495.15, radius=6.2, gravity=0.003)
print(phobos.area)
