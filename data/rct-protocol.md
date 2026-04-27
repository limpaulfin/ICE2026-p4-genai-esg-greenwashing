# RCT/Quasi-Experiment Protocol: AI vs Manual Greenwashing Detection

## Study Design
- **Type**: Within-subjects quasi-experiment (repeated measures)
- **Rationale**: Each ESG report (N=35) evaluated by BOTH AI-assisted and manual methods
- **H1**: AI-assisted auditors demonstrate higher greenwashing detection rates than manual methods

## Participants and Units
- **Unit of analysis**: ESG report (N=35)
- **Evaluators**: MBA students acting as auditors (minimum 10 per condition)
- **Treatment**: Auditors equipped with GenAI+RAG tool for greenwashing detection
- **Control**: Auditors using manual review protocols only (checklist-based)

## Randomization Protocol
- **Design**: Stratified crossover - reports randomized to evaluation ORDER (AI-first vs manual-first)
- **Stratification factors**:
  1. Greenwashing status: Confirmed (n=13) / Suspected (n=16) / Clean (n=6)
  2. Industry sector: Energy / Manufacturing / Financial / Other
  3. Report complexity: Short / Medium / Long (word count tertiles)
- **Block size**: 6 (stratified permuted blocks)
- **Washout**: 2-week interval between conditions to minimize carryover effects

## Blinding
- **Single-blind**: Auditors unaware of study hypothesis and ground truth labels
- **Outcome assessors**: Blinded to allocation during primary analysis
- **Unblinding**: After all data collection and primary analysis complete

## Outcome Variables
### Primary
- **Detection accuracy**: (TP + TN) / N
- **Precision**: TP / (TP + FP)
- **Recall (Sensitivity)**: TP / (TP + FN)
- **F1-score**: 2 * (Precision * Recall) / (Precision + Recall)

### Secondary
- **Time-to-audit**: Minutes per report
- **False positive rate**: FP / (FP + TN)
- **Inter-rater reliability**: Cohen's kappa between auditors within same condition

## Power Analysis
- **Test**: Paired t-test (within-subjects)
- **Effect size**: Cohen's d = 0.5 (medium)
- **Alpha**: 0.05 (two-sided)
- **Power**: 0.80
- **Minimum pairs needed**: ceil(31.40) = 32
- **Available pairs**: N = 35 reports
- **Achieved power**: Phi(0.998) = 0.841 > 0.80 (ADEQUATE)
- **Formula**: n >= (z_alpha/2 + z_beta)^2 / d^2 = (1.96 + 0.842)^2 / 0.25 = 31.40

## Bayesian Complement
- **Bayes Factor t-test**: BF_10 for paired comparison of AI vs manual detection rates
- **Prior**: Informative Cauchy prior (r = 0.707) based on existing AI audit literature
- **Beta-binomial model**: Posterior distribution for detection success rates
  - Prior: Beta(1, 1) (uninformative) for both conditions
  - Likelihood: Binomial(n_correct, n_total) per condition
  - Posterior: Beta(1 + successes, 1 + failures)
- **Decision criterion**: BF_10 > 3 = moderate evidence; BF_10 > 10 = strong evidence
- **Model comparison**: BIC for detection model selection

## Data Collection Procedures
1. **Pre-test**: Auditor training (2 hours) on greenwashing indicators and scoring rubric
2. **Phase 1**: First condition evaluation (randomized order)
3. **Washout**: 2-week interval
4. **Phase 2**: Crossover to second condition
5. **Post-test**: Debrief questionnaire on perceived difficulty and tool usability

## Ethical Considerations
- **Informed consent**: All participants sign consent forms
- **Data anonymization**: Reports de-identified before evaluation
- **Right to withdraw**: Participants may withdraw at any time without penalty
- **Data storage**: Encrypted storage, 5-year retention per institutional policy
- **IRB**: Protocol submitted for expedited review (minimal risk, educational context)

## CONSORT-AI Compliance
- Follows CONSORT-AI extension for AI intervention trials
- Pre-registered protocol with analysis plan
- Flow diagram documenting participant/report allocation
- AI system versioning and prompt documentation maintained
- Subgroup analyses pre-specified by greenwashing label type

## Timeline
| Week | Activity |
|------|----------|
| 1-2 | Auditor recruitment and training |
| 3 | Randomization and Phase 1 start |
| 4-5 | Phase 1 data collection |
| 6-7 | Washout period |
| 8-9 | Phase 2 (crossover) data collection |
| 10 | Data cleaning and analysis |
