# PLAN.md — hashcheck

**Goal:** CLI that verifies file checksums against a manifest and reports drift.
**Date:** 2026-07-15 · **Version:** v1
**Guides applied:** core, quality, first-run. **Skipped:** security (local single-user tool, no network, no user data).

## Summary
A single-binary Rust CLI: `hashcheck gen <dir>` writes a manifest of BLAKE3 hashes; `hashcheck verify <dir>` diffs the tree against it. Stack: Rust + clap + blake3, no other deps. Biggest risk: symlink/permission edge cases on traversal. First milestone: gen+verify round-trip on a flat directory.

## Core

**Functionality**
- User can generate a manifest for a directory tree (`gen`)
- User can verify a tree against a manifest, exit 0/1, list changed/missing/new files (`verify`)
- Non-goals v1: watch mode, remote manifests, any GUI

**Tech stack**
- Rust (single static binary, target is servers without runtimes). Rejected: Python — needs interpreter on target.
- blake3 crate (fast, parallel by default). Rejected: sha2 — slower, no benefit here.
- clap for args. MSRV: whatever current stable is; no platform constraints.

**Roadmap**
1. **Walk + hash** (S) — done when `gen` on a flat dir produces a correct manifest. Riskiest phase (traversal edge cases), so it's first.
2. **Verify + diff** (S) — done when round-trip on an unchanged tree exits 0, and a mutated file exits 1 with the path listed. Blocked by 1.
3. **Polish** (S) — done when `--help` is coherent, errors name the offending path, and symlink policy is documented. Blocked by 2.

**Caveats:** symlinks (policy: skip + warn, v1), files changing mid-hash (accepted, documented), very large trees (fine — blake3 is parallel; no work needed).

## Quality
- `cargo clippy -- -D warnings` + `rustfmt`, both block commit.
- Errors: I/O errors are recoverable (report path, continue); manifest parse failure is fatal.
- Tests: hashing and diff logic MUST be tested (tempdir fixtures); CLI glue MAY be skipped.
- One `main.rs` + one `lib.rs`; logic in lib, I/O in main.

## First-run
- Verified before writing: blake3 crate API from docs.rs (current version), `walkdir` behavior on symlinks from its docs. Unverified: none remaining.
- Vertical slice: phase 1 is runnable end-to-end (`gen` on a real dir) before verify exists.
- Per-phase check commands are in the roadmap "done when" lines.
- Edge cases in first draft: empty dir, unreadable file, manifest for a moved tree.

## Decision log

| Decision | Options | Default | Cost to reverse |
|---|---|---|---|
| Symlink handling | skip+warn / follow / hash link target path | skip+warn | Low |
| Manifest format | JSON / plain `hash  path` lines | plain lines | Medium (format is an interface) |

## Next actions
1. `cargo new hashcheck`, add clap/blake3/walkdir, commit CI with clippy gate
2. Implement walk+hash with tempdir test
3. Run `gen` on a real directory, eyeball the manifest

---
*Changelog: v1 initial.* *Kill criterion: if blake3 traversal can't beat `sha256sum -c` wall-clock on 10k files, the tool has no reason to exist.*