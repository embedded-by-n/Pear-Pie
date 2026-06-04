// =============================================================================
// pear_pie_hub_round.scad  -  Videosphere-style Pear Pie hub (Prusa-printable)
// =============================================================================
// One rounded ORB: a squashed-sphere base bowl + a tall rounded clear dome that
// meet flush at the rim (Videosphere look). Inside the bowl is a real MOUNTING
// DECK that the 5" LCD, the round SPI module-pods, and the switches mount onto.
// The screen sits deep on the deck so the round wall never clips its corners.
//
// PART:
//   "assembly"    -> EVERYTHING: bowl + deck + LCD + module-pods + switches +
//                    dome ring + clear dome ghost. START HERE.
//   "base"        -> bowl + internal mounting deck (LCD seat, SPI bays, switches)
//   "dome_ring"   -> thin rim ring that holds the clear dome (+ catch magnet)
//   "dome_buck"   -> vacuum-forming mould for the tall rounded clear dome
//   "module_pod"  -> a circular SPI clip-in pod (drops into a bay)
//   "module_dome" -> little clear dome buck for a module pod
//   "hinge" / "hinge_pin"
//
// USE: OpenSCAD. Set PART, F5 / F6, Export STL. Units mm.
// =============================================================================

PART = "assembly";
$fn  = 80;

// --- ORB FORM (printable; squashed sphere) ------------------------------------
ORB_DIA = 190;     // max diameter (prints in one piece on MK3/MK4)
ORB_H   = 150;     // total orb height (squashed sphere = rounded but not too tall)
WALL    = 3;
SPLIT_Z = 96;      // where the base bowl ends and the clear dome begins (the rim)
DECK_Z  = 58;      // height of the internal mounting deck
DECK_T  = 4;       // deck thickness

ORB_CZ = ORB_H/2;  // orb centre height
A = ORB_DIA/2;  C = ORB_H/2;

// --- 5" LCD (mounts on the deck, faces up through the dome) -------------------
SCREEN_W = 121;  SCREEN_H = 76;  SCREEN_R = 6;
SCREEN_OFF_X = 0;  SCREEN_OFF_Y = 18;  SCREEN_RECESS = 4;

// --- ROUND SPI MODULE BAYS (in the deck, below the screen) --------------------
BAY_COUNT = 2;  BAY_DIA = 32;  BAY_DEPTH = 16;  BAY_GAP = 18;  BAY_Y = -40;
CONTACT_RING_D = 22;  CONTACT_RING_W = 2;

// --- MANUAL SWITCHES ----------------------------------------------------------
SW_D = 9;  SW_X = 64;  SW_Y = -36;

// --- MAGNETS / POWER ----------------------------------------------------------
MAG_D = 6;  MAG_T = 2.5;  PWR_D = 9;  PWR_BAY_D = 5;

// --- DOME RING + BUCK ---------------------------------------------------------
FLANGE_W = 12;  FLANGE_T = 4;  VENT_D = 2;  RING_H = 7;

// --- MODULE POD ---------------------------------------------------------------
POD_DIA = BAY_DIA - 1.0;  POD_H = BAY_DEPTH + 8;  POD_WALL = 2;  POD_DOME_RISE = 8;

// --- HINGE --------------------------------------------------------------------
HG_LEAF_L = 24;  HG_LEAF_W = 16;  HG_T = 3;  HG_KN_D = 7;  PIN_D = 2.6;  SCREW_D = 3;

// =============================================================================
function rim_r(z) = A * sqrt(max(1 - pow((z - ORB_CZ)/C, 2), 0));   // orb radius at height z
module rrect(w,h,r) { offset(r) square([w-2*r, h-2*r], center=true); }
function bay_xs() = [ for (i=[0:BAY_COUNT-1]) -((BAY_COUNT-1)*(BAY_DIA+BAY_GAP))/2 + i*(BAY_DIA+BAY_GAP) ];

