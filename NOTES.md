
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
