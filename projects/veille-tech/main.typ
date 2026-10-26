#import "junia_template.typ": project

#show: project.with(
  title: "État de l'Art : Déploiement et Sécurité d'un Déploiement Kubernetes en Environnement Isolé (Air-Gapped)",
  subtitle: "UE 11 - Veille et prospectives technologiques",
  author: "Eudeline Nathan",
  promotion: "Cycle Ingénieur - 5ème année",
  date: "Janvier 2026",
  confidential: false,
  show_toc: false, 
  show_abstract: false,
  logo_school: "assets/school_logo.svg",
  keywords: ("Kubernetes", "Air-Gap", "DevOps", "GitOps", "Supply Chain Security", "OCI Packaging", "TEE", "OCI Registry", "ArgoCD"),
)

= Introduction

== Contexte : Le Paradoxe de l'Air-Gap

L'adoption des architectures "Cloud Native" et de Kubernetes est devenue le standard _de facto_ pour le déploiement d'applications modernes, promettant vélocité, scalabilité et résilience. Cependant, une fracture persiste entre ces méthodologies, conçues pour un monde hyper-connecté, et les réalités opérationnelles des infrastructures critiques (Défense, Santé, Finance, Recherche sécurisée) @gheibi2025.

Ces environnements, soumis à des contraintes strictes de souveraineté et de sécurité (RGPD, certifications gouvernementales), opèrent souvent en mode *"Air-Gap"* : ils sont physiquement ou logiquement isolés de l'Internet public. Cette isolation crée un paradoxe fondamental : comment bénéficier de l'agilité du modèle DevOps et de l'écosystème Kubernetes, qui dépendent intrinsèquement de dépôts publics et de mises à jour continues, au sein d'une infrastructure figée par conception pour des raisons de sécurité ?

== Problématique : La Sécurité de la Chaîne d'Approvisionnement en Milieu Déconnecté

La problématique centrale ne se limite pas à l'installation initiale d'un cluster, mais concerne la pérennité et la sécurité de la *Chaîne d'Approvisionnement Logicielle (Software Supply Chain Security - SSCS)*.

Dans un contexte connecté, la sécurité repose sur la validation en temps réel des signatures et la mise à jour continue des vulnérabilités (CVE). En environnement déconnecté, ces mécanismes sont rompus @heckathorn2023. Les opérateurs font face à un double défi :

1. *L'Intégrité du Transfert :* Comment garantir que les artefacts (images de conteneurs, binaires, configurations) importés depuis l'extérieur (le "Bastion") n'ont pas été compromis lors du transit ("Sneaker-netting") ?
2. *La Maintenabilité (Day 2 Ops) :* Comment éviter la dérive de configuration ("Configuration Drift") et l'obsolescence rapide des systèmes lorsque chaque mise à jour nécessite une intervention manuelle complexe ?

Cet état de l'art analyse les stratégies actuelles permettant de résoudre ces tensions, en comparant les approches historiques de réplication de registres aux nouvelles méthodes de packaging déclaratif d'artefacts OCI.

= Taxonomie des Stratégies de Déploiement

Cette section classe les approches identifiées dans la littérature et l'industrie pour déployer Kubernetes en environnement déconnecté.

== Stratégie A : Le Transfert Ad-hoc ("Sneaker-netting")

La méthode la plus primitive, souvent qualifiée de "Sneaker-netting", repose sur le transfert manuel de fichiers.

- *Mécanisme :* Les opérateurs utilisent des commandes impératives comme `docker save` pour exporter des images sous forme de fichiers `.tar`, téléchargent manuellement les binaires Kubernetes, et copient le tout sur des supports physiques (clés USB, disques durs) pour les importer dans la zone sécurisée (`docker load`) @heckathorn2023.
- *Analyse :* Bien que simple en apparence pour un déploiement unique, cette approche est considérée comme un *anti-pattern* moderne. Elle n'est pas reproductible, est hautement sujette à l'erreur humaine, et rend la gestion des dépendances (transitives) cauchemardesque. Elle ne permet aucune traçabilité fiable de la chaîne logistique.

== Stratégie B : Réplication de Registres (Miroirs Traditionnels)

C'est l'approche standard dans les grandes entreprises depuis une décennie.

- *Mécanisme :* Elle implique la mise en place d'une infrastructure lourde de "registres miroirs" (ex: JFrog Artifactory, Sonatype Nexus) à l'intérieur de la zone sécurisée. Ces registres sont périodiquement synchronisés avec l'extérieur via des passerelles unidirectionnelles (diodes de données) ou des procédures de transfert par lot.
- *Analyse :* Cette stratégie offre une expérience développeur proche du mode connecté (on tire les images depuis un registre). Cependant, elle impose un coût infrastructurel élevé et une complexité opérationnelle majeure pour maintenir la cohérence des miroirs. La sécurité repose entièrement sur la confiance accordée au point d'entrée du miroir.

== Stratégie C : Packaging Déclaratif d'Artefacts OCI (L'approche Moderne)

L'industrie converge aujourd'hui vers une approche qui traite "tout comme un artefact OCI" (Open Container Initiative) @ocispec2025.

- *Fondation Technique :* La spécification OCI Image Format définit un standard ouvert pour les images de conteneurs, comprenant un manifeste (métadonnées), des couches de système de fichiers (layers), et une configuration runtime. La version 1.1 introduit le support des *OCI Artifacts*, permettant de packager du contenu arbitraire (Helm charts, SBOMs, signatures) au-delà des simples images @ocispec2025.

