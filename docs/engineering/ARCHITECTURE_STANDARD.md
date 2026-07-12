# FlowVerse Architecture Standard

## Purpose

- Keep V1 and later phases cohesive, testable, evolvable, reliable, and performant.
- Choose the simplest design that satisfies the approved slice and confirmed near-term constraints.
- This standard does not select a framework, directory layout, process boundary, deployment topology, or architecture pattern.
- Accepted ADRs authorize target decisions; actual implemented facts require source/config/test evidence and Confirmed conformance in ARCHITECTURE_BASELINE.md.

## Context and Pattern Gate

Before selecting a pattern, confirm scale, data volume, traffic, team expertise, timeline, domain complexity, real-time needs, compliance, budget, and deployment constraints.

For every proposed pattern answer:

1. What specific confirmed problem does it solve?
2. What simpler alternative was considered?
3. Can the complexity be deferred safely?
4. Can the team operate, test, and recover it?
5. What cost, failure mode, and lock-in does it add?

Do not introduce microservices, event sourcing, CQRS, event buses, queues, plugin systems, distributed caches, service meshes, or generic platform layers merely because the product has multiple phases.

## High Cohesion

- Each module owns one clear business capability or platform responsibility and one primary reason to change.
- Each business invariant and mutable data/state set has one authoritative owner.
- Module internals are private by default; consumers use an explicit public contract.
- UI, transport, controller, or route layers adapt and orchestrate; they do not own core business rules.
- Core rules do not depend directly on React, HTTP, ORM/database details, AI providers, or third-party SDKs.
- Shared/common/utils/helpers contain only stable, domain-neutral, stateless code with at least two real independent consumers or a confirmed cross-cutting safety boundary.
- Do not create or expand god pages, components, stores, services, managers, base classes, or miscellaneous utility containers.
- Similar syntax alone is not sufficient for abstraction; semantics, lifecycle, ownership, and change reason must align.

## Low Coupling

- Production module dependencies have an explicit direction and no cycles.
- Cross-module work uses the provider's public entry point; no private deep imports, table access, repository access, or mutable-state reach-through.
- Shared/platform layers never depend back on feature/domain modules.
- A use-case owner coordinates cross-module consistency; do not rely on hidden shared mutation or implicit distributed transactions.
- External I/O adapters isolate confirmed volatility or test boundaries; avoid one-interface-per-class formalism.
- Composition happens at an explicit application boundary; do not use hidden service locators or mutable global state.
- Missing architecture/dependency tooling is Unverified, never proof that boundaries pass.

## Module and Contract Rules

Formal contracts are required for cross-module, external API, persistent-data, configuration, or asynchronous boundaries.

Each contract records:

- Module ID, responsibility, non-goals, owner, consumers, and allowed dependencies
- Inputs, outputs, validation, invariants, explicit errors, and caller recovery
- Side effects, data ownership, transaction and consistency boundaries
- Sync/async semantics, deadline, cancellation, retry owner, idempotency, and ordering
- Data scale, concurrency, memory, latency, availability, and other resource limits
- Permission, privacy, audit, logging/redaction, compatibility, versioning, and deprecation
- Contract, integration, failure, performance, and observability evidence

When Python and TypeScript become Confirmed targets, cross-boundary data uses explicit types. Any, arbitrary dictionaries/objects, and unchecked provider payloads require runtime validation and a documented reason.

## Extensibility Without Over-Engineering

Create an extension point only when at least one is true:

- Two real consumers share semantics, lifecycle, ownership, and change axis.
- A second implementation is already approved.
- A confirmed external/provider boundary needs isolation.
- An approved near-term phase names the variation.

Otherwise keep the implementation local and concrete.

- Record the variation axis, owner, default implementation, lifecycle, and contract tests.
- Do not add plugin registries, universal hooks, generic repositories, factories, or framework layers for hypothetical use.
- Local reversible implementation is preferred over central abstraction with uncertain consumers.
- Temporary flags, shims, adapters, and dual paths require an owner, removal trigger, due phase/date, and debt ID.

## Data and Multi-Phase Evolution

- Data, cache, draft, server state, and derived view state each have one authoritative owner.
- A cache is not a source of truth; record key, capacity, lifetime, invalidation, consistency, and owner.
- Once another module, stored record, deployed instance, test fixture, or client consumes a contract, it becomes a compatibility surface.
- Contract changes list consumers, compatibility class, release order, migration, rollback/forward recovery, and removal conditions.
- Breaking changes require user approval.
- Database/event evolution must be repeatable or recoverable, bounded, observable, and safe for the confirmed deployment model; use staged compatibility only when required by that model.
- Each product phase updates architecture baseline, accepted decisions, reliability/performance budgets, and technical debt.

## ADR Triggers

Draft an ADR before:

- Adding or changing an architecture-level public/data/deployment boundary, re-owning a capability/data set, or changing dependency direction
- Changing process, service, deployment, data-owner, transaction, or consistency boundaries
- Introducing an architecture framework, database, queue, event bus, shared/persistent cache, search system, or provider
- Changing a public API/event/schema/config contract or compatibility strategy
- Changing auth, trust, privacy, retention, key, retry, idempotency, or async-delivery semantics
- Confirming availability SLO, redundancy, failover, RTO/RPO, degradation, or recovery strategy
- Introducing a plugin/platform extension point or accepting an architecture exception
- Superseding an Accepted decision

Local reversible implementation modules/details inside a Confirmed boundary do not need an ADR when they change no public contract, dependency direction, ownership, data, security, reliability, or deployment semantics.

## Quality Gate

Every implementation plan states affected modules, ownership, public contracts, dependency edges, data movement, change class, ADR trigger, reliability/performance impact, and debt impact.

Completion requires:

- No new cycles, private cross-boundary access, second source of truth, or unapproved structural change
- Applicable unit, contract, integration, failure, architecture, performance, and E2E evidence
- Updated ARCHITECTURE_BASELINE.md, Accepted ADRs, RELIABILITY_BUDGET.md, and TECH_DEBT_REGISTER.md when affected
- No expired exception or undocumented TODO/FIXME/HACK

Do not invent generic LOC, coverage, complexity, service-count, or abstraction-count thresholds; confirm them from tooling, baseline, and user decisions.
