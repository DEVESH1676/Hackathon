import os
import sys
import pandas as pd

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

def main():
    print(f"Initializing Ollama LLM (Model: {config.OLLAMA_MODEL} at {config.OLLAMA_BASE_URL})...")
    from langchain_community.chat_models import ChatOllama
    from langchain_core.messages import HumanMessage
    
    llm = ChatOllama(
        base_url=config.OLLAMA_BASE_URL,
        model=config.OLLAMA_MODEL,
        temperature=0.7,
        num_predict=65536,  # Max output tokens - we need a LOT for 1000 rows
    )
    
    print("Generating 1000 tickets in a single call... This will take a while.")
    print("Model: qwen2.5-gpu (no thinking overhead)")
    
    try:
        response = llm.invoke([HumanMessage(content=PROMPT)])
        content = response.content.strip()
        
        # Strip markdown code blocks if present
        if content.startswith("```csv"):
            content = content[6:]
        if content.startswith("```"):
            content = content[3:]
        if content.endswith("```"):
            content = content[:-3]
        content = content.strip()
        
        output_path = os.path.join(os.path.dirname(__file__), 'synthetic_tickets.csv')
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # Quick validation
        lines = content.split('\n')
        non_empty = [l for l in lines if l.strip()]
        print(f"\nGeneration complete!")
        print(f"Total lines written: {len(non_empty)} (header + {len(non_empty)-1} tickets)")
        print(f"Saved to: {output_path}")
        
    except Exception as e:
        print(f"Error during generation: {e}")

if __name__ == "__main__":
    main()
