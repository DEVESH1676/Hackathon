---
trigger: always_on
description: "Master protocol for documenting progress in tillnow.md and managing files."
---

## Progress Reporting and File Management Protocol

This protocol governs how you document your work in `tillnow.md` and how you manage files and tool outputs. Adhering to this is critical for project tracking and collaboration.

### 1. Read the Implementation Plan First

Before working on any phase, you **MUST** read the `/home/devesh/pihacking/1pass/implementation_plan.md` file to understand:
1.  **Phase requirements:** What tasks must be completed.
2.  **Expected outputs:** What files should be created.
3.  **Next phase triggers:** What signals a move to the next phase.

### 2. `tillnow.md` Update Structure

At the conclusion of every significant action or phase, you **MUST** update the `tillnow.md` file. Each phase section must follow this structure:

```markdown
## Phase X: [Phase Name]
**Status:** [COMPLETE | IN PROGRESS | BLOCKED]

**What We Did Now:**
- [Specific task 1] - [Details of what was done.]
- [Specific task 2] - [Details of what was done.]

**Wrong Assumptions Corrected:**
- [Initial Assumption] - [Correction and what was learned.]

**Next Steps:**
- [Detailed plan for the next action.]

**Files Created/Modified:**
- `/path/to/file1` - [Purpose of the file.]
- `/path/to/file2` - [Purpose of the file.]
```

### 3. Blockers Documentation

If you are **BLOCKED**, you must clearly document it in the "Next Steps" section of `tillnow.md`:
1.  **What's blocked:** The specific task you cannot proceed with.
2.  **Why it's blocked:** The missing dependency, tool, or information.
3.  **What you are waiting for:** The specific input needed from the user.
4.  **Alternative approach:** A potential path forward once unblocked.

### 4. Tool Output Management

*   **Save All Outputs:** For every tool you run, you **MUST** save its full, raw output to a file in the `1pass/recon/` directory.
    *   *Example:* `whatweb "https://example.com" > 1pass/recon/whatweb_output.txt`
*   **Use Descriptive Filenames:** Filenames must be clear and include the tool and target.
    *   *Good:* `whatweb_events.1password.com.txt`
    *   *Bad:* `output.txt`

### 5. File Deletion Protocol

*   **Do Not Delete Files:** As a general rule, you should **NEVER** delete files, especially output logs and evidence.
*   **Deletion is Allowed ONLY if:**
    1.  The file is a temporary artifact that is no longer needed.
    2.  You have explicit permission from the user to delete the file.

### 6. Phase Completion Criteria

A phase is considered **COMPLETE** only when:
- All steps for that phase in `implementation_plan.md` are done.
- All expected output files have been created and saved.
- `tillnow.md` is fully updated with the completion status and all required sections.
- The next phase is clearly noted in the "Next Steps" section.

---
### **Changelog**
- **2026-03-28:** Created this master progress protocol by merging `till.md` and `phase-progress.md`. This new file provides a single, comprehensive guide for documenting work and managing files.
