


Due to the length of the 72-page thesis, the transcription is provided in parts to ensure all details, formatting, tables, and code blocks are accurately converted into Markdown. Below is **Part 1**, which covers the beginning of the document through the end of Chapter 3 (Methodology). 

*(Note: The repetitive page headers/footers and the Table of Contents have been omitted for brevity, as the Markdown headers natively reflect the document's structure.)*

***

# Università degli Studi di Genova
### Scuola Politecnica & Facoltà di Ingegneria
*Laurea Magistrale in Ingegneria Strategica*
*International MSc in Engineering Technology for Strategy and Security of Genoa University*

**Challenges in applying cloud cutting edge technologies in air gapped on premises datacenters**

**University supervisor:** Professor Bellotti
**Company advisor:** Dr. Giancarlo Camera
**Candidate:** Mina Gheibi

**December 2025**

---

## Acknowledgements

First and foremost, from the deepest part of my heart, I hope that Professor Bruzzone’s soul rests in peace. Losing him during my studies was one of the saddest moments of my life. He was not just a university professor, he taught his students how to think like strategists, how to grow, and how to persevere without surrendering to difficulties. He was an unforgettable person in my life, and I will always remember him with profound respect and gratitude.

I would also like to express my sincere gratitude to my university supervisors, Professor Bellotti and Professor Berta, whose guidance and support have been invaluable throughout my academic journey.

In particular, Professor Bellotti has been more than a supervisor to me; his advice, encouragement, and continuous assistance across several courses and during my internship helped me stay focused and move steadily toward my goals.

My deepest appreciation goes to Dr. Giancarlo Camera, my company advisor, for his patient guidance and for teaching me advanced techniques and knowledge related to new technologies, skills I could not have acquired even through different academic programs. His mentorship has been essential to my professional growth and confidence.

I am profoundly thankful to Mr. Lorenzo Motta, the first person who recognized my passion for learning and encouraged me to take a chance by offering me the opportunity to join the Hitachi Rail team. He opened the door to experiences that have significantly enriched both my academic and professional development.

Finally, I am deeply grateful to my family, whose unwavering support, patience, and encouragement have been the foundation of my academic journey. Without their presence, none of this would have been possible.

A special mention to my dear mother, who has always been my role model and the perfect example of a strong and successful woman. She was my first teacher, the one who showed me that a woman can go further and achieve her dreams without accepting any limits set by the world.

---

## Abstract

The growing complexity of modern industrial and mission-critical infrastructures has accelerated the adoption of cloud-native technologies that seek to enhance automation, resilience, and security across distributed systems. Although these paradigms have transformed software delivery in connected environments, their application in air-gapped networks remains significantly more challenging. In settings where external connectivity is intentionally restricted for security or regulatory reasons, organizations must rely on deployment strategies that guarantee reproducibility and operational continuity without access to public repositories. This thesis examines these challenges by designing and implementing an automated, secure, and fully offline GitOps pipeline for Kubernetes-based systems operating within an isolated environment.

The study focuses on the integration of Infrastructure-as-Code principles with GitOps methodologies to reproduce, manage, and govern the behavior of a cloud-native platform in the absence of internet connectivity. A virtualized air-gapped environment was constructed using Proxmox VE, consisting of independent nodes dedicated to the artifact repository, the Kubernetes control plane, and the automation controller. All container images, Helm charts, and configuration manifests were obtained externally, packaged, and transferred into the environment through controlled offline bundles. This approach ensured full network isolation while preserving the repeatability of deployments and updates.

The research investigates how declarative automation tools can be combined to achieve consistent system states. Infrastructure provisioning was carried out through automated playbooks that enforced deterministic configuration across nodes. The GitOps workflow was established by deploying Argo CD within the cluster and linking it to an internal GitLab instance, enabling continuous reconciliation between the repository and the live infrastructure. A test application was used to demonstrate the behaviour of the system under various conditions, including configuration drifts, update propagation, and rollback scenarios. The results showed that the GitOps controller was able to maintain alignment between the desired and actual states of the cluster, even when the environment lacked external network connectivity.

Security considerations formed another central aspect of the work. Access control mechanisms were applied through Role-Based Access Control, which restricted operations to the minimum necessary privileges and helped prevent unauthorized modifications to the system. Runtime visibility and vulnerability monitoring were integrated through a container security platform capable of analyzing process behavior and network interactions in real time. These components complemented the automated deployment pipeline by adding layers of protection and observability that are often difficult to achieve in offline environments.

The experimental findings demonstrate that an air-gapped Kubernetes infrastructure can support modern DevOps and GitOps practices when supported by well-structured offline workflows. The architecture developed in this research delivers reproducible deployments, continuous synchronization, and reliable recovery mechanisms, thereby addressing operational requirements commonly found in transportation, industrial automation, and other regulated sectors where safety, uptime, and compliance are critical. By combining declarative descriptions, local artifact management, and continuous reconciliation, the study provides evidence that cloud-native ecosystems can be adapted to stringent isolation constraints without compromising automation or governance.

The work also identifies several directions for future improvement. Extending the system to multi-node, high-availability architectures would provide insight into cluster behavior under failure conditions. Additional research on automated certificate lifecycle management, secret rotation, and the integration of security-as-code frameworks could further enhance the resilience and auditability of offline deployments. Finally, exploring controlled synchronization mechanisms between disconnected on-premises clusters and cloud-based systems may offer new possibilities for hybrid operational models. Together, these developments would contribute to the broader effort of designing autonomous, secure, and continuously verifiable platforms capable of supporting the next generation of industrial digitalization.

---

# 1. Introduction

## 1.1. Background (The Evolution to GitOps and Cloud-Native)

The IT world is constantly evolving. In the mid-1990s, infrastructures were primarily composed of physical hardware purchased and maintained within a company’s own buildings. Specialized operators were responsible for managing physical servers manually, and these systems followed the mutable infrastructure approach, where servers were maintained and modified directly in place.

In software development, code was often written in isolation, without structured version control. Compilation, testing, and packaging were handled manually by developers, and the resulting release packages were passed to operations teams for deployment. This process frequently caused delays ranging from hours to days depending on the availability and expertise of operations personnel. The lack of communication and cooperation between development and operations teams led to frustration on both sides, resulting in slow-release cycles and reduced overall productivity.

At the beginning of the 2000s, the Agile methodology emerged, introducing iterative development and collaboration improvements. However, Agile mainly enhanced the development process, not the deployment process, leaving a significant gap between the two. Around 2008, this gap led to the birth of DevOps, a philosophy that through a combination of tools and practices, enabled automation and integration between software development and operations teams. This shift allowed software to be built, tested, and released faster and more reliably, reducing the divide between the two domains.

Among the innovations introduced by DevOps, Continuous Integration and Continuous Deployment (CI/CD) pipelines and Infrastructure as Code (IaC) became central. IaC allows infrastructure to be defined, provisioned, and managed using code, ensuring consistency, traceability, and repeatability across environments. The adoption of virtualization technologies soon followed, leading to the widespread use of virtual machines and later containers, which enabled multiple isolated environments to run on a single physical host. In this context, the concept of immutable infrastructure emerged. once a server is provisioned, it is no longer modified; instead, a new instance replaces the old one for every update.

In 2006, the introduction of Amazon Web Services (AWS) marked the beginning of the cloud computing era, allowing organizations to access and scale computing resources via the internet. Cloud computing, together with DevOps best practices, containers, and orchestration platforms such as Kubernetes, paved the way for cloud-native architectures. These advances laid the foundation for the GitOps paradigm, which GitLab now supports through its integrated CI/CD and repository management features. a model that extends DevOps principles by using Git as the single source of truth. In GitOps, infrastructure and application configurations are expressed declaratively and stored in Git repositories, while tools such as Argo CD and Flux continuously synchronize the desired state with the live state of Kubernetes clusters. This approach enhances automation, auditability, and recovery, ensuring reproducible and version-controlled deployments. [1]

## 1.2. Problem Statement (Security and Automation Challenges in Isolated Infrastructure)

However, as cloud-native technologies have developed rapidly, new operational and security challenges emerged particularly in air-gapped environments, where systems are isolated from the public internet for security reasons. While this isolation strengthens protection against external threats, it introduces significant complexity in terms of deployment automation, software updates, and system observability. In such restricted contexts, traditional CI/CD pipelines cannot operate as intended, and manual installations increase the likelihood of errors and non-compliance. To address these limitations, organizations rely on a combination of IaC and GitOps methodologies, supported by tools such as RKE2, Argo CD, Terraform, GitLab CI/CD, Helm, and Customize, to establish secure and reproducible infrastructures even under offline constraints.[2]

At the same time, security and governance have become fundamental concerns in modern deployments. Mechanisms such as Role-Based Access Control (RBAC) ensure that only authorized users and services can access or modify resources, enforcing the principle of least privilege. However, misconfigured RBAC policies can be a common vulnerability, especially when permissions are manually defined. Establishing structured roles, bindings, and policies is therefore essential to maintaining compliance and reducing risk in highly regulated industries such as transportation and defense.

Besides deployment and access control, observability and runtime security are vital for maintaining reliable and resilient infrastructures. Monitoring tools such as Prometheus and Grafana provide visibility into system health and performance, enabling early detection of anomalies. Complementary to these, platforms like NeuVector offer real-time threat detection, vulnerability scanning, and network segmentation to protect containerized workloads from malicious activity. When integrated with GitOps workflows, these tools form a comprehensive, self-healing framework where automation, monitoring, and security reinforce one another.

## 1.3 Research Objectives and Key Contributions

The convergence of these practices, IaC, GitOps, RBAC, observability, and runtime protection illustrates a fundamental shift in how enterprises manage mission-critical and isolated infrastructures. By treating infrastructure as code, automating delivery pipelines, and embedding security at every stage, organizations can achieve systems that are not only resilient, auditable, and compliant, but also scalable across multiple clusters and environments.

Ultimately, the study of air-gapped deployment strategies offers valuable insights into the future of secure, automated, and self-governing infrastructures. It demonstrates that even under strict operational constraints, it is possible to design deployment pipelines that are reliable, reproducible, and aligned with organizational and regulatory requirements. These advancements form the foundation of next-generation platform engineering, where automation, observability, and security converge to meet the evolving demands of critical industries.[3]

---

# 2. State of the Art

## 2.1 Infrastructure as Code and GitLabs in Cloud-Native Systems

Infrastructure as Code (IaC) is an important new way of working in cloud and cloud-native computing. Due to the fast growth of companies and technologies, the traditional approaches that rely on manual provisioning and configuration of servers don’t work anymore because they encounter several issues, and the outcome of these problems is frustration. One of the big issues is the lack of homogeneity, which means DevOps cannot scale deployments well because of manual management. 
IaC enables engineers to manage infrastructure declaratively through code, ensuring repeatability, consistency, and auditability across environments. This shift is particularly critical in cloud-native systems, where scalability, resilience, and automation are central requirements. IaC practices integrate seamlessly with modern DevOps toolchains, such as GitLab, to establish automated pipelines that govern not only software delivery but also the underlying infrastructure that hosts cloud-native applications.

### 2.1.1 Evolution and Relevance of IaC in Cloud-Native Environments

One Recent research study introduces IaC as a fundamental tool of automation and innovation in multi-cloud deployments and emphasizes that IaC strategies provide “repeatable assets” for infrastructure implementation, which reduce disaster recovery times and eliminate configuration drift, while at the same time enabling DevOps teams to codify infrastructure as version-controlled logic.[4]

Another recent research expand this idea about IaC by suggesting OpenIaC, a framework that integrates IaC with zero-trust architecture and decentralized identity to ensure secure interoperability in cloud-native ecosystems[5]. Both of these perspectives converge on the principle that IaC is not just a technical tool, but a basis for establishing trust, scalability, and resilience in cloud-native clusters such as Kubernetes and RKE2.

The natural structure of IaC aligns with the microservices orientation of cloud-native design. By putting scripts (e.g., Ansible, Terraform) into CI/CD pipelines, IaC allows teams to create modular environments that match the modularity of containerized applications. This integration is essential for connecting automation, observability, and resilience in Kubernetes environments, and for ensuring that infrastructure management evolves with the same agility as application deployment.[6]

### 2.1.2 GitLab as a Central Facilitator of IaC and CI/CD

Among the many DevOps platforms available in the digital market, GitLab is recognized as one of the most complete all-in-one solutions, offering integrated version control, CI/CD pipelines, and infrastructure automation. In a comparative evaluation, researchers found that GitLab combines source code management, container registry, and CI/CD pipelines into a single platform, providing an effective open-source alternative to enterprise tools such as Azure DevOps and AWS DevOps Suite.[7] By using GitLab to combine everything in one platform, it reduces integration complexity and supports DevSecOps practices such as automated security testing and monitoring. One study also shows that Git platforms help teams build collaboration skills. GitLab makes teamwork easier through features such as version tracking, issue management, and merge requests. These features are especially useful for managing Infrastructure as Code (IaC) scripts.[8]

### 2.1.3 Integration of IaC and GitLab in Cloud-Native and Air-Gapped Pipelines

In cloud systems, Infrastructure as Code (IaC) and GitLab integrations can achieve the best results, especially within CI/CD pipelines. This process automates how software and infrastructure are built, tested, and deployed. Using workflow automation tools helps manage containerized applications more efficiently through declarative automation, low-code features, and secure monitoring.[9]

When these automation tools are connected to GitLab pipelines, they allow teams to automatically create and update Kubernetes clusters, ensuring that scaling, load balancing, and failover happen automatically within the same process that delivers the applications.

If the process of this integration is tested from a security perspective, it can be showed that this integration has a very close similarity to Zero-Trust principles.
In one of the recent studies, it was shown that open IaC frameworks and declarative IaC definitions combined with CI/CD automation provide strong auditability and minimize “snowflake systems,” ensuring that no infrastructure component is manually configured outside of version control. [5]
Based on this approach, all configurations, such as cluster bootstrap scripts, HAProxy load balancers, or MariaDB backends, should be defined and verified in code before deployment.

One of the recent studies describes how the combination of GitLab’s architecture, especially its DevOps and IaC principles, enables the integration of source code management, container registries, and CI/CD automation, incorporating security and compliance checks directly into the pipelines.[7]

While some other studies assume the use of public cloud access, critical industries often require air-gapped environments for security reasons to ensure that all processes remain highly protected.
During this research and implementation, Ansible and Terraform, especially Terraform, were the tools used for automating the provisioning of Proxmox VMs, enabling the deployment of RKE2 clusters, with GitLab acting as the internal repository for both application manifests and IaC scripts.
The Hauler VM also supplied offline images, which made it possible to deploy Rancher, NeuVector, and ArgoCD through reproducible IaC pipelines.

This setup confirms one of the recent studies that introduced how IaC architectures enhance automation and observability even under isolation constraints.[6]
As a result of this implementation, it was shown that by combining GitLab’s version control and ArgoCD’s GitLab synchronization, the system maintained continuous alignment between the repository state and the Kubernetes cluster.
This approach confirmed the possibility of achieving a secure, auditable, and fully automated infrastructure in disconnected environments.[5]
This combined system provides a truly trustworthy base for the next parts of the platform, especially monitoring and cluster security, which are very important for ensuring reliability in air-gapped environments.

## 2.2 Security Challenges in Kubernetes Environments

Keeping GitLab and Kubernetes environments secure means protecting all parts of the system, from the infrastructure to the pipelines, against mistakes, weaknesses, and cyber threats. Both Kubernetes and the GitLabs method have their own security challenges that must be carefully managed to maintain a strong defense. In this study, the focus is only on the security needs specific to Kubernetes environments.

Kubernetes can efficiently deploy, scale and manage embedded applications. But as more people use it, security risks grow, especially with workloads and access controls (RBAC). The rapid growth of Kubernetes has led to an increasing number of vulnerabilities, often caused by misconfigurations that lead to data breaches and weak security.[10]

Below are the items that will help keep the Kubernetes environment safe and reduce security risks.

### 2.2.1 Robust Authentication and Authorization (Strong Login and Access Control)

*   **Implement Role-Based Access Control**

Role-Based Access Control (RBAC) is an effective strategy for managing access to digital systems, especially in security-critical environments such as Kubernetes clusters, backup and recovery infrastructures, and enterprise storage systems. RBAC assigns permissions based on user roles (not individuals), thereby enforcing the principle of least privilege and enhancing data security. [11]

Kubernetes provides a robust RBAC mechanism to control permissions[10]. It allows administrators to set clear access rules, making sure that individuals or services only have the permissions necessary for their tasks or modify sensitive backup data. specially in storage systems RBAC supports data integrity and scalability, ensuring that only people with specific roles have access to modify or delete the data.[11]

So, by least privilege, RBAC reduces the risk of unauthorized access and security threats.
The importance of using RBAC implementing is specially for the big companies with too many employees. because RBAC doesn’t give permissions directly to people, instead permission (read, edit, etc.) are given to the roles (manager, auditor, etc.) so users are then assigned to these roles. based on the progress if someone change his job, there is just need to changing the roll not all the permissions. [12] In this case managing access is much easier with less errors.

One might ask whether AI can replace RBAC, but the answer is no.
AI (Artificial intelligence) can play a very important role in checking, monitoring, and finding any misconfigurations or unauthorized entries in a Kubernetes environment. It can even help detect serious, unusual, or dangerous behavior in Kubernetes clusters. However, for AI to achieve this aim, it's very dependent on having a clear structure of who should access what and that's exactly what RBAC provides[13]. So, in this process, RBAC sets the rules, and AI will monitor and detect violations of those rules.

Disable Anonymous Access, makes the cluster more secure and makes it easier to manage RBAC.
Anonymous access to the Kubernetes environment should be disabled to prevent unauthorized users from performing harmful actions and, therefore, reducing security risk for the environment. Additionally, default authorization settings must be carefully reviewed, adjusted, or turned off to ensure strong security controls and limit unauthorized access.

*   **Useful Tools and methods for RBAC Measurement**

To ensure the quality of RBAC settings and maintain strong security between users, it is important to continuously check and monitor access. Alerts should also be set up to warn administrators if any unauthorized access occurs.

**RBAC Lookup Tools:**
Tools such as RBAC-lookup and Polaris help identify instances and authorized service accounts by scanning cluster configurations and recommending security improvements.[10]

**rbac-lookup:** RBAC Lookup is a CLI that allows you to easily find Kubernetes roles and cluster roles bound to any user, service account, or group name.
```bash
kubectl rbac-lookup #installation
kubectl rbac-lookup cluster-admin #show all users or services
```

**Polaris:** is a free, open-source tool made by Fairwinds to help check and improve the configuration of Kubernetes clusters. It makes sure that Kubernetes settings follow best practices and company policies. This tool can also detect issues and send alerts for them. like: weak pod security limit, access control mistake, common configuration error and wrong resource limit. 
very specific feature of this tool is its connection to Prometheus Alert Manager, which helps Polaris automatically scan the cluster and send alerts if something breaks the rules.

**Falco:** Falco was deployed to track system calls in real time and generate alerts for any abnormal behavior.[10]
this tool designed for cloud and Kubernetes environments. It watches what’s happening in real time and uses custom rules to spot unusual or risky behavior. By analyzing system events and adding useful context, Falco can quickly send alerts about possible security threats or rule violations.

**Prometheus & Grafana:** Prometheus is a free, open-source tool, that collects and stores metrics (data) from your Kubernetes cluster and applications. metrics are small information like: CPU and memory usage, Number of running pods, Number of errors and etc. It will monitor the health and performance of the system over time. Additionally, Prometheus can send alerts if something goes wrong (like when CPU usage is too high). Grafana is an open-source tool used to create dashboards that show the data collected by Prometheus or Falco. It turns numbers and logs into easy-to-understand graphs and charts.
During this study, RBAC-Lookup were used for RBAC monitoring.

### 2.2.2 Secure Network Configuration and Isolation

To protect Kubernetes environments, it is important to use strong network communication and clear network policies.[14] These policies control how different parts of the system, such as pods and services, communicate with each other. By restricting connections to only those that are necessary, companies can reduce security risks and prevent threats from spreading within the cluster. Air-gapped environments can also be part of this security strategy, adding an extra layer of isolation from external networks.
Encrypting Pod-to-Pod communication is highly recommended, as Kubernetes' default network setup may expose unprotected data.[15]
Network policies are managed by Container Network Interface (CNI) plugins like Calico and Cilium, rather than Kubernetes itself. If these plugins or their data storage are compromised, security policies may fail.[16]
Policies should always follow the principle of least privilege.

### 2.2.3 Secure Pod and Container Configurations

Keeping the pod and container secure is very important and crucial because it directly affects the integrity of the entire cluster. The Pod Security Standards define three different policies that broadly cover the security spectrum:
*   **Privileged:** provides the widest possible level of permissions.
*   **Baseline:** a minimally restrictive policy that prevents known privilege escalations.
*   **Restricted:** a heavily restricted policy that follows current pod hardening best practices.

In this study, several hardening measures were applied across RKE2 clusters to ensure pod and container security within the air-gapped environment.

**Resource Control and Isolation**
CPU, memory, and storage limits were set for each pod using Kubernetes manifests and Linux Control Groups to prevent resource exhaustion or DoS attacks, emphasizing proper confinement as a core protection mechanism. [17]

**Privilege Restriction**
All containers ran as non-root users, using only the admin username and minimal capabilities. Privileged mode was disabled. Namespaces, capabilities, and seccomp were identified as the key defenses against container escape and host compromise. [18]

**Network Isolation**
The RKE2 cluster and supporting services operated entirely within isolated, air-gapped IP networks to prevent any external communication and ensure a secure internal environment.

### 2.2.4 Continuous Monitoring, Auditing, and Vulnerability Management

During this study, continuous monitoring and logging systems were implemented to track cluster performance, resource usage, and security events. Tools such as NeuVector and Rancher were used to observe pod behavior, detect unauthorized network traffic, and monitor real-time container activities inside the RKE2 cluster. Regular image and configuration checks were performed before deployment using Hauler bundles to reduce the risk of outdated or vulnerable components.
Security principles were integrated into the entire CI/CD workflow through GitLab and ArgoCD.
Although the air-gapped environment limited external scanning tools such as Trivy or Clair, internal audits and manual reviews were regularly conducted to ensure compliance with Kubernetes CIS Benchmarks and to maintain the integrity of the cluster.[18]

### 2.2.5 CI/CD Pipeline Security

This study applied several tools to ensure secure and controlled deployments in the air-gapped RKE2 environment. Only verified container images from the internal Hauler registry were used, preventing untrusted or internet-based sources from being deployed in the cluster.
The CI/CD workflow followed a pull-based model through ArgoCD, where the cluster pulled configuration and manifests directly from the private GitLab repository, keeping credentials safely inside the cluster and reducing exposure to unauthorized access. Authentication secrets were minimized and stored only in required namespaces, limiting the privileges of CI/CD tools and service accounts to prevent potential security vulnerabilities, following the principles of least privilege and secure automation.

## 2.3 Air-Gapped Deployments Strategies

Air-gapped deployments are mostly used in critical sectors such as transportation and industrial control systems, where systems are intentionally isolated from the public internet for safety reasons. This approach can reduce exposure to cyberattacks but creates challenges for software delivery, updates, and automation. As a result, during this project, these challenges were addressed by developing a controlled offline deployment workflow for the RKE2 cluster. 
Using tools like Hauler, container images and Helm charts were packaged into portable bundles and transferred to internal registries using a tool called MobaXterm. 
This ensured that only verified and cryptographically trusted components were deployed inside the isolated network, consistent with the security recommendations for railway communication systems. [19]
The integration of GitLab and ArgoCD within the isolated network IP enabled a secure pull-based deployment model, where configurations and manifests were synchronized directly from the private GitLab repository without exposing cluster credentials. This method provided the same level of traceability and control as online GitLab workflows while maintaining complete network isolation.
Human errors and procedural mistakes were also recognized as key risks in air-gapped operations; therefore, access control, documentation, and automation were emphasized to minimize manual errors and unauthorized changes. [20]

## 2.4 Observability and Runtime Security

Observability and runtime security were added directly to the ArgoCD deployment process to make the air-gapped RKE2 environment more reliable. Monitoring and security are essential parts that affect every level of the deployment pipeline. The pipeline also needs protection from possible attacks or other harmful scenarios. [21]
ArgoCD works as a Kubernetes controller and acts as a GitOps tool for continuous delivery. It is designed to automate the deployment of applications in Kubernetes.
ArgoCD continuously synchronizes and monitored the applications deployed from the private GitLab repository. This helped detect configuration changes or failed deployments early inside the isolated cluster. ArgoCD keeps watching the running applications and constantly checks if their current state matches the desired target state. This desired state is defined by configuration files stored in the Git repository, following the GitLabs idea that Git serves as the single source of truth.

In this approach ArgoCD works as an operator in a pull-based pipeline and continuously checks the repository for any changes, and when updates are found, it automatically keeps the deployed applications in the same state as the version stored in Git. This process can happen automatically or manually, but by changing the policy in ArgoCD to ‘automatic’, it will perform these checks continuously. If the deployed application differs from the target state, ArgoCD marks it as ‘OutOfSync’. The synchronization policy used in this GitLabs setup keeps everything aligned with the Git repository through specific settings, such as selfHeal: true (to automatically fix configuration drifts). In this case, GitLab becomes the single source of truth. In addition, monitoring the execution of deployment scripts helps detect possible errors during the deployment process, while ArgoCD offers real-time visibility of the running applications. [22] [1]

Integrating GitLab’s monitoring features with ArgoCD’s real-time protection creates a self-healing foundation for air-gapped, cloud-native systems. In this GitLab-based approach, tools like ArgoCD act as agents that automatically maintain the desired system state, reducing downtime and improving reliability, which is one of the main goals of cloud-native architecture.
This declarative GitLabs approach, which is adopted during this research, helps keep the infrastructure consistent and reduces the chance of human errors in the air-gapped RKE2 environment.
In the past, observability was mostly reactive, but it is now being integrated earlier in the development process. This approach embeds visibility directly into the code, build, and testing stages, making debugging faster and improving feedback loops. Modern observability relies on three key elements: logs, metrics, and traces. Within the deployment environment, monitoring tools such as Prometheus collect metrics from Kubernetes pods and system resources, while Grafana visualizes this data in dashboards, providing real-time insights into the performance and health of the cluster.[23]

While these tools provide a reliable foundation for automation, monitoring, and self-healing in cloud-native environments, their use in air-gapped infrastructures has received little attention in existing research.
Most studies focus on connected cloud systems, leaving a gap in understanding how these technologies can be effectively adapted for isolated industrial environments. This research addresses that gap by applying GitLab and ArgoCD in an air-gapped RKE2 cluster to achieve secure, automated, and observable software deployment.

**Table 1. Overview existing method & frameworks**

| Framework/Study | Core Focused and Contributions | Dimensions Considered |
| :--- | :--- | :--- |
| **[1], [2], [4]** | Define IaC as a foundation for automation and traceability; present GitLab as an integrated DevOps platform combining CI/CD and infrastructure management | Studies are limited to online cloud environments; lack validation in air-gapped or safety-critical infrastructures |
| **[7–15]** | Describe RBAC mechanisms, container hardening, and monitoring tools (Falco, Prometheus, Grafana) for Kubernetes security | Focused on open-network clusters; do not address offline or restricted environments |
| **[16], [17]** | Present security and operational methods for isolated networks, especially in railway and industrial contexts | Lack DevOps/IaC or GitLabs integration in air-gapped systems; mostly conceptual security frameworks |
| **[18]** | Multi-company case study showing manual configuration and inconsistent DevOps adoption; highlights lack of automation and homogeneous processes | Demonstrates limitations of manual deployment and absence of IaC; identifies need for declarative automation to ensure consistency and scalability |
| **[20], [21]** | Introduce GitOps and ArgoCD for automation, and define Shift-Left Observability for proactive monitoring in CI/CD | No practical integration of GitLabs and observability tools (GitLab + ArgoCD + Prometheus + Grafana) in air-gapped RKE2 clusters |
| **This research** | Implements IaC and GitOps principles in a real air-gapped industrial setup using GitLab, ArgoCD, Prometheus, and Grafana | Fills the identified gaps by demonstrating secure, automated, and observable cloud-native deployment under isolation |

---

# 3. Methodology

This methodology provides a clear and repeatable framework for studying how Infrastructure as Code (IaC) and GitOps automation can work together in air-gapped Kubernetes environments. It combines practical experimentation with real industrial conditions to show how automation and access control through RBAC can improve reliability and security in restricted systems.

## 3.1 Definition of Key Tools and Technologies

Before starting to describe the methodology, here is a short definition of what we used during the research:

*   **RKE2:** A secure, enterprise-grade Kubernetes distribution designed for high-compliance or air-gapped environments.
*   **Argo CD:** A GitOps controller that continuously monitors the desired state in a Git repository and applies it to a Kubernetes cluster to ensure the live state matches the declared one.
*   **Terraform:** An Infrastructure as Code tool that enables declarative scripting of infrastructure resources across clouds or on-premises, supporting repeatable provisioning.
*   **GitLab CI/CD:** A DevOps platform offering version control, continuous integration and delivery pipelines, used here as the internal repository and automation engine.
*   **Hauler:** An offline artifact packaging and registry tool designed to support container image and Helm chart delivery in disconnected or air-gapped environments.
*   **Helm:** A package manager for Kubernetes that packages, version-controls and deploys Kubernetes applications using charts, simplifying complex deployments.
*   **RBAC (Role-Based Access Control):** A security method that restricts access to system resources based on predefined roles and permissions, ensuring least-privilege access in Kubernetes clusters.[24]

## 3.2 Research Approach

This study follows a design-science and experimental research methodology focused on developing and validating a secure and automated deployment framework for air-gapped Kubernetes environments. The goal is to investigate how Infrastructure as Code (IaC) and GitLabs concepts can enable full automation, observability, and compliance within isolated, security-constrained datacenters.

The research integrates both quantitative evaluations. like., deployment time, drift detection rate, reproducibility and qualitative assessment like., maintainability, security, scalability. This mixed approach shows that the problem has two sides. it is technical and operational, but also organizational and process-driven, consistent with DevOps engineering studies.[25]

Although there is a large amount of research on DevOps and cloud-native automation, very few studies focus on the practical and security challenges of using GitOps and Infrastructure as Code in air-gapped environments. Most of the existing studies are on connected or hybrid cloud systems, where deployment pipelines depend on an Internet connection to download images and perform continuous updates.

However, because critical industries like railway often operate in isolated and offline networks to increase the security layer, normal CI/CD models do not work correctly. This research fills that gap by developing and testing a secure, reproducible, and fully automated GitOps-based framework that can work inside disconnected RKE2 clusters. In this way, it expands the current literature toward a less explored but highly important industrial field.

## 3.3 Methodological Framework

The methodological framework of this research follows the principles of Design-Based Research (DBR), which emphasizes building, testing, and refining practical solutions through iterative cycles. This approach was selected because it aligns well with engineering-oriented studies that aim to both design and validate technological artifacts.

The process began with an analysis of the problem, focusing on the challenges of manual deployments in air-gapped environments, where issues such as inconsistency, human error, and compliance risks are common.
In the development phase, a declarative automation architecture was designed using Infrastructure as Code (IaC) and GitOps principles to improve reproducibility and security.

During refinement and implementation, the proposed framework was deployed using RKE2, Argo CD, GitLab, and Terraform, all integrated with an offline Hauler registry. Each iteration was tested, adjusted, and optimized based on the results obtained.
Finally, the reflection and evaluation phase assessed the effectiveness of the solution using both quantitative and qualitative metrics, including deployment speed, reproducibility, and security compliance.

This iterative process allowed continuous learning and improvement, ensuring that both the technical and methodological aspects evolved together. The overall structure of this research aligns with Reeves’s Design-Based Research model.

*(Figure 1. Design-Based Research model [26])*

## 3.4 Research Design and Environment

The experimental environment was implemented entirely through virtualization using Proxmox VE with an isolated network bridge, providing a flexible and reproducible setup for the final demonstration. Three main virtual machines were deployed each serving a separate purpose within the air-gapped architecture.

**Table 2. Summarizes the virtual machines used in the experimental environment**

| VM | Role | Key Components |
| :--- | :--- | :--- |
| **Hauler** | Private offline registry | Hauler v1.2.5 |
| **RKE2** | Single-node(control-plane) | RKE2, kubectl, Helm, Argo CD |
| **Ansible-Runner** | Automation and playbook | Ansible, YAML-based playbooks |

The network was **completely air-gapped**, ensuring no outbound Internet connectivity for security and reproducibility. All required artifacts such as container images, Helm charts, and binary packages, were first downloaded from the Internet using a **separate Ubuntu workstation** connected outside the Proxmox environment. These resources were then packaged into **Hauler bundles (.tar.zst)** or standard **tar.gz archives**, transferred securely to the air-gapped VMs via **MobaXterm SCP** or USB drives, and finally extracted and imported into **Hauler** or other nodes as needed.

The **Hauler node** acted as the local image registry and chart repository, providing offline access to all dependencies required by RKE2, Rancher, and other components.
The **Ansible Runner VM** was used to automate installation and configuration tasks through declarative playbooks, ensuring that each setup could be reproduced consistently.
For specific CI/CD demonstrations, an optional **GitLab CE** instance was also deployed to host internal repositories and pipeline definitions. Each environment was rebuilt and tested multiple times to validate **reproducibility, automation accuracy, and deployment reliability**.

## 3.5 Tools and Components Used in Implementation

**Table 3. Tools and Components Used in the Study**

| Category | Tools | Function |
| :--- | :--- | :--- |
| Virtualization | Proxmox VE, Ubuntu 22.04 LTS | Multi-VM orchestration |
| Cluster Orchestration | RKE2 v1.29, kubectl | Kubernetes control-plane |
| Offline Repository | Hauler v1.2.5 | Packaging and image distribution |
| CI/CD & GitOps | GitLab CE, Argo CD v2.12 | Declarative deployment and sync |
| IaC Automation | Ansible, Terraform | Infrastructure provisioning |

## 3.6 Research Phases

The study methodology is divided into five consecutive phases:

1.  **Environment Initialization:**
    *   Install and configure the Hauler registry and RKE2 cluster.
    *   Validate offline image loading and TLS connectivity.
2.  **Automation Design (IaC):**
    *   Develop Ansible playbooks for one-button installation.
    *   Define Terraform modules for cluster provisioning.
3.  **GitOps Integration:**
    *   Connect Argo CD to GitLab repositories.
    *   Establish pull-based synchronization and self-healing mechanisms.
4.  **Security Hardening:**
    *   Define RBAC roles and cluster-level policies.

To provide a clear overview of the research process, the following diagram illustrates the overall workflow adopted in this study. Although the framework covers multiple stages, this research primarily focuses on the **IaC** and **GitOps** components specifically the integration between the **Git repository** and **Argo CD**.

*(Figure 2. The overall process and methodological workflow of the study)*

## 3.7 Data Collection and Evaluation Metrics

Both functional and performance metrics were collected:

**Table 4. Functional and performance metrics**

| Metric | Description | Measurement Method |
| :--- | :--- | :--- |
| **Deployment Duration** | Time required to provision and synchronize cluster components | Argo CD & Ansible logs |
| **Configuration Drift** | Deviations between desired vs actual state | Argo CD Sync Status |
| **System Health** | Pod uptime and resource availability | `kubectl get pods -A`, |
| **Network Isolation Validation** | Unauthorized outbound connections | tcpdump / iptables logs |

Data were analyzed quantitatively to compare manual vs automated deployments and qualitatively to interpret operational resilience.

## 3.8 Validation Strategy

The validation process was conducted through two complementary layers: **functional validation** and **security and performance validation**. Functional validation confirmed the successful synchronization of Argo CD under air-gapped conditions and verified the proper execution of automated rollback and drift correction mechanisms. 

The security and performance validation focused on testing RBAC enforcement based on the principle of least privilege, ensuring that access permissions were correctly applied and system behavior remained stable under restricted operational conditions.

***

**End of Part 1**
*Please let me know if you would like me to continue with Part 2 (Chapter 4: Implementation and beyond), as providing the remaining detailed logs, terminal commands, and analyses will require an additional response block to fit within system limits.*
