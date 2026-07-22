# Pear-Pie Cyber-Physical Home System

## Final Maker Project — CYBN8001 Building Cyber-Physical Systems
## Master of Applied Cybernetics, Australian National University, 2026 Cohort

_'In theory there is no difference between theory and practice. 
In practice, there is.'_\
(Norman 2018, p.236)

## Faming Foreword: 'Nothing about us, without us'

This paper is written by and for a person who is multiply neurodivergent, with direct lived experience of the material it covers. Providing the reader with a theoretical and lived-experience framing is essential to understanding the scope of this project's necessity, what inclusive design offers wider society, and why functions that appear paradoxical to a reader without lived experience of neurodivergence are in fact deliberate and useful to our community.

# PART ONE: PROTOTYPE DOCUMENTATION

## Makers: 
N Hall

## All code and documentation is available on GitHub:
https://github.com/embedded-by-n/Pear-Pie

## Objective of Prototype:

The objective of the Pear-Pie prototype is to design, build, and evaluate a functional cyber-physical home system that demonstrates how adaptive technologies can support participation within everyday home environments.

The prototype aims to integrate distributed sensing, local processing, and automated actuation into a single modular system capable of responding to changing environmental conditions and user needs. Through iterative design, testing, and reflection, the prototype explores how cybernetic feedback can be used to create technologies that increase affordances rather than simply providing static assistance.

As a proof of concept, the prototype demonstrates the practical application of the Lived Expertise Design Framework by translating systems thinking and lived expertise into a working cyber-physical intervention. Its purpose is to explore how a cyber-physical intervention can generate feedback about both the system being designed and the design process itself, informing future iterations of the technology and the framework.

## List of Functions, Desired and Fulfilled:

## System Functions
## System Functions

### ✅ Fulfilled

| # | Function | Order | Description |
|---|----------|-------|-------------|
| 1 | Presence sensing | First | **What:** Waveshare HMMD mmWave radar (S3KM1110, 24GHz) reads presence and rough range over UART. **How:** plain-text output ("ON", "Range 65") debounced on the Pico. **Why:** senses a person's existence, never their identity. No cameras, no microphones. |
| 2 | Adaptive baseline learning | First | **What:** each pod learns its own room's normal occupancy. **How:** an Exponentially Weighted Moving Average updates every loop, on-device, unsupervised. **Why:** the system learns *your* normal, never a neurotypical norm. A polyphasic sleeper is a valid baseline, not a fault. |
| 3 | Ambient light response and emergent trail | First | **What:** arrival sweep in blue, purple trail held, fade over time. **How:** lights trigger on the rising edge of presence; the trail across rooms is emergent, each pod independently reacting in turn. **Why:** externalises spatial memory. You can see where you have been. |
| 4 | BLE broadcast | First | **What:** every pod broadcasts its state each loop. **How:** BLE advertise-and-scan, uplink packet "PP" (pod_id, presence, unusual, sequence). No pairing, no central authority. **Why:** decentralised by design; no pod depends on any other to function. |
| 5 | Time Timer tool pod | First | **What:** a physical Time Timer on an LCD with a rotary dial. **How:** red winds on anticlockwise, drains clockwise, sixty minutes to the full circle. An EWMA learns your preferred duration and auto-starts at it; presence pauses and resumes it; completion sparkles gently instead of alarming. **Why:** makes time visible without ever issuing a demand. |
| 6 | Hub event logging | Second | **What:** the hub logs every broadcast from every pod. **How:** `bleak` scanner stamps each event with one shared clock into `pod_log.csv`. Over 2.7 million readings. **Why:** one consistent timebase is what makes pattern learning possible. |
| 7 | Second-order parameter control | Second | **What:** the hub retunes each pod's learning rate (alpha) and sensitivity (threshold). **How:** deterministic rules measure each space's activity and push clamped updates down over BLE (packet "PU"). Control, not machine learning. **Why:** this is the homeostat's second loop — the system adapts the rules the pods follow. |
| 8 | Next-room prediction | Second | **What:** the hub predicts where you will go next. **How:** a scikit-learn decision tree trained on movement transitions (hour, day, current space), holdout accuracy 0.58 against ~12.5% chance, wired into the control loop to pre-warm the predicted pod. **Why:** the home gets ready ahead of you, without asking. |
| 9 | E-ink status face | Second | **What:** a calm always-on summary: where you are, each room's learned rhythm, total readings. **How:** Inky Impression 7.3" refreshing every ten minutes. **Why:** information without demand. It never asks for anything. |
| 10 | Projected pattern map | Second | **What:** a live visual of the whole system thinking. **How:** pygame projection of the walked trail, learned occupancy, the predicted next room as a pulsing gold ring, and a rolling second-order activity log. **Why:** makes your own emergent patterns legible to you — the network observed, handed back to the actor inside it. |
| 11 | Graceful degradation | First | **What:** the system survives hub failure. **How:** pods hold their last-learned parameters locally and continue autonomously. **Why:** Ashby's ultrastability. The function the person depends on never disappears. |

