


> *Note: For brevity and to fit within the output limits, the standard administrative front matter (SF-298, Table of Contents, Lists of Figures/Tables/Acronyms, Acknowledgments) and the final References list have been omitted. The complete core thesis content (Abstract, Chapters I–VII, and Appendices) is transcribed below.*

***

# A DEVSECOPS APPROACH FOR DEVELOPING AND DEPLOYING CONTAINERIZED CLOUD-BASED SOFTWARE ON SUBMARINES
**by Bridger A. Smith**
**Naval Postgraduate School, December 2021**

## ABSTRACT
There are unique challenges for using secure cloud services in disconnected resource-constrained environments and with controlled data. To address those challenges, this thesis introduces a tactical-edge platform-as-a-service (PaaS) solution with a declarative-delivery method for submarine Consolidated Afloat Network Enterprise Services (CANES) operating systems. The PaaS is adapted from the Department of Defense’s Big Bang core elements for submarine-focused outcomes. Using the Team Submarine Project Blue initiative as a case study, this thesis consists of a feasibility study for running containerized applications on different submarine-compatible baselines and applying a prototype declarative software-delivery method called ZARF. We demonstrated the feasibility of using ZARF for packaging and automated deployment of the Project Blue PaaS and its software to the submarine CANES infrastructure. This research culminated in successful integration tests on a current and future submarine hardware and software baseline. The thesis documents the execution of the research, lessons learned, and recommendations for the Navy’s path forward for development of secure software and declarative deployment in air-gapped environments.

***

## I. INTRODUCTION

The United States Navy’s submarine crews currently plan and execute ship maintenance using Microsoft Office Excel spreadsheets. Sailors regularly use Excel’s fill function to manually paint cells to create a Gantt-chart workflow for the ship’s maintenance deconfliction plan or master integrated work schedule (IWS). This schedule is just blocks in the spreadsheet, merged and stacked, for tracking maintenance activities, with bars color-coded for the department responsible for completing each task. Building the IWS and updating it as the maintenance environment changes provides a common operating picture for a submarine crew and a Trident Refit Facility (TRF) during maintenance. For both stakeholders, the goal is to plan, coordinate, and execute timely and efficient maintenance to get the ship to sea on schedule.

While Microsoft Excel is authorized and readily available, it cannot be customized, adequately handle concurrent reads and writes, or be easily updated when the inevitable change to the schedule occurs. Using Excel requires manually and serially assembling job information from users in different submarine departments and from the disconnected ship and shore information technology (IT) systems. Given these challenges, the IWS is insufficient for managing maintenance, and manual routing of paperwork based on the IWS, such as the daily work authorization list called “Nightwork,” is also required. Following this approach to maintaining a common operating picture is tedious, error-prone, and subject to revision-control and administrative-bottlenecks issues, suggesting that other technology solutions should be pursued.

Partial digitalization of traditional processes to achieve desired outcomes is inefficient and loses time used for problem-solving, resource-contention resolution, and meaningful collaboration. These three elements are of high importance for the time-compressed cycles of submarine maintenance, where a several-hour delay could mean the difference between success and failure for the vessel and the fleet schedule. What is needed is a solution which eliminates the technical and cultural limitations that hurt efficiency in the fast-paced submarine refit environment. Automated processes, co-development of software with the TRF maintainers and submarine operators, and a secure deployment pipeline could replace ad-hoc solutions, providing maintainers with a more interconnected and adaptable environment for getting a ship underway.

Culturally, more attention should be paid to the system requirements given by submarine users. Since inception, the focus of the Trident Logistic Data System (the holistic logistic solution for ballistic-missile submarines) and other modernization strategies focused on the needs of shore facilities, leaving sailors forced to use poorly fitting tools like Excel. Considerations of ship interfaces for collaboration and integration with shore systems have been inadequate. Given that all work on a ship is supported and coordinated by the submariners, it is worth exploring the infrastructure and software delivery limitations for ways to improve maintenance coordination. This will be relevant as ship and shore systems are modernized to support the submarine operational cycle.

### A. PROBLEM DOMAIN
For digital modernization, the current operating environment and available technology must be understood and updated to meet new challenges. The capabilities and actions of threat actors operating in cyberspace have become more sophisticated and pose a real threat to national security. This means that cybersecurity must be aggressive when modernizing legacy infrastructure and processes, and in developing software for new mandated strategies (Department of Defense [DOD], 2021b). The United States government (USG) has adopted a proactive way to manage cyber-related risks by focusing on security issues early and more continuously in the software-system life cycle. The framework is called Development Security Operations (DevSecOps). As modern weapon systems become increasingly software-centric and network-oriented (Government Accountability Office [GAO], 2018) DevSecOps has become increasingly appealing to the DOD. To organize these efforts, the USG has issued policy on hardening its cybersecurity posture, promoting software development practices from industry, and reducing the barriers to access of cloud technologies, which should result in a reduction in the software deployment timeframe to warfighters (White House, 2021; DOD, 2019a). With cloud-based architectures, agile development methodologies, and robust cybersecurity technology becoming more widespread in the DOD, the submarine community can accelerate delivery of modern capabilities.

The planned future of DOD software engineering is to use DevSecOps methods on existing hardware, patch vulnerabilities quickly, and work with users to create software to meets their needs (Rosenburg, 2019). The solutions developed under the DevSecOps initiatives will be a holistic approach to cybersecurity that allows teams to build upon other services, creating a culture that learns from failure and does not repeat the same mistakes. The shift needs to occur as soon as possible because the current processes are outpaced by technology change and increasingly complex cyber threats. Supporting this approach, in 2019 the Defense Innovation Board for Software Acquisitions and Practices (SWAP) concluded the current DOD software acquisitions and development approach is broken and poses an untenable risk to national security (McQuade et al., 2019). It provides examples of the DOD’s lackluster record of deploying software-intensive systems on time, on schedule, and with the required performance. Adoption and implementation of DevSecOps could improve DOD software practices.

### B. CURRENT INITIATIVES
Consistent with recent policy changes, new programs such as the U.S. Navy’s Project Overmatch and the U.S. Air Force’s Advanced Battle Management System (ABMS) under the overall Joint All Domain Command and Control (JADC2) initiative, indicate that the DOD will no longer accept years-long software-delivery timelines and frequent program failures. Under new DevSecOps practices, such as building containerized applications and using cloud services, success stories are more common. However, new solutions must be compatible with the existing infrastructure to avoid impeding mission accomplishment.

For the ballistic-missile submarine (SSBN) maintenance community, this means integrating with the Trident Logistic Data System (LDS) and the Consolidated Afloat Network and Enterprise Services (CANES) submarine infrastructure. DevSecOps and cloud solutions for submarines must operate both connected and disconnected to broad-area networks, and from pier-side to surfaced and submerged at sea. New solutions must work in the resource-constrained and network-constrained environments in which sailors operate and must be designed for their skill levels.

Interviews done as a part of this research with the Navy’s Project Overmatch and the Air Force’s Platform One teams indicated that neither Agile Core Services (ACS) (the Navy software-security offering using RedHat OpenShift Linux) or Big Bang (the Air Force’s software-security service) could currently meet the resource constraints to deploy containerized software on submarines. For ACS, the overhead for processor, memory and storage using OpenShift templates make containerized applications too large to use on current submarine hardware and software baselines. A slimmed version of ACS adequate to run on the submarine platform would require time, budget and technical resources be redirected from the U.S. Navy Surface Fleet DevSecOps pipeline.

Platform One’s Big Bang, “software factory in a box,” offers an open-source tool accredited by the U.S. Defense Information Systems Agency (DISA) for tailoring a DOD-compliant DevSecOps observability platform-as-a-service (PaaS) and software container orchestrator. A PaaS typically includes the analytics, system management, and security processes for deploying applications in a cloud environment to meet observability goals (Azure, 2021b). Observability is essential to DevSecOps because interfaces allow for continuous monitoring of system-performance metrics such as processor and memory usage, as well as logging and alerts to help identify and recover from cyber incidents. It initially appeared that Big Bang’s system monitoring and logging software had processor and memory requirements designed for a large-scale data-center architecture. However, modified Big Bang deployments on an F-16 and U-2 aircraft demonstrated success in resource-constrained environments (Krazit, 2021; Sirota, 2021).

### C. APPROACH
For this study, Big Bang was chosen as a starting point due to its cybersecurity capabilities, its comparatively small resource requirements compared to Agile Core Services, its vendor-independent approach, and its core components compatible with deployment on the submarine CANES infrastructure. Following analysis of requirements, Big Bang provided the best scaffold for necessary changes to produce a submarine-compatible PaaS. In collaboration with the Project Blue team (a submarine-focused innovation and modernization effort supporting Team Submarine), a lightweight PaaS called CocoWow was developed to run containerized software on CANES delivered by an air-gap transfer. Air-gap or disconnected software delivery is standard for submarines consistent with the National Institute of Standards and Technology (NIST) and the DOD Risk Management Framework (RMF).

To deploy across the air gap, a declarative software delivery tool ZARF was created. ZARF packaged the lightweight PaaS and Beast Core container and automated their deployment on the chosen submarine CANES hardware and software baselines. Beast Core is an unclassified three-dimensional model and technical-documentation viewer for systems that are like the ones on a submarine. In general, expected benefits occur for including this type of digital-twin technology into sustainment. ZARF was designed as a declarative delivery model to (1) make installation user-friendly for users without software-developer skills, (2) deploy quickly to shorten the sometimes days-long shipboard software updates and installations, and (3) avoid further hardware and software baseline drift of the submarine CANES baseline which complicates DevSecOps practices at scale. ZARF improves on open-source air-gap tools like Sync offered at Platform One (Repo1 Sync, n.d.). What Sync does with heavy user involvement, ZARF automates in minutes with a few hundred lines of code. For CANES installation and testing, ZARF automated installation and enabled a successful deployment of cloud-based containerized applications for submarines.

### D. THESIS OVERVIEW
For the case study done in this thesis research, the author was embedded in Project Blue as a team member to help with several software tasks:
*   A deployment feasibility study of a hardened container for the commercial off-the-shelf digital-twin product called Beast Core.
*   Development of maintenance-planning support prototypes, for which the author supported user-centered design and wireframing from concept to high-fidelity prototype.
*   Iterative development, cybersecurity review and testing of both a declarative software delivery tool and a submarine-focused PaaS.

