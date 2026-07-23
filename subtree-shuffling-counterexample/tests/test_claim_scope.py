from pathlib import Path


def test_repository_states_only_the_fixed_pair() -> None:
    root = Path(__file__).resolve().parents[1]
    status = (root / "STATUS.md").read_text(encoding="utf-8")
    assert "d = 7, p = 15" in status
    assert "does **not** claim failure for every `p >= 15`" in status


def test_manuscript_source_exists() -> None:
    root = Path(__file__).resolve().parents[1]
    assert (root / "paper" / "subtree_shuffling_counterexample.tex").is_file()
