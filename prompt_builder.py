"""Prompt construction for TTB label compliance audits."""

import json
from typing import Any


def build_audit_prompt(
    guideline: dict[str, Any],
    *,
    section_key: str,
    selected_subclass: str,
    selected_net_contents: str,
    app_id: str,
    brand_name: str,
    alcohol_content: str,
    company_name: str,
    location_address: str,
    contains_sulfites: bool,
) -> str:
    """Build the structured audit prompt from UI selections and metadata."""
    if section_key == "4.2":
        if contains_sulfites:
            sulfite_instruction = (
                "- MANDATORY: Verify that 'Contains Sulfites' (or equivalent "
                "statutory wording) is clearly printed on the label."
            )
            sulfite_status = "Contains 10+ ppm Sulfites"
        else:
            sulfite_instruction = (
                "- NOTE: Applicant declared low/no sulfites (<10 ppm). Do NOT "
                "flag missing 'Contains Sulfites' text as a violation."
            )
            sulfite_status = "Exempt / Low Sulfites (<10 ppm)"
    else:
        sulfite_instruction = ""
        sulfite_status = "N/A"

    return f"""
You are an expert TTB label compliance auditor testing compliance against {guideline['cfr_part']}.

PAYLOAD MANIFEST METADATA:
- Primary Category: {guideline['section_name']} ({guideline['cfr_part']})
- Declared Subclass: {selected_subclass}
- Declared Net Contents: {selected_net_contents}
- Application ID: {app_id}
- Brand Name: {brand_name}
- Alcohol Content: {alcohol_content}
- Company / Manufacturer Name: {company_name}
- Producer / Bottler Location: {location_address}
- Declared Sulfite Status: {sulfite_status}

REGULATORY MANDATES:
- Mandatory Checks Required for Category: {json.dumps(guideline['mandatory_checks'])}
- Permitted Standard Container Sizes: {json.dumps(guideline['net_content_allowed_values'])}

AUDIT INSTRUCTIONS:
1. Verify whether the declared Subclass ({selected_subclass}) accurately matches the product description printed on the front or back label images.
2. Verify that the Net Contents ({selected_net_contents}) matches the printed label text and complies with statutory volume standards.
3. Verify that the Company/Manufacturer Name ({company_name}) and Producer/Bottler Location ({location_address}) match the mandatory name and address statement printed on the label.
4. Check that mandatory elements under {guideline['cfr_part']} (e.g. Government Warning statement, alcohol percentage, manufacturer name, location) are explicitly visible on the label images.
{sulfite_instruction}
5. Detail any discrepancies, missing mandatory regulatory elements, or formatting non-conformities clearly.
""".strip()
