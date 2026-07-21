# FlowVerse Review Checklist

## V1 and Evidence

- [ ] Work treats V1 as the first implementation; earlier direction-document provenance creates no legacy runtime, migration, redesign, or compatibility obligation.
- [ ] V1 package intake is APPROVED for the active bootstrap or implementation slice.
- [ ] Task-relevant target/runtime stack, version, command, asset, API, and applicable budget facts satisfy the matching readiness gate with exact evidence.
- [ ] No assumption, example, unavailable check, or diagnostic result is reported as project fact or success.

## Product

- [ ] The work home exposes the shared Bot and deterministic task entry points together; Bot failure does not block structured work.
- [ ] Candidate, formal content, memory, external facts, feedback, analysis, and human decision remain distinct and traceable.
- [ ] Actual-release confirmation and Cycle creation are atomic, one task has at most one active Cycle, and only a human decision normally closes a valid Cycle.
- [ ] AI and administrators never silently confirm user business facts.
- [ ] Agent execution is read-only and does not expose free Agent creation, Prompt editing, arbitrary wiring, custom DAGs, or a general Workflow Builder.
- [ ] Product copy makes no automated-publishing, growth, causality, income, or market-validation promise.

## UI

- [ ] The palette follows ../uiux/DESIGN_TOKENS.md and body text is not pure black.
- [ ] The interface remains calm and readable during long sessions.
- [ ] Cards, effects, metrics, and panels are restrained.
- [ ] Layouts at 1440 × 900 and 1280 × 720 preserve formal state, evidence, manuscript usability, and the primary action.
- [ ] At 390 × 844, approved content remains readable while prohibited complex/business actions are disabled with an explanation.
- [ ] Keyboard navigation, focus, contrast, labels, and reduced motion are verified.

## Interaction and Copy

- [ ] Every page identifies task/Cycle/object/version/authority context, semantic state, next action, impact, and recovery.
- [ ] Each page state has one primary CTA.
- [ ] Bot replies and action cards are distinct; text alone changes no business state and cards revalidate before action.
- [ ] Formal commands show current scope/version/impact, reject duplicate or stale submission, preserve input on failure, and wait for authoritative success.
- [ ] Observation, AI analysis candidate, recommendation, and human decision use distinct labels.
- [ ] User-facing copy avoids implementation jargon from ../uiux/COPY_RULES.md.
- [ ] Loading, empty, error, recovery, disabled, and unsaved states are covered where applicable.

## Engineering

- [ ] The diff contains no unrelated edits or accidental generated files.
- [ ] No unapproved dependency, backend contract, schema, auth, or runtime change exists.
- [ ] Components and tokens are reused instead of duplicated.
- [ ] Focused tests cover changed behavior, or N/A / unavailable is recorded with a reason.
- [ ] Repository-defined lint, build, typecheck, and tests pass, or missing checks are explicitly recorded.
- [ ] The implementation is mapped to every applicable acceptance criterion.

## Architecture and Evolution

- [ ] Every changed production file belongs to a Confirmed target module/owner; affected architecture rows have Confirmed implementation conformance at completion.
- [ ] New dependencies follow Confirmed directions; production architecture checks show no cycles.
- [ ] Cross-module work uses public contracts with no private deep import or cross-owner storage/state access.
- [ ] Mutable data, drafts, caches, and server state retain one authoritative owner.
- [ ] No shared/utils dumping ground, god component/store/service, hidden global state, or service locator is added or enlarged.
- [ ] Every abstraction/extension point has a real consumer, approved implementation/phase, or confirmed external boundary.
- [ ] Contract consumers, compatibility, release order, migration, and rollback/forward recovery are verified or N/A.
- [ ] Applicable unit, contract, integration, architecture, failure, and E2E tests pass.
- [ ] Required ADR, architecture baseline, decision log, and technical-debt entries are updated.
- [ ] TODO/FIXME/HACK and temporary flag/shim/dual path reference active, location-matching, non-expired debt IDs; Resolved/Superseded rows have no live references.

## Performance

- [ ] Affected scenarios use the Confirmed production build, environment, command, data scale, and cache state; unaffected work records N/A with reason.
- [ ] Same-condition baseline, after-results, raw repetitions, and deltas are recorded for performance-sensitive changes.
- [ ] Applicable Confirmed Lab budgets due at the current gate pass; Field SLOs use Confirmed post-release data or PendingFieldData.
- [ ] Bundle, Long Tasks, input/IME, approved persistence/streaming, memory, and long-session risks are checked where affected.
- [ ] Applicable data, DOM, cache, history, and AI context have Confirmed performance/resource bounds.
- [ ] Supersedable requests, streams, polling, timers, and workers are cancelled and cleaned up, or a documented fallback protects against stale results.
- [ ] Budgets were not relaxed and unavailable measurements are marked Unverified.

## Reliability

- [ ] At the current gate, every affected reliability/recovery/control row has Applicability classified; Required targets are Confirmed and verification is Passed.
- [ ] RTO/RPO rows are keyed to recoverable data sets/classes with restore and integrity evidence.
- [ ] Remote/background boundaries have finite lifecycles and Confirmed deadline/cancellation or stale-result behavior.
- [ ] Retry handles only transient failures, has one owner, finite attempts/deadline, no tight loop, and Confirmed side-effect idempotency/dedup semantics.
- [ ] Degradation is explicit and observable, with no fake success, silent loss, permission bypass, or integrity reduction.
- [ ] Queues, pools, backlog, concurrency, fan-out, and shared resources have Confirmed bounds/backpressure where applicable.
- [ ] Liveness, readiness, and startup semantics are distinct where applicable; checks avoid restart storms and are lightweight, bounded, non-destructive, and safe.
- [ ] Logs/metrics/traces support critical diagnosis without secrets, unauthorized personal data, or unbounded labels.
- [ ] Required backup/restore, compatibility, rollout/recovery, and failure tests have measured evidence.
- [ ] Unavailable reliability or recovery evidence is Unverified, never Passed.

## Final Report

- [ ] Changed files and user-visible behavior are summarized.
- [ ] Commands, results, manual checks, and visual evidence are listed.
- [ ] Remaining risks, assumptions, and follow-up work are explicit.