### 🟡 Partly fulfilled

| # | Function | Order | Description |
|---|----------|-------|-------------|
| 12 | Vitals sensing | First | **What:** respiration, heart rate and sleep staging via DFRobot C1001 60GHz radar. **How:** read on the Pi through the HumanDetection library. **Status:** it read, but values were unreliable, slow, and sometimes reported with nobody present. Deferred to protect the MVP; documented, not claimed. |
| 13 | RSSI proximity signal | Second | **What:** signal strength as a coarse distance measure. **How:** RSSI is captured with every logged reading. **Status:** logged, not yet used by the model. Feeds the designed localisation tier. |

### 🔵 Desired

| # | Function | Order | Description |
|---|----------|-------|-------------|
| 14 | Object-find | First | **What:** finding lost possessions, a core executive-function need. **How:** BLE beacons on objects, always-glow LED throwies, and an Anchor Pod combining charging dock, undocked-warning ring and a find button. **Why:** working memory support extended to things, not just spaces. |
| 15 | Sensor fusion | First | **What:** richer, cheaper sensing per pod. **How:** PIR for instant wake paired with mmWave for sustained stillness, plus designed light-spectrum, capacitive-touch and pressure-mat modalities. **Why:** radar catches a still person PIR misses; fusion covers both. |
| 16 | Modular clip-on capability | First | **What:** physical modules that add or remove functions. **How:** capability granted and removed at the hardware; unplugging at the bus physically deletes the function. **Why:** agency over the system's powers belongs in the person's hands, not a settings menu. |
| 17 | Simplex SMS channel | Second | **What:** the home's only external channel, outbound alerts. **How:** cellular module on the hub, AT commands over serial, send-only. **Why:** the data-diode principle — the system can reach out, nothing can reach in. |
| 18 | RTC module | Second | **What:** wall-clock time without any network. **How:** battery-backed real-time clock on the hub. **Why:** fully off-grid operation with accurate timestamps. |
| 19 | Encrypted BLE and threat modelling | Second | **What:** hardening the radio layer. **How:** encrypted BLE, formal threat model, security testing. **Why:** the current build is advertise-and-scan, unencrypted; stated honestly, scheduled properly. |
| 20 | Third-order loop | Third | **What:** the system regulates its own fit to the person. **How:** balancing checks at three timescales (daily rhythm, slow drift, "unusual for you"), adjusting how it adapts. **Why:** the regulated variable becomes the fit itself — never the person's behaviour. The named frontier of the project. |
| 21 | Neural network tier | Third | **What:** richer pattern recognition than the decision tree. **How:** designed for Edge Impulse or emlearn-style deployment. **Why:** deeper temporal patterns, still local, still private. |
| 22 | RSSI fusion localisation | Third | **What:** from "which room" toward "where in the path". **How:** fusing already-logged RSSI across multiple pods, resolving the doorway problem when two pods both hear presence. **Why:** finer spatial memory without adding a single sensor. |

