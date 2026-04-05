#!/usr/bin/env python3
"""
Digi Command Center — Telegram Alerts
Sends alerts to @operations_bolismedia on errors and completions
Integrates with logger.py to hook on run completion
"""

import subprocess
import json
from datetime import datetime
from pathlib import Path

SUPABASE_URL = "https://ynyeuuxynwfzukvvxxlp.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InlueWV1dXh5bndmenVrdnZ4eGxwIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MjI1NjYyNCwiZXhwIjoyMDg3ODMyNjI0fQ.yK9zsYBlMco3ExSn8JlKZvrFIseFHHlMkF8g1fIyRqU"

# Telegram settings
TELEGRAM_CHAT = "operations_bolismedia"  # Use Hermes native master-telegram MCP server
ALERTS_ENABLED = True
ERROR_ALERTS = True  # Alert on every error
COMPLETION_SUMMARIES = False  # Only detailed errors, not every completion

def send_telegram_alert(message: str, error: bool = False) -> bool:
    """Send alert to Telegram via Hermes MCP"""
    if not ALERTS_ENABLED:
        return False
    
    if error and not ERROR_ALERTS:
        return False
    
    try:
        # Use hermes MCP to send via master-telegram
        result = subprocess.run(
            [
                "hermes", "mcp", "send", "telegram",
                "--server", "master-telegram",
                "--chat", TELEGRAM_CHAT,
                "--text", message
            ],
            capture_output=True,
            text=True,
            timeout=10
        )
        return result.returncode == 0
    except Exception as e:
        print(f"Failed to send Telegram alert: {e}")
        return False

def alert_error(agent_name: str, job_id: str, error_message: str, run_id: str = None):
    """Alert on agent error"""
    message = f"""
🚨 **DIGI AGENT ERROR**

Agent: {agent_name}
Job ID: {job_id}
Status: Failed

Error: {error_message}

Time: {datetime.now().strftime('%H:%M:%S')}
"""
    
    if run_id:
        message += f"Run ID: {run_id}\n"
    
    print(f"📢 Sending error alert: {agent_name} ({job_id})")
    return send_telegram_alert(message.strip(), error=True)

def alert_completion(agent_name: str, job_id: str, duration: str = None, outputs: int = 0):
    """Alert on completion (optional, depends on config)"""
    if not COMPLETION_SUMMARIES:
        return False
    
    message = f"""
✅ **DIGI AGENT COMPLETED**

Agent: {agent_name}
Job ID: {job_id}

Time: {datetime.now().strftime('%H:%M:%S')}
"""
    
    if duration:
        message += f"Duration: {duration}\n"
    if outputs:
        message += f"Outputs: {outputs}\n"
    
    print(f"📢 Sending completion alert: {agent_name} ({job_id})")
    return send_telegram_alert(message.strip(), error=False)

def get_recent_errors(hours: int = 1) -> list:
    """Fetch recent error runs from Supabase"""
    result = subprocess.run(
        [
            "curl", "-s",
            f"{SUPABASE_URL}/rest/v1/agent_runs?status=eq.failed&order=created_at.desc&limit=20",
            "-H", f"Authorization: Bearer {SUPABASE_KEY}",
            "-H", "apikey: " + SUPABASE_KEY
        ],
        capture_output=True,
        text=True,
        timeout=30
    )
    
    try:
        return json.loads(result.stdout) if result.stdout else []
    except:
        return []

def check_and_alert_errors():
    """Check for recent errors and send alerts"""
    print(f"\n{'='*64}")
    print(f"Digi Alert Check - {datetime.now().strftime('%H:%M:%S')}")
    print(f"{'='*64}\n")
    
    errors = get_recent_errors(hours=1)
    
    if not errors:
        print("✅ No recent errors found")
        return
    
    print(f"⚠️  Found {len(errors)} recent errors, sending alerts...\n")
    
    for error_run in errors:
        agent_name = error_run.get('agent_id', 'Unknown')
        job_id = error_run.get('job_id', 'N/A')
        error_msg = error_run.get('error_message', 'Unknown error')
        run_id = error_run.get('id')
        
        alert_error(
            agent_name=agent_name,
            job_id=job_id,
            error_message=error_msg,
            run_id=run_id
        )
    
    print(f"\n{'='*64}")
    print(f"✅ Alert check complete")
    print(f"{'='*64}\n")

# Integration hook for logger.py
def on_run_completion(agent_name: str, job_id: str, status: str, duration: str = None, outputs: int = 0):
    """Called by logger.py when agent run completes"""
    if status == "failed":
        # Always alert on errors
        alert_error(agent_name, job_id, "Agent run failed", run_id=job_id)
    elif status == "completed" and COMPLETION_SUMMARIES:
        # Optional: alert on completion
        alert_completion(agent_name, job_id, duration, outputs)

if __name__ == "__main__":
    check_and_alert_errors()
