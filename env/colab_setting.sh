#!/bin/bash

echo "🚀 Starting environment setup for LLaVA..."

# 1️⃣ **GitHub 사용자 정보 변수 설정**
GIT_USER="illgamohduck"
GIT_EMAIL="hyunbyung87@gmail.com"

echo "🔧 Checking GitHub SSH key settings..."

# 현재 설정된 Git user.name과 user.email을 가져와 확인
CURRENT_GIT_USER=$(git config --global user.name)
CURRENT_GIT_EMAIL=$(git config --global user.email)

if [ "$CURRENT_GIT_USER" = "$GIT_USER" ] && [ "$CURRENT_GIT_EMAIL" = "$GIT_EMAIL" ]; then
    echo "✅ GitHub user settings are already configured."
else
    echo "🔧 Setting up GitHub user info..."
    git config --global user.name "$GIT_USER"
    git config --global user.email "$GIT_EMAIL"
fi

# 2️⃣ **SSH 키 설정 확인 및 적용**
DRIVE_HOME_DIR="/content/drive/MyDrive/구직/Twelvelabs"
LOCAL_SSH_DIR="$HOME/.ssh"
SSH_KEY_PATH="$LOCAL_SSH_DIR/id_ed25519"

mkdir -p "$LOCAL_SSH_DIR"

if [ -f "$SSH_KEY_PATH" ]; then
    echo "✅ SSH key already exists, skipping setup."
else
    echo "🔑 Setting up SSH key from Google Drive..."
    cp "$DRIVE_HOME_DIR/id_ed25519" "$SSH_KEY_PATH"
    chmod 600 "$SSH_KEY_PATH"
fi

# 3️⃣ **LLaVA 저장소 확인 및 클론**
DRIVE_REPO_DIR="$DRIVE_HOME_DIR/llava"
GIT_REPO_URL="git@github.com:IllgamhoDuck/llava.git"

if [ -d "$DRIVE_REPO_DIR" ]; then
    echo "✅ LLaVA repository already exists at: $DRIVE_REPO_DIR"
else
    echo "🚀 Cloning LLaVA repository..."
    git clone "$GIT_REPO_URL" "$DRIVE_REPO_DIR"
    if [ $? -ne 0 ]; then
        echo "❌ ERROR: Failed to clone repository. Check SSH key and repository access rights."
        exit 1
    fi
fi
echo "🔄 Upgrading to the latest code base..."
git pull
chmod +x "$DRIVE_REPO_DIR/.git/hooks/pre-push"
chmod +x "$DRIVE_REPO_DIR/.git/hooks/pre-commit"

# 4️⃣ **LLaVA 패키지 설치 (requirements.txt)**
echo "📦 Installing LLaVA dependencies..."
cd "$DRIVE_REPO_DIR" || { echo "❌ ERROR: Failed to change directory to $DRIVE_REPO_DIR"; exit 1; }
CACHE_DIR="$DRIVE_HOME_DIR/pip_cache"

mkdir -p "$CACHE_DIR"

pip install -e . --cache-dir "$CACHE_DIR"
pip install -e ".[train]" --cache-dir "$CACHE_DIR"
pip install flash-attn --no-build-isolation --cache-dir "$CACHE_DIR"
pip install datasets --cache-dir "$CACHE_DIR"
pip install xformers --cache-dir "$CACHE_DIR"
pip install -U transformers==4.37.2 --cache-dir "$CACHE_DIR"
pip install -U peft==0.7.1 --cache-dir "$CACHE_DIR"
pip install deepspeed==0.14.4 --cache-dir "$CACHE_DIR"


# 5️⃣ **Oh My Bash 설치**
bash -c "$(curl -fsSL https://raw.githubusercontent.com/ohmybash/oh-my-bash/master/tools/install.sh)"






