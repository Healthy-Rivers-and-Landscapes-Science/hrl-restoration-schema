#!/usr/bin/env python3
"""Generate a human-readable data dictionary from the LinkML schema."""

from __future__ import annotations

import argparse
import html
import os
import warnings
from pathlib import Path
from typing import Iterable


os.environ.setdefault("PYSTOW_HOME", str(Path.cwd() / ".cache" / "pystow"))
warnings.filterwarnings(
    "ignore",
    message=r".*urllib3 .*charset_normalizer.*doesn't match a supported version.*",
)

from linkml_runtime.linkml_model.meta import EnumDefinition, SlotDefinition
from linkml_runtime.utils.schemaview import SchemaView


SUBMISSION_CLASS = "RestorationProjectSubmission"
CANONICAL_CLASS = "RestorationProjectCanonicalRecord"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate docs/data_dictionary.md from a LinkML schema."
    )
    parser.add_argument(
        "--schema",
        default="schemas/hrl_restoration_project.yaml",
        help="Path to the LinkML schema.",
    )
    parser.add_argument(
        "--output",
        default="docs/data_dictionary.md",
        help="Path where the generated Markdown page should be written.",
    )
    args = parser.parse_args()

    schema_path = Path(args.schema)
    output_path = Path(args.output)

    view = SchemaView(str(schema_path))
    markdown = render_data_dictionary(view, schema_path)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(markdown, encoding="utf-8")


def render_data_dictionary(view: SchemaView, schema_path: Path) -> str:
    submission_slots = view.class_induced_slots(SUBMISSION_CLASS)
    canonical_slots = view.class_induced_slots(CANONICAL_CLASS)

    submission_by_name = {slot.name: slot for slot in submission_slots}
    canonical_changes = [
        slot
        for slot in canonical_slots
        if slot.name not in submission_by_name
        or bool(slot.required) != bool(submission_by_name[slot.name].required)
    ]

    lines = [
        "---",
        "hide:",
        "  - toc",
        "---",
        "",
        "# Data Dictionary",
        "",
        "<!-- This page is generated from the LinkML schema. Do not edit it directly. -->",
        "",
        "This page translates the source schema into a field-by-field reference for data submitters.",
        f"It is generated from `{schema_path.as_posix()}` so the schema remains the single source of truth.",
        "",
        "## Submitted Project Fields",
        "",
        render_slot_table(view, submission_slots),
        "",
        render_additional_guidance(submission_slots),
        "",
        "## Canonical Record Differences",
        "",
        "These fields or requirements apply after validation and ingestion into the standardized canonical record.",
        "",
        render_slot_table(view, canonical_changes),
        "",
        render_additional_guidance(canonical_changes),
        "",
        "## Controlled Vocabularies",
        "",
        render_vocabularies(view),
        "",
    ]
    return "\n".join(lines)


def render_slot_table(view: SchemaView, slots: Iterable[SlotDefinition]) -> str:
    rows = [
        '<div class="data-dictionary-table-wrapper">',
        '<table class="data-dictionary-table">',
        "<colgroup>",
        '<col class="data-dictionary-table__field">',
        '<col class="data-dictionary-table__required">',
        '<col class="data-dictionary-table__meaning">',
        '<col class="data-dictionary-table__expected">',
        '<col class="data-dictionary-table__multiple">',
        '<col class="data-dictionary-table__guidance">',
        "</colgroup>",
        "<thead>",
        "<tr>",
        "<th>Field</th>",
        "<th>Required?</th>",
        "<th>What it means</th>",
        "<th>Expected value</th>",
        "<th>Multiple values?</th>",
        "<th>Guidance</th>",
        "</tr>",
        "</thead>",
        "<tbody>",
    ]
    for slot in slots:
        rows.extend(
            [
                "<tr>",
                f"<td>{field_name(slot)}</td>",
                f"<td>{'Yes' if slot.required else 'No'}</td>",
                f"<td>{html_cell(slot.description or '')}</td>",
                f"<td>{expected_value(view, slot)}</td>",
                f"<td>{multiple_values(slot)}</td>",
                f"<td>{guidance(slot)}</td>",
                "</tr>",
            ]
        )
    rows.extend(["</tbody>", "</table>", "</div>"])
    return "\n".join(rows)


def field_name(slot: SlotDefinition) -> str:
    title = slot.title or slot.name
    if title == slot.name:
        return code(slot.name)
    return html_cell(f"{title}<br>{code(slot.name)}")


def expected_value(view: SchemaView, slot: SlotDefinition) -> str:
    enum = view.get_enum(slot.range) if slot.range else None
    if enum:
        values = list(enum.permissible_values.keys())
        if len(values) <= 10:
            return html_cell("<br>".join(code(value) for value in values))
        return f'Controlled vocabulary: <a href="#{anchor(slot.range)}">{html.escape(slot.range, quote=False)}</a>'

    type_labels = {
        "boolean": "Yes/no",
        "date": "Date",
        "decimal": "Number",
        "integer": "Whole number",
        "string": "Text",
    }
    return html_cell(type_labels.get(slot.range or "", slot.range or "Text"))


