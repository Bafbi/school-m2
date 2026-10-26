# 

> **scholar_lab** : [find paper about Air-gapped networks security, Software Supply Chain Security, Kubernetes offline deployment, Secure artifact delivery, CI/CD in critical infrastructure.](https://scholar.google.com/scholar_labs/search/session/7283378697407931117?hl=en)

## Papers
- [A DevSecOps Approach for Developing and Deploying Containerized Cloud-Based Software on Submarines](A%20DEVSECOPS%20APPROACH%20FOR%20DEVELOPING%20AND%20DEPLOYING%20CONTAINERIZED%20CLOUD-BASED%20SOFTWARE%20ON%20SUBMARINES.pdf) ([Summary](AGENT_A_DevSecOps_Approach_for_Developing_and_Deploying_Containerized_Cloud_Based_Software_on_Submarines.md)). Context: NPS 2021 master's thesis on DevSecOps for submarine CANES in air-gapped, resource-constrained environments. Summary: Adapts Big Bang into the CocoWow PaaS and uses ZARF for declarative air-gap delivery; validates with CANES lab and sandbox tests and provides recommendations for scaling.
- [Kubernetes (k8s) in the Air Gap](https://insights.sei.cmu.edu/documents/6212/kubernetes_in_the_air_gap.pdf) ([Summary](AGENT_kubernetes_in_the_air_gap.md))
- [Challenges in applying cloud cutting edge technologies in air gapped on premises datacenters](Challenges%20in%20applying%20cloud%20cutting%20edge%20technologies%20in%20air%20gapped%20on%20premises%20datacenters.txt) ([Summary](AGENT_Challenges_in_applying_cloud_cutting_edge_technologies.md))
- [A kubernetes ci/cd pipeline with asylo as a trusted execution environment abstraction framework](https://ieeexplore.ieee.org/abstract/document/9376148/) ([Summary](AGENT_A_Kubernetes_CICD_Pipeline_with_Asylo.md))
- [Sfide nell'applicazione di tecnologie cloud all'avanguardia in data center on-premise air-gapped](http://unire.unige.it/handle/123456789/14442)

## Specifications
- [OCI Image Format Specification](https://github.com/opencontainers/image-spec) ([Summary](AGENT_OCI_Image_Spec.md))


## Tools

### OCI (Open Container Initiative)
*Foundational standard enabling air-gap tooling.*

The OCI Image Format is the industry-standard specification for container images. It defines:
- **Image Manifest**: Describes image components (config, layers)
- **Image Layout**: Portable directory format for storing/transporting images
- **Artifacts**: Extensible format for packaging non-image content (Helm charts, SBOMs, signatures)

Tools like Hauler and Zarf work by manipulating OCI-formatted content, making this spec fundamental to understanding air-gap deployment strategies.

**Key Documents:**
- [Full Specification](https://github.com/opencontainers/image-spec/blob/main/spec.md)
- [Image Layout Format](https://github.com/opencontainers/image-spec/blob/main/image-layout.md)
- [Artifacts Guidance](https://github.com/opencontainers/image-spec/blob/main/artifacts-guidance.md)

### Hauler
What's Hauler? [#​](https://docs.hauler.dev/docs/intro#whats-hauler)

`Hauler` simplifies the airgap experience without requiring operators to adopt a specific workflow. `Hauler` simplifies the airgapping process, by representing assets (images, charts, files, etc...) as content and collections to allow operators to easily fetch, store, package, and distribute these assets with declarative manifests or through the command line.

`Hauler` does this by storing contents and collections as OCI Artifacts and allows operators to serve contents and collections with an embedded registry and fileserver. Additionally, `Hauler` has the ability to store and inspect various non-image OCI Artifacts.

- **repo** : [github@hauler-dev/hauler](https://github.com/hauler-dev/hauler)
- **doc** : [hauler docs #Airgap Swiss Army Knife](https://docs.hauler.dev/docs/intro)

### Asylo
*Featured in "A Kubernetes CI/CD Pipeline with Asylo..." paper.*

Asylo is an open-source framework from Google for developing applications that run in Trusted Execution Environments (TEEs) like Intel SGX. It allows developers to "wrap" applications to ensure confidentiality and integrity, protecting them even from the infrastructure provider or host admin.

### Tekton
*Orchestrator used in "A Kubernetes CI/CD Pipeline with Asylo..." paper.*

Tekton is a powerful, flexible, open-source framework for creating CI/CD systems, allowing developers to build, test, and deploy across cloud providers and on-premise systems. It runs native to Kubernetes using Custom Resource Definitions (CRDs).

### Kaniko
*Builder used in "A Kubernetes CI/CD Pipeline with Asylo..." paper.*

Kaniko is a tool to build container images from a Dockerfile, inside a container or Kubernetes cluster. It does not require a Docker daemon, making it secure and ideal for environments where privileged access is restricted.

### NeuVector
*Featured in "Challenges in applying cloud..." thesis.*

NeuVector is a container security platform that provides real-time threat detection, vulnerability scanning, and network segmentation. In air-gapped environments, it offers critical runtime visibility and protection without relying on external cloud intelligence.

### Argo CD & GitOps
*Validated for offline use in "Challenges in applying cloud..." thesis.*

Argo CD is a declarative, GitOps continuous delivery tool for Kubernetes. It can function effectively in air-gapped environments by synchronizing with internal Git repositories (e.g., self-hosted GitLab) and pulling images from private offline registries (like Hauler).

### Zarf
*Mentioned in "Kubernetes (k8s) in the Air Gap" as a primary tool alongside Hauler.*

Zarf helps simplify the deployment of a private registry in the air gap. It achieves this by defining required artifacts (containers, Helm Charts) as code, allowing for reproducible, versioned actions. Like Hauler, it facilitates fetching, packaging, and deploying applications in disconnected environments.

### Air-Gap Friendly K8s Distributions
The following distributions are noted for their ease of configuration for air-gapped environments (e.g., registry mirroring):
- **k3s**: Lightweight Kubernetes. Configured via `registries.yaml`.
- **RKE2**: Rancher Kubernetes Engine 2. Secure, government-grade distribution used in the "Challenges..." thesis.
- **Talos**: Container-optimized Linux OS. Configured via `--registry-mirror` or machine config.
