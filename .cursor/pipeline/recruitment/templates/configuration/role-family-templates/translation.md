# Translation Role-Family Template — Quarterly Configuration

> **Owner:** CTO-L

---

## Assessment Battery

| Component                             | Duration    | Pass                      | Auto-Reject        |
| ------------------------------------- | ----------- | ------------------------- | ------------------ |
| BLEU/TER                              | < 5 min     | BLEU ≥ 0.80               | < 0.60             |
| Transcreation Challenge               | 72-hr async | ≥ 75/100 (human-scored)   | < 60/100           |
| Localization Engineering (4 stations) | 90 min      | ≥ 80%, zero S1–2 failures | < 60% OR S1–2 fail |

## Engineering Challenge Stations

| Station                             | Duration | Method            | Auto-Reject               |
| ----------------------------------- | -------- | ----------------- | ------------------------- |
| A: String Extraction (Swift/Kotlin) | 25 min   | Diff-graded       | All strings not extracted |
| B: XLIFF Debugging (5 errors)       | 20 min   | Schema + diff     | ≤ 2 of 5 fixed            |
| C: Plural Rules (3 languages)       | 20 min   | CLDR-verified     | Incorrect for all 3       |
| D: RTL Layout Identification        | 25 min   | Answer-key graded | ≤ 2 of 6 identified       |

## CTO-L Human Review (R1 Exception Trigger)

| Time      | Activity                         | Pass                              |
| --------- | -------------------------------- | --------------------------------- |
| 0–10 min  | Transcreation re-score           | No axis revised downward > 10 pts |
| 10–20 min | Per-pair competency verification | ≥ 4 of 5 edge cases correct       |
| 20–30 min | Certification spot-check         | All claimed certs verified        |

## Certification Verification (Stage 6, Automated)

| Certification | Issuing Body            | Verification  | Minimum          |
| ------------- | ----------------------- | ------------- | ---------------- |
| JLPT          | Japan Foundation / JEES | JEES API      | N2+              |
| TOPIK         | NIIED (Korea)           | NIIED portal  | Level 4+         |
| ATA           | ATA                     | Directory API | Active + current |
| HSK           | CTI                     | CTI API       | Level 5+         |

## Per-Language-Pair Competency Matrix

| Language Pair | BLEU ≥ 0.80 | Transcreation ≥ 75 | Engineering ≥ 80 | Verdict     |
| ------------- | ----------- | ------------------ | ---------------- | ----------- |
| EN → ZH-CN    | TBD         | TBD                | TBD              | PASS / FAIL |
| EN → JA       | TBD         | TBD                | TBD              | PASS / FAIL |
| EN → KO       | TBD         | TBD                | TBD              | PASS / FAIL |
| EN → FR       | TBD         | TBD                | TBD              | PASS / FAIL |
| EN → ES       | TBD         | TBD                | TBD              | PASS / FAIL |

**Note:** Each pair vetted independently. Single column failure = entire pair fails.

---

**Configured By:** CTO-L | **Quarter:** [Qn YYYY] | **Audit Hash:** [SHA-256]
