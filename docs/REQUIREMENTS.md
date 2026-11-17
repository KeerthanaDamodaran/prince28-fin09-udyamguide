# Requirements: UdyamGuide

## Functional (what it does)

1. A user can ask a question in plain English and get an answer drawn from my verified sources.
2. Every answer cites the document and page number (or section) it came from.
3. If the documents do not contain the answer, the product says **"I don't know"** instead of guessing.
4. **Signature feature – Delayed Payment Calculator:** A user can enter the invoice date, invoice amount, acceptance date, agreed payment terms and payment date to calculate the applicable interest, with the relevant MSMED Act section cited.
5. A user can browse and search the underlying records through `GET /v1/documents`.

## Non-functional (how well, with numbers)

| # | Quality | Target | How I will measure it |
|---|---|---|---|
| 1 | Speed: record lookups | p95 under **500 ms** for `GET /v1/documents` | Load test (Week 6) |
| 2 | Speed: answers | p95 under **8 s** for a full answer; first token under **2 s** | Traces (Week 5) |
| 3 | Accuracy | Interest computed exactly for 20 test invoices; scheme eligibility correct for **90%+** of 30 profiles | Golden question set (Weeks 4 and 5) |
| 4 | Cost | Under **Rs 1.00** per answered question | `llm_calls` table (Week 2) |
| 5 | Availability | **95%** monthly uptime of the live URL | Uptime monitor from Day 5 |
