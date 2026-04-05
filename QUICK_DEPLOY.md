# Digi Dashboard — Quick Deploy

**Status:** Ready to run  
**Time to launch:** 3 minutes (local) or 15 minutes (production on Railway)

---

## 🚀 Local Development (3 min)

### 1. Install Dependencies
```bash
cd ~/.hermes/digi-command-center/dashboard
npm install
```

### 2. Environment Variables (Already Set!)
```bash
cp .env.example .env.local
# Keys are pre-filled, no action needed!
```

### 3. Run Dashboard
```bash
npm run dev
```

Open: **http://localhost:3000**

You'll see:
- 6 agent cards (Scout, Judge, Artisan, Guardian, Executor, Oracle)
- Live log tail (last 50 messages)
- Real-time status updates
- Refresh button for manual updates

---

## 🌐 Production Deploy to Railway (15 min)

### 1. Link Git Repo
```bash
cd ~/.hermes/digi-command-center
git init
git add .
git commit -m "Initial Digi Command Center deployment"
git remote add origin <your-railway-git-url>
```

### 2. Create Railway Project
1. Go to https://railway.app
2. Create new project → GitHub → select repo
3. Add service → select `/dashboard` directory
4. Configure environment variables in Railway dashboard:
   - `NEXT_PUBLIC_SUPABASE_URL`
   - `NEXT_PUBLIC_SUPABASE_ANON_KEY`

### 3. Deploy
```bash
git push origin main
# Railway auto-deploys! ✅
```

### 4. Get Live URL
- Check Railway dashboard for deployment URL
- Example: `https://digi-command-center-production.railway.app`
- Share with team!

---

## 🧪 Testing

### Test Agent Run
Trigger a test logger run to populate the dashboard:

```bash
cd ~/.hermes/digi-command-center
python3 logger.py
```

Then refresh dashboard → you'll see:
- New agent_run in Supabase
- Live logs appearing in real-time
- Progress indicators updating

---

## 📊 Live Features

### Agent Status Card
- Agent name + role
- Current status badge (running/completed/failed)
- Progress bar (if running)
- Start time

### Live Log Tail
- Last 50 messages
- Color-coded by level (info/warning/error/milestone)
- Timestamps
- Metadata preview

### Real-Time Updates
- Supabase subscriptions
- Auto-refresh every message
- No polling needed
- Scroll to bottom for latest

### Refresh Button
- Manual update trigger
- Fetches latest runs + logs
- Useful for catching missed messages

---

## 🔧 Customization

### Change Update Frequency
Edit `src/app/page.tsx`, search for `useEffect`:
```typescript
// Add polling if you want
setInterval(handleRefresh, 5000) // 5 seconds
```

### Add More Metrics
Edit `src/components/AgentCard.tsx`:
```typescript
// Add execution time, error count, etc.
<div>Total Time: {calcDuration(run)}</div>
```

### Custom Styling
Edit `tailwind.config.js` for theme colors, then update component classes.

---

## 🐛 Troubleshooting

### Dashboard Shows "No logs yet"
- Trigger a test run: `python3 logger.py`
- Refresh page
- Check browser console for errors (F12)

### Real-time updates not working
- Check browser console for Supabase connection errors
- Verify `.env.local` has correct keys
- Make sure you're not using service role key in frontend (use anon key)

### Build fails
```bash
# Clear cache and rebuild
rm -rf .next node_modules
npm install
npm run build
```

### Railway deployment fails
- Check Railway logs: `railway logs`
- Verify env vars are set correctly
- Make sure Node version is compatible (18+)

---

## 📱 Mobile View

Dashboard is fully responsive:
- Stacks vertically on mobile
- Touch-friendly controls
- Works on iPad, iPhone, Android

---

## 🔐 Security Notes

- ✅ Using anon key for frontend (read-only by default)
- ✅ Service key stored in `.env.local` (git-ignored)
- ✅ RLS policies protect Supabase tables
- ✅ No sensitive data in logs displayed on dashboard

---

## 📞 Support

**Issue?** Check:
1. `STATUS.md` — Deployment status
2. `IMPLEMENTATION.md` — Technical details
3. `README.md` — Architecture overview

**Still stuck?** Review:
- Browser console errors (F12)
- Railway logs (if deployed)
- Supabase dashboard for data verification

---

## 🎉 You're Done!

Digi Command Center dashboard is running. 

Next steps:
1. Integrate logger into first agent run
2. Watch dashboard update in real-time
3. Check Obsidian for daily summary
4. Celebrate! 🎊
