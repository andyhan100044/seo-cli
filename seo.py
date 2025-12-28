#!/usr/bin/env python3
"""
SEO CLI - 潜力词发现工具
10秒内完成「找词→意图→规划→大纲」全流程

Usage:
    python seo.py discover --date 2025-01-01
    python seo.py intent --word "AI generator"
    python seo.py outline --plan results/plan.json
    python seo.py batch --file keywords.txt
"""

import argparse
import sys
import json
import csv
from datetime import datetime, timedelta
from pathlib import Path
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
from rich.panel import Panel

# Import our modules
from db import Database
from skills.hot import collect_hot_words
from skills.trend import verify_trends
from skills.intent import analyze_intent
from skills.outline import generate_outline

# Initialize console
console = Console()

def print_banner():
    """Print application banner"""
    banner = """
[bold blue]██████╗ ██████╗ ██╗   ██╗███████╗██████╗  ██████╗[/bold blue]
[bold blue]██╔══██╗██╔══██╗╝██║   ██║██╔════╝██╔══██╗██╔════╝[/bold blue]
[bold blue]██████╔╝██████╔╝ ██║   ██║█████╗  ██████╔╝█████╗  [/bold blue]
[bold blue]██╔══██╗██╔═══╝  ╚██╗ ██╔╝██╔══╝  ██╔══██╗██╔══╝  [/bold blue]
[bold blue]██║  ██║██║       ╚████╔╝ ███████╗██║  ██║███████╗[/bold blue]
[bold blue]╚═╝  ╚═╝╚═╝        ╚═══╝  ╚══════╝╚═╝  ╚═╝╚══════╝[/bold blue]

[bold cyan]SEO CLI - 10秒发现潜力词，本地化关键词分析工具[/bold cyan]
"""
    console.print(banner)

def cmd_discover(args):
    """Discover new hot keywords"""
    console.print("\n[bold green]🔍 Discovering hot keywords...[/bold green]\n")

    # Determine date
    if args.date:
        try:
            target_date = datetime.strptime(args.date, '%Y-%m-%d')
        except ValueError:
            console.print("[red]Error: Invalid date format. Use YYYY-MM-DD[/red]")
            return 1
    else:
        target_date = datetime.now()

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Initialize database
    db = Database()

    # Collect hot words
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task("Collecting hot words...", total=None)

        try:
            hot_words = collect_hot_words(limit=args.limit)
            progress.update(task, description="✅ Hot words collected")

            if not hot_words:
                console.print("[yellow]No hot words found[/yellow]")
                return 0

            # Verify trends
            progress.add_task("Verifying trends...", total=None)
            verified_words = verify_trends(hot_words, timeout=args.timeout)

            # Save to CSV
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            csv_file = output_dir / f"potential_words_{timestamp}.csv"

            with open(csv_file, 'w', newline='', encoding='utf-8') as f:
                if verified_words:
                    writer = csv.DictWriter(f, fieldnames=verified_words[0].keys())
                    writer.writeheader()
                    writer.writerows(verified_words)

            console.print(f"\n[bold green]✅ Results saved to:[/bold green] {csv_file}")
            console.print(f"[bold]Total keywords found:[/bold] {len(verified_words)}")

            # Display summary table
            if verified_words:
                table = Table(title="Top Keywords")
                table.add_column("Keyword", style="cyan")
                table.add_column("Search Volume", style="green")
                table.add_column("Trend Score", style="blue")

                for word in verified_words[:10]:
                    table.add_row(
                        word['word'],
                        str(word.get('search_volume', 'N/A')),
                        f"{word.get('trend_score', 0):.2f}"
                    )

                console.print(table)

            return 0

        except Exception as e:
            console.print(f"\n[red]Error: {e}[/red]")
            console.print_exception()
            return 1

def cmd_intent(args):
    """Analyze keyword intent and generate site plan"""
    console.print(f"\n[bold green]🎯 Analyzing intent for:[/bold green] {args.word}\n")

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task("Analyzing keyword intent...", total=None)

        try:
            # Analyze intent
            result = analyze_intent(args.word, args.longtail)

            progress.update(task, description="✅ Intent analysis complete")

            # Save intent report (JSON)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            json_file = output_dir / f"{args.word.replace(' ', '_')}_intent_{timestamp}.json"

            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)

            # Save site plan (Markdown)
            md_file = output_dir / f"{args.word.replace(' ', '_')}_plan_{timestamp}.md"

            with open(md_file, 'w', encoding='utf-8') as f:
                plan = result['site_plan']
                f.write(f"# 站点规划：{args.word}\n\n")
                f.write(f"- 类型：{plan['type']}\n")
                f.write(f"- 核心功能：{plan['core_feature']}\n")
                f.write(f"- 技术栈：{plan['tech_stack']}\n")
                f.write(f"- 首屏文案：{plan['headline']}\n")
                f.write(f"- H2结构：\n")
                for item in plan['h2_structure']:
                    f.write(f"  - {item}\n")

            console.print(f"\n[bold green]✅ Intent report saved to:[/bold green] {json_file}")
            console.print(f"[bold green]✅ Site plan saved to:[/bold green] {md_file}")

            # Display results
            console.print(f"\n[bold]Intent Type:[/bold] {result['intent']}")
            console.print(f"[bold]Longtail Words Generated:[/bold] {len(result['longtail_words'])}")
            console.print(f"[bold]Site Type:[/bold] {plan['type']}")

            return 0

        except Exception as e:
            console.print(f"\n[red]Error: {e}[/red]")
            console.print_exception()
            return 1

