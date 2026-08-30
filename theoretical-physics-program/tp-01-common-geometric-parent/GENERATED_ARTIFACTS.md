# Generated artifacts

The canonical repository record is source-first. The original v1.1 package also contained compiled PDFs and generated PNG figures. They are intentionally not treated as irreplaceable source files here because the GitHub connector used for this import accepts UTF-8 repository content but not arbitrary local binary uploads.

Run:

```bash
python -m pip install -r requirements.txt
make all
```

to regenerate the verification results, figures and paper from the committed sources. `manifest_sha256.csv` preserves the checksums of the original complete package, including generated binaries.

Nothing mathematical has been reconstructed from screenshots or silently substituted for unavailable source.
