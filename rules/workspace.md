---
trigger: always_on
description: "Master protocol for workspace interaction, including file, folder, and command verification."
---

## Collaborative Workspace and Execution Protocol

To ensure seamless collaboration and prevent errors, you must treat the workspace as a dynamic environment and verify all actions before execution.

### 1. Collaborative Workspace Awareness (The "Why")

This project is worked on by **multiple agents concurrently**. The file structure can change between sessions without your knowledge. Never assume anything exists—always verify. Failing to do so can lead to working with outdated information, overwriting another agent's work, or executing invalid commands.

### 2. File and Folder Verification (The "How")

Before ANY file operation (read, write, edit, delete), you **MUST** verify the state of the filesystem.

*   **Check Directory Contents:**
    ```bash
    # Get a quick overview of a directory
    ls -la /path/to/dir/
    # Get a recursive view of a directory
    ls -laR /path/to/dir/
    ```

*   **Verify Existence Before Acting:**
    ```bash
    # Check if a directory exists
    test -d /path/to/dir && echo "EXISTS" || echo "MISSING"
    # Check if a file exists
    test -f /path/to/file && echo "EXISTS" || echo "MISSING"
    ```

*   **Project Path Conventions:**
    *   Project Root: `/home/devesh/pihacking/1pass/`
    *   Working Directory: `/home/devesh/pihacking/1pass/1pass/`
    *   Recon Outputs: `/home/devesh/pihacking/1pass/1pass/recon/`
    *   Credentials: `/home/devesh/pihacking/1pass/1pass/creds/`
    *   Tools: `/home/devesh/pihacking/1pass/1pass/tools/`

### 3. Command Execution Protocol

Before running any command, you **MUST** perform these checks:

*   **Verify Tool Installation:**
    ```bash
    which <tool_name> && <tool_name> --version
    ```
*   **Ensure Output Directories Exist:**
    ```bash
    test -d /path/for/output || mkdir -p /path/for/output
    ```

After running a command that creates a file, you **MUST** verify its creation:
```bash
# Example
some_command > expected_output.txt
test -f expected_output.txt && echo "SUCCESS" || echo "FAILED"
```

### 4. Error Handling

If a file or directory is missing when it should exist:
1.  Document the missing path in `tillnow.md`.
2.  Note the impact on the current phase.
3.  Suggest recovery steps or request user intervention.
