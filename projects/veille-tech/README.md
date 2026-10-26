# veille-tech — technology watch report: air-gapped Kubernetes at the CASD

M2 "Veille et prospectives technologiques" report, written in Typst.

The subject is cloud-native infrastructure in an air-gapped, on-premises
environment, framed around the CASD (secure data centre): Kubernetes CI/CD
without internet access, containerised DevSecOps on constrained platforms, and
the trust/attestation questions that come with it.

```
main.typ                 report source (Typst), junia_template.typ for the school layout
main.pdf, main_new.pdf   renders; Eudeline_Nathan.pdf is the submitted copy
research/                source papers (pdf) + rewritten summaries (md) + index.md
references.bib           bibliography
PLAN.md, context.md      outline, brief and constraints
index.md                 index of the research corpus
```

`main.typ` and `main_new.typ` are two generations of the same document; the
submitted version is `Eudeline_Nathan.pdf`.

Not committed: `.venv`, and the `CASD-EU/kube` working copy that was cloned into
this directory as a reference.