Following the reciprocity agreement dated November 2020 between the Navy’s Chief Technology Officer and Air Force’s Chief Software Officer, the Navy could use the Platform One DevSecOps pipeline to certify the Beast Core container. This three-dimensional model was developed consistent with the Model-Based Product Support initiative of the DOD which aims to include three-dimensional modeling in sustainment and maintenance practices (SEA06L, 2019). Using the open interface of Beast Core, Project Blue developed and certified prototypes for submarine maintenance, sustainment, and logistics operations.

Two interfaces for Beast Core are the Master Job File (for the creation and future reference of work packages used onboard a submarine) and The Bridger Project (a maintenance planning and workflow tool providing a common operating picture between the TRF and the shipboard crew). Both services are currently hosted in the Iron Bank under the Project Blue container and can be rapidly updated while maintaining certification. The Iron Bank is a DOD Centralized Artifacts Repository (DCAR) which holds hardened container images with reciprocity granted across components and classification levels (Chaillan, 2020). Within the Iron Bank, the Beast Core and Project Blue containers undergo continuous monitoring for configuration changes and are continuously scanned for common vulnerabilities and exposures (CVEs). More information on these three products is in Appendices A, B, and C.

This thesis begins with an overview of the motivation and designs of the maintenance-focused Project Blue software prototypes. The thesis then covers (1) the design for a lightweight submarine-compatible PaaS, (2) details about the declarative software delivery tool ZARF, and (3) perspectives of working within an agile software team. Chapter II covers current applications for submarine maintenance and potential opportunities for modernization. Chapter III details submarine-specific requirements for lightweight services. Chapter IV introduces the changes to Big Bang to create a submarine PaaS and the declarative air-gap transfer tool ZARF. Chapter V discusses cybersecurity issues and methods used in ZARF air-gap transfer of software. Chapter VI reports integration tests for the Project Blue PaaS using ZARF at the Naval Undersea Warfare Center CANES test lab in Newport, Rhode Island, the lessons learned from deploying an Iron Bank container, and data-management considerations from deploying a digital-twin application on a submarine CANES baseline. Chapter VII highlights the major accomplishments of this work and suggest areas for future research.

***

## II. PREVIOUS WORK

This section provides background on the current state of software readiness for United States Navy submarines and their sustainment. As the DOD pursues new solutions and technologies for submarines, it has addressed digital modernization and cybersecurity threats by adopting several industry “best practices.” These include agile-software methods, cloud computing, and DevSecOps. We discuss these trends and their applicability to the U.S. submarine force.

### A. DEFINITIONS AND KEY CONCEPTS
This section defines key terms for the remaining chapters of this thesis.

**Containers**
Containers enable software to run in different computing environments. They are packages of software that wrap all code, dependencies, and settings for an application into a single fully executable unit (Docker, n.d. b). Containerization allows an application and its components (e.g., databases, configurations, and default settings) to be isolated and abstracted from the outer computing environment so they can run under different operating systems and different versions of those operating systems. This provides flexibility to deploy applications organization-wide on any infrastructure, including the cloud, and reduces the risk of depending on a single service provider.

**Microservices**
In a microservice-based software-system architecture, the system is decomposed into many applications that each accomplish processes (Larson, 2014). The applications communicate by well-defined applications programming interfaces and each is fully abstractable from the rest of the system. Each microservice can have separate process flows, logic, data-access layers, and codebases. Microservices are an alternative to the traditional monolithic architectures of software systems.

**Container Orchestrators**
Container orchestrators automate the deployment and management of containers on any infrastructure (RedHat, 2019). This removes the need to redesign or reconfigure an application to deploy it in a different environment. Container orchestration also enables virtualization and scaling of microservices such as storage, networking, and security, which are components of cloud-based applications. Management tools can configure containers based on declared states which indicate how the containers should run.

**Infrastructure-as-Code**
Infrastructure-as-code (IaC) is the concept of managing the infrastructure required for containerized applications. It focuses on the servers, devices, and networking components. Instead of traditional methods to document procedures, infrastructure-as-code automates the configuration of infrastructure in designated files (Terraform, n.d.) describing in code how the infrastructure will be segmented and what resources are required. The result is a declarative repeatable environment that is effectively managed as a single piece of software.

**Configuration-as-Code**
Configuration-as-code (CaC) is another way to manage the configuration of applications (Macvittie, 2020). Like infrastructure-as-code, it results in a declarative state that can be automated, repeated, and managed as a single piece of software, with a focus on how the applications or services interact with each other on the infrastructure. The combination of infrastructure-as-code and configuration management through configuration-as-code using containerized software creates a declarative state.

**Kubernetes**
Kubernetes (K8s) is an open-source container-orchestration platform that automates the deployment, scaling, and management of containerized software (Kubernetes, n.d.). It is infrastructure-independent, meaning it can be deployed and executed independent of hardware and software (e.g., in the cloud, on your laptop, or on an air-gapped server). Automated provisioning of this infrastructure and the deployment of Kubernetes can be done by infrastructure-as-code or configuration-as-code methods.

**Platform-as-a-Service**
A platform-as-a-service (PaaS) simplifies the management of services and makes deployment of applications on cloud infrastructure easier (Mell & Grace, 2011). The complexities of these processes are abstracted for the user and made more observable with user interfaces. The services provided by the platform range from actual hardware in a data center to software-development tools. A platform-as-a-service typically includes the analytics, system management, and security processes for deploying applications in a cloud environment to meet observability goals (Azure, 2021b).

**Continuous Integration / Continuous Delivery**
Continuous integration and continuous delivery (CI/CD) shorten the lead time between engineering and operations by automating security, compliance, and verification controls as much as possible while preserving system reliability. Their methods can also be instrumented to track metrics related to software flow and delivery.

**DevOps**
DevOps (development operations) synchronize two parts of an organization, the development and the information-technology-operations teams, towards common objectives. Traditionally, developers create new features, responding to user feedback and demand. Information-technology operators maintain the stability and consistency of the production environment. In DevOps, these teams cooperate in a tight feedback loop to deliver information-technology services continuously and quickly with high quality and reliability (Azure, 2021a). This feedback loop encourages continuous improvement, contributes to reduced technical debt, and improves the quality and reliability of the information-technology services delivered.

**DevSecOps**
In DevSecOps (development security operations), security issues are addressed at each phase of the software development life cycle (IBM, 2021). It extends DevOps by including the way software is accredited and secured. If the security of software design and delivery is insufficiently considered until late in software development, there will be increased costs to rework and retest previously completed efforts.

**Air gap**
An air gap is a cybersecurity practice for improving a system’s security or defense against cyber events. It is defined by NIST in RFC 4949. Air-gapped systems are disconnected from the Internet and untrusted networks. Critical sectors such as national defense, payments and banking, energy, and aerospace use air-gapped systems for highly sensitive data or transactions. However, air-gapped systems present a challenge when they must exchange data with other systems, such as during system updates, since they must use portable storage media. Older air-gapped systems lack run-time monitoring, making it difficult to verify whether a system follows cybersecurity policy during the data transfer.

**GitOps**
GitOps is the process for automatic infrastructure updating for DevOps by dynamically updating it with code-configuration files based on events in the DevOps workflow (such as version controls, collaboration, and merge requests). GitOps changes the declarative state of the infrastructure based on the activity of the real-time system and allows elastic infrastructure management based on demand (GitLab, n.d.). This reduces the workload of building infrastructure and integrates infrastructure operations in the DevOps cycle.

**Iron Bank**
DOD’s Iron Bank repository contains fully accredited container images that are deployable on any infrastructure. Iron Bank provides free, open-source and commercial off-the-shelf software for DOD customers. It also hardens and secures images for consumption (Platform One, n.d.).

**Big Bang**
Big Bang provides DOD software teams or programs with secure and customizable DevSecOps environments. Big Bang is managed by the U.S. Air Force Platform One team and provides both infrastructure-as-code and configuration-as-code solutions. It also includes a continuous authority to operate (Platform One BigBang, n.d.).

**JADC2, ABMS, and Project Overmatch**
The DOD’s Joint All Domain Command and Control (JADC2) effort tries to connect “sensors to shooters” across platforms, domains, and services. It integrates the array of disparate, often service-specific, command-and-control networks by providing a framework for “data-driven warfare” (Garamone, 2020).

The Advanced Battle Management System (ABMS) is the primary digital modernization project of the U.S. Air Force and supports the JADC2 initiative (Pope, 2020). It tries to establish a common extensible warfighting network with a seamless flow of data across domains and classification levels.

Project Overmatch (PrOM) is the Navy part of JADC2, developing a Naval Operational Architecture that can support distributed maritime operations (Shelbourne, 2020). It provides connections between networks, integrates emerging technologies, and provides applications for both distributed maritime operations and multi-domain operations.

**Project Blue**
Project Blue is an innovation effort focused on the digital transformation and design for sustainment goals of Team Submarine. Project Blue focuses on giving sailors and maintainers at the Trident Refit Facilities, Submarine Readiness Squadrons, shipyards, and on submarines the tools to keep pace with the digital modernization.

### B. READINESS FOR MAINTENANCE AND SUSTAINMENT
Fleet readiness is a fundamental naval objective, characterized as having the manning, training, and equipment necessary to:
> deploy forward and win in day-to-day competition, in crisis, and in conflict... [and] consistently deliver maintenance on-time and in full, refurbish our critical readiness infrastructure, master all-domain fleet operations, and exercise with like-minded navies to enhance our collective strength. (Chief of Naval Operations [CNO], 2021, p. 7)

Fleet readiness for shipyard tasks and its impact on operational availability are important to achieve these objectives. Based on a recent U.S. Government Accountability Office (GAO) study, 38 of 51 (75 percent) aircraft-carrier and submarine-maintenance periods were completed late from 2015–2019 (U.S. Government Accountability Office [GAO], 2020b). This caused 7,424 days delayed. On average, shipyards were 113 days late for aircraft carriers and 225 days late for submarines, with the two main causes being unplanned work identified after maintenance planning was done and shipyard-workforce performance and capacity.

