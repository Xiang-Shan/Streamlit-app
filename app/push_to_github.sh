#!/bin/zsh
# Push to GitHub script

echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║  🚀 PUSH TO GITHUB                                          ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""
echo "Enter your GitHub username:"
read github_user

echo ""
echo "Pushing to GitHub..."
echo ""

cd /Users/xiang/my_venv3.13.3/code/Streamlit/Test2_backup/app2

git remote add origin "https://github.com/${github_user}/french-motor-insurance-dashboard.git" 2>/dev/null || echo "Remote already exists"
git branch -M main
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "✅ Successfully pushed to GitHub!"
    echo ""
    echo "🌐 Repository URL:"
    echo "   https://github.com/${github_user}/french-motor-insurance-dashboard"
    echo ""
    echo "📋 Verify files on GitHub:"
    echo "   ✓ app.py"
    echo "   ✓ requirements.txt"
    echo "   ✓ data_numeric.npz (12.75 MB) ⭐"
    echo "   ✓ data_categorical.npz (1.57 MB) ⭐"
    echo "   ✓ data_metadata.json ⭐"
    echo "   ✓ category_mappings.json ⭐"
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "☁️  NEXT: Deploy to Streamlit Cloud"
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
else
    echo ""
    echo "❌ Push failed. Please check:"
    echo "   1. GitHub repository exists"
    echo "   2. You have access to the repository"
    echo "   3. Your GitHub credentials are correct"
    echo ""
fi
