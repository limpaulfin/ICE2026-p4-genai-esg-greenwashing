# RAG Pipeline Design for ESG Evidence Retrieval

## Overview
A five-component Retrieval-Augmented Generation pipeline for evidence-based greenwashing claim verification. This pipeline serves as the AI tool used by the treatment group in the within-subjects quasi-experiment (N=35 ESG reports).

## Architecture Components

### Component 1: Document Indexer
- **Input**: Raw ESG sustainability reports (PDF/HTML)
- **Processing**:
  1. Structure extraction: Parse sections (environmental, social, governance)
  2. Table/figure extraction: Isolate quantitative claims from narrative
  3. Semantic chunking: Split by ESG topic boundaries (not fixed-size)
  4. Chunk size: 1000-1500 tokens with 200-token overlap
- **Output**: Indexed chunks in vector store + metadata (company, year, section, page)
- **Rationale**: Semantic chunking preserves ESG domain boundaries (e.g., Scope 1 vs Scope 2 emissions) better than fixed-size chunking [Polzer, 2025]

### Component 2: Claim Extractor
- **Input**: Indexed ESG report chunks
- **Processing**:
  1. Identify verifiable claims (quantitative targets, comparative statements, certifications)
  2. Classify claim type: emission reduction, renewable target, diversity metric, supply chain
  3. Extract claim metadata: baseline year, target year, metric, scope
- **Output**: Structured claim objects {claim_text, claim_type, metrics, source_chunk_id}
- **Prompt template**:
  ```
  Given the following ESG report excerpt, extract all verifiable claims.
  For each claim, identify: (1) the specific metric or target,
  (2) the baseline and target values, (3) the time frame,
  (4) whether third-party verification is referenced.
  Format: JSON array of claim objects.
  ```

### Component 3: Evidence Retriever
- **Input**: Extracted claims
- **Processing**:
  1. Query formulation: Transform claim into evidence search queries
  2. Hybrid retrieval: Dense (embedding similarity) + Sparse (BM25 keyword match)
  3. Source priority: (a) Regulatory databases (SEC, EU CSRD), (b) Prior enforcement actions, (c) Industry benchmarks (SBTi, CDP), (d) Cross-company comparisons
  4. Re-ranking: Cross-encoder re-ranking for utility-aware retrieval
- **Output**: Top-k evidence passages with relevance scores
- **Embedding approach**: General-purpose model (text-embedding-3-small or equivalent) with domain adaptation via fine-tuning on ESG terminology
- **Rationale**: Hybrid retrieval outperforms single-method approaches; utility-aware retrieval prioritizes verification-relevant evidence over mere semantic similarity [Deng, 2025]

### Component 4: Verification Generator
- **Input**: Claim + retrieved evidence passages
- **Processing**:
  1. Evidence alignment: Map evidence to specific claim components
  2. Consistency check: Compare claimed metrics against evidence
  3. Generate structured verification assessment
  4. Apply extended TerraChoice taxonomy for greenwashing classification
- **Output**: Verification result {verdict, evidence_summary, greenwashing_indicators, confidence}
- **Prompt template**:
  ```
  You are an ESG auditor. Given the CLAIM and EVIDENCE below,
  assess whether the claim is substantiated, unsubstantiated,
  or misleading.

  CLAIM: {claim_text}
  EVIDENCE: {evidence_passages}

  Evaluate against these greenwashing indicators:
  1. Vague/unverifiable language
  2. Selective disclosure (favorable metrics only)
  3. Misleading baselines or cherry-picked reference years
  4. Aspirational targets without implementation plans
  5. Hidden trade-offs (Scope 1 reduction offset by Scope 3 increase)
  6. No proof / missing third-party verification
  7. Irrelevance (certified for non-material issues)

  Output JSON: {verdict, indicators_found[], evidence_support_level,
  reasoning, confidence_score}
  ```

### Component 5: Confidence Scorer
- **Input**: Verification results from Component 4
- **Processing**:
  1. Evidence strength: Number and quality of supporting/contradicting evidence
  2. Retrieval confidence: Average relevance score of retrieved passages
  3. Claim complexity: Simple metric vs multi-factor assessment
  4. Composite score: Weighted aggregation
- **Output**: Confidence score [0, 1] with interpretive label
- **Scoring formula**:
  - Evidence strength (40%): f(supporting_count, contradicting_count, source_authority)
  - Retrieval quality (30%): mean(top-k relevance scores)
  - Claim specificity (20%): binary features (has_number, has_timeframe, has_verification)
  - Model consistency (10%): agreement across multiple generation passes

## Evaluation Metrics
1. **Retrieval accuracy**: Precision@k and Recall@k for evidence retrieval
2. **Answer faithfulness**: Proportion of generated assessments supported by retrieved evidence (no hallucination)
3. **Claim verification F1**: Against ground-truth greenwashing labels
4. **End-to-end detection accuracy**: Overall pipeline performance vs manual baseline

## Hallucination Mitigation
- Grounded generation: LLM must cite specific evidence passages
- Abstain mechanism: If retrieval confidence < 0.3, output "insufficient evidence"
- Multi-pass verification: Run verification twice, flag disagreements for human review
- Source attribution: Every claim in the output links back to a specific evidence chunk

## Integration with Experiment
- Treatment group auditors interact with Components 2-5 via a structured interface
- Auditors receive: claim list, evidence summaries, verification assessments, confidence scores
- Auditors make final greenwashing determination (AI-assisted, not AI-automated)
- Control group receives same reports without AI pipeline access
