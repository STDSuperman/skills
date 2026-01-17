# 项目类型视觉风格详解

> 本文件定义了不同项目类型的ZONE 2和ZONE 3内容配置，确保视觉风格与项目类型完全匹配。

---

## ZONE 2: 主要可视化区域配置

### Type 1: Web App / UI-Heavy Projects

**触发条件**: 项目具有图形用户界面、Web应用、前端项目

**配置内容**:

```markdown
// [IF TYPE IS "Web App" OR "UI-Heavy Project"]

- Main Visual: A high-fidelity **[UI RENDER]** of the application's main screen, showing a dashboard or key feature.

- Underlay: A slightly offset **[WIREFRAME BLUEPRINT (线框蓝图)]** of the same UI, revealing the structural layout.

- Floating Elements: Small, glowing cards representing UI components like "Button Kit", "Color Palette", "Icon Set".

- Label: "界面实例 (UI INSTANCE)"
```

**视觉焦点**: 渲染后的UI + 线框蓝图叠加

**适合示例**: React应用、Vue项目、仪表盘、管理系统

---

### Type 2: AI Model / Data Pipeline

**触发条件**: 机器学习模型、数据处理管道、AI项目

**配置内容**:

```markdown
// [IF TYPE IS "AI Model" OR "Data Pipeline"]

- Main Visual: A multi-layered, exploded view of a **[DATA PACKET or MODEL DIAGRAM]**.

- Top Layer: A card labeled with the primary input, e.g., "Input: User Query (用户查询)".

- Middle Layer: A visualization of the processing stage, e.g., "Processing: Transformer Blocks (处理：转换器模块)".

- Bottom Layer: A card showing the final output, e.g., "Output: Generated Text (输出：生成文本)".

- Floating Elements: Icons representing data sources or formats, like "API", "JSON", "VectorDB".

- Label: "数据流剖面 (DATAFLOW PROFILE)"
```

**视觉焦点**: 数据管道分层展示

**适合示例**: Transformer模型、数据处理管道、API服务、ETL流程

---

### Type 3: Library / Developer Tool

**触发条件**: 命令行工具、开发库、后端服务、无GUI项目

**配置内容**:

```markdown
// [IF TYPE IS "Library" OR "Developer Tool"]

- Main Visual: An exploded, 3D visualization of the **[CORE MODULE ARCHITECTURE (核心模块架构)]**.

- Top Layer: A glowing document card labeled with the main configuration file, e.g., "config.yaml" or "main.py".

- Middle Layer: Transparent blocks of code representing key functions or classes, e.g., "class Parser", "function execute()".

- Bottom Layer: A collection of resource assets like templates or plugins.

- Floating Elements: Badges for key dependencies, like "Pandas", "FastAPI", "React".

- Label: "架构分解 (ARCHITECTURE EXPLODED)"
```

**视觉焦点**: 核心模块架构分解图

**适合示例**: Python库、CLI工具、Rust工具、后端API、开发框架

---

## ZONE 3: 工程结构区域配置

### Type 1: Web App / UI-Heavy Projects

```markdown
// [IF TYPE IS "Web App" OR "UI-Heavy Project"]

- Main Panel: A detailed **"File Explorer & Component Tree" (文件与组件树)**.
    - Visuals: Vertical list of Folders (e.g., 📂 `components`, 📂 `pages`, 📂 `assets`), and Files (e.g., 📄 `Button.tsx`, 📄 `api.ts`).
    - Style: Clean, high-contrast UI list.

- Sub-Panel (Bottom Strip): A **Miniature Command Line**.
    - Content: A single line showing a relevant build or run command, e.g., `> npm run dev [RUNNING]` in amber text.

- Label: "前端工程 (FRONTEND ENGINEERING)".
```

**默认命令** (如果未找到明确命令):
```
> npm install && npm run dev
```

---

### Type 2: AI Model / Data Pipeline