def multiple_values(slot: SlotDefinition) -> str:
    if not slot.multivalued:
        return "No"
    serialization = annotation_value(slot, "submission_serialization")
    if serialization == "semicolon_delimited":
        return html_cell("Yes<br>Semicolon-delimited")
    return "Yes"


def rule_parts(slot: SlotDefinition) -> list[str]:
    parts: list[str] = []

    # max_length is omitted here — slot.comments always describes it in prose already

    minimum = getattr(slot, "minimum_value", None)
    maximum = getattr(slot, "maximum_value", None)
    if minimum is not None and maximum is not None:
        parts.append(f"Between {minimum} and {maximum}")
    elif minimum is not None:
        parts.append(f"Minimum: {minimum}")
    elif maximum is not None:
        parts.append(f"Maximum: {maximum}")

    if slot.pattern:
        parts.append(f"Must match pattern {code(slot.pattern)}")

    allowable_geometry = annotation_value(slot, "allowable_geometry_types")
    if allowable_geometry:
        parts.append(f"Allowable geometry types: {allowable_geometry.replace('; ', ';').replace(';', ', ')}")

    standardized_crs = annotation_value(slot, "standardized_crs_epsg")
    if standardized_crs:
        parts.append(f"Standardized CRS: EPSG:{standardized_crs}")

    input_crs_required = annotation_value(slot, "input_crs_required")
    if input_crs_required == "true":
        parts.append("Submitted spatial data must include a CRS")

    return parts


def guidance(slot: SlotDefinition) -> str:
    parts = rule_parts(slot)
    if has_long_guidance(slot):
        parts.append(f'See <a href="#{field_guidance_anchor(slot)}">detailed guidance</a>.')
    else:
        parts.extend(slot.comments or [])
    return html_list(parts)


def render_additional_guidance(slots: Iterable[SlotDefinition]) -> str:
    detailed_slots = [slot for slot in slots if has_long_guidance(slot)]
    if not detailed_slots:
        return ""

    lines = ["### Additional Field Guidance", ""]
    for slot in detailed_slots:
        lines.extend(
            [
                f'#### <span id="{field_guidance_anchor(slot)}"></span>{slot.title or slot.name} ({code(slot.name)})',
                "",
            ]
        )
        for comment in slot.comments or []:
            lines.append(f"- {html.escape(comment, quote=False)}")
        lines.append("")
    return "\n".join(lines).rstrip()


def has_long_guidance(slot: SlotDefinition) -> bool:
    comments = slot.comments or []
    return len(comments) > 3 or sum(len(comment) for comment in comments) > 280


def render_vocabularies(view: SchemaView) -> str:
    sections: list[str] = []
    for enum_name in view.all_enums().keys():
        enum = view.get_enum(enum_name)
        sections.append(render_enum(enum_name, enum))
    return "\n\n".join(sections)


def render_enum(enum_name: str, enum: EnumDefinition) -> str:
    lines = [f"### {enum_name}", ""]
    if enum.description:
        lines.extend([enum.description, ""])

    grouped: dict[str, list[str]] = {}
    ungrouped: list[str] = []
    for value_name, value in enum.permissible_values.items():
        group = annotation_value(value, "group")
        if group:
            grouped.setdefault(group, []).append(value_name)
        else:
            ungrouped.append(value_name)

    if grouped:
        for group_name, values in grouped.items():
            lines.extend([f"#### {group_name}", ""])
            lines.extend(f"- {value}" for value in values)
            lines.append("")
    else:
        lines.extend(f"- {value}" for value in ungrouped)

    return "\n".join(lines).rstrip()


def annotation_value(element: object, name: str) -> str | None:
    annotations = getattr(element, "annotations", None)
    if not annotations:
        return None
    if isinstance(annotations, dict):
        annotation = annotations.get(name)
    else:
        annotation = getattr(annotations, name, None)
    if annotation is None:
        return None
    return str(getattr(annotation, "value", annotation))


def html_cell(value: str) -> str:
    escaped = html.escape(str(value), quote=False)
    return (
        escaped.replace("&lt;br&gt;", "<br>")
        .replace("&lt;code&gt;", "<code>")
        .replace("&lt;/code&gt;", "</code>")
        .replace("&lt;a ", "<a ")
        .replace("&lt;/a&gt;", "</a>")
        .replace("&gt;", ">")
        .replace("\n", " ")
        .replace("|", "\\|")
    )


def code(value: str) -> str:
    escaped = html.escape(str(value), quote=False).replace("|", "\\|")
    return f"<code>{escaped}</code>"


def anchor(value: str) -> str:
    return value.lower().replace(" ", "-")


def field_guidance_anchor(slot: SlotDefinition) -> str:
    return f"{anchor(slot.name)}-guidance"


def html_list(items: list[str]) -> str:
    if not items:
        return ""
    parts = []
    for item in items:
        rendered = html_cell(item)
        if rendered and rendered[-1] not in ".!?":
            rendered += "."
        parts.append(rendered)
    return " ".join(parts)


if __name__ == "__main__":
    main()
