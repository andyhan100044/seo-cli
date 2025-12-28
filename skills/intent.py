"""
SEO CLI - Skill③: Intent Analysis & Site Planning
Analyze keyword intent and generate site plans
"""

import re
import json
from datetime import datetime
from typing import List, Dict

def analyze_intent(keyword: str, longtail_count: int = 20) -> Dict:
    """
    Analyze keyword intent and generate site plan

    Args:
        keyword: Target keyword to analyze
        longtail_count: Number of longtail keywords to generate

    Returns:
        Dictionary with intent analysis and site plan
    """
    # Classify intent
    intent_type = classify_intent(keyword)

    # Generate longtail keywords
    longtail_words = generate_longtail(keyword, intent_type, longtail_count)

    # Generate site plan
    site_plan = generate_site_plan(keyword, intent_type, longtail_words)

    return {
        'keyword': keyword,
        'intent': intent_type,
        'longtail_words': longtail_words,
        'site_plan': site_plan,
        'analysis_date': datetime.now().isoformat()
    }

def classify_intent(keyword: str) -> str:
    """
    Classify search intent based on keyword patterns

    Args:
        keyword: Keyword to classify

    Returns:
        Intent type: 'transactional', 'informational', or 'navigational'
    """
    keyword_lower = keyword.lower()

    # Transactional intent patterns
    transactional_patterns = [
        r'\b(buy|price|cost|cheap|discount|deal|sale|order|shop|store|purchase)\b',
        r'\b(best|top|review|compare|vs|alternative|service|provider|company)\b',
        r'\b(template|plugin|tool|software|app|generator|creator|maker)\b',
        r'\b(online|free|download|hire|hire|freelancer)\b'
    ]

    # Informational intent patterns
    informational_patterns = [
        r'\b(what|how|why|when|where|who|which)\b',
        r'\b(tutorial|guide|learn|understand|explain|tips|tricks|strategy)\b',
        r'\b(meaning|definition|vs|difference|similarity|examples|cases)\b',
        r'\b(about|info|information|overview|introduction|basics|introduction)\b'
    ]

    # Navigational intent patterns
    navigational_patterns = [
        r'\b(login|signin|portal|dashboard|account|profile)\b',
        r'\b(facebook|youtube|instagram|twitter|linkedin|github)\b',
        r'\b(company name|brand name|website|site|homepage)\b',
        r'\b(docs|documentation|wiki|help|support)\b'
    ]

    # Check patterns
    for pattern in transactional_patterns:
        if re.search(pattern, keyword_lower):
            return 'transactional'

    for pattern in informational_patterns:
        if re.search(pattern, keyword_lower):
            return 'informational'

    for pattern in navigational_patterns:
        if re.search(pattern, keyword_lower):
            return 'navigational'

    # Default to informational
    return 'informational'

def generate_longtail(keyword: str, intent_type: str, count: int) -> List[str]:
    """
    Generate longtail keywords based on intent type

    Args:
        keyword: Base keyword
        intent_type: Intent type
        count: Number of longtail keywords to generate

    Returns:
        List of longtail keywords
    """
    longtail_templates = {
        'transactional': [
            f"{keyword} best",
            f"{keyword} price",
            f"{keyword} buy online",
            f"{keyword} discount",
            f"{keyword} review",
            f"{keyword} vs",
            f"{keyword} comparison",
            f"buy {keyword}",
            f"{keyword} for sale",
            f"{keyword} deal",
            f"{keyword} cheap",
            f"{keyword} free",
            f"{keyword} template",
            f"{keyword} tool",
            f"{keyword} software",
            f"{keyword} app",
            f"{keyword} service",
            f"{keyword} provider",
            f"{keyword} company",
            f"{keyword} hire"
        ],
        'informational': [
            f"what is {keyword}",
            f"how to {keyword}",
            f"{keyword} tutorial",
            f"{keyword} guide",
            f"{keyword} meaning",
            f"{keyword} examples",
            f"why {keyword}",
            f"{keyword} benefits",
            f"{keyword} tips",
            f"{keyword} tricks",
            f"{keyword} strategy",
            f"{keyword} definition",
            f"{keyword} vs",
            f"{keyword} introduction",
            f"{keyword} basics",
            f"{keyword} overview",
            f"{keyword} information",
            f"{keyword} learn",
            f"{keyword} understand",
            f"{keyword} explained"
        ],
        'navigational': [
            f"{keyword} login",
            f"{keyword} official site",
            f"{keyword} contact",
            f"{keyword} support",
            f"{keyword} help",
            f"{keyword} documentation",
            f"{keyword} wiki",
            f"{keyword} dashboard",
            f"{keyword} account",
            f"{keyword} profile"
        ]
    }

    # Get base templates
    base_templates = longtail_templates.get(intent_type, longtail_templates['informational'])

    # Generate additional variations with modifiers
    modifiers = ['2024', 'online', 'free', 'new', 'best', 'top', 'fast', 'easy', 'simple', 'advanced']

    extended = []
    for template in base_templates:
        extended.append(template)
        for modifier in modifiers:
            extended.append(f"{modifier} {template}")

    # Remove duplicates and return requested count
    unique_longtails = list(dict.fromkeys(extended))

    return unique_longtails[:count]

