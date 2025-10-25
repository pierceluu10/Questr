#!/bin/bash

echo "🚀 SideQuestly GitHub Upload Script"
echo "=================================="
echo ""

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo "❌ Error: Not in a git repository!"
    exit 1
fi

echo "📋 Current git status:"
git status
echo ""

echo "📝 Please provide your GitHub repository details:"
echo ""

# Get GitHub username
read -p "Enter your GitHub username: " GITHUB_USERNAME

# Get repository name
read -p "Enter your repository name (default: SideQuestly): " REPO_NAME
REPO_NAME=${REPO_NAME:-SideQuestly}

# Construct the repository URL
REPO_URL="https://github.com/${GITHUB_USERNAME}/${REPO_NAME}.git"

echo ""
echo "🔗 Repository URL: ${REPO_URL}"
echo ""

# Confirm before proceeding
read -p "Is this correct? (y/n): " CONFIRM

if [ "$CONFIRM" != "y" ] && [ "$CONFIRM" != "Y" ]; then
    echo "❌ Cancelled by user"
    exit 1
fi

echo ""
echo "🔄 Adding remote origin..."
git remote add origin ${REPO_URL}

echo "📤 Pushing to GitHub..."
git push -u origin main

echo ""
echo "✅ Success! Your SideQuestly project is now on GitHub!"
echo "🌐 Visit: https://github.com/${GITHUB_USERNAME}/${REPO_NAME}"
echo ""
echo "🚀 Next steps for deployment:"
echo "1. Go to https://render.com"
echo "2. Create a new Web Service"
echo "3. Connect your GitHub repository"
echo "4. Use these settings:"
echo "   - Build Command: pip install -r requirements.txt"
echo "   - Start Command: gunicorn app:app"
echo "   - Environment Variables: SECRET_KEY=your-secret-key, FLASK_ENV=production"
