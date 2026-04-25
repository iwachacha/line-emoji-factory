from __future__ import annotations

import json

from jsonschema import Draft202012Validator

from conftest import ROOT


def load_schema() -> dict:
    return json.loads((ROOT / "schemas" / "post-release-metrics.schema.json").read_text(encoding="utf-8"))


def valid_metrics() -> dict:
    return {
        "schema_version": "1.0",
        "release": {
            "brand": "Test Brand",
            "release_id": "release-001",
            "public_date": "2026-04-26",
            "review_result": "approved",
        },
        "metrics": {
            "views": 100,
            "clicks": 25,
            "purchases": 3,
            "conversion_notes": "Small sample.",
            "refund_complaint_notes": "",
            "premium_eligibility_date": None,
        },
        "interpretation": {
            "sold_because": "Clear use case.",
            "did_not_sell_because": "",
            "review_friction": "",
            "usage_drift": "",
        },
    }


def test_post_release_metrics_schema_accepts_expected_shape():
    schema = load_schema()
    Draft202012Validator.check_schema(schema)
    errors = list(Draft202012Validator(schema).iter_errors(valid_metrics()))
    assert errors == []


def test_post_release_metrics_schema_rejects_negative_metrics_and_bad_release_id():
    schema = load_schema()
    data = valid_metrics()
    data["release"]["release_id"] = "001"
    data["metrics"]["views"] = -1

    messages = [error.message for error in Draft202012Validator(schema).iter_errors(data)]
    assert any("does not match" in message for message in messages)
    assert any("less than the minimum" in message for message in messages)
