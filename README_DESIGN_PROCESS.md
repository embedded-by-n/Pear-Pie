
1. Realising that I went gestalt and accidently did all the workd for the research project before doing the build itself.
2. 



















<img width="1202" height="572" alt="Screenshot 2026-04-01 083031" src="https://github.com/user-attachments/assets/d18fe7e9-5599-492f-ae26-aef32d8a3e8f" />

<img width="487" height="355" alt="Screenshot 2026-06-05 073751" src="https://github.com/user-attachments/assets/7aaa3c25-5ce9-4e55-9cbc-f9645eba5095" />
<img width="939" height="559" alt="Screenshot 2026-06-05 073628" src="https://github.com/user-attachments/assets/3fe059d4-77e9-41ab-afc7-b7a1b860b450" />
<img width="188" height="374" alt="Screenshot 2026-06-05 064814" src="https://github.com/user-attachments/assets/e5fe459e-e610-4a13-98f1-1876eca0fc17" />
<img width="255" height="271" alt="Screenshot 2026-06-05 054013" src="https://github.com/user-attachments/assets/ad5c60c5-bbe2-43a1-9ed1-d28aa95b402c" />
<img width="1092" height="564" alt="Screenshot 2026-04-23 143349" src="https://github.com/user-attachments/assets/829fef82-5657-49ab-9c8f-6d30c55bdb65" />

Radar Pear Pie Process Document:

Pear Pie ~ Running Document
Rules of this document
•	Every entry is proposed first and only added after Nina approves it.
•	Once an entry is in, it stays. Claude does not edit, rephrase, or tidy past entries.
•	New entries are appended in order.
________________________________________
Entry #1 ~ What the Pear Pie is
An off-grid home system designed specifically to assist with executive functioning. It needs to consider safety and functionality. It's my individual design idea.
The software and hardware clip together to make user-defined open-source systems more accessible for disabled people, or people with intellectual disabilities. You shouldn't have to be highly technical to understand open source.
Ease of access can be internet, can also not involve internet. Could have Wi-Fi, could also not have Wi-Fi.
A home console with all software built in — like a Raspberry Pi, but for disability. Premade rather than components only, where everything is self-built and created.
It would have an impact on society because it would help so many people to access this beautiful world of self-creation and technologies that is inaccessible to people without technical skill. It's also a way to help create a device that can lower costs for [unfinished ~ Nina to complete]
________________________________________
Entry #2 ~ Design Brief Notes
Display and interface
•	Has an ink LED display.
•	Each component of the system can clip on and off.
Power harvesting
•	Potential radio power harvesting.
•	Microturbines connected to taps in the house.
•	Use of friction power at doorways for closing and opening.
•	Pressure power pads.
•	Harvesting output and input power to generate power — think Woomera style.
•	Potentially use of spark jump power, like in radio-controlled little cars from the mid-fifties. I read something about that. Think the kinds of technologies included in things such as cat's whisker cohering.
Aesthetic
•	Mid-century Australian space design.
•	Mid-century 1950s atomic style technology.
Communications
•	SIM card for communications that go out but don't go back in.
Design philosophy
•	Reverse engineering of old technologies, to show that they have continued applicability into the future.
•	Think Indigenous style — time moves through us, not us through time. Therefore validity to all different forms of technologies.
•	The cross-application of old and new technologies together.
•	Not all tech needs to be high power or online for it to be useful, or beneficial to lots of people. For example, many poor people can't afford Wi-Fi. Maybe the futures of these technologies won't ever include being on the grid. It's good to work towards this. So [unfinished ~ Nina to complete]
________________________________________
Entry #3 ~ Systems thinking, feedback and control
Power and feedback
•	Solo input, multi-power input.
•	Feedback and control — using the output of the system to regulate and control it, such as harvesting output and input power to generate more power.
•	Device uses existing energy in the system, like the centrifugal flyball governor.
•	Aiming for balanced feedback.
Systems thinking
•	It might be useful to consider the Systems Thinking Playbook.
•	Concurrent sensing and actuating. Actuation needs the execution of actions.
•	Ashton and Murray feedback systems.
•	Systems connected in a way that each system influences each other.
Framing the design
•	The goal of my design — power to the people.
•	What assumptions are you making about people and how they use systems?
•	Frame what is and isn't outside the design brief.
•	How to make a low-variety customisable system which is modifiable [unfinished ~ Nina to complete]
________________________________________
Entry #4 ~ Variety, control, and circular causality
The design challenge
•	How to make a low-variety customisable system which is modifiable, with a wide event horizon.
•	The challenge and beauty is that we are absorbing part / all of the executive function component into the system itself. So it doesn't function how other systems like this usually would — because part of the point is that it's helping people with executive functioning challenges.
Feedback, design, and control (Part 2)
•	Tesla's radio boat — control via visual observation even at night.
•	Determining purpose and objective of the system separate from the physical mechanism.
•	Living loops, nodes.
Principles
•	Complexity does not always equal resilience.
•	High variety equals costly.
•	Control equals sense, compare, actuate, symbiote.
•	Control equals sense, compute, actuate, symbiote.
•	Circular causality [unfinished ~ Nina to complete]

**Pear Pie design log: decisions and processes from this chat**

* Identified scope risk: 12 weeks plus $250 cannot deliver a fully built modular ecosystem, so adopted a "build one fully, stub the rest" strategy. Hub built for real, Time Timer Pod plus External Time Timer fully working, remaining module slots present as labelled clip-in points only.

* Locked the hub compute platform as Raspberry Pi 5 8GB, chosen for GUI responsiveness and headroom to run Pygame plus BLE plus the joule reader concurrently.

* Locked the hub display as the official 7" Raspberry Pi touchscreen, chosen over e-ink and retro LCD options on the grounds of build simplicity (DSI ribbon, no driver work) and to free build time for the chassis and pressure pad.

* Selected Python with Pygame in full-screen mode as the Pear OS GUI framework, started at boot via systemd, so the aesthetic can be controlled rather than defaulting to Raspberry Pi OS desktop.

* Defined the module bus architecture: GPIO broken out to physical pogo-pin clip points, SPI for fast modules, I2C for slow ones, with a power rail and ground at every clip point.

* Defined the Time Timer module pair: a small Pod that clips into the hub (ID chip plus pogo contacts, optionally an RP2040 if more capability is wanted), paired with a wall-mounted External Time Timer using Adafruit Circuit Playground Bluefruit, PIR sensor, e-ink display, rotary encoder with click, and a 500mAh LiPo with charging breakout, communicating to the hub over BLE.

* Reframed the pressure pad after your clarification: not a sensor module on the data bus, but a power input feeding a separate power bus inside the hub. Clean architectural split between data modules (SPI/I2C) and power inputs (USB-C, future solar, harvest pad).

* Chose piezo discs over electromagnetic generators for the harvester, on the basis that piezo is cheaper, has no moving parts, and fits within the 12-week build window without taking time from the main hub build.

* Established the energy honesty position: the pad will not run the Pi, it will trickle-charge a backup battery and contribute visibly via a joule gauge. Stated this would be documented openly in the build journey rather than overclaimed.

* Locked the pad's physical location as a hallway runner, for continuous traffic across Demo Day so the joule gauge moves visibly rather than sitting flat between visitors.

* Locked the Demo Day visibility design: an LED wired directly off the piezo output (passive, current-limited, powered by the step itself) for the per-step pulse, plus a cumulative joule gauge rendered live on the touchscreen.

* Added the ADS1115 ADC breakout to the parts list, because the Pi 5 has no built-in analog input and the joule gauge needs to read the supercap voltage over time to compute cumulative joules.

* Compiled a full Australian-sourced parts list with rough AUD prices, totalling approximately $670 if everything is purchased new.

* Flagged budget reality: the course excludes lab/box items from the $250 cap, so the relevant figure after auditing the supplied box is closer to $370 in budget-counted parts. Identified five line items likely already supplied (CPB, USB-C PSU, microSD, PIR, hookup wire/headers/breadboard/resistors).

* Identified two paths to close the residual ~$120 budget overage: drop to Pi 4B plus a cheaper Waveshare 5" display to hit budget exactly, or document the overage as a deliberate scope decision in the build journey.

* Produced a visual mood image of the hardware in situ: walnut sideboard, mid-century atomic styling, the hub with touchscreen and step LED and four clip-in slots (one filled), the External Time Timer wall-mounted with PIR eye and rotary knob, the hallway runner with visible piezo discs and the cable returning to the hub.

* Open questions still on the table: chassis form factor (horizontal console vs upright tabletop radio), chassis material (wood vs painted aluminium for the Australian space program aesthetic), final count and arrangement of physical module slots in the chassis, and the build sequence across the 12 weeks.

Sensor selection exploration (active)
•	Reviewed Infineon XENSIV 60 GHz radar options (BGT60LTR11AIP, TR13C, UTR11AIP, LTR11SAIP)
•	Identified blockers: BGA packages need reflow, eval kits run high, current draw conflicts with off-grid budget, no CircuitPython drivers
•	Surveyed alternatives: HLK-LD2410 mmWave radar, VL53L1X and VL53L5CX time of flight, PAJ7620U2 gesture, capacitive touch via MPR121 or built in Bluefruit pads
•	APDS-9960 ruled out based on prior experience

