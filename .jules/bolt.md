## 2024-05-23 - [Optimization Trade-offs]
**Learning:** Faster isn't always better. Attempted to switch from SHA256 to XXH64 for 10x speedup, but this compromised data integrity (collision risk) and created non-deterministic behavior (dependent on optional library).
**Action:** When optimizing, always prioritize correctness and safety. Simple wins like increasing buffer size (8KB -> 64KB) are often safer and sufficient.
