# CLAUDE.md 更新指南

## 核心原则

只添加真正能帮助未来 Claude 会话的信息。上下文窗口是宝贵资源——每一行都必须证明
自己的价值。

---

## 应该写什么（5 类）

### 1. 已发现的命令和工作流

```markdown
## Build

`npm run build:prod` - Full production build with optimization
`npm run build:dev` - Fast dev build (no minification)
```

**为什么写**：避免未来的会话重新摸索这些命令。

### 2. Gotchas 和非显而易见的模式

```markdown
## Gotchas

- Tests must run sequentially (`--runInBand`) due to shared DB state
- `yarn.lock` is authoritative; delete `node_modules` if deps mismatch
```

**为什么写**：防止重复踩坑，节省调试时间。

### 3. 包/模块之间的依赖关系

```markdown
## Dependencies

The `auth` module depends on `crypto` being initialized first.
Import order matters in `src/bootstrap.ts`.
```

**为什么写**：架构知识无法从代码直接推断，是最需要显式说明的信息。

### 4. 已验证有效的测试方法

```markdown
## Testing

For API endpoints: Use `supertest` with the test helper in `tests/setup.ts`
Mocking: Factory functions in `tests/factories/` (not inline mocks)
```

**为什么写**：确立已经验证有效的测试模式，避免走弯路。

### 5. 配置和环境的特殊行为

```markdown
## Config

- `NEXT_PUBLIC_*` vars must be set at build time, not runtime
- Redis connection requires `?family=0` suffix for IPv6
```

**为什么写**：环境特有的知识，任何代码都看不出来，必须显式记录。

---

## 不应该写什么（4 类）

### 1. 代码已经说明的内容

**不好的写法：**
```markdown
The `UserService` class handles user operations.
```

类名本身已经说明了这一点，无需重复。

### 2. 通用编程最佳实践

**不好的写法：**
```markdown
Always write tests for new features.
Use meaningful variable names.
```

这是普遍适用的建议，不是项目特有信息。

### 3. 一次性修复记录

**不好的写法：**
```markdown
We fixed a bug in commit abc123 where the login button didn't work.
```

不会复现，只会污染文件。

### 4. 啰嗦的解释

**不好的写法：**
```markdown
The authentication system uses JWT tokens. JWT (JSON Web Tokens) are
an open standard (RFC 7519) that defines a compact and self-contained
way for securely transmitting information between parties as a JSON
object. In our implementation, we use the HS256 algorithm which...
```

**好的写法：**
```markdown
Auth: JWT with HS256, tokens in `Authorization: Bearer <token>` header.
```

---

## Diff 输出格式

每个建议修改按以下三段格式输出：

### 第一段：标明文件和位置

```
File: ./CLAUDE.md
Section: Commands（新增到 ## Architecture 之后）
```

### 第二段：展示变更

```diff
 ## Architecture
 ...

+## Commands
+
+| Command | Purpose |
+|---------|---------|
+| `npm run dev` | Dev server with HMR |
+| `npm run build` | Production build |
+| `npm test` | Run test suite |
```

### 第三段：说明原因

> **为什么这样改**：构建命令未记录，导致新会话不知道如何运行项目。补充后可节省
> 重复查找 `package.json` 的时间。

---

## 改文件的操作规范

- **使用 Edit 精确替换**，不要用 Write 全量覆盖，除非是大规模重写
- **改完再过自检清单**（见 SKILL.md 的 §A.3）
- **先展示 diff，等用户确认**，再实际修改文件

---

## 验证清单

提交更新前逐项确认：

- [ ] 每条新增内容都是项目特有的
- [ ] 无通用建议或显而易见的信息
- [ ] 命令已实际运行并验证可用
- [ ] 文件路径准确存在
- [ ] 新会话的 Claude 确实需要这条信息
- [ ] 已用最简洁的方式表达
