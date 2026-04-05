#!/bin/bash
# Digi Phase 3 Verification Script
# Checks that all Phase 3 components are in place and working

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║          Digi Command Center — Phase 3 Verification           ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

CHECKS_PASSED=0
CHECKS_TOTAL=0

check() {
    CHECKS_TOTAL=$((CHECKS_TOTAL + 1))
    if eval "$1"; then
        echo -e "${GREEN}✅${NC} $2"
        CHECKS_PASSED=$((CHECKS_PASSED + 1))
    else
        echo -e "${RED}❌${NC} $2"
    fi
}

warn() {
    echo -e "${YELLOW}⚠️${NC} $1"
}

# Phase 3.1: Obsidian Sync
echo ""
echo "📊 Phase 3.1: Obsidian Sync"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

check "[ -f ~/.hermes/digi-command-center/digi_obsidian_sync.py ]" \
    "digi_obsidian_sync.py exists"

check "grep -q 'digi_obsidian_sync.py' ~/sync_supabase.sh" \
    "Obsidian sync integrated in morning cron"

check "[ -f ~/sync_supabase.sh ]" \
    "Morning sync script exists"

check "crontab -l 2>/dev/null | grep -q 'sync_supabase.sh'" \
    "Morning sync scheduled in cron (7 AM)"

# Phase 3.2: Telegram Alerts
echo ""
echo "📱 Phase 3.2: Telegram Alerts"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

check "[ -f ~/.hermes/digi-command-center/digi_telegram_alerts.py ]" \
    "digi_telegram_alerts.py exists"

check "grep -q 'from digi_telegram_alerts import' ~/.hermes/digi-command-center/logger.py" \
    "Telegram alerts imported in logger.py"

check "grep -q 'on_run_completion' ~/.hermes/digi-command-center/logger.py" \
    "Telegram alerts hooked in logger.complete()"

# Phase 3.3: Railway Deployment
echo ""
echo "🚀 Phase 3.3: Railway Deployment"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

check "[ -f ~/.hermes/digi-command-center/RAILWAY_DEPLOY.md ]" \
    "RAILWAY_DEPLOY.md guide exists"

check "[ -f ~/.hermes/digi-command-center/dashboard/package.json ]" \
    "Dashboard package.json exists (ready for Railway)"

check "[ -f ~/.hermes/digi-command-center/dashboard/next.config.js ]" \
    "Dashboard next.config.js exists"

# Documentation
echo ""
echo "📚 Documentation"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

check "[ -f ~/.hermes/digi-command-center/PHASE_3_COMPLETE.md ]" \
    "PHASE_3_COMPLETE.md summary exists"

check "[ -f ~/.hermes/digi-command-center/INDEX.md ]" \
    "INDEX.md navigation guide exists"

# Environment
echo ""
echo "⚙️  Environment"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

check "[ -f ~/.hermes/digi-command-center/.env.local ]" \
    ".env.local configuration exists"

check "grep -q 'SUPABASE_URL' ~/.hermes/digi-command-center/.env.local" \
    "SUPABASE_URL configured in .env.local"

check "grep -q 'SUPABASE_KEY' ~/.hermes/digi-command-center/.env.local" \
    "SUPABASE_KEY configured in .env.local"

# Supabase Connection
echo ""
echo "🗄️  Supabase Connection"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

SUPABASE_URL=$(grep SUPABASE_URL ~/.hermes/digi-command-center/.env.local | cut -d'=' -f2)
if [ ! -z "$SUPABASE_URL" ]; then
    if curl -s "$SUPABASE_URL/rest/v1/" -H "apikey: test" > /dev/null 2>&1; then
        echo -e "${GREEN}✅${NC} Supabase API accessible"
        CHECKS_PASSED=$((CHECKS_PASSED + 1))
    else
        warn "Supabase API not responding (might be blocked by firewall)"
    fi
fi
CHECKS_TOTAL=$((CHECKS_TOTAL + 1))

# Test logger
echo ""
echo "🧪 Logger Test"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if python3 ~/.hermes/digi-command-center/logger.py > /tmp/digi_test.log 2>&1; then
    echo -e "${GREEN}✅${NC} Logger test passed"
    CHECKS_PASSED=$((CHECKS_PASSED + 1))
else
    echo -e "${RED}❌${NC} Logger test failed"
    warn "Check: python3 ~/.hermes/digi-command-center/logger.py"
fi
CHECKS_TOTAL=$((CHECKS_TOTAL + 1))

# Summary
echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                      VERIFICATION SUMMARY                      ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""
echo "Passed: $CHECKS_PASSED / $CHECKS_TOTAL"

if [ $CHECKS_PASSED -eq $CHECKS_TOTAL ]; then
    echo -e "${GREEN}✅ All checks passed! Phase 3 is ready.${NC}"
    echo ""
    echo "Next steps:"
    echo "1. Test locally: python3 logger.py"
    echo "2. Check Obsidian: Daily/2026-04-04.md"
    echo "3. Check dashboard: http://localhost:3000"
    echo "4. Deploy to Railway: Follow RAILWAY_DEPLOY.md"
    exit 0
else
    echo -e "${RED}❌ Some checks failed. See details above.${NC}"
    exit 1
fi
