# Greenwashing Detection Scoring Rubric

## Purpose
Standardized rubric for both AI-assisted and manual auditor experiment conditions.
Evaluators assess each ESG report excerpt across five dimensions on a 0-5 Likert scale.

## Scoring Dimensions

### 1. Vagueness (0-5)
| Score | Criteria |
|-------|----------|
| 0 | All claims specific, quantified, with clear baselines |
| 1 | Minor ambiguity in 1 claim; mostly precise language |
| 2 | Some vague terms ("eco-friendly", "sustainable") but majority claims quantified |
| 3 | Multiple vague claims; mix of quantified and unsubstantiated statements |
| 4 | Predominantly vague language; few specific commitments |
| 5 | Pervasive vagueness; no quantified targets or baselines |

### 2. Selectivity (0-5)
| Score | Criteria |
|-------|----------|
| 0 | Comprehensive disclosure across all material ESG dimensions |
| 1 | Minor omission in one non-critical area |
| 2 | Some positive metrics emphasized; negative metrics present but less prominent |
| 3 | Clear emphasis on favorable metrics; notable gaps in unfavorable areas |
| 4 | Significant omission of negative ESG impacts; cherry-picked reporting |
| 5 | Only positive metrics reported; material negative impacts entirely hidden |

### 3. Misleading Claims (0-5)
| Score | Criteria |
|-------|----------|
| 0 | All claims accurate, verifiable, and contextually appropriate |
| 1 | One minor claim could be misinterpreted without context |
| 2 | Some claims technically true but presented without necessary caveats |
| 3 | Multiple claims misleading through decontextualization or incomparable baselines |
| 4 | Several demonstrably misleading claims; false labels or fake certifications |
| 5 | Outright false environmental claims (fibbing per TerraChoice taxonomy) |

### 4. Irrelevance (0-5)
| Score | Criteria |
|-------|----------|
| 0 | All ESG claims material and relevant to company's actual impact areas |
| 1 | One minor irrelevant claim among otherwise material disclosures |
| 2 | Some claims technically true but immaterial to core operations |
| 3 | Mix of relevant and irrelevant claims; distraction from key impacts |
| 4 | Majority of highlighted claims are irrelevant or trivially true |
| 5 | Claims entirely disconnected from material ESG risks (e.g., "CFC-free" after ban) |

### 5. Overall Greenwashing Risk (0-5)
| Score | Criteria |
|-------|----------|
| 0 | Clean: Transparent, third-party verified, comprehensive ESG disclosure |
| 1 | Minimal risk: Minor issues in one dimension only |
| 2 | Low risk: Some concerns but overall good-faith reporting evident |
| 3 | Moderate risk: Multiple greenwashing indicators; suspected greenwashing |
| 4 | High risk: Clear pattern of misleading ESG communication |
| 5 | Confirmed greenwashing: Regulatory action, legal settlement, or retracted claims |

## TerraChoice Sin Mapping
Each dimension maps to the TerraChoice Seven Sins framework:
- Vagueness -> Sin of Vagueness
- Selectivity -> Sin of Hidden Trade-Off + Selective Disclosure (ext)
- Misleading -> Sin of Fibbing + Sin of False Labels + Sin of No Proof
- Irrelevance -> Sin of Irrelevance + Sin of Lesser of Two Evils
- Overall -> Composite assessment across all sins

## Experiment Conditions

### Condition A: AI-Assisted Group
- Evaluators receive ESG report excerpts + AI-generated analysis
- AI provides: sin classification, confidence score, evidence highlights
- Evaluators score using this rubric with AI suggestions visible

### Condition B: Manual Auditor Group
- Evaluators receive ESG report excerpts only
- No AI assistance; standard auditing tools permitted
- Evaluators score using this rubric independently

### Inter-Rater Reliability
- Minimum 2 evaluators per document per condition
- Cohen's kappa computed for each dimension
- Target: kappa >= 0.6 (substantial agreement)

## Sources
- TerraChoice (2010). The Sins of Greenwashing: Home and Family Edition.
- CFA Institute (2023). Handbook of AI and Big Data Applications in Investments.