### ⚪ Out of scope

| # | Function | Description |
|---|----------|-------------|
| 23 | Cameras, microphones, Wi-Fi | Deliberate exclusion, not a gap. The system captures no image or audio and holds no inbound network channel. Privacy is structural, which matters acutely in domestic-violence contexts. |
| 24 | Multi-occupant identification | Deliberate exclusion. The system senses existence, not identity, and cannot become a surveillance tool aimed at the people around its user. |
| 25 | Cloud connectivity, remote access, companion app | Against the thesis. No subscription, no account, no server dependency, no company that can sunset your support system. |
| 26 | Home Assistant / third-party integration | The architectural opposite of the design: centralised, networked, app-managed. Excluded from this build. |
| 27 | Medical diagnosis or clinical monitoring | Pear-Pie is an exploratory prototype. It does not diagnose, replace professional care, or provide emergency monitoring. |




an off-grid modular home system using a two-tier Raspberry Pi 5 and Pi Pico control system with BLE mesh, RADAR, and edge ML to create a self-regulating feedback loop. 
Inspired by W. Ross Ashby's homeostat (1948) and designed by a neurodivergent person for people with fluctuating capacity, it learns each user's homeostasis over time, adapts its actuation style accordingly, and recognises emergent patterns across the distributed pod network to help users pre-empt capacity shifts. 
First-order learning happens on the BLE mesh as pods regulate the home through peer-to-peer broadcast; second-order learning happens at the hub, which observes the network's behaviour over days and weeks and updates the rules the pods follow, so the system fits each user's homeostasis as it changes.
Particular care is given to PDA-profile (Persistent Drive for Autonomy) neurodivergent users, supporting executive functioning and working memory by externalising cognitive load. Asking who we unconsciously see as viable users of cutting-edge technology: the Pear Pie embodies the curb-cut effect. Design affordances for disability as a priority, and everyone benefits.

<img width="1440" height="1520" alt="image" src="https://github.com/user-attachments/assets/4dcc8783-aefc-49a5-9b68-2c56da2a0fee" />


# Overview

The Pear Pie is a distributed cyber-physical system inspired by W. Ross Ashby's homeostat (1948), built in Python (hub) and MicroPython (pods). It is an off-grid modular home system designed to support executive functioning and working memory for neurodivergent users with fluctuating capacity, while remaining useful to anyone.
Pods are placed throughout the home, each running a Raspberry Pi Pico 2 W with its own presence sensing (mmWave RADAR), a local Adaptive Baseline (Exponentially Weighted Moving Average) for learning what is normal in its space, and a small LED trail that quietly shows where the user has recently been. Pods broadcast their state peer-to-peer on a Bluetooth Low Energy mesh as a first-order regulation loop.
The hub is a Raspberry Pi running a Python observer that hears every pod, logs events with a single shared timestamp, and learns each user's emergent patterns over days and weeks using scikit-learn. It then pushes rule updates back down to the pods over the same BLE mesh as a second-order regulation loop. The pods regulate the home; the hub adjusts the rules the pods follow.
A separate pod variety, the vitals pod, uses DFRobot's C1001 60GHz mmWave sensor and Python HumanDetection library to add respiration, heart rate, and sleep tracking. The architecture supports multiple specialised pod types alongside the standard presence pods.
The system is off-grid by design. No cloud, no internet dependency. Outbound-only (simplex) SMS is the only channel that leaves the home. Pods continue to function autonomously if the hub fails; the system gracefully degrades from a learning homeostat to a stable one without losing the function the user actually experiences.

## Conceptual mapping to Ashby's homeostat

