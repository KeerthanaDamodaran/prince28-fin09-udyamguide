# Dataset: UdyamGuide

Helps micro and small enterprises find schemes, collateral-free loans and protection against delayed payments, citing MSME rules.

- **Start target:** Central scheme guidelines + MSMED Act
- **Full target:** + CGTMSE circulars, Tamil Nadu schemes and FAQs (2,500+ pages)
- **Collected by:** `scripts/fetch.py` as `examate-student-bot` (https://github.com/KeerthanaDamodaran/prince28-fin09-udyamguide): robots.txt respected, at most 4 requests at once, 0.5 s between requests to one site.

## Where the documents come from

- https://msme.gov.in/
- https://udyamregistration.gov.in/
- https://www.cgtmse.in/

## Terms I follow

Public scheme documents. Cite scheme and date.

- Every answer links to the original document.
- No personal data is collected.

<!-- generated:start -->
## Sources (generated 2026-11-23 13:57 UTC by scripts/dataset_report.py)

| Source | Licence / terms | Files | MB | Pages* | How | Fetched | Example URL |
|---|---|---|---|---|---|---|---|
| cgtmse | Project policy: reuse terms unverified; cite source and date | 1 | 0.5 | 37 | http | 2026-11-23 | https://www.cgtmse.in/Default/ViewFile/?id=1743176302611_CGTMSE+-+Scheme+Document+CGS+I_updated+as+on+Apr+1+2025.pdf&path=Page |
| pm-vishwakarma | Project policy: reuse terms unverified; cite source and date | 1 | 11.1 | 64 | http | 2026-11-23 | https://pmvishwakarma.gov.in/cdn/MiscFiles/eng_v30.0_PM_Vishwakarma_Guidelines_final.pdf |
| ramp | Project policy: reuse terms unverified; cite source and date | 1 | 0.1 | 2 | http | 2026-11-23 | https://www.nimsme.org/news-article/raising-accelerating-msme-performance-ramp-scheme |
| rbi | Project policy: reuse terms unverified; cite source and date | 1 | 0.2 | 7 | http | 2026-11-23 | https://www.rbi.org.in/commonman/Upload/English/FAQs/PDFs/MICRO30072025E.pdf |
| rbi-master | Project policy: reuse terms unverified; cite source and date | 1 | 0.2 | 11 | http | 2026-11-23 | https://www.rbi.org.in/Scripts/NotificationUser.aspx?Id=11060 |
| rbi-mudra | Project policy: reuse terms unverified; cite source and date | 1 | 0.1 | 4 | http | 2026-11-23 | https://www.rbi.org.in/Scripts/NotificationUser.aspx?Id=11946 |
| samadhaan | Project policy: reuse terms unverified; cite source and date | 1 | 0.1 | 2 | http | 2026-11-23 | https://samadhaan.msme.gov.in/ |
| scsthub | Project policy: reuse terms unverified; cite source and date | 1 | 1.0 | 7 | http | 2026-11-23 | https://www.scsthub.in/sites/default/files/NSSH_Guidelines_o.pdf |
| udyam | Project policy: reuse terms unverified; cite source and date | 1 | 0.0 | 2 | http | 2026-11-23 | https://udyamregistration.gov.in/Important.aspx |
| zed | Project policy: reuse terms unverified; cite source and date | 1 | 0.1 | 3 | http | 2026-11-23 | https://zed.msme.gov.in/ |

**Total:** 10 files, 13.4 MB, 139 pages. Not downloaded: 0 blocked by robots.txt, 0 failed.

*Pages = PDF pages, plus one page per 3,000 characters of text or HTML.

## Files (first 10 of 10)

The complete list, with a sha256 fingerprint of every file, is `data/manifest.jsonl`.

| # | Title / file | Source | Pages | Fetched | URL |
|---|---|---|---|---|---|
| 1 | CGTMSE Scheme Document | cgtmse | 37 | 2026-11-23 | https://www.cgtmse.in/Default/ViewFile/?id=1743176302611_CGTMSE+-+Scheme+Document+CGS+I_updated+as+on+Apr+1+2025.pdf&path=Page |
| 2 | PM Vishwakarma Scheme Guidelines | pm-vishwakarma | 64 | 2026-11-23 | https://pmvishwakarma.gov.in/cdn/MiscFiles/eng_v30.0_PM_Vishwakarma_Guidelines_final.pdf |
| 3 | RAMP Scheme Overview | ramp | 2 | 2026-11-23 | https://www.nimsme.org/news-article/raising-accelerating-msme-performance-ramp-scheme |
| 4 | RBI MSME FAQ | rbi | 7 | 2026-11-23 | https://www.rbi.org.in/commonman/Upload/English/FAQs/PDFs/MICRO30072025E.pdf |
| 5 | RBI MSME Master Direction | rbi-master | 11 | 2026-11-23 | https://www.rbi.org.in/Scripts/NotificationUser.aspx?Id=11060 |
| 6 | MUDRA Loan Scheme Guidelines | rbi-mudra | 4 | 2026-11-23 | https://www.rbi.org.in/Scripts/NotificationUser.aspx?Id=11946 |
| 7 | MSME Samadhaan Portal | samadhaan | 2 | 2026-11-23 | https://samadhaan.msme.gov.in/ |
| 8 | National SC-ST Hub Guidelines | scsthub | 7 | 2026-11-23 | https://www.scsthub.in/sites/default/files/NSSH_Guidelines_o.pdf |
| 9 | Udyam Registration Information | udyam | 2 | 2026-11-23 | https://udyamregistration.gov.in/Important.aspx |
| 10 | ZED MSME Portal | zed | 3 | 2026-11-23 | https://zed.msme.gov.in/ |
<!-- generated:end -->

## Known gaps

- (what is still missing from the start target, and why)
The current dataset is a starter corpus and does not yet cover all MSME schemes, guidelines, FAQs, and regional benefits.

Limited scheme coverage: Several schemes, including PMEGP, Stand-Up India, ASPIRE, ECLGS, TReDS, and MSE-CDP, still need their official guidelines and supporting documents to be collected and verified.

Tamil Nadu-specific schemes: State-level MSME subsidies, incentives, financial assistance, and eligibility guidelines are not yet comprehensively covered.

FAQs and operational guidance: The corpus mainly contains scheme documents and portal information. Detailed FAQs, application procedures, required documents, step-by-step processes, and troubleshooting guidance remain incomplete.

Regulatory updates: New circulars, amendments, revised eligibility criteria, interest rates, subsidy limits, and scheme updates need to be incorporated periodically.

Delayed payment coverage: MSMED Act provisions and Samadhaan portal information are included, but detailed case procedures, claim workflows, and supporting legal guidance need further coverage.

Limited corpus size: The current collection contains only 10 documents (139 pages, approximately 13.4 MB). It is sufficient for initial development and testing but not yet comprehensive enough for all MSME-related queries.

The dataset will be expanded incrementally using verified official sources. Documents will be deduplicated, source metadata maintained, and original references preserved to support reliable retrieval and citation.
