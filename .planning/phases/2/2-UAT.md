---
status: testing
phase: Classification Cascade + Novelty Detection
source: tillnow.md
started: 2026-04-08T14:43:00Z
updated: 2026-04-08T14:43:00Z
---

## Current Test
<!-- OVERWRITE each test - shows where we are -->

number: 1
name: Fast Path (High Confidence)
expected: |
  Submit a highly typical ticket (e.g. from the historical training set) via the Streamlit UI. The system routes without calling the LLM, and the UI displays a green badge reading "⚡ FAST PATH".
awaiting: user response

## Tests

### 1. Fast Path (High Confidence)
expected: |
  Submit a highly typical ticket (e.g. from the historical training set) via the Streamlit UI. The system routes without calling the LLM, and the UI displays a green badge reading "⚡ FAST PATH".
result: [pending]

### 2. LLM Judge (Medium Confidence)
expected: |
  Submit a moderately ambiguous ticket. The UI displays an amber badge reading "🧠 LLM JUDGE" and a callout box showing the LLM judge's rationale for the category switch.
result: [pending]

### 3. Escalated (Low Confidence)
expected: |
  Submit a vague/ambiguous ticket that lacks specific training precedence. The UI displays a red badge reading "🚨 ESCALATED" and doesn't invoke the LLM Judge.
result: [pending]

### 4. Novel Ticket Detection
expected: |
  Submit gibberish or a completely out-of-domain ticket (e.g., "Mow my lawn"). The UI displays a purple badge reading "🆕 NOVEL TICKET".
result: [pending]

## Summary

total: 4
passed: 0
issues: 0
pending: 4
skipped: 0

## Gaps

