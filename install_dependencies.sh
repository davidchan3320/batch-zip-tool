#!/bin/bash
# Installation script for Batch ZIP dependencies

echo "🗜️  Batch ZIP - 安裝相依套件"
echo "================================"
echo ""

# Check Python version
echo "正在檢查 Python 版本..."
if ! command -v python3 &> /dev/null; then
    echo "❌ 找不到 Python 3。請先安裝 Python 3.7 或更高版本。"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo "✅ 找到 Python $PYTHON_VERSION"
echo ""

# Create virtual environment
echo "正在建立虛擬環境..."
if [ -d ".venv" ]; then
    echo "⚠️  虛擬環境已存在，將使用現有環境"
else
    python3 -m venv .venv
    if [ $? -eq 0 ]; then
        echo "✅ 虛擬環境建立成功"
    else
        echo "❌ 虛擬環境建立失敗"
        exit 1
    fi
fi
echo ""

# Activate virtual environment and install packages
echo "正在安裝 Python 套件..."
source .venv/bin/activate

# Install tkinterdnd2
echo "正在安裝 tkinterdnd2 (拖放功能)..."
pip install tkinterdnd2
if [ $? -eq 0 ]; then
    echo "✅ tkinterdnd2 安裝成功"
else
    echo "❌ tkinterdnd2 安裝失敗"
    exit 1
fi
echo ""

# Check for 7-Zip
echo "正在檢查 7-Zip..."
if command -v 7z &> /dev/null; then
    echo "✅ 7-Zip 已安裝"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    echo "❓ 7-Zip 未安裝。是否要安裝？(需要 Homebrew) [y/N]"
    read -r response
    if [[ "$response" =~ ^[Yy]$ ]]; then
        if command -v brew &> /dev/null; then
            echo "正在安裝 p7zip..."
            brew install p7zip
            echo "✅ 7-Zip 安裝成功"
        else
            echo "❌ 找不到 Homebrew。請先安裝 Homebrew 或手動安裝 7-Zip。"
        fi
    else
        echo "⏭️  跳過 7-Zip 安裝"
    fi
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "❓ 7-Zip 未安裝。是否要安裝？[y/N]"
    read -r response
    if [[ "$response" =~ ^[Yy]$ ]]; then
        echo "正在安裝 p7zip-full..."
        sudo apt-get update
        sudo apt-get install -y p7zip-full
        echo "✅ 7-Zip 安裝成功"
    else
        echo "⏭️  跳過 7-Zip 安裝"
    fi
fi
echo ""

echo "================================"
echo "✨ 安裝完成！"
echo ""
echo "執行以下指令啟動應用程式："
echo "  python3 batch_zip_gui.py"
echo ""
echo "或使用啟動腳本："
echo "  ./run.sh"
echo ""