Here's your design process to date, organized by phase. This is genuinely substantial documentation for your build journey.
Starting position
•	Began with existing design brief defining Pear Pie as a homeostatic familiar for executive function difference: off-grid, PDA-aware, hardware-as-interface
•	Cybernetic wheel framing from Okai-Ugbaje paper structured the brief's argument
•	Core thesis locked from the start: presence as input, no network, designed to be ignorable
Architectural decisions
•	Considered Home Assistant Green as a shortcut, rejected as the architectural opposite of the thesis (centralised, networked, app-managed, sealed)
•	Considered Pi as single central controller, rejected for first-order homeostat limitations
•	Considered all-microcontroller mesh, rejected for adaptive learning constraints
•	Locked in two-tier architecture: on-hub clip-on Modules grant capabilities, distributed Pods extend through space
•	Locked in second-order cybernetic framing: Pods regulate the home (first order), hub regulates the rules the Pods follow (second order)
•	Locked in graceful degradation: Pods function autonomously without the hub, system degrades gracefully across timescales (minutes, hours, weeks, years)
Chip and board selection
•	Considered Circuit Playground Bluefruit (original brief), considered Adafruit ESP32-S3-Zero, considered STM32 family
•	Considered Raspberry Pi 5 as hub, rejected as overkill for power and boot time
•	Considered Pico 2 W only architecture (Inky Frame), considered keeping Linux on Pi
•	Considered Infineon BGA mmWave chips, rejected as industrial tier (BGA packaging, custom PCB required, no maker ecosystem)
•	Locked in: Pi Zero 2 W for hub (Linux + BLE + low power), Pi Pico 2 W for Pods (instant boot + deep sleep + ecosystem maturity)
Display selection
•	Considered Inky Frame for all-in-one simplicity, considered Inky Impression for cleaner face
•	Considered HyperPixel 2.1 Round LCD for Time Timer, rejected for always-on backlight (PDA-hostile) and GPIO monopolisation
•	Considered round e-ink for Time Timer, found unavailable at hobbyist scale
•	Locked in: Inky Impression 7.3" for hub face, rectangular e-ink behind round bezel + servo-driven physical wedge for Time Timer
•	Locked in: ambient NeoPixel ring around hub bezel as nightlight + state indicator + arrival pulse
Communication protocol exploration
•	Considered Wi-Fi for inter-device communication, rejected for "no network" thesis
•	Considered LoRa/Meshtastic, considered Bluetooth Mesh
•	Locked in: peer-to-peer BLE advertise-and-scan, no pairing, no addressing, no central authority
•	LoRa described in brief as future Pod type for village-scale extension, BLE Mesh described as enhancement path without new hardware
Sensor selection
•	Considered PIR alone, rejected as insufficient (misses stillness)
•	Considered camera-based presence detection, rejected for privacy
•	Locked in: PIR + LD2410C mmWave sensor fusion (PIR for fast wake, mmWave for sustained stillness)
•	Locked in: AS7341 light spectrum sensor for circadian baseline adaptation
•	Locked in: MPR121 capacitive touch in furniture for touch-as-input
•	Locked in: FSR pressure mat at front door for threshold sensing
•	Future-described in brief: ToF, ultrasonic, smell sensors, load cells in cupboards
Power and energy
•	Locked in: Pisugar 3 UPS HAT for hub with 3000mAh LiPo and USB-C top-up
•	Locked in: 1000mAh LiPos per Pod, replaceable, magnetic USB-C charging for relevant Pods
•	Considered tap microturbines and RF/piezo energy harvesting, kept as speculative future Pods in brief (not built)
Aesthetic and conceptual framing
•	Locked in: atomic space age form factor inherited from original brief
•	Added: bioluminescent / Avatar-grass framing for LED strips with breathing baselines
•	Added: presence trail concept (recent rooms glow at decay brightness)
•	Added: "spatial residue" / "ambient task memory" / "the home holds the residue of unfinished activity"
•	Added: Actor-Network Theory framing (user, cat, keys, doormat, home all as actants)
•	Added: "I am of no hierarchy above Jimmy" as the project's ethical thesis statement
•	Added: "the system senses your existence, not your identity" for the mmWave privacy framing
•	Added: second-order cybernetics framing for the hub's role
•	Added: "the user exists in the space, the system evolves around the user" as the locked design principle
Object find and anchor system
•	Considered RFID stickers, rejected for range and reader infrastructure
•	Locked in: BLE beacons stuck on possessions + always-glow LED throwies for passive findability
•	Locked in: Anchor Pod design that unifies magnetic charging dock + LED ring + find button (one physical object doing three jobs)
•	Locked in: LED ring red when object is undocked, button press lights the object beacon for find function
Machine learning stack
•	Considered training real neural network from scratch, rejected as too time-intensive
•	Locked in three-layer learning approach: 
o	Adaptive baseline (statistical pattern recognition over presence data, pandas-driven)
o	Decision tree classifier (scikit-learn, trained from user-labelled state data)
o	Edge Impulse tiny neural network (pre-trained for one specific task, e.g. sound classification or Cat TV)
•	Locked in: "what the system has learned" panel on hub display for transparent learning
Rejected explicitly with reasons
•	Home Assistant Green: anti-thesis (centralised, networked, app-managed)
•	Pimoroni Automation HAT: wrong architecture (wired-load, central)
•	APDS-9960 gesture sensor: known reliability issues from prior experience
•	Custom PCB with pogo pins for clip-on bus: not buildable in time
•	Infineon BGA radar chips: industrial tier, not maker-compatible
•	HyperPixel Round LCD: backlight always-on, GPIO conflicts
•	Real neural net training from scratch: time constraints
Final commitment (locked)
•	5x Pi Pico 2 W based Pods: Time Timer, Door PIR (with doormat), 2x Lamp Pods, Anchor Pod
•	1x Pi Zero 2 W hub with Inky Impression 7.3" + Breakout Garden HAT + NeoPixel bezel ring + Pisugar 3 UPS
•	5-6 Hub Modules (3 standard, 2 hot-swap demo, 1 USB Wi-Fi optional)
•	BLE beacons + LED throwies for object find system
•	Magnetic USB-C charging for Anchor Pod and portable Pods
•	Timeline: order Monday 19 May, build complete by 8 June, Demo Day 10 June
Process reflections worth capturing
•	Significant mid-conversation exploration phase where multiple product pages prompted re-evaluation
•	Returned to the original brief's architecture (slide 10) after exploring alternatives: the clip-on Modules on top of the BASE UNIT plus distributed Pods through the home
•	Pattern emerged of needing to hold design discipline against scope creep while staying open to genuine improvements
•	Several decisions were reversed once and then locked: clip-on bus dropped then re-locked, Badger Pods dropped then replaced with Pico foundations

