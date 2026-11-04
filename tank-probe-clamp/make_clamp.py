# Tank-wall C-clamp with reversible ultrasonic probe holder (JSN-SR04T / AJ-SR04M style probe).
# Units mm. Requires: pip install manifold3d trimesh numpy
import math, numpy as np, trimesh
from manifold3d import Manifold as M, CrossSection as CS

# ---------------- parameters ----------------
PROBE_D   = 18.4   # probe body hole (probe body ~18 mm)
PROBE_FL  = 23.0   # probe front flange diameter (just for reference / recess)
W         = 24     # frame thickness (Y)
T         = 10     # jaw / spine thickness
GAP       = 112    # jaw opening -> clear gap ~106 mm, fits walls ~60..105 mm
ARM       = 22     # arm reach past inner jaw
SCREW_D   = 16; PITCH = 3.0; DEPTH = 1.5; SCREW_L = 55; CLR = 0.4
TONGUE    = 12     # square tongue of the probe holder
PIN_D     = 3.4    # locking pin / M3 screw hole
SEG       = 96

def box(x0,y0,z0,x1,y1,z1): return M.cube([x1-x0,y1-y0,z1-z0]).translate([x0,y0,z0])
def cylz(r,h,seg=SEG): return M.cylinder(h,r,r,seg)
def cylx(r,x0,x1,y,z): return cylz(r,x1-x0).rotate([0,90,0]).translate([x0,y,z])

def thread(r_minor, depth, pitch, length, n=180):
    # single-start thread = extrude of eccentric profile with 360deg twist per pitch
    pts=[]
    for i in range(n):
        a=2*math.pi*i/n; f=i/n
        tri = 1-abs(2*f-1)                      # 0..1..0 over one turn -> V/trapezoid
        tri = min(1.0, tri*1.25)                # flatten crest a bit (trapezoidal)
        r=r_minor+depth*tri; pts.append((r*math.cos(a), r*math.sin(a)))
    turns=length/pitch
    return M.extrude(CS([pts]), length, int(turns*48), -360*turns)

def save(m,name):
    mesh=m.to_mesh(); t=trimesh.Trimesh(np.array(mesh.vert_properties)[:,:3], np.array(mesh.tri_verts))
    t.export(name); print(name,'watertight',t.is_watertight,'size',(t.bounds[1]-t.bounds[0]).round(1).tolist(),'vol',round(t.volume))

# ---------------- frame (XZ profile, Y = width) ----------------
TOP=70; SZ=40                                  # spine top, screw height
xo0,xo1 = 0,T                                  # outer jaw
xi0,xi1 = T+GAP, T+GAP+T                       # inner jaw
xa1 = xi1+ARM                                  # arm tip
frame = (box(xo0,0,0, xo1,W,TOP) +             # outer jaw (full height)
         box(xo0,0,TOP-T, xa1,W,TOP) +          # spine + arm
         box(xi0,0,20, xi1,W,TOP) +             # inner jaw
         box(xi0-6,0,20, xi0,W,62))             # inner pad (flat face against wall)
frame = frame + (cylx(14, -8, xo1, W/2, SZ) ^ box(-9,0,0, xo1,W,TOP))   # thread boss, trimmed flush
# fillets / gussets
frame = frame + box(xo1,0,TOP-T-6, xo1+6,W,TOP-T) + box(xi1,0,TOP-T-6, xi1+6,W,TOP-T)
# internal thread
nut = thread(SCREW_D/2-DEPTH+CLR, DEPTH, PITCH, T+8+2).rotate([0,90,0]).translate([-9,W/2,SZ])
frame = frame - nut - cylx(SCREW_D/2-DEPTH+CLR, -9, xo1+1, W/2, SZ)
# square socket at arm tip for holder tongue + vertical pin
sock_z = TOP-T/2
frame = frame + box(xa1,0,TOP-T-4, xa1+16,W,TOP+4)          # socket block
frame = frame - box(xa1+1,W/2-TONGUE/2-0.2,sock_z-TONGUE/2-0.2, xa1+17,W/2+TONGUE/2+0.2,sock_z+TONGUE/2+0.2)
frame = frame - cylz(PIN_D/2,40).translate([xa1+9,W/2,TOP-30])
save(frame,'clamp_frame.stl')

# ---------------- probe holder (symmetric about its mid-plane -> flip 180 deg) ----------------
HB=30; HH=22                                   # holder block, height
hx0=0
holder = box(0,-HB/2,-HH/2, HB,HB/2,HH/2) + box(-15,-TONGUE/2,-TONGUE/2, 1,TONGUE/2,TONGUE/2)
holder = holder - cylz(PROBE_D/2,HH+2).translate([HB/2,0,-HH/2-1])
holder = holder - cylz(PIN_D/2,40).translate([-15+9-1,0,-20])       # pin through tongue (matches socket pin at +9 from tip, tongue starts at tip+1)
# M3 set-screw / pinch hole into probe bore (sideways)
holder = holder - cylx(1.4, HB/2, HB+1, 0, 0)
save(holder,'probe_holder.stl')

# ---------------- screw ----------------
core_r = SCREW_D/2-DEPTH
screw = thread(core_r, DEPTH, PITCH, SCREW_L) + cylz(core_r+0.01, SCREW_L)
knob_pts=[((17 if i%2==0 else 15.5)*math.cos(2*math.pi*i/36),(17 if i%2==0 else 15.5)*math.sin(2*math.pi*i/36)) for i in range(36)]
knob = CS([knob_pts]).extrude(12).translate([0,0,-12])
tip = M.cylinder(4, core_r, core_r-2, SEG).translate([0,0,SCREW_L])
screw = (knob + screw + tip).translate([0,0,12])
save(screw,'clamp_screw.stl')

# ---------------- pin ----------------
pin = cylz(1.55,16) + M.cylinder(2.5,3.5,3.5,SEG).translate([0,0,16])
save(pin,'lock_pin.stl')

# lay frame on its side for printing (flat face on bed)
f=trimesh.load('clamp_frame.stl'); f.apply_transform(trimesh.transformations.rotation_matrix(-math.pi/2,[1,0,0])); f.apply_translation(-f.bounds[0]); f.export('clamp_frame.stl')
