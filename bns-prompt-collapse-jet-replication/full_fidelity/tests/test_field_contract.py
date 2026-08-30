from __future__ import annotations

from pathlib import Path

import h5py
import numpy as np
import pytest

from bnsjet.errors import ArtifactError
from bnsjet.field_contract import validate_field_snapshot


def write_snapshot(path: Path, *, omit_rho: bool = False) -> None:
    with h5py.File(path, "w") as handle:
        handle.attrs["contract_version"] = 1
        handle.attrs["coordinate_system"] = "Cartesian"
        handle.attrs["length_unit"] = "km"
        handle.attrs["mass_unit"] = "Msun"
        handle.attrs["time_unit"] = "s"
        handle.attrs["solver"] = "test"
        handle.attrs["campaign_id"] = "test-campaign"
        coordinates = handle.create_group("coordinates")
        coordinates["x"] = np.linspace(-1.0, 1.0, 3)
        coordinates["y"] = np.linspace(-1.0, 1.0, 3)
        coordinates["z"] = np.linspace(-1.0, 1.0, 3)
        fields = handle.create_group("fields")
        shape = (3, 3, 3)
        if not omit_rho:
            fields["rho"] = np.ones(shape)
        fields["pressure"] = np.ones(shape)
        fields["temperature"] = np.ones(shape)
        fields["ye"] = np.full(shape, 0.1)
        fields["b_squared"] = np.ones(shape)
        fields["u_t"] = np.full(shape, -1.0)
        fields["sqrt_gamma"] = np.ones(shape)
        metric = handle.create_group("metric")
        metric["lapse"] = np.ones(shape)
        meta = handle.create_group("meta")
        meta["time_s"] = 0.1


def test_valid_snapshot(tmp_path: Path) -> None:
    path = tmp_path / "snapshot.h5"
    write_snapshot(path)
    summary = validate_field_snapshot(path)
    assert summary["attributes"]["campaign_id"] == "test-campaign"
    assert summary["datasets"]["/fields/rho"]["shape"] == [3, 3, 3]


def test_missing_dataset_rejected(tmp_path: Path) -> None:
    path = tmp_path / "snapshot.h5"
    write_snapshot(path, omit_rho=True)
    with pytest.raises(ArtifactError):
        validate_field_snapshot(path)