module orb_outer() { translate([0,0,ORB_CZ]) resize([ORB_DIA, ORB_DIA, ORB_H]) sphere(d=100); }
module orb_inner() { translate([0,0,ORB_CZ]) resize([ORB_DIA-2*WALL, ORB_DIA-2*WALL, ORB_H-2*WALL]) sphere(d=100); }
module slab(z0, z1) { translate([-150,-150,z0]) cube([300,300,z1-z0]); }
module ring_recess(d, w, h) { difference() { cylinder(d=d, h=h); cylinder(d=d-2*w, h=h+1); } }

// =============================================================================
// BASE: orb bowl + internal mounting deck
// =============================================================================
module base() {
    difference() {
        union() {
            // bowl shell (lower orb), open at the top rim
            difference() {
                intersection() { orb_outer(); slab(0, SPLIT_Z); }
                intersection() { orb_inner(); slab(WALL, SPLIT_Z + 1); }
            }
            // the MOUNTING DECK: a solid plate filling the interior at DECK_Z
            intersection() { orb_inner(); slab(DECK_Z, DECK_Z + DECK_T); }
        }
        // --- everything below is cut into the deck top ---
        // LCD seat
        translate([SCREEN_OFF_X, SCREEN_OFF_Y, DECK_Z + DECK_T - SCREEN_RECESS])
            linear_extrude(SCREEN_RECESS + 1) rrect(SCREEN_W, SCREEN_H, SCREEN_R);
        // round SPI bays: bay + retention magnet + ring-contact recess + feed
        for (bx = bay_xs()) {
            translate([bx, BAY_Y, DECK_Z + DECK_T - BAY_DEPTH]) cylinder(d = BAY_DIA, h = BAY_DEPTH + 1);
            translate([bx, BAY_Y, DECK_Z + DECK_T - BAY_DEPTH - MAG_T]) cylinder(d = MAG_D, h = MAG_T + 0.5);
            translate([bx, BAY_Y, DECK_Z + DECK_T - BAY_DEPTH - 0.01]) ring_recess(CONTACT_RING_D, CONTACT_RING_W, 1.2);
            translate([bx, BAY_Y, DECK_Z - 1]) cylinder(d = PWR_BAY_D, h = DECK_T + 2);
        }
        // manual switches
        for (sx = [-SW_X, SW_X]) translate([sx, SW_Y, DECK_Z + DECK_T - 1]) cylinder(d = SW_D, h = DECK_T + 2);
        // main power hole through the bowl side near the bottom
        translate([-A - 6, 0, 30]) rotate([0,90,0]) cylinder(d = PWR_D, h = 24);
        // catch magnet pocket on the -Y rim
        translate([0, -(rim_r(SPLIT_Z - 8) - MAG_T), SPLIT_Z - 8]) rotate([-90,0,0]) cylinder(d = MAG_D, h = MAG_T + 0.5);
    }
}

// =============================================================================
// DOME RING: thin rim ring holding the clear dome (+ catch magnet); flush
// =============================================================================
module dome_ring() {
    rr = rim_r(SPLIT_Z);
    difference() {
        union() {
            difference() { cylinder(r = rr, h = RING_H); translate([0,0,-1]) cylinder(r = rr - 6, h = RING_H + 2); }
            translate([0, -(rr - 3), 0]) cylinder(d = MAG_D + 5, h = RING_H);
        }
        translate([0, -(rr - 3), -0.01]) cylinder(d = MAG_D, h = MAG_T + 0.5);
    }
}

// =============================================================================
// DOME BUCK: tall rounded clear dome (the upper orb), for vacuum forming
// =============================================================================
module dome_buck() {
    rr = rim_r(SPLIT_Z);
    rise = ORB_H - SPLIT_Z;
    union() {
        linear_extrude(FLANGE_T) circle(r = rr + FLANGE_W);
        difference() {
            translate([0,0,FLANGE_T - SPLIT_Z]) intersection() { orb_outer(); slab(SPLIT_Z, ORB_H + 1); }
            for (a=[0:60:359]) translate([cos(a)*(rr-14), sin(a)*(rr-14), -1]) cylinder(d=VENT_D, h=rise+FLANGE_T+4);
        }
    }
}

