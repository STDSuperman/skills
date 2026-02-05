#!/usr/bin/env python3
import argparse
import json
import os
import re
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
            ["git"] + cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, check=True
        )
        return result.stdout

    def extract_repo_name(self, repo_url: str) -> Optional[str]:
        """从仓库 URL 提取仓库名。

        Args:
            repo_url: 仓库 URL（支持 HTTPS 和 SSH 格式）

        Returns:
            仓库名，例如 "news-daily"，提取失败则返回 None
        """
        patterns = [
            r"github\.com[:/]([^/]+)/([^/]+?)(?:\.git)?$",
            r"([^/]+)/([^/]+?)(?:\.git)?$",
        ]

        for pattern in patterns:
            match = re.search(pattern, repo_url)
            if match:
                return match.group(2)

        return None

    def clone_repo(self, cache_dir: Path) -> Path:
        """克隆或更新仓库到缓存目录。

        Args:
            cache_dir: 缓存目录路径

        Returns:
            仓库根目录路径

        Raises:
            Exception: 克隆失败
        """
        repo_url = self.config["repo_url"]
        
        if cache_dir.exists():
            print(f"更新现有仓库: {cache_dir}")
            try:
                self.run_git(["fetch", "origin"], cache_dir)
                self.run_git(["reset", "--hard", "origin/HEAD"], cache_dir)
                print(f"✅ 仓库更新成功")
                return cache_dir
            except subprocess.CalledProcessError as e:
                raise Exception(f"更新仓库失败: {e.stderr}")
        else:
            print(f"正在克隆仓库: {repo_url}")
            cache_dir.parent.mkdir(parents=True, exist_ok=True)
            try:
                self.run_git(["clone", repo_url, cache_dir], cache_dir.parent)
                print(f"✅ 仓库克隆成功: {cache_dir}")
                return cache_dir
            except subprocess.CalledProcessError as e:
                raise Exception(f"克隆仓库失败: {e.stderr}")

    def detect_repo_type(self, repo_path: Path) -> str:
        """检测仓库类型。

        Args:
            repo_path: 仓库路径

        Returns:
            仓库类型：vitepress、vuepress、generic 或 custom
        """
        repo_type = self.config.get("repo_type")
        if repo_type:
            return repo_type

        if (repo_path / "docs" / ".vitepress").exists():
            return "vitepress"

        if (repo_path / "docs" / ".vuepress").exists():
            return "vuepress"

        if (repo_path / ".vitepress").exists():
            return "vitepress"

        if (repo_path / ".vuepress").exists():
            return "vuepress"

        return "generic"

    def parse_vitepress_navbar(self, repo_path: Path) -> Optional[str]:
        """解析 VitePress 配置文件，获取导航栏路由。

        Args:
            repo_path: 仓库路径

        Returns:
            路由目录路径，例如 "daily"，如果解析失败则返回 None
        """
        vitepress_dir = repo_path / "docs" / ".vitepress"
        if not vitepress_dir.exists():
            return None

        config_path = vitepress_dir / "config.js"
        if not config_path.exists():
            return None

        try:
            with open(config_path, "r", encoding="utf-8") as f:
                content = f.read()

            nav_match = re.search(r'nav\s*:\s*\[(.*?)\]', content, re.DOTALL)
            if not nav_match:
                return None

            nav_content = nav_match.group(1)
            
            link_matches = re.findall(r"link\s*:\s*['\"]([^'\"]+)['\"]", nav_content)
            
            for link in link_matches:
                link = link.strip()
                if link and link != "/" and link.startswith("/") and link.endswith("/"):
                    return link[1:-1]
            
            return None
        except Exception:
            return None

    def parse_vuepress_navbar(self, repo_path: Path) -> Optional[str]:
        """解析 VuePress 配置文件，获取导航栏路由。

        Args:
            repo_path: 仓库路径

        Returns:
            路由目录路径，例如 "daily"，如果解析失败则返回 None
        """
        vuepress_dir = repo_path / "docs" / ".vuepress"
        if not vuepress_dir.exists():
            return None

        config_files = ["config.ts", "config.js", "config.mjs"]
        config_path = None
        
        for cf in config_files:
            path = vuepress_dir / cf
            if path.exists():
                config_path = path
                break
        
        if not config_path:
            return None

        try:
            with open(config_path, "r", encoding="utf-8") as f:
                content = f.read()

            navbar_match = re.search(r'navbar\s*:\s*\[(.*?)\]', content, re.DOTALL)
            if not navbar_match:
                return None

            navbar_content = navbar_match.group(1)
            
            link_matches = re.findall(r"link\s*:\s*['\"]([^'\"]+)['\"]", navbar_content)
            
            for link in link_matches:
                link = link.strip()
                if link and link != "/" and link.startswith("/") and link.endswith("/"):
                    return link[1:-1]
            
            return None
        except Exception:
            return None

    def update_vitepress_base(self, repo_path: Path) -> None:
        """更新 VitePress 配置文件，添加 base 路径配置。

        Args:
            repo_path: 仓库路径
        """
        vitepress_dir = repo_path / "docs" / ".vitepress"
        if not vitepress_dir.exists():
            return

        config_path = vitepress_dir / "config.js"
        if not config_path.exists():
            return

        repo_name = self.extract_repo_name(self.config["repo_url"])
        if not repo_name:
            print("⚠️  无法从仓库 URL 提取仓库名，跳过 base 配置更新")
            return

        base_path = f"/{repo_name}/"

        try:
            with open(config_path, "r", encoding="utf-8") as f:
                content = f.read()

            if "base:" in content:
                print(f"✅ 检测到 base 配置已存在: {base_path}")
                return

            new_content = content.replace(
                "export default {",
                f"export default {{\n  base: '{base_path}',"
            )

            with open(config_path, "w", encoding="utf-8") as f:
                f.write(new_content)

            print(f"✅ 已添加 base 配置: {base_path}")
        except Exception as e:
            print(f"⚠️  更新 VitePress base 配置失败: {str(e)}")

    def update_vitepress_sidebar(self, repo_path: Path, filepath: Path) -> None:
        """更新 VitePress 配置文件，添加新日报到侧边栏。

        Args:
            repo_path: 仓库路径
            filepath: 日报文件路径
        """
        vitepress_dir = repo_path / "docs" / ".vitepress"
        if not vitepress_dir.exists():
            return

        config_path = vitepress_dir / "config.js"
        if not config_path.exists():
            return

        daily_dir = repo_path / "docs" / "daily"
        if not daily_dir.exists():
            return

        try:
            with open(config_path, "r", encoding="utf-8") as f:
                content = f.read()

            filename = filepath.name

            md_files = sorted(daily_dir.glob("*.md"), reverse=True)

            sidebar_items = []

            for md_file in md_files:
                if md_file.name == "index.md":
                    continue

                date_str = md_file.stem
                if date_str.startswith("daily-news-"):
                    date_str = date_str[11:]
                link_name = md_file.stem
                sidebar_items.append(
                    f"            {{ text: '{date_str}', link: '/daily/{link_name}' }}"
                )

            new_items_block = ",\n".join(sidebar_items)

            sidebar_pattern = r"sidebar:\s*\{\s*'/daily/':\s*\[\s*\{\s*text:\s*'([^']+)',\s*items:\s*\[[^\]]*\]"
            new_sidebar = f"sidebar:\n    {{\n      '/daily/': [\n        {{\n          text: '每日日报',\n          items: [\n{new_items_block}\n          ]\n        }}\n      ]\n    }}"

            content = re.sub(r"sidebar:\s*\{[^\}]+\}", new_sidebar, content, flags=re.DOTALL)

            with open(config_path, "w", encoding="utf-8") as f:
                f.write(content)

            print("✅ 已更新 VitePress 侧边栏配置")
            print(f"📋 侧边栏包含 {len(sidebar_items)} 个项目")
        except Exception as e:
            print(f"⚠️  更新 VitePress 侧边栏配置失败: {str(e)}")

    def update_vuepress_sidebar(self, repo_path: Path, filepath: Path) -> None:
        """更新 VuePress 配置文件，添加新日报到侧边栏。

        Args:
            repo_path: 仓库路径
            filepath: 日报文件路径
        """
        vuepress_dir = repo_path / "docs" / ".vuepress"
        if not vuepress_dir.exists():
            return
        
        config_files = ["config.ts", "config.js", "config.mjs"]
        config_path = None
        
        for cf in config_files:
            path = vuepress_dir / cf
            if path.exists():
                config_path = path
                break
        
        if not config_path:
            return
        
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                content = f.read()

            filename = filepath.name
            
            sidebar_pattern = r"(sidebar\s*:\s*\{[^}]*'/daily/'\s*:\s*\[\s*\{\s*text\s*:\s*'[^']+'\s*,\s*collapsible\s*:\s*false\s*,\s*children\s*:\s*)('auto'|'auto'|\[.*?\])"
            
            auto_detected = False
            sidebar_match = re.search(sidebar_pattern, content, re.DOTALL)
            if sidebar_match:
                current_children = sidebar_match.group(2)
                if "'auto'" in current_children:
                    auto_detected = True

            if auto_detected:
                print("✅ 检测到侧边栏配置使用 'auto' 模式")
                print("💡 新文件已添加，侧边栏将自动更新")
                print("⚠️  注意：如果 VuePress 开发服务器正在运行，请重启服务器以使新文件在侧边栏中显示")
            else:
                print("ℹ️  检测到侧边栏配置使用显式列表")
                print("💡 建议使用 'auto' 模式以支持自动检测新文件")
                print("⚠️  如需自动更新侧边栏，请将 children 修改为 'auto'")
        except Exception as e:
            print(f"⚠️  检测 VuePress 侧边栏配置失败: {str(e)}")

    def get_target_dir(self, repo_path: Path) -> Path:
        """获取目标目录路径。

        Args:
            repo_path: 仓库路径

        Returns:
            目标目录路径
        """
        repo_type = self.detect_repo_type(repo_path)

        if repo_type == "vitepress":
            base_dir = repo_path / "docs"
            
            nav_route = self.parse_vitepress_navbar(repo_path)
            if nav_route:
                target_dir = base_dir / nav_route
                print(f"检测到 VitePress 导航栏路由: /{nav_route}/")
                return target_dir
            else:
                print("未检测到导航栏路由，使用默认目录: docs/")
                return base_dir
        elif repo_type == "vuepress":
            base_dir = repo_path / "docs"
            
            nav_route = self.parse_vuepress_navbar(repo_path)
            if nav_route:
                target_dir = base_dir / nav_route
                print(f"检测到 VuePress 导航栏路由: /{nav_route}/")
                return target_dir
            else:
                print("未检测到导航栏路由，使用默认目录: docs/")
                return base_dir
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
        script_dir = Path(__file__).parent.parent
        cache_dir = script_dir / ".repo-cache"
        
        repo_path = self.clone_repo(cache_dir)
        filepath = self.write_report(content, repo_path)
        
        repo_type = self.detect_repo_type(repo_path)
        if repo_type == "vitepress":
            self.update_vitepress_base(repo_path)
            self.update_vitepress_sidebar(repo_path, filepath)
        elif repo_type == "vuepress":
            self.update_vuepress_sidebar(repo_path, filepath)
        
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
