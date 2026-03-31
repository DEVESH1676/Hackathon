---
trigger: always_on
---

# Phase-Driven Development Protocol

## Work in Phases - No Skipping

Work **strictly** in phases as defined in `implementation_plan.md`:

```
Phase 0: Intelligence Gathering (Passive)
  └─ 0.1: White Paper Deep Dive
  └─ 0.2: OSINT & Subdomain Enumeration
  └─ 0.3: Prior Vulnerability Research

Phase 1: Account Setup & Environment Prep
  └─ 1.1: Create Trial Account
  └─ 1.2: Install All Clients (CLI, Extension)
  └─ 1.3: Configure Interception Proxy
  └─ 1.4: Install Session Analyzer

Phase 2: Active Reconnaissance
  └─ 2.1: Web App Fingerprinting
  └─ 2.2: Events API Reconnaissance
  └─ 2.3: API Endpoint Mapping
  └─ 2.4: JavaScript Analysis
  └─ 2.5: API Fuzzing
  └─ 2.6: Secret Scanning

Phase 3: Threat Modeling
Phase 4: Events API Deep Dive
Phase 5: Web App Security Testing
Phase 6: CLI Reverse Engineering
Phase 7: Browser Extension Analysis
Phase 8: Cryptographic Analysis
Phase 9: Business Logic Testing
Phase 10: Exploitation & Report
```

## Phase Completion Checklist

Before marking a phase COMPLETE:
- [ ] All steps in implementation_plan.md are done
- [ ] All output files created in `1pass/recon/`
- [ ] `tillnow.md` updated with completion status
- [ ] Wrong assumptions documented
- [ ] Next phase steps noted

## Blockers Protocol

If blocked:
1. Document in `tillnow.md` under "Next Steps"
2. List what user needs to provide
3. Note alternative approach for once unblocked

## Never Skip Documentation

Even failed attempts must be documented:
- What was attempted
- Why it failed
- What to try next

**"No documentation = no progress tracking = phase never completes."**

---
### **Changelog**
- **2026-03-28:** Reviewed the file and confirmed its content is well-structured and aligns with the project's needs. No changes to the protocol were made, but this changelog was added to maintain a consistent format across all rule files.
