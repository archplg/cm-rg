# Phase 2F write corruption diagnosis

- Platform: Windows-11-10.0.26200-SP0
- Python: 3.14.3 (tags/v3.14.3:323c59a, Feb  3 2026, 16:04:56) [MSC v.1944 64 bit (AMD64)]
- Test dir: C:\Users\Сергей Долгов\archipelago_cross_model\diagnose_write_test
- OneDrive env: C:\Users\Сергей Долгов\OneDrive

## Results

| Test | Result | Detail |
|---|---|---|
| 1. Atomic single | FAIL | 12154/12044 bytes |
| 2. Direct single | FAIL | 12154/12044 bytes |
| 3. 30 sequential | FAIL | 30/30 failed |
| 4. Delayed re-read | PASS | 0 corrupted |
| 5. Large file | FAIL | 150866/150814 bytes |

## Test 3 failure sizes

- TEST_seq_00: 12152 bytes (expected 12042)
- TEST_seq_01: 12152 bytes (expected 12042)
- TEST_seq_02: 12152 bytes (expected 12042)
- TEST_seq_03: 12152 bytes (expected 12042)
- TEST_seq_04: 12152 bytes (expected 12042)
- TEST_seq_05: 12152 bytes (expected 12042)
- TEST_seq_06: 12152 bytes (expected 12042)
- TEST_seq_07: 12152 bytes (expected 12042)
- TEST_seq_08: 12152 bytes (expected 12042)
- TEST_seq_09: 12152 bytes (expected 12042)
