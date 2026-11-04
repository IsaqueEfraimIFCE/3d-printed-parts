# Parametric case: ESP32-C3 SuperMini + GY-521 (MPU-6050). Units: mm. Requires trimesh + manifold3d.
import trimesh
from trimesh.creation import box as _box, cylinder as _cyl

def box(x0,y0,z0,x1,y1,z1):
    b=_box(extents=[x1-x0,y1-y0,z1-z0]); b.apply_translation([(x0+x1)/2,(y0+y1)/2,(z0+z1)/2]); return b
def cyl(x,y,z0,z1,d,axis='z'):
    c=_cyl(radius=d/2,height=z1-z0,sections=48)
    if axis=='x': c.apply_transform(trimesh.transformations.rotation_matrix(1.5708,[0,1,0]))
    c.apply_translation([x,y,(z0+z1)/2] if axis=='z' else [(z0+z1)/2,x,y]); return c
U=lambda *m: trimesh.boolean.union(list(m),engine='manifold')
D=lambda a,*m: trimesh.boolean.difference([a,*m],engine='manifold')

L,W,H=60,32,16; WALL=2; FLOOR=2; POST=5; PILOT=1.8
# ---- base ----
base=D(box(0,0,0,L,W,H), box(WALL,WALL,FLOOR,L-WALL,W-WALL,H+1))
posts=[]
for (x,y) in [(WALL,WALL),(L-WALL-POST,WALL),(WALL,W-WALL-POST),(L-WALL-POST,W-WALL-POST)]:
    posts.append(D(box(x,y,FLOOR,x+POST,y+POST,H), cyl(x+POST/2,y+POST/2,FLOOR+2,H+1,PILOT)))
# ESP32-C3 SuperMini: board x 2..24.5, y 7..25, sits on 2 mm ledges, USB-C through -X wall
esp=[box(4,7,FLOOR,24.5,9,FLOOR+2), box(4,23,FLOOR,24.5,25,FLOOR+2),
     box(25,7,FLOOR,26.5,25,FLOOR+5)]            # rear fence
usb_z=FLOOR+2+1.0+1.6                               # ledge + PCB + half connector
usb=U(box(-1,16-4.5+1.6,usb_z-1.6,WALL+1,16+4.5-1.6,usb_z+1.6),
      cyl(16-4.5+1.6,usb_z,-1,WALL+1,3.2,'x'), cyl(16+4.5-1.6,usb_z,-1,WALL+1,3.2,'x'))
# GY-521: board x 34..55.2, y 8.2..23.8, 2x M2 bosses (holes 2.54 from +X edge, 15.24 apart), 4 mm standoff
mpu=[]
for y in (16-7.62,16+7.62):
    mpu.append(D(cyl(52.66,y,FLOOR,FLOOR+4,5), cyl(52.66,y,FLOOR+0.8,FLOOR+5,PILOT)))
mpu.append(box(34,10,FLOOR,36,22,FLOOR+4))           # support pad
base=D(U(base,*posts,*esp,*mpu), usb)
base.export('case_base.stl')
# ---- lid ----
LT=2; LIP=3; CL=0.25; LW=1.5
lid=box(0,0,0,L,W,LT)
lip=D(box(WALL+CL,WALL+CL,-LIP,L-WALL-CL,W-WALL-CL,0),
      box(WALL+CL+LW,WALL+CL+LW,-LIP-1,L-WALL-CL-LW,W-WALL-CL-LW,1))
cut=[box(x-0.3,y-0.3,-LIP-1,x+POST+0.3,y+POST+0.3,0) for (x,y) in
     [(WALL,WALL),(L-WALL-POST,WALL),(WALL,W-WALL-POST),(L-WALL-POST,W-WALL-POST)]]
lid=U(lid,D(lip,*cut))
holes=[]
for (x,y) in [(4.5,4.5),(L-4.5,4.5),(4.5,W-4.5),(L-4.5,W-4.5)]:
    holes+= [cyl(x,y,-1,LT+1,2.4), cyl(x,y,LT-1.2,LT+1,4.2)]   # M2 clearance + head recess
holes+= [cyl(8,11,-1,LT+1,3), cyl(8,21,-1,LT+1,3)]              # BOOT/RST pin-poke holes
holes+= [box(x,12,-1,x+1.2,20,LT+1) for x in (38,41,44,47)]      # vent slots
lid=D(lid,*holes)
lid.apply_transform(trimesh.transformations.rotation_matrix(3.14159,[1,0,0]))  # flip: print flat face down
lid.apply_translation([0,0,-lid.bounds[0][2]])
lid.export('case_lid.stl')
for n,m in [('base',base),('lid',lid)]:
    print(n,'watertight',m.is_watertight,'bounds',m.bounds.round(2).tolist(),'vol mm3',round(m.volume))
