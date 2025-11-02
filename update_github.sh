#!/bin/bash
# Git 更新仓库脚本
# 用于快速提交和推送代码到GitHub

echo "==============================================="
echo "GitHub 仓库更新脚本"
echo "==============================================="
echo ""

# 检查git状态
echo "1. 检查Git状态..."
git status

echo ""
read -p "是否继续更新? (y/n): " confirm

if [ "$confirm" != "y" ] && [ "$confirm" != "Y" ]; then
    echo "操作已取消"
    exit 0
fi

# 添加所有更改
echo ""
echo "2. 添加所有更改..."
git add .

# 获取提交信息
echo ""
read -p "请输入提交信息 (或按回车使用默认): " commit_msg

if [ -z "$commit_msg" ]; then
    commit_msg="Update: $(date '+%Y-%m-%d %H:%M:%S')"
fi

# 提交更改
echo ""
echo "3. 提交更改..."
echo "提交信息: $commit_msg"
git commit -m "$commit_msg"

# 推送到远程仓库
echo ""
echo "4. 推送到GitHub..."
git push origin main

echo ""
echo "==============================================="
echo "✅ 更新完成！"
echo "==============================================="
echo ""
echo "仓库地址: https://github.com/2921323707/Psychological_Assesment"
echo ""

