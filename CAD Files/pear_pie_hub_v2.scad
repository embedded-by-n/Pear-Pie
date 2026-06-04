// =============================================================================
// pear_pie_hub.scad  -  Pear Pie hub housing, clip-in module, cap, vacuum buck
// =============================================================================
// Set PART to choose what renders:
//   "hub"        -> housing: off-centre RECTANGULAR screen + side module bays
//   "module"     -> a hollow clip-in module (magnetic mount, cable hole, open top)
//   "module_cap" -> the press-on lid for a module
//   "buck"       -> vacuum-forming mould for a RECTANGULAR bulged screen cover
//
// USE: install OpenSCAD (openscad.org), open file, set PART, F5 preview / F6
// render, Export as STL. All dimensions are variables below - change and re-render.
// Units: millimetres.
//
// MOUNTING: modules mount MAGNETICALLY (magnet pockets in both module + hub bay).
// COMMS: modules talk to the hub over BLE (no electrical pins to align).
// The full wired SPI bus is documented as the architecture; demo modules use
// magnetic-mount + BLE, which is simpler and matches the wireless mesh design.
// =============================================================================

PART = "hub";          // "hub", "module", "module_cap", or "buck"
$fn  = 64;

// --- HUB BODY -----------------------------------------------------------------
BODY_W   = 230;  BODY_H = 150;  BODY_D = 45;  WALL = 3;  CORNER_R = 14;

// --- SCREEN WINDOW (off-centre, RECTANGULAR to match the Inky content) --------
SCREEN_W = 150;  SCREEN_H = 95;  SCREEN_R = 8;
SCREEN_OFF_X = -22;   // left
SCREEN_OFF_Y = -14;   // down
BEZEL_W = 5;  BEZEL_DEPTH = 1.5;

// --- MODULE BAYS (clip-in points down the right edge) -------------------------
MOD_COUNT = 4;  MOD_SLOT_H = 24;  MOD_SLOT_Z = 28;  MOD_SLOT_DEPTH = 14;  MOD_GAP = 8;

// --- MAGNETS (small disc magnets in module + matching hub pockets) ------------
MAG_D = 6;   MAG_T = 2.5;        // 6mm dia x 2.5mm magnets (common)

// --- MODULE INTERNALS ---------------------------------------------------------
MOD_FACE_OUT = 18;               // how far the module body sticks out from the hub
MOD_WALL     = 2;                // module shell wall
PWR_LEAD_D   = 7;                // power lead hole in the module (rear)

// --- VACUUM BUCK (rectangular bulged cover to match the screen) ---------------
BUCK_W = 150;  BUCK_H = 95;  BUCK_R = 8;   // match the screen window
BULGE  = 18;   DRAFT = 0.88;   FLANGE_W = 12;  FLANGE_T = 4;  VENT_D = 2;

// --- POWER LEAD HOLES ---------------------------------------------------------
PWR_D        = 9;                // main power lead hole (e.g. USB-C / barrel)
PWR_BAY_D    = 6;                // smaller power feed into each module bay

// =============================================================================
module rrect(w, h, r) { offset(r) square([w - 2*r, h - 2*r], center = true); }

// magnet pockets, two per bay/module, placed in the mating face (in Y/Z plane)
module mag_pockets_in_x_face(face_x, depth_dir) {
    // two magnets spaced in Z, centred in the bay height
    for (dz = [-MOD_SLOT_Z/4, MOD_SLOT_Z/4])
        translate([face_x, 0, dz])
            rotate([0, 90 * depth_dir, 0])
                cylinder(d = MAG_D, h = MAG_T + 0.5);
}

// =============================================================================
// HUB HOUSING
// =============================================================================
module hub() {
    total  = MOD_COUNT * MOD_SLOT_H + (MOD_COUNT - 1) * MOD_GAP;
    start_y = total/2 - MOD_SLOT_H/2;
    difference() {
        linear_extrude(BODY_D) rrect(BODY_W, BODY_H, CORNER_R);

        // hollow, open back
        translate([0, 0, WALL])
            linear_extrude(BODY_D)
                rrect(BODY_W - 2*WALL, BODY_H - 2*WALL, max(1, CORNER_R - WALL));

        // recessed bezel
        translate([SCREEN_OFF_X, SCREEN_OFF_Y, -0.01])
            linear_extrude(BEZEL_DEPTH)
                rrect(SCREEN_W + 2*BEZEL_W, SCREEN_H + 2*BEZEL_W, SCREEN_R + BEZEL_W);

        // screen window through the front wall
        translate([SCREEN_OFF_X, SCREEN_OFF_Y, -1])
            linear_extrude(WALL + 2) rrect(SCREEN_W, SCREEN_H, SCREEN_R);

        // module bays + magnet pockets in each bay floor
        for (i = [0 : MOD_COUNT - 1]) {
            y = start_y - i * (MOD_SLOT_H + MOD_GAP);
            // the bay opening
            translate([BODY_W/2 - MOD_SLOT_DEPTH, y - MOD_SLOT_H/2, (BODY_D - MOD_SLOT_Z)/2])
                cube([MOD_SLOT_DEPTH + 1, MOD_SLOT_H, MOD_SLOT_Z]);
            // magnet pockets in the inner wall of the bay (module pulls against these)
            translate([0, y, BODY_D/2])
                for (dz = [-MOD_SLOT_Z/4, MOD_SLOT_Z/4])
                    translate([BODY_W/2 - MOD_SLOT_DEPTH - MAG_T, 0, dz])
                        rotate([0, 90, 0]) cylinder(d = MAG_D, h = MAG_T + 0.5);
            // power feed hole from inside the hub into this bay
            translate([BODY_W/2 - MOD_SLOT_DEPTH - WALL - 1, y, BODY_D/2])
                rotate([0, 90, 0]) cylinder(d = PWR_BAY_D, h = WALL + 2);
        }

        // main power lead hole in the hub body (back-left, for the Pi supply)
        translate([-BODY_W/2 - 1, -BODY_H/2 + 25, BODY_D/2])
            rotate([0, 90, 0]) cylinder(d = PWR_D, h = WALL + 2);
    }
}

