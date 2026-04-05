#!/usr/bin/env python3
"""
Digi Command Center — Obsidian Sync
Syncs agent runs, logs, and metrics to Obsidian vault
Run as cron job every 30 min during agent hours, or in morning routine
"""

import subprocess
import json
from datetime import datetime, timedelta
from pathlib import Path

SUPABASE_URL = "https://ynyeuuxynwfzukvvxxlp.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InlueWV1dXh5bndmenVrdnZ4eGxwIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MjI1NjYyNCwiZXhwIjoyMDg3ODMyNjI0fQ.yK9zsYBlMco3ExSn8JlKZvrFIseFHHlMkF8g1fIyRqU"

# Obsidian paths
OBSIDIAN_PATH = Path.home() / "Library" / "Mobile Documents" / "iCloud~md~obsidian" / "Documents" / "Vault"
DIGI_PATH = OBSIDIAN_PATH / "Central Intel" / "Digi"
DAILY_PATH = OBSIDIAN_PATH / "📊 Active Org" / "Daily"

DIGI_PATH.mkdir(parents=True, exist_ok=True)
DAILY_PATH.mkdir(parents=True, exist_ok=True)

def query_supabase(query: str) -> list:
    """Execute SQL query against Supabase"""
    result = subprocess.run(
        [
            "curl", "-s", "-X", "POST",
            f"{SUPABASE_URL}/rest/v1/rpc/sql",
            "-H", f"Authorization: Bearer {SUPABASE_KEY}",
            "-H", "Content-Type: application/json",
            "-d", json.dumps({"query": query})
        ],
        capture_output=True,
        text=True,
        timeout=30
    )
    try:
        return json.loads(result.stdout) if result.stdout else []
    except:
        return []

def get_agent_runs(hours_back: int = 24) -> dict:
    """Get agent runs from last N hours"""
    cutoff = datetime.utcnow() - timedelta(hours=hours_back)
    
    query = f"""
    SELECT 
        r.id, r.job_id, r.status, r.progress_percent,
        r.started_at, r.completed_at, r.error_message,
        a.name, a.role
    FROM agent_runs r
    JOIN agents a ON r.agent_id = a.id
    WHERE r.created_at > '{cutoff.isoformat()}'
    ORDER BY r.created_at DESC
    """
    
    # Fallback: use REST API table query
    result = subprocess.run(
        [
            "curl", "-s",
            f"{SUPABASE_URL}/rest/v1/agent_runs?limit=100&order=created_at.desc",
            "-H", f"Authorization: Bearer {SUPABASE_KEY}",
            "-H", "apikey: " + SUPABASE_KEY
        ],
        capture_output=True,
        text=True,
        timeout=30
    )
    
    try:
        data = json.loads(result.stdout) if result.stdout else []
        # Filter to last N hours
        runs = []
        for run in data:
            if run.get('created_at'):
                created = datetime.fromisoformat(run['created_at'].replace('Z', '+00:00'))
                if created > cutoff:
                    runs.append(run)
        return {run['id']: run for run in runs}
    except:
        return {}

def get_agent_logs(run_ids: list) -> dict:
    """Get logs for specific runs"""
    if not run_ids:
        return {}
    
    # Query logs for these runs
    ids_str = ','.join([f"'{rid}'" for rid in run_ids])
    result = subprocess.run(
        [
            "curl", "-s",
            f"{SUPABASE_URL}/rest/v1/agent_logs?agent_run_id=in.({','.join(run_ids)})&limit=500",
            "-H", f"Authorization: Bearer {SUPABASE_KEY}",
            "-H", "apikey: " + SUPABASE_KEY
        ],
        capture_output=True,
        text=True,
        timeout=30
    )
    
    try:
        logs = json.loads(result.stdout) if result.stdout else []
        # Group by run_id
        grouped = {}
        for log in logs:
            run_id = log.get('agent_run_id')
            if run_id not in grouped:
                grouped[run_id] = []
            grouped[run_id].append(log)
        return grouped
    except:
        return {}

def get_agents() -> dict:
    """Get all agents"""
    result = subprocess.run(
        [
            "curl", "-s",
            f"{SUPABASE_URL}/rest/v1/agents?select=id,name,role",
            "-H", f"Authorization: Bearer {SUPABASE_KEY}",
            "-H", "apikey: " + SUPABASE_KEY
        ],
        capture_output=True,
        text=True,
        timeout=30
    )
    
    try:
        agents = json.loads(result.stdout) if result.stdout else []
        return {agent['id']: agent for agent in agents}
    except:
        return {}

