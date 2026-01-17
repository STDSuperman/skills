# Midjourney 提示词生成模板

> 本文件包含完整的Midjourney提示词模板，确保保留所有艺术风格和分析框架。

## 使用说明

当完成项目分析后，使用本模板生成最终的Midjourney提示词。根据分析结果填写所有占位符。

---

## 完整提示词模板

```markdown
/imagine prompt: A high-density [ORIENTATION] technical visualization of "[CHINESE PROJECT NAME]".

[VERSION: V10.2 CRYSTAL SLATE UI-DENSITY]

// --- 1. VIEWPORT & PHYSICS (NON-NEGOTIABLE) ---

[Perspective]: **Strict 90° Top-Down Flat-Lay**. Like a high-res document scan. Absolutely perpendicular.

[Object]: A single, massive **"Integrated Smart Glass Slate" (全息玻璃板)** covering 97% of the canvas.

[Background]: **Adaptive Gaussian Ambient**. A heavy, smooth Gaussian blur gradient derived from the interface's dominant colors (Frosted Glass / Ambient Glow effect). Soft, diffused, glowing backdrop. No paper texture.

[Style]: Apple Bento Grids meets Industrial Control Panel. Clean, Organized, Information-Dense.


// --- 2. LAYOUT STRATEGY: [ORIENTATION] ---

// IF VERTICAL: "Vertical Waterfall Layout". Zone 2 (Top), Zone 3 (Middle), Zone 4 (Bottom). Tightly stacked.

// IF HORIZONTAL: "Bento Grid Layout". Zone 2 (Left Big), Zone 3 (Right Top), Zone 4 (Right Bottom).


// --- 3. THE CONTENT ZONES ---

// [ZONE 1: HEADER - IDENTITY]
- Strip: Title "[CHINESE PROJECT NAME]" + Badges "[LICENSE] / [VERSION]".

// [ZONE 2: PRIMARY VISUAL - THE CORE VISUALIZATION]
// Purpose: Dynamically showcase the project's core based on its type.

[根据项目类型选择以下对应的ZONE 2内容 - 见visual-styles.md]

// [ZONE 3: ENGINEERING - STRUCTURE & OPERATIONS]
// Purpose: Showcase the project's engineering backbone, adapted to its type.

[根据项目类型选择以下对应的ZONE 3内容 - 见visual-styles.md]

// [ZONE 4: PROJECT IDENTITY & METRICS HUB - RIGHT BOTTOM]

// Container: A unified, sleek glassmorphism card

// --- HEADER: IDENTITY (Module B Integrated) ---
- Alignment: Top Row.
- Typography: "[PROJECT NAME]" (Bold, White, Sans-serif) + Label: "[VERSION]" (Neon Accent Badge).
- Elements: A cluster of 3-4 small, 3D transparent glass cubes floating in the top-right corner. Each cube encases a glowing [TECH STACK] icon, casting subtle refractions.

// --- BODY: VISUALIZATION CORE ---
- Content: A dynamic [CHART TYPE] (e.g., Force-Directed Graph or Radar Chart).
- Context: Visualizing [DATA FLOW OR DEPENDENCY] within the project.
- Backdrop: Subtle grid lines and watermark text: "数据拓扑 (TOPOLOGY)".

// --- FOOTER: METADATA STREAM ---
- Alignment: Bottom edge strip.
- Font: Monospace, small size, high contrast.
- Data Stream: "Stars: [NUM]  |  Forks: [NUM]  |  Contributors: [NUM]  |  Lang: [LANGUAGE]"


// --- 4. TEXT & DETAILING ---

[Typography]: **Simplified Chinese (Sans-Serif)**. Crisp, legible, white and dark grey text.
[Decor]: Minimalist icons (Folder, Git Branch, Server, User) strictly aligned to the grid.
[Color Palette]: **Titanium White** (Glass Base) + **[THEME COLOR]** (Highlights) + **Deep Graphite** (Text).


--ar [ASPECT RATIO] --stylize 250 --v 6.1 4k high resolution
--no tilt, isometric, 3d angle, floating, levitating, drop shadow, depth of field, messy, handwritten, camera parameters, zone position number, repeat elements or module, illegle Chinese text
```

---

## 占位符填写指南

### 基础信息
- `[ORIENTATION]`: 布局方向 - `landscape` (横向) 或 `portrait` (纵向)
- `[CHINESE PROJECT NAME]`: 项目中文名称
- `[PROJECT NAME]`: 项目英文名称
- `[VERSION]`: 版本号
- `[LICENSE]`: 许可证类型

### 技术信息
- `[TECH STACK]`: 技术栈（如 Python, React, Rust）
- `[LANGUAGE]`: 主要编程语言
- `[THEME COLOR]`: 主题色（基于技术栈logo颜色）

### GitHub指标
- `[NUM]`: 具体数字（Stars/Forks/Contributors）
- **CRITICAL**: 不得使用 `[NUM]` 或 `[INSERT]` 等占位符，必须填入具体数值或 "N/A"

### 布局参数
- `[ASPECT RATIO]`: 宽高比 - `16:9` (landscape) 或 `9:16` (portrait)

### ZONE 2 & 3 内容
- 根据项目类型从 `visual-styles.md` 中选择对应的配置
- Web App → UI Render + Wireframe
- Library/Tool → File Structure + Config Panels
- AI Model → Data Pipeline + Inference Stats

---

## 重要约束

1. **语言强制**: 所有UI标签和描述文本必须使用简体中文
2. **视角固定**: 严格90°俯视，不允许任何角度倾斜
3. **数据真实**: 不得使用占位符，未知数据使用 "N/A" 或 "LATEST"
4. **视觉一致**: CLI工具必须强制使用"Library/Tool"风格，不得生成UI渲染