| Ashby's Homeostat | Pear Pie |
| --- | --- |
| Magnetic needle position | Pod sensor readings (presence, vitals) feeding the Adaptive Baseline |
| Essential variable bounds | The user's fluctuating capacity, kept within dignity-preserving thresholds |
| First-order feedback | Pods sense, learn locally, light the trail, and broadcast state over the BLE mesh |
| Uniselector switching | Hub adjusts pod parameters (alpha, threshold) when patterns drift from the learned norm |
| Second-order adaptation | Hub observes the network over days and weeks, learns each user's homeostasis, and pushes rule updates down to the pods |
| Ultrastability | System gracefully degrades: pods continue autonomously if the hub fails, holding their last-learned configuration |

## Control algorithm: Ashby-style ultrastability

This system implements a double feedback loop faithful to Ashby's design, distributed across two physical tiers: the pods at the first order, and the hub at the second.

### First-order loop (local homeostasis, on each pod)

Each pod maintains its sense of normal in its own space by running an Adaptive Baseline (Exponentially Weighted Moving Average) over its sensor readings. When a reading sits sufficiently above the learned normal, the pod treats it as "unusual" (presence) and acts accordingly.

Pod actions:

* Newly unusual reading: trigger arrival sweep (blue), hold purple trail at full
* Sustained unusual reading: reset the fade timer, keep the trail bright
* No unusual reading: trail fades over the configured FADE_SECONDS, broadcast quiet state
* Every loop: pod broadcasts its current state on the BLE mesh, so other pods and the hub can react

The pods do not coordinate explicitly. Each one regulates its own space. The light trail across rooms is an emergent pattern, the visible result of the person moving and each pod independently reacting in turn.

### Second-order loop (network learning, at the hub)

The hub observes the pod network over time. It scans every BLE broadcast, stamps each event with its own clock for a single shared timebase, and logs them into a continuous record of the home's behaviour. Over days and weeks, the hub learns each user's emergent patterns: which spaces are usually occupied when, how the user moves between them, what counts as a typical day versus an unusual one.

When the hub recognises that a pod's current alpha (learning rate) or threshold (sensitivity) no longer fits the user's actual rhythms, it pushes a parameter update down to that pod over the same BLE mesh:

* Pod parameters (alpha, threshold) drift from the learned norm  →  Hub broadcasts a downlink update packet
* Pod receives the update and applies the new parameters  →  Local Adaptive Baseline adjusts to the user's current homeostasis

This is analogous to Ashby's uniselector mechanism, but informed rather than random: the hub does not search blindly for a stable configuration, it learns one from the user's actual data and pushes it down. The trial-and-error happens in the data, not in the live system.

### Graceful degradation (ultrastability under disturbance)

If the hub fails, is removed, or loses power, the pods continue to function autonomously at their last-learned configuration. The system degrades from a learning homeostat to a stable one without losing the function the user actually experiences. This is the structural commitment Ashby called ultrastability: the system stays in its viable region even under significant disturbance.

### Why it works

