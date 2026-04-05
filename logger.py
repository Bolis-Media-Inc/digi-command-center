#!/usr/bin/env python3
"""
Digi Command Center — Structured Logging Integration
Logs to: Supabase (real-time) + Obsidian (searchable) + JSON (backup)
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any
from uuid import UUID

try:
    from supabase import create_client, Client
except ImportError:
    print("⚠️  supabase-py not installed. Install: pip install supabase")
    Client = None

# Optional: Telegram alerts on completion
try:
    from digi_telegram_alerts import on_run_completion
    TELEGRAM_ALERTS_AVAILABLE = True
except ImportError:
    TELEGRAM_ALERTS_AVAILABLE = False


class DigiLogger:
    """Structured logger for Digi agents with multi-destination support."""

    def __init__(
        self,
        agent_name: str,
        agent_id: str,
        job_id: str,
        supabase_url: Optional[str] = None,
        supabase_key: Optional[str] = None,
        obsidian_vault: Optional[str] = None,
    ):
        """
        Initialize logger.
        
        Args:
            agent_name: Human-readable agent name (e.g., "Scout")
            agent_id: Unique agent ID (e.g., "sourcer")
            job_id: Cron job ID
            supabase_url: Supabase project URL (env: SUPABASE_URL)
            supabase_key: Supabase service key (env: SUPABASE_KEY)
            obsidian_vault: Path to Obsidian vault root (env: OBSIDIAN_VAULT)
        """
        self.agent_name = agent_name
        self.agent_id = agent_id
        self.job_id = job_id
        self.run_id = None
        self.started_at = datetime.utcnow()

        # Supabase
        self.supabase_url = supabase_url or os.getenv("SUPABASE_URL")
        self.supabase_key = supabase_key or os.getenv("SUPABASE_KEY")
        self.supabase: Optional[Client] = None
        if self.supabase_url and self.supabase_key:
            try:
                self.supabase = create_client(self.supabase_url, self.supabase_key)
            except Exception as e:
                print(f"⚠️  Supabase connection failed: {e}")

        # Obsidian
        self.obsidian_vault = obsidian_vault or os.getenv("OBSIDIAN_VAULT")
        self.obsidian_log_path: Optional[Path] = None
        if self.obsidian_vault:
            vault_root = Path(self.obsidian_vault)
            digi_dir = vault_root / "Digi" / "agent_runs"
            digi_dir.mkdir(parents=True, exist_ok=True)
            self.obsidian_log_path = digi_dir / f"{self.job_id}.md"

        # Local JSON
        self.json_log_dir = Path(os.getenv("HOME", ".")) / ".hermes" / "digi-logs"
        self.json_log_dir.mkdir(parents=True, exist_ok=True)
        self.json_log_path = self.json_log_dir / f"{self.job_id}.jsonl"

    def start_run(self) -> str:
        """Initialize a new agent run. Returns run_id."""
        if self.supabase:
            try:
                # First, look up agent_id by role
                agent_result = self.supabase.table("agents").select("id").eq("role", self.agent_id).limit(1).execute()
                if agent_result.data:
                    agent_uuid = agent_result.data[0]["id"]
                    # Create agent_runs entry
                    result = self.supabase.table("agent_runs").insert({
                        "agent_id": agent_uuid,
                        "job_id": self.job_id,
                        "status": "running",
                        "progress_percent": 0,
                        "started_at": self.started_at.isoformat(),
                    }).execute()
                    self.run_id = result.data[0]["id"] if result.data else None
                else:
                    print(f"⚠️  Agent role '{self.agent_id}' not found in database")
            except Exception as e:
                print(f"⚠️  Failed to create run in Supabase: {e}")

        # Obsidian header
        if self.obsidian_log_path:
            header = f"""# {self.agent_name} Run
- **Job ID:** {self.job_id}
- **Started:** {self.started_at.isoformat()}
- **Status:** Running

