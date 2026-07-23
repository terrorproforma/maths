# Manuscript build

The source file is `subtree_shuffling_counterexample.tex`.

```bash
latexmk -pdf -file-line-error -halt-on-error -interaction=nonstopmode subtree_shuffling_counterexample.tex
```

The repository workflow compiles the manuscript, uploads the PDF as a workflow artifact, and commits the reviewed build to this directory on the review branch.

The author line is intentionally anonymous. Replace it only after the human contributors agree on authorship and disclosure.
