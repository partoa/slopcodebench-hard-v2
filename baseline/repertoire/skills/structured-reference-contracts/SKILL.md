---
name: structured-reference-contracts
description: Construct, interpret, compose, or validate references such as resource names, URIs, paths, pointers, selectors, or source locations when identity, resolution context, or location specificity matters to a consumer.
---

# Preserve reference meaning and resolution

A reference has a target, a representation, and rules for interpreting it in a context. A plausible-looking string does not establish that it identifies the intended thing. References can identify one target, a collection, a query result or an unresolved target; do not assume uniqueness.

## Determine the contract

Identify what the consumer needs to locate or distinguish, its scope, the reference language, and the required granularity. Establish whether names, positions, labels, identities or matching rules determine the target. Determine whether a reference is absolute, relative or context-dependent under the applicable contract.

Use the actual reference system's grammar and rules. URIs, filesystem paths, JSON reference systems and CSS selectors are not interchangeable. Do not transfer delimiters, escaping, normalization or uniqueness assumptions between them. Consult applicable authoritative documentation when those rules are unfamiliar.

## Construct from structure

Carry semantic components and provenance through processing rather than reconstructing a target from an incomplete message at the end. Preserve the context needed to compose or resolve nested references. Use suitable parsers or builders when their guarantees match the task; an elaborate abstraction is not required for a simple known grammar.

Distinguish a container from one member, a label from an identity, and a position from a stable identifier. Choose among them according to the consumer obligation and governing syntax. More detail is not automatically better: expose the specificity needed to fulfill the responsibility, subject to privacy, authority and compatibility constraints.

## Check meaning at the resolution boundary

Where meaningful, verify that the produced reference resolves or matches the intended target in the declared context. For missing or deliberately unresolved targets, verify the contractually required interpretation and response instead. Check the expected cardinality rather than assuming that matching at least one target is sufficient.

Consider relevant contrasting conditions: nesting, similarly named neighbors, empty names, separator-like characters, case distinctions, Unicode, relative contexts, moved or renamed entities, and absent or multiple matches. Select cases from the actual grammar and use, not a universal requirement to support every possible naming convention.

Check both encoding/decoding and intended identity where applicable. A round trip can preserve the wrong reference; equality of strings alone does not establish the right target. Conversely, two differently represented references need not identify different things if the contract makes them equivalent.

Track source versus transformed locations when normalization or execution changes the structure. Verify each public path through the system that owes a location, rather than assuming a correct formatter will be reached everywhere. Keep exact required representations separate from provisional choices about granularity.
