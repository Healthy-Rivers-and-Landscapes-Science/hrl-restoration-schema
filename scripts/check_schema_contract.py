#!/usr/bin/env python3
"""Check invariants for the restoration submission, canonical, and public contracts."""

from __future__ import annotations

import argparse
import os
from pathlib import Path


os.environ.setdefault("PYSTOW_HOME", str(Path.cwd() / ".cache" / "pystow"))

from linkml_runtime.utils.schemaview import SchemaView


def induced_slots(view: SchemaView, class_name: str) -> dict[str, object]:
    return {slot.name: slot for slot in view.class_induced_slots(class_name)}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--schema", default="schemas/hrl_restoration_project.yaml")
    args = parser.parse_args()

    view = SchemaView(args.schema)
    submission = induced_slots(view, "RestorationProjectSubmission")
    canonical = induced_slots(view, "RestorationProjectCanonicalRecord")
    public = induced_slots(view, "RestorationProjectPublicRecord")

    required_submission = {
        "project_id",
        "project_name",
        "project_stage",
        "lead_entity",
        "early_implementation",
        "system",
        "project_type",
        "geometry",
    }
    for slot_name in required_submission:
        require(slot_name in submission and submission[slot_name].required, f"{slot_name} must be required for submissions")

    for slot_name in {
        "contact_name",
        "contact_email",
        "construction_start_year",
        "construction_completion_year",
        "estimated_budget",
        "funding_secured",
        "funding_gap",
        "target_species",
        "project_description",
    }:
        require(slot_name in submission and not submission[slot_name].required, f"{slot_name} must be conditionally required by the pipeline")

    project_id = submission["project_id"]
    require(project_id.range == "string" and project_id.identifier, "project_id must be a string identifier")
    lead_entity = submission["lead_entity"]
    require(lead_entity.multivalued, "lead_entity must permit multiple entities")
    require(lead_entity.range == "string", "submissions must accept cataloged lead-entity names and aliases")
    require(
        str(lead_entity.annotations["submission_serialization"].value) == "semicolon_delimited",
        "lead_entity must use semicolon-delimited submission serialization",
    )
    require(canonical["lead_entity"].range == "LeadEntityEnum", "canonical records must use stable lead-entity IDs")
    require(public["lead_entity"].range == "LeadEntityEnum", "public records must use stable lead-entity IDs")
    lead_entity_enum = view.get_enum("LeadEntityEnum")
    required_lead_entity_ids = {
        "dwr",
        "ebmud",
        "water_forum",
        "sfpuc",
        "yuba_water_agency",
        "solano_county_water_agency",
        "sutter_butte_flood_control_agency",
        "river_partners",
        "modesto_irrigation_district",
        "turlock_irrigation_district",
        "south_yuba_river_citizens_league",
    }
    require(
        required_lead_entity_ids <= set(lead_entity_enum.permissible_values),
        "LeadEntityEnum must contain the current program lead-entity catalog",
    )
    for entity_id in required_lead_entity_ids:
        entity = lead_entity_enum.permissible_values[entity_id]
        require(entity.annotations and "full_name" in entity.annotations, f"{entity_id} needs catalog full_name metadata")

    internal_canonical_only = {
        "source_project_id",
        "source_organization_code",
        "last_submission_id",
        "source_data_as_of",
        "update_date",
    }
    for slot_name in internal_canonical_only:
        require(slot_name in canonical, f"{slot_name} must be canonical")
        require(slot_name not in submission and slot_name not in public, f"{slot_name} must not be submitted or public")
    for slot_name in internal_canonical_only - {"source_project_id"}:
        require(canonical[slot_name].required, f"{slot_name} must be required for canonical records")

    require("funding_gap" in canonical and canonical["funding_gap"].required, "funding_gap must be required for canonical records")
    require(submission["funding_gap"].range == "integer", "submitted funding_gap must retain its integer range")
    require("funding_gap" not in public, "funding_gap must not be public")
    require("record_status" in canonical and canonical["record_status"].required, "record_status must be required for canonical records")

    expected_public = {
        "project_id", "project_name", "project_description", "project_stage", "lead_entity",
        "early_implementation", "construction_start_year", "construction_completion_year",
        "estimated_budget", "funding_sources", "system", "project_type", "acreage",
        "acreage_bypass_floodplain", "acreage_fish_food", "acreage_tributary_floodplain",
        "acreage_tributary_rearing", "acreage_tributary_spawning", "acreage_tidal_wetland",
        "target_species", "geometry",
    }
    require(set(public) == expected_public, "public record slots must match the approved public contract")
    require("record_status" not in public, "public records contain active projects only and must not expose lifecycle status")
    require(public["project_description"].required, "project_description must be required for public records")


if __name__ == "__main__":
    main()
