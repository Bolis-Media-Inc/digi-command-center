# Digi Dashboard — Railway Deployment

**Goal:** Deploy Next.js dashboard to production on Railway  
**Time:** 15 minutes  
**Cost:** Free tier available, ~$5/month for production

---

## 📋 Prerequisites

- ✅ Railway account (https://railway.app) — free to start
- ✅ GitHub account with repo access
- ✅ Supabase keys (already in `.env.local`)
- ✅ Dashboard running locally (verified working)

---

## 🚀 Step-by-Step Deployment

### 1. Prepare Repository

First, initialize git in the dashboard directory:

```bash
cd ~/.hermes/digi-command-center

# Initialize git if not already done
git init
git add .
git commit -m "Initial Digi Command Center deployment"

# Add Railway as remote (or push to GitHub first)
git remote add railway https://github.com/<your-username>/digi-command-center.git
```

**If using GitHub:**
```bash
# Create new repo on GitHub, then:
git remote add origin https://github.com/<your-username>/digi-command-center.git
git branch -M main
git push -u origin main
```

### 2. Create Railway Project

1. Go to https://railway.app
2. Click **"Create New Project"**
3. Select **"Deploy from GitHub"**
4. Authenticate with GitHub
5. Select your repository (`digi-command-center`)
6. Railway will auto-detect the `package.json` in `/dashboard`

### 3. Configure Environment Variables

In Railway dashboard:

1. Go to **Project Settings** → **Variables**
2. Add these variables:
   ```
   NEXT_PUBLIC_SUPABASE_URL=https://ynyeuuxynwfzukvvxxlp.supabase.co
   NEXT_PUBLIC_SUPABASE_ANON_KEY=<copy from .env.local>
   ```

**Important:** Only use the **ANON** key for the frontend (read-only, safe public)

### 4. Configure Build & Deploy

Railway should auto-detect Next.js. Configure if needed:

1. Go to **Deployments** tab
2. Click **"Configure" → "Settings"**
3. Set:
   - **Start Command:** `npm run start`
   - **Build Command:** `npm run build`
   - **Root Directory:** `dashboard/`

### 5. Deploy

```bash
# Push to trigger auto-deploy
git push origin main
```

Railway will:
1. ✅ Detect Next.js app
2. ✅ Install dependencies
3. ✅ Run `npm run build`
4. ✅ Start `npm run start`
5. ✅ Assign live URL

### 6. Get Live URL

1. In Railway dashboard, click **Domains**
2. You'll see: `https://digi-command-center-production.railway.app`
3. Click to verify it's live
4. Share the URL with your team!

---

## ✅ Post-Deployment Verification

### Check Dashboard is Live

```bash
curl https://digi-command-center-production.railway.app
# Should return HTML (not error)
```

### Test Real-Time Connection

1. Open live dashboard in browser
2. Trigger a test logger run (locally or via cron)
3. Dashboard should update in real-time

### Monitor Logs

In Railway:
1. Click **Project**
2. Go to **Logs**
3. You'll see Next.js server logs
4. Check for any errors

---

## 🔧 Troubleshooting

### Build Fails

**Error:** `npm ERR! Module not found`

**Solution:**
```bash
cd dashboard
npm install
npm run build  # test locally first
git add .
git commit -m "Fix dependencies"
git push origin main
```

### App Shows "No logs yet"

- Ensure Supabase keys are correct
- Verify agent runs exist in Supabase
- Check browser console (F12) for errors
- Try refreshing page

### Deployment Stuck

1. Check Railway **Logs** for errors
2. Verify environment variables are set
3. Try redeploying: **Deployments** → **Redeploy**

### Real-time updates not working

**Problem:** Dashboard doesn't auto-update when agents run

**Solution:**
1. Verify `NEXT_PUBLIC_SUPABASE_URL` is set
2. Verify `NEXT_PUBLIC_SUPABASE_ANON_KEY` is set
3. Check browser console: Network tab → look for supabase connections
4. Ensure agents are actually writing to Supabase

---

## 📊 Monitoring & Maintenance

### View Logs
```bash
# Via Railway dashboard: Logs tab
# Or via Railway CLI:
railway logs --service digi-dashboard
```

### Update Code
```bash
cd ~/.hermes/digi-command-center
git add .
git commit -m "Update dashboard"
git push origin main
# Railway auto-deploys!
```

### Rollback to Previous Version
```bash
git revert <commit-hash>
git push origin main
# Railway redeploys previous version
```

### Monitor Uptime & Performance
- Railway dashboard shows:
  - CPU usage
  - Memory usage
  - Network traffic
  - Deployment history

---

## 💰 Costs & Plan

**Free Tier:**
- Up to $5 credit/month
- Usually enough for low-traffic dashboard

**Pro Considerations:**
- If > 1000 page views/day → consider paid plan
- Supabase charges separately (free tier also available)
- Estimate: $5-10/month for Digi dashboard

**Recommendation:** Start on free tier, upgrade if needed

---

## 🎯 Next: End-to-End Test

Once dashboard is live:

1. ✅ Keep local dashboard running (or close it)
2. ✅ Trigger test agent run: `python3 logger.py`
3. ✅ Check live dashboard: logs appear in real-time
4. ✅ Check Obsidian: Daily summary updated
5. ✅ Check Telegram: Alert sent (if error)

Then you're done with Phase 3! 🎉

---

## 📞 Support

**Railway Issues:** https://docs.railway.app  
**Next.js Issues:** https://nextjs.org/docs  
**Supabase Issues:** https://supabase.com/docs  

---

**Status:** Ready to deploy ✅
