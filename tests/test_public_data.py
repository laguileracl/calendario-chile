"""Tests del repo público sobre los datos incluidos (muestra + API estática)."""
from datetime import date

from calendario_chile.constants import TYPE_ENUM, CATEGORY_ENUM, VALID_ISO


def _d(s):
    return date.fromisoformat(s)


def test_dataset_not_empty(records):
    assert len(records) > 0


def test_dates_valid_and_ordered(records):
    for r in records:
        _d(r["start_date"]); _d(r["end_date"])
        assert r["start_date"] <= r["end_date"]
        assert r["year"] == int(r["start_date"][:4])


def test_type_and_category_enums(records):
    assert all(r["type"] in TYPE_ENUM for r in records)
    assert all(r["category"] in CATEGORY_ENUM for r in records)


def test_iso_subdivisions(records):
    for r in records:
        for s in r["subdivisions"]:
            assert s in VALID_ISO


def test_multiday_duration(records):
    for r in records:
        if r["is_multiday"]:
            assert r["duration_days"] > 1


def test_public_safe_no_internal_block(records):
    assert all("source" not in r for r in records)


def test_plebiscites_have_legal_basis(records):
    """Los plebiscitos nacionales 2020 y 2022 deben traer fundamento legal."""
    pl = [r for r in records if r["date"] in ("2020-10-25", "2022-09-04")
          and "Plebiscito nacional" in r["name"]["es"]]
    for r in pl:
        assert r["legal_basis"], f"sin legal_basis: {r['id']}"
        assert r["is_irrenunciable"] is True
        assert r["irrenunciability_category"] == 2