- *Mécanisme :* Des outils comme *Hauler* @hauler2024 ou *Zarf* @smith2021devsecops exploitent le format *OCI Image Layout*—une structure de répertoire portable et vérifiable par hash (SHA-256). Ces outils permettent d'encapsuler non seulement les images Docker, mais aussi les charts Helm, les fichiers de configuration, et les binaires dans un package unique, signé et immuable.

- *Analyse :* C'est l'approche adoptée par le projet CASD. Elle permet d'appliquer les principes *GitOps* même en déconnecté : le package devient la "Vérité Terrain". L'adressage par contenu (content-addressable storage) garantit l'intégrité sans connexion réseau : chaque blob est identifié par son empreinte SHA-256, permettant une vérification cryptographique à la volée. Elle simplifie considérablement la chaîne logistique en réduisant le problème de synchronisation à un simple transfert de fichier monolithique @gheibi2025. De plus, cette méthode permet le déploiement de plateformes complètes (PaaS) via des outils déclaratifs, validés dans des contextes opérationnels contraints comme les sous-marins @smith2021devsecops.

== Stratégie D : Isolation Matérielle et Exécution de Confiance (TEE)

Une approche émergente pour les environnements à très haute sécurité (Zero Trust).

- *Mécanisme :* Décrite notamment par les travaux sur *Asylo* @asylo2021, cette stratégie ne se contente pas de sécuriser le transport, mais protège l'exécution elle-même. Les workloads tournent dans des enclaves matérielles (Intel SGX), garantissant que même l'administrateur de l'infrastructure (le fournisseur IaaS ou l'admin système) ne peut pas accéder aux données ou au code en mémoire.
- *Analyse :* Bien qu'offrant le niveau de sécurité ultime, cette approche ajoute une complexité significative (recompilation des applications, dépendances matérielles) et reste pour l'instant réservée aux cas d'usage les plus critiques, souvent en complément de la Stratégie C.

= Analyse Comparative et Discussion

Afin d'identifier la solution optimale, cette étude compare les stratégies selon quatre critères clés identifiés dans la littérature : la *Maintenabilité* (facilité de mise à jour), la *Sécurité/Conformité* (respect du modèle Air-Gap), l'*Expérience Développeur* (DX), et la *Portabilité*.

#figure(
  table(
    columns: (auto, auto, auto, auto, auto),
    inset: 10pt,
    align: horizon,
    [*Critères*], [*Strat. A* \ (Ad-hoc)], [*Strat. B* \ (Miroir)], [*Strat. C* \ (Packaging OCI)], [*Strat. D* \ (TEE/Asylo)],
    
    [Maintenabilité], [Faible], [Moyenne], [Élevée], [Moyenne],
    [Sécurité], [Faible], [Moyenne], [Élevée], [Très Élevée],
    [Exp. Développeur], [Pénible], [Bonne], [Très Bonne], [Complexe],
    [Portabilité], [Moyenne], [Faible], [Très Élevée], [Faible (Hardware)]
  ),
  caption: [Comparaison des stratégies de déploiement Air-Gap. Source : Auteur],
)

== Compromis Sécurité vs Agilité

L'analyse révèle que la *Stratégie C (Packaging OCI)* offre actuellement le meilleur compromis ("Sweet Spot"). Contrairement à la Stratégie A, elle garantit la *reproductibilité* grâce à une approche déclarative ("Infrastructure as Code"). Contrairement à la Stratégie B, elle est agnostique de l'infrastructure et évite le coût de maintenance de miroirs lourds @heckathorn2023.

La *Stratégie D (TEE)*, bien que supérieure sur le plan de la sécurité pure, impose une "taxe" trop élevée sur la vélocité de développement pour être généralisée à tous les services, comme le montre le surcoût de compilation (~900s vs 26s) relevé dans l'étude Asylo @asylo2021.

== L'Émergence du "GitOps Déconnecté"

L'innovation majeure identifiée est la capacité d'appliquer le modèle *GitOps* en environnement isolé. En combinant un outil de packaging (comme Hauler) avec un contrôleur GitOps (comme ArgoCD) configuré pour pointer vers ce registre local, on parvient à réconcilier la boucle de rétroaction DevOps avec l'isolation physique. Le "colis" transporté devient l'état désiré du système, permettant une auditabilité totale.

= Conclusion

L'état de l'art du déploiement Kubernetes en environnement Air-Gapped a considérablement évolué. Historiquement caractérisé par une ère de "bricolage" manuel (Stratégie A), le domaine a traversé une phase industrielle basée sur la réplication (Stratégie B), pour atteindre aujourd'hui l'ère du *packaging autonome* (Stratégie C).

Pour des projets comme celui du CASD, qui visent à concilier conformité stricte (RGPD) et modernisation technologique, l'approche par *Packaging d'Artefacts OCI* couplée au *GitOps* s'impose comme la référence. Elle permet de transformer la contrainte de l'Air-Gap non plus en un obstacle opérationnel, mais en une simple étape formelle d'un pipeline automatisé et sécurisé.

Les perspectives futures se tourneront vers l'intégration native de la vérification de signatures (ex: Sigstore/Cosign) directement au niveau des contrôleurs d'admission Kubernetes, renforçant encore la chaîne de confiance sans intervention humaine.

#pagebreak()
#bibliography("references.bib", title: "Références Bibliographiques", style: "ieee")
