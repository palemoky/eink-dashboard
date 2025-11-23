# Git Hooks

本项目使用 Git hooks 来自动化代码质量检查。

## 安装 Hook

```bash
# 配置 Git 使用项目中的 hooks 目录
git config core.hooksPath githooks
```

## Pre-commit Hook

在每次提交前自动运行以下检查：

1. **Black** - 代码格式化
2. **isort** - 导入语句排序
3. **Ruff** - 代码质量检查

如果格式化工具发现问题，会自动修复并重新暂存文件。如果 ruff 发现问题，会阻止提交并提示修复。

## Pre-push Hook

在每次推送前自动运行：

1. **pytest** - 运行所有测试

只有当推送的提交中包含 Python 文件修改时才会运行测试。如果测试失败，会阻止推送。

## 跳过 Hook（不推荐）

如果需要临时跳过 hook：
```bash
git commit --no-verify  # 跳过 pre-commit
git push --no-verify    # 跳过 pre-push
```

## 手动运行检查

```bash
# 格式化所有代码
black src/ tests/
isort src/ tests/

# 检查代码质量
ruff check src/ tests/

# 运行测试
PYTHONPATH=. pytest tests/
```
