# Project Plan: State of the Art Paper (Air-Gapped Kubernetes)

## Goal
Produce a concise academic review (5-8 pages) in French on the **"State of the Art of Kubernetes Deployment and Supply Chain Security in Air-Gapped Environments"**. This document will serve as a rigorous analysis of existing methodologies, justifying modern architectural choices like OCI Artifact Packaging and GitOps.

## Strategy
*   **Format:** Academic/Thesis Chapter (Rigorous, Standardized).
*   **Language:** French.
*   **Analysis Method:** Taxonomy-based (Categorizing deployment strategies by their architectural paradigm).
*   **Key Comparison Criteria:**
    1.  **Maintainability (Day 2 Ops):** Ease of updates and patching.
    2.  **Security & Compliance:** Adherence to RGPD/Air-Gap strictures and supply chain integrity.
    3.  **Developer Experience (DX):** Friction levels for development teams.
    4.  **Portability:** Avoidance of vendor lock-in.
*   **Role of CASD PoC:** It will be cited as a concrete implementation example of "Strategy C" (OCI Packaging), treated alongside other examples in the literature.

## Roadmap

### Phase 1: Structure & Outline
- [x] Define the core thesis and scope (Option B: State of the Art).
- [x] Establish the Taxonomy of Strategies.
- [ ] **Current Step:** Validate detailed outline in `PLAN.md`.

### Phase 2: Drafting Content (Iterative)
- [ ] **Draft Section 1: Introduction**
    - Context: The "Air-Gap Paradox" (Cloud Native agility vs. Physical isolation).
    - Problem: Software Supply Chain Security (SSCS) without internet.
- [ ] **Draft Section 2: Taxonomy of Strategies**
    - *Stratégie A : Transfert de Fichiers Ad-hoc ("Sneaker-netting").*
    - *Stratégie B : Miroirs de Registres (Legacy Enterprise).*
    - *Stratégie C : Packaging d'Artefacts OCI (Modern/Zarf/Hauler).*
    - *Stratégie D : Exécution de Confiance (Trusted Execution Environments/Asylo).*
- [ ] **Draft Section 3: Comparative Analysis**
    - Evaluate strategies A-D against the 4 criteria (Maintainability, Security, DX, Portability).
- [ ] **Draft Section 4: Conclusion**
    - Synthesis: Why OCI Packaging + GitOps is the converging standard.

### Phase 3: Review & Refine
- [ ] Review for academic tone (French).
- [ ] Verify integration of sources (Heckathorn, Gheibi, Asylo paper).
- [ ] Final formatting.

---

## Detailed Paper Outline (Target Structure)

### 1. Introduction
*   **Contexte :** L'adoption croissante de Kubernetes dans les infrastructures critiques (Défense, Santé, Finance) et la tension avec les exigences de souveraineté (Air-Gap).
*   **Problématique :** Comment garantir la sécurité de la chaîne d'approvisionnement logicielle (SSCS) et maintenir l'agilité (DevOps) dans un environnement physiquement déconnecté ?

### 2. Taxonomie des Stratégies de Déploiement
Cette section classe les approches identifiées dans la littérature et l'industrie.

*   **2.1 Stratégie A : Le Transfert Ad-hoc ("Sneaker-netting")**
    *   *Description :* Téléchargement manuel de tarballs Docker (`docker save/load`) et de binaires.
    *   *Analyse :* Approche naïve, non reproductible, risque élevé d'erreur humaine et de "Configuration Drift".

*   **2.2 Stratégie B : Réplication de Registres (Miroirs Traditionnels)**
    *   *Description :* Mise en place de miroirs complets (Artifactory, Nexus) synchronisés périodiquement.
    *   *Analyse :* Standard industriel actuel. Robuste mais lourd à maintenir (coût infrastructurel, complexité de synchronisation).

*   **2.3 Stratégie C : Packaging Déclaratif d'Artefacts OCI (L'approche Moderne)**
    *   *Description :* Utilisation de l'image OCI comme conteneur universel pour tout (images, charts Helm, fichiers). Outils : **Hauler**, **Zarf**.
    *   *Analyse :* "Tout est code". Permet l'Application de GitOps en déconnecté. C'est l'approche utilisée par le projet CASD.

*   **2.4 Stratégie D : Isolation Matérielle et Exécution de Confiance (TEE)**
    *   *Description :* Protection des workloads contre l'infrastructure elle-même via Intel SGX/Asylo (réf. papier Asylo).
    *   *Analyse :* Niveau de sécurité maximal (Zero Trust), mais complexité d'implémentation et dépendance matérielle.

### 3. Analyse Comparative et Discussion
Tableau comparatif des stratégies selon les critères définis :
*   **Maintenabilité :** La Stratégie C offre le meilleur compromis grâce à l'automatisation.
*   **Sécurité :** La Stratégie D est supérieure mais coûteuse. La C offre une excellente traçabilité (Supply Chain).
*   **Expérience Développeur (DX) :** La Stratégie B et C tentent d'imiter l'expérience connectée.
*   **Portabilité :** Les approches basées sur OCI (C) sont les plus agnostiques.

### 4. Conclusion
*   Synthèse des tendances.
*   Recommandation de l'approche hybride : Packaging OCI (Hauler) couplé à des pratiques GitOps rigoureuses pour concilier sécurité et vélocité.