* **Negative feedback** at the pod layer keeps each space's essential variable (presence relative to learned normal) in range
* **Parameter adaptation** at the hub layer searches for the alpha and threshold configurations that fit the specific user
* **Emergent behaviour**: the light trail across the home is not programmed, it arises from independent pods reacting to one moving person
* **Requisite variety**: by allowing tiered learning (pod-level statistics, hub-level patterns) and graceful degradation, the system holds enough variety to absorb disturbances without demanding that variety from the user
* **Dignity as an essential variable**: the system is designed so that its core function (recognising the user's presence and rhythms, ambient support of executive functioning) is preserved even when the hub or any individual pod fails, because the user's ability to function is the variable the whole system exists to keep in range

## System behaviour goals

1. **Dignified equilibrium**: the system maintains each user's homeostasis without ever demanding their attention or compliance, ambient regulation, never intrusive prompting.
2. **Sensing variety**: the pod network learns and adapts across multiple modalities (presence, vitals, time) so the system fits the user's actual life rather than a fixed assumption of it.
3. **Self-organisation**: the hub finds each user's own stable pattern from their lived data, not from preset normal.
4. **Resilience**: the system gracefully degrades, pods continue at their last-learned configuration if the hub is removed, and the home keeps working at the level the user actually experiences.
5. **Curb-cut benefit**: designed for neurodivergent users with fluctuating capacity, the system serves anyone who benefits from a home that quietly remembers, supports, and adapts.

## Hardware

### Hub
* Raspberry Pi (current build runs on Pi 5; architecture supports Pi Zero 2 W for lower-power deployment)
* 5" LCD touchscreen for ambient status display
* RTC module for real-time wall-clock timestamps (needed off-grid, no internet)
* Cellular module for simplex (out-only) SMS, the only channel that leaves the home

### Presence pods
* Raspberry Pi Pico 2 W (one per pod, identical hardware, single config.py per pod)
* 24GHz mmWave RADAR module for presence sensing
* Lorikeet (WS2812-compatible) LED strip for the ambient light trail
* USB-C power, breadboard prototype

### Vitals pod (specialised pod variety)
* DFRobot C1001 60GHz mmWave sensor (respiration, heart rate, sleep staging)
* Raspberry Pi running DFRobot's Python HumanDetection library
* Bed-mounted or desk-mounted configurations supported via the C1001's work-mode switching

### Network
* Bluetooth Low Energy mesh between all pods and the hub (peer-to-peer, no pairing, no central authority)
* Up-path: pods broadcast state in a shared uplink packet format
* Down-path: hub broadcasts rule updates in a shared downlink packet format
* All packet contracts are file-replicated between hub and pod folders to guarantee byte-for-byte agreement

### Off-grid posture
* No cloud, no internet dependency, no wifi-to-outside
* Simplex (out-only) SMS is the only channel that leaves the home; nothing comes back in
* All learning runs locally on the hub and the pods

## Hardware setup notes

1. **Pod placement**: each pod's radar should be positioned to cover the space it's meant to sense (typically a doorway, key area of a room, or a path between spaces). Avoid pointing two pods' radars directly at each other; the overlap creates double-counting and confuses the learned baseline.
2. **Pod height**: mid-wall height (about 1.2-1.5m from floor) works well for whole-room presence. Lower or higher trades off coverage area for sensitivity to specific motion types.
3. **Radar field of view**: mmWave modules have wider beams than most users expect. Constraining the field with a simple shielding shroud (metal, opaque) gives cleaner per-space sensing and reduces false-positive presence when someone walks past a doorway without entering.
4. **Power**: presence pods run from USB-C and draw very little. The hub draws more (especially with the touchscreen), and benefits from a UPS HAT or backup battery if the home loses power mid-learning.
5. **BLE range**: legacy BLE adverts carry across a typical home easily, but very thick walls, metal cladding, or multiple floors may attenuate the signal. If a pod isn't being heard, move the hub or add a relay pod between them.
6. **Sensor calibration**: each pod's Adaptive Baseline (Exponentially Weighted Moving Average) needs time to settle. Allow ~10 minutes of typical use after installation before judging whether the pod is reading the space correctly.

### Pod configuration

Every pod runs identical code; only the per-pod `config.py` differs. Setting up a new pod is therefore: copy the pod files, edit `POD_ID` in `config.py`, flash to the Pico, install in place.

Per-pod settings (in `config.py`):

* **POD_ID**: unique integer per pod, used by the hub to identify the source of each broadcast and to address downlink rule updates
* **PRESENCE_PIN**: GPIO pin connected to the radar's presence output (default: 11)
* **LED_PIN**: GPIO pin connected to the lorikeet data line (default: 0)
* **NUM_LEDS**: number of LEDs on this pod's strip (default: 5)
* **FADE_SECONDS**: duration of the presence trail fade (default: 30)
* **ALPHA**: Adaptive Baseline learning rate (default: 0.01; smaller = slower, steadier adaptation)
* **THRESHOLD**: how far above the baseline a reading must sit to be classed as "unusual" (default: 0.5)

Pod-to-hub identity mapping is held in `pod_registry.py` on the hub side, which maps each `POD_ID` to its space (e.g. hallway, lounge) and role (e.g. presence, vitals).

### BLE packet contracts

The mesh's reliability depends on every device agreeing on the byte layout of the packets. Two shared contracts are file-replicated across both the hub and pod folders, and must remain byte-for-byte identical:

* **`uplink_packet.py`**: pod-to-hub state packets. Marker `b"PP"`, carrying pod_id, presence, unusual flag, and sequence number.
* **`downlink_packet.py`**: hub-to-pod parameter updates. Marker `b"PU"`, carrying target_pod_id, alpha, threshold.

If either packet's format is changed in one folder, the matching copy in the other folder must be updated in the same commit. Mismatched copies will silently fail to decode rather than throwing an obvious error, so this is one of the project's hard rules.

### Off-grid clock

The hub has no internet, so it cannot fetch the real time on boot. An RTC (real-time clock) module on the hub provides wall-clock timestamps for all logged events. This is essential for time-of-day pattern learning ("this happens every weekday morning"); without it, logs would be in seconds-since-boot rather than real dates and times.

### Simplex (out-only) SMS

For the rare cases where the system needs to reach beyond the home (e.g. a fall alert), a cellular module attached to the hub sends SMS via AT commands over serial. No inbound channel exists; the system cannot be reached, only reached out from. This applies the data-diode design principle (one-way information flow) at the system's only external interface.

## Getting started

The Pear Pie is a two-tier system, so setup happens in two halves: hub setup and pod setup. Identical pod code is flashed to each Pico, and a single per-pod `config.py` differs between them.

### Hub setup (Raspberry Pi)

* Clone the repository:
  `git clone https://github.com/embedded-by-n/Pear-Pie.git`
* Move into the hub directory:
  `cd Pear-Pie/Pear-Pie(HUB)`
* Install Python dependencies:
  `pip install pyserial scikit-learn pandas`
* (Vitals pod) Clone DFRobot's HumanDetection library if using the C1001:
  `git clone https://github.com/DFRobot/DFRobot_HumanDetection.git`
* Wire the RTC module to the Pi's I2C pins and enable the I2C interface via `sudo raspi-config`
* Run the hub:
  `python main.py`

The hub will begin scanning for pods on the BLE mesh and logging every received broadcast to `pod_log.csv` with its own clock for a single shared timebase.

### Pod setup (Raspberry Pi Pico 2 W)

* Flash MicroPython firmware to the Pico (drag the `.uf2` onto the Pico's BOOTSEL drive). The current verified build uses `RPI_PICO2_W-20260406-v1.28.0.uf2` from `micropython.org/download/RPI_PICO2_W/`.
* Copy the following files from `Pear-Pods(MODULES)/` onto the Pico:
  `main.py`, `config.py`, `led.py`, `gossip.py`, `baseline.py`, `uplink_packet.py`, `downlink_packet.py`, `rule_listener.py`
* Edit `config.py` on the Pico: set `POD_ID` to a unique integer (1, 2, 3...). Leave the rest at defaults unless the wiring differs.
* Wire the radar (VIN/GND/OT2 to power, ground, GP11), and the lorikeet LED strip (data to GP0, power, ground).
* On boot, the Pico will run `main.py`: it senses, learns its local baseline, lights the trail, and broadcasts on the BLE mesh. The hub will start hearing it immediately.

Repeat the pod setup for each additional pod, changing only `POD_ID` in `config.py`.

### Pod registry

After setting up pods, edit `pod_registry.py` on the hub to map each `POD_ID` to its space and role:

```python
POD_REGISTRY = {
    1: {"space": "hallway",  "role": "presence"},
    2: {"space": "lounge",   "role": "presence"},
    ...
}
```

The hub uses this to translate raw pod IDs into meaningful spaces during analysis and learning.

## References

* Ashby, W. R. (1960). *Design for a Brain: The Origin of Adaptive Behaviour*
* Ashby, W.R. (1956) An Introduction to Cybernetics. London: Chapman & Hall.
* Beresford, P. (2003) It's Our Lives: A Short Theory of Knowledge, Distance and Experience. London: Citizen Press.
* Checkland, P. (1999) Systems Thinking, Systems Practice. Chichester: Wiley.
* Churchman, C.W. (1970) Operations Research as a Profession. Management Science, 17(2), pp. B37–B53.
* Duvall, J., Sivakanthan, S., Daveler, B., Sundaram, S. A., & Cooper, R. A. (2022). "Inventors with disabilities, an opportunity for innovation, inclusion, and economic development." *Technology and Innovation*, 22(3), 315-329. https://doi.org/10.21300/22.3.2022.5
* Gibson, J.J. (1979) The Ecological Approach to Visual Perception. Boston: Houghton Mifflin.
* Indigenous Protocol and Artificial Intelligence Working Group (2020). *Indigenous Protocol and Artificial Intelligence Position Paper*. Honolulu, Hawai'i.
* Kaiko I, Ham I van der and Schomaker J (30 June 2026) ‘The condition that causes people to get lost in their own home’, ABC News, accessed 2 July 2026, https://www.abc.net.au/news/2026-07-01/developmental-topographical-disorientation-people-lost-in-home/106863294, accessed 2 July 2026.
* Latour, B. (2005) Reassembling the Social: An Introduction to Actor-Network-Theory. Oxford: Oxford University Press.
* Meadows, D.H. (2008) Thinking in Systems. Chelsea Green.
* Midgley, G. (2000) Systemic Intervention: Philosophy, Methodology, and Practice. New York: Kluwer Academic/Plenum Publishers.
* Norman D (2013) *The design of everyday things: revised and expanded edition*, Basic Books, New York.
* Okai-Ugbaje, S. (forthcoming). "The Cybernetic Wheel: A model to aid the design and development of safe, responsible and sustainable technological systems."
* Oliver, M. (1990) The Politics of Disablement. London: Macmillan.
* Rosenblueth, A., Wiener, N., & Bigelow, J. (1943). "Behavior, purpose and teleology." *Philosophy of Science*, 10(1), 18-24
* Shakespeare, T. (2018) Disability: The Basics. London: Routledge.
* Swift, B. (2025). Hendrix homeostat [Source code repository]. ANU Cybernetic Studio. https://github.com/ANUcybernetics/hendrix-homeostat. README structure and conceptual-mapping framework adapted for the Pear Pie project.
* Tsing, A.L. (2012) On Nonscalability: The Living World Is Not Amenable to Precision-Nested Scales. Common Knowledge, 18(3), pp. 505–524.
* Ulrich, W. (1983) Critical Heuristics of Social Planning: A New Approach to Practical Philosophy. Bern: Haupt.
* von Foerster, H. (1974). *Cybernetics of Cybernetics*
* Wiener, N. (1948) Cybernetics: Or Control and Communication in the Animal and the Machine. Cambridge, MA: MIT Press.

* ANUcybernetics. *hendrix-homeostat* (related work, ANU Master of Applied Cybernetics). https://github.com/ANUcybernetics/hendrix-homeostat

## Licence

Copyright (c) 2026 Nicola Hall

Licensed under the GNU Affero General Public License v3.0 (AGPL-3.0). See LICENSE file for details.

The AGPL closes the SaaS/network loophole that ordinary GPL leaves open: anyone who modifies and deploys this system over a network must release their modifications under the same terms. This is a deliberate choice to keep the Pear Pie and its descendants open, repairable, and free from being locked behind proprietary services, consistent with the project's commitment to open, accessible, and dignified assistive technology.
