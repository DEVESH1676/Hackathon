"""
Standalone ticket generator - run on laptop.
Requirements: pip install langchain-community langchain-core
Usage: python generate_standalone.py
Output: synthetic_tickets.csv in same directory
"""
import os, sys, time

OLLAMA_BASE_URL = "http://localhost:11434"
CLOUD_MODEL = "deepseek-v3.2:cloud"

PROMPT_BATCH_1 = """Generate exactly 500 realistic IT support tickets as CSV. Output ONLY raw CSV, no explanations.

Header: ticket_id,title,description,category,resolution,priority,department,created_at

Categories (distribute evenly across 500):
- Infrastructure (100): servers, VMs, storage, K8s, CI/CD, DNS, load balancers
- Application (85): CRM crashes, API timeouts, microservice failures, memory leaks, deployment issues
- Security (75): phishing, MFA failures, cert expirations, vulnerability scans, ransomware, DLP
- Database (85): slow queries, replication lag, deadlocks, backup failures, connection pools, ORA errors
- Network (75): VPN drops, firewall rules, VLAN misconfigs, BGP flaps, packet loss, DNS failures
- Access Management (80): AD groups, RBAC, service accounts, SSO issues, PAM access, offboarding

Priority: P1 Critical(10%), P2 High(25%), P3 Medium(40%), P4 Low(25%)

Departments: Infrastructure->Cloud Platform Engineering, Application->Application Support Team, Security->Security Operations Center (SOC), Database->Database Administration (DBA), Network->Network Operations Center (NOC), Access Management->Identity & Access Management (IAM)

Rules:
- ticket_id: TKT-2024-00001 through TKT-2024-00500
- created_at: Random dates between 2024-01-01 and 2024-12-31 in YYYY-MM-DD HH:MM:SS format
- description: 2-4 real sentences. Use server names (PROD-APP-07), error codes (ORA-12541, HTTP 503), tool names (ServiceNow, Jira, Splunk, CrowdStrike, Okta, Terraform, Ansible, AWS, Azure AD)
- resolution: Specific technical steps with commands, file paths, tool names. NOT generic.
- ~10% descriptions should have minor typos like a real employee
- 15% should be ambiguous (could fit 2 categories)
- Wrap fields containing commas in double quotes

Output RAW CSV only. Start with header row. No markdown. No code blocks."""

PROMPT_BATCH_2 = """Generate exactly 500 realistic IT support tickets as CSV. Output ONLY raw CSV, no explanations.

Header: ticket_id,title,description,category,resolution,priority,department,created_at

Categories (distribute evenly across 500):
- Infrastructure (100): cloud migration, container orchestration, bare metal servers, hypervisor patching, CDN config, S3 storage issues
- Application (85): ERP module errors, SSO integration bugs, webhook failures, queue worker crashes, cache invalidation, log4j patches
- Security (75): SOC alerts, endpoint compromise, DDoS mitigation, SSL cert issues, insider threats, compliance violations
- Database (85): PostgreSQL vacuum, MongoDB sharding, schema migrations, index bloat, transaction locks, data corruption
- Network (75): SD-WAN issues, MPLS circuits, NTP sync, DHCP exhaustion, wireless interference, MTU mismatches
- Access Management (80): API key rotation, privileged access reviews, MFA enrollment, LDAP sync, conditional access policies, license compliance

Priority: P1 Critical(10%), P2 High(25%), P3 Medium(40%), P4 Low(25%)

Departments: Infrastructure->Cloud Platform Engineering, Application->Application Support Team, Security->Security Operations Center (SOC), Database->Database Administration (DBA), Network->Network Operations Center (NOC), Access Management->Identity & Access Management (IAM)

Rules:
- ticket_id: TKT-2024-00501 through TKT-2024-01000
- created_at: Random dates between 2024-01-01 and 2024-12-31 in YYYY-MM-DD HH:MM:SS format
- description: 2-4 real sentences. Use server names (PROD-DB-03, STG-WEB-12), error codes (PG::DeadlockDetected, ECONNREFUSED), tool names (Grafana, PagerDuty, Datadog, HashiCorp Vault, Kubernetes, Docker, Jenkins)
- resolution: Specific technical steps with commands, file paths, tool names. NOT generic.
- ~10% descriptions should have minor typos like a real employee
- 15% should be ambiguous (could fit 2 categories)
- Wrap fields containing commas in double quotes

Output RAW CSV only. Start with header row. No markdown. No code blocks."""

