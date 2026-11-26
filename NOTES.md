
# Engineering notes: UdyamGuide

## D03 · PostgreSQL

### Migrations (upgrade, downgrade, upgrade)

46650489b28b -> 637336e336ec (head), add gin index on metadata
<base> -> 46650489b28b, create documents and pages

### The loader is idempotent

run 1:
records=20 inserted=0 updated=0 unchanged=20
records=20 inserted=0 updated=0 unchanged=20

run 2:
records=20 inserted=0 updated=0 unchanged=20
records=20 inserted=0 updated=0 unchanged=20

run 3 (after editing one record):
records=20 inserted=0 updated=1 unchanged=19
records=20 inserted=0 updated=0 unchanged=20


### EXPLAIN for ?scheme=VALUE

1) What the planner chooses on its own:
Seq Scan on documents  (cost=0.00..11.00 rows=1 width=36) (actual time=1.087..1.087 rows=0.00 loops=1)
  Filter: (metadata @> '{"id": "003"}'::jsonb)
  Rows Removed by Filter: 21
  Buffers: shared read=2 dirtied=2
Planning:
  Buffers: shared hit=133 read=8 dirtied=1
Planning Time: 7.847 ms
Execution Time: 1.104 ms

-- 2) Seq scan switched off, to prove the index can be used:
Bitmap Heap Scan on documents  (cost=12.81..16.82 rows=1 width=36) (actual time=1.474..1.475 rows=0.00 loops=1)
  Recheck Cond: (metadata @> '{"id": "003"}'::jsonb)
  Buffers: shared hit=1 read=2
  ->  Bitmap Index Scan on ix_documents_metadata_gin  (cost=0.00..12.81 rows=1 width=0) (actual time=1.460..1.460 rows=0.00 loops=1)
        Index Cond: (metadata @> '{"id": "003"}'::jsonb)
        Index Searches: 1
        Buffers: shared hit=1 read=2
Planning:
  Buffers: shared hit=1
Planning Time: 0.073 ms
Execution Time: 1.517 ms


Why did the planner choose a Seq Scan on my table? (2 lines, your own words)

The planner chose a Sequential Scan because the table contains only around 20 rows, so reading the entire table is cheaper than using an index.

When would it switch to the GIN index? (1 line)

When the table grows large enough that using the GIN index is estimated to be cheaper than scanning the entire table.


## D04 · Docker, Compose and tests

### The image

The output of: docker images udyamguide:dev

IMAGE            ID             DISK USAGE   CONTENT SIZE   EXTRA
udyamguide:dev   c7de1319de16        300MB           70MB

The output of: docker run --rm udyamguide:dev id
uid=999(app) gid=999(app) groups=999(app)


- Size: 300 MB (target: under 400 MB)
- First build: 5.9 s. After changing one line of code: 12.6 s.
- Which step said CACHED, and why? The `uv sync` dependency-related step was cached in the first build because Docker reused a previously built layer, but it ran again in the second build because the source COPY step invalidated the cache.

### The stack

The output of: docker compose ps -a

NAME                   IMAGE                    COMMAND                  SERVICE   CREATED         STATUS                      PORTS
udyamguide-api-1       udyamguide-api           "sh -c 'exec uvicorn…"   api       9 minutes ago   Up 56 seconds (healthy)     8000/tcp
udyamguide-db-1        pgvector/pgvector:pg17   "docker-entrypoint.s…"   db        9 minutes ago   Up 9 minutes (healthy)      0.0.0.0:5433->5432/tcp, [::]:5433->5432/tcp
udyamguide-migrate-1   udyamguide-migrate       "sh -c 'alembic upgr…"   migrate   9 minutes ago   Exited (0) 56 seconds ago
udyamguide-redis-1     redis:7-alpine           "docker-entrypoint.s…"   redis     9 minutes ago   Up 9 minutes (healthy)      0.0.0.0:6379->6379/tcp, [::]:6379->6379/tcp

