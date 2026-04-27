"""RCIFENI-O prompt builders for RAG and baseline conditions."""

ROLE = (
    "Expert ESG auditor and greenwashing detection specialist. "
    "10+ years experience with TerraChoice Seven Sins framework, "
    "CSRD, ISAE 3000, IFRS S1/S2 standards."
)

NOTICES = (
    "Respond ONLY valid JSON. No markdown. No explanation outside JSON. "
    "confidence must be float 0.0-1.0. label must be exactly one of: "
    "confirmed_greenwashing, suspected_greenwashing, clean. "
    "scores must be integers 0-5."
)

FORMAT = (
    '{"label": "confirmed_greenwashing|suspected_greenwashing|clean", '
    '"confidence": 0.0-1.0, "reasoning": "brief 1-2 sentence explanation", '
    '"scores": {"vagueness": 0-5, "selectivity": 0-5, '
    '"misleading": 0-5, "irrelevance": 0-5, "overall_risk": 0-5}}'
)

OKR = (
    "O: Accurately classify ESG claim as greenwashing or clean. "
    "KR1: Label matches enforcement evidence when available. "
    "KR2: Confidence reflects actual certainty. "
    "KR3: Scores reflect specific greenwashing dimensions."
)

EXAMPLE = (
    '{"label": "confirmed_greenwashing", "confidence": 0.92, '
    '"reasoning": "Claim contradicts ASA ruling banning the advertisement.", '
    '"scores": {"vagueness": 4, "selectivity": 3, '
    '"misleading": 5, "irrelevance": 1, "overall_risk": 5}}'
)


def build_rag_params(report, evidence_cases):
    """Build RCIFENI-O params for RAG condition (with evidence)."""
    evidence_text = ""
    for i, (sim, doc) in enumerate(evidence_cases, 1):
        verdict = "GREENWASH" if doc["type"] == "greenwash" else "LEGITIMATE"
        evidence_text += (
            f"Case {i} (sim={sim:.2f}, verdict={verdict}): "
            f"{doc['company']} - {doc['claim'][:150]}"
        )
        if doc["accusation"]:
            evidence_text += f" | Accusation: {doc['accusation'][:150]}"
        evidence_text += "\n"

    context = (
        f"RAG-augmented greenwashing detection experiment. "
        f"Evidence retrieved from GreenClaims enforcement database. "
        f"Similar cases provided below for cross-reference."
    )
    instructions = (
        f"1. Read the retrieved evidence cases carefully. "
        f"2. Evaluate the target claim against evidence patterns. "
        f"3. Apply TerraChoice Seven Sins framework. "
        f"4. Classify and score the claim. "
        f"5. Cite specific evidence in reasoning."
    )
    inp = (
        f"RETRIEVED EVIDENCE:\n{evidence_text}\n"
        f"TARGET CLAIM:\n"
        f"Company: {report['company']} | Sector: {report.get('sector', 'Unknown')} | "
        f"Country: {report.get('country', 'Unknown')} | Year: {report.get('year', '2023')}\n"
        f"Claim: {report.get('excerpt_summary', '')}\n"
        f"Enforcement: {report.get('enforcement', 'None')}"
    )
    return ROLE, context, instructions, FORMAT, inp, OKR, NOTICES, EXAMPLE


def build_baseline_params(report):
    """Build RCIFENI-O params for baseline condition (no evidence)."""
    context = (
        f"Greenwashing detection using general ESG knowledge only. "
        f"No external evidence database. Evaluate claim on its own merits."
    )
    instructions = (
        f"1. Read the ESG claim carefully. "
        f"2. Apply TerraChoice Seven Sins framework from general knowledge. "
        f"3. Classify based solely on claim text and general ESG knowledge. "
        f"4. Score each greenwashing dimension."
    )
    inp = (
        f"Company: {report['company']} | Sector: {report.get('sector', 'Unknown')} | "
        f"Country: {report.get('country', 'Unknown')} | Year: {report.get('year', '2023')}\n"
        f"Claim: {report.get('excerpt_summary', '')}"
    )
    return ROLE, context, instructions, FORMAT, inp, OKR, NOTICES, EXAMPLE
