from pathlib import Path
import json
import cadquery as cq

OUT = Path('tmp/kokoshield/package/CAD')
OUT.mkdir(parents=True, exist_ok=True)

def rounded_box(w, d, h, r, x=0, y=0, z=0):
    return cq.Workplane('XY').box(w, d, h, centered=(True, True, False)).edges('|Z').fillet(r).translate((x,y,z))

def cyl(r,h,x,y,z):
    return cq.Workplane('XY').circle(r).extrude(h).translate((x,y,z))

points = [(x,y) for x in (-34,34) for y in (-23,23)]
body = rounded_box(86,62,32,5).cut(rounded_box(81.2,57.2,32,3,0,0,2.8))
for x,y in points:
    body = body.union(cyl(4.5,28.4,x,y,2.5)).cut(cyl(1.15,14,x,y,18))
for x in (-19,19):
    tab = rounded_box(15,13,3.4,2.5,x,34.3,0).cut(cyl(2.1,4,x,37,0))
    body = body.union(tab)
port = rounded_box(12,8,7,1.5,-12,-31,6)
body = body.cut(port)
body = body.cut(cq.Workplane('XY').box(7,6,7,centered=(True,True,False)).translate((42,0,7)))

lid = rounded_box(86,62,3.2,5,0,0,32)
for x,y in points:
    lid = lid.cut(cyl(1.40,4,x,y,31.8))

# External ventilated hood with top roof, two separate sets of slots, and an open bottom.
hood = rounded_box(30,30,31,3,60,0,1).cut(rounded_box(25.2,25.2,31,2,60,0,-1.4))
for z in (7,13,19,25):
    for y in (-14.5,14.5):
        hood=hood.cut(cq.Workplane('XY').box(19,7,2.4).translate((60,y,z)))
    hood=hood.cut(cq.Workplane('XY').box(7,17,2.4).translate((74.5,0,z)))
hood=hood.cut(cq.Workplane('XY').box(8,7,7,centered=(True,True,False)).translate((45,0,7)))
for y in (-10,10):
    ear=rounded_box(12,8,3.5,2.00,49,y,1.0).cut(cyl(1.55,4,46,y,0.8))
    hood=hood.union(ear)

# Simplified size envelopes for the demonstration, as separate visual parts.
board=rounded_box(43,23,1.6,1.5,-5,-1,7.3)
chip=rounded_box(14,11,2.0,1.2,-2,0,8.9)
board=board.union(chip)
sensor=rounded_box(17,12,1.6,1.0,60,0,11)
sensor=sensor.union(rounded_box(5,5,1.0,.5,60,0,12.6))

parts = [
    ('Enclosure_Base', body, (0.10,0.29,0.22), (0,0,0)),
    ('Enclosure_Lid', lid, (0.71,0.77,0.48), (0,0,32)),
    ('Ventilated_Sensor_Hood', hood, (0.79,0.62,0.28), (17,0,8)),
    ('Controller_Size_Envelope', board, (0.20,0.52,0.40), (0,0,10)),
    ('Sensor_Size_Envelope', sensor, (0.18,0.58,0.60), (17,0,1)),
]
asm=cq.Assembly(name='KokoShield_Field_Node')
browser_parts=[]
for idx,(name,shape,rgb,explode) in enumerate(parts):
    val=shape.val()
    assert val.isValid() and len(shape.solids().vals())==1, (name, len(shape.solids().vals()))
    asm.add(shape,name=name,color=cq.Color(*rgb))
    if idx<3:
        # Exports sit flat on their lower face for inspection or slicing.
        on_bed=shape.translate((0,0,-val.BoundingBox().zmin))
        cq.exporters.export(on_bed, str(OUT/f'{name}.stl'), tolerance=0.06, angularTolerance=0.22)
    vertices, triangles=val.tessellate(0.34,0.25)
    browserv=[]; remap={}; indices={}
    for i,v in enumerate(vertices):
        key=tuple(round(x,2) for x in v.toTuple())
        if key not in indices:
            indices[key]=len(browserv); browserv.append(key)
        remap[i]=indices[key]
    tris=[[remap[j] for j in t] for t in triangles]
    tris=[t for t in tris if len(set(t))==3]
    browser_parts.append(dict(name=name,vertex=browserv,face=tris,color=rgb,explode=explode))
    bounds=val.BoundingBox()
    print(name, round(bounds.xlen,1),round(bounds.ylen,1),round(bounds.zlen,1),len(tris))
asm.save(str(OUT/'KokoShield_Field_Node.step'))
Path('tmp/kokoshield/assets/mesh.json').write_text(json.dumps(browser_parts,separators=(',',':')))
