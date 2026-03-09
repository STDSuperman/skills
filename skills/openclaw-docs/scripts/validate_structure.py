#!/usr/bin/env python3
"""
文档结构验证器
检测文档框架是否发生根本性变化
"""

import json
from pathlib import Path
from typing import Dict, Tuple


class StructureValidationError(Exception):
    """文档结构验证失败异常"""
    pass


def validate_docs_structure(repo_path: Path) -> Tuple[bool, str]:
    """
    验证文档结构是否符合预期

    Args:
        repo_path: 仓库路径

    Returns:
        (是否有效, 错误信息)

    Raises:
        StructureValidationError: 验证失败时抛出
    """
    docs_json = repo_path / 'docs' / 'docs.json'

    # 检查 1: docs.json 是否存在
    if not docs_json.exists():
        raise StructureValidationError(
            "❌ 文档结构已改变：docs.json 文件不存在\n"
            f"   预期路径: {docs_json}\n"
            "   可能原因: 仓库已切换到新的文档框架\n"
            "   建议: 需要重新设计文档解析策略"
        )

    # 检查 2: 能否解析 JSON
    try:
        with open(docs_json, encoding='utf-8') as f:
            config = json.load(f)
    except json.JSONDecodeError as e:
        raise StructureValidationError(
            f"❌ 文档结构已改变：docs.json 格式无效\n"
            f"   错误: {e}\n"
            "   建议: 需要重新设计文档解析策略"
        )

    # 检查 3: navigation 字段是否存在
    if 'navigation' not in config:
        raise StructureValidationError(
            "❌ 文档结构已改变：docs.json 缺少 'navigation' 字段\n"
            "   当前结构与预期不符\n"
            "   建议: 需要重新设计文档解析策略"
        )

    # 检查 4: navigation.languages 字段是否存在
    if 'languages' not in config['navigation']:
        raise StructureValidationError(
            "❌ 文档结构已改变：docs.json 缺少 'navigation.languages' 字段\n"
            "   当前结构与预期不符\n"
            "   建议: 需要重新设计文档解析策略"
        )

    # 检查 5: 是否有英文语言配置
    languages = config['navigation']['languages']
    if not isinstance(languages, list) or len(languages) == 0:
        raise StructureValidationError(
            "❌ 文档结构已改变：navigation.languages 不是有效的列表\n"
            "   建议: 需要重新设计文档解析策略"
        )

    en_config = None
    for lang in languages:
        if lang.get('language') == 'en':
            en_config = lang
            break

    if not en_config:
        raise StructureValidationError(
            "❌ 文档结构已改变：未找到英文文档配置\n"
            "   可能原因: 仓库不再提供英文文档\n"
            "   建议: 需要重新设计文档解析策略"
        )

    # 检查 6: 英文配置下是否有 tabs
    if 'tabs' not in en_config or not en_config['tabs']:
        raise StructureValidationError(
            "❌ 文档结构已改变：英文配置下没有 tabs\n"
            "   建议: 需要重新设计文档解析策略"
        )

    # 检查 7: 是否能解析出至少一个文档
    has_valid_doc = False
    for tab in en_config['tabs']:
        if 'groups' in tab and tab['groups']:
            for group in tab['groups']:
                if 'pages' in group and group['pages']:
                    has_valid_doc = True
                    break
        if has_valid_doc:
            break

    if not has_valid_doc:
        raise StructureValidationError(
            "❌ 文档结构已改变：无法从 docs.json 解析出任何文档\n"
            "   建议: 需要重新设计文档解析策略"
        )

    # 检查 8: docs 目录是否存在
    docs_dir = repo_path / 'docs'
    if not docs_dir.exists() or not docs_dir.is_dir():
        raise StructureValidationError(
            f"❌ 文档结构已改变：docs 目录不存在\n"
            f"   预期路径: {docs_dir}\n"
            "   建议: 需要重新设计文档解析策略"
        )

    return True, "✅ 文档结构验证通过"


if __name__ == '__main__':
    import sys
    from pathlib import Path

    # 设置 UTF-8 输出
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    SCRIPT_DIR = Path(__file__).parent
    SKILL_DIR = SCRIPT_DIR.parent

    # 加载配置
    config_file = SKILL_DIR / 'references' / 'config.json'
    with open(config_file) as f:
        config = json.load(f)

    repo_path = SKILL_DIR / config['repo_path']

    try:
        is_valid, message = validate_docs_structure(repo_path)
        print(message)
        sys.exit(0)
    except StructureValidationError as e:
        print(str(e))
        sys.exit(1)
