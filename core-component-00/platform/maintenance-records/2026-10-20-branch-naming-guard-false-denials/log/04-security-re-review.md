# 04 — Security Re-Review

| Field    | Value                                                                                                                                                   |
| -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Reviewer | Dr. Noor Haddad                                                                                                                                         |
| Role     | Staff Engineer, Security, Safety & Evaluation (BCU-00), independent of the delivery chain, holding a review veto                                        |
| Scope    | Revised, uncommitted H-MAE01 hook and its tests in the `agb-guard` worktree, checked against the four conditions in `03-independent-security-review.md` |
| Verdict  | NO VETO WITH FINDINGS                                                                                                                                   |

All four conditions are met. One new P2 finding remains. It is a regression in the bash line-continuation form,
and it is a condition for commit. No finding is P0 or P1. Approval rests with the user.

## Method

- `python -m pytest -q test_multi_agent_branch_naming_guard.py` from the hooks folder: `237 passed in 21.56s`.
- I re-ran the differential harness, comparing the new `_find_invalid_name` with the committed regexes loaded
  from `git show HEAD:...`. It covered the 32 original inputs, 10 new probes and 10 approved-scope controls.
  The command name was assembled at runtime.
- On the 32 original inputs, every input from Findings 1 to 5 in record 03 is now denied. Findings 6 to 8 are
  unchanged, apart from `--attr-source HEAD`, which is now denied.
- All 10 approved-scope controls give ALLOW. They include worktrees on existing branches such as
  `ide-adaptation`, `--detach`, `-d`, and the `core00/` and `anu00/` prefixes.
- Timing: the record 03 Finding 4 input takes 0.010 s at 13.6 KB and 0.142 s at 102 KB, and is denied.
  25,000 git words with an open quote take 0.046 s. A 200 KB option cluster takes 0.458 s.
- Every lazy-regex fallback is gone, and every look-ahead is bounds-checked. No crash path before the deny
  print was found.

## Conditions Checked

1. **Findings 1 to 3 closed, with regression tests: met.** Every failing input from record 03 is denied:
   comments holding a quote, `\"`, the backtick-quote form, `(…)`, `$(…)`, backticks, `bash -c`,
   `pwsh -Command` and `Invoke-Expression`. Each has a test, run under both the Bash and the PowerShell tool.
   `cmd /c "git …"` is now denied too.
2. **Finding 4 bounded, with a timing test: met.** No backtracking regex remains. The test
   `test_slow_input_is_linear_and_still_denied` (×800 and ×6000, under 1 s) and the test
   `test_large_balanced_input_is_fast` both pass. My own measurement is 0.142 s at 102 KB.
3. **Findings 5 to 8 fixed or stated: met.**
   - Finding 5 (bundled options) is fixed and tested.
   - The `--attr-source` part of Finding 6 is fixed. Abbreviated long options, adjacent quoting, expansion,
     aliases, ref plumbing, remote guessing and the basename rule are stated in the docstring.
4. **Differential re-run: met.** This record holds the results.

On the builder's doubts:

- The denial of quoted mentions is the trade-off I accepted.
- An unknown letter before `b` or `c` makes git reject the option cluster, so no branch is created.
- `--attr-source=HEAD checkout -b bad` is denied, which I verified. It has no test.

## Remaining Findings

1. **P2, regression: bash line continuation hides the creation flag.** Both passes treat a newline as a
   separator, so a `\` at the end of a line splits the command.
   - `git worktree add \⏎  -b bad ../wt` gives ALLOW, and the same input with CRLF line endings also gives
     ALLOW. The committed guard denied both.
   - `git checkout \⏎  -b bad` and `git \⏎  checkout -b bad` give ALLOW in both versions.
   - Long worktree commands are often written this way, so this is a natural input.
   - Fix: before both passes, collapse `\` followed by `\r?\n`, and a backtick followed by `\r?\n`, into a
     space. Add a test for each form above with both line endings.
2. **P3: a PowerShell backtick continuation is falsely denied.** `git worktree add `⏎`  -b agent/a/b ../wt`
   and `git worktree add `⏎`  ../wt ide-adaptation` are both denied with the name `` ` ``. This fails closed.
   The fix for Finding 1 closes it.
3. **P3: quote-split command words are missed.** `g''it checkout -b bad` gives ALLOW in both versions. If
   `_raw_words` deleted quotes rather than replacing them with spaces, this form would be denied. The same
   change would also close the adjacent-quoting limit (`-b 'master'x`).
4. **P3: no test for `--attr-source=HEAD`.** The behaviour is correct. The test is missing.

## Conditions

1. Finding 1 is closed, with tests for the LF and CRLF line endings of every form listed, before the change is
   committed. I re-run those inputs, and the two backtick inputs from Finding 2, before the change is
   committed.
2. Findings 2 to 4 are at Harness Engineering's discretion.