The last line of: docker compose logs migrate   (first up, then after down + up)

migrate-1  | records=20 inserted=0 updated=0 unchanged=20


### Breaking the database on purpose


db stopped:  /health
db stopped:  /ready
db started:  /ready

API stopped: /health → {"status":"ok","app":"udyamguide","env":"local"}

DB stopped: /ready → {"status":"not_ready","checks":{"database":false}}

DB started: /ready → {"status":"ready","checks":{"database":true}}

[+] stop 1/1
 ✔ Container udyamguide-db-1 Stopped                                                             0.5s
{"status":"ok","app":"udyamguide","env":"local"}{"status":"not_ready","checks":{"database":false}}
(udyamguide) PS D:\Genai-training\prince28-fin09-udyamguide> docker compose start db
>> curl.exe -s localhost:8000/ready
[+] start 1/1
 ✔ Container udyamguide-db-1 Started                                                             0.4s
{"status":"ready","checks":{"database":true}}


Why should a load balancer stop sending traffic here but not restart the app? (2 lines)

A load balancer should stop sending traffic to an unhealthy instance to prevent users from receiving errors.
It doesn't restart the app because its job is to route traffic; restarting and recovery are handled by the orchestrator (e.g., Docker/Kubernetes).

### Tests and coverage


uv run poe test              → 16 passed in 0.29s


uv run poe test-integration  → 7 passed in 2.66s


coverage TOTAL, unit only    → 16 passed, 7 skipped in 2.00s


coverage TOTAL, with integration tests → 23 passed in 4.05s


Two files or lines my coverage report says are never run, and whether they matter: (2 lines)

Coverage reports show which lines your tests never executed. Those lines may be untested code, not necessarily bugs.

They matter if they contain important logic (error handling, edge cases, validation); they may not matter much if they're startup code, logging, or rarely used branches.

# D05 · CI/CD and going live

- **Live URL:** https://udyamguide.onrender.com
- **CI run for PR #4:** https://github.com/KeerthanaDamodaran/prince28-fin09-udyamguide/actions
- **First automatic deploy:** 2:45 PM (approx.)
- **Merge clicked:** 2:45 PM → **Smoke test passed:** 2:47 PM → **Lead time:** ~2 min

## Smoke test output from that CD run

```text
waiting: … 200 <old sha>
waiting: … 200 <old sha>
waiting: … 200 <new sha>
Smoke test passed
```

## Rollback drill

- **Rolled back to SHA:** `ce83d7778803cab285e56e305da8cd4d6e64dfa2`
  - Started: 3:30 PM (approx.)
  - Smoke passed: 3:34 PM (approx.)
  - Duration: ~4 min
- **Rolled forward to SHA:** `d6a440fd774013b2bc7b1ef894d8b516ac2be008`
  - Duration: ~3 min

### Why did the database stay on the newer schema during rollback?

Migrations only move the database forward; deploying an older application image does not undo them. This is safe because the older code can still work with the newer, backward-compatible database schema.

## Where my secrets live

- **Neon connection string:** GitHub Secret `DATABASE_URL` + Render environment variables. Not in Git or the Docker image.
- **Render deploy hook:** GitHub Secret `RENDER_DEPLOY_HOOK` only.

## Monitoring

- **UptimeRobot:** Checks `/health` every 5 minutes; alerts go to my email.
- **One thing that would make my live app faster on its first request:** Use an always-on Render instance to prevent cold starts caused by the free service spinning down.

## D05 · CI/CD and Going Live

### Rollback Drill
If a faulty deployment reaches production, I will identify the last known stable commit, revert the faulty commit, push the changes, and allow the CI/CD pipeline to redeploy the stable version. I will then run the smoke test and verify that the `/health` endpoint returns HTTP 200.

### Lead Time
Lead time is the time taken for a code change to move from development to production deployment. For this project, I tracked the process from committing the code, pushing it to GitHub, passing CI checks, merging into main, and deploying to Render.

