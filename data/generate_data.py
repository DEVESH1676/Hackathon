import os
import sys
import pandas as pd
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

# Hack to load config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

PROMPT_TEMPLATE = """You are a Senior IT Service Desk Data Engineer at a Fortune 500 enterprise. Generate exactly 200 realistic IT support tickets in CSV format.

STRICT SCHEMA: ticket_id,title,description,category,resolution,priority,department

CATEGORY DISTRIBUTION:
- Infrastructure: 40 tickets (servers, VMs, storage)
- Application: 35 tickets (CRM crashes, microservice failures)
- Security: 30 tickets (phishing, MFA failures)
- Database: 35 tickets (query performance, replication lag)
- Network: 30 tickets (VPN drops, BGP flaps)
- Access Management: 30 tickets (AD group additions, SSO issues)

PRIORITY DISTRIBUTION: P1 (10%), P2 (25%), P3 (40%), P4 (25%)

ROUTING:
- Infrastructure -> Cloud Platform Engineering
- Application -> Application Support Team
- Security -> Security Operations Center (SOC)
- Database -> Database Administration (DBA)
- Network -> Network Operations Center (NOC)
- Access Management -> Identity & Access Management (IAM)

REALISM: Vary descriptions, include tools like ServiceNow, Jira. Format: 'TKT-2024-[random 5 digits]'
BATCH_SEED: {batch_seed}

Output ONLY the raw CSV text.
"""

def generate_batch(batch_seed, llm):
    """Generates a single batch of 200 synthetic tickets."""
    prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    chain = prompt | llm
    
    print(f"Generating batch {batch_seed}...")
    try:
        response = chain.invoke({"batch_seed": batch_seed})
        # Strip potential markdown codeblocks if they are returned by LLM
        content = response.content.strip()
        if content.startswith("```csv"):
            content = content[6:]
        if content.startswith("```"):
            content = content[3:]
        if content.endswith("```"):
            content = content[:-3]
        return content.strip()
    except Exception as e:
        print(f"Error generating batch: {e}")
        return ""

def main():
    print(f"Initializing Ollama LLM (Model: {config.OLLAMA_MODEL} at {config.OLLAMA_BASE_URL})...")
    from langchain_community.chat_models import ChatOllama
    
    llm = ChatOllama(
        base_url=config.OLLAMA_BASE_URL,
        model=config.OLLAMA_MODEL,
        temperature=0.7
    )
    
    all_csv_data = []
    
    # Generate 5 batches of 200 = 1000 tickets
    for i in range(1, 6):
        batch_csv = generate_batch(i, llm)
        if batch_csv:
            lines = batch_csv.split('\n')
            # Only keep header for the first batch
            if i == 1:
                all_csv_data.extend(lines)
            else:
                # skip header for subsequent batches
                all_csv_data.extend(lines[1:])
    
    output_path = os.path.join(os.path.dirname(__file__), 'synthetic_tickets.csv')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(all_csv_data))
    
    print(f"Data generated and saved to {output_path}")

if __name__ == "__main__":
    main()