// =============================================================================
// CIRCULAR MODULE POD
// =============================================================================
module module_pod() {
    difference() {
        union() {
            cylinder(d = POD_DIA, h = POD_H - POD_DOME_RISE);
            translate([0,0,POD_H - POD_DOME_RISE])
                intersection() {
                    translate([0,0, POD_DOME_RISE - (pow(POD_DIA/2,2)+pow(POD_DOME_RISE,2))/(2*POD_DOME_RISE)])
                        sphere(r = (pow(POD_DIA/2,2)+pow(POD_DOME_RISE,2))/(2*POD_DOME_RISE));
                    cylinder(d = POD_DIA + 1, h = POD_DOME_RISE + 1);
                }
        }
        translate([0,0,POD_WALL]) cylinder(d = POD_DIA - 2*POD_WALL, h = POD_H);
        translate([0,0,-0.01]) cylinder(d = MAG_D, h = MAG_T + 0.5);
        translate([0,0,-0.01]) ring_recess(CONTACT_RING_D, CONTACT_RING_W, 1.2);
    }
}
module module_dome() {
    union() {
        linear_extrude(2) circle(r = POD_DIA/2 + 6);
        translate([0,0,2]) intersection() {
            translate([0,0, POD_DOME_RISE - (pow(POD_DIA/2,2)+pow(POD_DOME_RISE,2))/(2*POD_DOME_RISE)])
                sphere(r = (pow(POD_DIA/2,2)+pow(POD_DOME_RISE,2))/(2*POD_DOME_RISE));
            cylinder(d = POD_DIA + 1, h = POD_DOME_RISE + 1);
        }
    }
}

// =============================================================================
// HINGE
// =============================================================================
module hinge() {
    difference() {
        union() {
            translate([0,-HG_LEAF_W,0]) cube([HG_LEAF_L,HG_LEAF_W,HG_T]);
            cube([HG_LEAF_L,HG_LEAF_W,HG_T]);
            for (kx=[0,HG_LEAF_L*2/3]) translate([kx,0,HG_KN_D/2]) rotate([0,90,0]) cylinder(d=HG_KN_D,h=HG_LEAF_L/3);
            translate([HG_LEAF_L/3,0,HG_KN_D/2]) rotate([0,90,0]) cylinder(d=HG_KN_D,h=HG_LEAF_L/3);
        }
        translate([-2,0,HG_KN_D/2]) rotate([0,90,0]) cylinder(d=PIN_D,h=HG_LEAF_L+4);
        for (sx=[HG_LEAF_L*0.35,HG_LEAF_L*0.75]) for (sy=[-HG_LEAF_W*0.55,HG_LEAF_W*0.55]) translate([sx,sy,-1]) cylinder(d=SCREW_D,h=HG_T+2);
    }
}
module hinge_pin() { cylinder(d = PIN_D - 0.2, h = HG_LEAF_L); }

// =============================================================================
// ASSEMBLY
// =============================================================================
module assembly() {
    color("#FFF3D6") base();
    color("#1C5C5A") translate([SCREEN_OFF_X, SCREEN_OFF_Y, DECK_Z + DECK_T - SCREEN_RECESS + 0.5])
        linear_extrude(SCREEN_RECESS) rrect(SCREEN_W, SCREEN_H, SCREEN_R);
    for (bx = bay_xs()) color("#E91FEC") translate([bx, BAY_Y, DECK_Z + DECK_T - BAY_DEPTH + 0.5]) module_pod();
    for (sx = [-SW_X, SW_X]) color("#C8F02C") translate([sx, SW_Y, DECK_Z + DECK_T - 1]) cylinder(d = SW_D - 2, h = 4);
    color("#FFD24A") translate([0,0,SPLIT_Z]) dome_ring();
    color([0.18,0.77,0.95,0.20]) intersection() { orb_outer(); slab(SPLIT_Z, ORB_H + 1); }
}

// =============================================================================
if (PART == "assembly")         assembly();
else if (PART == "base")        base();
else if (PART == "dome_ring")   dome_ring();
else if (PART == "dome_buck")   dome_buck();
else if (PART == "module_pod")  module_pod();
else if (PART == "module_dome") module_dome();
else if (PART == "hinge")       hinge();
else if (PART == "hinge_pin")   hinge_pin();