def cmd_outline(args):
    """Generate content outline from site plan"""
    console.print(f"\n[bold green]📝 Generating outline from:[/bold green] {args.plan}\n")

    try:
        # Check if file exists
        plan_file = Path(args.plan)
        if not plan_file.exists():
            console.print(f"[red]Error: Plan file not found: {args.plan}[/red]")
            return 1

        # Generate outline
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            progress.add_task("Generating content outline...", total=None)
            outline = generate_outline(plan_file)

        # Save outline
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = f"outline_{timestamp}.md"

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"# {outline['outline']['H1']}\n\n")

            for section in outline['outline']['sections']:
                f.write(f"## {section['H2']}\n\n")
                if 'key_points' in section:
                    for point in section['key_points']:
                        f.write(f"- {point}\n")
                    f.write("\n")

        console.print(f"\n[bold green]✅ Outline saved to:[/bold green] {output_file}")
        console.print(f"[bold]Estimated Word Count:[/bold] {outline['word_count']}")

        return 0

    except Exception as e:
        console.print(f"\n[red]Error: {e}[/red]")
        console.print_exception()
        return 1

def cmd_batch(args):
    """Batch process keywords from file"""
    console.print(f"\n[bold green]📦 Batch processing keywords from:[/bold green] {args.file}\n")

    try:
        # Read keywords from file
        keywords = []
        with open(args.file, 'r', encoding='utf-8') as f:
            for line in f:
                keyword = line.strip()
                if keyword:
                    keywords.append(keyword)

        if not keywords:
            console.print("[yellow]No keywords found in file[/yellow]")
            return 0

        console.print(f"[bold]Processing {len(keywords)} keywords...[/bold]\n")

        results = []

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Processing keywords...", total=len(keywords))

            for keyword in keywords:
                try:
                    result = analyze_intent(keyword)
                    results.append(result)
                    progress.advance(task)
                except Exception as e:
                    console.print(f"[red]Error processing '{keyword}': {e}[/red]")
                    progress.advance(task)

        # Save to CSV
        output_file = Path(args.output)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            fieldnames = ['keyword', 'intent', 'longtail_count', 'site_type', 'headline']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

            for result in results:
                writer.writerow({
                    'keyword': result['keyword'],
                    'intent': result['intent'],
                    'longtail_count': len(result['longtail_words']),
                    'site_type': result['site_plan']['type'],
                    'headline': result['site_plan']['headline']
                })

        console.print(f"\n[bold green]✅ Batch processing complete![/bold green]")
        console.print(f"[bold]Results saved to:[/bold] {output_file}")
        console.print(f"[bold]Successfully processed:[/bold] {len(results)}/{len(keywords)}")

        return 0

    except Exception as e:
        console.print(f"\n[red]Error: {e}[/red]")
        console.print_exception()
        return 1

def main():
    """Main entry point"""
    print_banner()

    parser = argparse.ArgumentParser(
        description='SEO CLI - 10秒发现潜力词，本地化关键词分析工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s discover --date 2025-01-01 --limit 50
  %(prog)s intent --word "AI generator" --longtail 20
  %(prog)s outline --plan results/plan.json
  %(prog)s batch --file keywords.txt --output results.csv
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Discover command
    discover_parser = subparsers.add_parser('discover', help='发现新热词')
    discover_parser.add_argument('--date', help='指定日期，格式：YYYY-MM-DD')
    discover_parser.add_argument('--limit', type=int, default=100, help='关键词数量限制')
    discover_parser.add_argument('--output', default='./results', help='输出目录')
    discover_parser.add_argument('--timeout', type=int, default=10, help='超时时间（秒）')

    # Intent command
    intent_parser = subparsers.add_parser('intent', help='分析关键词意图')
    intent_parser.add_argument('--word', required=True, help='要分析的关键词')
    intent_parser.add_argument('--longtail', type=int, default=20, help='长尾词数量')
    intent_parser.add_argument('--output-dir', default='./results', help='输出目录')

    # Outline command
    outline_parser = subparsers.add_parser('outline', help='生成内容大纲')
    outline_parser.add_argument('--plan', required=True, help='规划文件路径')

    # Batch command
    batch_parser = subparsers.add_parser('batch', help='批量处理')
    batch_parser.add_argument('--file', required=True, help='关键词文件路径')
    batch_parser.add_argument('--output', default='./results/batch_results.csv', help='输出CSV路径')

    # Parse arguments
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    # Route to appropriate command handler
    if args.command == 'discover':
        return cmd_discover(args)
    elif args.command == 'intent':
        return cmd_intent(args)
    elif args.command == 'outline':
        return cmd_outline(args)
    elif args.command == 'batch':
        return cmd_batch(args)
    else:
        console.print(f"[red]Unknown command: {args.command}[/red]")
        return 1

if __name__ == '__main__':
    sys.exit(main())
