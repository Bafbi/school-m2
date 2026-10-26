// junia_template.typ

// --- Helper Functions ---
#let spacer = v(1em)

// --- Main Project Template ---
#let project(
  title: "",
  subtitle: "UE 11 - Veille et prospectives technologiques",
  author: "",
  promotion: "Cycle Ingénieur - 5ème année",
  date: datetime.today().display("[month repr:long] [year]"),
  tutor_school: "",
  confidential: false, // Rarement confidentiel pour un état de l'art académique
  logo_school: none, 
  
  // Contenu optionnel (désactivé par défaut pour ce format court)
  show_abstract: false,
  show_toc: false, 
  show_figures_list: false,
  show_info_block: false,

  abstract_content: [],
  keywords: (),
  
  body
) = {
  // 1. CONFIGURATION GLOBALE
  // Police Arial (ou équivalent) taille 11pt
  set text(font: "Liberation Sans", size: 11pt, lang: "fr")
  
  // Marges 2.5cm partout
  set page(
    paper: "a4",
    margin: 2.5cm,
  )

  // Paragraphes : Justifiés, interligne 1.5 max
  set par(justify: true, leading: 0.8em, first-line-indent: 0pt, spacing: 1.5em)
  
  // Titres : Numérotés 1. 1.1. 1.1.1.
  set heading(numbering: "1.1")
  show heading: it => {
    set text(weight: "bold", font: "Liberation Sans")
    if it.level == 1 {
      pad(bottom: 0.5em, top: 1em, text(size: 14pt, fill: rgb("#303030"), upper(it)))
    } else {
      pad(bottom: 0.5em, top: 0.5em, text(size: 12pt, fill: rgb("#303030"), it))
    }
  }

  // Figures et Tableaux : Légendes
  show figure.where(kind: table): set figure.caption(position: top)
  show figure.caption: it => [
    #text(style: "italic", size: 10pt)[#it]
  ]

  // 2. PAGE DE COUVERTURE (FICHE A)
  set page(numbering: none, header: none, footer: none)
  
  // Logos en haut
  grid(
    columns: (1fr, 1fr),
    align: (left, right),
    if logo_school != none { image(logo_school, width: 4cm) } else { rect(width: 4cm, height: 1.5cm, fill: luma(240))[Logo JUNIA] },
    // Pas de logo entreprise obligatoire pour ce cours, sauf si lié au stage
    [] 
  )

  v(4fr)

  // Bloc Titre
  align(center)[
    #text(size: 14pt)[#subtitle] \
    #v(1em)
    #rect(inset: 2em, stroke: 2pt + rgb("#403075"), radius: 5pt)[
      #text(size: 20pt, weight: "bold", fill: rgb("#403075"))[#title]
    ]
    #v(1em)
    #if confidential [
      #text(fill: red, weight: "bold")[CONFIDENTIEL]
    ]
  ]

  v(4fr)

  // Bloc Info Bas
  if show_info_block {
      align(center)[
    En vue de l'obtention du diplôme *#promotion* \
    \
    Enseignant référent : #tutor_school
  ]

  v(2fr)
  }


  // Pied de page couverture
  grid(
    columns: (1fr, 1fr),
    align: (left, right),
    text(weight: "bold")[#author],
    text(style: "italic")[#date]
  )
  
  pagebreak()

  // 3. ÉLÉMENTS OPTIONNELS (Si activés)
  if show_abstract {
    heading(outlined: false, numbering: none)[Résumé]
    abstract_content
    v(1em)
    [*Mots clés :* #keywords.join(", ")]
    pagebreak()
  }

  if show_toc {
    outline(title: "Sommaire", indent: auto, depth: 2)
    pagebreak()
  }

  // 4. CONFIGURATION DU CORPS DE TEXTE
  // La numérotation commence ici
  set page(
    numbering: "1",
    header: [
      #text(size: 9pt, style: "italic")[#title]
      #h(1fr)
      #context(counter(page).display())
    ],
  )
  counter(page).update(1)

  body
  
  // La bibliographie doit être appelée dans le fichier main.typ
}