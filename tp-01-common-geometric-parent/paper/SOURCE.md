# Manuscript source storage

The original 49,719-byte LaTeX manuscript is stored losslessly as seven UTF-8 chunks in `source_chunks/` because the repository connector used for this import has conservative per-file transfer limits.

Run:

```bash
python paper/rebuild_source.py
```

The script concatenates the chunks, verifies the original SHA-256 value

```text
e0a531a8aa65a5118527be0bf5caac18471d792fd139fe1b59fe4ef4a5b2b3dd
```

and writes `paper/tp01_dirac_brst_global_audit_v1_1.tex`. `make paper` performs this step automatically before compilation.
