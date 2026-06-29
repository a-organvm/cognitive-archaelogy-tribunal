## 2024-05-23 - [Redundant Hashing in Deduplication]
**Learning:** Logic that re-processes collections (like checking for duplicates) must coordinate with insertion logic to avoid re-doing expensive work. The `Deduplicator` computed hashes on insertion (for size collisions) but then re-computed them during the final scan, leading to 2x+ work for duplicates.
**Action:** Always check if an expensive result is already cached before computing it, especially when multiple passes over data are involved.