## Logs
"""
            self.obsidian_log_path.write_text(header)

        return self.run_id or self.job_id

    def log(
        self,
        message: str,
        level: str = "info",
        metadata: Optional[Dict[str, Any]] = None,
    ):
        """Log a message to all destinations."""
        timestamp = datetime.utcnow().isoformat()

        # Supabase
        if self.supabase and self.run_id:
            try:
                self.supabase.table("agent_logs").insert({
                    "agent_run_id": self.run_id,
                    "level": level,
                    "message": message,
                    "metadata": metadata or {},
                    "created_at": timestamp,
                }).execute()
            except Exception as e:
                print(f"⚠️  Failed to log to Supabase: {e}")

        # Obsidian
        if self.obsidian_log_path:
            try:
                log_entry = f"- [{timestamp}] **{level.upper()}:** {message}\n"
                if metadata:
                    log_entry += f"  - Metadata: {json.dumps(metadata)}\n"
                with open(self.obsidian_log_path, "a") as f:
                    f.write(log_entry)
            except Exception as e:
                print(f"⚠️  Failed to write to Obsidian: {e}")

        # Local JSON
        try:
            log_entry = {
                "timestamp": timestamp,
                "agent_name": self.agent_name,
                "job_id": self.job_id,
                "run_id": self.run_id or self.job_id,
                "level": level,
                "message": message,
                "metadata": metadata or {},
            }
            with open(self.json_log_path, "a") as f:
                f.write(json.dumps(log_entry) + "\n")
        except Exception as e:
            print(f"⚠️  Failed to write to JSON log: {e}")

        # Console (for debugging)
        console_msg = f"[{level.upper()}] {self.agent_name}: {message}"
        print(console_msg)

    def milestone(self, message: str, metadata: Optional[Dict[str, Any]] = None):
        """Log a milestone event."""
        self.log(message, level="milestone", metadata=metadata)

    def error(self, message: str, metadata: Optional[Dict[str, Any]] = None):
        """Log an error."""
        self.log(message, level="error", metadata=metadata)

    def warning(self, message: str, metadata: Optional[Dict[str, Any]] = None):
        """Log a warning."""
        self.log(message, level="warning", metadata=metadata)

    def debug(self, message: str, metadata: Optional[Dict[str, Any]] = None):
        """Log debug info."""
        self.log(message, level="debug", metadata=metadata)

    def set_progress(self, percent: int):
        """Update progress percentage."""
        if self.supabase and self.run_id:
            try:
                self.supabase.table("agent_runs").update({
                    "progress_percent": min(100, max(0, percent)),
                }).eq("id", self.run_id).execute()
            except Exception as e:
                print(f"⚠️  Failed to update progress: {e}")

    def add_output(
        self,
        output_type: str,
        content: str,
        title: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        """Add a deliverable output."""
        if self.supabase and self.run_id:
            try:
                self.supabase.table("agent_outputs").insert({
                    "agent_run_id": self.run_id,
                    "output_type": output_type,
                    "title": title,
                    "content": content,
                    "metadata": metadata or {},
                }).execute()
            except Exception as e:
                print(f"⚠️  Failed to add output: {e}")

        self.log(f"Output added: {output_type}", level="milestone", metadata={"type": output_type})

    def complete(self, status: str = "completed", error_message: Optional[str] = None):
        """Mark run as complete."""
        completed_at = datetime.utcnow().isoformat()

        if self.supabase and self.run_id:
            try:
                update_data = {
                    "status": status,
                    "completed_at": completed_at,
                    "progress_percent": 100 if status == "completed" else 0,
                }
                if error_message:
                    update_data["error_message"] = error_message
                self.supabase.table("agent_runs").update(update_data).eq("id", self.run_id).execute()
            except Exception as e:
                print(f"⚠️  Failed to complete run: {e}")

        # Update Obsidian
        if self.obsidian_log_path:
            try:
                content = self.obsidian_log_path.read_text()
                content = content.replace(
                    "- **Status:** Running",
                    f"- **Status:** {status.capitalize()}\n- **Completed:** {completed_at}"
                )
                self.obsidian_log_path.write_text(content)
            except Exception as e:
                print(f"⚠️  Failed to update Obsidian: {e}")

        self.log(f"Run {status}: {error_message or 'Success'}", level="milestone")
        
        # Send Telegram alert on errors
        if TELEGRAM_ALERTS_AVAILABLE and status == "failed":
            try:
                duration = (datetime.utcnow() - self.started_at).total_seconds() / 60  # minutes
                on_run_completion(
                    agent_name=self.agent_name,
                    job_id=self.job_id,
                    status=status,
                    duration=f"{duration:.1f}m",
                )
            except Exception as e:
                print(f"⚠️  Failed to send Telegram alert: {e}")


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    # Example: Scout agent run
    logger = DigiLogger(
        agent_name="Scout",
        agent_id="sourcer",
        job_id="test-sourcer-001",
        supabase_url=os.getenv("SUPABASE_URL"),
        supabase_key=os.getenv("SUPABASE_KEY"),
        obsidian_vault=os.getenv("OBSIDIAN_VAULT"),
    )

    logger.start_run()
    logger.log("Initializing Scout agent")
    logger.log("Scanning Instagram feeds", level="info")
    logger.set_progress(25)

    logger.milestone("Found 5 trending posts", metadata={"count": 5})
    logger.set_progress(50)

    logger.log("Filtering for quality", level="info")
    logger.set_progress(75)

    logger.add_output(
        output_type="analysis",
        content="Top 5 posts with metadata",
        title="Scout Output",
        metadata={"source": "instagram", "count": 5}
    )

    logger.complete("completed")
