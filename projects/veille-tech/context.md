# État de l'Art : Contexte et Sujet

```md
# Architecture and Concepts

This document outlines the architectural decisions, design philosophy, and core concepts behind the Kubernetes environment project.

## Project Goal

The primary objective is to establish a **reliable, reproducible, and automated** method for setting up Kubernetes environments, specifically tailored for hosting services within an **air-gapped** infrastructure.

While currently serving as a Proof of Concept (PoC) for experimentation and testing, the project is built on strict **Infrastructure as Code (IaC)** and **DevOps** principles. The long-term vision is to maintain a "Single Source of Truth" repository that can bootstrap a production-ready environment from scratch with minimal human intervention.

## Core Philosophies

### 1\. Single Source of Truth

The repository is designed to be the definitive state of the infrastructure. Modifications occur via code changes, ensuring that the entire state can be recreated or recovered at any time.

### 2\. Air-Gap First & RGPD Compliance

Due to strict **RGPD certification** and security regulations, we cannot use public cloud services. \* **Bare Metal / On-Premise**: Everything runs on internal hardware using Hyper-V. \* **Vendoring**: All dependencies (binaries, images, tools) are bundled locally. \* **Bastion Model**: Setup is prepared in a connected zone and transferred to an isolated "Bastion" machine that manages the secure network.

### 3\. Developer Experience (DX)

We use a high-performance "glue" layer (**Mise**) to automate complex workflows, keeping the development cycle fast even within a complex monorepo.

### 4\. Opinionated Framework

The project is built as a portable engine. It separates the **Engine** (the logic of _how_ to build) from the **Manifest** (the data of _what_ to build).
```

C'est un excellent contexte de projet. Le défi principal de votre sujet est la contradiction apparente entre des méthodologies "Cloud Native" (Kubernetes, DevOps, GitOps, mise à jour continue) et des contraintes d'infrastructure très rigides (Air-gapped, Bare Metal, On-premise, RGPD/Souveraineté).

C'est exactement ce type de tension qui fait un excellent sujet d'État de l'Art : Comment concilier l'agilité moderne avec des contraintes de sécurité maximales ?

### La sécurité de la chaîne d'approvisionnement logicielle (Software Supply Chain) en milieu déconnecté

C'est le sujet le plus lié à votre contrainte "Air-Gap" et "Vendoring". La littérature scientifique actuelle regorge d'articles sur la sécurité de la Supply Chain (post-SolarWinds), mais souvent dans un contexte connecté.

-   **Lien avec le projet :** Votre "Bastion Model" et le "Vendoring" local.
    
-   **Problématique :** Quels sont les paradigmes architecturaux permettant de garantir l'intégrité et la mise à jour continue (CI/CD) d'orchestrateurs de conteneurs dans des infrastructures critiques isolées (Air-gapped) ?
    
-   **Ce que vous allez analyser :**
    
    -   Les limites des approches classiques (téléchargement direct).
        
    -   Les solutions de "Mirroring" et de signature cryptographique (ex: Sigstore, TUF - The Update Framework).
        
    -   Les risques de sécurité spécifiques aux transferts "Bastion".
        
    
-   **Mots-clés pour recherche (IEEE/Scholar) :** Air-gapped networks security, Software Supply Chain Security, Kubernetes offline deployment, Secure artifact delivery, CI/CD in critical infrastructure.