### Deployment Verification
- CI checks passed.
- CD workflow completed.
- Docker image deployed to Render.
- Smoke test passed.
- Production `/health` endpoint returned HTTP 200.
- Live version matched the latest main commit.

# D06 · Collecting the corpus

- **Start target:** Central scheme guidelines + MSMED Act
- **Collected today:** 10 files, 139 pages, 13.4 MB
- **Doors used:** URL list / by hand

## Licence check

| Source | Licence or terms, in my words | May I show full text in answers? |
|---|---|---|
| Government scheme documents | Publicly accessible government documents; reuse terms not verified | No, prefer summaries and citations |
| RBI documents | Official regulatory information; verify reuse terms | No, summarize and cite the original |
| MSME portals | Public portal information; reuse terms not verified | No, cite official source |

## robots.txt

- **Site:** [Government and MSME source websites. Their robots.txt rules were respected.](https://www.cgtmse.in/)
- **What it says:** User-agent: *
Allow: /
Sitemap: https://www.cgtmse.in/site-map.xml
Crawling restrictions were checked by the collector before fetching pages.
- **Was anything blocked for my bot?** No blocked files in today's final report (0 blocked, 0 failed). I respected robots.txt and didn't bypass restrictions.

## Kill and resume

- **Run 1:** I pressed Ctrl+C after 10 files.
- **Run 2:** downloaded=0 skipped=10
- **Run 3:** downloaded=0 skipped=10

## Capacity (from docs/CAPACITY.md)

- **Tokens per page, measured:** 414
- **Full corpus:** 1.03 M tokens, 2,976 chunks, embedding about Rs 17, vectors 9 MB

- **The number that surprised me most, and why:**

  The corpus was only 13.4 MB but covered 139 pages. The actual embedding and vector storage requirements can be larger than the raw file size, so I need to measure them after chunking.

## One thing that went wrong today, and how I fixed it

The CGTMSE sitemap was malformed and couldn't be parsed. Instead of repeatedly retrying it, I switched to collecting documents through verified individual URLs and manual collection, while respecting website restrictions.

## D07 · Parsing My Corpus

1. ## Current Dataset Status

Source entries in data/sources.csv: 10

Files downloaded in the latest fetch: 1

Files skipped in the latest fetch: 9

Total documents currently in Postgres: 30

Total pages currently in Postgres: 121

Replacement NSSH PDF: 28 pages; text extraction verified

Re-parsing the replacement PDF: Pending

Note: The database totals are existing totals, not confirmed D07 parsing totals. Do not use them to calculate parsing coverage until the manifest and parsing results are checked.

2. ## Parsing Failures

Reason

Files

What I did

no_text_layer

1 (original NSSH PDF)

Found an alternative PDF source and downloaded a replacement. Verified that the replacement contains extractable text. Re-parsing is pending.

Original failed file:
data/raw/scsthub/nssh-guidelines-o-b2cca3c3.pdf

Replacement file:
data/raw/scsthub/nssh-guidelines-a2ad8a5d.pdf

Replacement verification:

Pages: 28

First-page text extracted successfully.

Document: National Scheduled Caste and Scheduled Tribe Hub (NSSH) guidelines.

Memorandum dated: 15 November 2021.

3. What I Observed in Parsed Pages

Readable extraction:

PM Vishwakarma — page 32: readable headings and text.

PM Vishwakarma — page 57: Markdown grid table.

Important to Know — page 3: readable bullet points.

CGTMSE — pages 2–10: generally readable section content.

Extraction problems:

PM Vishwakarma — page 7: garbled characters.

PM Vishwakarma — page 61: garbled characters and control symbols.

PM Vishwakarma — page 62: empty extracted text.

PM Vishwakarma — page 64: duplicate government/ministry headers.

CGTMSE — page 10: some table columns have generic names such as Col2 and Col4.

Table extraction:

PM Vishwakarma — page 57: Markdown grid table.

CGTMSE — page 10: Markdown table, but column names are partially generic.

4. Parser Choice

PDF parser: PyMuPDF

Reasons:

PM Vishwakarma: 64 pages and 22 extracted tables.

CGTMSE: 37 pages and 14 extracted tables.

FAQ PDF: 7 pages and 1 extracted table.

PyMuPDF successfully extracted text and tables from these PDFs. However, some pages still need better handling because of garbled text, empty pages and imperfect table structures.

5. Document Types That Need Better Handling

Scanned PDFs without a text layer.

PDFs with unusual font encodings.

Complex tables with merged cells or unclear column structures.

6. One Thing That Went Wrong Today

The original NSSH guidelines PDF failed during parsing with the reason no_text_layer.

I searched for an alternative source and downloaded a replacement PDF. The replacement contains 28 pages, and PyMuPDF successfully extracted its first-page text.

Current status: Replacement verified; database re-parsing and failure-resolution confirmation are still pending.

# D08 · LLM Gateway

## 1. Model Configuration

- **Primary:** `gemini-4-hydrogen` (Google Gemini)
- **Fallback:** `openai/gpt-oss-20b` (Groq)
- **Primary API endpoint:** `https://generativelanguage.googleapis.com/v1beta/openai`
- **Fallback API endpoint:** `https://api.groq.com/openai/v1`
- **Timeout:** 30 seconds
- **USD-INR conversion rate:** ₹95 per USD (used for cost estimates)
- **Configuration verified:** `src/udyamguide/config.py`

## 2. Performance

### First question on my laptop

Question: "What are the current limits for micro, small and medium enterprises?"

- Provider: Gemini
- Model: `gemini-4-hydrogen`
- First words after: Not recorded
- Total time: **22.04 seconds**
- Input tokens: **217**
- Output tokens: **177**
- Estimated cost: **₹0.000000**
- Attempts: 2
- Fallback: No

### Question 6

Question: "Will my buyer pay me this month?"

- Provider: Gemini
- First words after: **7.56 seconds**
- Total time: **8.78 seconds**
- Input tokens: **212**
- Output tokens: **154**
- Estimated cost: **₹0.000000**
- Attempts: 1
- Fallback: No

### Same question on my live URL

- First words after: Not tested yet.
- Day 1 latency target: **Under 1.5 seconds**.

## 3. Tokens: English Against Tamil

| Message | Input tokens |
|---|---:|
| "Hi" (baseline, mostly system prompt) | 205 |
| English refund sentence | 240 |
| Same sentence in Tamil | 254 |

**Calculation:**

Tamil / English = 254 / 240 = 1.0583

- Tamil needs approximately **1.06 times** the input tokens of English.
- Tamil used 14 more tokens, approximately 5.83% more than English in this test.

## 4. What the Model Does Without My Documents

### Question 6: "Will my buyer pay me this month?"

**Did it admit it cannot know?** Yes.

Exact words:

> I am not sure whether your buyer will pay you this month, as I cannot predict a specific buyer's actions or see your invoice details.

It also explained MSME delayed-payment protections, including the maximum 45-day agreed credit period and the MSME Samadhaan portal.

### A detail it got wrong or invented

**Question:** "What are the current limits for micro, small and medium enterprises?"

**What Groq said:**

It returned outdated and incorrect MSME classification figures in repeated tests, including:

- Micro: ₹25 lakh turnover
- Small: ₹5 crore turnover
- Medium: ₹10 crore turnover

Other responses also incorrectly used paid-up capital or outdated turnover limits.

**What is correct under the revised MSME classification:**

| Category | Investment limit | Annual turnover limit |
|---|---:|---:|
| Micro | ₹2.5 crore | ₹10 crore |
| Small | ₹25 crore | ₹100 crore |
| Medium | ₹125 crore | ₹500 crore |

**Observation:** Gemini returned the correct revised classification in the test, whereas Groq produced inconsistent and outdated answers.

### Off-topic question

**English question:** "Explain in one sentence what a refund is."

- Provider: Groq fallback.
- Response: "I’m sorry, but that question is outside the scope of UdyamGuide."
- Result: Correctly declined the unrelated question in one sentence.

**Tamil equivalent:**

"பணத்தைத் திரும்பப் பெறுதல் என்றால் என்ன என்பதை ஒரே வாக்கியத்தில் விளக்கவும்."

- Provider: Groq fallback.
- Result: Answered the unrelated question instead of refusing it.

**Conclusion:** Scope enforcement is inconsistent across languages.

### Additional off-topic test

**Question:** "Who won the 2011 cricket world cup?"

- Provider: Groq fallback.
- First words after: 33.77 seconds.
- Total time: 34.20 seconds.
- Input tokens: 241.
- Output tokens: 258.
- Estimated cost: ₹0.009070.
- Response: "I am not sure."

## 5. Fallback and Circuit Breaker

- **Primary provider:** Gemini (`gemini-4-hydrogen`).
- **Fallback provider:** Groq (`openai/gpt-oss-20b`).
- **Fallback observed:** Yes.
- Groq answered the English refund, Tamil refund, cricket and repeated MSME questions.
- First words after: 33.77 seconds for the cricket question.

### Controlled failure test

- Deliberately breaking the Gemini primary provider: Not yet confirmed.
- Fallback response during a deliberate primary failure: Not yet measured.
- Question number at which "llm call gemini ... error" stopped appearing in logs: Not recorded.
- Circuit-breaker opening and recovery: Not yet verified.

## 6. The Bill

**Endpoint:** `/v1/usage?days=1`

**Date:** 26 November 2026

| Metric | Result |
|---|---:|
| Total calls | 17 |
| Errors | 7 |
| Fallbacks | 7 |
| Input tokens | 2,345 |
| Output tokens | 2,562 |
| Estimated total cost | ₹0.073 |

### Average cost per call

₹0.073 / 17 = ₹0.00429

- Average estimated cost per call: **₹0.00429**
- Equivalent to approximately 0.43 paise per call.
- Day 1 cost target: Under ₹0.50 per answered question.
- **Result: PASS**

### Fallback rate

7 / 17 × 100 = 41.18%

- Fallback rate: **41.18%**
- This needs investigation because a significant proportion of calls used the fallback provider.

**Note:** These are application-reported estimated costs, not confirmation of actual provider billing. Gemini requests displayed ₹0.000000 in the terminal.

## 7. One Thing That Went Wrong Today, and How I Fixed It

### Problem

Initially, several unit tests failed:

- Chat API requests returned HTTP 503.
- Usage API tests returned HTTP 500.
- The unit-test client was using the real LLM gateway and usage repository instead of test doubles.

### Root cause

The closer `tests/unit/conftest.py` fixture took precedence over the root `tests/conftest.py` fixture.

The unit fixture did not override all the required dependencies.

### Fix

- Imported `get_gateway` and `LLMGateway`.
- Added a fake LLM gateway using `LLMGateway([llm])`.
- Imported `get_usage_repo`.
- Added a `FakeUsage` repository.
- Added dependency overrides for the gateway and usage repository in the unit-test client fixture.

### Result

- All 7 chat API tests passed.
- All 78 unit tests passed.


## 8. Day 1 Overall Observations

1. Gemini successfully answered the tested MSME classification question with the revised limits.
2. Groq fallback produced inconsistent and outdated MSME information.
3. English off-topic refusal worked, but the Tamil equivalent was answered.
4. The model correctly admitted it could not predict whether a specific buyer would pay.
5. Usage tracking successfully reported calls, errors, fallbacks, tokens and estimated cost.
6. Average estimated cost per call was comfortably below the ₹0.50 target.
7. Fallback was used in 41.18% of recorded calls.
8. Live URL latency has not yet been measured.
9. Controlled primary-provider failure and circuit-breaker behaviour still need testing.