```markdown
// [IF TYPE IS "AI Model" OR "Data Pipeline"]

- Main Panel: A split view showing a **"File Explorer"** on the left and a **"Configuration Snippet"** on the right.
    - File Explorer: Shows relevant data science project structure (e.g., 📂 `data`, 📂 `models`, 📄 `train.py`, 📄 `config.yaml`).
    - Config Snippet: A small window displaying key parameters from a config file (e.g., `learning_rate: 0.001`, `batch_size: 32`).

- Sub-Panel (Bottom Strip): A **Miniature Command Line**.
    - Content: A single line showing a training or inference command, e.g., `> python train.py --epochs 100 [TRAINING]`.

- Label: "模型结构 (MODEL STRUCTURE)".
```

**默认命令** (如果未找到明确命令):
```
> pip install [PROJECT_NAME]
```

---

### Type 3: Library / Developer Tool

```markdown
// [IF TYPE IS "Library" OR "Developer Tool"]

- Main Panel: A detailed **"File Explorer"** showing the library's source code structure.
    - Visuals: Vertical list of key modules and files (e.g., 📂 `src/core`, 📂 `tests`, 📄 `main.py`, 📄 `pyproject.toml`).

- Sub-Panel (Bottom Strip): A **Miniature Command Line**.
    - Content: A single line showing a test or publish command, e.g., `> pytest -v [PASS]` in green text.

- Label: "库结构 (LIBRARY STRUCTURE)".
```

**默认命令** (如果未找到明确命令):
```
> ./build.sh --release
```

---

## 数据验证与回退协议 (CRITICAL)

### 1. 安装与操作逻辑检查

**检测流程**:
1. 识别主要包管理器/构建系统:
   - `package.json` → `npm`
   - `requirements.txt` / `setup.py` → `pip`
   - `Cargo.toml` → `cargo`
   - `go.mod` → `go build`

2. 提取标准安装或运行命令

3. **回退策略** (如果未找到明确命令):
   - Web App → `> npm install && npm run dev`
   - Python Library → `> pip install [PROJECT_NAME]`
   - General/Unknown → `> ./build.sh --release`

**约束**: 命令必须简短（最多40字符），以适应"Miniature Command Line"视觉效果

---

### 2. 视觉资产现实检查

**检查项**: 项目是否真的有GUI?

**操作**:
- 如果项目是CLI/后端工具 → **强制**将视觉风格设为"Library/Tool"
- **禁止**为命令行工具生成"UI Render"

---

### 3. 指标数据清洗

**检查项**: Stars、Forks或版本是否有具体数字?

**操作**:
- 版本未知 → 使用 "v1.0.0" 或 "LATEST"
- Stars/Forks未知 → 使用 "N/A" 或移除该指标
- **CRITICAL**: 确保最终提示词中不保留任何 `[NUM]` 或 `[INSERT]` 占位符

---

## 颜色主题映射

根据技术栈logo自动确定主题色:

| 技术栈 | 主题色 | RGB参考 |
|--------|--------|---------|
| Python | Blue/Yellow | `#306998` / `#FFD43B` |
| JavaScript/Node | Yellow | `#F7DF1E` |
| React | Cyan/Blue | `#61DAFB` |
| Vue | Green | `#42B883` |
| Rust | Orange/Red | `#DEA584` / `#000000` |
| Go | Cyan | `#00ADD8` |
| TypeScript | Blue | `#3178C6` |
| Java | Red/Blue | `#007396` / `#E76F00` |

---

## 深度本地化规则

**核心目标**: 生成几乎完全中文的界面

**转换示例**:
- "Deploy" → "部署"
- "Build" → "构建"
- "Configuration" → "配置"
- "Pipeline" → "管道"
- "Dependencies" → "依赖"
- "Components" → "组件"

**保留英文的场景**:
- 代码中的特定关键词
- 专有技术名词（如 React, Transformer）
- 命令行命令
