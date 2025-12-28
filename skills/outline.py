"""
SEO CLI - Skill④: Content Outline Generation
Generate detailed content outlines based on site plans
"""

import json
from typing import Dict, List

def generate_outline(plan_file: str) -> Dict:
    """
    Generate content outline from site plan

    Args:
        plan_file: Path to site plan JSON file

    Returns:
        Dictionary with outline information
    """
    # Read plan file
    try:
        with open(plan_file, 'r', encoding='utf-8') as f:
            plan = json.load(f)
    except Exception as e:
        raise ValueError(f"Failed to read plan file: {e}")

    keyword = plan['keyword']
    intent = plan['intent']
    site_type = plan['type']

    # Generate outline based on site type
    if '工具' in site_type:
        outline = generate_tool_outline(keyword)
    elif '博客' in site_type or '知识库' in site_type:
        outline = generate_blog_outline(keyword)
    elif '导航' in site_type:
        outline = generate_directory_outline(keyword)
    else:
        outline = generate_generic_outline(keyword)

    return {
        'keyword': keyword,
        'intent': intent,
        'site_type': site_type,
        'outline': outline,
        'word_count': estimate_word_count(outline),
        'target_keywords': extract_target_keywords(outline, keyword),
        'estimated_reading_time': estimate_reading_time(outline)
    }

def generate_tool_outline(keyword: str) -> Dict:
    """Generate outline for tool-based website"""
    return {
        'H1': f'{keyword}在线工具',
        'type': 'tool',
        'sections': [
            {
                'H2': f'什么是{keyword}？',
                'content_type': 'introduction',
                'word_count': 300,
                'reading_time': 2,
                'key_points': [
                    f'{keyword}的定义和用途',
                    f'为什么需要{keyword}',
                    f'{keyword}的应用场景',
                    f'{keyword}的优势和特点'
                ],
                'target_keywords': [f'{keyword}是什么', f'{keyword}介绍', f'{keyword}定义']
            },
            {
                'H2': f'如何使用我们的{keyword}工具',
                'content_type': 'tutorial',
                'word_count': 500,
                'reading_time': 3,
                'key_points': [
                    '步骤1：上传文件或输入数据',
                    '步骤2：选择参数和选项',
                    '步骤3：点击生成或处理按钮',
                    '步骤4：下载结果或查看输出',
                    '步骤5：保存或分享结果'
                ],
                'target_keywords': [f'{keyword}使用方法', f'如何使用{keyword}', f'{keyword}教程']
            },
            {
                'H2': f'{keyword}工具的核心功能',
                'content_type': 'features',
                'word_count': 400,
                'reading_time': 2,
                'key_points': [
                    '免费使用，无需注册',
                    '5秒快速生成',
                    '支持多种格式输入输出',
                    '结果准确可靠',
                    '安全的数据处理',
                    '移动端友好'
                ],
                'target_keywords': [f'{keyword}功能', f'{keyword}特点', f'{keyword}优势']
            },
            {
                'H2': f'{keyword}应用场景',
                'content_type': 'use_cases',
                'word_count': 350,
                'reading_time': 2,
                'key_points': [
                    '个人用户：日常工作和学习',
                    '企业用户：业务流程优化',
                    '学生用户：作业和学习辅助',
                    '自由职业者：提升工作效率',
                    '电商卖家：商品描述优化'
                ],
                'target_keywords': [f'{keyword}应用', f'{keyword}场景', f'{keyword}用途']
            },
            {
                'H2': '常见问题解答',
                'content_type': 'faq',
                'word_count': 300,
                'reading_time': 2,
                'key_points': [
                    '工具完全免费吗？有什么限制？',
                    '支持哪些文件格式？',
                    '生成需要多长时间？',
                    '数据安全如何保障？',
                    '可以商用吗？',
                    '如何提高处理效果？'
                ],
                'target_keywords': [f'{keyword}FAQ', f'{keyword}问题', f'{keyword}帮助']
            }
        ]
    }

def generate_blog_outline(keyword: str) -> Dict:
    """Generate outline for blog/knowledge base"""
    return {
        'H1': f'{keyword}完整指南：从入门到精通',
        'type': 'blog',
        'sections': [
            {
                'H2': f'{keyword}基础入门',
                'content_type': 'basics',
                'word_count': 800,
                'reading_time': 4,
                'key_points': [
                    f'{keyword}的定义和概念',
                    f'{keyword}的历史和发展',
                    f'{keyword}的重要性',
                    '核心概念详解',
                    '基本原理和工作机制'
                ],
                'target_keywords': [f'{keyword}入门', f'{keyword}基础', f'{keyword}概念']
            },
            {
                'H2': f'{keyword}进阶教程',
                'content_type': 'tutorial',
                'word_count': 1200,
                'reading_time': 6,
                'key_points': [
                    '环境搭建和配置',
                    '基础操作和实践',
                    '进阶技巧和方法',
                    '实战项目和案例',
                    '性能优化建议'
                ],
                'target_keywords': [f'{keyword}教程', f'{keyword}进阶', f'{keyword}学习']
            },
            {
                'H2': f'{keyword}最佳实践',
                'content_type': 'best_practices',
                'word_count': 1000,
                'reading_time': 5,
                'key_points': [
                    '行业标准和规范',
                    '常见问题和解决方案',
                    '避坑指南和注意事项',
                    '效率提升技巧',
                    '工具和资源推荐'
                ],
                'target_keywords': [f'{keyword}最佳实践', f'{keyword}技巧', f'{keyword}方法']
            },
            {
                'H2': f'{keyword}实战案例分析',
                'content_type': 'cases',
                'word_count': 600,
                'reading_time': 3,
                'key_points': [
                    '成功案例1：某企业的{keyword}实施',
                    '成功案例2：个人用户的高效应用',
                    '失败案例分析：常见错误和教训',
                    '案例总结和经验分享'
                ],
                'target_keywords': [f'{keyword}案例', f'{keyword}实战', f'{keyword}分析']
            },
            {
                'H2': '常见问题解答',
                'content_type': 'faq',
                'word_count': 400,
                'reading_time': 2,
                'key_points': [
                    f'{keyword}适合初学者吗？',
                    '学习{keyword}需要多长时间？',
                    '需要掌握哪些前置知识？',
                    f'{keyword}的就业前景如何？',
                    '如何持续学习和提升？'
                ],
                'target_keywords': [f'{keyword}FAQ', f'{keyword}问题', f'{keyword}解答']
            }
        ]
    }

