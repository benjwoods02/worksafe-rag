# Generation quality — labelling sheet

Fill in the `yaml` block under each answer. Then run:

    python score_answers.py

## Label definitions

| Field | Values | Meaning |
|---|---|---|
| `grounded` | `yes` / `partial` / `no` | Is EVERY factual claim supported by the cited sources? One unsupported claim makes it `partial`. |
| `citations` | `valid` / `some_invalid` | Does each citation point to a source that actually supports the claim attached to it? |
| `modality` | `correct` / `wrong` / `na` | WorkSafe defines "must" as a legal requirement and "should" as recommended practice. Did the answer preserve the distinction? `na` if neither appears. |
| `complete` | `yes` / `missing` / `na` | Does it capture the qualifications a duty holder would need? `missing` if it omits an exception, condition or duty that changes what someone should do. |
| `refusal` | `correct` / `over_refused` / `failed` / `na` | Unanswerable questions: did it decline? `over_refused` = declined when the answer was there. `na` for answerable questions it answered. |

Leave a field blank to skip it. `notes` is free text.

---

## 1. `c001` [conceptual]

**Q:** if I am encapsulating asbestos rather than removing it, what category of work is that

### Answer

According to the sources provided, encapsulating asbestos is classified as **asbestos-related work**, not asbestos removal work.

[1] states that "asbestos-related work is any work involving asbestos permitted under regulation 7 that is not asbestos removal work" and specifically lists "rectifying work to ACM (for example, encapsulation)" as an example of asbestos-related work.

Additionally, [2] notes that "asbestos-related work is work involving asbestos other than asbestos removal."

The key distinction is that [4] defines removal work as "the complete removal or replacement of asbestos, ACM or asbestos-contaminated dust or debris," whereas encapsulation involves sealing or protecting the asbestos in place rather than removing it.

### Sources given to the model

**[1]** `72527-00131` — Interpretive guidelines – The Health and Safety at Work (Asbestos) Regulations 2016, p.84  
> 11.0 What is asbestos-related work? What are examples of asbestos-related work? Asbestos-related work is any work involving asbestos permitted under regulation 7 (Section 3 of these guidelines) that is not asbestos removal work. Examples include: – maintenance and servicing work involving ACM – rectifying work to ACM (for example, encapsulation). Table 25 provides examples of the activities that a

**[2]** `72529-00032` — Asbestos assessments, p.25  
> or near a public area. For more information see Section 5.1 When sampling might be needed for Class B or unlicensed removal ASSURANCE FOR ASBESTOS-RELATED WORK AND AFTER SURVEY SAMPLING Asbestos-related work is work involving asbestos other than asbestos removal. It includes work that may involve the disturbance of asbestos – for example drilling into a soffit to install a light or installing duct

**[3]** `8-00082` — ACOP: Management and removal of asbestos, p.64  
> and cements. There is little opportunity for asbestos fibres to become airborne unless the matrix is damaged. Encapsulation helps protect the asbestos from mechanical damage, increases the length of the product’s serviceability and may also be used to prevent the release of airborne asbestos during its removal. Workers encapsulating asbestos should: > > be trained and experienced in working with a

**[4]** `72533-00010` — Working with or near asbestos, p.10  
> part of a structure, or that is loadbearing or otherwise related to the physical integrity of the structure. Removal work means the complete removal or replacement of asbestos, ACM or asbestos-contaminated dust or debris, regardless of the quantity or whether it is friable or non-friable. Before a building can be refurbished or demolished all asbestos must be positively identified, removed, and th

**[5]** `8-00081` — ACOP: Management and removal of asbestos, p.64  
> APPROVED CODE OF PRACTICE // MANAGEMENT AND REMOVAL OF ASBESTOS 62 Example of enclosing asbestos as a control measure: A large dockside warehouse used for temporarily storing grain and stockfeed has walls made from various materials, including asbestos cement sheets. Apart from the driver of a large front-end loader that goes into the warehouse to load or unload the feed, there are no other worker

**[6]** `68244-00080` — Managing asbestos in your building or workplace – for PCBUs, p.54  
> is not reasonably practicable or cannot be done immediately. Asbestos material that has been encapsulated needs to be checked regularly for signs of deterioration or damage. If there is any sign of damage or disturbance to the asbestos material, you should arrange for: – urgent repair (for example, reapplication of the encapsulant), or – another control measure to be used (for example, asbestos re

```yaml
id: c001
grounded: yes
citations: valid
modality: na
complete: yes
drift: none
refusal: na
human:
notes: quotes [1] p84 verbatim and correctly distinguishes encapsulation (asbestos-related work) from removal. verified
```

---

## 2. `c002` [conceptual]

**Q:** what information must be reachable within ten seconds for someone handling a gas cylinder

### Answer

According to the sources provided, **secondary identifiers** are the information that must be available within ten seconds to any person handling a cylinder [1].

Secondary identifiers consist of:

a. "an indication of the degree of hazard and other risks associated with the gas" [1]

b. Information on "how to prevent and manage those risks" [1]

This information is "normally in the form of hazard/warning and precautionary statements and/or risk phrases" and includes [1]:

- An indication of the general degree of hazard (e.g. 'highly flammable gas', 'flammable', 'fatal/toxic', 'very ecotoxic')
- An indication of the circumstances in which the gas may adversely behave (e.g. 'heat', 'open flames', 'if inhaled', 'aquatic environment')
- An indication of the steps to be taken to prevent unintentional ignition/combustion/inhalation/release

### Sources given to the model

**[1]** `20566-00060` — Guide to gas cylinders, p.40  
> 4.0 Marking and labelling What are the secondary identifiers? A secondary identifier is information that must be available within ten seconds to any person handling the cylinder, and consists of an indication of the degree of hazard and other risks associated with the gas. It must also include information on how to prevent and manage those risks. This is normally in the form of hazard/warning and 

**[2]** `20566-00059` — Guide to gas cylinders, p.39  
> are correctly labelled as to the cylinder’s contents. What are the priority identifiers? Priority identifiers are information that must be available to any person handling the cylinder. It must consist of an indication of the type of hazard that exists, normally in the form of signal words, including a description of the type of hazard and/or pictograms (which may have a description of the hazard)

**[3]** `20566-00088` — Guide to gas cylinders, p.55  
> 6.0 Handling and storage What are the requirements for handling cylinders? General Highly hazardous gases must be under the control of a certified handler. The handler must be present and available in the workplace or the area where the gases are stored and handled unless the gases are secured against unauthorised access. Also, a person must not possess a gaseous fumigant unless they hold a contro

**[4]** `20566-00090` — Guide to gas cylinders, p.56  
> 6.0 Handling and storage What are the requirements for storing cylinders? Gases that must be secured Some gases must be secured so that only workers who are permitted will have access to the cylinders. The Hazardous Substances Calculator can be used to find out any restrictions that apply to particular gases. General storage requirements Irrespective of the type of gas or the quantity stored, gas 

**[5]** `20566-00002` — Guide to gas cylinders, p.3  
> KEY POINTS – Improper handling of gases under pressure may cause injury, death or ill health to a person due to the pressure of their containers. – Cylinders, including cryogenic containers and fire extinguishers (but not aerosol dispensers) must be approved before being filled in New Zealand. – Every cylinder and its contents must be clearly identified. – Cylinders must be handled and stored care

**[6]** `20566-00086` — Guide to gas cylinders, p.54  
> 6.0 Handling and storage Why must cylinders be handled and stored carefully? The contents of a cylinder store the energy that has gone into compressing them, and if the cylinder is weakened, this mechanical energy may be released violently. Some gases store a considerable amount of chemical energy, and may react chemically with the environment. In either case the chemical energy will augment the m

```yaml
id: c002
grounded: yes
citations: valid
modality: correct
complete: yes
drift: none
refusal: na
human:
notes: correctly discriminates SECONDARY identifiers (ten seconds) from PRIORITY identifiers in [2]. verified against [1] p40
```

---

## 3. `c003` [conceptual]

**Q:** a lagged pipe has burst unexpectedly, can asbestos removal start straight away

### Answer

Yes, asbestos removal can start straight away if a lagged pipe has burst unexpectedly.

This is one of the limited circumstances where removal work may start immediately. According to the sources: "a sudden, unexpected event (such as equipment failure, fire, or flood) that may expose people to respirable asbestos fibres, or creates a risk of exposure (such as a burst pipe lagged with asbestos)" [1][2][3]

However, the licensed asbestos removalist must follow specific notification requirements:

- "Must immediately notify WorkSafe by telephone and in writing within 24 hours after the verbal notice was provided" [1]
- Notify WorkSafe at the email address asbestos@worksafe.govt.nz [1][3]
- "The notification should contain sufficient detail so WorkSafe can verify the circumstances specified above have been met" [3]

Note: WorkSafe does not accept lack of planning, resourcing challenges, or commercial factors as reasons for not meeting the usual notification requirements [3].

### Sources given to the model

**[1]** `72531-00050` — Asbestos removal, p.41  
> 7.0 Asbestos removal control plan (ARCP) Limited circumstances where removal work may start immediately Removal work may start immediately in either of these limited circumstances: – a sudden, unexpected event (such as equipment failure, fire, or flood) that may expose people to respirable asbestos fibres, or creates a risk of exposure (such as a burst pipe lagged with asbestos) – an unexpected br

**[2]** `8-00231` — ACOP: Management and removal of asbestos, p.171  
> START IMMEDIATELY Removal work may start immediately in the following limited circumstances: > > a sudden unexpected event that may lead to a situation where there is a risk of exposure, for example a burst pipe lagged with asbestos, or > > an unexpected breakdown of an essential service that needs immediate rectification, for example gas, water, sewage or telecommunications services. If this is t

**[3]** `72527-00073` — Interpretive guidelines – The Health and Safety at Work (Asbestos) Regulations 2016, p.50  
> 8.0 What are the duties for licensed asbestos removal? THERE ARE LIMITED CIRCUMSTANCES WHERE REMOVAL WORK MAY START IMMEDIATELY Removal work may start immediately in either of these circumstances: – a sudden, unexpected event (such as equipment failure, fire, or flood) that may expose people to respirable asbestos fibres (such as a burst pipe lagged with asbestos) – an unexpected breakdown of an e

**[4]** `8-00230` — ACOP: Management and removal of asbestos, p.171  
> 169 SECTION 26.0 // DUTIES FOR LICENSED ASBESTOS REMOVAL WORK 1. the name, licence number, and business contact details of the licensed asbestos removalist 2. the name and business contact details of the supervisor or supervisors of the licensed asbestos removal work 3. the name of the competent person or licensed asbestos assessor engaged to carry out a clearance inspection and issue a clearance 

**[5]** `72533-00029` — Working with or near asbestos, p.24  
> normal rather than follow the further steps below. But be wary, sometimes asbestos can pop up in unexpected places. Have a plan, and the right equipment available, in case of an unexpected discovery. See Section 4.6 below for details. If you or your workers uncover or damage previously unidentified asbestos or ACM after the work has started Following the above steps should make sure you are aware 

**[6]** `72533-00063` — Working with or near asbestos, p.49  
> agreed schedule worked and no unexpected asbestos was disturbed. Scenario two: demonstrating safe work practices Plumber Kev installs new hot water cylinder with pipes going through cement sheeting Kev, an Oamaru plumber, is installing a new vented hot water cylinder in a house. Kev confirms that the old hot water cylinder and asbestos lagging round its pipes and joins has been safely removed by a

```yaml
id: c003
grounded: yes
citations: valid
modality: correct
complete: yes
drift: none
refusal: na
human: agree
notes: HUMAN VERIFIED by Ben - the source does contain 'Must immediately notify WorkSafe by telephone and in writing within 24 hours after the verbal notice was provided' and the asbestos@worksafe.govt.nz address. My uncertainty was an artifact of the 400-char excerpt, not a model error. Label unchanged.
```

---

## 4. `c004` [conceptual]

**Q:** when must air monitoring be carried out for airborne asbestos

### Answer

# When Air Monitoring Must Be Carried Out for Airborne Asbestos

The requirements differ by type of work:

## Class A Licensed Asbestos Removal

Air monitoring must be done: [3][4]

- **Immediately before** Class A asbestos removal work starts, if "the licensed asbestos assessor determines that the air may contain respirable asbestos fibres in concentrations greater than trace levels" [4]
- **During** Class A asbestos removal work and "in a place that is adjacent to any negative pressure enclosure" [4]
- "While asbestos work is being carried out means continuously (every day for the entirety of the asbestos removal shift duration) until the removal is complete and clearance inspection commences" [4]
- **During Stage 3** of the clearance inspection "unless no enclosure is in place and Stage 3 is not feasible" [3]

## Class B Asbestos Removal and Unlicensed Asbestos Removal

Air monitoring is **not required**, but may be carried out "to check if the asbestos removalist is complying with their duty to eliminate or minimise exposure to airborne asbestos" and "not exceeding the airborne contamination standard for asbestos." Air monitoring should also be considered if work is being done "in, or next to a public location." [3][6]

## Asbestos-Related Work (Other Than Removal)

Monitoring must be carried out "if there is uncertainty about whether the airborne contamination standard for asbestos is likely to be exceeded." [6]

### Sources given to the model

**[1]** `72527-00074` — Interpretive guidelines – The Health and Safety at Work (Asbestos) Regulations 2016, p.50  
> on assessor independence and conflicts of interest, see Section 8.3.3 of these guidelines. When must air monitoring occur? Air monitoring must be carried out at the asbestos removal area and in any place adjacent to any negative pressure enclosure immediately before the removal work start if the asbestos assessor determines that it is likely that the air contains respirable asbestos fibres greater

**[2]** `72527-00143` — Interpretive guidelines – The Health and Safety at Work (Asbestos) Regulations 2016, p.90  
> 12.0 What are the duties for asbestos-related work? Carrying out air monitoring if there is uncertainty as to whether the asbestos airborne containment standard is likely to be exceeded Regulation 51: Duty to carry out air monitoring Air monitoring must take place if there is uncertainty about whether the airborne contamination standard for asbestos is likely to be exceeded. The airborne contamina

**[3]** `72531-00098` — Asbestos removal, p.76  
> 10.0 Air monitoring When is air monitoring required? Air monitoring is required in certain situations, as shown in Table 18. FOR CLASS A LICENSED ASBESTOS REMOVAL WORK FOR CLASS B ASBESTOS REMOVAL AND UNLICENSED ASBESTOS REMOVAL Air monitoring must be done: – immediately before Class A asbestos removal work starts (if the licensed asbestos assessor determines it is likely the air contains respirab

**[4]** `72529-00031` — Asbestos assessments, p.25  
> 4.0 Air monitoring requirements for asbestos removal and related work Air monitoring is an essential element in managing the risk of asbestos exposure during and after asbestos removal. Purpose of air monitoring Air monitoring during and after asbestos removal detects respirable fibres and measures how many are present. This information is used to assess if control measures are working during remo

**[5]** `72531-00097` — Asbestos removal, p.75  
> 10.0 Air monitoring Use air monitoring to measure airborne asbestos levels to help check if control measures a working effectively. What is air monitoring? Air monitoring is a process of measuring the concentration of airborne asbestos fibres to evaluate the effectiveness of asbestos removal control measures. The purpose of air monitoring is to show: – that control measures (such as wet stripping)

**[6]** `8-00280` — ACOP: Management and removal of asbestos, p.203  
> 201 SECTION 30.0 // AIR MONITORING AND SAMPLING ACTION LEVEL CONTROL ACTION 5. Conduct further air monitoring Do not re-start until fibre levels are at or below 0.01 fibres/ml 6. Retain records for five years Class A asbestos removal air monitoring action levels Any information gathered from these actions should be referred to during future asbestos jobs (where applicable). 30.3.2 CLASS B ASBEST

```yaml
id: c004
grounded: yes
citations: valid
modality: correct
complete: yes
drift: none
refusal: na
human: agree
notes: HUMAN VERIFIED (Ben): not a misattribution - the same text appears in BOTH sources. My flag was an artifact of the 400-char excerpt. Label unchanged.
```

---

## 5. `c005` [conceptual]

**Q:** do workers doing ongoing asbestos removal need health monitoring

### Answer

Yes, workers doing ongoing asbestos removal need health monitoring. [1][3]

Specifically, health monitoring is required for workers carrying out unlicensed asbestos removal work who are at risk of exposure to asbestos. [1] More broadly, workers must get health monitoring if they are at risk of asbestos exposure when doing "any other ongoing asbestos-related work or unlicensed asbestos removal where there is a risk of airborne asbestos exposure." [3]

**What the health monitoring must include:**

Unless another type of monitoring is recommended by a medical practitioner, the health monitoring must include: [1]
- consideration of the worker's demographic, medical, and occupational history and records of the worker's personal exposure to asbestos
- a physical examination of the worker

**Timing:**

For licensed asbestos removal workers, an initial full asbestos medical must occur within four weeks of the worker starting asbestos removal work, and then a full asbestos medical every two years thereafter. [6]

**Who is responsible:**

The PCBU (Person Conducting a Business or Undertaking) engaging the workers to conduct asbestos removal work has the duty to provide health monitoring. [3]

### Sources given to the model

**[1]** `72527-00118` — Interpretive guidelines – The Health and Safety at Work (Asbestos) Regulations 2016, p.75  
> 9.0 What are the duties for unlicensed asbestos removal? When is monitoring required (Asbestos Regulations)? A PCBU must ensure health monitoring is provided to its workers who are carrying out ongoing asbestos removal work and are at risk of exposure to asbestos when carrying out the work. What must the health monitoring involve (Asbestos Regulations)? Unless another type of monitoring is recomme

**[2]** `8-00147` — ACOP: Management and removal of asbestos, p.107  
> 105 SECTION 16.0 // HEALTH MONITORING > > licensed asbestos assessor work > > workers carrying out other ongoing asbestos-related work or unlicensed asbestos removal work and are at risk of exposure to airborne asbestos when doing that work. 16.2.1 SELF-EMPLOYED AND HEALTH MONITORING If any of the people referred to in section 16.2 of this code are self-employed PCBUs, they should monitor their ow

**[3]** `72531-00208` — Asbestos removal, p.148  
> 18.0 Health monitoring Health monitoring looks at whether a worker’s health is being harmed because of what they are being exposed to while working. Purpose of health monitoring Health monitoring can be used to detect if workers are experiencing health effects from potential exposures. Asbestos-related diseases take years to appear, but doctors can run tests to monitor the health of people who wor

**[4]** `68244-00093` — Managing asbestos in your building or workplace – for PCBUs, p.62  
> 8.0 Monitor your control measures The duty to provide health monitoring is shared between relevant PCBUs. You may not be providing health monitoring to workers, but you must check that health monitoring is being provided to workers by another PCBU. What health monitoring requirements do you need to check? Before you have work involving asbestos carried out at your building or workplace, you must c

**[5]** `20227-00042` — General risk and workplace management - part 1, p.31  
> 6.0 Health monitoring In addition, there may be other monitoring requirements under other health and safety regulations. See our guidance Exposure monitoring and health monitoring – guidance for businesses (Appendix 6) for information about other monitoring requirements (for example, for health monitoring for work involving asbestos under the Health and Safety at Work (Asbestos) Regulations 2016).

**[6]** `72531-00211` — Asbestos removal, p.150  
> 18.0 Health monitoring When health monitoring occurs A full asbestos medical must be conducted every two years following the initial medical examination, which must occur within four weeks of the worker starting asbestos removal work A full asbestos medical should be done every two years from when asbestos work starts, no matter when the worker started work with their current PCBU. Table 41 shows 

```yaml
id: c005
grounded: yes
citations: valid
modality: correct
complete: yes
drift: none
refusal: na
human: agree
notes: HUMAN VERIFIED (Ben): not a misattribution - same text in both sources. Excerpt artifact again. Label unchanged.
```

---

## 6. `c006` [conceptual]

**Q:** must a certified handler be physically present when highly hazardous gases are in use

### Answer

Based on the sources provided, the answer depends on the specific type of hazardous gas:

**For fumigants and acutely toxic gases (6.1A and 6.1B):**

A certified handler is NOT always required to be physically present during use. According to [2] and [6], a person who is not a certified handler can handle these substances if a certified handler:

- "is present at the place where the substance is being handled, and
- has provided guidance to the person about handling the substance, and
- is available at all times to assist while the person is handling the substance" [2]

**For explosives:**

A certified handler "must always be present when explosives are being transported" [2], though the sources do not explicitly state the requirement for explosives during use (only transport is specified).

**For storage:**

The sources state that highly hazardous gases "must be under the control of a certified handler. The handler must be present and available in the workplace or the area where the gases are stored and handled unless the gases are secured against unauthorised access" [1].

In summary: Physical presence is not always mandatory for use, but the certified handler must be available to provide guidance and assistance. For storage, presence is required unless the gases are secured against unauthorised access.

### Sources given to the model

**[1]** `20566-00088` — Guide to gas cylinders, p.55  
> 6.0 Handling and storage What are the requirements for handling cylinders? General Highly hazardous gases must be under the control of a certified handler. The handler must be present and available in the workplace or the area where the gases are stored and handled unless the gases are secured against unauthorised access. Also, a person must not possess a gaseous fumigant unless they hold a contro

**[2]** `2620-00003` — Certified handler requirements - quick guide, p.3  
> 3/8 worksafe.govt.nz 0800 030 040 Certified handler compliance certificates Compliance certifiers issue certified handler compliance certificates for particular phases of the life cycle (ie manufacture, transport, use, storage or disposal) of hazardous substances. These certificates are valid for five years. A certified handler compliance certificate shows that a worker meets the competency requir

**[3]** `37924-00001` — Agrichemicals - certified handlers, p.2  
> 2/2 worksafe.govt.nz 0800 030 040 For more detailed information on certified handlers The regulations Health and Safety at Work (Hazardous Substances) Regulations 2017 The guidance Certified Handler Requirements (WorkSafe New Zealand) Important to know: Certified handler certificates are issued for a particular hazardous substance or class of substances and for particular phases of the life cycle 

**[4]** `3921-00004` — Hazardous substances that activate key safety controls, p.5  
> 3 2.0 Certified handlers1 A certified handler is someone who has a current compliance certificate to show that they have received the information, training and instruction that they need to handle highly hazardous substances. Do you need a certified handler?2 You need a certified handler if your workplace handles any amount of substances requiring a controlled substance licence (CSL) or have an ac

**[5]** `218-00012` — Working safely with chemicals and fuels on farms, p.12  
> 10 GOOD PRACTICE GUIDELINES // WORKING SAFELY WITH CHEMICALS AND FUELS ON FARMS 10 You must know about the chemicals and fuels you use on your farm and the risks they pose. You must be trained to use them. You need to be certified to use the more hazardous chemicals and fuels. 3.1 APPROVED HANDLER TEST CERTIFICATES An approved handler is someone who is certified to use very hazardous substances. T

**[6]** `37924-00002` — Agrichemicals - certified handlers, p.2  
> will not be able to continue to work as a certified handler. Can hazardous substances under the control of a certified handler be handled by someone else? Yes, provided that the certified handler: – is present at the location where the substance is being handled – has provided guidance to the person handling the substance – is available at all time to provide assistance while the substance is bein

```yaml
id: c006
grounded: yes
citations: valid
modality: correct
complete: missing
drift: adjacent
refusal: na
human: agree
notes: HUMAN CONFIRMED (Ben) as a fail on substantive drift. Ben adds that the SOURCE WORDING is itself confusing and partly contradictory across documents - so some of this failure is attributable to the corpus, not only the model. Still scored as drift: the answer had [1] p55 stating plainly that a handler must be present for highly hazardous gases and did not use it.
```

---

## 7. `c007` [conceptual]

**Q:** what should I look at when choosing a contractor from a health and safety perspective

### Answer

# What to Look at When Choosing a Contractor – Health and Safety Perspective

When choosing a contractor, you should consider the following:

## Health and Safety Record and Performance [3][4]
- The contractor's incident and hazard and risk reporting procedures
- Assessment of their health and safety performance, including:
  - Any work injuries or near misses over the past five years
  - Information on prosecutions they have undergone
- Evidence of proactive steps they have taken to improve health and safety
- Evidence of ongoing improvement in health and safety

## Competence and Capacity [3][4][5]
- The contractor's ability and capacity to do the work
- Their finances, capacity and equipment to do the work
- The contractor's ability to provide competent workers and equipment needed for healthy and safe work
- Relevant industry certification (such as Safetree certification) [3][4]

## Worker Engagement [1][3][4]
- Whether the contractor has effective worker engagement
- Worker representation and opportunities for workers to have their say

## Documented Health and Safety System [3][4]
The contractor should have a documented health and safety system including:
- A health and safety policy
- A drug and alcohol policy, including testing
- Training and supervision
- Health and safety meetings
- Hazard identification and risk assessment and management
- Auditing and inspection programmes
- Incident reporting and investigation
- Emergency procedures

## Important Note
"Cost may be a factor that you consider, but you should never prioritise this over health and safety." [1]

### Sources given to the model

**[1]** `5355-00035` — PCBUs working together: advice when contracting, p.22  
> 20 2.0 Building health and safety into contract management ASSESSING HEALTH AND SAFETY COMPETENCE You should give full and careful consideration to the information gained from tenderers at the pre-qualification/tendering stages. This will help you assess the level of competence that each potential contractor holds, and judge their capability where this is critical to health and safety. Ask a compe

**[2]** `53539-00038` — Keeping healthy and safe while working on the road or roadside, p.30  
> introduction Use procurement practices that support positive health and safety outcomes When selecting contractors, consider their health and safety records. For example, you can look for: – evidence of proactive steps to improve health and safety – evidence of ongoing improvement in health and safety outcomes – evidence of effective worker engagement. Using a centralised prequalification system m

**[3]** `71748-00051` — Part A: Managing health and safety through the contracting chain, p.31  
> 46 4.0 What is expected of principals, contractors, subcontractors and other PCBUs? Choosing a capable contractor 4.1.8 When choosing a contractor, consider their health and safety record as well as their ability and capacity to do the work. 4.1.9 Consider: – the contractor’s incident and hazard and risk reporting procedures – doing an assessment of their health and safety performance, including: 

**[4]** `71736-00070` — Approved code of practice: Safe practice for forestry and harvesting operations, p.48  
> 46 4.0 What is expected of principals, contractors, subcontractors and other PCBUs? Choosing a capable contractor 4.1.8 When choosing a contractor, consider their health and safety record as well as their ability and capacity to do the work. 4.1.9 Consider: – the contractor’s incident and hazard and risk reporting procedures – doing an assessment of their health and safety performance, including: 

**[5]** `5355-00029` — PCBUs working together: advice when contracting, p.19  
> 17 2.0 Building health and safety into contract management 17 Lead PCBUs should follow these steps when building health and safety into contract management. Scoping the work At the beginning of any project, think about health and safety before work starts. This is a crucial first step to choosing the best contractors for your job. You need to be satisfied that the contractors you choose are able t

**[6]** `5355-00032` — PCBUs working together: advice when contracting, p.20  
> to certain tasks or occasional activities, depending on the type of work. Using the pre-tender information Information gained from pre-tender questionnaires may be recorded and, after the contract has been signed, used to develop and implement a health and safety plan (this is completed by the chosen contractor). It may also be used for selecting future contractors for contracts not requiring a te

```yaml
id: c007
grounded: yes
citations: valid
modality: correct
complete: yes
drift: none
refusal: na
human:
notes: [3] p31 and [4] p48 both verified - same passage in two documents
```

---

## 8. `c008` [conceptual]

**Q:** what weight can different ground types support under a scaffold base

### Answer

According to the source provided, here are the nominal bearing capacities for different ground conditions [1]:

| Ground Condition | Bearing Capacity |
|---|---|
| Soft clay – can be moulded by light finger pressure | 2,000 kg/m² |
| Sand | 5,000 kg/m² |
| Stiff clay – can be moulded by strong finger pressure | 7,500 kg/m² |
| Hard clay – difficult to indent with thumb | 10,000 kg/m² |
| Rock | 50,000 kg/m² |

These values are used to calculate the minimum contact area required for soleboards and baseplates. As the source notes, "The softer the ground and/or the heavier the loads, the bigger the soleboard required" [1].

### Sources given to the model

**[1]** `19966-00085` — Scaffolding in New Zealand, p.59  
> 57 SECTION 8.0 // ERECTING THE SCAFFOLD 57 GROUND CONDITIONS NOMINAL BEARING CAPACITY (kg/m2) Soft clay – can be moulded by light finger pressure 2,000 Sand 5,000 Stiff clay – can be moulded by strong finger pressure 7,500 Hard clay – difficult to indent with thumb 10,000 Rock 50,000 Table 13: Load-bearing capacity of different ground conditions SOME TYPES OF SUPPORTING SURFACES AND STRUCTURES > C

**[2]** `19966-00086` — Scaffolding in New Zealand, p.60  
> GOOD PRACTICE GUIDELINES // SCAFFOLDING IN NEW ZEALAND 58 58 Example calculation: If the scaffold is to be erected on a stiff clay surface (load-bearing capacity 7,500 kg/m2) and each standard has a design load of 860 kg: Minimum contact area = 860 kg ÷ 7,500 kg/ m2 = 0.115 m2 To calculate the length of a soleboard that is 225 mm wide: Length of soleboard = 0.115 ÷ 0.225 = 0.511 m BASEPLATES A bas

**[3]** `19966-00065` — Scaffolding in New Zealand, p.46  
> GOOD PRACTICE GUIDELINES // SCAFFOLDING IN NEW ZEALAND 44 44 > where the design is not covered by the manufacturer’s specifications or instructions > when substituting components from different scaffold systems that have not been tested, theoretically and/or physically, as safe to combine > where additional components are included in a proprietary system and cannot be installed in accordance with 

**[4]** `19966-00007` — Scaffolding in New Zealand, p.8  
> TABLES 1 Requirements in this guidance 11 2 An example of a risk rating table 19 3 Competency requirements based on height of scaffold 22 4 NZQA registered unit standards 22 5 Minimum approach distance limits for persons from exposed live parts (where consent has been obtained) 27 6 Grading for inspected scaffolding equipment 28 7 PPE standards and uses 32 8 Suggested inspection frequency 40 9 Ty

**[5]** `19966-00075` — Scaffolding in New Zealand, p.53  
> 51 SECTION 7.0 // SCAFFOLDING DESIGN 51 7.9 STABILITY The scaffold structure must be designed and constructed to remain stable against overturning, and it must be able to provide support for all loads imposed on it for the full period that the scaffold is in place. If stability is in doubt, the scaffold must be assessed by a competent person. MINIMUM TIP FACTOR RATIO MINIMUM FREE-STANDING SCAFFOLD

**[6]** `19966-00066` — Scaffolding in New Zealand, p.46  
> position of ties. > Section of the proposed ties and what the ties are connected to. > Detailed list of scaffold components and weights. > Screening information such as weight and porosity, to determine wind loads on the scaffold. > Intended use of the scaffold. > Duty loading of the scaffold. > Soil samples (on request) to determine the load-bearing capacity of the ground the scaffold is to be er

```yaml
id: c008
grounded: yes
citations: valid
modality: na
complete: yes
drift: none
refusal: na
human:
notes: every figure verified against [1] p59 exactly (2,000 / 5,000 / 7,500 / 10,000 / 50,000 kg/m2)
```

---

## 9. `c009` [conceptual]

**Q:** an excavation face looked stable yesterday, is that enough to rely on

### Answer

No. The sources explicitly state that "an excavation face can appear stable for 24 hours, but may be unstable" [1][2].

Additionally, the sources require that "a competent person should frequently check the soil condition and the state of shoring, benching, battering, and excavated faces for signs of earth fretting, slipping, slumping, or ground swelling" [6]. The condition of soil can "change quickly when the soil dries out, the water table changes or water saturates the soil" [6].

So appearing stable yesterday is not enough to rely on. Regular inspection by a competent person is required.

### Sources given to the model

**[1]** `17-00045` — Excavation safety, p.31  
> (eg hiabs, cranes, trolleys) > manual handling training > geotechnical site assessment > inspecting to ﬁnd out what might aff ect the stability of the excavation (an excavation face can appear stable for 24 hours, but may be unstable) > identiﬁcation and inclusion in safe system of work > minimum approach distances for mobile plant and work activity from overhead lines > minimum approach distances

**[2]** `17-00030` — Excavation safety, p.23  
> SECTION 4.0 // PLANNING THE WORK SITE ISSUES POSSIBLE FACTORS MINIMUM CONSIDERATIONS Ground conditions > soil types > stability > ground water > other soil and rock properties > contaminated soils > potential for seismic hazards (such as fault rupture, liquefaction and rock fall) > inspecting to ﬁnd out what might affect the stability of the excavation (an excavation face can appear stable for 24 

**[3]** `20006-00267` — Health and safety at opencast mines, alluvial mines and quarries, p.164  
> 12.0 Extraction in and around water Extracting beneath water Excavations should be kept stable even if you cannot see them. When extracting beneath water, slopes will be saturated. Draglines, clam shells and long-reach hydraulic excavators may over-steepen the slope they stand on and cause failure. These slopes should be treated as a significant hazard. Working methods should be based on the geote

**[4]** `17-00044` — Excavation safety, p.31  
> SECTION 5.0 // CONTROLLING EXCAVATION RISKS This section outlines common risks that PCBUs should manage throughout any excavation. First try and eliminate the risks but if that is not reasonably practicable, then minimise them, so far as is reasonably practicable. A combination of controls may need to be used. Make sure controls prevent anyone being harmed, so far as is reasonably practicable. The

**[5]** `20006-00211` — Health and safety at opencast mines, alluvial mines and quarries, p.133  
> 10.0 Controlling ground instability in excavations Post excavation inspection of blasted sections When the excavator reaches the batter face following a blast, the designed toe and crest should be achieved, and no blast-induced damage should be visible of the face. After excavation is completed, the face should be inspected and analysed for excessive over break. The damage should be classified int

**[6]** `17-00052` — Excavation safety, p.36  
> 34 GOOD PRACTICE GUIDELINES // EXCAVATION SAFETY HSE Regulation 24 requires any excavated face more than 1.5 m high to be shored, so far as is reasonably practicable, unless: > the face is cut back to a safe slope, or > the material in the face is of proven good standing quality under all reasonably foreseeable conditions of work and weather, or > by reason of the nature of the work and the positi

```yaml
id: c009
grounded: yes
citations: some_invalid
modality: correct
complete: yes
drift: none
refusal: na
human: agree
notes: HUMAN CONFIRMED (Ben) as genuine misattribution. Ben raises chunk OVERLAP as a possible mechanism - if a sentence spans two chunks, which chunk is 'the' citation is ill-defined. Note: does not explain THIS case, since the two chunks are p31 and p36 and page-bounded chunking means overlap only ever occurs WITHIN a page. Real risk for same-page pairs though.
```

---

## 10. `c010` [conceptual]

**Q:** what protective equipment should be planned for a confined space emergency response

### Answer

According to the sources, PPE planned for confined space emergency response should include [1]:

- Respiratory protective equipment (RPE)
- Safety helmet
- Gloves
- Hearing protectors
- Safety harness
- Lifeline

The source notes: "Take care when selecting the right PPE for an emergency response. As well as respiratory protective equipment (RPE), this could include items such as safety helmet, gloves, hearing protectors, safety harness and lifeline." [1]

Additionally, the sources indicate that site-specific emergency procedures and equipment should be established for every confined space job, which will include "PPE and RPE for rescuers" [2], though the sources do not provide a more detailed specification of what additional PPE beyond those listed above should be included for rescue personnel specifically.

### Sources given to the model

**[1]** `21215-00005` — Confined spaces: planning entry and working safely in a confined space, p.3  
> 3/3 worksafe.govt.nz 0800 030 040 worksafe.govt.nz 0800 030 040 PPE can include: – respiratory protective equipment (RPE) – safety helmet – gloves – hearing protectors – safety harness – lifeline. Take care when selecting the right PPE for an emergency response. As well as respiratory protective equipment (RPE), this could include items such as safety helmet, gloves, hearing protectors, safety har

**[2]** `21215-00006` — Confined spaces: planning entry and working safely in a confined space, p.3  
> skills to safely do this work. Regularly reassess their competency for working in confined spaces. Workers who use detectors to test whether the atmosphere is safe must be trained to use them correctly. Confined space emergency procedures Have a site-specific emergency procedure and emergency equipment for every confined space job. This will include: – first aid – firefighting equipment – a rescue

**[3]** `19966-00043` — Scaffolding in New Zealand, p.32  
> to find out the appropriate work methods, risk management, and emergency planning. If the scaffolding is partly or completely within a confined space, make sure: > workers are trained in confined space entry and enough workers are available to carry out a rescue in the event of an emergency > an entry permit system is established > a permit is completed and approved by the PCBU in charge of the co

**[4]** `2599-00036` — Key technical findings, p.23  
> 23 GENERAL FINDINGS Most organisations had sufficiently identified and planned for civil defence emergencies including fires and earthquakes. Poor performing organisations failed to identify emergency situations arising in specific tasks such as falls from heights or rescue from confined space, and had ineffective or non-existent plans to mitigate risks. Higher performing organisations identified 

**[5]** `72531-00094` — Asbestos removal, p.73  
> 9.0 Asbestos removal enclosures Site clearance without an enclosure The licenced assessor should follow the normal Class A clearance inspection process with adjustments: perform a preliminary check of site condition, thorough visual inspection, and decide on what Stage 3 steps of the clearance inspection (surface testing air monitoring) are required based on the circumstances. See Asbestos assessm

**[6]** `20016-00070` — Health and Safety in Welding, p.52  
> Appendices Appendix 4: More information WorkSafe guidance Approvals, hazard classifications and control measures Burns Confined spaces Electrical safety on small construction sites Electric welding machines Emergency plans Energy isolation and locking out machinery Eye protection First aid at work Flammable liquids and fire risk Guide to gas cylinders Hazardous substances toolbox and calculator He

```yaml
id: c010
grounded: yes
citations: valid
modality: correct
complete: yes
drift: none
refusal: na
human:
notes: quotes [1] p3 verbatim, verified
```

---

## 11. `c011` [conceptual]

**Q:** after crane repairs, who must be satisfied before a new inspection certificate issues

### Answer

According to the sources, a new certificate of inspection will be issued after repairs when **an equipment inspector is satisfied** [4].

Specifically, the sources state: "the repairs are to be carried out to the satisfaction of an equipment inspector, and a new certificate of inspection will be issued" [4].

Additionally, for structural repairs requiring welding, "the repairs are to be carried out to the satisfaction of an equipment inspector, and a new certificate of inspection will be issued" [4].

### Sources given to the model

**[1]** `410-00071` — Approved code of practice for cranes, p.44  
> equipment inspector that appropriate alternatives are available. In all cases, the repairs are to be carried out to the satisfaction of an equipment inspector, and a new certificate of inspection will be issued (4) all New Zealand manufactured equipment is inspected and tested by an inspection body in accordance with the requirements of the manufacturing standard, and any inspection and test plan 

**[2]** `410-00089` — Approved code of practice for cranes, p.61  
> 61 Testing of the load limits is to be performed each week by the crane operator or a competent person whilst the crane is erected or in regular service. (e) A plan should be developed for dealing with any emergency. 11.3 Inspections Inspection of new and existing tower cranes is to be in four distinct parts as follows: Part 1: Tower Crane – Inspection at Erection and After Repairs (by an equipmen

**[3]** `410-00094` — Approved code of practice for cranes, p.64  
> 64 (e) Inspection of tie-in collars and supports and documentation of manufacture (f) Either a load test or statement of a satisfactory load test acceptable to the inspection body Note: After any repairs have been carried out, the crane is to be load tested to the figure provided by the manufacturer in the repair specification. (g) Confirmation that rope length is suitable for the application. Par

**[4]** `410-00070` — Approved code of practice for cranes, p.44  
> 44 (6) where practical, factors affecting the remaining life, based on the actual conditions of use, are recorded at every inspection. Such factors may include, but are not limited to, operating hours, utilisation and service conditions (if variable) (7) non-destructive testing (NDT) reports are approved by a suitably qualified signatory working for an IANZ-accredited inspection body. The NDT repo

**[5]** `410-00060` — Approved code of practice for cranes, p.39  
> 39 (5) Suspension or cancellation of a certificate of inspection (a) An equipment inspector who is satisfied on reasonable grounds that equipment is unsafe or unfit for use must recommend to an inspection body that the current certificate of inspection be suspended or cancelled, or that a new certificate not be issued. The inspection body, after giving the controller of the equipment concerned a s

**[6]** `410-00083` — Approved code of practice for cranes, p.54  
> 54 PART 9: FUNCTIONS OF EQUIPMENT INSPECTORS AND INSPECTION BODIES 9.1 Functions (1) The functions of an equipment inspector are to: (a) carry out equipment inspections on behalf of an inspection body. If it is a new crane, all documentation, including the design verification, shall be checked (b) make recommendations to the inspection body relating to the issue, renewal, suspension, or cancellati

```yaml
id: c011
grounded: yes
citations: some_invalid
modality: correct
complete: yes
drift: none
refusal: na
human:
notes: the quoted text is visible in [1] p44 but cited as [4] p44, whose excerpt covers 'factors affecting the remaining life'. Adjacent chunks of the same page so the text may span - but as shown, the citation points to the wrong one
```

---

## 12. `c012` [conceptual]

**Q:** if I hire out forklifts what must I tell customers about exhaust fumes

### Answer

If you hire out forklifts, you must tell customers the following about exhaust fumes [1]:

**Information you must provide:**

1. "You should provide your customers with information on the type of work the forklift is designed and manufactured to do. You should also provide any instructions that must be followed to ensure the forklift does not put the health and safety of workers at risk, including advising them of the risks associated with forklifts and carbon monoxide." [1]

2. Ask your customer if they will use the forklift in areas with poor ventilation. "If they will, advise them to hire or purchase an electric forklift instead. Electric forklifts are good to use in any workplace environment as they don't emit harmful gases." [1]

3. If they intend to use a fuel-powered forklift indoors or in a poorly ventilated area, "Tell the customer that if they intend to use a fuel powered forklift indoors or in a poorly ventilated area they must have a safety plan to prevent carbon monoxide poisoning." [1]

4. "Tell the customer about the importance of keeping the forklift well-maintained to reduce the amount of dangerous gases in the exhaust fumes." [1]

5. "Provide them with a copy of the fact sheet Forklifts and Carbon Monoxide" [1]

You can also advise customers to place a sticker or sign in the forklift warning of the dangers of carbon monoxide [1][6].

### Sources given to the model

**[1]** `674-00002` — Suppliers of forklifts - risk of carbon monoxide poisoning, p.2  
> WHAT INFORMATION DO I NEED TO PROVIDE TO CUSTOMERS? You should provide your customers with information on the type of work the forklift is designed and manufactured to do. You should also provide any instructions that must be followed to ensure the forklift does not put the health and safety of workers at risk, including advising them of the risks associated with forklifts and carbon monoxide. Ask

**[2]** `674-00000` — Suppliers of forklifts - risk of carbon monoxide poisoning, p.1  
> F A C T S H E E T worksafe.govt.nz 0800 030 040 SUPPLIERS OF FORKLIFTS – RISK OF CARBON MONOXIDE POISONING This fact sheet is for ‘persons conducting a business or undertaking’ (PCBUs) that hire or sell (supply) forklifts. Suppliers have a duty to provide customers with relevant health and safety information. The exhaust fumes from liquid petroleum gas (LPG), petrol and diesel engine forklifts con

**[3]** `20162-00001` — Forklifts and carbon monoxide, p.2  
> 2/3 worksafe.govt.nz 0800 030 040 How to keep workers safe PCBUs have a duty to eliminate risks to health and safety, so far as is reasonably practicable. Therefore eliminating the source of carbon monoxide from the workplace by using electricpowered forklifts instead of fuel-powered forklifts should be the first option you consider. Use carts, trolleys, palletizers or similar equipment in rooms o

**[4]** `674-00003` — Suppliers of forklifts - risk of carbon monoxide poisoning, p.2  
> with a copy of the fact sheet Forklifts and Carbon Monoxide You can also advise customers of the risk is to place a sticker or sign in the forklift with a warning of the dangers of carbon monoxide. Figure 1: Avoid using LPG and other fuel-powered forklifts in coolstores and areas with poor ventilation Figure 2: Use electric forklifts in coolstores and areas with poor ventilation

**[5]** `365-00082` — Safe use of timber preservatives and anti-sapstain chemicals, p.47  
> NZTPC Best Practice Guideline – V1 Page 47 7.5.1.2 To minimise the risk of physical injury to employees, Department of Labour H&S recommends that mechanical handling equipment such as forklift hoists be provided to move drums and bags of chemicals. 7.5.1.3 Forklift hoists can be hazardous if employees do not observe safe operating procedures. Advice is contained in the Department of Labour H&S pub

**[6]** `674-00004` — Suppliers of forklifts - risk of carbon monoxide poisoning, p.3  
> worksafe.govt.nz 0800 030 040 For example: WARNING: CARBON MONOXIDE POISONING RISK This forklift is fuelled by LPG/diesel/petrol (select one) and emits carbon monoxide when operating. Carbon monoxide is a dangerous gas that can cause headaches, dizziness, unconsciousness and even death. It can quickly build up in areas with limited ventilation. The risk of carbon monoxide exposure increases when f

```yaml
id: c012
grounded: yes
citations: valid
modality: wrong
complete: yes
drift: none
refusal: na
human:
notes: MODALITY FAILURE. Question asks what I 'must' tell customers. Source [1] says 'You SHOULD provide your customers with information'. The answer headlines it as 'Information you must provide' while quoting 'should' underneath. WorkSafe explicitly defines must = legal requirement, should = recommended practice. Materially wrong for a duty holder
```

---

## 13. `c013` [conceptual]

**Q:** does someone only passing briefly through a hearing protector area need protection

### Answer

Yes. According to the sources, someone passing briefly through a hearing protector area must wear hearing protectors.

[1] states: "Every person in a designated hearing protector area must wear hearing protectors. This includes people working full or part time in those areas, and people passing through or spending very short amounts of time there."

This requirement applies regardless of how briefly they are in the area.

### Sources given to the model

**[1]** `779-00034` — ACOP: Management of noise in the workplace, p.23  
> • Training and education for people wearing hearing protectors. 6.3 The Need for Hearing Protectors Every person in a designated hearing protector area must wear hearing protec- tors. This includes people working full or part time in those areas, and people passing through or spending very short amounts of time there. 6.4 Hearing Protector Areas When the noise levels exceed, or are likely to excee

**[2]** `779-00033` — ACOP: Management of noise in the workplace, p.23  
> MANAGEMENT OF NOISE IN THE WORKPLACE 23 6. C 6. C 6. C 6. C 6. CONTR ONTR ONTR ONTR ONTROL OL OL OL OL OF OF OF OF OF N N N N NOISE OISE OISE OISE OISE E E E E EXPOSURE XPOSURE XPOSURE XPOSURE XPOSURE WITH WITH WITH WITH WITH H H H H HEARIN EARIN EARIN EARIN EARING P P P P PROTECT TECT TECT TECT TECTORS ORS ORS ORS ORS 6.1 Introduction Immediately it is known that employees are being exposed to no

**[3]** `779-00035` — ACOP: Management of noise in the workplace, p.24  
> 24 MANAGEMENT OF NOISE IN THE WORKPLACE Figure 5: Mandatory sign indicating that hearing protectors must be worn The requirements for hearing protector areas are detailed in Clause 10 Hearing protector areas of AS/NZS 1269.3. The meaning of signs must be explained to employees as a part of training (Part 6: Training and Education). Where sign-posting is not practicable, alternative arrangements sh

**[4]** `779-00014` — ACOP: Management of noise in the workplace, p.12  
> 11. Use of hearing protectors in many situations is the only means of control that is left for employers. However, hearing protection in the form of earmuffs or plugs is often a misused control option. Its effectiveness in protecting employees’ hearing depends on: • Selecting the correct device; • Having the device fit an individual properly; and • The amount of time the hearing protector is actua

**[5]** `3993-00003` — Hearing protection, p.3  
> What are the barriers that might stop your workers from wearing hearing protection? What’s the answer? Even if your work is not consistently noisy, your hearing can still be damaged from a single loud noise exposure. What’s the answer? It’s never too late to protect your hearing, even if it is partially damaged. If you need hearing aids in the future, they will only be effective if you have some h

**[6]** `3993-00000` — Hearing protection, p.1  
> Hearing protection is the least effective control measure, and should only be considered once all options to eliminate the noise at source or minimise the exposure to noise have been exhausted. You must provide hearing protection in your work if it is needed to manage noise risks, and train your workers on how to use it correctly. NOISE Hearing Protection EARMUFFS EARPLUGS Attribution 4.0 Internat

```yaml
id: c013
grounded: yes
citations: valid
modality: correct
complete: yes
drift: none
refusal: na
human:
notes: quotes [1] p23 verbatim and verified. clean answer to a yes/no question
```

---

## 14. `c014` [conceptual]

**Q:** is notification needed before a quarantine fumigation using methyl bromide

### Answer

Yes, notification is required before a quarantine fumigation using methyl bromide.

**Timing:** Notification must be provided **at least 24 hours before the start of the fumigation** [3][5].

**Who must be notified** depends on the amount of methyl bromide being used:

- For fumigations using **less than 100 kg**: Occupants of each property within **25 metres** of the site must be notified [3][5].

- For fumigations using **more than 100 kg in a 24-hour period**: Occupants of each property within **100 metres** of the site (including moored boats) must be notified [3][5].

- **If a marae is adjacent to the site**: The PCBU must "make appropriate notification arrangements with local Māori" [3][5].

**Exception for regular fumigations:** If fumigation is carried out weekly at the site, the PCBU may notify relevant persons before the initial fumigation and then annually thereafter, rather than before each fumigation [3][5].

**Responsibility:** It is the responsibility of the person applying methyl bromide to ensure notification occurs, though the actual notification may be done by someone on their behalf [2].

### Sources given to the model

**[1]** `3169-00012` — Summary of submissions - proposed safe work instruments, p.6  
> approval and must be complied with under HSWA. Concern was raised with clause 8(5) Notification of intended fumigation – quarantine or pre-shipment fumigation using methyl bromide and the ability of a PCBU who intends to carry out quarantine or pre-shipment fumigation using methyl bromide to notify relevant persons annually. WorkSafe notes that this clause only applies if there are to be regular f

**[2]** `2119-00031` — Methyl bromide fumigations, p.22  
> 22 Methyl Bromide Fumigations Post Reassessment Guidance for Fumigations April 2011 143/01 Section 3: Notification of fumigations The notification requirements when using methyl bromide for space fumigation have changed. Depending on the type of fumigation, the person using methyl bromide must inform the following people at least 24 hours before the fumigation begins. Table 5: Notification require

**[3]** `3175-00009` — Health and Safety at Work (Hazardous Substances—Requirements for Specified Fumigants) Safe Work Instrument 2017, p.6  
> Health and Safety at Work (Hazardous Substances—Requirements for Specified Fumigants) Safe Work Instrument 2017 6 Modified requirements applying to quarantine or pre-shipment fumigation using methyl bromide 8 Notification of intended fumigation – quarantine or pre-shipment fumigation using methyl bromide (1) This clause applies to a PCBU who intends to carry out quarantine or pre-shipment fumigati

**[4]** `2119-00043` — Methyl bromide fumigations, p.32  
> 32 Methyl Bromide Fumigations Post Reassessment Guidance for Fumigations April 2011 143/01 Appendix 4: Example of notification record sheet Name of person who conducted notification Organisation Date and time of notice Method of notification Letter Fax Email Contact details of person notified Reason for notifying the person Recapture not used, occupant within 25 metres of fumigation site. Recaptur

**[5]** `61687-00014` — Consolidated SWI: Health and Safety at Work (Hazardous Substances – Requirements for Specified Fumigants) Safe Work Instrument 2017, p.10  
> at a site must notify the occupants of each property within 25 m of the site of the PCBU's intention to carry out fumigation not less than 24 hours before the start of the fumigation. (3B) If a marae is adjacent to a site, the PCBU who intends to carry out fumigation using methyl bromide must make appropriate notification arrangements with local Māori. (3C) A PCBU who intends to apply more than 10

**[6]** `3175-00002` — Health and Safety at Work (Hazardous Substances—Requirements for Specified Fumigants) Safe Work Instrument 2017, p.2  
> specifies an alternative time by which a PCBU must ensure signs are removed, for the purposes of regulation 14.10(5)(b) of the Regulations, for fumigation using Ripper Range: clause 8 modifies the notification requirements in regulation 14.7 of the (d) Regulations (under regulation 14.7(4) of the Regulations) for quarantine or pre- shipment fumigation using methyl bromide:

```yaml
id: c014
grounded: yes
citations: valid
modality: correct
complete: yes
drift: none
refusal: na
human: agree
notes: HUMAN VERIFIED (Ben): the 100 kg / 100 m threshold IS in source [3] - '(3C) A PCBU who intends to apply more than 100 kg of methyl bromide in a 24-hour period must notify the occupants of each property within 100 m of the site, including moored boats... not less than 24 hours before'. Excerpt artifact. Label unchanged.
```

---

## 15. `c015` [conceptual]

**Q:** how far must a fixed barrier sit from a robot arm reach

### Answer

According to the sources, a fixed barrier must be at least **500 mm from the robot work envelope (extreme reach of the robot arm and tooling)** [1].

This is stated in the context of designing openings for feeding material to stop trapping hazards.

### Sources given to the model

**[1]** `20169-00079` — Safe use of machinery, p.61  
> 10.0 Choosing the right guard Any openings for feeding material in should be designed to keep every part of a person away from any hazard. To stop trapping, any fixed barriers should be at least 500 mm from the robot work envelope (extreme reach of the robot arm and tooling). Design and place presence-sensing devices (such as photoelectric curtains) to detect if anyone enters a restricted space or

**[2]** `5645-00012` — Ergonomics of machine guarding, p.13  
> MINISTRY OF BUSINESS, INNOVATION & EMPLOYMENT ERGONOMICS OF MACHINE GUARDING 12 the arm has to be bent round it. At 200 mm from the reach curve it is no longer possible to reach around the additional barrier because the arm is fully extended, stopping the wrist from reaching the edge of the barrier. With the barrier in each of these positions it is still possible for the hand to reach back underne

**[3]** `5645-00011` — Ergonomics of machine guarding, p.12  
> barrier. However, the hand can reach underneath the barrier to a distance of almost 200 mm from the edge. If the edge of the additional barrier is less than 430 mm from the reach curve, the arm can still be partly bent around it, though not so far as in Figure 4. The closer the edge of the additional barrier is to the reach curve, the less ability

**[4]** `5645-00010` — Ergonomics of machine guarding, p.12  
> MINISTRY OF BUSINESS, INNOVATION & EMPLOYMENT ERGONOMICS OF MACHINE GUARDING 11 If the arm is pulled back until the wrist is near the edge of the additional barrier, the hand can be bent around the barrier and may reach the dangerous part if it is too close. Generally the hand will not reach as far as 200 mm around that point. The reach of a hand bent around the end of a barrier will therefore be 

**[5]** `5645-00009` — Ergonomics of machine guarding, p.11  
> MINISTRY OF BUSINESS, INNOVATION & EMPLOYMENT ERGONOMICS OF MACHINE GUARDING 10 ◊ Reach around barriers When an operator’s arm reaches over or around a barrier, the action is described as a ‘reasonable reach curve’. The ability to reach around barriers is determined by the distance of the elbow joint and wrist joint from the reach curve (e.g. from the finger tip). The average elbow joint is 460 mm

**[6]** `5645-00005` — Ergonomics of machine guarding, p.7  
> MINISTRY OF BUSINESS, INNOVATION & EMPLOYMENT ERGONOMICS OF MACHINE GUARDING 6 Figure 2: The height of guarding can change reach lengths. ◊ Reaching over barriers The height of a barrier or guard needs to limit an operator being able to reach over into the danger zone. Where the barrier is low, the worker can bend over and increase their reach longer than their arm. Where the barrier is at armpit 

```yaml
id: c015
grounded: yes
citations: valid
modality: wrong
complete: yes
drift: none
refusal: na
human:
notes: MODALITY FAILURE. Source [1] p61 reads 'any fixed barriers SHOULD be at least 500 mm from the robot work envelope'. The answer states 'a fixed barrier MUST be at least 500 mm'. Recommended practice reported as a legal requirement
```

---

## 16. `c016` [conceptual]

**Q:** what properties make a substance hazardous in welding work

### Answer

According to the sources, a hazardous substance is any product or chemical with the following properties [1][4]:

- Explosive
- Flammable
- Oxidising
- Toxic
- Corrosive
- Hazardous to the environment (eco-toxic)

In welding specifically, "a hazardous substance is any product or chemical with properties that are explosive, flammable, oxidising, toxic, corrosive or hazardous to the environment (eco-toxic)" [1]. When used in welding, these substances "produce airborne contaminants, exposing workers to toxic fumes, gases and vapours" [1].

### Sources given to the model

**[1]** `20016-00043` — Health and Safety in Welding, p.34  
> 6.0 Hazardous substances and airborne contaminants The control measures for hazardous substances depend on the classification of a substance. What could go wrong A hazardous substance is any product or chemical with properties that are explosive, flammable, oxidising, toxic, corrosive or hazardous to the environment (eco-toxic). Hazardous substances when used in welding produce airborne contaminan

**[2]** `20006-00390` — Health and safety at opencast mines, alluvial mines and quarries, p.237  
> 15.0 Plant and structures – Electric shock: Welding processes that use electricity pose both obvious and subtle hazards of electric shock – which can be fatal. Take precautions, as explained in our guide Health and Safety in Welding when using welding equipment. Expert assistance can be needed in some circumstances to identify subtle hazards. Appropriate equipment selection, set-up and maintenance

**[3]** `20016-00052` — Health and Safety in Welding, p.40  
> 7.0 Fire and explosion Sources of ignition Welding (and associated processes such as grinding) generates heat, flames and sparks, which are all sources of ignition. When combined with sources of fuel and oxygen, they present a significant risk of fire and explosion. Common sources of fuel in workplaces that carry out welding include: – flammable gases, such as acetylene, hydrogen, methane, natural

**[4]** `48889-00031` — Safe work with lifts, escalators and moving walkways, p.23  
> 3.0 How can you manage risk? When you carry out a risk assessment, consider whether you can implement engineering control measures. Engineering control measures (such as interlocking guards) are higher in the hierarchy and considered to be more effective. For more information, see our guidance: – Keeping workers safe when servicing machinery – Safe use of machinery – Manual handling Also see: – Ha

**[5]** `20016-00058` — Health and Safety in Welding, p.44  
> 8.0 Welding gases – epoxy coatings can produce carbon dioxide and carbon monoxide – vinyl paints can produce hydrogen chloride – phosphate rust-inhibiting paints can release phosphine during welding processes. Cylinders, including cryogenic containers and fire extinguishers (but not aerosol dispensers), must meet the requirements in 15.7(1) of the Hazardous Substances Regulations before being supp

**[6]** `20160-00000` — Toolbox talk 1: welding work health effects, p.1  
> 1/1 worksafe.govt.nz 0800 030 040 Health effects from welding – Welding produces toxic fumes and gases – Some welding processes are more hazardous than others – Some welding fumes and gases make you sick straight away; others gradually damage your lungs over a period of years – Welding also produces ultraviolet and infrared radiation that can cause eye damage. It can also burn your skin (similar t

```yaml
id: c016
grounded: yes
citations: some_invalid
modality: na
complete: yes
drift: none
refusal: na
human:
notes: the properties list is verified verbatim in [1] p34, but the answer cites [1][4] and [4] is 'Safe work with lifts, escalators' p23 on engineering controls - does not support the claim
```

---

## 17. `c017` [conceptual]

**Q:** when is a ladder actually the right tool for a task

### Answer

According to the sources, a ladder is the right tool when it meets these specific criteria [1][2]:

- The task is **light** and **of short duration**
- Examples given include "changing a light bulb or touching up paint" [1][2]

Additionally, for stepladders specifically, sources [6] note that use should take into account:
- that it is **light work**
- the height of the task
- if a safe handhold is available
- if it avoids side loading and over-reaching
- if the worker's feet are fully supported

Source [3] states that "Portable ladders should be used for low-risk and short-duration tasks."

The sources emphasize an important limitation: "Ladders do not offer any protection from a fall" [1][2]. Therefore, ladders should be considered only after eliminating or minimising fall risks through other means, and "should therefore be the last form of work access equipment you consider" [3].

### Sources given to the model

**[1]** `70203-00039` — Extractives quarterly report – Q2 October to December 2024, p.25  
> 2.0 Health and safety performance REGULATOR COMMENTS AND RECOMMENDATIONS Is a ladder the right tool for carrying out your job safely? Ladders are primarily a means of access to carry out light tasks that are of short duration, for example changing a light bulb or touching up paint. They do not offer any protection from a fall. Consider control measures when selecting the best way to work at height

**[2]** `19961-00000` — Safe working with ladders and stepladders, p.1  
> 1/2 worksafe.govt.nz 0800 030 040 HSWA • H E A L T H & S A F E T Y A T W O R K A C T • F A C T S H E E T May 2022 Safe working with ladders and stepladders This fact sheet is for anyone considering using a ladder or stepladder at work. It provides information to help you work safely while using them. Is a ladder the right tool for carrying out your job safely? Ladders are primarily a means of acce

**[3]** `20006-00386` — Health and safety at opencast mines, alluvial mines and quarries, p.235  
> 15.0 Plant and structures Portable ladders Portable ladders should be used for low-risk and short-duration tasks. The user should maintain three points of contact with a ladder or stepladder to reduce the likelihood of slipping and falling. Ladders and stepladders do not offer fall protection and should therefore be the last form of work access equipment you consider. Portable ladders should compl

**[4]** `71736-00065` — Approved code of practice: Safe practice for forestry and harvesting operations, p.44  
> of mud and debris. – Keep three points of contact when climbing in or out of the machine. Care when hooking and unhooking logs – Where possible use a grapple. – When the breaker-out is pulling out chokers from a motorised carriage, face the carriage directly to minimise twisting. Choose tools and machinery with built-in controls to reduce physical impacts on the operator – Select equipment that is

**[5]** `71748-00046` — Part A: Managing health and safety through the contracting chain, p.27  
> of mud and debris. – Keep three points of contact when climbing in or out of the machine. Care when hooking and unhooking logs – Where possible use a grapple. – When the breaker-out is pulling out chokers from a motorised carriage, face the carriage directly to minimise twisting. Choose tools and machinery with built-in controls to reduce physical impacts on the operator – Select equipment that is

**[6]** `20109-00072` — Working at height in New Zealand, p.51  
> 4.0 Good practice for managing work at height risks Where side-on loadings cannot be avoided, stop the stepladder from tipping over by tying the steps to a suitable point, or use a more suitable type of access equipment. Avoid holding items when climbing ladders and stepladders by using tool belts. On a stepladder Where a handhold cannot be maintained, the use of a stepladder should take into acco

```yaml
id: c017
grounded: yes
citations: valid
modality: correct
complete: yes
drift: none
refusal: na
human:
notes: content verified against the ladders fact sheet. NOTE: leads with [1], an Extractives QUARTERLY REPORT that quotes the guidance, rather than the guidance itself. Not wrong, but a weaker citation than available
```

---

## 18. `c018` [conceptual]

**Q:** how should I identify hazards for work at height alongside my workers

### Answer

# Identifying Hazards for Work at Height With Your Workers

According to the sources, here's how you should identify hazards alongside your workers:

## Four Methods of Identification

You should use these four ways to identify hazards [1][3]:

1. **Physical inspections** – walk around the workplace using a checklist to identify and manage hazards
2. **Task analysis** – identify the hazards involved in each task of the job
3. **Process analysis** – identify hazards at each stage of the production or service delivery process
4. **Analysis of accident investigation** – identify hazards and causal factors from investigations involving similar types of work

## Involving Your Workers

**Ask your workers directly.** "With your workers, identify hazards that could be associated with the work activity" and "Ask your workers what hazards they can identify." [2] Your workers have "operational day-to-day knowledge that will be invaluable when assessing work risks." [1]

## Additional Resources

Review your incident and injury records (including near misses), as this "may also help identify hazards." [2]

After identifying hazards, you then move to assessing the risk [2] and controlling the hazards [3].

### Sources given to the model

**[1]** `70203-00040` — Extractives quarterly report – Q2 October to December 2024, p.26  
> 2.0 Health and safety performance 1. Identify Hazards Identify any hazards of working at height where someone could fall. Four ways of identifying hazards are: – physical inspections – walk around the workplace using a checklist to identify and manage hazards – task analysis – identify the hazards involved in each task of the job – process analysis – identify hazards at each stage of the productio

**[2]** `20109-00024` — Working at height in New Zealand, p.20  
> 3.0 General principles of good risk management Step 1: Identify the hazards With your workers, identify hazards that could be associated with the work activity. Every work environment will be different. Looking at your work environment and thinking about things that could go wrong may help you to identify hazards. Reviewing your incident and injury records (including near misses) may also help ide

**[3]** `503-00000` — Planning a safe approach to working at height, p.1  
> F A C T S H E E T 1 worksafe.govt.nz 0800 030 040 PLANNING A SAFE APPROACH TO WORKING AT HEIGHT This fact sheet will help you manage working at height safely. Start by planning a safe approach. Too many falls from height are caused by a failure to plan and organise work properly. Planning safe working at height means: > > identifying the hazards > > assessing the hazards > > controlling the hazard

**[4]** `4415-00011` — Working on roofs - good practice guidelines, p.9  
> 4 maintained to ensure they are safe to use. In a workplace, a ladder should meet the standard AS/NZS 1892.1: Portable ladders – Part 1: Metal. Your work plan should include information about: • safe access to the roof area • assessment of the roofing materials • identify hazards associated with working at height from or through the roof • brittle roofing assessment • other working at height hazar

**[5]** `20169-00022` — Safe use of machinery, p.22  
> 4.0 Identify hazards Fatigue and shift-work Fatigue is a hazard. PCBUs must take all reasonably practicable measures to minimise the risk of fatigue, such as when employees drive or use dangerous machinery. Shift-work can be hazardous because it disrupts normal rest patterns. Employees need enough recovery time outside work so they can be safe and productive at work. Along with enough sleep, break

**[6]** `55020-00036` — Extractives quarterly report - Q4 April to June 2022, p.24  
> 2.0 Health and safety performance PCBUs should: – change the way a task is carried out when a safer alternative is identified, and encourage their workers accordingly – ensure suitable equipment, including PPE, is available and workers have adequate training for its use – ensure workers are trained to identify fall-from-height hazards they might encounter and have appropriate supervision – review 

```yaml
id: c018
grounded: yes
citations: valid
modality: correct
complete: yes
drift: none
refusal: na
human:
notes: four methods verified in [1] p26. Same pattern as c017 - cites a quarterly report over the actual Working at Height guidance, which was present as [2]
```

---

## 19. `c019` [conceptual]

**Q:** what must a PCBU provide so workers are protected from health and safety risks

### Answer

According to the sources, a PCBU must provide the following to protect workers from health and safety risks:

**Information, training, instruction, and supervision** [1][2][3][4]
- PCBUs must "provide the information, training, instructions or supervision necessary to protect all persons from risks arising from work carried out as a part of the conduct of the business or undertaking" [1]
- The type and extent depends on "the nature of the work carried out and the experience of the workers, and the risk that workers and others...are exposed to" [3]

**A safe work environment and systems** [1][2][6]
- "provide and maintain a work environment that is without risks to health and safety" [1]
- "provide and maintain safe systems of work" [1]

**Safe plant, structures, and substances** [1][2][6]
- "provide and maintain safe plant and structures" [1]
- "ensure the safe use, handling and storage of substances" [1]

**Adequate welfare facilities** [1][2][3]
- "provide adequate and accessible facilities for the welfare of workers" [1]

**Personal protective equipment** [1]
- "provide suitable personal protective equipment and clothing for workers" [1]

**Health and condition monitoring** [2][3]
- "monitor the health of workers and the exposures at the workplace" [2]

All these duties must be met "so far as is reasonably practicable" [1][2].

### Sources given to the model

**[1]** `62251-00004` — Workplace exposure standards (WES) and biological exposure indices (BEI) – 16th edition, p.5  
> Obligations and rights under the Health and Safety at Work Act 2015 (HSWA) and Health and Safety at Work (General Risk and Workplace Management) Regulations 2016 What are the obligations of a person conducting a business or undertaking (PCBU)? PCBUs must ensure the health and safety of workers doing work for the PCBU and to ensure the health and safety of others whose work is influenced or directe

**[2]** `863-00002` — Health and safety leadership guide: for owners and company directors of small to medium businesses, p.2  
> PCBUs must, so far as reasonably practicable: ›› provide and maintain a work environment, plant, structures and systems of work that are without risks to health and safety ›› ensure the safe use, handling and storage of plant, structures and substances ›› provide adequate facilities at work for the welfare of workers, including ensuring access to those facilities ›› provide information, training, 

**[3]** `824-00032` — Introduction to the Health and Safety at Work Act 2015 - special guide, p.25  
> 3.0 PCBU duties Ensuring the safe use, handling and storage of plant, structures, and substances PCBUs must, so far as is reasonably practicable, make sure that plant, structures, and substances are safely used, handled and stored. Providing adequate facilities for the welfare at work of workers in carrying out work for the business or undertaking, including ensuring access to those facilities PCB

**[4]** `20227-00021` — General risk and workplace management - part 1, p.17  
> 3.0 Information, training, instruction and supervision PCBUs must ensure all persons are provided the information, training, instruction or supervision they need to protect them from health and safety risks arising from the PCBU’s work. Having well trained, instructed and supervised people in the workplace Training helps people share knowledge and develop skills, and is an important part of managi

**[5]** `3232-00008` — Protecting workers from solar UV radiation, p.7  
> Who is responsible? As a PCBU, you have a primary duty to ensure your workers are not put at risk by the work they do. If you have identified UV radiation exposure as a potential health hazard for your workers, it is your responsibility to manage the risks arising from this hazard. You must take steps to eliminate and minimise the risk, so far as reasonably practicable. This may include providing 

**[6]** `20109-00016` — Working at height in New Zealand, p.14  
> PCBUs must also make sure, so far as is reasonably practicable, that other persons’ health and safety is not put as risk by the work that they do. – PCBUs must, so far as is reasonably practicable, have effective practices in place for providing and maintaining: - a work environment that is without risk to health and safety - safe plant and structures - safe use, handling and storage of plant, sub

```yaml
id: c019
grounded: yes
citations: valid
modality: correct
complete: yes
drift: none
refusal: na
human:
notes: verified in [4] p17 and [2]. correctly preserves 'so far as is reasonably practicable'
```

---

## 20. `c020` [conceptual]

**Q:** what should be considered when selecting air monitoring sites for a fumigation

### Answer

# Factors to Consider When Selecting Air Monitoring Sites for Methyl Bromide Fumigations

According to the sources, several key factors should be considered:

**Location and Wind Direction:**
- The potential effects of nearby valley situations or marked changes in terrain should be taken into account when determining the optimum downwind direction [1]
- Whether the air flow is likely to be channelled in a specific direction away from the site [1]
- For port-based fumigations when the wind is blowing offshore, monitoring must be done at landward sites at the edge of the buffer zone that are judged as having the greatest potential for methyl bromide exposure [4]
- A smoke generator or similar device should be used before ventilation starts to determine the most likely downwind direction if wind conditions are light and variable [4]

**Physical Environment:**
- The presence of buildings, trees and walls can affect airflows around the monitoring site [1]
- A free flow of air around the monitor is necessary to ensure representative sampling [1]
- Sampling in a stagnant or sheltered micro-environment should be avoided [1]
- Specific recommendations on separation distances between monitoring sites and nearby buildings, trees and walls are given in Australia/New Zealand Standard AS/NZS 3580.1.1:2007 [1][5]

**Other Contaminants:**
- The presence of other potential sources of volatile organic compounds (VOCs) in the vicinity should be avoided whenever possible, as monitoring equipment like photo-ionisation detectors (PIDs) respond to other VOCs [1]

**Sensitive Locations:**
- Monitoring should be considered for any nearby locations that could be regarded as more sensitive than the site directly downwind – for example, residential or business areas [2]

### Sources given to the model

**[1]** `2119-00007` — Methyl bromide fumigations, p.7  
> 7 Methyl Bromide Fumigations Post Reassessment Guidance for Fumigations April 2011 143/01 What other factors should be considered when selecting monitoring sites? The potential effects of nearby valley situations or marked changes in terrain should be taken into account when determining the optimum downwind direction. In particular, consideration should be given to whether the air flow is likely t

**[2]** `2119-00005` — Methyl bromide fumigations, p.6  
> 6 Methyl Bromide Fumigations Post Reassessment Guidance for Fumigations April 2011 143/01 However, if the wind direction changes, this information should be recorded and explained in the annual monitoring report, if one is required for the site. The only exception to the above would be if the ventilation process is suspended for a significant period of time (e.g. where ventilation is not allowed d

**[3]** `2119-00019` — Methyl bromide fumigations, p.13  
> averages, only when those monitoring sites are within 10 metres of each other. The data and calculations behind the annual average concentrations should be clearly outlined in the annual report if one is required for the site. The application of this recommendation is illustrated in Figure 2, which shows a simplified example of the possible variation in monitoring sites around a single fumigation 

**[4]** `2119-00004` — Methyl bromide fumigations, p.5  
> port-based fumigations when the wind is blowing offshore. In this situation, the monitoring must be done at one or more landward sites, at the edge of the buffer zone, that are judged as having the greatest potential for methyl bromide exposure to occur. If the wind conditions are light and variable, a smoke generator or similar device should be used before the start of the ventilation period to d

**[5]** `2119-00008` — Methyl bromide fumigations, p.7  
> more of methyl bromide. When monitoring is first carried out at a fumigation site, it would be preferable for the measurements to be continued for much longer than the minimum times indicated, to ensure that the initial reduction of the indicated exposure to less than 0.05 ppm is not just part of the fluctuations that are often observed with atmospheric monitoring. Monitoring should begin a few mi

**[6]** `2119-00036` — Methyl bromide fumigations, p.26  
> 26 Methyl Bromide Fumigations Post Reassessment Guidance for Fumigations April 2011 143/01 Appendix 1: Example of how to record methyl bromide air monitoring information (This cover sheet should be on letterhead paper that shows the name and address of the company or other entity carrying out the monitoring. As most monitoring data will be recorded electronically, it is recommended that the Page 1

```yaml
id: c020
grounded: yes
citations: valid
modality: correct
complete: yes
drift: none
refusal: na
human:
notes: the port/offshore-wind claim verified verbatim in [4] p5; valley and terrain factors match the [1] p7 heading
```

---

## 21. `u001` [unanswerable]

**Q:** what is the current adult minimum wage in New Zealand

### Answer

The sources provided do not contain information about the current adult minimum wage in New Zealand. They focus on WorkSafe New Zealand's financial reports, employee surveys about health and safety perceptions, and demographic data from workplace surveys. I cannot answer this question based on these sources.

### Sources given to the model

**[1]** `968-00072` — Annual report: 2013/14, p.56  
> 54 WORKSAFE NEW ZEALAND // ANNUAL REPORT 2013 – 2014 15. EMPLOYEE ENTITLEMENTS $000 ACTUAL 2014 Current portion Accrued salaries and wages 1,103 Annual leave 1,884 Retirement and long service leave 119 Total current portion 3,106 Non-current portion Retirement and long service leave 767 Total non-current portion 767 TOTAL EMPLOYEE ENTITLEMENTS 3,873 16. PROVISIONS $000 ACTUAL 2014 Current portion 

**[2]** `51475-00013` — Segmentation and insights programme: Employers and workers 2021, p.15  
> LOCATIONS OF W ORK Who we surveyed – WORKERS HOUSEHOLD INCOME $20,000 or less $20,001-$30,000 $30,001-$50,000 $50,001-$70,000 $70,001-$100,000 $100,001-$150,000 Over $150,000 SIZE OF EMPLOYER Up to 5 employees 6-9 10-19 20-49 50-99 100+ 23% 10% 15% 16% 8% 25% GENDER 1 Female 47% Male 53% SOCIO-ECONOMIC STATUS LEVEL 2 9% 15% 25% 26% 18% 6% 1 2 3 4 5 6 3% 4% 10% 20% 21% 25% 16% (Highest) (Lowest) OR

**[3]** `51481-00086` — New Zealand Psychosocial Survey 2021, p.69  
> Q U E S T I O N N A I R E 3. Gender Are you: Male Female Another gender 4. Age Which age group are you in: 18–19 45–49 70–74 20–24 50–54 75 or over 25–29 55–59 30–34 60–64 40–44 65–69 5. Ethnicity Which of these ethnic groups best describe you: (you can choose more than one) New Zealand European Māori Samoan Cook Island Māori Tongan Niuean Chinese Indian Another ethnic group: (please tell us) Don’

**[4]** `956-00120` — Annual report: 2015/16, p.86  
> 10. PAYABLES $000 ACTUAL 2016 ACTUAL 2015 Payables under exchange transactions Creditors 3,024 1,806 Income in advance 788 – Accrued expenses 2,560 4,113 Other 86 37 Total payables under exchange transactions 6,458 5,956 Payables under non-exchange transactions Taxes payables (GST, PAYE and rates) 318 262 Grants payables – – Grants received subject to conditions – – Other – – Total payables under 

**[5]** `22568-00083` — Annual report: 2018/19, p.62  
> 17% in 2017 to 20% in 2019) as being among their top three considerations.15 These shifts may reflect employers’ increased concerns regarding the performance of New Zealand’s economy as indicated by recent business confidence polls, which show New Zealand business confidence is at its lowest level since March 2009.16 Measure RESULT 2015/16 RESULT 2016/17 RESULT 2017/18 TARGET 2021/22 RESULT 2018/1

**[6]** `65355-00014` — Segmentation and insights programme: Employers and workers 2023, p.15  
> Verian WorkSafe 2023 Who we surveyed Background and research method Workers All data on this chart is weighted. Base: All workers (3,300). Source: S3, S4, S5, S6, S8, Q1a, Q1f, Q12, Q13, Q15 (worker questionnaire). 1Note: Less than 1% of respondents identified as ‘another gender’. 2https://www.auckland.ac.nz/en/arts/our-research/research-institutes-centres-groups/compass/whole-population-data-anal

```yaml
id: u001
grounded: na
citations: na
modality: na
complete: na
drift: none
refusal: correct
human:
notes: declined; characterised sources accurately (financial reports, surveys)
```

---

## 22. `u002` [unanswerable]

**Q:** what is the Reserve Bank official cash rate

### Answer

The sources provided do not contain information about the Reserve Bank official cash rate. 

The sources are WorkSafe's financial reports and only discuss WorkSafe's own financial position, cash holdings, and interest rate risks. While [2] mentions a secondment to the Reserve Bank of New Zealand, it does not provide information about the official cash rate.

I cannot answer this question using only the sources provided.

### Sources given to the model

**[1]** `3196-00114` — Annual report: 2016/17, p.86  
> 5. Cash and cash equivalents Cash and cash equivalents include cash on hand, deposits held on call with banks and other short-term, highly liquid investments with original maturities of three months or less. CASH AND CASH EQUIVALENTS $000 ACTUAL 2017 ACTUAL 2016 Cash at bank and on hand 654 2,475 Term deposits with maturities less than three months – – TOTAL CASH AND CASH EQUIVALENTS 654 2,475 Cas

**[2]** `72241-00108` — Annual report: 2024/25, p.70  
> 4.0 Financial statements $000 ACTUAL 2025 ACTUAL 2024 Secondments to other government agencies Reserve Bank of New Zealand 95 – Maritime New Zealand – 75 Fire and Emergency New Zealand 68 5 Total secondments to other government agencies 163 80 Secondments from other government agencies Ministry of Business, Innovation, and Employment 195 96 NZ Transport Authority 87 – Department of Internal Affair

**[3]** `22568-00103` — Annual report: 2018/19, p.79  
> $000 ACTUAL 2019 ACTUAL 2018 Extractives Industry Advisory Group Total Extractives Industry Advisory Group remuneration 26 13 TOTAL COMMITTEE MEMBER REMUNERATION 117 89 5. Cash and cash equivalents Cash and cash equivalents include cash on hand, deposits held on call with banks and other short-term, highly liquid investments with original maturities of three months or less. CASH AND CASH EQUIVALEN

**[4]** `63292-00145` — Annual report: 2022/23, p.99  
> CASH FLOW INTEREST RATE RISK Cash flow interest rate risk is the risk that the cash flows from a financial instrument will fluctuate because of changes in market interest rates. WorkSafe has investment policies to manage the risk associated with cash flow interest rate risk. WorkSafe currently has no variable interest rate investments. CURRENCY RISK Currency risk is the risk that the fair value or

**[5]** `72094-00035` — Quarterly report 2024/25 – Quarter 4, p.22  
> 22 Memorandum accounts $000 Total YTD Balance YTD Actual Prior Year Total YTD Major Hazard Facilities Levies Revenue 20,706 1,538 19,168 Expenditure (21,239) (2,613) (18,626) Total surplus/(deficit) (533) (1,075) 542 Add Crown Account surplus/(deficit) 3,053 1,152 1,901 Total surplus/(deficit) - WorkSafe held levies 2,520 77 2,443 Current financial position: Statement of financial position $000 Ac

**[6]** `35068-00147` — Annual report: 2019/20, p.108  
> CASH FLOW INTEREST RATE RISK Cash flow interest rate risk is the risk that the cash flows from a financial instrument will fluctuate because of changes in market interest rates. WorkSafe has investment policies to manage the risk associated with cash flow interest rate risk. WorkSafe currently has no variable interest rate investments. CURRENCY RISK Currency risk is the risk that the fair value or

```yaml
id: u002
grounded: na
citations: na
modality: na
complete: na
drift: none
refusal: correct
human:
notes: precise - spotted that [2] mentions an RBNZ secondment but gives no cash rate
```

---

## 23. `u003` [unanswerable]

**Q:** how do I apply for a New Zealand work visa

### Answer

I cannot answer this question based on the provided sources. The sources only cover New Zealand workplace health and safety applications (compliance certifier authorisation, controlled substance licences, site senior executive certificates, hazardous substances exemptions, and asbestos assessor licensing). They do not contain information about work visa applications.

For work visa information, you would need to contact Immigration New Zealand directly.

### Sources given to the model

**[1]** `2320-00003` — Guide for compliance certifier authorisation (Body corporate), p.4  
> Part 4 on how to complete the application form. You must be accredited by IANZ to a recognised industry standard before submitting an application. All application forms are available on the WorkSafe website at www.worksafe.govt.nz or can be requested by e-mail at hsapplications@worksafe.govt.nz. Accompanying these application forms are various annexes (Annexes A, B, C, D, E and F) which are also a

**[2]** `20658-00002` — Application for a controlled substance licence, p.2  
> 2/6 worksafe.govt.nz 0800 030 040 Application for a controlled substance licence 2. Evidence of identity For applicants who have not held a CSL before You must provide verified^ copies of at least one primary and one supporting identity document. – At least one of these should be a photographic identity document. ^ The documents can be verified by the issuing authority or a Justice of the Peace, r

**[3]** `59509-00000` — New SSE CoC Form, p.1  
> F O R M 1/5 worksafe.govt.nz 0800 030 040 Application for a new site senior executive certificate of competence Use this form to apply for a new SSE certificate of competence (CoC) under the Health and Safety at Work (Mining Operations and Quarrying Operations) Regulations 2016 1. Applicant details Full legal name: Physical address: (include postcode) Postal address: (with company name if applicab

**[4]** `2872-00000` — Application for exemption from separation distance and/or other matters, p.1  
> 1/5 worksafe.govt.nz 0800 030 040 F O R M Application for exemption from Part 11 requirements for separation distance and/or building type Under Regulation 11.40 of the Health and Safety at Work (Hazardous Substances) Regulations 2017 and section 220 of the Health and Safety at Work Act 2015 If there is insufficient information provided for WorkSafe New Zealand to fully assess the application, it 

**[5]** `21479-00000` — Application for exemption from Part 11 requirements for separation distance and/or building type, p.1  
> 1/5 worksafe.govt.nz 0800 030 040 F O R M Application for exemption from Part 11 requirements for separation distance and/or building type Under Regulation 11.40 of the Health and Safety at Work (Hazardous Substances) Regulations 2017 and section 220 of the Health and Safety at Work Act (HSWA) 2015 Section 6 of this application form is to be completed and signed by the compliance certifier Email: 

**[6]** `20519-00007` — Asbestos assessor licensing guide for applicants, p.8  
> 2.0 How to apply for a licence Methods of payment You can pay the application fees over internet banking or over the counter at any Westpac branch. When paying, the applicant must enter ‘Asbestos’ in the particulars, and enter the first 12 characters of the full legal name that will be on the licence document as the reference. Failure to do so could result in lost tracking of the payment and neces

```yaml
id: u003
grounded: na
citations: na
modality: na
complete: na
drift: none
refusal: correct
human:
notes: PROMPT VIOLATION: redirects to Immigration NZ, which is outside knowledge
```

---

## 24. `u004` [unanswerable]

**Q:** how do I register a company with the Companies Office

### Answer

The sources provided do not contain information about how to register a company with the Companies Office. 

The sources discuss WorkSafe New Zealand's registration processes for adventure activity operators, and they mention the Companies Office only in passing (regarding certificates of incorporation for name changes [6]), but they do not explain the Companies Office registration process itself.

To answer your question, you would need to consult the Companies Office directly or their guidance materials.

### Sources given to the model

**[1]** `65466-00006` — Application for registration, or for renewal of registration, as an adventure activity operator, p.6  
> 6/6 worksafe.govt.nz 0800 030 040 Application for registration, or for renewal of registration, as an adventure activity operator 2 Currently WorkSafe New Zealand. Declaration If the applicant for registration is an individual, this declaration must be completed by that individual. If the applicant is a corporate entity or unincorporated group of persons, this declaration must be completed by an a

**[2]** `65460-00004` — Application to provide an additional adventure activity under your current adventure activity operator registration, p.4  
> report(s) for the activities the applicant wishes to add to their registration Fees There is no fee to add an activity to an existing registration. Declaration If the applicant is an individual, this declaration must be completed by that individual. If the applicant is a corporate entity or unincorporated group of persons, this declaration must be completed by an authorised representative who is i

**[3]** `65454-00004` — Application to amend your current adventure activity operator registration, p.4  
> to the safety audit the applicant passed to obtain the new certificate a copy of the auditor’s activity Technical Expert evaluation report(s) for the activity locations the applicant wishes to add to their registration (if applicable) Fees There is no fee to amend the details of your current registration. Declaration If the applicant is an individual, this declaration must be completed by that in

**[4]** `1490-00045` — Health and Safety in Employment (AA) Regulations 2011 - Guidance for operators, p.20  
> the Department of your intentions. If your business wants to provide the different activities after 31 December 2013, you do not need to notify the Department of your intentions (although you will still need to obtain a safety audit and registration). Topic 2 in this guidance document outlines the timeframes for meeting the requirements of the notification process. Auditing and registering If your

**[5]** `31460-00010` — Gas Appliance Supplier Declaration Database user guide, p.12  
> Gas Appliance Declaration Database User Guide 12 | P a g e 6. Complete Your Registration If you have not done so before you need to review the Terms and Conditions and Privacy Policy before you can access the Gas Appliance Supplier Declaration Database. You can also update your personal details or company details at the same at the same time. Steps 1. You can update the your personal details if ne

**[6]** `65454-00000` — Application to amend your current adventure activity operator registration, p.1  
> F O R M 1/5 worksafe.govt.nz 0800 030 040 Applicant details All fields mandatory unless stated otherwise. Full name: (company name or, if an individual, full legal name) Trading name(s) if different from above: Web/internet site: (if applicable) New Zealand Business Number (NZBN): Business phone number: Business email: Business physical address: (including postcode) Business postal address: (if di

```yaml
id: u004
grounded: na
citations: na
modality: na
complete: na
drift: none
refusal: correct
human:
notes: noted Companies Office appears only in passing re certificates of incorporation
```

---

## 25. `u005` [unanswerable]

**Q:** how do I lodge a personal grievance for unfair dismissal

### Answer

# Lodging a Personal Grievance for Unfair Dismissal

The sources provided explain what a personal grievance for unjustified dismissal is and which body handles it, but they do not contain the procedural steps for how to actually lodge one.

## What the sources do say:

The sources indicate that [1][2]:
- Employees who feel bullying behaviour led to their "unjustified dismissal" can raise a personal grievance
- The **Employment Relations Authority** (http://era.govt.nz) can resolve disputes about "personal grievances for unjustified dismissal"

## What is missing:

The sources do not explain:
- The specific steps or process for filing a personal grievance
- Timeframes for lodging
- Required documentation
- Where or how to submit the grievance

**Before taking external action, the sources also note [2] that MBIE's free mediation service (Phone 0800 20 90 20) is available and "can help parties resolve an employment relationship problem."**

To get the procedural details you need, you would need to consult the Employment Relations Authority directly or seek additional guidance beyond these sources.

### Sources given to the model

**[1]** `782-00070` — Preventing and responding to bullying at work, p.46  
> well as breach of contract. Employees that feel that bullying behaviour led to their unjustified disadvantage or unjustified dismissal might raise a personal grievance. – – In terms of harassment, the ERA only provides protection from sexual and racial harassment, which is also covered by the Human Rights Act 1993 (HRA). This gives grounds for a personal grievance under the ERA, or a claim under t

**[2]** `785-00016` — Bullying at work: advice for workers, p.12  
> ERA only provides protection from sexual and racial harassment, which is also covered by the Human Rights Act 1993 (HRA). This gives grounds for a personal grievance under the ERA, or a claim under the HRA. > > MBIE’s free mediation service (Phone 0800 20 90 20; https://employment.govt.nz/ resolving-problems/steps-to-resolve/mediation/request-mediation) is available to any employer or employee and

**[3]** `782-00069` — Preventing and responding to bullying at work, p.46  
> 6.0 Seeking external help Bullying complaints may be dealt with by different Government bodies depending on the circumstances. If parties to a complaint are not satisfied by your actions, and they have made reasonable efforts to work with you to try to resolve the issue using internal processes, they may decide to seek external help. You may also seek external help. In addition, certain behaviour 

**[4]** `785-00015` — Bullying at work: advice for workers, p.12  
> 12 12 04 WHO CAN HELP? Bullying complaints may be dealt with by different Government bodies depending on the circumstances. If you are not satisfied by the business or undertakings’ actions, and have made reasonable efforts to try to resolve the issue using internal processes, you may decide to seek external help. In addition, certain behaviour should be dealt with externally in the first instance

**[5]** `20130-00067` — Worker engagement, participation and representation, p.42  
> 4.0 Worker participation practices A person who has been affected by adverse conduct may apply to the District Court for an appropriate order (for example, to restrain someone from engaging in adverse conduct). However, an employee who wishes to take action against an employer (or former employer) in respect of adverse conduct for a prohibited health and safety reason will instead need to bring a 

**[6]** `4143-00001` — Example - Sexual harassment policy, p.1  
> culture that is fair and free of sexual harassment – – encourage positive leadership styles and invest in our managers to achieve this – – focus on behaviour rather than people, and aim to promote harmonious relationships across the company – – openly discuss sexual harassment in both formal and informal settings, and provide information and training about it including consequences of such behavio

```yaml
id: u005
grounded: na
citations: na
modality: na
complete: na
drift: adjacent
refusal: correct
human:
notes: BORDERLINE - gave sourced context (what a PG is, ERA handles it, cited [1][2]) before stating it lacks procedural steps. Did not use outside knowledge. Reasonable people could score this as a partial answer.
```

---

## 26. `u006` [unanswerable]

**Q:** what qualifications make someone a licensed building practitioner

### Answer

The sources provided do not contain information about qualifications for a licensed building practitioner. These sources focus specifically on asbestos assessments, asbestos surveys, exposure monitoring, pressure equipment, and related occupational health and safety matters in New Zealand.

To answer your question about licensed building practitioner qualifications, you would need sources related to the Building Act 2004 and Building Practitioner licensing requirements, which are not included here.

### Sources given to the model

**[1]** `72529-00011` — Asbestos assessments, p.12  
> 1.0 About these guidelines Competent persons Competent persons can perform asbestos assessments for Class B asbestos removal work only. For example: – air monitoring during Class B asbestos removal – clearance inspections for Class B asbestos removal – issuing clearance certificates for Class B asbestos removal. A competent person must have the knowledge, experience, skills, and qualifications to 

**[2]** `70743-00014` — Conducting asbestos surveys, p.14  
> 2.0 Qualifications and experience for surveying Competence can be demonstrated through a combination of relevant qualifications and practical experience. Competence to carry out asbestos surveys Before carrying out a survey of a building to identify asbestos, the surveyor should be able to demonstrate that they are a competent person. Competence can be demonstrated through a combination of relevan

**[3]** `38257-00089` — Exposure monitoring and health monitoring - good practice guidelines, p.56  
> Appendices TYPE OF PROFESSIONAL WHAT MONITORING SERVICES CAN THEY PROVIDE? QUALIFICATIONS AND CERTIFICATIONS TO LOOK FOR PROFESSIONAL ASSOCIATION MEMBERSHIPS TO LOOK FOR General Practitioners (GPs) Deal with medical referrals: – to diagnose work-related illness or injury – if needed, can refer to other practitioners for further medical assessment/formal diagnosis. Qualifications to look for: – is 

**[4]** `8-00281` — ACOP: Management and removal of asbestos, p.203  
> competent person may carry it out. The licensed asbestos assessor or competent person will determine air monitoring variables such as sample duration time and monitoring locations in consultation with the asbestos removalist or PCBU conducting asbestos-related work. In this case, a competent person is a person who, through training or experience, has the skills and knowledge of asbestos removal in

**[5]** `2-00044` — ACOP: Pressure equipment (excluding boilers), p.30  
> the person seeking the qualification has the requisite training, skills, knowledge and experience. (4) The qualification issuing agencies recognised by the Secretary and the occupational groups for which they issue qualifications are: (a) Certification Board for Inspection Personnel for equipment inspectors; (b) Institution of Professional Engineers New Zealand for design verifiers; and (c) New Ze

**[6]** `70743-00015` — Conducting asbestos surveys, p.15  
> 2.0 Qualifications and experience for surveying PCBUs providing surveying services should be able to provide the commissioning PCBU with evidence that the workers carrying out the work are competent. This may include a combination of: – qualification records for the workers carrying out the work – the status of any relevant accreditations and certifications for the workers carrying out the work – 

```yaml
id: u006
grounded: na
citations: na
modality: na
complete: na
drift: none
refusal: correct
human:
notes: PROMPT VIOLATION: redirects to Building Act 2004 / BPB, outside knowledge
```

---

## 27. `u007` [unanswerable]

**Q:** how do I claim ACC weekly compensation after an injury

### Answer

The sources provided do not contain information about how to claim ACC weekly compensation after an injury. 

The sources define what ACC weekly compensation is and provide statistics about claims, but they do not explain the process or procedures for making a claim.

To find this information, you would need to contact ACC directly or consult sources that specifically cover ACC claims procedures.

### Sources given to the model

**[1]** `67185-00046` — Report: Overview of work-related harm and risk in Aotearoa New Zealand, p.28  
> the work health and safety system is performing. Under New Zealand’s universal and no-fault accident compensation system, seeking medical attention following an injury usually leads to the lodgement of an ACC claim. The total number of work-related ACC claims therefore gives a reasonable indication of the total number of workers experiencing injuries. There are over 200,000 work-related ACC claims

**[2]** `1295-00033` — Towards 2020 - Progress towards the 2020 work-related injury reduction target - May 2017, p.34  
> motor vehicle account. WorkSafe uses a customised dataset of ACC work-related claims involving weekly compensation payments (for more than a week away from work) to produce the third indicator for monitoring progress towards the target. Stats NZ will publish this data as part of the forthcoming Work-related injuries at a glance product.39 Not all injuries appear in the ACC claims data. For example

**[3]** `67185-00038` — Report: Overview of work-related harm and risk in Aotearoa New Zealand, p.24  
> June 2024 Page | 23 Injuries resulting in more than a week away from work Injuries resulting in more than a week away from work (often referred to as ‘WAFW’ injuries) are identified through accepted ACC claims where the injured worker has received weekly compensation payments from ACC.13 There are around 35,000 WAFW injury claims per year, around 70 times more than serious non-fatal injuries and 5

**[4]** `63292-00047` — Annual report: 2022/23, p.35  
> 5 A work-related acute injury resulting in more than a week away from work is one where an injured worker has received weekly compensation from ACC for loss of earnings while recovering from injury. Indicator 3: Work-related acute injury resulting in more than a week away from work5 Latest official data: 2021 calendar year 13.8 ACC week away from work injury claims per 1,000 FTEs 6% higher than 20

**[5]** `56880-00002` — Fact sheet - Work-related serious injury outcome indicators - December 2022, p.2  
> 2/2 worksafe.govt.nz 0800 030 040 2 A serious non-fatal injury is an injury to a patient who is admitted to hospital with a probability of death of 6.9% or more. 3 A work-related acute injury resulting in more than a week away from work is one where an injured worker has received weekly compensation from ACC for loss of earnings while recovering from injury. Indicator 2: Work-related serious non-f

**[6]** `3196-00019` — Annual report: 2016/17, p.18  
> Annual Report 2016-2017 Rate of injury resulting in more than a week away from work We have not seen the same progress for injuries resulting in more than a week away from work (WAFW). This rate increased each year from 2011 to 2015, and although 2016 data shows a slight reversal in this trend, the indicator remains higher than the 2009-11 baseline. 11.7 ACC weekly compensation claims for injury p

```yaml
id: u007
grounded: na
citations: na
modality: na
complete: na
drift: none
refusal: correct
human:
notes: PROMPT VIOLATION: redirects to ACC. Correctly noted sources define the term and give statistics but not process
```

---

## 28. `u008` [unanswerable]

**Q:** what notice period must I give when resigning from a job

### Answer

The sources provided do not contain information about notice periods for resigning from a job. They address New Zealand workplace health and safety topics such as petroleum operations notifications, WorkSafe enforcement notices, health and safety representative arrangements, and safety case requirements—but not employment resignation procedures.

To answer your question, I would need sources covering employment law or employment agreements.

### Sources given to the model

**[1]** `32-00005` — Petroleum notifications quick guide, p.3  
> 3/4 worksafe.govt.nz 0800 030 040 worksafe.govt.nz 0800 030 040 Notify WorkSafe before starting well-drilling operations You must give the notice of well operations to WorkSafe at least 21 days (or a shorter period if specified by WorkSafe) before starting the following well operations: – – drilling, completion, suspension, or abandonment, and – – recommencing drilling after completing, suspending

**[2]** `824-00096` — Introduction to the Health and Safety at Work Act 2015 - special guide, p.68  
> with an improvement notice must comply with the notice within the compliance period or be liable on conviction to a fine. Inspectors may extend the compliance period before it expires. Prohibition notices An Inspector may issue a prohibition notice if they reasonably believe a workplace activity involves or will involve a serious risk to health and safety arising from an immediate or imminent expo

**[3]** `20225-00034` — Worker representation through Health and Safety Representatives and Health and Safety Committees, p.25  
> time by giving reasonable notice to the other parties. If a PCBU withdraws from an agreement (or negotiations for an agreement) concerning a work group, their leaving does not affect the validity of any agreement reached between the original or remaining parties. A PCBU must give reasonable notice to the other parties. Reasonable notice may depend on factors such as the industry involved, how many

**[4]** `1034-00056` — Petroleum: Major accident prevention policy and safety case requirements, p.35  
> fails to comply with a notice issued by an inspector under the Act; or (iii) fails to provide a revised safety case when required under regulation 31, 32, or 33; or (b) WorkSafe has finally rejected a revised safety case. (2) Before withdrawing acceptance of a safety case, WorkSafe must give the permit operator or the drilling contractor at least 30 days’ written notice of its intention to do so, 

**[5]** `1034-00057` — Petroleum: Major accident prevention policy and safety case requirements, p.36  
> WORKSAFE NEW ZEALAND // MAJOR ACCIDENT PREVENTION POLICY AND SAFETY CASE REQUIREMENTS 34 34 (3) WorkSafe may provide a copy of the notice to any other person. (4) The permit operator or the drilling contractor may, by the date specified by WorkSafe, make written submissions to WorkSafe in relation to the proposed withdrawal of acceptance. (5) Before making a final decision to withdraw acceptance o

**[6]** `410-00035` — Approved code of practice for cranes, p.26  
> 26 then- (i) determine the date on which the cancellation takes effect, which must be a reasonable period after the date on which the decision is made, and (ii) publish a notice in the New Zealand Gazette indicating that the exemption is to be cancelled on the date specified in the notice. (3) Exemptions for equipment (a) Pursuant to regulation 6 of the PECPR Regulations, the Secretary may: (i) ex

```yaml
id: u008
grounded: na
citations: na
modality: na
complete: na
drift: none
refusal: correct
human:
notes: clean decline, accurate characterisation of sources
```

---

## 29. `u009` [unanswerable]

**Q:** what is the maximum residential tenancy bond a landlord can require

### Answer

The sources provided do not contain information about the maximum residential tenancy bond a landlord can require. 

The sources discuss asbestos management for residential landlords [1][3][4], lead-based paint guidelines [2][6], electrical safety in rental properties [5], and tenant protections under the Residential Tenancies Act 1986 [6], but none address bond limits.

To answer your question, you would need sources that specifically cover the Residential Tenancies Act 1986 provisions on bond requirements.

### Sources given to the model

**[1]** `64539-00000` — Policy clarification: What residential landlords need to do to manage asbestos, p.1  
> 1/2 worksafe.govt.nz 0800 030 040 HSWA • H E A L T H & S A F E T Y A T W O R K A C T • O P E R A T I O N A L P O L I C Y February 2024 What residential landlords need to do to manage asbestos This policy’s purpose This policy clarification sets out when residential landlords (landlords) have a duty to identify asbestos and prepare an asbestos management plan, as required by the Health and Safety a

**[2]** `983-00014` — Guidelines for the management of lead-based paint, p.12  
> Landlords are thus required to protect occupants and others from (among other things) lead contamination arising from paintwork in the tenant’s property or its fixtures and fittings. However, this would not apply to the tenant’s own painted furnishings. 3.5 Resource Management Act 1991 The Resource Management Act 1991 is the main controlling statute dealing with the sustainable management of natur

**[3]** `68256-00004` — Asbestos in the home, p.4  
> doing the work. You can read more about other persons at the workplace on the WorkSafe website What to know about ‘other persons’ at work Residential landlords Under HSWA, residential landlords must make sure that work carried out at their property is done safely. If there is a risk that workers or other people (including tenants) could be exposed to asbestos fibres when work is carried out, resid

**[4]** `68256-00005` — Asbestos in the home, p.5  
> This duty applies when the work is being carried out. It applies to: – any area where work is carried out that could create a risk of exposure to asbestos fibres, and – any access route for the area where work is carried out. You can read more about the duties residential landlord have to manage asbestos on the WorkSafe website Policy clarification: Residential landlords and asbestos The role of W

**[5]** `1592-00005` — New Zealand Electrical Code of Practice for managing electrical risks associated with electrically conductive thermal insulation (NZECP 55: 2016), p.6  
> Page 6 of 28 INTRODUCTION Regulations detailing new insulation and smoke alarm requirements to implement changes to the Residential Tenancies Act 1986 were announced by the New Zealand Government in April 2016. This gives effect to a package of amendments intended to improve the quality of residential rental properties, including changes to the minimum insulation standards of tenanted residential 

**[6]** `983-00013` — Guidelines for the management of lead-based paint, p.12  
> 11 GUIDELINES FOR THE MANAGEMENT OF LEAD-BASED PAINT 3.2 Health Act 1956 The Health Act 1956 is the prime statute controlling health hazards to the public at large. It identifies lead poisoning by absorption equal to or in excess of 0.48 μmol/l from non-occupational sources as a notifiable disease (Section B of Schedule 2), which must be reported by a medical practitioner to the medical officer of

```yaml
id: u009
grounded: na
citations: na
modality: na
complete: na
drift: none
refusal: correct
human:
notes: listed what the sources did cover (asbestos for landlords, lead paint, RTA 1986) - grounded decline
```

---

## 30. `u010` [unanswerable]

**Q:** how do I dispute a parking infringement notice

### Answer

I cannot answer this question using the sources provided. The sources provided relate only to New Zealand workplace health and safety matters—specifically electrical and gas safety regulations, and the Health and Safety at Work Act 2015.

Parking infringement notices fall outside the scope of these workplace health and safety sources. You would need to consult sources about traffic law or contact the relevant local authority or transport enforcement agency for information on disputing parking infringements.

### Sources given to the model

**[1]** `626-00072` — Designing, installing and maintaining safe electrical and gas installations and distribution systems, p.45  
> fee will not exempt you from having to carry out any remedial action. Continuing to commit an offence may result in further notices or prosecution. If the impact assessment made by Energy Safety indicates that the effect of non– compliance is sufficiently serious, or a previous history of non–compliance exists, an Infringement notice may be issued directly following an investigation or audit. For 

**[2]** `632-00038` — Supplying safe electrical and gas products, p.32  
> AND ADVISORIES A Warning notice will outline: > > the offence observed > > the remedial action to take. The Warning notice may be accompanied by advice to cease supply and notify consumers who purchased that product. A follow-up audit may be made to monitor compliance with the Regulations and any remedial action required. If remedial action is not taken within the specified timeframe, Energy Safet

**[3]** `632-00039` — Supplying safe electrical and gas products, p.33  
> SECTION 8.0 // ENFORCEMENT OF ELECTRICAL AND GAS PRODUCT SAFETY 31 31 Paying an Infringement fee will not exempt you from having to carry out any remedial action. Continuing to commit an offence may result in further notices or prosecution. If the impact assessment made by Energy Safety indicates that the effect of non-compliance is sufficiently serious, or a previous history of non-compliance exi

**[4]** `626-00071` — Designing, installing and maintaining safe electrical and gas installations and distribution systems, p.45  
> 43 SECTION 6.0 // AUDITS AND ENFORCEMENT 43 If remedial action is not taken within the specified timeframe, Energy Safety may escalate the enforcement to ensure protection of the public and property. Warnings While an Infringement notice may follow from an unresolved Warning notice, there is no requirement to give a Warning notice first. INFRINGEMENT NOTICES Regulations 10, 11 and 12 of the Electr

**[5]** `824-00097` — Introduction to the Health and Safety at Work Act 2015 - special guide, p.69  
> 9.0 Enforcement event has occurred, or prevent a particular site (including the operation of plant) being disturbed for a specified period. A non-disturbance notice may be issued if the Inspector reasonably believes it is necessary to facilitate the exercise of his or her compliance powers. Notices must be displayed. A non-disturbance notice does not prevent any action to assist anyone who has bee

**[6]** `2422-00012` — Assessing fit and proper person status: Technical guide, p.8  
> 6 When considering infringement offences, the decision maker will consider: – the relevance of the infringement offence for the authorisation being sought – the particular circumstances of the offence and – the particular circumstances of the individual. As a guide, if a person has had four or more infringements of a similar type within the previous two years, these may be taken to indicate a patt

```yaml
id: u010
grounded: na
citations: na
modality: na
complete: na
drift: none
refusal: correct
human:
notes: PROMPT VIOLATION: redirects to traffic law / local authority
```

---

## 31. `id001` [identifier]

**Q:** what does Regulation 47 require

### Answer

The sources provided contain multiple different Regulation 47s from different regulatory frameworks, so I cannot give you a single answer without knowing which one you're asking about:

1. **Electricity Regulation 47** [1] - specifies what home-owners may do on low voltage electrical installations, including removing and replacing fittings, fuse links, connecting/disconnecting appliances, relocating switches and outlets, and installing/extending subcircuits (with testing and certification requirements).

2. **GSMR 47 (Gas Safety and Measurement Regulations)** [4] - describes what a Certificate of Compliance must contain, requiring the certificate issuer to confirm the gasfitting work was done lawfully and safely, and that information is correct. It also specifies what attachments or references to documents must be included.

3. **Asbestos Regulations 47** [5] - relates to maintenance and servicing work involving asbestos-containing materials (though the source does not detail the specific requirements of this regulation).

Which Regulation 47 did you want to know about?

### Sources given to the model

**[1]** `1580-00007` — New Zealand Electrical Code of Practice for homeowner/occupier's electrical wiring work in domestic installations (NZECP 51: 2004), p.6  
> Electricity Regulation 47 47. Home-owners' electrical wiring work (1) For the purposes of section 110 of the Act, any person to whom that section applies may do or assist in doing the following work on low voltage electrical installations: (a) Remove and replace any of the following kinds of fittings where the work does not involve work on any switchboard: (i) Switches: (ii) Socket-outlets: (iii) 

**[2]** `5307-00082` — ACOP: Flammable liquids road tank wagons, p.49  
> 47 Appendices 47 I certify that I have design checked/inspected the following: Vehicle: Owner: Type of vehicle: Hazardous substances: Registration number: Fleet number: Tank number: Capacity: Drawings: Flammable liquid tank wagons Appendix B: Manufacturer’s declaration I declare that I have made such detailed examinations and checks as I considered necessary and it is my opinion that: 1. The desig

**[3]** `626-00079` — Designing, installing and maintaining safe electrical and gas installations and distribution systems, p.49  
> 47 SECTION 6.0 // AUDITS AND ENFORCEMENT 47 OFFENCES RELATING TO CERTIFICATION AND PERIODIC ASSESSMENTS > > Once prescribed electrical work has been done: – – failing to test the installation (Regulation 65) – – failing to certify or arrange certification of the work (Regulation 66) – – arranging certification, inspecting, issuing and keeping a certificate of compliance if not satisfied that the w

**[4]** `1826-00000` — Checklist for certificates of compliance (CoCs) - Gas, p.1  
> Checklist for Certificates of Compliance (CoCs) – Gas Page 1 of 3 www.energysafety.govt.nz Checklist for Certificates of Compliance (CoCs) – Gas The Certificate of Compliance (CoC) provides a legally recognisable statement of the safety status of completed gasfitting specifically for the purpose of connection to gas supply, and also for other purposes, including auditing and investigations. A CoC 

**[5]** `8-00323` — ACOP: Management and removal of asbestos, p.232  
> APPROVED CODE OF PRACTICE // MANAGEMENT AND REMOVAL OF ASBESTOS 230 SAFE WORK PRACTICE ONE: SEALING, PAINTING, COATING AND CLEANING ACMs This safe work practice is designed to comply with regulation 7(2)(h): maintenance and servicing work involving ACM in accordance with these regulations. Depending on the type of asbestos-related work, follow the requirements outlined in Asbestos Regulations 47 t

**[6]** `3645-00008` — Guide to Completing and Submitting Plans for Mines and Tunnels, p.7  
> Page 7 of 47 Guide to Submitting Mine and Tunnel Plans Health and Safety at Work (Mining Operations and Quarrying Operations) Regulations 2016 The Health and Safety at Work (Mining Operations and Quarrying Operations) Regulations 2016, or HSW regs, specify WorkSafe’s requirements for mine plans. The most commonly-referenced regulations are: • Regulation 28: Mine surveyor • Regulation 73: Considera

```yaml
id: id001
grounded: yes
citations: valid
modality: na
complete: na
drift: none
refusal: correct
human:
notes: EXCELLENT behaviour, FLAWED QUESTION. Identified that the corpus contains three different Regulation 47s (Electricity, Hazardous Substances, Gas Safety) and declined to pick one. The golden set treats every chunk containing 'regulation 47' as correct - conflating separate instruments
```

---

## 32. `id002` [identifier]

**Q:** what does Regulation 92 require

### Answer

Based on the sources provided, Regulation 92 of the MOQO Regulations requires the preparation of a **Principal control plan (PCP)** [1][2][3].

According to the sources, the PCP is "a plan required under MOQO Regulation 92. The plan documents systems and processes in place at the mining or tunnelling operation to manage hazards at the operation, and the measures that are necessary to manage principal hazards at the mining or tunnelling operation" [1].

The sources do not provide additional detail about what specifically must be included in the Principal control plan beyond this general description.

### Sources given to the model

**[1]** `113-00150` — ACOP: Ground or strata instability in underground mines or tunnels, p.99  
> SECTION 11.0 // GLOSSARY TERM EXPLANATION Principal control plan (PCP) A plan required under MOQO Regulation 92. The plan documents systems and processes in place at the mining or tunnelling operation to manage hazards at the operation, and the measures that are necessary to manage principal hazards at the mining or tunnelling operation. See MOQO Regulation 93. Principal hazard Any hazard arising 

**[2]** `155-00101` — Emergency preparedness in mining and tunnelling operations, p.64  
> APPROVED CODE OF PRACTICE // EMERGENCY PREPAREDNESS IN MINING AND TUNNELLING OPERATIONS 64 TERM EXPLANATION PHMP See Principal hazard management plan. Principal control plan A plan required under regulation 92 of the MOQO Regulations. The plan documents systems and processes in place at the mining or tunnelling operation to manage hazard, and the measures that are necessary to manage principal haz

**[3]** `170-00101` — ACOP: emergency preparedness in mining and tunnelling operations, p.64  
> APPROVED CODE OF PRACTICE // EMERGENCY PREPAREDNESS IN MINING AND TUNNELLING OPERATIONS 64 TERM EXPLANATION PHMP See Principal hazard management plan. Principal control plan A plan required under regulation 92 of the MOQO Regulations. The plan documents systems and processes in place at the mining or tunnelling operation to manage hazard, and the measures that are necessary to manage principal haz

**[4]** `4496-00022` — Summary of submissions - proposed Health and Safety at Work (Hazardous Substances - Information and Process Requirements for Compliance Certifiers) Performance Standard 2018, p.14  
> regulation 17.93(1)(a) as evidence that the design of a stationary tank meets the requirements for a tank design under regulation 17.91(2)(b)(i). Consideration by suitably trained and qualified professionals (eg Professional engineers or Advanced trades) should also be acceptable. Noted. The submitter’s comments raise an issue that only the Regulations can deal with. SPECIFIC COMMENTS Clause 15 – 

**[5]** `4490-00011` — Health and Safety at Work (Hazardous Substances—Information and Process Requirements for Compliance Certifiers) Performance Standard 2019, p.7  
> issued under regulation 17.93(1)(a) as evidence that the design of a stationary tank meets the requirements of regulation 17.91(2)(b)(i). (2) A compliance certifier may accept a compliance certificate for a fabricator (in relation to a certified design or designs) issued under regulation 17.93(1)(b) as evidence that the fabrication of the stationary tank meets the requirements of regulation 17.91(

**[6]** `3789-00005` — Summary of submissions, p.5  
> Some submitters commented that periods of up to 15 years are provided for in regulation 17.92(2). This regulation allows WorkSafe to determine validity periods of compliance certificates for individual stationary container systems and individual PCBUs. These periods are maximums. They do not apply generally, and the period determined by WorkSafe will depend on the individual system. Some submitter

```yaml
id: id002
grounded: yes
citations: valid
modality: correct
complete: yes
drift: none
refusal: na
human:
notes: answered: MOQO Reg 92 requires a Principal Control Plan. verified against [1][2][3]
```

---

## 33. `id003` [identifier]

**Q:** what does Regulation 84 require

### Answer

The sources reference Regulation 84 in multiple contexts, but each refers to different regulations:

1. **Mining Operations and Quarrying Operations** – MOQO Regulation 84 specifies "what must be included in a PHMP for air quality" [1]. The sources indicate it relates to principal hazard management plans for air quality [2], but do not detail the specific requirements.

2. **Electricity (Safety) Regulations 2010** – Regulation 84 concerns "Declared High Risk Articles" and requires that "All high risk products must be formally approved, or covered by certification that is recognised as an equivalent to an approval (under Regulations 85 or 86A) before being offered" [3].

The sources do not provide the full text of what either Regulation 84 requires. To answer your question completely, you would need to consult the actual regulations themselves.

### Sources given to the model

**[1]** `131-00089` — ACOP: Air quality in the extractives industry, p.63  
> plan required under MOQO Regulation 66. The PHMP describes a principal hazard and sets out the controls used to manage it. A PHMP must be prepared for each principal hazard identified at the mining or tunnelling operation. MOQO Regulations 68, 69 and 70 cover what needs to be included in a PHMP, and requirements for reviews, revisions and audits. MOQO Regulation 84 specifies what must be included 

**[2]** `38257-00073` — Exposure monitoring and health monitoring - good practice guidelines, p.47  
> Workplace Management) Regulations 2016 regulation 30 Mining operations – Monitor and assess airborne dust and contaminants at the mine – Regularly monitor the atmosphere at the mining operation to manage hazards associated with unsafe concentrations of oxygen, methane, and other gases in the air. The monitoring measures must be detailed in the principal hazard management plan for air quality. Heal

**[3]** `632-00020` — Supplying safe electrical and gas products, p.20  
> GOOD PRACTICE GUIDELINES // SUPPLYING SAFE ELECTRICAL AND GAS PRODUCTS 18 18 CATEGORY OF PRODUCTS SAFETY REQUIREMENTS High risk Recognised Approval or Certification Medium risk Supplier Declaration of Conformity (SDoC) made by the New Zealand manufacture or importer Other products Comply with fundamental safety requirements The New Zealand market is aligned with the Australian regulatory regime th

**[4]** `52924-00006` — Health and Safety at Work (Hazardous Substances - Requirements for Specified Fumigants) Amendment Safe Work Instrument (No 2) 2022, p.4  
> inserted After new clause 18, insert: Requirements applying to Tri-Form 80 19 Tri-Form 80 required to comply with specified regulations (1) Tri-Form 80 is required to comply with: (a) regulation 14.4 of the Regulations, under regulation 14.4(1)(c) of the Regulations: (b) regulation 14.20 of the Regulations, under regulation 14.20(1)(c) of the Regulations: (c) regulation 14.21 of the Regulations, u

**[5]** `72527-00136` — Interpretive guidelines – The Health and Safety at Work (Asbestos) Regulations 2016, p.86  
> sure there are decontamination facilities The PCBU for which asbestos-related work is carried out must ensure there are facilities available to decontaminate the asbestos-related work area, any plant used in that area and workers carrying out that work. There are requirements to meet before items contaminated with asbestos are removed from the work area (regulation 52). 12.9 12.1 84

**[6]** `2-00115` — ACOP: Pressure equipment (excluding boilers), p.84  
> 84 APPROVED CODE OF PRACTICE FOR PRESSURE EQUIPMENT APPENDIX D: MANUFACTURER’S DATA REPORTS D1. The manufacturer’s data reports shall be completed for all equipment in accordance with the requirements of the relevant manufacturing standard. D2. Where the manufacturing standard does not specify the preparation of a data report then the report included in this appendix shall be completed for equipme

```yaml
id: id003
grounded: yes
citations: valid
modality: na
complete: na
drift: none
refusal: correct
human:
notes: same ambiguity as id001 - MOQO Reg 84 vs Electricity (Safety) Reg 84. correctly enumerated rather than guessing
```

---

## 34. `id004` [identifier]

**Q:** what does Regulation 35A require

### Answer

The sources provided do not contain the specific requirements of Regulation 35A itself. 

The sources only mention that Regulation 35A of the Geothermal Energy regulations is one of the regulations under which notifiable incidents must be reported to WorkSafe [1][3][4][5], but they do not detail what Regulation 35A actually requires.

To answer your question about what Regulation 35A requires, you would need to consult the Geothermal Energy regulations directly.

### Sources given to the model

**[1]** `72431-00044` — High Hazards and Petroleum and Geothermal team – A year in review 2024/25, p.30  
> section 24(1) of the Act, regulation 70 of the Petroleum Exploration and Extraction regulations, regulation 33 of the Major Hazard Facility regulations, and regulation 35A of the Geothermal Energy regulations. Figure 3 shows the number of notifiable incidents at high hazard sites between July 2017 and June 2025. The number of notifiable incidents reported indicates an improved understanding by ope

**[2]** `22496-00004` — Policy clarification: Storing class 6 and 8 hazardous substances, p.2  
> substance location is, and complies with the requirements for, one of the following: a. a store for class 6 or 8 substances other than an indoor storage cabinet (regulation 13.35), or b. an indoor storage cabinet for class 6 substances (regulation 13.36), or c. an indoor storage cabinet for class 8 substances (regulation 13.37). The requirements for indoor storage cabinets are defined in the Regul

**[3]** `63565-00019` — Major Hazard Facilities, Petroleum, and Geothermal annual report 2022–23, p.16  
> 1.0 Review of the past year Notifiable incidents Notifiable incidents, known to high hazard industries as ‘near-misses’ or ‘precursor events’ must be reported to WorkSafe under section 24(1) of the Act, regulation 70 of the Petroleum Exploration and Extraction (PEE) regulations, regulation 33 of the MHF regulations, and regulation 35A of the Geothermal Energy regulations. Figure 6 shows the number

**[4]** `69276-00025` — Major Hazard Facilities, Petroleum, and Geothermal annual report 2023–24, p.19  
> 1.0 Review of the past year Notifiable incidents Notifiable incidents, known to high hazard industries as ‘near-misses’ or ‘precursor events’ must be reported to WorkSafe under section 24(1) of the Act, regulation 70 of the Petroleum Exploration and Extraction regulations, regulation 33 of the MHF regulations, and regulation 35A of the Geothermal Energy regulations. Figure 7 shows the number of no

**[5]** `56547-00017` — Major Hazard Facilities, Petroleum, and Geothermal annual report 2021–22, p.17  
> 2.0 Review of the past year Notifiable incidents Notifiable incidents, known to high hazard industries as ‘near-misses’ or ‘precursor events’ must be reported to WorkSafe under section 24(1) of the Act, regulation 70 of the PEE regulations, regulation 33 of the MHF regulations, and regulation 35A of the Geothermal Energy regulations. Figure 5 shows the number of notifiable incidents at high hazard

**[6]** `5361-00056` — Draft - Health and Safety at Work (Hazardous Substances - Location Compliance Certification for classes 2 to 6 and 8) Performance Standard 2019, p.30  
> whether the requirements of regulation 11.30 have been met for the purposes of 10.34(1)(j) when a class 3.1A, 3.1B, or 3.1C substance is located in a package in a building or an external storage area. (2) The compliance certifier must— (a) take the action in column 3 of table 2.13; and (b) make and retain the records specified in column 4 of table 2.13. Table 2.13 Regulation Action Records 11.30 V

```yaml
id: id004
grounded: yes
citations: valid
modality: na
complete: na
drift: none
refusal: correct
human:
notes: correct refusal: sources only cite Reg 35A as a reporting trigger, never state its content
```

---

## 35. `id005` [identifier]

**Q:** what does Regulation 73A require

### Answer

# What Regulation 73A Requires

According to the sources, Regulation 73A sets the principal requirements for persons connecting an electrical installation to a supply of electricity [1][3]. It "brings together all the elements that control the safety of an electrical installation" [1][3].

Before connecting a low or extra-low voltage installation or part installation on which prescribed electrical work has been done, the person doing the connection must be satisfied that [1]:

- the installation is safe to connect
- the testing required by the electricity regulations has been done
- a Certificate of Compliance (CoC) has been completed for all the prescribed electrical work performed in New Zealand
- if the work is required to be inspected, a Record of Inspection (RoI) has been prepared for that work

For low voltage installations specifically, Regulation 73A(1)(e) requires the person doing the connection to "ensure that the polarity and phase rotation of the supply are correct" [2].

The sources note that "connection" refers to the prescribed electrical work that is "the final step that will allow electricity to flow in the electrical installation or part installation on which other prescribed electrical work has been done" [2][3].

The sources do not provide the complete text of all of Regulation 73A's requirements; they refer readers to "see regulation 73A of the Regulations for the full requirements" [1].

### Sources given to the model

**[1]** `66840-00023` — Electrical safety for low voltage electrical installations in imported buildings, p.20  
> Step 4: Connect the electrical installation to an electricity supply Once steps 1 to 3 have been completed, the connection can be carried out as per the requirements of regulation 73A Regulation 73A sets the principal requirements for persons connecting an electrical installation to a supply of electricity. This regulation brings together all the elements that control the safety of an electrical i

**[2]** `52237-00002` — Safety alert - Serious incidents resulting from the use of live polarity testing, p.2  
> worksafe.govt.nz 0800 030 040 2/2 Energy Safety advice The following apply when doing a connection on an electrical installation as required by the Electrical (Safety) Regulations 2010: – Regulation 73A (1) of the Electricity (Safety) Regulations 2010 requires before connecting to a power supply a low or extra-low voltage installation or part installation on which prescribed electrical work has be

**[3]** `66840-00030` — Electrical safety for low voltage electrical installations in imported buildings, p.25  
> 3) for the electrical installation. It is important that the mains work CoC and RoA adequately describe the parts of the installation covered by them. Note: Details of high-risk PEW (including details of the CoC provided in respect of that work) must be lodged on the database referred to in regulation 112A of the Regulations (Electricity and Gas High-risk database) by the person who inspected the 

**[4]** `626-00045` — Designing, installing and maintaining safe electrical and gas installations and distribution systems, p.30  
> this must be issued after the connections are carried out (Regulation 74A). When you have connected it and are satisfied that the tests, such as polarity, are correct and it will be safe for use, sign off the ESC AND > > ensure that when connecting the power supply, it is subject to provisions of amendment Regulation 73A (2) of Regulation 38 (2) > > be satisfied that tests have been carried out to

**[5]** `626-00039` — Designing, installing and maintaining safe electrical and gas installations and distribution systems, p.27  
> 25 SECTION 4.0 // SAFETY OF ELECTRICAL INSTALLATIONS AND WORKS 25 > > the installation or part installation is safe to use, on the grounds that is electrically safe complies with these regulations; and > > where the prescribed electricity work comprised the maintenance or alteration of, or the addition to, the installation or part installation, the work has not adversely affected any other part of

**[6]** `626-00040` — Designing, installing and maintaining safe electrical and gas installations and distribution systems, p.27  
> a RoI and an entry in the online Electricity and Gas High-risk Database. If the installation of the meter is the connection of the installation, then the connection is subject to the verification provisions of Regulations 73A, and an ESC must also be issued after the connections are carried out. PERIODIC VERIFICATION A person who owns or operates works, installations, fittings, or appliances must 

```yaml
id: id005
grounded: yes
citations: valid
modality: correct
complete: yes
drift: none
refusal: na
human:
notes: answered: Reg 73A covers connecting an installation to supply. verified in [1][3]
```

---

## 36. `id006` [identifier]

**Q:** what does Regulation 1 require

### Answer

The sources provided do not contain information about what "Regulation 1" requires. 

The sources reference various regulations (such as Regulation 10, Regulation 60, Regulation 9, etc.) but do not include the text of Regulation 1 or describe its requirements.

To answer your question, I would need a source that covers Regulation 1.

### Sources given to the model

**[1]** `69621-00005` — How to use the quantity-ratio sum (QRS) to work out whether a workplace requires a ‘hazardous substance location’ (HSL) or a location compliance certificate (LCC), p.6  
> 3.0 When does this guidance not apply? This guidance does not cover class 1 explosives. Regulation 10(6) describes the QRS requirements for explosives. Where compliance certification is required at any amount of a substance or based on the capacity of the container (for example, certification of tank wagons or stationary containers systems), the QRS will not need to be applied. An example of this 

**[2]** `73123-00001` — Ethanol-water dilutions intended for drinking – regulatory clarification, p.1  
> Regulation 1.9(3) provides alternative requirements for EWD if the EWD is contained and stored as follows: – the substance is stored in containers at premises used for storing or handling (including processing) EWD, and – the containers are constructed in accordance with sections F4.1-F4.5 and F4.7 of Appendix F of AS 1940:2017, and – the areas at the premises where the EWD is stored or handled (i

**[3]** `626-00028` — Designing, installing and maintaining safe electrical and gas installations and distribution systems, p.21  
> be applied. Part 1 cannot be applied for: > > Domestic installations with maximum demand up to 80A single phase or 50A Multi–phase. These installations MUST comply with Part 2 (Regulation 60(1)). > > Specific high-risk installations (medical, mobile medical, connectable, shows and carnivals, hazardous areas, marinas). These installations MUST comply with AS/NZS 3000 Part 2 and the relevant Compani

**[4]** `5361-00023` — Draft - Health and Safety at Work (Hazardous Substances - Location Compliance Certification for classes 2 to 6 and 8) Performance Standard 2019, p.13  
> or 4 substance is present, the requirements of regulation 10.26(2) have been met for the purposes of— (i) regulation 10.34(1)(a), for a class 2 or 3.1 substance; and (ii) regulation 10.36(1)(a), for a class 3.2 or 4 substance; and (b) in relation to a hazardous substance location where a class 5.1.1 or 5.1.2 substance is present, the requirements of regulation 12.8(4) have been met for the purpose

**[5]** `3504-00003` — Electrical and gas safety requirements for caravan, motorhome and boating, p.5  
> 1.0 Gas regulations overview The Gas (Safety & Measurement) Regulations 2010 require that all gas appliances and fittings are capable of operating safely when installed correctly and used for their intended purpose. They also set out a general requirement for safety, defining what is deemed to be unsafe. A person who owns, supplies, sells, hires or operates an installation in a recreational vehicl

**[6]** `5361-00056` — Draft - Health and Safety at Work (Hazardous Substances - Location Compliance Certification for classes 2 to 6 and 8) Performance Standard 2019, p.30  
> whether the requirements of regulation 11.30 have been met for the purposes of 10.34(1)(j) when a class 3.1A, 3.1B, or 3.1C substance is located in a package in a building or an external storage area. (2) The compliance certifier must— (a) take the action in column 3 of table 2.13; and (b) make and retain the records specified in column 4 of table 2.13. Table 2.13 Regulation Action Records 11.30 V

```yaml
id: id006
grounded: yes
citations: valid
modality: na
complete: na
drift: none
refusal: correct
human:
notes: correct refusal. NOTE: 'Regulation 1' is almost certainly a bad auto-generated question - definitions/interpretation clauses are not substantive requirements
```

---

## 37. `id007` [identifier]

**Q:** what is set out in Section 57

### Answer

The sources indicate that Section 57 of the Health and Safety at Work Act 2015 relates to "Requirement to keep records" [1][3][4], but the sources do not provide the specific details of what Section 57 actually sets out.

To find out the exact requirements in Section 57, you would need to consult the Health and Safety at Work Act 2015 itself or WorkSafe's detailed guidance on record-keeping obligations.

### Sources given to the model

**[1]** `113-00136` — ACOP: Ground or strata instability in underground mines or tunnels, p.88  
> EXTRACTIVES: GROUND OR STRATA INSTABILITY IN UNDERGROUND MINES AND TUNNELS 88 The legislation that applies to this section is: Health and Safety at Work Act 2015 Section 23 Meaning of notifiable injury or illness Section 24 Meaning of notifiable incident Section 25 Meaning of notifiable event Section 55 Duty to preserve sites Section 56 Duty to notify notifiable event Section 57 Requirement to kee

**[2]** `824-00051` — Introduction to the Health and Safety at Work Act 2015 - special guide, p.34  
> 32 32 Notifications and authorisations IN THIS PART: Section 4: Notifications and authorisations NOTIFIABLE EVENTS 4.1 When must PCBUs notify the regulator? 4.2 What does a PCBU need to do if a notifiable event occurs (sections 55-57 of HSWA)? 4.3 Investigating notifiable events AUTHORISATIONS AND OTHER NOTIFICATIONS 4.4 What are authorisations and when are they needed? 4.5 WorkSafe needs to be to

**[3]** `155-00097` — Emergency preparedness in mining and tunnelling operations, p.61  
> SECTION 10.0 // NOTIFICATIONS AND NOTIFIABLE EVENTS The mine or tunnel operator must inform WorkSafe about particular work activities and notifiable events within specified timescales. For more information on notifications see WorkSafe’s special guide Introduction to the Health and Safety at Work Act 2015. 10.1 NOTIFIABLE EVENTS The legislation that applies in this section is: Health and Safety at

**[4]** `170-00097` — ACOP: emergency preparedness in mining and tunnelling operations, p.61  
> SECTION 10.0 // NOTIFICATIONS AND NOTIFIABLE EVENTS The mine or tunnel operator must inform WorkSafe about particular work activities and notifiable events within specified timescales. For more information on notifications see WorkSafe’s special guide Introduction to the Health and Safety at Work Act 2015. 10.1 NOTIFIABLE EVENTS The legislation that applies in this section is: Health and Safety at

**[5]** `20130-00058` — Worker engagement, participation and representation, p.37  
> 4.0 Worker participation practices IN THIS SECTION: 4.1 Worker participation practices (section 61 of HSWA) 4.2 Workers should know that their participation counts 4.3 Making a decision on a health and safety matter 4.4 Demonstrating commitment to worker participation 4.5 Prohibition of adverse, coercive or misleading conduct against a worker (sections 88–97 of HSWA) 35

**[6]** `824-00006` — Introduction to the Health and Safety at Work Act 2015 - special guide, p.6  
> NOTIFICATIONS AND AUTHORISATIONS 4.0 Notifications and authorisations 34 4.1 When must PCBUs notify the regulator? 35 4.2 What does a PCBU need to do if a notifiable event occurs (sections 55-57 of HSWA)? 37 4.3 Investigating notifiable events 38 4.4 What are authorisations and when are they needed? 38 4.5 WorkSafe needs to be told about certain work activities before the work begins 39 OFFICERS 5

```yaml
id: id007
grounded: yes
citations: valid
modality: na
complete: na
drift: none
refusal: correct
human:
notes: partial: correctly identified Section 57 as 'Requirement to keep records' from the sources, then declined on detail. honest boundary
```

---

## 38. `id008` [identifier]

**Q:** what is set out in Section 96B

### Answer

The sources provided do not contain detailed information about what is set out in Section 96B itself.

The sources only reference Section 96B of the Hazardous Substances and New Organisms Act 1996 in the context of prescribed exposure standards. They indicate that "a group standard approval issued under section 96B" is one of the ways a prescribed exposure standard can be prescribed [2][3][5][6].

To find out what Section 96B specifically sets out, you would need to consult the Hazardous Substances and New Organisms Act 1996 itself, which is not provided in these sources.

### Sources given to the model

**[1]** `131-00020` — ACOP: Air quality in the extractives industry, p.17  
> SECTION 1.0 // INTRODUCTION > > an approval or a reassessment in accordance with section 77B of the Hazardous Substances and New Organisms Act 1996 > > a group standard approval issued under section 96B of the Hazardous Substances and New Organisms Act 1996. To find out if a substance has a prescribed exposure standard, you can: > > Go to the controls database on the Environmental Protection Autho

**[2]** `20227-00074` — General risk and workplace management - part 1, p.51  
> Appendices TERM DEFINITION Prescribed exposure standard (from GRWM Regulations) Means a workplace exposure standard or a biological exposure index that has the purpose of protecting persons in a workplace from harm to health and that is prescribed in— (a) regulations; or (b) a safe work instrument; or (c) a control under section 77 or 77A, or an exposure limit under section 77B, of the Hazardous S

**[3]** `21444-00003` — Appendix A: Glossary, p.2  
> Appendices TERM DEFINITION Prescribed exposure standard (from GRWM Regulations) Means a workplace exposure standard or a biological exposure index that has the purpose of protecting persons in a workplace from harm to health and that is prescribed in— (a) regulations; or (b) a safe work instrument; or (c) a control under section 77 or 77A, or an exposure limit under section 77B, of the Hazardous S

**[4]** `62251-00102` — Workplace exposure standards (WES) and biological exposure indices (BEI) – 16th edition, p.84  
> Appendix TERM DEFINITION PES A prescribed workplace exposure standard or biological exposure index that has the purpose of protecting persons in a workplace from harm to health. PES are prescribed in: (i) regulations (ii) a safe work instrument, or (iii) the Hazardous Substances and New Organisms Act 1996 as a control under section 77 or 77A, or an exposure limit under section 77B or a group stand

**[5]** `20529-00035` — General risk and workplace management - part 2, p.24  
> 3.0 Risks to be managed under the GRWM Regulations A WES for a substance refers to the airborne concentration of a substance at which it is believed nearly all workers can be repeatedly exposed to day after day without coming to harm. Compliance with the WES level does not guarantee that all workers are protected from discomfort or ill-health. The range of individual susceptibility to hazardous an

**[6]** `20529-00041` — General risk and workplace management - part 2, p.28  
> Appendix TERM DEFINITION Plant (from section 16 of HSWA) Includes— (a) any machinery, vehicle, vessel, aircraft, equipment (including personal protective equipment), appliance, container, implement, or tool; and (b) any component of any of those things; and (c) anything fitted or connected to any of those things. Prescribed exposure standard (from GRWM Regulations) Means a workplace exposure stand

```yaml
id: id008
grounded: yes
citations: valid
modality: na
complete: na
drift: none
refusal: correct
human:
notes: correct refusal: sources cite s96B HSNO only as a route by which standards are prescribed
```

---

## 39. `id009` [identifier]

**Q:** what is set out in Section 77

### Answer

The sources provided do not contain the full text of Section 77. 

Section 77 is referenced in sources [2], [3], and [6] in relation to the Hazardous Substances and New Organisms Act 1996 (HSNO Act), where it is mentioned as a source for prescribing controls or exposure limits related to hazardous substances. However, the sources do not detail what Section 77 itself sets out.

To answer your question fully, you would need to consult the Hazardous Substances and New Organisms Act 1996 directly.

### Sources given to the model

**[1]** `61708-00033` — Reserve judgement: WorkSafe New Zealand v Sand Safaris 2014 Limited, p.20  
> [76] WorkSafe made extensive submissions on how the question of reasonable practicability is to be assessed. Section 22 provides the following definition of reasonably practicable: 22 Meaning of reasonably practicable In this Act, unless the context otherwise requires, reasonably practicable, in relation to a duty of a PCBU set out in subpart 2 of Part 2, means that which is, or was, at a particul

**[2]** `20227-00074` — General risk and workplace management - part 1, p.51  
> Appendices TERM DEFINITION Prescribed exposure standard (from GRWM Regulations) Means a workplace exposure standard or a biological exposure index that has the purpose of protecting persons in a workplace from harm to health and that is prescribed in— (a) regulations; or (b) a safe work instrument; or (c) a control under section 77 or 77A, or an exposure limit under section 77B, of the Hazardous S

**[3]** `21444-00003` — Appendix A: Glossary, p.2  
> Appendices TERM DEFINITION Prescribed exposure standard (from GRWM Regulations) Means a workplace exposure standard or a biological exposure index that has the purpose of protecting persons in a workplace from harm to health and that is prescribed in— (a) regulations; or (b) a safe work instrument; or (c) a control under section 77 or 77A, or an exposure limit under section 77B, of the Hazardous S

**[4]** `58975-00016` — WorkSafe New Zealand v Chunda Limited and JMK Homes Limited, p.14  
> (e) The payment is to be made periodically on the basis that I have already set out in this decision. [74] I turn to JMK Homes Limited. [75] JMK was an offsite property developer that contracted Chunda. That does not absolve it from responsibility. Section 38 of the Act makes that clear. [76] The need for oversight is acknowledged by the fact that Mr Yang was overseeing the project remotely. [77] 

**[5]** `2278-00005` — HSNOCOP 44: Below ground stationary container systems for petroleum – design and installation, p.7  
> of this Code are complied with:  Clause 33(a): o sections 10 and 13 of this Code  Clause 73(3)(a)(iii) o section 11 and 12 of this Code This publication is approved as a means of compliance with:  clause 73(4)(b) for pipework, and  clause 77 which specifies markings on the tank, and  clause 81(1) which specifies markings, and  clauses 32, 34, 35, 35A and 36 of Schedule 8 of the Hazardous Sub

**[6]** `20529-00035` — General risk and workplace management - part 2, p.24  
> 3.0 Risks to be managed under the GRWM Regulations A WES for a substance refers to the airborne concentration of a substance at which it is believed nearly all workers can be repeatedly exposed to day after day without coming to harm. Compliance with the WES level does not guarantee that all workers are protected from discomfort or ill-health. The range of individual susceptibility to hazardous an

```yaml
id: id009
grounded: yes
citations: valid
modality: na
complete: na
drift: none
refusal: correct
human:
notes: correct refusal, correctly attributed s77 to the HSNO Act
```

---

## 40. `id010` [identifier]

**Q:** what is set out in Section 78

### Answer

The sources provided do not explain what is set out in Section 78. 

The sources only reference that codes of practice are "approved pursuant to Sections 78 and 79" of the Hazardous Substances and New Organisms Act 1996 [1][2][5][6], but they do not describe the content or requirements of Section 78 itself.

To answer your question, you would need to consult the Hazardous Substances and New Organisms Act 1996 directly.

### Sources given to the model

**[1]** `2086-00001` — HSNOCOP 29: Flammable gases and oxygen tank wagons, p.2  
> 2 Flammable Gases and Oxygen Tank Wagons HSNO COP 29 June 2013 EPA0235 Preface This code of practice HSNO COP 29 version 2.0 Flammable Gases and Oxygen Tank Wagons is approved pursuant to Sections 78 and 79 of the Hazardous Substances and New Organisms Act 1996 (HSNO Act). It is confirmed that the requirements of Sections 78 and 79 have been met. Approval of this code is limited to those matters t

**[2]** `2266-00001` — HSNOCOP 18-3: Retail fireworks, p.2  
> HSNOCOP 18-3 Page 2 of 37 August 2008 PREFACE This Code of Practice (HSNOCOP 18-3) is approved pursuant to Sections 78 and 79 of the Hazardous Substances and New Organisms Act. The Environmental Risk Management Authority has delegated the power to approve codes of practice to the Chief Executive of the Authority, and this Code of Practice is approved in accordance with that delegation. It is confi

**[3]** `8-00102` — ACOP: Management and removal of asbestos, p.80  
> APPROVED CODE OF PRACTICE // MANAGEMENT AND REMOVAL OF ASBESTOS 78 The legislation that applies in this section is: Health and Safety at Work Act 2015 Section 34 PCBUs must consult with other PCBUs on the same duty Section 36(3)(f) Primary duty of care (provision of information, training, instruction or supervision) Section 168 Powers of entry and inspection Health and Safety at Work (Asbestos) Re

**[4]** `2164-00001` — HSNOCOP 63: Management and handling of used oil, p.2  
> 2 HENOCOP 63 Management and Handling of Used Oil Code of Practice November 2013 Approval of code of practice This code of practice HSNOCOP 63 Management and Handling of Used Oil is approved pursuant to Sections 78 and 79 of the Hazardous Substances and New Organisms Act. It is confirmed that the requirements of Sections 78 and 79 have been met. This code of practice is approved as a means of compl

**[5]** `2095-00001` — Code of practice for outdoor pyrotechnic displays, p.2  
> 2 Outdoor pyrotechnic displays October 2012 EPA0192 Preface This Code of Practice entitled Outdoor pyrotechnic displays is approved as a Code of Practice under Sections 78 and 79 of the Hazardous Substances and New Organisms (HSNO) Act. The Environmental Protection Authority (EPA) has delegated the power to approve Codes of Practice to the Chief Executive of the EPA, and this code is approved in a

**[6]** `2263-00001` — HSNOCOP 30: Outdoor pyrotechnic displays, p.2  
> 2 Outdoor pyrotechnic displays October 2012 EPA0192 Preface This Code of Practice entitled Outdoor pyrotechnic displays is approved as a Code of Practice under Sections 78 and 79 of the Hazardous Substances and New Organisms (HSNO) Act. The Environmental Protection Authority (EPA) has delegated the power to approve Codes of Practice to the Chief Executive of the EPA, and this code is approved in a

```yaml
id: id010
grounded: yes
citations: valid
modality: na
complete: na
drift: none
refusal: correct
human:
notes: correct refusal: sources only say codes are approved 'pursuant to Sections 78 and 79'
```

---

## 41. `id011` [identifier]

**Q:** what is set out in Section 83

### Answer

Based on the sources provided, Section 83 of the Health and Safety at Work Act (HSWA) sets out **the right of a worker to cease or refuse to carry out unsafe work** [1].

Specifically, Section 83 covers:

- A worker can refuse to carry out work or stop work they are doing if they believe that carrying out the work would expose them or someone else to a serious health and safety risk caused by:
  - immediate exposure to a hazard, or
  - because they will very soon be exposed to a hazard [1]

The sources also note that Section 83 does not apply to members of the Armed Forces [5][6].

### Sources given to the model

**[1]** `20225-00062` — Worker representation through Health and Safety Representatives and Health and Safety Committees, p.40  
> PIN must be treated as an improvement notice issued by the inspector under HSWA. The inspector must give a copy of their decision (either in person or some other way, in accordance with section 116) to: a. the person who asked for the PIN to be reviewed, and b. the HSR who issued the PIN. Ceasing (stopping) unsafe work H Meaning of cease work Section 82 Right of worker to cease or refuse to carry 

**[2]** `71736-00117` — Approved code of practice: Safe practice for forestry and harvesting operations, p.85  
> 83 83 14.0 Introduction to Part C IN THIS SECTION: 14.1 What does this Part cover? 14.2 What are the common health and safety risks faced by workers constructing or using access roads and landing sites?

**[3]** `71760-00002` — Part C: Site access and preparation of log landings, p.3  
> 83 83 14.0 Introduction to Part C IN THIS SECTION: 14.1 What does this Part cover? 14.2 What are the common health and safety risks faced by workers constructing or using access roads and landing sites?

**[4]** `20130-00013` — Worker engagement, participation and representation, p.8  
> the election of HSRs (section 62(1)), the establishment of an HSC (section 66(1)(b)), and the worker’s right to cease unsafe work or for an HSR to direct unsafe work to cease (sections 83 and 84). Worker participation practices See Section 4 Worker participation practices are what the PCBU puts in place so that workers can help to improve work health and safety on an ongoing basis. These practices

**[5]** `20225-00012` — Worker representation through Health and Safety Representatives and Health and Safety Committees, p.7  
> The worker engagement, participation and representation part of HSWA does not apply to: – a volunteer worker – a worker who is a prisoner carrying out work inside a prison. 2. Certain sections of the worker engagement, participation and representation part of HSWA do not apply to members of the Armed Forces. These relate to requests for the election of HSRs (section 62 (1)), the establishment of a

**[6]** `20130-00022` — Worker engagement, participation and representation, p.15  
> that the PCBU may not be aware of – prioritise the health and safety matters that need to be addressed – reduce work-related injuries and illnesses – increase productivity, efficiency and quality – motivate the workforce – boost cooperation and trust between workers and PCBUs – and strengthen working relationships – increase workers’ awareness about work health and safety matters – strengthen work

```yaml
id: id011
grounded: yes
citations: valid
modality: correct
complete: yes
drift: none
refusal: na
human:
notes: BEST identifier answer: s83 HSWA = right to cease or refuse unsafe work. substantively correct and verified
```

---

## 42. `id012` [identifier]

**Q:** what is set out in Section 55

### Answer

The sources provided do not contain information about what is "set out in Section 55" as a distinct topic. 

Section 55 appears only as page number references in the headers of these document excerpts (showing "55 SECTION X.0"). The actual content shown relates to various topics like Mobile Elevating Work Platforms, Scaffolding, hazardous substances definitions, performance monitoring, and forestry operations—but these are not described as being "Section 55" content.

To answer your question accurately, I would need a source that explicitly describes what Section 55 contains.

### Sources given to the model

**[1]** `26-00084` — Mobile elevating work platforms, p.57  
> 55 SECTION 7.0 // APPENDICES Crushing hazards > > Have a traffic management plan and set up exclusion zones. > > Keep all staff away when raising, lowering or slewing the MEWP. > > Make sure there is enough overhead clearance when using the MEWP. Consider how high any boom lifts go when driving over drop offs, kerbs, gutters etc? > > Operators must never put themselves under, through or between bo

**[2]** `19966-00082` — Scaffolding in New Zealand, p.57  
> 55 SECTION 8.0 // ERECTING THE SCAFFOLD 55 > If the scaffold is erected adjacent to or over public spaces or adjoining property specific controls like hoardings, catch fans or barricades with clear signs should be provided. Catch platforms should be designed to support a uniformly distributed load of not less than 5 kPa. > The bottom lift should have a maximum height of 3 m, and all other lifts sh

**[3]** `95-00093` — MHF: Safety assessment, p.57  
> 55 SECTION 6.0 // APPENDICES 55 TERM BRIEF EXPLANATION Safety management system (SMS) Defined in the MHF Regulations, generally a comprehensive integrated system for managing all aspects of risk control at a MHF and used by the operator as the primary means of ensuring safe operation of the MHF. Safety-critical element Defined in the MHF Regulations, means any part of a facility or its plant (incl

**[4]** `71-00089` — MHF: Major Accident Prevention Policy and Safety Management Systems, p.57  
> SECTION 10.0 // PERFORMANCE MONITORING 55 55 10.3 PERFORMANCE MONITORING OF SMS ELEMENTS Performance monitoring involves developing detailed performance standards for measuring the effectiveness of the SMS. You can use a performance standard to establish the level of performance required for elements of the SMS. A comprehensive set of workable performance standards appropriate to the MHF will be n

**[5]** `71736-00083` — Approved code of practice: Safe practice for forestry and harvesting operations, p.57  
> 55 5.0 Introduction to Part B 55 What does this Part cover? 5.1.1 This Part provides guidance on: – safe worker – general workplace requirements and facilities – first aid – emergency plans – personal protective equipment (PPE) – training, information, instruction and supervision – communications – alcohol and drugs – mobile plant. 5.1

**[6]** `71754-00002` — Part B: General requirements, p.4  
> 55 5.0 Introduction to Part B 55 What does this Part cover? 5.1.1 This Part provides guidance on: – safe worker – general workplace requirements and facilities – first aid – emergency plans – personal protective equipment (PPE) – training, information, instruction and supervision – communications – alcohol and drugs – mobile plant. 5.1

```yaml
id: id012
grounded: yes
citations: valid
modality: na
complete: na
drift: none
refusal: correct
human: disagree
notes: HUMAN DISAGREES (Ben) - and is right to. These documents do carry page headers of the form '55 SECTION 7.0 //', so the model's explanation may well be accurate for the six chunks it was actually given. Downgrading my 'FABRICATED EXPLANATION' claim to unverified. Ben's more useful point: the explanation should not be there AT ALL. A user never sees the sources, so describing their layout leaks implementation detail instead of answering.
```

---

## 43. `id013` [identifier]

**Q:** Table A2

### Answer

I can see references to "Table A2" in the sources provided, but I need clarification about what specific information you're seeking.

The sources contain multiple tables labeled as part of "Appendix 2: NHEWS Occupational distribution within industry group" [2][3]:

- Table A2.1: Occupational distribution: Health & Community Services [3]
- Table A2.2: Occupational distribution: Manufacturing [3]
- Table A2.3: Occupational distribution: Construction [3]
- Table A2.4: Occupational distribution: Accommodation, Cafes & Restaurants [1]
- Table A2.5: Occupational distribution: Finance & Insurance [1]
- Table A2.6: Occupational distribution: Agriculture, Forestry & Fishing [1]

**What specific information from Table A2 would you like me to provide?** For example, are you asking about occupational distributions in a particular industry, or something else?

### Sources given to the model

**[1]** `5444-00211` — Worker Exposure Survey Report - Part 2, p.161  
> 161 Occupation % Caterer/cook 22 Bar tender/waiter 13 Manager/director 11 Cleaner/housekeeper 9 Assistant Various 8 Kitchen hand 7 Office worker 5 Note: All others below 5% Table A2.4: Occupational distribution: Accommodation, Cafes & Restaurants (n=91) Occupation % Accountant/financial advisor 30 Manager/director 18 Banking 10 Officer/various 9 Customer service 7 Office worker 5 Note: All others 

**[2]** `5444-00009` — Worker Exposure Survey Report - Part 2, p.7  
> 7 Table 9G: Psychosocial working conditions – Part 1 125 Table 10G: Psychosocial working conditions – Part 2 127 Key observations 128 Limitations 131 Summary 134 References 138 Appendices 140 Appendix 1: Worker Exposure Survey Questionnaire 141 Appendix 2: NHEWS Occupational distribution within industry group 160 Table A2.1: Occupational distribution: Health & Community Services 160 Table A2.2: Oc

**[3]** `5444-00210` — Worker Exposure Survey Report - Part 2, p.160  
> 160 Appendix 2: NHEWS Occupational distribution within industry group Occupation % Nurse 23 Childcare worker 9 Carer 9 Office worker 8 Community services/social worker 7 Medical industry worker 7 Manager/director 5 Note: All others below 5% Table A2.1: Occupational distribution: Health & Community Services (n=956) Occupation % Labourer/process worker 12 Manager/director 10 Machine operator 10 Offi

**[4]** `1574-00059` — New Zealand Electrical Code of Practice for repair and maintenance of domestic electrical appliances by the owner of the appliance (NZECP 50: 2004), p.50  
> A2.2 Fuses and circuit-breakers on switchboards are normally labelled (below each fuse or circuit-breaker) with the type of circuit they control, see Table 4. A2.3 The number of fuses and/or circuit-breakers on the main switchboard will depend on the number of circuits in the electrical installation. However, in general, there will be: (a) A least 2 lighting circuits; (b) Any number of socket-outl

**[5]** `1580-00077` — New Zealand Electrical Code of Practice for homeowner/occupier's electrical wiring work in domestic installations (NZECP 51: 2004), p.72  
> A2.2 Fuses and circuit-breakers on switchboards are normally labelled (below each fuse or circuit-breaker) with the type of circuit they control, see Table 12. A2.3 The number of fuses and/or circuit-breakers on the main switchboard will depend on the number of circuits in the electrical installation. However, in general, there will be: (a) At least 2 lighting circuits; (b) Any number of socket-ou

**[6]** `29-00012` — Safe use of safety nets, p.12  
> BEST PRACTICE GUIDELINES // SAFE USE OF SAFETY NETS 10 Table 1 sets out the net classifications. Class Energy absorption capacity (kJ) Mesh size (mm) A1 2.3 60 A2 2.3 100 B1 4.4 60 B2 4.4 100 Table 1: Classification of nets according to energy absorption capacity and mesh size. Both classes A1 and A2 nets are suitable for system S safety nets. Class A2 nets (2.3 kJ energy absorption capacity and 1

```yaml
id: id013
grounded: yes
citations: valid
modality: na
complete: na
drift: none
refusal: correct
human:
notes: asked for clarification and enumerated the Table A2.x variants found. reasonable given a two-word query
```

---

## 44. `id014` [identifier]

**Q:** Table 27

### Answer

I cannot find Table 27 in the sources provided. The sources contain tables numbered up to Table 19 (in source [6]), but Table 27 is not included in any of the documents you've provided.

If you need information from Table 27, please provide the source document that contains it.

### Sources given to the model

**[1]** `60496-00000` — Summary of submissions - Proposed changes to safety audit standard for adventure activities, p.2  
> CONTENTS Submissions received 1 General observations 1 Specific observations 1 tables 1 Analysis of comments from submitters on proposed changes to content 2 2 Analysis of general comments from submitters on the consultation document 26 3 Consequential amendments to content (not consulted on) 27

**[2]** `1679-00026` — Operator protective structures on self-propelled mobile mechanical plant, p.27  
> OPERATOR PROTECTIVE STRUCTURES ON SELF-PROPELLED MOBILE MECHANICAL PLANT 27 Only operators with suitable training and experience shall operate machinery in medium-risk and high-risk areas (see Tables 1A and 1B). It is recommended that operators wear protective helmets while operating machinery.

**[3]** `1106-00048` — New Zealand Adventure Activity Certification Scheme - a performance study, p.29  
> at 12%. Table 15: Level of Value Gained from the Safety Audit Standard: Staff Safety Standard Section High Moderate Low None N N % N % N % N % 2. Safety Management System Requirements 34 24 38 27 46 33 22 16 140 3. Leadership and Management 36 26 42 31 36 26 23 17 137 4. Hazard Management 36 27 42 31 35 26 22 16 135 5. Standard Operating Procedures 44 33 39 29 30 22 21 16 134 6. Emergency Prepared

**[4]** `812-00005` — Offences and penalties under the Health and Safety at Work Act 2015, p.3  
> done or provided under HSWA (section 27 of HSWA). The maximum penalties are shown in Table 2. OFFENCE INDIVIDUAL PCBU (EG A SELF-EMPLOYED PCBU) OTHER PCBU (EG AN ORGANISATION THAT IS A PCBU) Section 27 (PCBUs must not levy workers) $5,000 fine $25,000 fine Table 2: Maximum penalties for charging workers OFFENCES IN RELATION TO NOTIFIABLE EVENTS Notifiable events include someone’s death, a notifiab

**[5]** `1106-00047` — New Zealand Adventure Activity Certification Scheme - a performance study, p.29  
> 29 Table 14: Level of Value Gained from the Safety Audit Standard: Participant Safety High Moderate Low None N Standard Section N % N % N % N % 2. Safety Management System Requirements 43 31 36 26 38 27 23 16 140 3. Leadership and Management 38 27 39 28 40 29 22 16 139 4. Hazard Management 39 28 41 30 37 27 21 15 138 5. Standard Operating Procedures 43 31 41 30 30 22 24 17 138 6. Emergency Prepare

**[6]** `1106-00051` — New Zealand Adventure Activity Certification Scheme - a performance study, p.31  
> 31 Table 17: Level of Value gained from the Safety Audit Standard: Supplier Confidence High Moderate Low None N Standard Section N % N % N % N % 2. Safety Management System Requirements 70 50 31 22 11 8 27 19 139 3. Leadership and Management 55 42 35 27 13 10 27 21 130 4. Hazard Management 57 43 31 23 12 9 32 24 132 5. Standard Operating Procedures 53 40 36 27 13 10 29 22 131 6.Emergency Preparedn

```yaml
id: id014
grounded: yes
citations: valid
modality: na
complete: na
drift: none
refusal: correct
human:
notes: correct refusal - and this one is a RETRIEVAL miss, not a generation failure. 8 ground-truth chunks contain Table 27; retrieval surfaced none of them
```

---

## 45. `id015` [identifier]

**Q:** Table 31

### Answer

The sources provided do not contain a complete "Table 31" that I can present to you.

Source [5] references Table 31 in its text, describing it as showing "a clear association of lower socioeconomic status with both incidence and prevalence of work-related hearing problems," but the actual table itself is not included in the excerpt provided.

To access Table 31, you would need to consult the full document: "Report: Overview of work-related harm and risk in Aotearoa New Zealand, p. 70" [5].

### Sources given to the model

**[1]** `5361-00057` — Draft - Health and Safety at Work (Hazardous Substances - Location Compliance Certification for classes 2 to 6 and 8) Performance Standard 2019, p.31  
> Health and Safety at Work (Hazardous Substances—Location Compliance Certification for Classes 2 to 6, and 8) Performance Standard 2019 Draft for consultation 31 (b) make and retain the records specified in column 4 of table 2.14 that correspond to the provision specified in column 2 of that table. Table 2.14 Item Regulation Action Records 1 11.31 Determine which elements of 11.31 apply. A record o

**[2]** `4272-00002` — Towards 2020 - Progress towards the 2020 work-related injury reduction target - November 2017, p.4  
> appendices Appendix 1: Data tables 31 Appendix 2: Confidence intervals 38 Appendix 3: Definitions 39 tables 1 Fatal work-related injury 12 2 Fatal work-related injury, selected industries 12 3 Serious non-fatal work-related injury 16 4 Serious non-fatal work-related injury, selected industries 17 5 Injury resulting in more than a week away from work 21 6 Injury resulting in more than a week away f

**[3]** `1106-00051` — New Zealand Adventure Activity Certification Scheme - a performance study, p.31  
> 31 Table 17: Level of Value gained from the Safety Audit Standard: Supplier Confidence High Moderate Low None N Standard Section N % N % N % N % 2. Safety Management System Requirements 70 50 31 22 11 8 27 19 139 3. Leadership and Management 55 42 35 27 13 10 27 21 130 4. Hazard Management 57 43 31 23 12 9 32 24 132 5. Standard Operating Procedures 53 40 36 27 13 10 29 22 131 6.Emergency Preparedn

**[4]** `4161-00049` — Safe Work with Precast Concrete, p.33  
> – – make sure that workers have the appropriate experience and training needed for precast concrete work – – engage with workers when making decisions about providing information and training. Provide ongoing training as needed, including refresher training so that skills and knowledge are kept up-to-date. Skills decline if they are not used regularly. 4.1 TABLE 3: Worker training: What could go w

**[5]** `67185-00124` — Report: Overview of work-related harm and risk in Aotearoa New Zealand, p.70  
> tinnitus that began at any stage in their working life. This is consistent with noise having cumulative effects over time, and with concurrent age-related decline in hearing acuity. Table 30: Self-reported incidence and prevalence of hearing loss by gender and age Began in past 12 months (incidence) Began at any stage in working life (prevalence) All workers 2% 10% Male 2% 14% Female 2% 6% 18 - 

**[6]** `1106-00047` — New Zealand Adventure Activity Certification Scheme - a performance study, p.29  
> 29 Table 14: Level of Value Gained from the Safety Audit Standard: Participant Safety High Moderate Low None N Standard Section N % N % N % N % 2. Safety Management System Requirements 43 31 36 26 38 27 23 16 140 3. Leadership and Management 38 27 39 28 40 29 22 16 139 4. Hazard Management 39 28 41 30 37 27 21 15 138 5. Standard Operating Procedures 43 31 41 30 30 22 24 17 138 6. Emergency Prepare

```yaml
id: id015
grounded: yes
citations: valid
modality: na
complete: na
drift: none
refusal: correct
human:
notes: correct refusal, and precise: noted [5] references Table 31's finding but does not reproduce the table
```

---
