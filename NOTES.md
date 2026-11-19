
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