Similar sustainment issues are occurring across the Navy. The naval aviation community is seeing supportability issues with its aircraft maintenance and logistic software, which significantly reduce readiness (Wilson et. al., 2020). Under Marine Corps Order 4151.22, the Conditions Based Maintenance Program (CBM+) is mandated for Marine Air Ground Task Forces to include platform sensor data and predictive-maintenance analytics into sustainment. CBM+ is prioritized to “increase asset availability” and “reduce life cycle costs,” which should enable a more lethal and ready Marine Corps (Commandant of the Marine Corps, 2020). Common themes such as current software hindering the maintainer’s efficiency and a push for data-driven concepts in sustainment have arisen in the submarine force. However, without effort and investment, resolving from the current readiness issues will take years (GAO, 2020a).

For the Navy to address the performance and capacity issues in the dynamic shipyard environment, maintenance must become more efficient and well-coordinated. This requires developing a common operating picture with stakeholders and providing tools to satisfy the needs of maintainers. Achieving these goals includes addressing the information systems as a major contributor to productivity (Eversden, 2020). In January 2021, the Assistant Secretary of the Navy launched Operation Cattle Drive, calling for upgrading several legacy logistics and financial information systems, due to being “unneeded, obsolete, unproductive, insecure and un-auditable” (Department of the Navy Chief Information Officer, 2020). Infrastructure and software modernization is needed for fleet readiness. Furthermore, if the DOD modernization comes only from the acquisition of monolithic commercial off-the-shelf technology, it can take years to deliver and fully implement. It will take even longer to determine if the solutions improve the issues identified by the GAO about the inability to coordinate and execute work.

Besides the physical sustainment of warships, the fleet struggles to adequately maintain and update its software. This is reflected in reports on the submarine force’s cybersecurity practices and the years-long cycles between operating-system upgrades and software overhauls (Ziezulewicz, 2021; PMW-160, 2020). As weapon systems become more software-centric and software better follows industry best practices, the Navy must upgrade its practices. Decades of mandated traditional practices, risk-averse bureaucracies, vendors locking in use of their software and data, and issues in coupling an already stressed system with complex commercial-software requirements, may cancel out the expected benefits of better logistics software.

For readiness, timely maintenance of physical and software systems enables more days at sea and better deployment of leading-edge technologies against the adversary. For the submarine community, progress towards the Chief of Naval Operations’ (CNO) readiness objectives and the (DOD) modernization efforts begin with the modernization of information technology for the TRFs and Submarine Readiness Squadrons (SRS).

### C. SUSTAINMENT SOFTWARE
To improve readiness, the Columbia submarine program adopted a Design for Sustainment acquisition strategy which affects the submarine design for maintainability and builds the support for refit execution (Schafer & Baker, 2019). Much as DevSecOps integrates cybersecurity requirements early in the software life cycle, sustaining a ship must also be considered during the initial conceptualization and design. For physical components such as pumps, valves, and pipes, detailed physical-arrangement reviews can ensure access for in-place maintenance and removals. Arrangement reviews can be done with three-dimensional modeling or physical mockups. Overall, a sustainable design requires effort and a willingness to balance the requirements of people, time, cost, weight and volume, and other resources that occur in submarine design.

Designing software for sustainment is not simple. Software development can be more of an art than a science, with success relying on human elements that are difficult to control. Across the Department, thousands of digital systems and databases, and fit-for-purpose business processes, exists from digitizing the original processes. Each system differs in the degree of documentation, further complicating matters. Also, planning decades-long software sustainment is difficult when technology evolves more quickly than policy and acquisitions. This means hardware or software in a ship may be obsolete by the time the ship is delivered.

Project Blue was founded to explore opportunities to digitally transform sustainment of the strategic submarine fleet and enable squadrons to maintain two SSBN classes at the same time. It proposed that the transition period from the Ohio to the Columbia class SSBN platform could be done at lower risk by improving the efficiency of maintenance support. Process improvements included scheduling and planning, coordinating, executing refit periods, quality assurance, work accounting, and configuration management. Project Blue’s ongoing feasibility studies with SRS members helped identify and understand the unique cybersecurity and infrastructure requirements of submarines. They also helped in identify missing capabilities on the Ohio and Columbia platforms and assess where software could improve user efficiency. Three-dimensional modeling, cloud-collaboration tools, and digital threads enable the holistic life cycle view needed to modernize legacy processes.

Project Blue’s efforts focuses on submarines, complementary to the existing and planned systems within the Navy. The Naval Maintenance Repair and Overhaul (N-MRO) system, being developed for the Naval Surface Fleet under U.S. Fleet Forces, could also be used by the submarine force. Its maintenance planning and execution software has been designed based on user feedback sessions from Navy Surface Fleet sailors and is linked to the Joint Fleet Maintenance Manual (JFMM), the main reference for Navy maintenance. The Fleet Forces have contracted with Lockheed Martin and its partners, including manufacturing-work and cloud-applications developer IFS, to provide commercial off-the-shelf software for naval ships and aircraft (DeRosa, 2021). The N-MRO solution is a large-scale replacement for many current practices of the surface fleet and could be adapted for the submarine fleet.

While IFS offers many necessary services for manufacturing work at the TRFs, its delivery timeline relative to the Columbia class is an issue based on how intimately linked the SSBN mission is to the Trident Logistic Data System (LDS). LDS set a precedent by including holistic integrated logistics support (ILS) for the submarine platform. It is a shore-based automated information system, with an environmental-support system and application processes. It is part of logistic support for the Trident Submarine System, to “provide an integrated information system necessary to support the intensified level of maintenance and logistics support required for Trident submarines to achieve their high level of operational availability” (Hiza, 1982). ILS helps identify life-cycle costs and reduce cost growth by ensuring that support, equipment, and systems can meet expected operational needs. From its perspective, systems cannot satisfy operational requirements unless they can be restored to service within deadlines. From its inception, the Ohio program focused on the concept of total ILS and designed LDS to meet the high operational demands and unique maintenance control requirements for Ohio submarines. As the program of record for SSBN logistics, its continued success came from a culture of continuous improvement.

The Columbia program’s Design for Sustainment also embraces the total ILS concept. Like the Ohio program, it will provide necessary capabilities for the Columbia class throughout its life cycle, including integration of planning and production toward the timely completion of submarine refits and incremental overhaul. This system should be compatible with the maintenance activity’s infrastructure and the need for reliability without disrupting the active planning and production work. DevSecOps methods should quickly prototype, test, and iterate new capabilities for this environment and provide confidence in their ability to meet operational objectives.

Planning future operations and sustainment of a major weapon system involves evaluating product-support alternatives and minimizing the logistics footprint (DOD, 2019b). An important product-support activity “Reset” restores systems to desired levels of capabilities for the unit’s future mission. Embedded reset teams help the operational maintainer, meet requirements for maintenance and operations, improve deployment time, and reduce costs. An example of a “Reset” is a Refit period in which teams do resupply and maintenance to reset the submarine platform for another patrol.

Currently, submarine crews plan maintenance using paper-based methods or using customized Excel spreadsheets. This is because of the mandate of legacy information systems, lack of advocacy for the sailor’s needs, software-acquisition barriers, and a secretive approach to submarine data. Hand-written Gantt charts and manually updated whiteboards are still standard for communicating shipboard, divisional, and daily maintenance responsibilities. Efforts to use existing commercial off-the-shelf solutions such as Microsoft Project, Smart Sheets, and Excel plugins are attractive because of their accessibility and familiarity. However, customizing such solutions for the submarine fleet entails hidden costs as it is risky to rely on products not specifically designed for them. This typically results in software that slowly diverges from the needs, increasing the gap to be closed (Schwartz, 2017). For instance, while Microsoft Project appears to offer a low-cost opportunity to improve submarine-to-SRS collaboration, it has licensing costs and challenges, unnecessary features for man-hour and cost estimation, scaling issues when managing many jobs, irrelevant features for submariners, and a need to provide custom training for crews and maintainers, all of which have limited value for submarine maintenance. A tailored solution could likely deliver better value to this task. Within the submarine force, the Nosis program’s successes in supporting applications for submarines and its sailor-defined use cases does offer lessons learned and collaboration opportunities (Nosis, 2021).

### D. DEVSECOPS SECURE PLATFORM-AS-A-SERVICE
Emerging cybersecurity threats have encouraged the DOD to adopt industry best practices (DOD, 2019a) including DevSecOps. These include practices of DevOps, agile methods, and hardened cybersecurity postures. They also include DevSecOps “playbooks” and frameworks, cloud technologies, open-source tools to avoid vendor dependence, GitOps, IaC and CaC services to run K8s architectures, and DevSecOps pipelines for CI/CD. The Project Overmatch team at the Naval Warfare Information Systems Command (NAVWAR), the Air Force’s Platform One team supporting ABMS, the Army Futures Command’s software factory, and the Navy PEO-Digital’s Black Pearl team have all use DevSecOps environments. These support a baseline PaaS to provide the necessary monitoring, logging, container orchestration, cloud-security controls, and software-development tools to comply with the DOD, DISA, and NIST requirements about cloud and container security:
*   DOD Cloud Computing Strategy
*   DISA Cloud Computing Security Requirements Guide
*   DISA Secure Cloud Computing Architecture (SCCA)
*   National Institute of Standards and Technology (NIST) Cybersecurity Framework
*   NIST Application Container Security Guide
*   DISA Container Hardening Process Guide
*   DOD Enterprise DevSecOps Strategy Guide, Version 2.0.
*   DevSecOps Tools and Activities Guidebook, Version 2.0.
*   DOD Cloud Computing Security Requirements Guide
*   DISA’s Secure Cloud Computing Architecture (SCCA) for the Cloud environment

Project Overmatch has partnered with RedHat to expand the Navy’s deployment of Agile Core Services (ACS). ACS operates at the platform level on the CANES network and allow the different systems on a ship to “speak the same language” (Howard, 2017). With these services, application developers have confidence that data flows correctly and resource redundancies are minimized (Underwood, 2020). RedHat OpenShift templates are one element of the Navy’s baseline DevSecOps pipeline (Naval Information Warfare Center [NIWC], 2020).

DOD Platform One provides an open-source DevSecOps solution called Big Bang (Platform One Big Bang, n.d.). Platform One offers DevSecOps services certified for DOD systems under DISA accreditation. Programs can download and manage their own development platforms using Big Bang or can have the Platform One team manage their application development, testing, and production needs on a Cloud Native Computing Foundation (CNCF) K8s platform called Party Bus (Platform One Party Bus, n.d.). These products use open-source tools to avoid vendor lock-in and enable accreditations by the Iron Bank.

