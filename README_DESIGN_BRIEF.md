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

| # | Function | Order | Status |
|---|----------|-------|--------|
| 1 | Presence sensing via mmWave radar (existence, not identity) | First | ✅ Fulfilled |
| 2 | On-pod adaptive baseline learning (EWMA, unsupervised, on-device) | First | ✅ Fulfilled |
| 3 | Ambient LED light response with emergent room-to-room trail | First | ✅ Fulfilled |
| 4 | BLE advertise-and-scan broadcast (no pairing, no central authority) | First | ✅ Fulfilled |
| 5 | Time Timer tool pod with learned session duration and persistent memory | First | ✅ Fulfilled |
| 6 | Hub event logging with single shared timebase (2.7M+ readings) | Second | ✅ Fulfilled |
| 7 | Second-order parameter control (hub retunes pod alpha and threshold) | Second | ✅ Fulfilled |
| 8 | Next-room prediction via decision tree, wired into pod pre-warming | Second | ✅ Fulfilled |
| 9 | Calm e-ink status face (10-minute refresh, no demands) | Second | ✅ Fulfilled |
| 10 | Live projected pattern map with second-order activity overlay | Second | ✅ Fulfilled |
| 11 | Graceful degradation (pods run autonomously without hub) | First | ✅ Fulfilled |
| 12 | RSSI capture as coarse proximity signal | Second | 🟡 Partly fulfilled — logged with every reading, not yet used in the model |
| 13 | Vitals sensing (respiration, heart rate, sleep) via C1001 60GHz radar | First | 🟡 Partly fulfilled — sensor read, accuracy unreliable, deferred |
| 14 | Third-order loop: system regulates its own fit to the person | Third | 🔵 Desired |
| 15 | Neural network tier for richer pattern recognition | Third | 🔵 Desired |
| 16 | RSSI fusion for within-room localisation | Third | 🔵 Desired |
| 17 | Simplex (outbound-only) SMS alert channel | Second | 🔵 Desired |
| 18 | RTC module for off-grid wall-clock time | Second | 🔵 Desired |
| 19 | Object-find: BLE beacons, LED throwies, Anchor Pod | First | 🔵 Desired |
| 20 | Sensor fusion: PIR fast-wake paired with mmWave stillness detection | First | 🔵 Desired |
| 21 | Encrypted BLE and formal threat modelling | Second | 🔵 Desired |
| 22 | Modular clip-on capability expansion (physical agency over functions) | First | 🔵 Desired |
| 23 | Home Assistant or third-party smart home integration | — | ⚪ Out of scope |
| 24 | Cloud connectivity, remote access, companion app | — | ⚪ Out of scope |
| 25 | Cameras, microphones, Wi-Fi | — | ⚪ Out of scope (deliberate exclusion, privacy by design) |
| 26 | Medical diagnosis or clinical monitoring | — | ⚪ Out of scope |
| 27 | Multi-occupant identification or person tracking | — | ⚪ Out of scope (senses existence, not identity) |














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
