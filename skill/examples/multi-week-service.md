# PLAN.md — wgdealer

**Goal:** Telegram bot that issues and revokes WireGuard configs across a multi-country server fleet.
**Date:** 2026-07-15 · **Version:** v1
**Guides applied:** all four (network-facing, handles user data, multi-week implementation).

## Summary
A Go service: users request a config via Telegram, the bot allocates a peer on the least-loaded server in the chosen country and returns a `.conf` file; admins can revoke. State in SQLite, peers managed over wgctrl. Stack: Go + wgctrl-go + telegram-bot-api + SQLite. Biggest risk: the bot host is a single point holding credentials to every VPN node. First milestone: issue one working config on one server, manually triggered.

## Core

**Functionality**
- User can request a config for a country; receives a `.conf` file + QR (one active peer per user per country)
- User can list and revoke their own peers
- Admin can add/remove servers, revoke any peer, see per-server load
- System reaps peers with no handshake for 30 days
- Non-goals v1: payments, bandwidth quotas, AmneziaWG/VLESS transports, web UI

**Tech stack**
- Go — single binary per node, wgctrl-go is native. Rejected: Rust — no mature wgctrl equivalent; Python — deployment weight on nodes.
- SQLite via `modernc.org/sqlite` (CGO-free) — one bot host, low write rate. Rejected: Postgres — an extra service for <50 writes/s is pure ops cost.
- Node control: small Go agent on each server exposing gRPC over mTLS. Rejected: SSH-exec from bot — fragile parsing, and a shell foothold is a worse credential to hold than a scoped API.
- Constraint: nodes run Linux kernel WireGuard; agent needs CAP_NET_ADMIN only.

**Roadmap**
1. **Node agent** (M) — gRPC: AddPeer/RemovePeer/ListPeers/Stats. Done when a manual gRPC call creates a peer and a phone connects through it. Riskiest phase (kernel/wgctrl behavior), so first.
2. **Allocator + store** (M) — schema, IP pool per server, least-loaded selection. Done when unit tests cover allocation, collision, and revoke. Blocked by 1.
3. **Bot commands** (M) — /new /list /revoke with config rendering + QR. Done when the full user flow works on one real server. Blocked by 2.
4. **Admin + fleet** (M) — server registry, mTLS cert issuance, admin commands. Done when a second country comes online with no code changes. Blocked by 3.
5. **Reaper + ops** (S) — handshake-age reaper, backups, alerts. Done when a stale peer is auto-removed in a timed test. Blocked by 4.

**Caveats:** Telegram is blocked in some target regions (users may need the VPN to reach the bot that issues the VPN — document a bootstrap path); IP pool exhaustion per server (fixed /24 per node, alert at 80%); wgctrl requires the agent to run as root or with CAP_NET_ADMIN.

## Security & privacy

**Threat model**
- Assets, ranked: node credentials (mTLS keys), user↔peer mapping (deanonymizing), server WG private keys, bot token.
- Attackers that apply: opportunistic scanners (nodes have public ports), malicious user (resource exhaustion via /new spam), seized/compromised node. Cut: nation-state traffic analysis — out of scope, stated to users.
- Surface: Telegram webhook/polling, gRPC ports on every node, SQLite file on bot host.
- Non-threats: WireGuard protocol attacks (trusting upstream), Telegram MITM (their transport).

**Data inventory**
- Telegram user ID ↔ peer pubkey ↔ assigned IP — sensitive; lives in SQLite; kept while peer active + 7 days.
- Handshake timestamps per peer — internal; on nodes, ephemeral.
- Deliberately NOT collected: usernames, traffic logs, connection source IPs.

**Controls**
- Bot↔node: mTLS, unique cert per node, bot is the only CA client → compromised node can't call siblings.
- Peer private keys generated client-side is impossible via Telegram, so: generated on bot host, sent once in the `.conf`, never stored — DB keeps pubkeys only.
- /new rate limit: 3/day/user. IP pool exhaustion alert.
- Secrets: bot token + CA key in env from systemd credentials, never in repo; node certs rotated on admin command.
- Deps: `govulncheck` in CI, lockfile pinned.

**Privacy posture:** no third parties receive anything; user can `/wipe` (deletes mapping + revokes peers, actually deletes rows); logging is peer-pubkey-only, no Telegram IDs at info level. Regulatory: none formally, but the user base assumes deniability — the data-minimization lines above ARE the product.

**Failure plan:** DB leak exposes user↔pubkey mapping (worst case — hence 7-day retention); detection: agent heartbeat alerts + auth-failure counters; response: single admin command revokes a node's cert and drains its peers; recovery: nightly encrypted SQLite backup, restore tested in phase 5.

## Quality
- `golangci-lint` (errcheck, govet, staticcheck) blocks merge; `gofmt` enforced.
- Errors: node-unreachable is recoverable (retry, mark degraded); DB corruption is fatal-loud.
- MUST test: allocator, IP pool math, revoke paths, config rendering. MAY skip: Telegram handler glue.
- Layout: `core/` (allocation, no I/O), `agent/`, `bot/`, `store/` — core imports nothing project-specific. Files ≤400 lines.
- Pre-resolved: clarity over cleverness in the allocator even if it costs an extra query.

## First-run
- Verify before writing: wgctrl-go AddPeer semantics against its source (does it replace or append allowed-ips?); telegram-bot-api file-upload API against current docs; SQLite driver's concurrency mode. Obtain one real `wg show dump` sample before writing the parser.
- Unverified assumptions remaining: agent behavior under kernel <5.6 (accepted: fleet is ≥6.1).
- Vertical slice: phase 1 ends with a phone connected through a bot-created peer — full stack proven before any breadth.
- Increments: one gRPC method + its test at a time; `go vet` after each.
- Two failed fixes on the same bug → stop, re-read wgctrl source, not a third guess.

## Decision log

| Decision | Options | Default | Cost to reverse |
|---|---|---|---|
| Peer key generation | bot-side, never stored / bot-side, stored encrypted | never stored | High (privacy promise) |
| Node transport | gRPC+mTLS / SSH exec / WireGuard-tunneled HTTP | gRPC+mTLS | High |
| Retention after revoke | 0 / 7 / 30 days | 7 days | Low |
| One peer per country per user | enforce / allow N | enforce | Low |

## Next actions
1. Verify wgctrl-go AddPeer/allowed-ips semantics against source; note findings in FIRST_RUN log
2. Scaffold `agent/` with AddPeer + one integration test on a throwaway VPS
3. Connect a phone through a manually-issued peer (phase 1 "done when")
4. Draft SQLite schema + IP-pool allocation test cases

---
*Changelog: v1 initial.*
*Re-plan triggers: phase overruns 2×; wgctrl assumption falls; transport decision changes.*
*Kill criterion: if agent+mTLS ops overhead exceeds ~1 day/month for a 5-node fleet, fall back to plain wg-quick + manual config distribution — the bot must earn its complexity.*