def sync_digi_runs():
    """Sync agent runs to Obsidian"""
    print(f"\n{'='*64}")
    print(f"Digi Command Center Sync - {datetime.now().strftime('%H:%M:%S')}")
    print(f"{'='*64}\n")
    
    # Get runs from last 24 hours
    print("🤖 Fetching agent runs from Supabase...")
    runs = get_agent_runs(hours_back=24)
    agents = get_agents()
    
    if not runs:
        print("   No agent runs found in last 24 hours")
        return
    
    print(f"   Found {len(runs)} agent runs\n")
    
    # Get logs
    print("📝 Fetching agent logs...")
    logs = get_agent_logs(list(runs.keys()))
    print(f"   Found logs for {len(logs)} runs\n")
    
    # Create daily summary
    print("📊 Creating Digi summary for Daily.md...")
    today = datetime.now().strftime("%Y-%m-%d")
    daily_file = DAILY_PATH / f"{today}.md"
    
    # Read existing daily file
    if daily_file.exists():
        daily_content = daily_file.read_text()
    else:
        daily_content = f"# {today}\n\n"
    
    # Build Digi section
    digi_section = "\n## 🤖 Digi Agent Summary\n\n"
    
    # Status breakdown
    status_counts = {}
    for run in runs.values():
        status = run.get('status', 'unknown')
        status_counts[status] = status_counts.get(status, 0) + 1
    
    digi_section += "### Status\n"
    for status, count in status_counts.items():
        digi_section += f"- {status.capitalize()}: {count}\n"
    
    # Agent summary
    digi_section += "\n### Agents\n"
    agent_runs = {}
    for run in runs.values():
        agent_id = run.get('agent_id')
        if agent_id not in agent_runs:
            agent = agents.get(agent_id, {})
            agent_name = agent.get('name', 'Unknown')
            agent_role = agent.get('role', 'unknown')
            agent_runs[agent_id] = {
                'name': agent_name,
                'role': agent_role,
                'runs': []
            }
        agent_runs[agent_id]['runs'].append(run)
    
    for agent_id, agent_data in agent_runs.items():
        digi_section += f"\n#### {agent_data['name']} ({agent_data['role']})\n"
        for run in agent_data['runs'][:3]:  # Last 3 runs per agent
            status_icon = "✅" if run.get('status') == 'completed' else "❌" if run.get('status') == 'failed' else "🔄"
            started = run.get('started_at', 'N/A')[:10] if run.get('started_at') else 'N/A'
            digi_section += f"- {status_icon} {run.get('job_id')} ({started})\n"
    
    # Insert/update Digi section
    if "## 🤖 Digi Agent Summary" in daily_content:
        # Replace existing section
        parts = daily_content.split("## 🤖 Digi Agent Summary")
        before = parts[0]
        after = parts[1].split("##")[1:] if len(parts[1].split("##")) > 1 else []
        after_str = "##".join(after) if after else ""
        daily_content = before + digi_section + ("\n##" + after_str if after_str else "")
    else:
        # Append new section
        daily_content += digi_section
    
    daily_file.write_text(daily_content)
    print(f"   ✅ Updated Daily/{today}.md\n")
    
    # Create detailed run files
    print("📋 Creating detailed run logs...")
    for run_id, run in runs.items():
        agent = agents.get(run.get('agent_id'), {})
        agent_name = agent.get('name', 'Unknown')
        
        run_file = DIGI_PATH / f"{run.get('job_id')}.md"
        
        content = f"# {agent_name} Run\n"
        content += f"- **Job ID:** {run.get('job_id')}\n"
        content += f"- **Status:** {run.get('status')}\n"
        content += f"- **Started:** {run.get('started_at', 'N/A')}\n"
        content += f"- **Completed:** {run.get('completed_at', 'N/A')}\n"
        
        if run.get('error_message'):
            content += f"- **Error:** {run.get('error_message')}\n"
        
        content += f"\n## Logs\n"
        
        # Add run logs
        run_logs = logs.get(run_id, [])
        for log in run_logs:
            timestamp = log.get('created_at', '')[:19] if log.get('created_at') else 'N/A'
            level = log.get('level', 'info').upper()
            message = log.get('message', '')
            content += f"- [{timestamp}] **{level}:** {message}\n"
        
        run_file.write_text(content)
    
    print(f"   ✅ Created {len(runs)} detailed run logs\n")
    
    # Summary
    print(f"{'='*64}")
    print(f"✅ Sync Complete")
    print(f"{'='*64}")
    print(f"Daily summary: Daily/{today}.md")
    print(f"Run logs: {len(runs)} files in Digi/")
    print()

if __name__ == "__main__":
    sync_digi_runs()