def generate_directory_outline(keyword: str) -> Dict:
    """Generate outline for directory/resource site"""
    return {
        'H1': f'{keyword}资源导航',
        'type': 'directory',
        'sections': [
            {
                'H2': f'{keyword}官方资源',
                'content_type': 'official',
                'word_count': 500,
                'reading_time': 3,
                'key_points': [
                    '官方网站和文档',
                    '官方教程和指南',
                    '官方工具和软件',
                    '官方社区和论坛',
                    '更新日志和公告'
                ],
                'target_keywords': [f'{keyword}官方', f'{keyword}官网', f'{keyword}文档']
            },
            {
                'H2': '优质第三方工具',
                'content_type': 'tools',
                'word_count': 600,
                'reading_time': 3,
                'key_points': [
                    '在线工具推荐',
                    '桌面软件推荐',
                    '浏览器插件推荐',
                    '移动应用推荐',
                    '工具对比和评测'
                ],
                'target_keywords': [f'{keyword}工具', f'{keyword}软件', f'{keyword}推荐']
            },
            {
                'H2': '学习资源汇总',
                'content_type': 'resources',
                'word_count': 700,
                'reading_time': 4,
                'key_points': [
                    '在线课程推荐',
                    '书籍和电子书推荐',
                    '视频教程推荐',
                    '博客和公众号推荐',
                    '社区和论坛推荐'
                ],
                'target_keywords': [f'{keyword}学习', f'{keyword}资源', f'{keyword}教程']
            },
            {
                'H2': '最新动态和资讯',
                'content_type': 'news',
                'word_count': 400,
                'reading_time': 2,
                'key_points': [
                    '行业新闻和趋势',
                    '新工具发布',
                    '技术更新和升级',
                    '会议和活动信息',
                    '专家观点和评论'
                ],
                'target_keywords': [f'{keyword}新闻', f'{keyword}动态', f'{keyword}资讯']
            }
        ]
    }

def generate_generic_outline(keyword: str) -> Dict:
    """Generate generic outline for other types"""
    return {
        'H1': keyword,
        'type': 'generic',
        'sections': [
            {
                'H2': f'关于{keyword}',
                'content_type': 'overview',
                'word_count': 500,
                'reading_time': 3,
                'key_points': [
                    f'{keyword}的定义',
                    f'{keyword}的背景',
                    f'{keyword}的重要性',
                    '相关概念介绍'
                ],
                'target_keywords': [f'{keyword}介绍', f'{keyword}概述', f'{keyword}背景']
            },
            {
                'H2': f'{keyword}详细介绍',
                'content_type': 'details',
                'word_count': 800,
                'reading_time': 4,
                'key_points': [
                    '核心内容详解',
                    '技术细节分析',
                    '实施方法和步骤',
                    '最佳实践建议'
                ],
                'target_keywords': [f'{keyword}详解', f'{keyword}分析', f'{keyword}方法']
            },
            {
                'H2': f'{keyword}应用指南',
                'content_type': 'guide',
                'word_count': 700,
                'reading_time': 4,
                'key_points': [
                    '应用场景介绍',
                    '使用方法说明',
                    '注意事项提醒',
                    '常见问题解答'
                ],
                'target_keywords': [f'{keyword}应用', f'{keyword}使用', f'{keyword}指南']
            }
        ]
    }

def estimate_word_count(outline: Dict) -> int:
    """Estimate total word count for outline"""
    total = 0
    for section in outline['sections']:
        total += section.get('word_count', 500)
    return total

def estimate_reading_time(outline: Dict) -> int:
    """Estimate total reading time in minutes"""
    total = 0
    for section in outline['sections']:
        total += section.get('reading_time', 3)
    return total

def extract_target_keywords(outline: Dict, main_keyword: str) -> List[str]:
    """Extract all target keywords from outline"""
    keywords = {main_keyword.lower()}

    for section in outline['sections']:
        if 'target_keywords' in section:
            for keyword in section['target_keywords']:
                keywords.add(keyword.lower())

    return list(keywords)

def save_outline_to_markdown(outline_data: Dict, output_file: str):
    """Save outline to Markdown file"""
    outline = outline_data['outline']

    content = f"# {outline['H1']}\n\n"
    content += f"**类型**: {outline['type']}\n\n"
    content += f"**预估字数**: {outline_data['word_count']}\n\n"
    content += f"**预估阅读时间**: {outline_data['estimated_reading_time']}分钟\n\n"

    for section in outline['sections']:
        content += f"## {section['H2']}\n\n"

        if 'key_points' in section:
            content += "**要点**:\n\n"
            for point in section['key_points']:
                content += f"- {point}\n"
            content += "\n"

        if 'target_keywords' in section:
            content += f"**目标关键词**: {', '.join(section['target_keywords'])}\n\n"

    content += "## 目标关键词总览\n\n"
    content += f"总计: {len(outline_data['target_keywords'])}个\n\n"

    for keyword in outline_data['target_keywords']:
        content += f"- {keyword}\n"

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)
