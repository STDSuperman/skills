#!/usr/bin/env python3
import argparse
import os
import subprocess
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional

from dotenv import load_dotenv


def load_config() -> Optional[Dict[str, Any]]:
    """加载 .env 配置文件。

    Returns:
        配置字典，如果未配置仓库地址则返回 None
    """
    config_path = Path(__file__).parent.parent / ".env"
    if not config_path.exists():
        return None

    load_dotenv(config_path)

    repo_url = None
    if "GITHUB_REPO_URL" in os.environ:
        repo_url = os.environ["GITHUB_REPO_URL"].strip()
    else:
        return None

    if not repo_url:
        return None

    return {
        "repo_url": repo_url,
        "repo_type": os.environ.get("REPO_TYPE", "").strip() or None,
        "repo_target_dir": os.environ.get("REPO_TARGET_DIR", "").strip() or None,
        "filename_format": os.environ.get("FILENAME_FORMAT", "daily-news-%Y%m%d.md").strip(),
    }


class RepoPublisher:
    """仓库发布器，负责将日报内容发布到 GitHub 仓库。"""

    def __init__(self, config: Dict[str, Any]):
        """初始化仓库发布器。

        Args:
            config: 配置字典，包含仓库 URL、类型等信息
        """
        self.config = config

    def run_git(self, cmd: list, cwd: Path) -> str:
        """执行 Git 命令。

        Args:
            cmd: Git 命令参数列表（不包含 'git'）
            cwd: 执行命令的工作目录

        Returns:
            命令输出

        Raises:
            subprocess.CalledProcessError: Git 命令执行失败
        """
        result = subprocess.run(
            ["git"] + cmd, cwd=cwd, capture_output=True, text=True, check=True
        )
        return result.stdout

    def clone_repo(self, temp_dir: Path) -> Path:
        """克隆仓库到临时目录。

        Args:
            temp_dir: 临时目录路径

        Returns:
            仓库根目录路径

        Raises:
            Exception: 克隆失败
        """
        repo_url = self.config["repo_url"]
        print(f"正在克隆仓库: {repo_url}")

        try:
            self.run_git(["clone", repo_url, temp_dir], temp_dir.parent)
            repo_path = temp_dir
            print(f"✅ 仓库克隆成功: {repo_path}")
            return repo_path
        except subprocess.CalledProcessError as e:
            raise Exception(f"克隆仓库失败: {e.stderr}")

    def detect_repo_type(self, repo_path: Path) -> str:
        """检测仓库类型。

        Args:
            repo_path: 仓库路径

        Returns:
            仓库类型：vuepress、generic 或 custom
        """
        repo_type = self.config.get("repo_type")
        if repo_type:
            return repo_type

        if (repo_path / "docs").exists():
            return "vuepress"

        if (repo_path / ".vuepress").exists():
            return "vuepress"

        return "generic"

    def get_target_dir(self, repo_path: Path) -> Path:
        """获取目标目录路径。

        Args:
            repo_path: 仓库路径

        Returns:
            目标目录路径
        """
        repo_type = self.detect_repo_type(repo_path)

        if repo_type == "vuepress":
            return repo_path / "docs"
        elif repo_type == "custom":
            target = self.config.get("repo_target_dir", "")
            return repo_path / target if target else repo_path
        else:
            return repo_path

    def generate_filename(self) -> str:
        """生成日报文件名。

        Returns:
            文件名
        """
        fmt = self.config["filename_format"]
        return datetime.now().strftime(fmt)

    def write_report(self, content: str, repo_path: Path) -> Path:
        """写入日报内容到文件。

        Args:
            content: 日报内容
            repo_path: 仓库路径

        Returns:
            写入的文件路径

        Raises:
            Exception: 写入失败
        """
        target_dir = self.get_target_dir(repo_path)
        target_dir.mkdir(parents=True, exist_ok=True)

        filename = self.generate_filename()
        filepath = target_dir / filename

        print(f"正在写入日报到: {filepath}")

        try:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"✅ 日报写入成功")
            return filepath
        except Exception as e:
            raise Exception(f"写入日报失败: {str(e)}")

    def commit_and_push(self, repo_path: Path, filepath: Path) -> None:
        """提交并推送变更。

        Args:
            repo_path: 仓库路径
            filepath: 日报文件路径

        Raises:
            Exception: 提交或推送失败
        """
        try:
            self.run_git(["add", str(filepath.relative_to(repo_path))], repo_path)
            self.run_git(["status"], repo_path)

            filename = filepath.name
            commit_message = f"feat: 添加日报 {filename}"
            self.run_git(["commit", "-m", commit_message], repo_path)

            print("正在推送到远程仓库...")
            self.run_git(["push"], repo_path)
            print("✅ 推送成功")
        except subprocess.CalledProcessError as e:
            raise Exception(f"提交或推送失败: {e.stderr}")

    def publish(self, content: str) -> None:
        """发布日报到仓库。

        Args:
            content: 日报内容
        """
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            repo_path = self.clone_repo(temp_path)
            filepath = self.write_report(content, repo_path)
            self.commit_and_push(repo_path, filepath)


def main():
    """主函数。"""
    parser = argparse.ArgumentParser(
        description="将日报发布到 GitHub 仓库", formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "--content", type=str, help="日报内容字符串"
    )
    parser.add_argument(
        "--file", type=Path, help="日报文件路径"
    )
    args = parser.parse_args()

    if not args.content and not args.file:
        parser.error("必须提供 --content 或 --file 参数")
    if args.content and args.file:
        parser.error("--content 和 --file 参数不能同时使用")

    content = ""
    if args.content:
        content = args.content
    elif args.file:
        if not args.file.exists():
            print(f"❌ 文件不存在: {args.file}")
            return
        with open(args.file, "r", encoding="utf-8") as f:
            content = f.read()

    config = load_config()
    if not config:
        print("⚠️  未配置仓库地址，跳过发布")
        print("💡 提示: 复制 .env.example 到 .env 并填写 GITHUB_REPO_URL")
        return

    try:
        publisher = RepoPublisher(config)
        publisher.publish(content)
    except Exception as e:
        print(f"❌ 发布失败: {str(e)}")


if __name__ == "__main__":
    main()
