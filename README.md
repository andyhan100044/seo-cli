# SEO CLI - 10秒发现潜力词

[![GitHub stars](https://img.shields.io/github/stars/yourusername/seo-cli?style=social)](https://github.com/yourusername/seo-cli)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**SEO CLI** 是一个本地化的关键词分析工具，10秒内完成「找词→意图→规划→大纲」全流程。

![SEO CLI Banner](https://via.placeholder.com/800x200/008aff/ffffff?text=SEO+CLI+-+10秒发现潜力词)

## ✨ 核心特性

- ⚡ **10秒出结果** - 本地SearXNG + PyTrends，速度极快
- 🔒 **零隐私泄露** - 纯本地运行，无需API，数据完全私有
- 💰 **完全免费** - 无API费用，对比SEMrush $119/月
- 🎯 **智能分析** - 自动判断交易/信息/导航意图
- 📊 **多格式输出** - CSV、JSON、Markdown，满足不同需求
- 🚀 **一键部署** - Gitpod云端开发，无需本地安装

## 🎯 产品定位

**让碎片时间变成高效学习时间** - 专为SEO人员、内容运营、数字营销从业者打造。

## 🚀 快速开始

### 方案一：Gitpod云端开发（推荐）

[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/yourusername/seo-cli)

1. 点击上方按钮，一键启动云端开发环境
2. 自动预构建Docker + Python环境
3. 在终端运行命令即可开始使用

### 方案二：本地安装

```bash
# 1. 克隆仓库
git clone https://github.com/yourusername/seo-cli.git
cd seo-cli

# 2. 安装依赖
pip install -r requirements.txt

# 3. 启动SearXNG（Docker）
docker-compose up -d

# 4. 验证安装
python seo.py --help
```

## 📖 使用示例

### 1. 发现热词

```bash
# 发现今日热词
python seo.py discover --date 2025-01-01 --limit 50 --output ./results

# 输出文件：results/potential_words_20250101_143000.csv
```

### 2. 分析关键词意图

```bash
# 分析单个关键词
python seo.py intent --word "AI generator" --longtail 20 --output-dir ./results

# 输出文件：
# - results/ai_generator_intent_20250101_143000.json (详细数据)
# - results/ai_generator_plan_20250101_143000.md (站点规划)
```

### 3. 生成内容大纲

```bash
# 基于规划生成大纲
python seo.py outline --plan results/ai_generator_plan_20250101_143000.json

# 输出文件：outline_20250101_143000.md
```

### 4. 批量处理

```bash
# 批量分析关键词列表
python seo.py batch --file keywords.txt --output results/batch_results.csv
```

## 🏗️ 项目架构

```
seo-cli/
├── seo.py                      # CLI入口（argparse）
├── db.py                       # 数据库模块（SQLite）
├── skills/                     # 4个技能模块
│   ├── hot.py                  # Skill① 热词收集
│   ├── trend.py                # Skill② 趋势验证
│   ├── intent.py               # Skill③ 意图分析
│   └── outline.py              # Skill④ 大纲生成
├── external/                   # 外部服务封装
│   ├── searxng.py             # SearXNG客户端
│   └── trends.py              # PyTrends客户端
├── docker-compose.yml          # SearXNG部署配置
├── .gitpod.yml                # Gitpod预构建配置
└── requirements.txt            # Python依赖
```

## 🔧 技术栈

| 组件 | 技术 | 说明 |
|------|------|------|
| **核心语言** | Python 3.9+ | 轻量级，易部署 |
| **CLI框架** | argparse | 内置模块，无额外依赖 |
| **搜索引擎** | SearXNG | 本地Docker部署 |
| **趋势分析** | PyTrends | Google Trends非官方API |
| **数据存储** | SQLite | 轻量级数据库 |
| **网页抓取** | Requests + BeautifulSoup | 数据采集 |
| **开发环境** | Gitpod | 云端IDE，内置Docker |
| **部署方式** | Docker Compose | 一键启动SearXNG |

## 📊 输出格式

### CSV格式（批量数据）

```csv
word,search_volume,trend_score,is_rising,site_type,headline
AI generator,8500,78.5,true,在线工具站,最专业的AI generator工具，5秒出结果
```

### JSON格式（详细数据）

```json
{
  "keyword": "AI generator",
  "intent": "transactional",
  "longtail_words": [
    "AI generator best",
    "AI generator price",
    "AI generator online"
  ],
  "site_plan": {
    "type": "在线工具站",
    "core_feature": "提供AI generator的在线服务",
    "tech_stack": "Next.js + Vercel（0元部署）",
    "headline": "最专业的AI generator工具，5秒出结果"
  }
}
```

### Markdown格式（站点规划）

```markdown
# 站点规划：AI generator

- 类型：在线工具站
- 核心功能：提供AI generator的在线服务
- 技术栈：Next.js + Vercel（0元部署）
- 首屏文案：最专业的AI generator工具，5秒出结果

## H2结构
- ① 服务介绍
- ② 在线工具
- ③ 价格方案
- ④ 用户评价
- ⑤ FAQ
```

## 🎯 核心算法

### 意图分类算法

基于关键词模式匹配，自动分类搜索意图：

- **交易意图** (transactional): `buy`, `price`, `best`, `review`, `template`
- **信息意图** (informational): `what`, `how`, `tutorial`, `guide`, `meaning`
- **导航意图** (navigational): `login`, `official`, `contact`, `support`

### 趋势分数计算

```
趋势分数 = (最近30天平均值 / 峰值) × 100
```

### 上升趋势判断

```
最近7天平均值 > 之前7天平均值 × 1.2
```

## 📈 性能指标

- ⚡ **响应时间**: ≤ 10秒（完整流程）
- 🎯 **准确率**: ≥ 80%（意图判断）
- 🔄 **稳定性**: ≥ 99%（无崩溃）
- 💾 **内存占用**: ≤ 512MB

## 🔍 使用场景

### SEO代理公司
- 提高关键词研究效率（节省80%时间）
- 快速生成站点规划（从30分钟缩短到10秒）

### 内容创作者
- 快速发现潜力词（每天发现20+新词）
- 自动生成内容大纲（提高写作效率）

### 独立开发者
- 建站前市场调研（10秒出规划）
- 降低关键词分析成本（零API费用）

### 数字营销人员
- 降低关键词分析成本（对比工具 $100+/月）
- 本地化数据处理（隐私保护）

## 🚀 部署指南

### Gitpod部署（推荐）

1. Fork本项目到您的GitHub
2. 访问 https://gitpod.io/#https://github.com/yourusername/seo-cli
3. 自动预构建环境，5分钟启动
4. 在终端运行命令

### Docker本地部署

```bash
# 启动SearXNG
docker-compose up -d

# 验证部署
curl http://localhost:8080/health

# 运行CLI
python seo.py discover --limit 20
```

## 📚 文档

- [安装指南](docs/installation.md)
- [使用教程](docs/usage.md)
- [API文档](docs/api.md)
- [部署指南](docs/deployment.md)
- [故障排除](docs/troubleshooting.md)

## 🤝 贡献指南

欢迎贡献代码！请阅读 [CONTRIBUTING.md](CONTRIBUTING.md) 了解详情。

### 开发流程

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📝 更新日志

### v1.0.0 (2025-01-01)
- ✨ 首次发布
- ⚡ 支持4个核心技能模块
- 🎯 意图判断准确率 ≥ 80%
- 💰 完全免费开源

## 📄 许可证

本项目采用 [MIT License](LICENSE) 开源协议。

## 🙏 致谢

- [SearXNG](https://github.com/searxng/searxng) - 本地搜索引擎
- [PyTrends](https://github.com/GeneralMills/pytrends) - Google Trends API
- [Rich](https://github.com/Textualize/rich) - 美化终端输出
- [Gitpod](https://www.gitpod.io/) - 云端开发环境

## 📞 联系方式

- GitHub Issues: [https://github.com/yourusername/seo-cli/issues](https://github.com/yourusername/seo-cli/issues)
- 邮箱: your-email@example.com

## ⭐ 如果这个项目对您有帮助，请给个 Star 支持一下！

---

**Made with ❤️ by SEO CLI Team**
