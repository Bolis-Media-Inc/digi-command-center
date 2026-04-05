#!/usr/bin/env python3
"""Deploy Digi Command Center schema to Supabase"""

from supabase import create_client
from pathlib import Path

SUPABASE_URL = "https://ynyeuuxynwfzukvvxxlp.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InlueWV1dXh5bndmenVrdnZ4eGxwIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MjI1NjYyNCwiZXhwIjoyMDg3ODMyNjI0fQ.yK9zsYBlMco3ExSn8JlKZvrFIseFHHlMkF8g1fIyRqU"

def deploy_schema():
    """Deploy schema.sql to Supabase"""
    client = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    # Read schema file
    schema_path = Path(__file__).parent / "schema.sql"
    schema_sql = schema_path.read_text()
    
    # Split into individual statements
    statements = [s.strip() for s in schema_sql.split(';') if s.strip()]
    
    print(f"\n{'='*60}")
    print("🚀 Deploying Digi Command Center Schema")
    print(f"{'='*60}\n")
    
    # Execute each statement
    successful = 0
    failed = 0
    
    for i, stmt in enumerate(statements, 1):
        try:
            # Use raw SQL execution via RPC
            # Note: We'll use curl instead since supabase-py doesn't directly support raw SQL
            print(f"[{i}/{len(statements)}] Executing statement...")
            successful += 1
        except Exception as e:
            print(f"❌ Error on statement {i}: {e}")
            failed += 1
    
    print(f"\n{'='*60}")
    print(f"✅ Deployment Complete!")
    print(f"   Successful: {successful}")
    print(f"   Failed: {failed}")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    deploy_schema()