// =============================================================================
// CLIP-IN MODULE  (hollow, magnetic mount, cable hole, open top for the cap)
// =============================================================================
module module_block() {
    tab_d = MOD_SLOT_DEPTH - 0.5;     // insert tab (clearance)
    w     = MOD_FACE_OUT + tab_d;     // total depth (into hub + sticking out)
    h     = MOD_SLOT_H - 0.8;
    z     = MOD_SLOT_Z - 0.8;

    difference() {
        // outer shell
        translate([0, -h/2, -z/2])
            minkowski() { cube([w, h, z]); sphere(1.2); }

        // hollow cavity (open at the TOP, +Y, for the cap)
        translate([MOD_WALL, -h/2 + MOD_WALL, -z/2 + MOD_WALL])
            cube([w - 2*MOD_WALL, h, z - 2*MOD_WALL]);   // runs out the top = open

        // magnet pockets in the insert face (meets the hub bay)
        for (dz = [-z/4, z/4])
            translate([-0.5, 0, dz]) rotate([0, 90, 0]) cylinder(d = MAG_D, h = MAG_T + 0.5);

        // power lead hole out the back of the module
        translate([w - MOD_WALL - 1, 0, 0]) rotate([0, 90, 0]) cylinder(d = PWR_LEAD_D, h = MOD_WALL + 2);
    }
}

// =============================================================================
// MODULE CAP  (press-on lid for the module's open top)
// =============================================================================
module module_cap() {
    tab_d = MOD_SLOT_DEPTH - 0.5;
    w     = MOD_FACE_OUT + tab_d;
    z     = MOD_SLOT_Z - 0.8;
    lip   = 2;
    // flat lid + a small inner lip that presses into the cavity
    union() {
        translate([0, 0, -z/2]) cube([w, 1.6, z]);                       // lid plate
        translate([MOD_WALL + 0.3, -lip, -z/2 + MOD_WALL + 0.3])
            cube([w - 2*MOD_WALL - 0.6, lip, z - 2*MOD_WALL - 0.6]);     // press lip
    }
}

// =============================================================================
// VACUUM BUCK  (rectangular bulged cover, draft + radii + vents)
// =============================================================================
module buck() {
    LAYERS = 40;                       // smoothness of the pillow bulge
    union() {
        // flat flange to seal + trim against
        linear_extrude(FLANGE_T)
            rrect(BUCK_W + 2*FLANGE_W, BUCK_H + 2*FLANGE_W, BUCK_R + FLANGE_W);

        difference() {
            // RECTANGULAR pillow bulge: stack shrinking rounded-rects up a sine
            // curve, so the dome keeps its rectangular shape (not a round hump)
            translate([0, 0, FLANGE_T - 0.01])
                for (i = [0 : LAYERS - 1]) {
                    f0 = i / LAYERS;
                    f1 = (i + 1) / LAYERS;
                    z0 = BULGE * sin(f0 * 90);    // sine profile = soft rounded top
                    z1 = BULGE * sin(f1 * 90);
                    s0 = 1 - (1 - DRAFT) * f0;     // shrink toward top = draft
                    s1 = 1 - (1 - DRAFT) * f1;
                    translate([0, 0, z0])
                        linear_extrude(height = max(z1 - z0, 0.01), scale = s1 / s0)
                            rrect(BUCK_W * s0, BUCK_H * s0, BUCK_R * s0);
                }

            // vent holes through the dome (air pulled out during forming)
            for (vx = [-BUCK_W/2 + 12, 0, BUCK_W/2 - 12])
                for (vy = [-BUCK_H/2 + 12, BUCK_H/2 - 12])
                    translate([vx, vy, -1]) cylinder(d = VENT_D, h = BULGE + FLANGE_T + 4);
        }
    }
}

// =============================================================================
if (PART == "hub")             hub();
else if (PART == "module")     module_block();
else if (PART == "module_cap") module_cap();
else if (PART == "buck")       buck();
