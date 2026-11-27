# Capacity plan: UdyamGuide

Full corpus target: + CGTMSE circulars, Tamil Nadu schemes and FAQs (2,500+ pages)

<!-- generated:start -->
## Measured on my start corpus (2026-11-27 09:03 UTC)

| What | Value |
|---|---|
| Files | 17 |
| Size on disk | 21.7 MB |
| Pages (PDF pages + 1 per 3,000 characters of text/HTML) | 271 |
| Characters of text | 485,617 |
| Estimated tokens (characters / 4) | 121,404 |
| Tokens per page | 449 |
| PDFs with almost no text (scanned? OCR is Day 7) | 1 |
| Files not measured (zip, xlsx, unreadable) | 0 |

## Estimate for the full corpus (target: 2,500 pages)

| What | How | Value |
|---|---|---|
| Scale factor | target / measured | x 9.2 |
| Tokens | measured tokens x scale | 1.12 M |
| Raw files | measured MB x scale | 201 MB |
| Chunks | tokens / 400 x 1.15 overlap | 3,224 |
| Embedding cost, one time | tokens x 1.15 x $0.15 per 1M | $0.19 = Rs 18 |
| Vector storage | chunks x 768 numbers x 4 bytes | 10 MB |
| Text in Postgres | characters x scale x 1.2 | 5 MB |

Assumptions: 4 characters per token, 400-token chunks, 768-dimension embeddings at $0.15 per 1M tokens, Rs 95 per US dollar.
<!-- generated:end -->

## What I conclude

1. Is embedding cost a problem for this product? (1 line, with the number)

Not a major concern for the planned corpus. The generated estimate uses the configurable rate of $0.15 per 1 million tokens; actual cost depends on the embedding provider and model selected.

2. Do the vectors and text fit in my free Postgres? (1 line: compare with the storage limit on my database dashboard)

Neon Free provides 1 GB per project; I can't see your dashboard's actual usage, so I can't confirm how much your vectors + text currently occupy

3. Which number above am I least sure about, and how will I measure it better? (1 line)

Actual vector storage — I'll measure it after embedding by checking the row count and database storage used by the vectors and text.

4. What changes if the corpus grows 10 times? (2 lines)

Embedding costs and storage grow roughly 10× if chunk sizes and embedding dimensions stay the same. I'll optimize chunking, remove duplicate documents, and monitor Neon storage before scaling.