Here's your design process to date, organized by phase. This is genuinely substantial documentation for your build journey.
Starting position
•	Began with existing design brief defining Pear Pie as a homeostatic familiar for executive function difference: off-grid, PDA-aware, hardware-as-interface
•	Cybernetic wheel framing from Okai-Ugbaje paper structured the brief's argument
•	Core thesis locked from the start: presence as input, no network, designed to be ignorable
Architectural decisions
•	Considered Home Assistant Green as a shortcut, rejected as the architectural opposite of the thesis (centralised, networked, app-managed, sealed)
•	Considered Pi as single central controller, rejected for first-order homeostat limitations
•	Considered all-microcontroller mesh, rejected for adaptive learning constraints
•	Locked in two-tier architecture: on-hub clip-on Modules grant capabilities, distributed Pods extend through space
•	Locked in second-order cybernetic framing: Pods regulate the home (first order), hub regulates the rules the Pods follow (second order)
•	Locked in graceful degradation: Pods function autonomously without the hub, system degrades gracefully across timescales (minutes, hours, weeks, years)
Chip and board selection
•	Considered Circuit Playground Bluefruit (original brief), considered Adafruit ESP32-S3-Zero, considered STM32 family
•	Considered Raspberry Pi 5 as hub, rejected as overkill for power and boot time
•	Considered Pico 2 W only architecture (Inky Frame), considered keeping Linux on Pi
•	Considered Infineon BGA mmWave chips, rejected as industrial tier (BGA packaging, custom PCB required, no maker ecosystem)
•	Locked in: Pi Zero 2 W for hub (Linux + BLE + low power), Pi Pico 2 W for Pods (instant boot + deep sleep + ecosystem maturity)
Display selection
•	Considered Inky Frame for all-in-one simplicity, considered Inky Impression for cleaner face
•	Considered HyperPixel 2.1 Round LCD for Time Timer, rejected for always-on backlight (PDA-hostile) and GPIO monopolisation
•	Considered round e-ink for Time Timer, found unavailable at hobbyist scale
•	Locked in: Inky Impression 7.3" for hub face, rectangular e-ink behind round bezel + servo-driven physical wedge for Time Timer
•	Locked in: ambient NeoPixel ring around hub bezel as nightlight + state indicator + arrival pulse
Communication protocol exploration
•	Considered Wi-Fi for inter-device communication, rejected for "no network" thesis
•	Considered LoRa/Meshtastic, considered Bluetooth Mesh
•	Locked in: peer-to-peer BLE advertise-and-scan, no pairing, no addressing, no central authority
•	LoRa described in brief as future Pod type for village-scale extension, BLE Mesh described as enhancement path without new hardware
Sensor selection
•	Considered PIR alone, rejected as insufficient (misses stillness)
•	Considered camera-based presence detection, rejected for privacy
•	Locked in: PIR + LD2410C mmWave sensor fusion (PIR for fast wake, mmWave for sustained stillness)
•	Locked in: AS7341 light spectrum sensor for circadian baseline adaptation
•	Locked in: MPR121 capacitive touch in furniture for touch-as-input
•	Locked in: FSR pressure mat at front door for threshold sensing
•	Future-described in brief: ToF, ultrasonic, smell sensors, load cells in cupboards
Power and energy
•	Locked in: Pisugar 3 UPS HAT for hub with 3000mAh LiPo and USB-C top-up
•	Locked in: 1000mAh LiPos per Pod, replaceable, magnetic USB-C charging for relevant Pods
•	Considered tap microturbines and RF/piezo energy harvesting, kept as speculative future Pods in brief (not built)
Aesthetic and conceptual framing
•	Locked in: atomic space age form factor inherited from original brief
•	Added: bioluminescent / Avatar-grass framing for LED strips with breathing baselines
•	Added: presence trail concept (recent rooms glow at decay brightness)
•	Added: "spatial residue" / "ambient task memory" / "the home holds the residue of unfinished activity"
•	Added: Actor-Network Theory framing (user, cat, keys, doormat, home all as actants)
•	Added: "I am of no hierarchy above Jimmy" as the project's ethical thesis statement
•	Added: "the system senses your existence, not your identity" for the mmWave privacy framing
•	Added: second-order cybernetics framing for the hub's role
•	Added: "the user exists in the space, the system evolves around the user" as the locked design principle
Object find and anchor system
•	Considered RFID stickers, rejected for range and reader infrastructure
•	Locked in: BLE beacons stuck on possessions + always-glow LED throwies for passive findability
•	Locked in: Anchor Pod design that unifies magnetic charging dock + LED ring + find button (one physical object doing three jobs)
•	Locked in: LED ring red when object is undocked, button press lights the object beacon for find function
Machine learning stack
•	Considered training real neural network from scratch, rejected as too time-intensive
•	Locked in three-layer learning approach: 
o	Adaptive baseline (statistical pattern recognition over presence data, pandas-driven)
o	Decision tree classifier (scikit-learn, trained from user-labelled state data)
o	Edge Impulse tiny neural network (pre-trained for one specific task, e.g. sound classification or Cat TV)
•	Locked in: "what the system has learned" panel on hub display for transparent learning
Rejected explicitly with reasons
•	Home Assistant Green: anti-thesis (centralised, networked, app-managed)
•	Pimoroni Automation HAT: wrong architecture (wired-load, central)
•	APDS-9960 gesture sensor: known reliability issues from prior experience
•	Custom PCB with pogo pins for clip-on bus: not buildable in time
•	Infineon BGA radar chips: industrial tier, not maker-compatible
•	HyperPixel Round LCD: backlight always-on, GPIO conflicts
•	Real neural net training from scratch: time constraints
Final commitment (locked)
•	5x Pi Pico 2 W based Pods: Time Timer, Door PIR (with doormat), 2x Lamp Pods, Anchor Pod
•	1x Pi Zero 2 W hub with Inky Impression 7.3" + Breakout Garden HAT + NeoPixel bezel ring + Pisugar 3 UPS
•	5-6 Hub Modules (3 standard, 2 hot-swap demo, 1 USB Wi-Fi optional)
•	BLE beacons + LED throwies for object find system
•	Magnetic USB-C charging for Anchor Pod and portable Pods
•	Timeline: order Monday 19 May, build complete by 8 June, Demo Day 10 June
Process reflections worth capturing
•	Significant mid-conversation exploration phase where multiple product pages prompted re-evaluation
•	Returned to the original brief's architecture (slide 10) after exploring alternatives: the clip-on Modules on top of the BASE UNIT plus distributed Pods through the home
•	Pattern emerged of needing to hold design discipline against scope creep while staying open to genuine improvements
•	Several decisions were reversed once and then locked: clip-on bus dropped then re-locked, Badger Pods dropped then replaced with Pico foundations
Want me to file this as a markdown document you can paste into your build journey, or is the inline version enough?

STARTING POSITION

Project began as the Pear Pie: an off-grid, modular, disability-first smart home system designed for users with executive function difference, including PDA
Core thesis locked from the start: presence as input, no network by default, designed to be ignorable
Cybernetic Wheel framework (Okai-Ugbaje) selected as methodological anchor
Indigenous-relational ethical framing: "I am of no hierarchy above Jimmy", time moves through us not us through time
Aesthetic direction: mid-century atomic, Australian space-age, Woomera-style
Original design notes specified power harvesting from environmental energy (microturbines, friction, piezo pads, RF, spark-jump)

ARCHITECTURAL DECISIONS

Considered Home Assistant Green, rejected as the architectural opposite of the thesis (centralised, networked, app-managed, sealed)
Considered single-Pi central controller, rejected for first-order homeostat limitations
Considered all-microcontroller mesh, rejected for adaptive learning constraints
Locked two-tier architecture: on-Hub clip-on Modules grant capabilities, distributed Pods extend through space
Locked second-order cybernetic framing: Pods regulate the home (first order), Hub regulates the rules the Pods follow (second order)
Locked graceful degradation across timescales: Pods function autonomously without the Hub, system degrades gracefully from learning homeostat to stable one
Locked the user-system relationship itself as an essential variable being maintained

HUB CONTROLLER ITERATION

Initially considered Circuit Playground Bluefruit (original brief), Adafruit ESP32-S3-Zero, STM32 family
Considered Pi 5 as Hub, originally chosen for ML headroom
Considered Pico 2 W only architecture (Inky Frame), considered keeping Linux on Pi
Initially locked Pi 5, defensibly reframed as mains-powered
LATER REVERSED: switched Hub to Pi Zero 2 W for genuine off-grid thesis alignment, lower power, smaller form factor, ~$51 savings
Confirmed Inky Impression 7.3" Spectra 6 works with Pi Zero 2 W via same 40-pin GPIO header
Identified the AI Kit (Hailo NPU) as wrong tool: vision-focused while Pear Pie has no cameras by design

POD CONTROLLER SELECTION

Considered Infineon BGA mmWave chips, rejected as industrial tier (BGA packaging, custom PCB required, no maker ecosystem)
Considered Plasma Stick 2040 W and Plasma 2350 W as integrated LED-driving boards
Locked Pico 2 WH for Pods: deep sleep at 10µA for off-grid thesis, instant boot, cost, form factor
5x Pico 2 WH ordered from Pimoroni

COMMUNICATION PROTOCOL

Considered WiFi for inter-device communication, rejected for "no network" thesis
Considered LoRa/Meshtastic, considered Bluetooth Mesh
Considered formal Bluetooth Mesh protocol, rejected for adding central coordination and provisioning complexity
Locked peer-to-peer BLE advertise-and-scan: no pairing, no addressing, no central authority
Architecture achieves mesh-like properties (decentralization, redundancy, resilience) using simpler primitives
BLE RSSI used for topology awareness: 1-2m precision, sufficient for detecting Pod movement
Three-radio architecture articulated: BLE (always-on nervous system), WiFi (opt-in via Module for high-bandwidth), 24GHz mmWave (per-Pod presence sensing)
LoRa described as future Pod type for village-scale extension

SENSOR SELECTION

Considered PIR alone, rejected as insufficient (misses stillness)
Considered camera-based presence detection, rejected for privacy
Considered Infineon BGA radar chips, rejected as industrial tier
Locked PIR + 24GHz mmWave sensor fusion (PIR for fast wake, mmWave for sustained stillness)
Initial radar choice: DFRobot SEN0557 (5V supply)
Considered HLK-LD2420 (3.3V supply, cleaner architecture) but sourcing risk in Australia
Considered HLK-LD2410C (5V supply but 3.3V signals, well-supported)
Locked AS7341 light spectrum sensor for circadian baseline adaptation
Locked MPR121 capacitive touch in furniture for touch-as-input (later scoped out)
Locked FSR pressure mat at front door for threshold sensing (later scoped out)

POWER ARCHITECTURE EVOLUTION

Original plan: Adafruit PowerBoost 1000 for Trail Pod power management
Considered PiicoDev LiPo Expansion (charging only, no boost)
LATER REVISED: switched to Adafruit AF-6106 bq25185 USB/DC/Solar Charger with 5V Boost
Saves cost AND adds solar input AND simpler architecture than PowerBoost
Considered DFM8001 Indoor Energy Harvesting Kit, identified as microwatt-scale (wrong regime for Trail Pods, right for future ultra-low-power Pods)
Hub power: switched from Waveshare UPS HAT for Pi 5 to Pisugar 3 for Pi Zero
Three-tier power architecture for Biotrail Pods: USB-C mains tap-in, LiPo battery, embedded solar cell
Solar reframing: "off-network" not "off-grid", indoor solar provides trickle not primary power
One demo Pod with full solar treatment, document architecture for all three as solar-ready

LED AESTHETIC ITERATION

Original plan: 50-LED NeoPixel strip per Trail Pod
Considered Wireless Plasma Kit (Plasma Stick 2040 W + 50 LED string) at $74
Reconsidered LED count after power math: 50 LEDs at 30% brightness = 1.5-3W per Pod, not battery viable
Iterated down to NeoPixel Ring 16 or 12 with reduced power demand
Iterated to 10 NeoPixels with diode trick (no level shifter needed)
MAJOR REVISION: switched to flexible LED filaments
Filaments selected for: authentic bioluminescent diffuse glow, tiny power draw (0.06W per filament), curved organic shapes, retro futuristic aesthetic, multiple colors per Pod for context shifts
Multiple filament colors per Pod chosen over RGB NeoPixels: amber for evening, cool white for daytime, dim red for nighttime
Aesthetic acknowledgment: filaments fade in daylight, glow in dim/dark conditions, this is on-thesis (calm tech recedes when not needed)

BIOTRAIL POD CRYSTALLIZATION

