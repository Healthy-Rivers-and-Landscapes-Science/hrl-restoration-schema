#!/usr/bin/env python3
"""Validate the repository's LinkML attribute-contract fixtures."""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path


FIXTURES: dict[str, tuple[str, bool]] = {
    "examples/valid/restoration_project_submission_minimal.yaml": (
        "RestorationProjectSubmission",
        True,
    ),
    "examples/valid/restoration_project_submission_without_target_species.yaml": (
        "RestorationProjectSubmission",
        True,
    ),
    "examples/valid/restoration_project_submission_without_description.yaml": (
        "RestorationProjectSubmission",
        True,
    ),
    "examples/valid/restoration_project_canonical_representative.yaml": (
        "RestorationProjectCanonicalRecord",
        True,
    ),
    "examples/valid/restoration_project_canonical_without_description.yaml": (
        "RestorationProjectCanonicalRecord",
        True,
    ),
    "examples/valid/restoration_project_public_representative.yaml": (
        "RestorationProjectPublicRecord",
        True,
    ),
    "examples/valid/restoration_project_public_without_target_species.yaml": (
        "RestorationProjectPublicRecord",
        True,
    ),
    "examples/invalid/restoration_project_submission_missing_project_id.yaml": (
        "RestorationProjectSubmission",
        False,
    ),
    "examples/invalid/restoration_project_submission_invalid_controlled_value.yaml": (
        "RestorationProjectSubmission",
        False,
    ),
    "examples/invalid/restoration_project_submission_malformed_contact_email.yaml": (
        "RestorationProjectSubmission",
        False,
    ),
    "examples/invalid/restoration_project_submission_missing_required_project_name.yaml": (
        "RestorationProjectSubmission",
        False,
    ),
    "examples/invalid/restoration_project_public_missing_project_description.yaml": (
        "RestorationProjectPublicRecord",
        False,
    ),
    "examples/invalid/restoration_project_submission_construction_start_year_below_minimum.yaml": (
        "RestorationProjectSubmission",
        False,
    ),
    "examples/invalid/restoration_project_submission_non_numeric_funding_gap.yaml": (
        "RestorationProjectSubmission",
        False,
    ),
    "examples/invalid/restoration_project_public_private_contact_email.yaml": (
        "RestorationProjectPublicRecord",
        False,
    ),
    "examples/invalid/restoration_project_public_funding_gap.yaml": (
        "RestorationProjectPublicRecord",
        False,
    ),
    "examples/invalid/restoration_project_public_record_status.yaml": (
        "RestorationProjectPublicRecord",
        False,
    ),
}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--schema", default="schemas/hrl_restoration_project.yaml")
    args = parser.parse_args()

    environment = os.environ.copy()
    environment.setdefault("PYSTOW_HOME", str(Path.cwd() / ".cache" / "pystow"))
    failures: list[str] = []

    for fixture, (target_class, should_pass) in FIXTURES.items():
        command = [
            "linkml-validate",
            "--schema",
            args.schema,
            "--target-class",
            target_class,
            fixture,
        ]
        result = subprocess.run(command, env=environment, capture_output=True, text=True)
        passed = result.returncode == 0
        expected = "pass" if should_pass else "fail"
        actual = "pass" if passed else "fail"
        print(f"{fixture}: expected {expected}, got {actual}")
        if passed != should_pass:
            failures.append(fixture)
            if result.stdout:
                print(result.stdout, file=sys.stderr, end="")
            if result.stderr:
                print(result.stderr, file=sys.stderr, end="")

    if failures:
        raise SystemExit(f"Fixture expectations were not met: {', '.join(failures)}")


if __name__ == "__main__":
    main()
