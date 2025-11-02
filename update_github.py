#!/usr/bin/env python3
"""
Git 更新仓库脚本 (Python版本)
用于快速提交和推送代码到GitHub
"""

import subprocess
import sys
from datetime import datetime


def run_command(cmd, description):
    """执行Shell命令"""
    print(f"\n{description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 错误: {e}")
        if e.stderr:
            print(e.stderr)
        return False


def check_git_status():
    """检查Git状态"""
    return run_command("git status", "检查Git状态")


def add_changes():
    """添加所有更改"""
    return run_command("git add .", "添加所有更改")


def commit_changes(message):
    """提交更改"""
    cmd = f'git commit -m "{message}"'
    return run_command(cmd, f"提交更改: {message}")


def push_to_github():
    """推送到GitHub"""
    return run_command("git push origin main", "推送到GitHub")


def main():
    """主函数"""
    print("=" * 50)
    print("GitHub 仓库更新脚本")
    print("=" * 50)
    
    # 检查Git状态
    if not check_git_status():
        print("\n❌ 无法检查Git状态，请确保已初始化Git仓库")
        sys.exit(1)
    
    # 询问是否继续
    print("\n" + "=" * 50)
    confirm = input("是否继续更新? (y/n): ").strip().lower()
    
    if confirm != 'y':
        print("操作已取消")
        sys.exit(0)
    
    # 添加所有更改
    if not add_changes():
        print("\n❌ 添加文件失败")
        sys.exit(1)
    
    # 获取提交信息
    print("\n" + "=" * 50)
    commit_msg = input("请输入提交信息 (或按回车使用默认): ").strip()
    
    if not commit_msg:
        commit_msg = f"Update: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    
    # 提交更改
    if not commit_changes(commit_msg):
        print("\n❌ 提交失败，可能没有需要提交的更改")
        sys.exit(1)
    
    # 推送到GitHub
    if not push_to_github():
        print("\n❌ 推送失败，请检查网络连接和仓库权限")
        sys.exit(1)
    
    # 完成
    print("\n" + "=" * 50)
    print("✅ 更新完成！")
    print("=" * 50)
    print("\n仓库地址: https://github.com/2921323707/Psychological_Assesment")
    print()


if __name__ == "__main__":
    main()