Renamed Trail Pods to Biotrail Pods to embed bioluminescent concept in product name
Form factor decided: mushroom-shape with domed translucent cap, wooden stem, solar cell on cap top
Anatomical mapping: top of cap (solar), cap interior (LED filaments), translucent dome (glowing surface), stem (electronics housing), base (sits on shelf)
Direct biological reference: Mycena chlorophos and other bioluminescent fungi
Cybernetic-fungal metaphor: mycelium-network distributed intelligence
Designed to be "intentionally organic with retro futuristic design" for sensory-sensitive users
Glow-in-the-dark phosphorescent dome added (strontium aluminate, green to match real fungi)
Phosphor functions as material storage of light energy, released slowly when LEDs off
Phosphor demonstrates graceful degradation materially: Pod continues glowing when power lost
3D printed in glow PLA filament chosen over painted acrylic dome (uniform glow, custom shape, $38.90 for 1kg covers all 3 Pods)
Electret idea explored and rejected for LED powering: physics blocks sustained current; phosphor IS the correct version of "passive light emission" principle

SMS MODULE PATH SELECTED

Considered Path A (WiFi-mediated SMS via Twilio): easy mock, requires WiFi Module present
Considered Path B (real cellular SMS via 4G LTE modem): more architecturally correct, more expensive
Locked Path B: Waveshare SIM7600G-H 4G HAT (B) at ~$130, Aldi Mobile prepaid SIM, high-gain antenna
Physical clip-in via USB-C connection to Hub (not HAT-on-Pi) preserves the physical Module thesis
One-way design: SMS out only, never SMS in (privacy by hardware design)
Demo Day staging: Pod detects pattern → Hub sends SMS to panelist's phone in real time

ML STACK FINALIZED

Considered training real neural network from scratch, rejected as too time-intensive
Locked three-layer learning approach: adaptive baseline (pandas), decision tree classifier (scikit-learn), Edge Impulse tiny neural network for one specific task
Hailo NPU rejected: vision-focused, opaque, contradicts interpretable-learning thesis
"What the system has learned" panel on Hub display for transparent learning

SCOPE DECISIONS