def generate_site_plan(keyword: str, intent_type: str, longtail_words: List[str]) -> Dict:
    """
    Generate site plan based on intent type

    Args:
        keyword: Target keyword
        intent_type: Intent type
        longtail_words: List of longtail keywords

    Returns:
        Site plan dictionary
    """
    plan_templates = {
        'transactional': {
            'type': '在线工具站',
            'core_feature': f'提供{keyword}的在线服务',
            'tech_stack': 'Next.js + Vercel（0元部署）',
            'headline': f'最专业的{keyword}工具，5秒出结果',
            'h2_structure': [
                '① 服务介绍',
                '② 在线工具',
                '③ 价格方案',
                '④ 用户评价',
                '⑤ FAQ'
            ],
            'content_strategy': '围绕工具功能布局，突出便捷性和效果',
            'monetization': '免费试用 + 付费订阅模式'
        },
        'informational': {
            'type': '博客/知识库',
            'core_feature': f'{keyword}专业教程和资讯',
            'tech_stack': 'Hugo + GitHub Pages（免费）',
            'headline': f'{keyword}完整指南：从入门到精通',
            'h2_structure': [
                '① 基础知识',
                '② 进阶教程',
                '③ 实战案例',
                '④ 常见问题',
                '⑤ 资源推荐'
            ],
            'content_strategy': '围绕教程和指南布局，建立权威性',
            'monetization': '广告 + 联盟营销 + 课程销售'
        },
        'navigational': {
            'type': '导航/门户站',
            'core_feature': f'{keyword}相关资源导航',
            'tech_stack': '静态HTML + GitHub Pages',
            'headline': f'{keyword}一站式导航平台',
            'h2_structure': [
                '① 官方资源',
                '② 第三方工具',
                '③ 教程资源',
                '④ 社区讨论',
                '⑤ 最新动态'
            ],
            'content_strategy': '围绕资源导航布局，提供一站式服务',
            'monetization': '广告 + 联盟推广'
        }
    }

    # Get template for intent type
    template = plan_templates.get(intent_type, plan_templates['informational'])

    return {
        **template,
        'keyword': keyword,
        'longtail_coverage': len(longtail_words),
        'longtail_keywords': longtail_words[:10],  # Include top 10 longtails in plan
        'seo_strategy': f'重点优化"{keyword}"主词，布局{len(longtail_words)}个长尾词',
        'target_audience': get_target_audience(intent_type),
        'success_metrics': get_success_metrics(intent_type)
    }

def get_target_audience(intent_type: str) -> str:
    """Get target audience description based on intent type"""
    audiences = {
        'transactional': '有明确购买或使用需求的用户',
        'informational': '希望学习或了解相关知识的用户',
        'navigational': '寻找特定网站或资源的用户'
    }
    return audiences.get(intent_type, '普通用户')

def get_success_metrics(intent_type: str) -> str:
    """Get success metrics based on intent type"""
    metrics = {
        'transactional': '转化率、付费用户数、客单价',
        'informational': '页面浏览量、用户停留时间、订阅数',
        'navigational': '用户访问量、资源点击率、跳出率'
    }
    return metrics.get(intent_type, '页面访问量')

def generate_intent_report(result: Dict, output_file: str):
    """Generate detailed intent report in JSON format"""
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

def generate_site_plan_markdown(result: Dict, output_file: str):
    """Generate site plan in Markdown format"""
    plan = result['site_plan']

    content = f"""# 站点规划：{result['keyword']}

## 基本信息
- **关键词**: {result['keyword']}
- **意图类型**: {result['intent']}
- **站点类型**: {plan['type']}
- **核心功能**: {plan['core_feature']}

## 技术方案
- **推荐技术栈**: {plan['tech_stack']}
- **部署成本**: 0元（免费托管）
- **开发周期**: 1-2周

## 内容策略
- **主标题**: {plan['headline']}
- **长尾词覆盖**: {plan['longtail_coverage']}个
- **SEO策略**: {plan['seo_strategy']}

## 页面结构
"""

    for item in plan['h2_structure']:
        content += f"- {item}\n"

    content += f"""
## 变现模式
- **推荐方式**: {plan['monetization']}
- **目标受众**: {plan['target_audience']}
- **成功指标**: {plan['success_metrics']}

## 长尾关键词布局
"""

    for i, longtail in enumerate(plan['longtail_keywords'], 1):
        content += f"{i}. {longtail}\n"

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)