The Army Futures Command and Army Software Factory partnered with VMware to use its Tanzu product for its standard software-security baseline (Patel, 2021). Tanzu accelerates applications delivery, manages cloud services, combines development and operations, and speeds K8s adoption (Bowen, 2021). The Army Futures Command is partnering soldiers with VMware Tanzu lab specialists to train soldiers to build cloud-based applications and deploy them anywhere.

Black Pearl has developed its own PaaS offering called Lighthouse (Black Pearl, n.d.). It will serve as an observability, monitoring, logging and alerting platform similar to Big Bang. Like Platform One’s Party Bus, Party Barge offers Black Pearl managed security solutions. In 2021 Black Pearl became established under the Navy’s program office for digital services and continues to push for accreditation of its tools.

While other DevSecOps offerings run on an Amazon AWS or Microsoft Azure backbone, these four DOD DevSecOps offerings were analyzed by the author for usability with current submarine requirements. Unfortunately, none could be used on submarine hardware and software baselines without significant modification, for both technical and administrative reasons. ACS running OpenShift requires too many resources to run submarine containerized applications on CANES, although it supports Red Hat Enterprise Linux operating systems (NIWC, 2020). During PaaS analysis, Black Pearl, which was initially intended to mirror Platform One, was not far enough along in accreditation for Lighthouse and was using the Platform One technical stack and baseline. No reciprocity agreement exists between the Army and Navy to use the capabilities of VMWARE Tanzu and that disqualified it, although, later it was discovered that the Marine Coders, a group of innovators in the Marine Corps, had used VMware Tanzu as a DevSecOps offering for its innovation challenge in March 2021. Finally, a reciprocity agreement between the Air Force and Navy was made while Black Pearl was expanding its accreditations and pushing for adoption. This agreement helped Navy teams like Project Blue use the Platform One DevSecOps services and GitOps pipelines to develop their first mission applications and gain expertise with the technical details.

Ultimately, Platform One’s Big Bang appeared as the best solution for submarine integration for our project based on its cybersecurity features, intended use within Black Pearl, vendor-independent approach, relationship to Iron Bank, DISA accreditation, open-source nature, small resource requirements in the submarine CANES environment, and success in production. Also, Big Bang core components could be immediately used for Project Blue’s submarine-focused PaaS to run its containerized applications. The Project Blue platform will be covered more in Chapter IV.

***

## III. METHOD

This chapter surveys the context in which the air-gap software delivery tool ZARF was developed, and the need for a submarine specific PaaS to run containerized software on submarines. It describes the software development approach and cybersecurity assumptions made.

### A. PROBLEM CONTEXT
In December 2018, the CNO announced an intent to adopt the framework of the “Compile to Combat in 24 Hours” (C2C24) program (CNO, 2018). It emphasized software modernization and interoperability, as well as identified artificial intelligence and machine learning as key focus areas for improving warfighter lethality and readiness. It looked to shorten risk-management framework accreditation, improve cybersecurity monitoring, and shorten the delivery cycle to under 24 hours for Navy warships with a common software life cycle and data environment. It encouraged feedback and identifying barriers for successful adoption and migration to the C2C24 framework.

Previously, NIWC had run a pilot program with several Navy units including the USS Essex (LHD-2) to test C2C24 (CHIPS Magazine, 2018). It used data standardization, shared infrastructure, automation for functional and cybersecurity controls testing, and cloud services, all fundamentals for a DevSecOps pipeline in an operational environment. The pilot program used the CANES infrastructure, the standard computing environment for command, control, intelligence, and logistics services on Navy ships (Space and Naval Warfare Systems Command, 2011).

In December 2020, the CNO announced the availability of the newly approved Rapid Assess and Incorporate Software Engineering (RAISE) Framework for Navy DevSecOps environments and for CANES (CNO, 2020). RAISE further enhanced Navy software accreditation timelines using automation, cyber verification tools, and a Cybersecurity Tech Authority providing certified DevSecOps pipelines (NIWC, 2018). The memo mandated, beginning January 2021, that all programs with new software or upgrades for the surface-ship version of CANES running ACS would use the RAISE framework. The Navy’s first Application Arsenal (applications for Navy ship systems) was later released in August 2021 (Gamboa, 2021). For ACS, CANES, RAISE, and Navy DevSecOps focused teams, NAVWAR supports a Navy DevSecOps pipeline as part of the Project Overmatch and JADC2 initiatives. While much of this was created for the surface Navy, it can also help the submarine force.

### B. SOLUTION ASSUMPTIONS
Information from NAVWAR stakeholders helped develop containerized cloud-based software for submarines. CANES configurations used for submarines and ACS documentation provided the submarine hardware and software requirements for a submarine PaaS (PMW-160, 2019; NIWC, 2020). An environment of Red Hat Enterprise Linux versions 7 and version 8 operating systems was chosen for integration tests.

Following review of the documentation, interviews explained what would be needed to overcome the compatibility challenges of ACS with the submarine CANES baseline. It was determined that processor, memory, and storage requirements of ACS were too large, and thus incompatible with the CANES infrastructure onboard submarines (NIWC, 2020; PMW-160, 2020). An alternate DevSecOps PaaS solution was needed. A few interviewees were exploring the U.S. Air Force solution called Big Bang, which sought to achieve lower life cycle costs for DevSecOps in staging and production environments. With budget issues affecting many DOD programs, it was determined by the author and the Project Blue team that the submarine solution should be low-risk, reusable across the DOD, and scale across the submarine platform for efficient software updating during a refit. Furthermore, the reciprocity agreement between the Air Force and Navy Chief Information Officers could reduce authorization and operation timelines (Department of the Navy Chief Information Officer, 2021).

### C. SOLUTION DEVELOPMENT
In 2020, the submarine-focused Project Blue team delivered the Beast Core hardened container image to the Iron Bank repository on Platform One. Having passed the certification needed to be in the Iron Bank and having received DISA accreditation for DOD use, a feasibility study to run containers in the submarine environment was next. The study gathered requirements from the DOD DevSecOps initiatives including Project Overmatch (Navy), Project Convergence (Army,) and ABMS (Air Force) to promote joint software collaboration and avoid redundancy. Performance requirements for the PaaS options were compared to the submarine CANES deployment environment.

Core elements and the open-source concept of the Project Blue PaaS came from Platform One’s Big Bang. As a DISA-accredited open-source DOD-owned DevSecOps solution, Big Bang offered a mature starting point for integration into the Navy’s Linux operating systems. 

A PaaS for submarines must consider the environment in port, at sea, and for the sailors using the tools. The service should fit in a submarine implementation of CANES while allowing room for other applications. This is important because the Beast Core container requires significant graphics data. The resource requirements for processor, memory and storage were determined from technical specifications provided by the Naval Undersea Warfare Center-Newport CANES test facility and are shown in Chapter VI.

For submarines, isolated (air-gap) environments are needed to avoid exposing potential vulnerabilities until patching is possible. Information systems on submarines are also primarily classified networks, whereas shore support activities, such as the SRSs or TRFs use Unclassified Naval Nuclear Propulsion Information (UNNPI) data. Network segregation requirements and lack of infrastructure further complicate network and data synchronization and hinder maintenance collaboration. Given these limitations, consensus was reached within Project Blue that air-gap software-delivery efficiencies should be pursued for submarines. Finding efficiencies in the air-gap transfer for submarines could apply to other air-gap systems and help with data synchronization needs between the submarine and refit facility. A declarative approach (a combination of GitOps, CaC and IaC) for software delivery was selected to create a repeatable delivery method with as much automation as possible. This could lower the barrier to delivery and provide a scalable solution for long-term sustainability across all CANES submarine platforms (Smith et al., 2021).

A submerged submarine is a weapon system operating at a low bandwidth. Since outside resources and technical guidance are then unavailable, troubleshooting, deploying, or restarting the system must be designed for the skills of the submariners. Leading-edge technologies may be difficult to control. User interfaces, displays, code repositories, threat indicators, system analysis, and recovery methods must be sufficiently intuitive that external communications are not required for troubleshooting.

For end-to-end deployment, the GitOps environment and DevSecOps CI/CD pipelines hosted by Platform One can build, secure, and test containerized, cloud-based applications. This was used for the development of the Project Blue applications and ZARF installation tool. Cloud-based containers can be stored, continuously monitored for vulnerabilities, and matched to configuration updates in the Iron Bank. ZARF was built using the platform independent GO programming language (GO, n.d.) and provides a declarative approach to software delivery (Github, n.d.). It enabled deploying Big Bang core elements, Iron Bank images, Project Blue’s PaaS, the Beast Core mission application, and its digital-twin data to submarine CANES. Hash verification in ZARF ensures file integrity during air-gap transfer. For installation, ZARF provides one-time-use credentials and transport-layer security (TLS) using certificates to do automated network instantiation, configuration, and troubleshooting. Testing was done on an unclassified RedHat Linux 7 CANES virtual machine supplied by NUWC. Interoperability tests on selected operating systems proved portability of the ZARF method and the services using Virtual Box and Vagrant as a sandbox environment.

Core elements of Big Bang keep consistency with DISA accreditation and maintain compliance with DOD and NIST DevSecOps policy. The continuous monitoring and logging tools of Promtail, Grafana, and Loki provided lightweight applications for observability. The PLG stack replaced the heavier Elastic, Fluentd, and Kibana EFK stack used by Big Bang, but display the same representations of behaviors that could indicate possible compromise or abnormal system behavior. Gitea provided a small Git download environment to maintain an auditable changelog and repository for utility-cluster data. K3s was used as an open-source CNCF container orchestrator for deploying K8s to edge devices. The Docker registry and Containerd were taken from the Iron Bank. For K3s pod and node monitoring and manipulation, K9s provided a small open-source user interface for K8s to allow a user to interact with the node architecture. K9s provides an operator-friendly substitute interface for the industry standard Kubectl. With ZARF, the Beast Core mission application and interfaces for the Project Blue PaaS were bundled and chosen to minimize the resource requirements.

***

## IV. APPROACH

This chapter covers the key components of Project Blue’s PaaS called CocoWow, which provides a lightweight open-source solution for running containerized applications on submarines and achieving DevSecOps cybersecurity goals. Specifics are provided for the software delivery tool ZARF, which helps streamline air-gap delivery and create repeatable installation. Details for the changes to Big Bang to run on submarine hardware and software baselines are also discussed in this chapter. This work’s main contribution to submarine DevSecOps is ZARF appliance mode, which replaces the Big Bang Elasticsearch, Fluentd, and Kibana (EFK) services with the Promtail, Loki, and Grafana (PLG) services. Using the PLG services for the Project Blue PaaS keeps cybersecurity and observability goals for submarines.

### A. PROJECT BLUE’S PLATFORM-AS-A-SERVICE
CocoWow provides a DOD DevSecOps–compliant capability for submarines. It has the necessary services to meet DevSecOps observability goals for system performance monitoring and cybersecurity management. This PaaS provides a lightweight container orchestrator and virtual security-operations center (vSOC) for running K8s clusters on submarine CANES Linux operating systems following the PMW-160 CANES Roadmap. Alerts and indications when using CocoWow’s services can reveal when a system requires attention or has abnormal behavior.

The tools in CocoWow were based on best practices for monitoring and observability as defined by Google Cloud architecture guidelines (Google Cloud, n.d. a; Google Cloud n.d. b), the DOD DevSecOps Playbook and the DevOps Research and Assessment (DORA) studies. The Google Cloud guidelines specify these:
*   Transparency of the overall health of systems functioning, resource availability, as well as communication of system outages
*   Visibility of leading indicators of outages, service degradation, bugs, and unauthorized activity
*   Monitoring for key business and systems metrics and long-term trends for capacity planning and business purposes
*   Access to tooling to help troubleshoot and debug systems in production
*   Access to tooling and data to help trace, understand, and diagnose infrastructure problems in the production environment, including interactions between services
*   Identifying unknown unknowns for risk and contingency planning, as well as the ability to expose unexpected side effects of changes or added functions.

The Project Blue team specially considered the tactical environment of submarines in the design for CocoWow. Using the PaaS, submariners must observe and troubleshoot behaviors in a disconnected or contested environment. Surfacing or coming to periscope depth may not be an option if the system requires outside technical support. A balance between lightweight capability to fit in the constrained CANES environment and observability of behaviors within the system had to be maintained.

Useability, intuitiveness, and ability to manage routine operations were prioritized for user presentation in CocoWow. The submarine sailor lacks the time and training that a software developer would have and must rely on basic training and continuing education programs to troubleshoot in an isolated environment. For newly developed systems, senior leadership with years of experience will be unavailable, meaning a more objective, systematic approach to troubleshooting and system operations is required. New systems may do things not seen before. CocoWow tries to ensure a submariner has the tools needed to operate its technology and benefit from its capabilities.

CocoWow was derived from Big Bang, a DevSecOps PaaS deployable software factory and container orchestrator. The biggest change for CocoWow from Big Bang occurred in the separation from the vSOC EFK services, which were replaced with a smaller PLG stack:
*   Promtail - used for application monitoring and log shipping to Loki (Grafana Labs Promtail, n.d.)
*   Loki - infrastructure log aggregation and labeling (Grafana Labs Loki, n.d.)
*   Grafana - computer resource metrics and observability interface (Grafana Labs, n.d.)

The PLG stack provided similar observation and functional services as the EFK stack but requires fewer computing resources. Also, lightweight user-friendly graphical interfaces and syntax-friendly options were included. K9s was included as a K8s architecture, services, and applications visualization tool to substitute for the heavy-syntax Kubectl standard (Derailed, n.d.). Gitea was included as a small self-hosted Git service for the code repository when a Kubernetes utility cluster will be deployed on a larger scale (Gitea, n.d.). Gitea can also store the data associated with large applications, such as digital-twin data, and provides an alternate data-loading method for the running K8s clusters. K3s was selected as a certified CNCF K8s service, optimized for “unattended, resource-constrained, remote locations or inside IoT [Internet of Things] appliances” (Rancher Labs, n.d.; Containerd; 2021).

**Table 1. Summary of Project Blue PaaS and Beast Core mission services.**
| Services | Functions |
|---|---|
| K9s | Kubernetes (K8s) graphical interface, command-line interface, and metrics-visualization tool. Substitute for the K8s industry standard Kubectl (K9s, n.d.) |
| Gitea | Changelog and Git source for utility-cluster data for larger-scale applications (Gitea, n.d.) |
| Promtail | Event logging, monitoring, and alerting service (Grafana Labs Promtail, n.d.) |
| Loki | Infrastructure log aggregation and labeling service (Grafana Labs Loki; n.d.) |
| Grafana | System performance dashboard for the metrics and monitoring platform (Grafana Labs; n.d.) |
| Kiwigrid/k8s-sidecar | Kubernetes pod monitor for auditing clusters (Platform One Big Bang, n.d.) |
| K3s | Edge-optimized container orchestrator (Rancher Labs, n.d.) |
| Twistlock | Container runtime security service (Platform One Big Bang, n.d.) |
| Beast Core | Container for three-dimensional model and technical systems documentation viewer (Beast Code, n.d.) |

### B. ZARF AIR-GAP DELIVERY TOOL
Installing updates can be laborious with older technology on submarines. ZARF streamlines software delivery over the air gap by using a declarative delivery state for scalability, repeatability, and ease of installation. This approach uses GitOps, IaC and CaC to define the desired installation goal. This declarative state means the software developer defines the system configuration information before installation, automating and simplifying the process (Smith et al., 2021). The original integration tests for ZARF were limited to submarine use but could extend to delivery challenges for other DOD air-gap systems. For submarines, two key considerations went into the creation of ZARF: (1) hosting Unclassified Naval Nuclear Propulsion Data (UNNPI) in the cloud, and (2) exposing legacy submarine technology to the Internet, expanding the cyberattack surface of the weapon system.

To deploy DevSecOps services and Project Blue’s submarine applications, ZARF must manage the bottleneck and sustainability issues a manual transfer of software between air-gapped systems creates. This addresses baseline drift (i.e., different ships on different versions of the same CANES baseline) which complicates installation. Installation overhead or technical debt gained from the current procedural software delivery approach, as observed in both the testing and operational CANES environments for submarines, prevents fast and scalable software delivery. Baseline drift poses a significant issue to continuous integration and continuous delivery because deviations from a platform-common baseline may prevent consistent, repeatable, and fast software changes across the fleet (Smith et al., 2021). With ZARF, a scalable and repeatable method is available using the declarative state for different versions of the CANES baseline.

ZARF has two phases in installation. Phase 1 ensures proper configuration and instantiation of the PaaS while Phase 2 deploys the application and loads the data into the K8s architecture. Details are given in Appendix D. This separation was made with troubleshooting in mind. ZARF also has a command to remove its artifacts from the system to allow a restart from a clean state.

Three modes for software delivery to air-gapped systems are possible using ZARF as well as custom modes. For the CANES lab testing discussed in Chapter VI, Appliance mode bundled K3s resources and delivered them to a CANES baseline to run the Beast Core container. Creating appliance mode required changes to Platform One’s Big Bang solution to ensure resources are within the capabilities of the submarine version of CANES. The three modes are now discussed in this chapter with their relationship to Big Bang highlighted. Edge mode and Data-Center mode are standard Big Bang modes optimized using ZARF.

#### 1. Appliance Mode (Single-Use Mission Applications):
Appliance mode for ZARF brings K8s resources and dependencies to low-resource single-application environments. In this mode, and for the test case in Chapter VI, a K8s utility cluster is not required. By contrast, in larger data-center environments, a utility cluster is desirable when system-load management and resource balancing supports many users, services, and applications. An example of a single-use mission application in Appliance mode is the Beast Core container running on a standard CANES RedHat Linux 7 virtual machine using K3s as the container orchestrator and the PLG vSOC. As the only container in the architecture, no other applications compete for resources with Beast Core. Testing a K8s architecture this way was a good start in the feasibility study for submarine CANES lab testing.

In Appliance mode, ZARF provides a simple way to bundle resources and dependencies of K3s for air-gap transfer. ZARF deploys a basic K3s cluster using Traefik 2 (the K3s traffic load balancer). It also configures transportation-layer-security to deploy Podinfo for secure network communications, a small web application for running microservices in K8s (Prodan, 2021). Podinfo is used by other GitOps projects like Flux and Flagger for end-to-end testing. Flux does data reconciliation across different application interfaces and is used by Big Bang in data-center type deployments.

#### 2. Edge Mode (with Istio Service-Mesh)
In Edge mode, an Istio service “mesh” handles when a system grows from a single mission application to multiple services and containers. Istio manages the microservices running in a K8s based system (Istio, 2021). Istio provides an efficient way to secure, connect, and monitor services within a mesh, and is integrated into Big Bang. Jaeger is a tool to troubleshoot problems in distributed service meshes (Jaeger, 2021). Kiali provides dashboards for operators to view features such as network topology and system health (Kiali, n.d.). The combination of the services in Appliance mode and those in Edge mode comprise a larger deployment.

#### 3. Data-Center Mode
The EFK services for utility-cluster management consists of Elasticsearch, Fluentd, and Kibana. Elasticsearch collects logs monitored by the platform (Elastic, n.d.). Fluentd gathers logs from within the system and feeds them to Elasticsearch. Kibana is a Web interface for Elasticsearch. Notably, EFK is a portable option used by other K8s orchestration platforms such as RedHat OpenShift, the template for the Navy DevSecOps offering (RedHat, n.d.). Adding the EFK stack and its operator service to Edge mode creates Data-Center mode and a full Big Bang deployment.

***

## V. CYBERSECURITY CONSIDERATIONS

ZARF addresses some technical challenges of deploying secure software in air-gap environments like submarines. Other considerations are discussed here for building security into the software delivery.

### A. ESTABLISHING CHAIN OF TRUST IN AIR-GAP DELIVERY
Air-gapped delivery of software reduces the risks of cyberattack vulnerability for a submarine. Connecting a submarine to a DevSecOps pipeline on the Internet is not currently available. A DevSecOps pipeline for submarines can aid software sustainment, cybersecurity, and updates, but the weapon system must remain secure when it connects to new software through air-gap transfer or in a future-connected state. Ransomware is an issue because cyberattacks target industrial control systems, resulting in failures, operations delay, and damage to oil pipelines, dams, and power grids (Butt et al., 2019). A submarine is an industrial control system because it’s nuclear power plant supplies propulsion, electricity, and supports weapons operations. A cyberattack compromising confidence in the weapon system is a threat to national security, especially for SSBNs, which holds 70% of the U.S. nuclear weapons (Korda, 2021).

Another reason to explore air-gap deployment is the technical limitations of the legacy submarine infrastructure. The Ohio class submarines and their supporting infrastructure for the TRFs were built beginning in the 1970s (Eckstein, 2020). Submarine construction lags the advances in technology between builds and class changes. This introduces challenges for including cloud-based technologies like the cloud-native access point (CNAP), while meeting the stringent Naval nuclear-propulsion information (NNPI) handling requirements (DOD, 2021e).

The chain of trust for an application or service begins with building a software-development team. Team choices, coding practices, and priorities with respect to cybersecurity become observable with new code creation and revisions in a DevSecOps pipeline. An attacker can still exploit many things in air-gap development and delivery. They can directly target a source-code repository (such as GitLab where ZARF is hosted), use brute force or social-engineering methods to break into a network, or steal data using side channels such as by monitoring wireless connections. Defense-in-depth practices such as multi-factor authentication can help prevent such activities; Platform One uses the Single Sign On multi-factor approach for user access.

In software development, automated static and dynamic code reviews using openly available tools like Snort, Fortify, and Trufflehog help identify possible vulnerabilities as code changes are made. Additional automated security tools and code dependency checks can monitor for poor coding and enforce code-coverage metrics for applications. Insider-threat training, red teaming, penetration testing, continuous monitoring for CVEs using repositories like the NIST CVE databases, using tools like Twistlock for container monitoring, and using cloud-based access points, such as the CNAP as Platform One does to create their software-defined network perimeter and zero-trust architecture are all practices observed during this study that make it difficult for an attacker to exploit Project Blue and ZARF software. These defense-in-depth measures can lower the risk of bugs and vulnerabilities being introduced into source code and help identify integration issues before they make it into a weapons system.

As the DOD continues to focus on a future with artificial intelligence, data analytics, and default connectivity, focusing on cybersecurity is important. Although achieving perfect security and complete confidence a system will not be vulnerable to a cyber threat is impossible, it is possible to make it much harder for an attacker to succeed. Air-gap transfer methods are not enough. Raising the bar will require DOD investment in capability and competency building with a focus on human factors. Added complexity introduced by the human element can be managed by presenting principles of DevSecOps to enable a culture focused on creating cybersecure and capable systems on both sides of the air gap.

### B. ZARF AIR-GAP TRANSFERS
Some details on the ZARF process:
*   **Continuously monitored, immutable container images:** ZARF pulls hardened container images from the Iron Bank. Iron Bank continuously scans containers for configuration updates, known vulnerabilities, and known exploits using backend sources like NIST. This prevents known vulnerabilities getting onto the weapons system.
*   **Create package Signature:** ZARF runs the Secure Hashing Algorithm (SHA) on the files bundled in the transferred file as well as on the entire file. This can be compared to the posted hash values for these files to later show the data is unmodified.
*   **Air-gap/sneaker net:** Air-gap deployment keeps the submarine network isolated from the Internet and lowers the risk of an unpatched vulnerability being discovered.
*   **Signature verification:** A ZARF file has a unique signature based on its contents due to the properties of a hash function. The signature on the connected environment should match the signature in the air-gap environment, and this should be checked both in Iron Bank and before installation.
*   **Establish Root:** Privileges with files should be guided by the Principle of Least Privilege. Only system administrators should have root access. Changes to the network and server should only be done by an authorized administrator.
*   **Install a one-time ephemeral Certificate Authority (CA) or pre-validated network certificates:** ZARF can create a single-use certificate for a faster alternative initialization of the transport-layer security required to communicate with Kubernetes.
*   **Logins to Grafana and Gitea:** ZARF creates single-use passwords to access the application program interfaces to monitor for performance and compromise.
*   **PaaS Installed:** ZARF installs an observability platform for system metrics monitoring, log aggregation, security alerting, and troubleshooting. This contains the virtual security operations center (vSOC) required by the DevSecOps Reference Design Architecture, and reports behaviors that may indicate a compromise.

***

## VI. RESULTS

This chapter documents the conditions, products, and the results of the feasibility testing of the Project Blue PaaS using the ZARF air-gap delivery tool. The submarine CANES baseline selected was HW1.2SW3 with resources listed in Table 2.

**Table 2. Resources available for submarine CANES**
| HW1.2 SW 3 Resources | Total available |
|---|---|
| Virtual processors | 56 virtual CPUs |
| Memory (GB) | 256 Gigabytes |
| Disk storage (TB) | 8 Terabytes |

To handle the limitations of Table 2, the Big Bang PaaS was adapted to create CocoWow, a submarine PaaS to run cloud-based containers in a lightweight configuration. The resulting services, memory, and processor allocations are shown in Table 3.

**Table 3. CocoWow resource requirements**
| Service | Memory (MB/GB) | Processors (CPUs) |
|---|---|---|
| K9s (*) | Steady State: 50MB RAM<br>Max: 739 MB RAM | Steady State: 0.5 CPUs<br>Max: 1 CPUs |
| Gitea | Steady State: 512 MB RAM<br>Max: 2 GB RAM | Steady State: 0.1 CPUs<br>Max: 1 CPUs |
| Promtail | Steady State: 256 MB RAM<br>Max: 3 GB RAM | Steady State: 0.25 CPUs<br>Max: 2 CPUs |
| Loki | Steady State: 128 MB RAM<br>Max: 2 GB RAM | Steady State: 0.1 CPUs<br>Max: 1 CPUs |
| Grafana | Steady State: 128 MB RAM<br>Max: 2 GB RAM | Steady State: 0.1 CPUs<br>Max: 1 CPUs |
| K3s (**) | Steady State: 512MB RAM<br>Max: 1GB RAM | Steady State: 0.250 CPUs<br>Max: N/A |
| Docker-registry | Steady State: 512 MB RAM<br>Max: 2 GB RAM | Steady State: 0.1 CPUs<br>Max: 1 CPUs |
| Twistlock | Steady State: 256MB<br>Max: 256MB | Steady State: 0.1 CPUs<br>Max: 1 CPUs |
| Cluster auditor | Steady State: 2GB<br>Max: 2 GB | Steady State: 0.1 CPUs<br>Max: 0.5 CPUs |
| Beast Core container | Steady State: 512 MB<br>Max: 2GB | Steady State: 0.125 CPUs<br>Max: 1 CPU |
| Beast Core data | \multicolumn{2}{|c|}{25GB storage} |
*\* Command line tool. Not always running and negligible when unused.*
*\*\* Implementation details for max K3s resources is atypical. K3s scales up based on system load.*

### A. TESTING
#### 1. CANES Lab
The feasibility study concluded with testing at the Naval Undersea Warfare Center in Newport, Rhode Island. Table 4 shows the conservative build specifications based on resource requirements of both the Big Bang and the Project Blue PaaS, as well as the data requirements for running the Beast Core container.

**Table 4. Conservative virtual machine pre-build specifications for CANES lab testing**
| | Beast Core data | CocoWow (PaaS + Beast Core container) | Total | % CANES |
|---|---|---|---|---|
| CPUs | - | 12 | 12 | 21% |
| Storage | 25 GB | 5GB | 30GB | 0.4% |
| RAM | - | 32 | 32GB | 12.5% |

To test intuitiveness, the container installation and PaaS tests were done in two parts. Configuration for the CANES baseline was done by the NUWC Application Integration team and Project Blue software developers. They simulated the information-technology and software teams who would be brought in during maintenance for an application update or system overhaul on a submarine. The author then acted as the stand-in submariner due to his warfare qualifications. Unaided, the author used the tools provided in ZARF to deploy CocoWow and use Grafana, Loki, Gitea, K9s, and Beast Core. The author was involved in the creation of ZARF, so he may have had some bias. Nonetheless, this tested whether typical personnel on a submarine would have a satisfactory level of knowledge to do these tasks on a ship either in port or at sea.

SUCCESS for the CANES lab integration tests using ZARF met the following criteria:
*   Installation of the K3s Kubernetes architecture
*   Login and observe Grafana
*   Login and observe Loki
*   Verify log capture for Promtail
*   Login and observe Gitea
*   Observe system functions, services, metrics with K9s
*   Observe Beast Core function

Table 5 summarizes the tests. ZARF integration tests were completed outside the lab on a RedHat 7 and 8 operating system in preparation for the lab environment. The NUWC team provided the RedHat 7.4 and 7.6 virtual machine images on testing Day One. The Nosis program office provided the installation team with a Nosis RedHat 8 virtual machine image on testing Day Two. The Ubuntu operating system and Doom container were brought by the Project Blue Team.

**Table 5. Submarine platform integration tests**
| Submarine compatibility | |
|---|---|
| **HW1.2SW3** | **Integration tests** |
| Ohio RedHat Linux 7.4 | SUCCESS |
| Ohio RedHat Linux 7.6 | SUCCESS |
| Virginia RedHat Linux 8 | SUCCESS |
| Ubuntu Linux DOOM | SUCCESS |

#### 2. Sandbox Testing
Additional testing of ZARF was done on a variety of operating systems using a Virtual Box and Vagrant machine sandbox environment before CANES lab testing. This demonstrated the portability of ZARF to other environments.

**Table 6. ZARF sandbox testing**
| ZARF operating systems compatibility | |
|---|---|
| RedHat Linux 7 | PASSED |
| RedHat Linux 8 | PASSED |
| CentOS 7 | PASSED |
| CentOS 8 | PASSED |
| Ubuntu Linux | PASSED |
| Debian Linux | PASSED |
| Rocky Linux | PASSED |

***

## VII. CONCLUSION

The major achievements of this research are (1) demonstration of technology and a trusted method of delivery for containerized software in a connectivity-constrained and resource-constrained environment using GitOps; (2) demonstration of the feasibility of a software-delivery model (Smith et. al. 2021); (3) prototyping of logistics software for submarines and maintenance-support facilities; (4) contributing to knowledge of how to apply DevSecOps to submarines.

Successful CocoWow installation using ZARF on the CANES servers for the HW1.2SW3 baseline demonstrated a way to deploy cloud-based containerized applications for submarines, edge systems, and air-gap environments while satisfying cybersecurity objectives. This broadens the options available for integration with JADC2 and Team Submarine. It is consistent with the Digital Transformation goals of the DOD and looks to further the CNO’s goals for fleet readiness. Our work demonstrated that using Big Bang and CocoWow as container orchestrators enables containers to be delivered to a submarine baseline in a declarative state using ZARF. Pairing this research with the quantitative framework for cost comparisons between declarative and imperative states will allow the Navy to extend this research (Smith et al., 2021).

### A. CONCLUSIONS FROM THE TESTING
The successful integration tests in the CANES test facility at NUWC-Newport confirmed adequacy of the DevSecOps methods. However, the three-dimensional modeling graphics only partially rendered on the testing laptop due to the graphics limitations and older application versions on the device. The technical-documentation viewer for the ship systems within Beast Core was available, and the services for CocoWow worked as designed, so the approach and deliverables for the study were mostly a success. A containerized version of the video game DOOM was deployed using ZARF in Appliance mode to show that other legacy Microsoft software on submarines could be containerized.

The testing environments and legacy infrastructure that the Navy currently operates have significant cybersecurity issues. An air-gap environment is not ideal for aging technology. Cyber compromise of a system across the air gap can happen, and without up-to-date and patched systems, compromise by an attacker is easier. Using years-old technology because of the slowness of administrative and bureaucratic practices is unacceptable in today’s cyber landscape. Adopting and integrating new technology in submarine environments remains a challenge given the constraints of the onboard submarine infrastructure and the rapid pace of technology advancements beyond the procurement system.

In the CANES lab testing, partition issues delayed the configuration and installation of the Beast Core container. This unforeseen obstacle revealed the data-management requirements for Beast Core, although the Beast Core data was only a small sample of what a complete Ohio-class submarine would have been. This process must be improved to ensure the footprint of the digital twin does not overrun the system capacity. New workstation hardware will likely be required. Also, in a virtual machine environment, abstraction using graphical interfaces makes building and balancing resources easier. However, transferring gigabytes of digital-twin data requires time, which makes troubleshooting difficult and significantly slows installation.

### B. RECOMMENDATIONS
Technical challenges met were largely due to existing infrastructure and practices.
*   A declarative approach to software delivery is necessary to meet Navy warfighting objectives. A GitOps environment with a single declarative baseline is critical for scalable DevSecOps solutions and should be adopted by the submarine facilities. This has been achieved in varying degrees of success by the Project Overmatch Collaborative Software Armory, the Platform One Party Bus, Black Pearl Party Barge, and the pipelines at Navy PEO-Integrated Warfare System called The Forge. Within these pipelines, teams can access representative environments which aid interoperability and minimize breaking changes, which can be identified and tested before being delivered to the platform. A representative environment is readily available with the CNAP.
*   External hard drive size has decreased while storage capacity has grown significantly. Edge storage devices like Amazon Snowball could help applications like digital twins on a submarine where space is limited.
*   VMware Vsphere cloud management has issues running Kubernetes. PuTTY (a secure-shell and client-connection application) was a substitute to avoid creating artifacts that would break the Kubernetes architecture. VMware should try to handle this increasingly popular service.
*   Classification guidance should better address cloud-based technology and modern accreditation frameworks. Default classification levels of Secret or higher for submarines challenge the adoption of new technologies and complicate software delivery. Much maintenance information and data useful for analytics is unclassified and could be shared across organizations or networks. An accredited cloud repository for UNNPI data at the Trident Refit Facilities and onboard the submarines could support analytics, artificial-intelligence, and machine-learning applications. Studying and applying this model for the Columbia ballistic-missile submarine class should be explored.

### C. COMMITMENT TO DEVSECOPS
Cultural challenges were observed during the study. The USG and DOD must commit to DevSecOps to continually adapt and deliver capability fast enough to keep warfighters from losing a competitive edge or becoming disadvantaged. Leadership must emphasize that applying lessons learned and finding success across organizations (versus competing with them) is necessary to rapidly modernize information technology and maximize availability and readiness by reducing maintenance inefficiencies, including updating software. Program managers (with direct support from their product support managers) under Title 10 U.S. Code § 2337 have single-point accountability for sustainment objectives, to include continuous information-technology support with considerations for DevSecOps (DOD 2019b). A principal duty includes evaluating and exploiting opportunities across programs to improve use of industry and DOD resources. Despite this mandate, some Navy stakeholders interviewed expressed frustration about their leadership’s resistance to adopt Big Bang due to its U.S. Air Force source.

The processes and culture within the current software environment are insufficient to rapidly modernize technology and improve cyber posture. This must change in the interest of national security (DOD, 2018a). The introduction of new ideas and mandates naturally bring resistance and discomfort, as a shift from the status quo may not be well understood, or seen as necessary (Cameron & Green, 2009). Reciprocity agreements are an example. When they are in place, trusting in the hard work and competency of those involved versus reviewing and validating their legitimacy should occur. The latter does the same work twice, displays an inherent lack of trust, and wastes valuable time, yet DOD components repeatedly delay reciprocity (Barnett, 2021). Reciprocity should not excuse due diligence by a program but should not hurt the efficiency reciprocity will create.

The Navy should look to certify the DevSecOps work being done by each service to hasten joint solutions and create a faster path to delivery when pathfinder teams identify breakthrough solutions. This may not be most efficiently achievable through eMASS. The eMASS system is not uniformly implemented by all services (Department of Defense Education Activity, 2019) and needs a significant software reorganization. It is burdensome, not intuitive, and its training provides inadequate information for Navy accreditation.

Regardless of whether reciprocity is part of the overall strategy, cybersecurity subject-matter experts should be included in development teams so that architectural and software designs meet basic cybersecurity needs and co-developing the accreditation strategy happens long before pushing code to pipelines for production. Poorly designed systems are just as much of a threat as poorly coded systems. Acquisition and architectural problems will continue to be relevant as the next generation of ships are developed and delivered.

Cybersecurity training should be continued fleet-wide but also includes the idea that perfect security does not exist. It is important to emphasize that cybersecurity is everyone’s responsibility, and the job of a cybersecurity professional is not to be perfect, but to manage the risk that comes with connecting systems. There will always be risk and inevitable failures as the DOD looks to modernize with its new strategy. Creating a culture that understands cyberspace risk, balances them against connectivity benefits, and supplies training and tolerance for failure as systems are modernized will enable a more agile and cybersecure environment.

### D. SOFTWARE IS NEVER DONE
An agile mindset that “software is never done” must resonate in acquisition and operations leadership. Software sustainment should be regarded as highly as physical sustainment. Modern software engineering best practices revolves around agile development and continuous improvement. It is not waterfall-based with phases that are completed and never revisited. Software must get into production quickly, although it may fail, to understand critical requirements and progress in a dynamically changing environment. The prototyping of The Bridger Project, the Master Job File, and the Beast Core products occurred over six months. Convincing the appropriate channels to pilot these tools took twice as long as their development and is ongoing.

The Project Blue feasibility study suggests that predefined requirements are unnecessary for innovative cultural changes. No requirement exists for a submarine PaaS, although it is desired. Some of the best innovations, such as the Sidewinder Missile, have come about organically and through an agile approach.

### E. INTEROPERABILITY ACROSS COMPONENTS
The JADC2 initiative seeks to integrate sensors from the services’ representative programs: Project Overmatch, ABMS, and Project Convergence. Collaboration will be critical for achieving the vision of the DevSecOps policy designs and architecture interoperability. Outside of these programs, countless teams and innovators in the DOD ecosystem operate in data-siloed environments, looking to build enterprise synergy, and organically build solutions to meet mission needs inadequately addressed by the programs of record. These innovative teams likely possess the desire, agility, talent, and speed to combine the critical pieces to the wickedly complex puzzle that is JADC2 and achieve DOD objectives in the current cyber-driven software-defined conflict. Innovative solutions can occur outside the traditional top-heavy, formal, command-and-control DOD structure. Relying on a single solution stemming from a program of record (with ownership of the requirement), is an insufficient strategy to develop and implement the needed capabilities and modernizations to remain strategically relevant. Helping small, organic, discovered teams bring solutions across the bureaucratic “Valley of Death” will be critical to organizational success.

Although the Navy has the Application Arsenal, it is tailored to ACS. The Navy could benefit from studying the Iron Bank as a DISA-approved source for hosting, scanning, and monitoring containers for threats and vulnerabilities. Under reciprocity with Black Pearl, Navy teams like Project Blue are already using this service. This would avoid rework in accreditation systems like eMASS, the Navy’s commonly used software accreditation pathway. Similarly, improvement in the documentation of Big Bang would help the broad stakeholder community looking to use it. Communicating to the other services about development, security, and operations is critical to building new relationships that support joint initiatives. The lack of formal means, ability, or bandwidth to produce it when asked, is a problem. However, the Navy would benefit from accrediting and authorizing Big Bang for broad use, as it would enable teams to use a vendor-independent platform. This would democratize the environment for innovation and experimentation, allowing pursuits of DevSecOps goals to begin without having to buy services in a budget-constrained environment. It will also enable further joint-service collaboration.

### F. ONE TEAM, ONE FIGHT
Throughout this study, teams interviewed expressed concerns with Navy software systems being slow, unresponsive, and bureaucratically managed. However, while they acknowledged improvements had been made, there remained disinterest in adopting solutions that are not their own and warned about Platform One. Many excellent Air Force, Navy, Space Force, Army and Marine Corps teams gave objective feedback and offered guidance to the author that was critical to the success of this thesis.

In the author’s opinion, the many innovation teams interviewed looking to implement DevSecOps in their programs believed in ideas central to the culture of DevSecOps. These beliefs were held despite the timelines given to them to move their products into production. The DevSecOps ideals that resonated within these teams included (1) industry best practices of agile-software development enable flexible and secure product management; (2) continuous integration and continuous delivery can accelerate relevant outcomes for warfighters; and (3) cybersecurity with continuous monitoring must be prioritized. This parallels the sentiments seen in the various articles, policy, and anecdotal experiences for DOD’s adoption of DevSecOps and how it translates to success in a technology-driven and software-centric 21st century.

On the current course without synergy, JADC2 goals risk being delayed. The consequence is that warfighters will suffer because of preconceived, institutional bias inhibiting the emergence and maturity of working capabilities and improved security. Innovation and progress become stagnated when solutions cannot escape organizational bounds, require unnecessary rework, or are impeded under the status quo by legacy practices accepted by a frozen and risk-averse middle.

CocoWow and ZARF show how the DOD can benefit from collaboration and partnerships with academic institutions such as the Naval Postgraduate School. Hundreds of students, with fleet and government experience, are waiting to solve DOD-relevant problems. The power of collaboration between uniformed forces, civilians, contractors, and academics cannot be understated.

For sailors, participation in the software life cycle means enablement, and ideally, the standup of Sailor Coders. This should be promoted, officially organized, and resourced within the Navy. A school model like the Defense Language Institute should be established to build military coding competency. Programs like Marine Coders and the Space Force’s Supra Coders programs are examples on which Sailor Coders could be modeled. Sailors could participate in these cohorts and then be assigned as software sustainers.

### G. FUTURE RESEARCH
This research can be extended into the operational realm for submarines and provide immediate impact. A missing component of the DevSecOps pipeline was a submarine PaaS. Using CocoWow and ZARF, pilot periods can be designed to validate the usefulness of the maintenance planning software designed by Project Blue. With the prototypes designed by the author and built with Project Blue, sailors will be given the opportunity to provide input to replace Excel as the primary tool for maintenance planning. This will enable solutions that can help achieve the goal of getting a ship to sea on schedule.

While this research was unclassified, transferring the capabilities to higher classification networks should be explored. Further study is recommended into the requirements for submarine data using cloud environments. To develop a common operating picture between the TRFs, SRS, shipyards, and the submarines, cloud classification guidance will be required. Being able to create useful data, include it in future planning evolutions, and avoid data silos through cloud access can cause immediate benefits to submarine maintenance.

Digital modernization for the submarine environment is a priority. Understanding the current technology limitations on the submarines and the TRFs will be critical for adopting new technologies. Creating a network and infrastructure map to identify where improvements can be made would provide information on how to better invest resources to meet modernization goals. Infrastructure limitations or unknowns remains one of the greatest barriers to adoption of new technologies.

How to best manage the data produced during a maintenance period should be explored. The Bridger Project was prototyped to digitize the maintenance execution process and create useful data for analytics. Insights and efficiencies can be gained by the incorporation of machine learning and artificial intelligence into the maintenance planning process. The development of the IWS is a weeks-long process using numerous Excel spreadsheets and includes many maintenance deconfliction meetings. Thousands of man-hours are spent on the creation and updating of this document over the course of a submarine maintenance cycle. The inclusion of automation and natural language processing into current maintenance deconfliction practices can continue the push for creating a holistic and integrated solution for planning, which saves sailors time and resources.

***

## APPENDIX A. THE BEAST CORE DIGITAL TWIN AND TECHNICAL DOCUMENT VIEWER

The following features show three-dimensional modeling for the sustainment practices of submarines with the Beast Core container. Data for this study was provided by Beast Code as part of the feasibility study for deploying cloud-based containerized applications to submarines, as well as to understand deploying digital twins under submarine resource constraints.

*   **Selection screen:** The Beast Core viewer dashboard lets the user select a platform to view. Further options include the hull silhouette and applicable shipboard systems.
*   **Full hull view:** The Beast Core viewer provides external and internal vantage points.
*   **Component selection and specification view:** Individual components can be selected and the technical data such as name, system, and characteristics can be reviewed.
*   **Search function:** The search function can quickly identify components and locations, and zoom on locations.
*   **Flow mode visualizer:** Using the System Visualizer, flow within a system can be visualized with dotted lines.
*   **Component state:** Individual components can be manipulated as when a valve’s state is changed from open to shut.
*   **Two-dimensional system diagram viewer:** Red hyperlinks indicate association within the three-dimensional model. Clicking on the hyperlink will cause the system to traverse to the component.
*   **Avatar mode:** Takes the user to the specific location as a first-person viewer where components can be highlighted, technical information accessed, and the most direct path provided.

***

## APPENDIX B. MASTER JOB FILE

Master Job File includes three-dimensional modeling data for maintenance prototyped by Beast Code with inputs from the author. The Master Job File is linked to the processes from the Joint Fleet Maintenance Manual and supports future design requirements for submarine platforms. This tool is for the planners who create the procedures for a submarine maintenance cycle.

*   **Master Job File dashboard:** Tracks jobs created. Features include a collapsible left-hand menu, progress and review status, search functions, and a creation button to begin a new Master Job.
*   **Component and job search:** Super Search searches for components, documentation, and Master Job files. Fuzzy search provides a broader search.
*   **Procedure creation:** A Master Job File follows the specifications in the Joint Fleet Maintenance Manual (JFMM). 13 sections cover the requirements for creating work packages.
*   **Reference viewer:** The references for a procedural step can be linked and displayed.
*   **Critical steps and inspection points:** Following guidance from the JFMM, procedural steps may require additional certification signatures at inspection.

***

## APPENDIX C. THE BRIDGER PROJECT

The Bridger Project provides an interface to Beast Core for a submarine crew and enables planning and executing workflows during maintenance. It was prototyped by Beast Code. The prototype used agile methods for software development of the cloud-based containerized software for submarine sustainment.

*   **Job status tracking:** A detailed workflow is created both automatically with LDS and manually by the team or work center. Jobs are categorized based on status: in planning, at review, ready for work, in process, testing, done.
*   **Individual job data:** Attributes include assigned priority, quality assurance (QA) work, tagout required, associated Work Authorization Form (WAF), etc.
*   **Integrated work schedule:** The refit support module shows an Integrated Work Schedule Gantt chart viewer.
*   **Timeline changes:** Dates and major milestones can be adjusted as conditions within an availability change. Permissions are determined from user roles such as Commanding Officer (CO).
*   **SOSMIL:** Tracks jobs that require higher visibility and coordination between the ship and the Refit facilities.
*   **Nightwork:** The Nightwork list is the source for Ship’s Duty Officers (SDOs) and Production Officers to authorize maintenance.
*   **Print nightwork:** Once approved, this Nightwork document is printed and routed for signature at the daily supervisor meeting.
*   **Job summary & Refit reports:** Logs comments and lessons-learned associated with the work and attests to completion of the job, generating a detailed report from information logged for each job executed.

***

## APPENDIX D. ZARF

The following are the procedural steps and outputs for deploying ZARF to an operating system. ZARF was created in collaboration with Defense Unicorns and Project Blue.

### A. PHASE 1: PLATFORM-AS-A-SERVICE INSTALL

ZARF initialization of the platform-as-a-service occurs with the following command:
```text
~?./zarf init
```

ZARF asks the user if they would like to generate their own TLS certificates.
```text
~? Will Zarf be generating a TLS chain or importing an existing ingress cert?
Generate TLS chain with an ephemeral CA
```

ZARF asks for the user network configuration for their environment.
```text
~? Enter a host DNS entry or IP Address for the cluster ingress localhost
```

ZARF makes initial checks to verify its system initializations are correct.
```text
INFO[0007] Preflight check: validating os type
INFO[0007] Preflight check: validating AMD64 arch
INFO[0007] Preflight check: validating user is root
INFO[0007] Preflight check: validating hostname
INFO[0007] Installing K3s
INFO[0007] Creating temp path
path=/tmp/zarf-050516502
INFO[0007] Extracting the package, this may take a few moments
```

ZARF asks the operator to confirm the package.
```text
~? Deploy this Zarf package? Yes
INFO[0202] Loading dynamic config
path=/tmp/zarf-050516502/zarf.yaml
INFO[0202] Deploying Zarf component
name=k3s
INFO[0202] Loading files for local install
...
```

ZARF asks the operator if they want the Kubernetes management tool K9s.
```text
~? Deploy the management component? Yes
INFO[0240] Deploying Zarf component
name=management
INFO[0240] Loading files for local install
```

ZARF asks the operator if they want the Promtail, Loki and Grafana logging services.
```text
? Deploy the logging component? Yes
INFO[0246] Deploying Zarf component
name=logging
...
```

ZARF asks the operator if they want the Gitops-service component.
```text
? Deploy the gitops-service component? No
INFO[0260] Cleaning up temp files
...
```

ZARF tells the operator that k9s is available and provides the one-time use credentials for signing into the services.
```text
INFO[0266] Installation complete. You can run “/usr/local/bin/k9s” to monitor the status of the deployment.
WARN[0266] Credentials stored in ~/.git-credentials
Gitea Username (if installed)=zarf-git-user
Grafana Username=zarf-admin
Password (all)=Z3WnUtoZL69i-WEiPYK2vzqoGT89
```

ZARF has successfully completed the initial PaaS installation. K9s can verify that all services are available and running.

### B. PHASE 2: APPLICATION AND DATA INSTALL

ZARF begins the deployment of the mission application.
```text
~?root@zarf-test:/home/vagrant# ./zarf package deploy
```

ZARF asks what package should be deployed:
```text
? Choose or type the package file zarf-package-appliance-demo-doom.tar.zst
INFO[0005] Creating temp path
path=/tmp/zarf-247049737
INFO[0005] Extracting the package, this may take a few moments
```

ZARF asks the user if this is the correct package.
```text
~? Deploy this Zarf package? Yes
```

ZARF deploys the elements specified and displays successful steps.
```text
INFO[0012] Loading dynamic config
path=/tmp/zarf-247049737/zarf.yaml
INFO[0012] Deploying Zarf component
name=baseline
...
INFO[0012] Updating image
image=“registry.dso.mil/platform-one/big-bang/apps/product-tools/zarf/game:doom”
...
INFO[0012] Cleaning up temp files 
```

K9s verifies that the DOOM container is running on the system.
ZARF has now successfully deployed the PaaS and mission applications. Normal operations with system monitoring and observation using K9s, Promtail, Loki, and Grafana can start.

ZARF is designed to achieve a declarative state, so installation and uninstallation are easy and quickly repeatable. ZARF destroy requires a `--confirm` flag to ensure the operator understands that all services and ZARF artifacts will be removed, returning the system to the prior-to-installation condition.

```text
root@zarf-test:/home/vagrant# ./zarf destroy --confirm
/usr/local/bin/k3s-remove.sh []
-e
+[ -s /etc/systemd/system/k3s.service ]
+ basename /etc/systemd/system/k3s.service
+ systemctl stop k3s.service
+[ -x /etc/init.d/k3s* ]
+ killtree 78979 79072 79688 80593 80609 80800 81205 81389 82502 84332
...
+ rm -rf /run/k3s
+ rm -rf /run/flannel
+ rm -rf /var/lib/rancher/k3s
+ rm -rf /var/lib/kubelet
+ rm -f /usr/local/bin/k3s
+ rm -f /usr/local/bin/ctr
+ rm -f /usr/local/bin/crictl
+ rm -f /usr/local/bin/kubectl
+ rm -f /usr/local/bin/k9s
+ rm -f /usr/local/bin/k3s-remove.sh
+ rm -fr zarf-pki
-e
```