Scoped IN for v1: Hub (Pi Zero 2 W + Inky Impression + radar + PIR + NeoPixel ring), Time Timer Pod (Inky Frame 4.0"), 3x Biotrail Pods, SMS Module
Scoped OUT for v1 with documentation as v2: Door Pod (piezo self-powered version), Charge and Find Pod, Watcher Pod (C1001 60GHz), UWB positioning
Acoustic Noise Pod added then deferred: documented as planned v2 if time permits
Door piezo Pod with energy harvesting documented as planned v2

ACADEMIC POSITIONING

Compiled academic reference list across cybernetics (Wiener, Ashby, Beer, von Foerster), calm tech (Weiser), adaptive architecture (Price's Generator, Negroponte), Indigenous-relational tech (Abdilla & Fitch, Indigenous Protocol AI), Actor-Network Theory (Latour), disability design (Curb-Cut Effect, Hendren, Blackwell), PDA clinical (Newson, O'Nions), CPS technical (NIST, Greer et al.), self-organising systems (Gershenson)
Drafted "Contribution to the field" paragraph: honest framing of novel synthesis rather than novel components
Drafted Biotrail Pods aesthetic description: mushroom-form bioluminescent indicators with Mycena chlorophos reference and mycelium-network metaphor
Rejected "first ever" overclaim framing in favor of "novel synthesis of established research traditions applied to this specific user population"

KEY PROCESS REFLECTIONS

Pattern of holding design discipline against scope creep while staying open to genuine improvements
Multiple decisions reversed once and then re-locked: Pi 5 → Pi Zero 2 W, 50 LEDs → 10 filaments, PowerBoost → bq25185 solar charger
Returned to original design intent in several places: power harvesting from doorways (piezo Pod concept), no central authority (advertise/scan instead of formal mesh), retro mid-century aesthetic (filaments over NeoPixels)
Cost evolution: Round 1 (Pimoroni) at $465, Round 2 estimated at $670-720, total approximately $1135-1185 (down from $1265-1335 with Pi 5)
Budget overage from $250 nominal documented openly as scope decision in build journey

The Pear-Pie Cyber-Physical Home System
Beyond the Master of Applied Cybernetics, I aim to continue my studies in the School of Cybernetics and contribute lived-experience to the development of humanitarian technologies and systems communication methodologies that practically improve the design and function of systems to more genuinely afford those who rely upon them.


Through lived and professional practice in neurodivergence and social welfare systems navigation, I gained priceless understanding of the difference between well-intentioned policy-in-theory and that same policy-in-practice.

By marrying these I wanted to develop a device that would device which would equitably bring would increase the privacy, autonomy, dignity and equitable affordance of people with disabilities in everyday life. 


and I am determined to continue in the field of Cybernetics, where I wish to contribute to the development of humanitarian technologies and system communication methodologies that help to improve the functional realities of social welfare systems and equitable access to technologies that increase the privacy, autonomy, dignity and affordance of people with disabilities.

make a difference in the lives of people who are not afforded in their environments.

methodologies to communicate intersectionally about the valuable contribution that we have to offer if we are genuinely afforded. 

the opportunity through Cybernetics to make a difference for people with disabilities and help others to understand that even if we need a bit more time and patience, we have so much knowledge and experience that we want to share. <3


- 
- 

This quote perfectly sums the necessary purpose of the cyber-physical system which I have decided to build for this project. 
I am a neurodivergent and have spent my own personal life and professional career as a psychosocial worker in the social welfare system navigation and a professional career in psychosocial work, I have a keen understand

both theory and practice by integrating the knowledge developed throughout Semester 1 of the Master of Applied Cybernetics with my professional experience in the psychosocial disability sector and lived-expertise of neurodiversity and social welfare system navigation. 

These intersecting perspectives have enabled me to understand the Australian social welfare system through multiple ontological lenses: as a student of applied cybernetics at the Australian National University, as a psychosocial practitioner working within the disability sector, as a person with lived experience of neurodivergence and as a person who has used these systems themselves.. Together, these perspectives have shaped the design of this project and informed a systems-based approach to addressing a complex real-world challenge.














# 1. Introduction

This is the final Maker Project for CYBN8001. It demonstrates the knowledge and technical skills developed across Semester 1, cross-applied with my existing professional expertise in the psychosocial disability and education sectors, and my lived expertise as a neurodivergent person navigating Australian welfare systems.

Pear-Pie is a distributed, privacy-preserving cyber-physical home system supporting participation for people with fluctuating cognitive, sensory, emotional and executive functioning demands. Modular sensor and tool pods sit throughout the home. They sense local conditions, learn patterns of activity, communicate over Bluetooth Low Energy, and provide ambient support without requiring interaction. A central hub observes patterns emerging across the pod network and adjusts the rules individual pods follow. This creates a two-level adaptive system inspired by W. Ross Ashby's homeostat.

Pear-Pie is affordable, modular, privacy-preserving, adaptive, locally controlled and low power. It survives network or hub failure, functions without cloud connectivity, and responds to individual rather than standardised patterns of behaviour.

# RED: FIGURE 1 — photograph of the full system in situ. Hub with e-ink face, pods installed, office Time Timer. Label the components.]

# 1.1 Motivation

The motivation for Pear-Pie emerged through the convergence of lived experience, professional practice, and academic study.

As a neurodivergent person and psychosocial practitioner, I repeatedly encountered the gap between policy as intended and policy as experienced. Many barriers to participation occur before people reach formal support systems, where difficulties recognising needs, communicating, organising information, or sustaining engagement can prevent access altogether.

Pear-Pie responds by intervening upstream, supporting the cognitive, sensory, communicative, and environmental conditions that make participation possible. Guided by Nardi and O'Day's (1999) concept of technology with heart, the project explores how cyber-physical systems can increase dignity, autonomy, and participation through practical, everyday support.

# 1.2 The Design Challenge

Pear-Pie did not begin with a design framework. It began as an attempt to build a cyber-physical home system from my own lived experience.

As the project evolved, I repeatedly found myself struggling to explain why the system was necessary to people who had never experienced the barriers it was designed to address. This became especially apparent during the project demonstration, where explaining the technology proved easier than communicating the lived conditions that made it necessary.

Building Pear-Pie therefore became an iterative process of designing, reflecting, and refining. As I tested ideas, I gradually recognised that I had developed my own way of moving from lived experience to system design. Looking back, I was able to reverse-engineer that process into a repeatable design framework.

The framework and Pear-Pie therefore co-evolved. The artefact generated the framework, and the framework, in turn, reshaped the artefact.

# 1.3 Scope

Pear-Pie is a working prototype. Its first- and second-order feedback loops are operational, with eight pods collectively logging more than 2.7 million sensor readings.

The third-order feedback loop and several additional pod types have been designed but not yet implemented. Throughout this project, completed functions are clearly distinguished from proposed future development.

# 2.1 What is the problem?  Unafforded People

The first design question is not What is wrong with the person? It is What opportunities for action and participation are absent from the relationship between the person and their environment?

Three complementary perspectives shape this project. The Social Model of Disability locates disability in inaccessible social, physical, and institutional environments rather than solely within individual impairment (Oliver 1990). Affordance Theory explains participation as a relationship between a person and their environment, where opportunities for action emerge through that interaction rather than existing in either alone (Gibson 1979). The Curb Cut Effect demonstrates that designing for those experiencing the greatest barriers often improves participation for many others as well (Blackwell 2017).

Together, these perspectives suggest that participation is fundamentally relational. The problem is not simply the person or the environment, but whether the relationship between them affords meaningful action.

To describe this relationship, I propose the complementary systems term unafforded people.

#### Unafforded person or people: A person, community, or group whose opportunities for participation are constrained because the affordances required for equitable engagement are absent or insufficient within their environments, technologies, institutions, or communities.

The term is not intended to replace disabled, diminish disability identity, or override the language people use for themselves. Instead, it provides a systems-oriented way of describing where participation breaks down by shifting attention from individual deficit to missing affordances. Disability is one context in which unaffordance becomes particularly visible, but every person is afforded in some environments and unafforded in others.

This shift also changes the design problem. Rather than asking how a person can better adapt to an environment, it asks how environments, technologies, and institutions can better adapt to the person.

This project argues that many supports currently provided to neurodivergent people remain fundamentally one-directional. Timers, printed schedules, reminder cards, and visual prompts can assist with specific tasks, but they cannot sense changing conditions, recognise when support is required, or adapt their behaviour. They provide support, but they do not participate in a feedback loop.

As early as 1964, Michael Arbib distinguished between passive prosthetic devices, such as a peg leg, and adaptive prostheses capable of sensing and responding through feedback (Arbib 1964). The difference was not simply technological sophistication. A peg leg provides static support regardless of changing conditions, whereas a feedback-controlled prosthesis continuously senses, adjusts, and responds to the person using it.

More than sixty years later, many supports available to neurodivergent people remain the equivalent of the peg leg. They are valuable and often essential, but they are fundamentally passive technologies. They ask the person to do the work of sensing, interpreting, remembering, adapting, and responding. The feedback loop remains inside the person rather than being shared with the technology.

Pear-Pie is designed to close that gap. Rather than providing one-directional assistance, it functions as an affordance technology: a cyber-physical system that senses, learns, and adapts to changing conditions, allowing the environment itself to participate in the feedback loop. Instead of requiring the user to continually adapt to their surroundings, the surroundings begin to adapt to them.

The term unafforded is intended as a practical systems language rather than a replacement for disability identity. Many people identify proudly as disabled, and that language remains appropriate in legislation, policy, scholarship, and personal identity. Unafforded instead provides a complementary term that shifts attention from individual deficit to the relationship between people and their environments.

In this sense, unafforded functions as a boundary object (Star & Griesemer 1989). It provides a shared language that can travel between different communities—disabled people, support workers, clinicians, policymakers, engineers, and researchers—without requiring each to abandon their own perspective. Rather than creating a single universal definition, it creates a common point of communication about where participation breaks down.

This shift in language also changes where we look for knowledge. If participation depends on relationships between people and systems, then understanding those relationships requires listening to the people who repeatedly experience them. This leads to the second principle of the framework: lived expertise as feedback.

# 2.2 How do we understand it? — The Lived Expertise Feedback Model

If unaffordance arises through relationships between people and systems, those relationships must be understood through the experiences generated within them.

Feedback is foundational to cybernetics. Systems can only learn and adapt when information about the consequences of their behaviour is returned and influences future action (Wiener 1948; Ashby 1956). Without feedback, systems cannot distinguish intended outcomes from experienced outcomes.

Human service systems typically evaluate themselves through institutional measures such as compliance, policy implementation, service utilisation, and organisational performance. These measures describe how the system operates. They rarely describe how the system is experienced by the people expected to navigate it.

Lived expertise: Situated systems knowledge developed through repeated interaction with an environment, technology, institution, community, or social system over time.

Lived expertise is more than lived experience alone. It emerges through repeated interaction with the same system, revealing recurring barriers, informal workarounds, unintended consequences, hidden dependencies, and the gap between intended and actual system behaviour.

Institutional actors understand systems through their design, governance, and intended operation. People who continually navigate those systems understand them through their effects. Both describe the same system, but each observes different forms of knowledge.

From a cybernetic perspective, lived expertise functions as an essential source of feedback. It provides information about system behaviour that institutional measures cannot observe. Rather than treating lived expertise as consultation undertaken after design, this framework positions it as a continuous feedback signal that guides where intervention is needed and how systems should adapt.

[RED: FIGURE 3 — Lived Expertise Feedback Model diagram. You have drawn this.]





This project presents the Pear-Pie Cyber-Physical Home System, a distributed, privacy-preserving home system designed to support participation for people experiencing fluctuating cognitive, sensory, and executive functioning demands. Developed as the final Maker Project for CYBN8001, the project demonstrates how applied cybernetics can be used to translate lived expertise into the design of practical cyber-physical technologies.



This thesis develops a conceptual and analytical framework for understanding participation in socio-technical systems through the lens of affordance and cybernetics. It introduces the concept of the Unafforded Person as a relational condition arising when the affordances available within a person's ecological context are insufficient to support equitable participation. Building on this concept, it proposes a methodology that interprets lived expertise as a source of systems feedback, enabling analysts to identify mismatches between institutional assumptions and real-world system behaviour and thereby reveal hidden barriers, omitted conditions, and opportunities for intervention.

This project demonstrates how lived expertise can be integrated with the theoretical foundations of applied cybernetics to analyse complex socio-technical systems and inform the design of practical interventions. Drawing together the concepts, methods, and technical capabilities developed throughout Semester 1 of the Master of Applied Cybernetics, alongside professional experience within the psychosocial disability sector and lived expertise navigating Australian social welfare systems as a neurodivergent person, the project applies systems thinking across the complete design process. This includes analysing institutional policies and service systems, identifying the relationships between intended system behaviour and lived system performance, developing conceptual and analytical frameworks, and translating those insights into a cyber-physical intervention designed to improve participation.

Rather than waiting for large-scale institutional reform, this project explores how cyber-physical technologies can create meaningful interventions from the ground up. While systemic change remains important, people continue to navigate complex systems every day. The Pear-Pie Cyber-Physical Home System therefore demonstrates how affordable, privacy-preserving, and scalable technologies can support people within existing systems by increasing environmental affordance, strengthening communication between people and institutions, and enabling more equitable participation. In doing so, the project illustrates how applied cybernetics can operate not only as a framework for analysing systems but also as a practice for designing interventions that respond directly to lived conditions.



This thesis develops a systems analysis methodology that integrates affordance theory, critical systems thinking, applied cybernetics and lived expertise. Within this framework, lived expertise is interpreted as a source of systems feedback, enabling comparison between institutional and lived system representations to identify omitted boundary conditions and upstream intervention opportunities. 



This project represents the culmination of the theoretical, technical, and practical knowledge developed throughout Semester 1 of the Master of Applied Cybernetics at the Australian National University. As the final Maker Project for CYBN8001, it demonstrates the application of applied cybernetics across the complete design process: understanding a complex socio-technical system, analysing its dynamics, developing conceptual and analytical frameworks, identifying opportunities for intervention, designing a cyber-physical system, and implementing that system through integrated hardware and software.

More than the construction of a technological artefact, this project demonstrates the practice of applied cybernetics. It brings together systems thinking, cybernetic theory, human-centred design, embedded systems engineering, machine learning, and cyber-physical systems design to explore how technology can respond to complex human problems in ways that are technically robust, socially meaningful, and ethically grounded.

The motivation for this work emerges from the convergence of lived experience, professional practice, and academic study. As a neurodivergent person, I have spent years navigating Australia's social welfare and education systems. These experiences revealed that the greatest barriers to participation are often not a person's impairment, but the complex interactions between people, environments, technologies, policies, and institutions. Through repeatedly encountering these barriers, I came to recognise lived expertise as a legitimate form of systems knowledge—knowledge that can only be acquired through practice, rather than theory alone, or by listening to those who have lived that experience.

Later, through my professional career as a psychosocial worker and educator, I encountered these same challenges from another perspective. Supporting people to navigate complex social systems highlighted the persistent gap between policy as it is intended and policy as it is experienced in practice. This reinforced my belief that understanding complex systems requires more than institutional perspectives alone; it also requires the situated knowledge of the people who live within those systems every day.

This project brings these experiences together with the theoretical foundations of applied cybernetics. Rather than beginning with technology and searching for a problem, it begins with lived experience and asks how cyber-physical systems might better support people navigating complex environments. Guided by Nardi and O'Day's (1999) vision of technologies with heart, the project explores how technology can strengthen communication between people and systems, increase environmental affordance, and support more equitable engagement with social services.

In doing so, the project proposes the Lived Expertise Conceptual Framework, comprising a conceptual terminology (Unafforded People), a cybernetic model (The Lived Expertise Feedback Model), and an analytical methodology (The Lived Expertise Systems Boundary Analysis Methodology). Together, these contributions provide a systems-based approach to understanding the gap between intended and experienced systems and inform the design of cyber-physical interventions that respond to those gaps.

More broadly, I hope this work contributes to the development of affordable, scalable, privacy-preserving technologies that expand equitable access to innovation for marginalised and low-socioeconomic communities. Meaningful technological progress should not simply increase technical capability; it should also enhance dignity, autonomy, opportunity, and inclusion.

The Pear-Pie Cyber-Physical Home System is presented as an applied demonstration of this conceptual framework. The following sections first introduce the theoretical contributions that informed its design before demonstrating how those ideas were translated into a practical cyber-physical intervention.

# 2. A Lived Expertise Framework for Designing Cyber-Physical Systems

## 2a) Conceptual Terminology: _Unafforded Person/People and Affordance Technology_

A proposed conceptual terminology that reframes disability and technology through the relationship between people, environments, institutions, and affordances.

### Why language matters

The language used to describe people and technology shapes how systems are understood and, consequently, where responsibility for change is located. Within many Western systems, disability has historically been framed through deficit-oriented language that categorises people according to what they cannot do. While the Social Model of Disability has shifted attention towards environmental barriers (Oliver 1990; Shakespeare 2018), much of the language surrounding disability, support services, and technology continues to position disability as an attribute of the individual rather than as a relationship between people and their environments.

This project proposes two complementary conceptual terms—unafforded and affordance technology—to provide a systems-oriented language for discussing participation, technology, and inclusion.

### Unafforded people

This project introduces unafforded people as a complementary systems term rather than a replacement for disabled. The intention is not to redefine disability or diminish disability identity, but to provide language that foregrounds the relationship between people and the affordances provided by their environments.

#### Definition

Unafforded (proposed conceptual terminology)
A person, community, or group whose opportunities for participation are constrained because the affordances required for equitable engagement are absent or insufficient within their environments, technologies, institutions, or communities.

Many people identify proudly as disabled, and for many the term represents identity, community, political advocacy, and empowerment. This project fully acknowledges and respects those perspectives. Accordingly, the terms disabled person and unafforded person are used interchangeably throughout this report where appropriate, with disabled retained when referring to legislation, policy, existing disability scholarship, and people's preferred identities.

The purpose of unafforded is therefore not to replace existing language, but to extend it. Rather than locating disability solely within the individual, it draws attention to the interaction between people and their environments, encouraging a shared understanding of responsibility for creating conditions that enable participation.

Importantly, this project begins from the premise that affordance is relational rather than categorical. Every person is both afforded and unafforded in different environments throughout their lives. Disability therefore represents one important context in which unaffordance becomes highly visible, but it is not the only one. By understanding affordance as a universal human condition rather than as a characteristic of a particular group, accessibility becomes a shared design objective rather than a specialised accommodation.

This relational framing extends Affordance Theory (Gibson 1979; Norman 2013) by asking not only what environments afford, but what happens when the affordances necessary for participation are systematically absent. It also builds upon the Social Model of Disability by providing conceptual language that foregrounds relationships between people, environments, institutions, technologies, and communities rather than individual deficit.

### Language, identity, and participation

Questions surrounding disability language are neither straightforward nor culturally universal. Scholars and advocates have long recognised that labels can simultaneously enable access to support while also reinforcing deficit-based understandings of people. This tension is particularly evident within many Aboriginal and Torres Strait Islander communities, where disability has often been described in relational and functional ways rather than through categorical identity labels.

Damian Griffis (First Peoples Disability Network) argues that many Aboriginal approaches focus less on defining people by disability and more on understanding what supports are required for meaningful participation within family and community. However, accessing contemporary support systems such as the National Disability Insurance Scheme often requires people to adopt deficit-oriented language and demonstrate what they cannot do in order to become eligible for assistance (Griffis 2017). The challenge is therefore not only one of service provision, but of language itself.

These perspectives resonate strongly with this project's systems approach. If participation is understood relationally rather than categorically, then the focus shifts from asking "What is wrong with this person?" towards asking "What affordances are missing from this environment?" This subtle linguistic shift changes where responsibility for intervention is located and opens new possibilities for systems design.

### Affordance Technology

This project also proposes the complementary term affordance technology.

Rather than describing technologies according to the category of people they are assumed to serve—as implied by terms such as assistive technology or disability aid—the term affordance technology foregrounds their function: increasing environmental affordance.

#### Definition

Affordance Technology (proposed conceptual terminology)
Technologies intentionally designed to increase people's opportunities for action, participation, autonomy, and interaction within their environments.

Viewed through this lens, technologies commonly regarded as disability technologies are revealed to be technologies that increase affordance for everyone. Automatic doors, ramps, subtitles, speech recognition, predictive text, GPS navigation, voice assistants, ergonomic tools, and many other everyday technologies originated from, or were significantly advanced through, efforts to improve accessibility. Today they are used widely throughout society because they increase participation, convenience, safety, and efficiency for all users.

This phenomenon reflects the Curb Cut Effect, whereby designing for people experiencing the greatest barriers frequently produces broader societal benefits. Similarly, Duvall et al. (2022) argue that inventors with disabilities represent an under-recognised source of innovation because lived experience reveals problems, opportunities, and design requirements that others may never encounter. Rather than viewing disability as a limitation on innovation, they position lived expertise as a valuable driver of technological creativity.

This principle also aligns closely with the PADE methodology, which places intended users at the centre of problem identification, analysis, design, and evaluation. When technologies are designed from lived expertise rather than retrofitted for accessibility, they are more likely to generate solutions that extend well beyond their original user group.

Accordingly, this project argues that affordance technologies should not be viewed as niche products designed for a segregated population. They represent a broader philosophy of inclusive innovation that seeks to increase participation by improving the relationship between people and their environments. Within this framing, disability becomes not a category of people requiring special technologies, but one of the richest sources of insight into how future technologies can be designed to benefit society as a whole.

Ultimately, unafforded and affordance technology provide a shared conceptual language for the remainder of this project. Together they shift attention away from individual deficit and towards the design of environments, institutions, and technologies that enable more people to participate, contribute, and flourish.


## 2b) Conceptual Model: _Lived Expertise Feedback Model_ 

A proposed cybernetic model that positions lived expertise as the feedback signal enabling inclusive systems to learn, adapt, and continually improve.

Why feedback matters

Feedback is a foundational principle of cybernetics. Whether biological, ecological, technological, or social, systems are only capable of learning and adapting when information about the consequences of their actions is returned to the system and influences future behaviour (Wiener 1948; Ashby 1956). Without effective feedback, systems cannot distinguish between intended outcomes and experienced outcomes, limiting their capacity to respond to changing conditions and improve over time.

Within contemporary human service systems, however, much of the feedback used to evaluate performance originates from institutional measures such as compliance, policy implementation, service utilisation, or organisational performance. While these measures provide valuable information about the operation of the system, they often fail to capture how those systems are actually experienced by the people who use them. Consequently, many barriers to participation remain invisible within conventional forms of evaluation.

Lived expertise as systems knowledge

This project proposes that lived expertise constitutes a distinct form of systems knowledge.

Lived expertise is not simply lived experience, nor is it equivalent to consultation or participation. Rather, it emerges through repeated interaction with the same system over time. As people continually navigate environments, technologies, institutions, and policies, they develop situated knowledge about how those systems behave in practice. This knowledge includes tacit understandings of barriers, workarounds, unintended consequences, and interactions that are often inaccessible through observation, policy analysis, or institutional data alone.

From a cybernetic perspective, lived expertise represents a unique source of feedback because it captures the difference between how a system is intended to function and how it is actually experienced. This distinction is fundamental. While designers and institutions typically understand systems from the perspective of intention, people living within those systems understand them through continual interaction. Both perspectives describe the same system, but each reveals different forms of knowledge.

The Lived Expertise Feedback Model

This project proposes a cybernetic interpretation of lived expertise that integrates principles from the Social Model of Disability (Oliver 1990; Shakespeare 2018), Affordance Theory (Gibson 1979; Norman 2013), participatory design (Sanders & Stappers 2008), and the Curb Cut Effect into a continuous learning model.

Within this model, individuals interact with environments, technologies, institutions, and communities. These interactions either increase or reduce environmental affordance. Where affordances are absent, barriers to participation emerge. Through repeated engagement with these barriers, people develop lived expertise—a distinct form of systems knowledge generated through ongoing interaction with the system itself.

When this lived expertise is intentionally incorporated into systems analysis, policy development, service design, and technological innovation, it functions as a cybernetic feedback signal. It communicates where intended system behaviour differs from experienced system behaviour, enabling designers, organisations, and institutions to identify opportunities for adaptation and redesign.

As interventions improve environmental affordance, participation increases and barriers are reduced. These changes generate new experiences, producing further feedback and allowing the system to continue learning over time. In this way, lived expertise becomes the mechanism through which socio-technical systems can continually evaluate, adapt, and improve rather than relying solely on institutional assumptions about success.

Through the Curb Cut Effect, improvements originally developed in response to significant barriers frequently extend benefits to much broader populations. Likewise, Duvall et al. (2022) argue that inventors with disabilities represent an under-recognised source of innovation because lived expertise exposes problems and opportunities that others may never encounter. Within this model, lived expertise therefore becomes not only a mechanism for improving accessibility, but also a catalyst for broader technological and social innovation.

Figure X. The Lived Expertise Feedback Model

Insert conceptual feedback loop diagram illustrating:

Environment → Interaction → Experience
Repeated interaction → Lived Expertise
Lived Expertise → Feedback
Feedback → System adaptation
Adaptation → Increased affordance
Increased affordance → Improved participation
New experiences → Continuous feedback loop
Contribution

Participatory and co-design methodologies have long recognised the importance of involving people with lived experience throughout the design process. This project extends these approaches by proposing that lived expertise should be understood not simply as a source of consultation, but as a distinct form of systems knowledge that functions as a cybernetic feedback mechanism.

By positioning lived expertise as feedback, this conceptual model reframes inclusion as a process of continuous learning rather than one-off consultation. It proposes that the most effective socio-technical systems are those capable of continually comparing intended outcomes with lived experience and adapting accordingly.

This conceptual model provides the theoretical foundation for the Lived Expertise Systems Boundary Analysis Methodology, presented in the following section, which operationalises this feedback process by comparing intended and experienced representations of the same system to identify systems gaps that would otherwise remain invisible.

## 2c) Analytical Methodology: _Lived Expertise Systems Boundary Analysis Methodology_

_The Lived Expertise Systems Boundary Analysis Methodology is a complementary systems mapping and analysis methodology that compares intended and experienced representations of the same system to identify systems gaps, hidden barriers, and intervention opportunities by expanding conventional institutional system boundaries through lived expertise._ 

Why do we need to analyse systems differently?

Institutional boundaries are often treated as precise, whereas people's lived interactions with systems occur across diffuse, overlapping, and upstream conditions. Conventional systems analysis frequently begins with the institutional definition of where a system starts and finishes. While this approach is effective for understanding organisational structures, governance, and service delivery, it can overlook the conditions that determine whether people can access, engage with, or benefit from those systems in the first place.

The Lived Expertise Systems Boundary Analysis Methodology was developed to address this limitation.

Problem: Institutional boundaries hide upstream causes.
Response: Expand the analytical boundary using lived expertise.
Method: Compare intended and experienced representations of the same system.
Output: Identify systems gaps, hidden barriers, and intervention opportunities.

Rather than replacing conventional systems analysis, this methodology complements existing approaches by recognising lived expertise as a legitimate source of systems knowledge. It proposes that understanding complex socio-technical systems sometimes requires stepping beyond institutional boundaries to examine the upstream conditions that connect people to them.

Theory
Where do you draw the system boundary?

Every systems analysis begins with a boundary judgement. Where the system boundary is drawn determines what is considered part of the system, what is excluded, which relationships are examined, whose perspectives are represented, and ultimately what conclusions can be reached.

Churchman (1970) argued that systems cannot be understood independently of the boundaries chosen by the observer. Building on this work, Ulrich's (1983) Critical Systems Heuristics and Midgley's (2000) Systemic Intervention demonstrate that system boundaries are analytical choices rather than objective realities. These boundary judgements determine which empirical observations, values, stakeholders, and causal relationships become visible, while simultaneously obscuring those that fall outside the chosen boundary.

Institutional systems frequently draw these boundaries around formal organisational responsibility. Policy, legislation, eligibility, funding, assessment, and service delivery become the focus of analysis because they define where institutions perceive their responsibility to begin and end. While these boundaries are administratively necessary, they do not necessarily reflect where the system begins for the people attempting to navigate it.

For many people, particularly those navigating complex disability and social support systems, engagement with formal services is shaped by conditions that originate well before the point of service delivery. Executive functioning, communication, transport, housing, digital access, sensory environments, previous experiences with institutions, social supports, financial stability, and countless other interacting conditions influence whether participation within the formal system is possible at all. Although these conditions often exist outside institutional responsibility, they remain part of the lived system that determines real-world outcomes.

From a critical systems perspective, restricting analysis to institutionally defined boundaries risks overlooking the upstream conditions that determine access, participation, and outcomes. Expanding the analytical boundary through lived expertise enables these otherwise invisible conditions to become visible.

This broader understanding of systems also aligns with Actor-Network Theory (Latour, 2005), which proposes that systems emerge through relationships between human and non-human actors rather than existing solely within organisations or institutions. Policies, technologies, forms, algorithms, transport systems, homes, physical environments, and everyday objects all participate in shaping people's capacity to act. Rather than treating these elements as external context, this methodology considers them integral components of the lived system.

Similarly, Tsing's (2012) critique of scalability highlights how institutional systems depend upon simplified representations that enable consistency across large organisations. These intended representations are necessary for governance, yet they inevitably simplify the diverse, relational, and locally contingent conditions through which systems are actually experienced. Consequently, institutional representations describe how a system is intended to function, while lived expertise reveals how that same system functions in practice.

The central proposition of this methodology is therefore:

Institutional systems frequently draw their boundaries around the point of service delivery, whereas lived systems begin much earlier in the upstream conditions that determine whether service engagement is possible.

### Intended and Experienced Systems

The Lived Expertise Systems Boundary Analysis Methodology compares two complementary representations of the same system.

The intended system represents how institutions describe the system. It includes policy, legislation, organisational structures, eligibility requirements, service pathways, operational processes, and intended outcomes. It reflects the assumptions embedded within the formal design of the system.

The experienced system represents how people actually encounter and navigate that same system. Rather than beginning at the point of service delivery, it includes the upstream conditions, informal relationships, environmental factors, personal circumstances, workarounds, delays, barriers, and feedback processes that shape whether participation within the institutional system is possible.

Neither representation is incorrect. They simply describe different perspectives of the same system.

The intended system explains how the institution expects the system to operate.

The experienced system explains how the system actually operates within everyday life.

The analytical value emerges through comparing these two representations.

#### (Insert Intended System Diagram here.)

Policy, legislation, organisational structures, eligibility requirements, service pathways, institutional boundaries.

#### (Insert Experienced System Diagram here.)

Upstream conditions, lived pathways, environmental influences, informal relationships, barriers, feedback loops, and conditions experienced before reaching formal services.

### Systems Gaps

Comparing intended and experienced representations reveals what this project defines as systems gaps.

A systems gap is the difference between how a system is intended to function and how it is experienced in practice.

These gaps frequently occur where institutional assumptions fail to account for upstream conditions influencing participation. They may appear when formal pathways exist but cannot realistically be accessed, when environmental barriers prevent engagement before institutional processes begin, when responsibility is distributed across multiple organisations, or when people develop informal workarounds to achieve outcomes the system was originally intended to provide.

Rather than viewing these differences as isolated service failures, the methodology interprets them as evidence that the analytical system boundary is incomplete.

Systems gaps therefore represent opportunities for further systems inquiry rather than simply identifying operational problems.

#### The Lived Expertise Systems Boundary Analysis Methodology

The methodology consists of five iterative stages:

1. Map the intended system by documenting institutional structures, policies, actors, responsibilities, service pathways, and intended outcomes.
2. Map the experienced system by documenting lived pathways, upstream conditions, informal relationships, barriers, workarounds, environmental influences, and feedback encountered through lived experience.
3. Expand the analytical system boundary by identifying conditions influencing participation that exist beyond institutional responsibility but materially affect system behaviour.
4. Compare intended and experienced representations to identify systems gaps between institutional assumptions and lived reality.
5. Identify intervention opportunities by analysing where changes to technologies, environments, communication, policy, services, relationships, or system design may reduce identified systems gaps.

This methodology does not replace conventional systems analysis. Instead, it extends existing approaches by incorporating lived expertise into the process of systems inquiry. By expanding analytical boundaries beyond institutional definitions and comparing intended and experienced representations of the same system, it reveals hidden barriers, upstream causal relationships, and intervention opportunities that remain obscured within conventional top-down analyses.


# (Insert intended system diagram here.)(policy, service pathways, official processes)
# (Insert experienced system diagram here.)what people actually have to navigate).


# 3. Applying the Lived Expertise Conceptual Framework
Existing participatory and systems approaches seek to understand lived experience as one perspective within a system. This project instead proposes that lived expertise constitutes a distinct form of systems knowledge. By comparing intended and experienced representations of the same system, the Lived Expertise Systems Analysis Methodology identifies systems gaps that remain invisible from institutional perspectives alone. These gaps become the feedback through which systems can learn, adapt, and improve.


- building empthy
- 
# Case Study: NDIS Top-down model vs Bottom-up Model

# Gap Analysis

# Design Opportunity

# Pear Pie Cyber-Physical Home System

# Technical Implementation



# WHAT is it:  A general overview.
The Pear Pie is a cyber-physical system that reimagines what a smart home system of the future could be like and who it could be designed for.
It is a low-cost, scalable, high-privacy and ultra-low power distributed network of pods with edge machine learning capability.\
These pods are equipped with RADAR sensors, microcontrollers and are divided into two catergories of pods; sensor pods and tool pods. \
Sensor pods primary function is to learn and respond to movement in the environment.\
Tool pods are capable of performing a miriad of functions such as reading vital signs and sleep tracking (Vital Pods).\
The pods also have a centralised hub which analyses the emergent patterns across the distributed network of pods, which help to learn and predict the movements of the user in the space, sending weighted recommendations back to each pod and displaying the patterns of behaviour of the user in the home on the main hub display. \

# WHAT questions it explores: The applied theory.
This project proposes a cybernetic interpretation of lived expertise as a feedback mechanism connecting the Social Model of Disability, Affordance Theory, participatory design, and the Curb Cut Effect. Repeated interaction with environmental barriers generates situated knowledge that is difficult to obtain through observation alone. I propose this as a conceptual cybernetic model that synthesises these existing theories and explains how lived expertise functions as a feedback mechanism within inclusive design.

<img width="10080" height="3555" alt="image" src="https://github.com/user-attachments/assets/91cb47f8-d5df-4532-b401-bd7cf42e80b7" />

QUESTION 1: What if we designed a technology for all people but use a neurodivergent person as the primary user case. What curb cut advantages could come to fruition?\

THEORETICAL BASIS:\ 
1. Affordance Theory\
_Definition:_ People are afforded and unafforded by their environment and technology design. I posit that there is untapped expertise in people whose experiences are not afforded naturally by our environment and current technologies.
In this case, I am focusing on the experience of neurodivergent people.

2. The Social Model of Disability\ 
_Definition:_ Closely tied to this, is the social model of disability which tells us that the individual is disabled by their environment and inaccommodations that exist within it.

3. Curb Cut Theory\ 
_Definition:_ When technologies are designed for/by disabled users, it creates opportunities for others that may not have otherwise been obvious. For example, the sensor door among others, which many people do not realise are actually invented by and for disabled people but also benefit others in wider society. 
Therefore, what greater efficiencies and streamlining can be made by respecting the contributions og those with minority expertise in unaffordance in the environment. 

4. Technological Use/Function Bias\
_Definition:_ Who do we see as a valid user of a technology/innovation.

5. Information Ecologies and technology with heart.\
_Definition:_ By designing a piece of technology

6. Accessability to Security, Privacy and Information Sovereignty\
_Definition:_

7. 


- # WHO is it for:
-
- Designed to be low-cost, scalable, high-privacy and ultra-low power, utilising RADAR sensing and edge machine learning technologies.


Policy in practice - the gap between the lived experience of system navigation and the well-intended policies and social systems and uphold/reinforce them.


In the book Information Ecologies, Nardi and O'Day (1993) reflect upon the important of technology The heart of this project lies  *practice* roots of my career as a psychosocial disability worker and lived-expertise as a neurodivergent person with Autism and ADHD. 
This project brings together two complementary forms of knowledge: *practice*, grounded in my lived experience as a neurodivergent person and my career in the psychosocial disability sector, and *theory*, developed through the Master of Applied Cybernetics.


Night and O'day Information Ecologies and Metropolis the 'heart of the technology'
Not for us without us  - get quote
Lived-expertise design
- my experience = 'practice' (lived-expertise in neurodivergence, professional career for over a decade in psychosocial sector, building devices to help my clients with practical problems)
- applied cybernetics masters = 'theory'. I see cybernetics losely as the theory of practice. plus other theoretical studies i have undertaken related to them.




# WHY is it needed: The problem.
*'If you've met one person with Autism, you've met one person with Autism'*  
~ A common phrase in the Autistic community.


## 1 Pervasive Interconnected System Challenges of the Neurodivergent Person.
The beauty and challenge of being neurodivergent is that the combination of skills, challenges and affordance requirements we each possess, are unique.

This is to say that the effective affordance of neurodivergent people *must* also be individualised to be effective.
For example, appropriate communication affordance for one person may be a physical aid with large buttons and for another person, like myself, the best communication aid is predictable format such as an email instead of verbal conversations.\ This is also before introducing the complexities of being multiply-neurodivergent.

Due to the psychosocial nature of neurodivergence, many of the challenges we have personally and the barriers that we face are invisible, hence being called an *'hiddden disability'*.
these skills and challenges have pervasive interconnected implications across every avenue of our lives. Not helped by miseducation and stigma across politics, society and economics.

The unique and often paradoxical combination of needs and challenges we face, can lead to confusion, disbelief and even the slowed diagnosis of certain cohorts of neurodivergent people. 

In the following diagrams, I provide a lived-experience impression of the invisible complexity and reinforcing feedback loops faced by a person with their own unique presentation of AuDHD and the interconnected systems that these invisible challenges pervasively impact and vice versa.\

Diagram A will show the internal experience and layers of external system relationships, overlayed onto an ecological systems map.

Following this, 
Diagram B will give the reader the chance to have their very own rapid #*Choose-your-own-unafforded-adventure*!\
Where you will be able to face the trials and tribulations of attempting to gain welfare system support as a person who is neurodivergent. 

The importance of reading through these diagrams carefully cannot be understated, as many of the design features and choices may seem non-sensical to a person without lived-understanding of neurodivergence. 
Without providing you with an explicit explanation and sense of the scope, complexity and strain that invisible disability places on a neurodivergent person, the gravity of the solutions that the Pear Pie provide are not able to be seen or fully appreciated for the potential positive impact they may have on the life of a person who has had to survive without these afforance requirements being met. 



    * internal system
    * personal external system
    * interpersonal systems
    * wider welfare system
    * wider employment systems
    * national systems (economic losses of potential)

    


Colonial roots of technological function:
Mass production design:

(designed for mass consumption, optimisation and productivity
s our society continues to technologically evolve, we are headed in the direction of power and wealth concentration, this naturally includes the concentration of access to technologies, innovations and 

The evolution of technocratic society, wealth inequality we can help people to live better lives and work to minimise the painful inaffordances and catch-22 barriers created by the lived realities of even well-intentioned social welfare system design.

# WHY is it needed: The GOAL!
To design a cyber-physical system that functions on a grass-roots level to practically intervene in the cycle of to practically address the interconnected system challenges faced by neurodivergent people. 

Practically assisting the individual to overcome the catch-22 barriers that exist in our current welfare systems such as the NDIS, DSP and Aged Care Systems. increasing agency, autonomy and quality of life.

at a grassroots level, overcome catch-22 access barriers to welfare systems such as the NDIS.

agency, autonomy and quality of life for neurodivergent people by building a cyber-physical system that practically addresses the daily challenges and catch-22 barriers that interconnect across sytems  invent a cyber-physical system that practically addresses the catch-22 barriers and daily challenges that neurodivergent people face every day. 

neurodivergent people increases the autonomy and dignity of neurodivergent people practically addresses the multi-dimensional, catch-22 barriers faced by neurodivergent people everyday in their personal and professional lives and attempts to access and engage with welfare systems. 

, which prevent neurodivergent people from receiving necessary care and therefore access to an equitable quality of life. 

high-tech components and bespoke technological design, cost effectively to people who are otherwise exclude by capacity, funds or slow-moving systems of governance. , that aims to find a practical, grass roots way to assist low socioeconomic and unafforded(disabled) people



# WHO is it for:
  # The system in question.
The Pear Pie has been designed for neurodivergent community members as priority users.
As the system was developed by and for a person with lived-experience of neurodivergence, it has been developed specifically for an individual with Autism, ADHD and a Personal Drive for Autonomy profile. 
Additionally, the function of the device is well suited to individuals experiencing challenges with interrelated brain functions such people with Alzheimer's, Traumatic Brain Injury as well as Developmental Topolographical Disorientation (Kaiko et. al, 2026).

Tdemonstrates the untapped innovation potential of designing with affordance of marginalised community members, in this case neurodivergent people, as priority. 

The Pear Pie is an  that utulises the Cybernetic Wheel principles of SARS (Safe, Affordable, Responsible, Sustainable) (Okai-Ugbaje, S. (forthcoming)) and the PADE methodology (Duval et al, 2022) by including the intended user throughout the design process. 



# WHY is it needed:


# Acknowledgement 
The kindness, encouragement, and generosity I have experienced within the School of Cybernetics have been deeply meaningful. As a neurodivergent student navigating an academic system that is not always designed to accommodate autistic ways of learning, I have been fortunate to study in a community that has consistently demonstrated patience, curiosity, and a genuine commitment to inclusion.

Meaningful inclusion of neurodivergent people remains uncommon, particularly in ways that provide the time, space, and trust needed for people to contribute at their best. It is my hope that this project contributes, in some small way, to amplifying neurodivergent perspectives within applied cybernetics and the broader discourse surrounding humanitarian engineering and systems design.

I would like to sincerely thank the teaching staff who have shaped my thinking throughout this semester:

Dr Tom Biedermann – for encouraging imaginative thinking, futurism, and the confidence to think beyond conventional boundaries.
Dr Safiya Noble – for introducing me to humanitarian engineering and continually emphasising the importance of privacy, security, and human dignity in technical systems.
Dr Ash Lenton– for introducing the Sensorium and inspiring my exploration of calming technologies.
Gabby – for her guidance in machine learning and programming, her generosity in supporting me when I was unable to communicate, and for being an inspiring role model for women in technical fields.
Songyuen – for broadening my understanding of emergent systems and machine learning.
Andrew Meares – for generous conversations about neurodivergence and for sharing valuable resources on communication.
Kathrin – for encouraging my interest in improving communication within autism systems and for helping me appreciate the lineage of thinkers and practitioners whose work has brought us here.
Jessamy – for introducing me to feminist engineering and actor-network theory.
Paul – for encouraging critical thinking and reminding me to be unapologetically myself.

Thank you to my fellow students—Katrina, Sam, Muhammad, Kane, Yeu, Grace, Jim, Gareth, Jules, and Dennis—for your friendship, encouragement, advice, and willingness to share your knowledge throughout the semester. I am also grateful to senior student Sui Jackson for his generosity with time, technical knowledge, and practical support.

Finally, I would like to thank my family. Mum, thank you for the late-night Monday soup that kept me going. Dad, thank you for sharing your technical knowledge and practical skills. And to Barnabas, thank you for reminding me to rest, for your unwavering emotional support, and for believing in me even when I struggled to believe in myself.

To everyone who has shared their expertise, time, encouragement, and passion for cybernetics—thank you. Your generosity has inspired me to continue pursuing applied cybernetics and to contribute my own lived experience of neurodiversity and systems navigation to this emerging field.


# Definition of Key Terms
Affordance Theory:
The relationship between a person's capabilities and the opportunities for action provided by their environment.
Curb Cut Effect:
Designing for accessibility often benefits everyone.
Capability Approach:
Focuses on what people are genuinely able to do, rather than the services or resources available to them.
Distributed Cognition:
Cognition is shared across people, technologies, and environments, not confined to the individual.
Social Model of Disability:
Disability arises through the interaction between people and environments that are not designed to accommodate diverse needs.


# Methodological Underpinnings
PADE Model:
Structured the project's problem identification, analysis, design, and evaluation.
Cybernetic Wheel:
Guided iterative learning through observation, feedback, and adaptation.
Double Diamond:
Supported an iterative process of discovering, defining, developing, and delivering the solution.





Rather than intervening in the navigation of social welfare systems themselves, the Pear-Pie Cyber-Physical Home System intervenes further upstream by supporting the sensory, cognitive, and emotional conditions that enable engagement to occur. It recognises that before a person can navigate complex systems, they must first have the capacity to participate in them.

# WHERE is it used:
# HOW does it work:
# WHAT hardware:

# WHAT software:





