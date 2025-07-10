# Terminal Stonks - 发布说明

## 项目概述

Terminal Stonks 是一个用于在终端中渲染股票 K 线图的 Python 库。它允许您直接在命令行界面中可视化股票数据，无需图形界面。

## 包结构

```
terminal-stonks/
├── terminal_stonks/          # 主包目录
│   ├── __init__.py          # 包初始化文件
│   └── k_chart.py           # 核心 KChart 类
├── tests/                   # 测试文件
│   ├── __init__.py
│   └── test_k_chart.py
├── .github/workflows/       # CI/CD 配置
│   └── publish.yml         # 自动发布 workflow
├── pyproject.toml          # 包配置文件
├── README.md               # 项目文档
├── LICENSE                 # MIT 许可证
├── MANIFEST.in             # 包文件清单
└── example.py              # 使用示例

```

## 发布到 PyPI

### 手动发布

1. 构建包：
```bash
python -m build
```

2. 上传到 Test PyPI（测试）：
```bash
python -m twine upload --repository testpypi dist/*
```

3. 上传到 PyPI（正式发布）：
```bash
python -m twine upload dist/*
```

### 自动发布

本项目配置了 GitHub Actions 自动发布工作流：

1. **测试发布**: 当推送版本标签（如 `v0.1.0`）时，自动发布到 Test PyPI
2. **正式发布**: 当创建 GitHub Release 时，自动发布到 PyPI

#### 发布步骤：

1. 更新版本号在 `pyproject.toml` 中
2. 创建并推送版本标签：
```bash
git tag v0.1.0
git push origin v0.1.0
```
3. 在 GitHub 上创建 Release（用于正式发布）

## 配置要求

### GitHub Secrets

需要在 GitHub 仓库设置中配置以下环境：

- `pypi`: 用于发布到 PyPI
- `testpypi`: 用于发布到 Test PyPI

### PyPI 配置

使用 Trusted Publishing 方式，无需在 GitHub 中设置 API 密钥：

1. 在 PyPI 上创建项目
2. 配置 Trusted Publishing，指向您的 GitHub 仓库
3. GitHub Actions 将自动获得发布权限

## 安装和使用

### 从 PyPI 安装

```bash
pip install terminal-stonks
```

### 基本使用

```python
import pandas as pd
from terminal_stonks import KChart

# 创建示例数据
data = pd.DataFrame({
    'Open': [100, 102, 101, 103, 105],
    'High': [105, 106, 104, 107, 108],
    'Low': [99, 101, 100, 102, 104],
    'Close': [102, 101, 103, 105, 107]
}, index=pd.date_range('2024-01-01', periods=5, freq='D'))

# 创建并渲染图表
chart = KChart(data)
chart.render(title="我的股票图表")
```

## 特性

- 🎨 美观的 ASCII 图表渲染
- 🌈 颜色编码的 K 线（红色看涨，绿色看跌）
- 📏 自动缩放以适应终端大小
- 📅 日期标签显示
- 💰 价格标签显示
- 🔄 兼容实时数据可视化

## 依赖要求

- Python 3.8+
- pandas >= 1.3.0
- rich >= 10.0.0

## 许可证

MIT License - 详见 LICENSE 文件

## 贡献

欢迎贡献！请查看 README.md 了解贡献指南。

## 版本历史

### 0.1.0 (初始版本)
- 基本的 K 线图渲染功能
- 自动缩放图表
- 颜色编码的看涨/看跌 K 线
- 日期和价格轴标签 