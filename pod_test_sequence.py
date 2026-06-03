# =============================================================================
# pod_selftest.py  (POD)  -  run this when commissioning each new pod.
#
# Walks through every subsystem in order and tells you PASS / CHECK for each,
# so you know a pod is good before you deploy it. Run it in Thonny on the Pico
# and follow the on-screen prompts.
#
# Tests, in order:
#   0. Files + config   (is POD_ID set for THIS pod?)
#   1. LEDs             (blue sweep -> purple -> off)
#   2. Radar            (presence + distance, walk-away)
#   3. BLE broadcast    (does gossip send without error?)
#   4. Listener         (does the rule/neighbour scanner start?)
# =============================================================================

import time


def line():
    print("-" * 46)

def countdown(secs):
    for s in range(secs, 0, -1):
        print("   ...", s)
        time.sleep(1)


print("=" * 46)
print("POD SELF-TEST  -  commissioning check")
print("=" * 46)

# -----------------------------------------------------------------------------
# 0. Files + config
# -----------------------------------------------------------------------------
line()
print("[0] FILES + CONFIG")
ok_imports = True
try:
    import config
    print("    POD_ID =", config.POD_ID, " <-- confirm this is right for THIS pod")
    print("    ALPHA =", config.ALPHA, " THRESHOLD =", config.THRESHOLD)
except Exception as e:
    print("    CONFIG FAIL:", e); ok_imports = False

for mod in ("led", "sensors", "gossip", "baseline",
            "rule_listener", "neighbours", "uplink_packet", "downlink_packet"):
    try:
        __import__(mod)
        print("    import", mod, "... ok")
    except Exception as e:
        print("    import", mod, "... FAIL:", e); ok_imports = False

print("    RESULT:", "PASS" if ok_imports else "FAIL - fix imports before continuing")
time.sleep(1)

# -----------------------------------------------------------------------------
# 1. LEDs
# -----------------------------------------------------------------------------
line()
print("[1] LED TEST - watch the strip")
try:
    import led
    print("    blue arrival sweep...")
    led.arrival_sweep()
    time.sleep(0.5)
    print("    solid purple (2s)...")
    led.set_trail(1.0); time.sleep(2)
    print("    off.")
    led.clear()
    print("    RESULT: PASS if you saw blue -> purple -> off")
except Exception as e:
    print("    LED FAIL:", e)
time.sleep(1)

# -----------------------------------------------------------------------------
# 2. Radar
# -----------------------------------------------------------------------------
line()
print("[2] RADAR TEST - 10 seconds")
print("    STAND CLOSE for 5s, then STEP BACK past 2m for 5s.")
try:
    import sensors
    sensors.begin()
    countdown(3)
    saw_present = False
    saw_absent = False
    saw_distance = False
    for i in range(20):
        p = sensors.read_presence()
        d = sensors.last_distance_cm
        if p == 1: saw_present = True
        if p == 0: saw_absent = True
        if d is not None: saw_distance = True
        print("    present:", p, " distance_cm:", d)
        time.sleep(0.5)
    print("    saw presence:", saw_present,
          " saw absence:", saw_absent,
          " saw distance:", saw_distance)
    if saw_present and saw_absent and saw_distance:
        print("    RESULT: PASS - radar reads presence + distance + gating")
    else:
        print("    RESULT: CHECK - did you move close then far? distances showing?")
except Exception as e:
    print("    RADAR FAIL:", e)
time.sleep(1)

# -----------------------------------------------------------------------------
# 3. BLE broadcast
# -----------------------------------------------------------------------------
line()
print("[3] BLE BROADCAST TEST")
try:
    import gossip
    import config
    gossip.broadcast(config.POD_ID, 1, 0)
    print("    broadcast sent ok (pod", config.POD_ID, "state present)")
    print("    RESULT: PASS - pod can advertise. (Check the hub logger sees it.)")
except Exception as e:
    print("    BLE BROADCAST FAIL:", e)
time.sleep(1)

# -----------------------------------------------------------------------------
# 4. Listener (rule updates + neighbours)
# -----------------------------------------------------------------------------
line()
print("[4] LISTENER TEST")
try:
    import rule_listener
    from baseline import AdaptiveBaseline
    import config
    learner = AdaptiveBaseline(config.ALPHA)
    rule_listener.start(learner)
    print("    scanner started ok (listening for hub updates + neighbour pods)")
    time.sleep(2)
    rule_listener.stop()
    print("    RESULT: PASS - listener starts and stops cleanly")
except Exception as e:
    print("    LISTENER FAIL:", e)

# -----------------------------------------------------------------------------
print("=" * 46)
print("SELF-TEST DONE.")
print("If all PASS, this pod is ready to deploy.")
print("Remember: POD_ID printed in [0] must be UNIQUE per pod.")
print("=" * 46)
