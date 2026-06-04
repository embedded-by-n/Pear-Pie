// =============================================================================
// pear_pie_hub.scad  -  Pear Pie hub housing, clip-in module, and vacuum buck
// =============================================================================
// THREE parts in one file. Set PART below to choose which one renders:
//   "hub"    -> the main housing: off-centre screen window + side module slots
//   "module" -> a single clip-in module block (the magenta blocks in the concept)
//   "buck"   -> a vacuum-forming mould to make bulged clear screen covers
//
// HOW TO USE:
//   1. Install OpenSCAD (free): openscad.org
//   2. Open this file.
//   3. Set PART = "hub" / "module" / "buck" below.
//   4. F5 = quick preview, F6 = full render, then Export as STL to print.
//   5. Change any number at the top and it regenerates. It is all parametric.
//
// Units are millimetres.
// =============================================================================

PART = "buck";          // "hub", "module", or "buck"

$fn = 64;              // smoothness of curves (raise for final render, lower for speed)

// --- HUB BODY -----------------------------------------------------------------
BODY_W      = 230;     // overall width of the hub face
BODY_H      = 150;     // overall height of the hub face
BODY_D      = 45;      // depth (front to back)
WALL        = 3;       // wall thickness
CORNER_R    = 14;      // rounding of the body's vertical corners

// --- SCREEN WINDOW (deliberately off-centre, per your concept) ----------------
SCREEN_W       = 150;  // screen aperture width
SCREEN_H       = 95;   // screen aperture height
SCREEN_R       = 10;   // screen corner rounding
SCREEN_OFF_X   = -22;  // push LEFT (negative = left of centre)
SCREEN_OFF_Y   = -14;  // push DOWN (negative = below centre)
BEZEL_W        = 5;    // a shallow recessed bezel lip around the screen
BEZEL_DEPTH    = 1.5;  // how deep the bezel recess sits

// --- SIDE MODULE SLOTS (the clip-in points down the right edge) ---------------
MOD_COUNT      = 4;    // how many module slots
MOD_SLOT_H     = 22;   // each slot's height (along the body height)
MOD_SLOT_Z     = 26;   // each slot's size through the depth
MOD_SLOT_DEPTH = 12;   // how far each slot bites into the side wall
MOD_GAP        = 8;    // gap between slots

// --- VACUUM-FORMING BUCK (for bulged clear covers) ----------------------------
BUCK_W      = 150;     // cover footprint width  (match SCREEN_W-ish)
BUCK_H      = 95;      // cover footprint height
BUCK_R      = 12;      // footprint corner rounding
BULGE       = 20;      // how far the dome bulges out
DRAFT       = 0.86;    // top-vs-base scale (<1 = draft angle so it releases)
FLANGE_W    = 12;      // flat flange around the base (to seal + trim)
FLANGE_T    = 4;       // flange thickness
VENT_D      = 2;       // vent hole diameter (lets air be sucked out)

// =============================================================================
// helpers
// =============================================================================
module rrect(w, h, r) {
    // a 2D rounded rectangle, centred on the origin
    offset(r) square([w - 2*r, h - 2*r], center = true);
}

// =============================================================================
// PART: HUB HOUSING
// =============================================================================
module hub() {
    difference() {
        // outer body
        linear_extrude(BODY_D) rrect(BODY_W, BODY_H, CORNER_R);

        // hollow cavity, open at the BACK (front wall stays solid)
        translate([0, 0, WALL])
            linear_extrude(BODY_D)            // runs past the top = open back
                rrect(BODY_W - 2*WALL, BODY_H - 2*WALL, max(1, CORNER_R - WALL));

        // shallow recessed bezel on the very front face
        translate([SCREEN_OFF_X, SCREEN_OFF_Y, -0.01])
            linear_extrude(BEZEL_DEPTH)
                rrect(SCREEN_W + 2*BEZEL_W, SCREEN_H + 2*BEZEL_W, SCREEN_R + BEZEL_W);

        // the screen window, cut clean through the front wall
        translate([SCREEN_OFF_X, SCREEN_OFF_Y, -1])
            linear_extrude(WALL + 2)
                rrect(SCREEN_W, SCREEN_H, SCREEN_R);

        // side module slots down the RIGHT edge
        total = MOD_COUNT * MOD_SLOT_H + (MOD_COUNT - 1) * MOD_GAP;
        start_y = total/2 - MOD_SLOT_H/2;     // centre the column vertically
        for (i = [0 : MOD_COUNT - 1]) {
            y = start_y - i * (MOD_SLOT_H + MOD_GAP);
            translate([ BODY_W/2 - MOD_SLOT_DEPTH,
                        y - MOD_SLOT_H/2,
                        (BODY_D - MOD_SLOT_Z)/2 ])
                cube([MOD_SLOT_DEPTH + 1, MOD_SLOT_H, MOD_SLOT_Z]);
        }
    }
}

// =============================================================================
// PART: CLIP-IN MODULE (one block that slots into a side slot)
// =============================================================================
module module_block() {
    tab_d   = MOD_SLOT_DEPTH - 0.4;     // the bit that inserts (slight clearance)
    face_d  = 16;                       // how far the module body sticks out
    h       = MOD_SLOT_H - 0.6;
    z       = MOD_SLOT_Z - 0.6;

    // insert tab
    cube([tab_d, h, z]);
    // outer body (the visible block)
    translate([tab_d, -3, -3])
        minkowski() {
            cube([face_d, h + 6, z + 6]);
            sphere(2);                  // softens the outer edges
        }
}

// =============================================================================
// PART: VACUUM-FORMING BUCK (mould for bulged clear covers)
// =============================================================================
module buck() {
    union() {
        // flat flange at the base (seal + trim edge)
        linear_extrude(FLANGE_T)
            rrect(BUCK_W + 2*FLANGE_W, BUCK_H + 2*FLANGE_W, BUCK_R + FLANGE_W);

        difference() {
            // the bulged dome: a draughted footprint intersected with a dome
            intersection() {
                // footprint column with DRAFT (narrower at the top, so it releases)
                linear_extrude(height = BULGE + 2, scale = DRAFT)
                    rrect(BUCK_W, BUCK_H, BUCK_R);
                // smooth convex dome (a squashed sphere; we keep its top half)
                resize([BUCK_W, BUCK_H, BULGE * 2])
                    sphere(d = 100);
            }

            // vent holes (air gets sucked out through these during forming)
            for (vx = [-BUCK_W/2 + 12, 0, BUCK_W/2 - 12])
                for (vy = [-BUCK_H/2 + 12, BUCK_H/2 - 12])
                    translate([vx, vy, -1])
                        cylinder(d = VENT_D, h = BULGE + 4);
        }
    }
}

// =============================================================================
// render the chosen part
// =============================================================================
if (PART == "hub")    hub();
else if (PART == "module") module_block();
else if (PART == "buck")   buck();
