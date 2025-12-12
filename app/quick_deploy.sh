#!/bin/zsh
# Quick deployment script for app2

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║  🚀 DEPLOYING APP2 TO GITHUB                                ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

cd /Users/xiang/my_venv3.13.3/code/Streamlit/Test2_backup/app2

echo "📦 Initializing git..."
git init

echo "📦 Adding files..."
git add .

echo "📦 Committing..."
git commit -m "Initial commit: French Motor Insurance GLM Dashboard

- Dataset: 678,013 insurance policies (14.3MB NPZ format)
- Interactive Streamlit dashboard with 7 analysis tabs  
- 92.5% size reduction from original CSV
- Self-contained deployment ready for Streamlit Cloud"

echo ""
echo "✅ Git repository initialized and committed!"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📝 NEXT STEPS:"
echo ""
echo "1️⃣  Create GitHub repository:"
echo "   Go to: https://github.com/new"
echo "   Name: french-motor-insurance-dashboard"
echo "   Description: Interactive Streamlit dashboard for French Motor Insurance GLM analysis"
echo "   Visibility: Public"
echo "   Click 'Create repository'"
echo ""
echo "2️⃣  Enter your GitHub username:"
read "github_user?   Username: "
echo ""
echo "3️⃣  Pushing to GitHub..."

git remote add origin "https://github.com/${github_user}/french-motor-insurance-dashboard.git"
git branch -M main
git push -u origin main

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "✅ Successfully pushed to GitHub!"
echo ""
echo "🌐 Repository URL:"
echo "   https://github.com/${github_user}/french-motor-insurance-dashboard"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "☁️  FINAL STEP - Deploy to Streamlit Cloud:"
echo ""
echo "1. Go to: https://share.streamlit.io"
echo "2. Sign in with GitHub"
echo "3. Click 'New app'"
echo "4. Repository: ${github_user}/french-motor-insurance-dashboard"
echo "5. Branch: main"
echo "6. Main file: app.py"
echo "7. Click 'Deploy!'"
echo ""
echo "⏱️  Deployment takes 2-3 minutes..."
echo ""
echo "🎉 Your app will be live at:"
echo "   https://${github_user}-french-motor-insurance-dashboard.streamlit.app"
echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║  🎊 CONGRATULATIONS! YOUR DASHBOARD IS BEING DEPLOYED!      ║"
echo "╚══════════════════════════════════════════════════════════════╝"