def clean_csv(content):
    content = content.strip()
    for prefix in ["```csv", "```"]:
        if content.startswith(prefix):
            content = content[len(prefix):]
    if content.endswith("```"):
        content = content[:-3]
    return content.strip()

def print_progress(current, total, start_time, batch_num, bar_width=40):
    pct = min(current / total, 1.0)
    filled = int(bar_width * pct)
    bar = '#' * filled + '-' * (bar_width - filled)
    elapsed = time.time() - start_time
    if current > 0:
        eta = (elapsed / current) * (total - current)
        eta_str = f"{int(eta//60)}m {int(eta%60)}s"
    else:
        eta_str = "..."
    rate = current / elapsed if elapsed > 0 else 0
    sys.stdout.write(f"\r  Batch {batch_num} [{bar}] {current}/{total} ({pct*100:.1f}%) | {rate:.1f} t/s | ETA: {eta_str}  ")
    sys.stdout.flush()

def generate_batch(llm, prompt, batch_num):
    from langchain_core.messages import HumanMessage
    print(f"\n{'='*55}")
    print(f"  BATCH {batch_num}: Generating 500 tickets...")
    print(f"{'='*55}")
    
    start_time = time.time()
    collected = []
    ticket_count = 0
    header_seen = False
    
    for chunk in llm.stream([HumanMessage(content=prompt)]):
        text = chunk.content
        collected.append(text)
        nl = text.count('\n')
        if nl > 0:
            if not header_seen:
                header_seen = True
                ticket_count += max(0, nl - 1)
            else:
                ticket_count += nl
            if ticket_count > 0:
                print_progress(min(ticket_count, 500), 500, start_time, batch_num)
    
    print()
    elapsed = time.time() - start_time
    content = clean_csv(''.join(collected))
    lines = [l for l in content.split('\n') if l.strip()]
    actual = len(lines) - 1
    print(f"  Done: {actual} tickets in {int(elapsed//60)}m {int(elapsed%60)}s")
    return content, actual

def main():
    print("Installing deps if needed...")
    try:
        from langchain_community.chat_models import ChatOllama
    except ImportError:
        os.system("pip install langchain-community langchain-core")
        from langchain_community.chat_models import ChatOllama
    
    print(f"Connecting to Ollama at {OLLAMA_BASE_URL} with model {CLOUD_MODEL}")
    llm = ChatOllama(base_url=OLLAMA_BASE_URL, model=CLOUD_MODEL, temperature=0.7, num_predict=65536)
    
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'synthetic_tickets.csv')
    
    csv_1, c1 = generate_batch(llm, PROMPT_BATCH_1, 1)
    with open(out, 'w', encoding='utf-8') as f:
        f.write(csv_1)
    print(f"  Saved batch 1 ({c1} tickets)")
    
    try:
        csv_2, c2 = generate_batch(llm, PROMPT_BATCH_2, 2)
        lines_1 = csv_1.split('\n')
        lines_2 = csv_2.split('\n')
        merged = '\n'.join(lines_1 + lines_2[1:])
        with open(out, 'w', encoding='utf-8') as f:
            f.write(merged)
        print(f"\n  TOTAL: {c1+c2} tickets saved to {out}")
    except Exception as e:
        print(f"\n  Batch 2 failed: {e}. Batch 1 ({c1} tickets) still saved.")

if __name__ == "__main__":
    main()
