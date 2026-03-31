import os
import sys
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

PROMPT = """You are a Senior IT Service Desk Data Engineer at a Fortune 500 enterprise (50,000 employees, hybrid cloud infrastructure). Generate exactly 1000 realistic IT support tickets in CSV format.

STRICT SCHEMA (use these exact column headers):
ticket_id,title,description,category,resolution,priority,department

CATEGORY DISTRIBUTION (enforce exactly):
- Infrastructure: 200 tickets (servers, VMs, storage, cloud resources, DNS, load balancers, Kubernetes pods, CI/CD pipelines)
- Application: 175 tickets (CRM crashes, ERP errors, microservice failures, API timeouts, deployment rollbacks, memory leaks, log4j patches)
- Security: 150 tickets (phishing attempts, MFA failures, certificate expirations, SOC alerts, vulnerability scans, ransomware indicators, DLP violations)
- Database: 175 tickets (query performance, replication lag, deadlocks, backup failures, schema migrations, connection pool exhaustion, Oracle/PostgreSQL/MongoDB specific)
- Network: 150 tickets (VPN drops, firewall rule requests, VLAN misconfigs, BGP flaps, SD-WAN issues, packet loss, DNS resolution failures)
- Access Management: 150 tickets (AD group additions, RBAC role requests, service account creation, SSO issues, PAM vault access, offboarding access revocation, API key rotation)

PRIORITY DISTRIBUTION:
- P1 Critical: 10% (production down, security breach, data loss)
- P2 High: 25% (degraded service, security vulnerability, key system affected)
- P3 Medium: 40% (workaround exists, scheduled maintenance, standard requests)
- P4 Low: 25% (cosmetic issues, documentation, feature requests, training)

DEPARTMENT ROUTING:
- Infrastructure -> Cloud Platform Engineering
- Application -> Application Support Team
- Security -> Security Operations Center (SOC)
- Database -> Database Administration (DBA)
- Network -> Network Operations Center (NOC)
- Access Management -> Identity & Access Management (IAM)

CRITICAL REALISM RULES:
1. EVERY description MUST be 2-5 sentences long, written as a real employee would write. Some formal, some casual, ~10% with minor typos. Include real server names like PROD-APP-07, error codes like ORA-12541, HTTP 503, etc.
2. Include realistic enterprise tools: ServiceNow, Jira, Splunk, CrowdStrike, Okta, HashiCorp Vault, AWS Console, Azure AD, Terraform, Ansible.
3. Resolutions MUST be specific technical steps (NOT generic). Example: "Restarted Apache Tomcat service on PROD-APP-07 via Ansible playbook restart_tomcat.yml. Root cause: JVM heap exhaustion at 95% - increased from 4GB to 8GB in /opt/tomcat/bin/setenv.sh."
4. Include 15% ambiguous tickets where the category could reasonably be 2+ categories (e.g., "Cannot access database" could be Network, Database, or Access Management).
5. Include 10% recurring/pattern tickets (same root cause, different reporters).
6. Ticket IDs must be sequential: TKT-2024-00001 through TKT-2024-01000.
7. DO NOT get lazy with descriptions. Every single row must have a unique, detailed description. No "check" or "update request" placeholders.

Output ONLY the CSV data starting with the header row. No explanations, no markdown, no code blocks. Properly escape any commas in text fields using double quotes.
"""

TARGET_TICKETS = 1000

def print_progress(current, total, start_time, bar_width=40):
    """Print a live progress bar to terminal."""
    pct = current / total
    filled = int(bar_width * pct)
    bar = '█' * filled + '░' * (bar_width - filled)
    
    elapsed = time.time() - start_time
    if current > 0:
        eta = (elapsed / current) * (total - current)
        eta_str = f"{int(eta//60)}m {int(eta%60)}s"
    else:
        eta_str = "calculating..."
    
    rate = current / elapsed if elapsed > 0 else 0
    
    sys.stdout.write(f"\r  [{bar}] {current}/{total} tickets ({pct*100:.1f}%) | {rate:.1f} tickets/s | ETA: {eta_str}  ")
    sys.stdout.flush()

def main():
    print(f"╔══════════════════════════════════════════════════════╗")
    print(f"║  Synthetic Ticket Generator                        ║")
    print(f"║  Model: {config.OLLAMA_MODEL:<43}║")
    print(f"║  Host:  {config.OLLAMA_BASE_URL:<43}║")
    print(f"║  Target: {TARGET_TICKETS} tickets                              ║")
    print(f"╚══════════════════════════════════════════════════════╝")
    print()
    
    from langchain_community.chat_models import ChatOllama
    from langchain_core.messages import HumanMessage
    
    llm = ChatOllama(
        base_url=config.OLLAMA_BASE_URL,
        model=config.OLLAMA_MODEL,
        temperature=0.7,
        num_predict=65536,
    )
    
    output_path = os.path.join(os.path.dirname(__file__), 'synthetic_tickets.csv')
    
    print("[1/3] Sending prompt to Ollama... (waiting for first token)")
    start_time = time.time()
    
    # Use streaming to track progress in real-time
    collected_chunks = []
    ticket_count = 0
    header_seen = False
    
    try:
        for chunk in llm.stream([HumanMessage(content=PROMPT)]):
            text = chunk.content
            collected_chunks.append(text)
            
            # Count newlines = new CSV rows = new tickets
            newlines = text.count('\n')
            if newlines > 0:
                if not header_seen:
                    header_seen = True
                    ticket_count += (newlines - 1)  # first newline is after header
                else:
                    ticket_count += newlines
                
                if ticket_count > 0:
                    print_progress(min(ticket_count, TARGET_TICKETS), TARGET_TICKETS, start_time)
        
        print()  # newline after progress bar
        elapsed = time.time() - start_time
        print(f"\n[2/3] Stream complete in {int(elapsed//60)}m {int(elapsed%60)}s")
        
        # Join all chunks and clean
        content = ''.join(collected_chunks).strip()
        
        # Strip markdown code blocks if present
        if content.startswith("```csv"):
            content = content[6:]
        if content.startswith("```"):
            content = content[3:]
        if content.endswith("```"):
            content = content[:-3]
        content = content.strip()
        
        # Write to file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # Final validation
        lines = [l for l in content.split('\n') if l.strip()]
        actual_tickets = len(lines) - 1  # minus header
        
        print(f"\n[3/3] Validation:")
        print(f"  ✓ File saved: {output_path}")
        print(f"  ✓ Total lines: {len(lines)} (header + {actual_tickets} tickets)")
        
        if actual_tickets < TARGET_TICKETS:
            print(f"  ⚠ Warning: Got {actual_tickets}/{TARGET_TICKETS} tickets (model may have hit context limit)")
            print(f"    → {actual_tickets} tickets is still usable for the hackathon prototype")
        else:
            print(f"  ✓ Target reached: {actual_tickets}/{TARGET_TICKETS}")
        
        print(f"\n  Time: {int(elapsed//60)}m {int(elapsed%60)}s")
        print(f"  Rate: {actual_tickets/elapsed:.1f} tickets/second")
        print(f"\n{'='*55}")
        print(f"  DONE. Run `core/embeddings.py` next to ingest into ChromaDB.")
        print(f"{'='*55}")
        
    except Exception as e:
        print(f"\n\n✗ Error during generation: {e}")

if __name__ == "__main__":
    main()
