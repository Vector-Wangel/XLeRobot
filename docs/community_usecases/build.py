#!/usr/bin/env python3
"""Build the English and Chinese community pages from the same curated records."""
import argparse
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TEXT = {
    'en': {
        'title': 'Community Use Cases',
        'intro': 'Research and community projects that use, adapt, or extend XLeRobot. Explore how teams work with the platform, from manipulation and teleoperation to simulation and household applications.',
        'scope': 'Each entry describes the specific use reported by its authors. Simulation examples and hardware derivatives are identified separately.',
        'papers': 'Research papers', 'projects': 'Community projects', 'all': 'All entries',
        'search': 'Search papers and projects', 'placeholder': 'Try teleoperation, VLA, or a project name',
        'filter': 'Filter by entry type', 'count': '{shown} of {total} entries',
        'empty': 'No matching entries. Try another term or choose All entries.',
        'snapshot': 'Based on the September 18, 2026 collection, with selected source checks on September 24, 2026.',
        'share': 'Share your project',
        'contribute': 'Using XLeRobot in your research or project? Suggest an addition with a paper, repository, or demonstration link and a short description of how you use it.',
        'suggest': 'Suggest a community use case', 'source': 'Source',
    },
    'zh': {
        'title': '社区应用案例',
        'intro': '这里收录使用、改造或扩展 XLeRobot 的研究论文和社区项目，涵盖机器人操作、遥操作、仿真与家庭应用。',
        'scope': '每个条目说明作者如何使用 XLeRobot；仿真案例和硬件改型会单独标明。',
        'papers': '研究论文', 'projects': '社区项目', 'all': '全部条目',
        'search': '搜索论文和项目', 'placeholder': '试试遥操作、VLA 或项目名称',
        'filter': '按条目类型筛选', 'count': '显示 {shown} / {total} 个条目',
        'empty': '没有匹配的条目，请尝试其他关键词或选择“全部条目”。',
        'snapshot': '基于 2026 年 9 月 18 日的资料整理，并于 2026 年 9 月 24 日定向复核部分来源。',
        'share': '分享你的项目',
        'contribute': '如果你正在用 XLeRobot 做研究或开发项目，欢迎提供论文、代码仓库或演示链接，并简要说明具体用途。',
        'suggest': '推荐一个社区应用案例', 'source': '来源',
    },
}
CATEGORIES = {
    'hardware': ('Hardware adaptations', '硬件改造'),
    'teleoperation': ('Teleoperation and data collection', '遥操作与数据采集'),
    'learning': ('Robot learning', '机器人学习'),
    'applications': ('Applications and student projects', '应用与学生项目'),
    'simulation': ('Simulation environments and integrations', '仿真环境与集成'),
}
KINDS = {
    'software_integration': ('Software integration', '软件集成'),
    'software_extension': ('Software extension', '软件扩展'),
    'measurement_tooling': ('Measurement tools', '测量工具'),
    'data_collection_tooling': ('Data collection tools', '数据采集工具'),
    'application_project': ('Application project', '应用项目'),
    'student_project': ('Student project', '学生项目'),
    'student_application_project': ('Student application', '学生应用项目'),
    'simulation_project': ('Simulation project', '仿真项目'),
    'hardware_derivative': ('Hardware derivative', '硬件改型'),
    'real_robot_experiments': ('Physical robot experiments', '实机实验'),
    'teleoperation_user_study': ('Teleoperation study', '遥操作研究'),
    'simulation_embodiment': ('Simulation', '仿真'),
    'hardware': ('Hardware adaptation', '硬件改造'),
    'teleoperation': ('Teleoperation', '遥操作'),
    'learning': ('Robot learning', '机器人学习'),
    'applications': ('Application', '应用项目'),
    'simulation': ('Simulation', '仿真'),
}


def esc(value):
    return html.escape(str(value), quote=True)


def label(pair, lang):
    return pair[0 if lang == 'en' else 1]


def card(item, entry_type, lang, images):
    t = TEXT[lang]
    summary = item['summary_' + lang]
    # Include both translations in search so names and technical terms work in either language.
    search = ' '.join(str(item.get(k, '')) for k in
                      ('title', 'authors', 'summary_en', 'summary_zh', 'category', 'kind'))
    kind = item.get('kind', item.get('category', 'applications'))
    if kind not in KINDS:
        raise ValueError('Unknown use-case kind: ' + kind)
    meta = [label(KINDS[kind], lang)]
    if entry_type == 'paper':
        meta.extend(str(item[key]) for key in ('year', 'venue') if item.get(key))
        status = item.get('status_' + lang)
        if not status:
            status = label({'preprint': ('Preprint', '预印本'),
                            'historical_preprint': ('Historical preprint', '历史预印本'),
                            'published': ('Published', '已发表')}.get(item.get('status'), ('', '')), lang)
        if status:
            meta.append(status)
    links = item.get('links', [])
    if not links and item.get('url'):
        links = [{'url': item['url'], 'label_en': 'Project', 'label_zh': '项目'}]
    if not links:
        raise ValueError('No source link for ' + item['id'])
    title_url = item.get('url', links[0]['url'])
    out = [f'<article class="community-card" id="case-{esc(item["id"])}" '
           f'data-community-type="{entry_type}" data-community-search="{esc(search)}">',
           '<div class="community-meta">' + ' · '.join(esc(m) for m in meta) + '</div>',
           f'<h3 class="community-title"><a href="{esc(title_url)}">{esc(item["title"])}</a></h3>']
    if item.get('authors'):
        authors = item['authors']
        if isinstance(authors, list):
            authors = ', '.join(authors[:3]) + (' et al.' if lang == 'en' else ' 等') if len(authors) > 4 else ', '.join(authors)
        out.append(f'<p class="community-authors">{esc(authors)}</p>')
    image = images.get(item.get('image_key'))
    if image:
        alt = image.get('alt_' + lang, item['title'])
        out.append(f'<img class="community-image" src="../_static/community/{esc(image["filename"])}" '
                   f'alt="{esc(alt)}" loading="lazy" decoding="async">')
    out.append(f'<p class="community-description">{esc(summary)}</p>')
    out.append('<p class="community-links">' + ' '.join(
        f'<a href="{esc(link["url"])}">{esc(link["label_" + lang])}</a>' for link in links) + '</p>')
    if image:
        credit = image.get('credit_' + lang, t['source'])
        out.append(f'<p class="community-credit"><a href="{esc(image["source_url"])}">{esc(credit)}</a></p>')
    out.append('</article>')
    return '\n'.join(out)


def render(data, lang):
    t = TEXT[lang]
    papers, projects = data['papers'], data['projects']
    count = len(papers) + len(projects)
    switch = ('<span aria-current="page">English</span> · '
              '<a href="https://xlerobot.readthedocs.io/zh-cn/latest/relatedworks/index.html" lang="zh-CN">中文</a>') if lang == 'en' else (
              '<a href="https://xlerobot.readthedocs.io/en/latest/relatedworks/index.html" lang="en">English</a> · '
              '<span aria-current="page">中文</span>')
    out = ['<!-- Generated by docs/community_usecases/build.py; edit data.json instead. -->',
           '# ' + t['title'], '', t['intro'], '', t['scope'], '',
           '<nav class="community-language" aria-label="Language">' + switch + '</nav>', '',
           f'<p class="community-jump"><a href="#research-papers">{t["papers"]} ({len(papers)})</a>'
           f' <a href="#community-projects">{t["projects"]} ({len(projects)})</a></p>', '',
           '<div class="community-controls">',
           f'<label for="community-search">{t["search"]}</label>',
           f'<input type="search" id="community-search" placeholder="{esc(t["placeholder"])}" autocomplete="off">',
           f'<fieldset class="community-filters"><legend>{t["filter"]}</legend>']
    for kind, key in [('all', 'all'), ('paper', 'papers'), ('project', 'projects')]:
        out.append(f'<button type="button" data-community-filter="{kind}" '
                   f'aria-pressed="{"true" if kind == "all" else "false"}">{t[key]}</button>')
    out.extend(['</fieldset>',
        f'<p id="community-results" role="status" aria-live="polite" data-count-template="{esc(t["count"])}">'
        + t['count'].format(shown=count, total=count) + '</p>',
        f'<p id="community-empty" hidden>{t["empty"]}</p>', '</div>', '',
        '<!-- Explicit labels preserve the same anchors in both languages. -->',
        '(research-papers)=', '## ' + t['papers'], '',
        '<div class="community-group"><div class="community-grid community-papers">'])
    out.extend(card(p, 'paper', lang, data['images']) for p in papers)
    out.extend(['</div></div>', '', '(community-projects)=', '## ' + t['projects'], ''])
    for category, titles in CATEGORIES.items():
        selected = [p for p in projects if p['category'] == category]
        if not selected:
            continue
        # Markdown headings remain visible to Sphinx's document structure and navigation.
        out.extend(['### ' + label(titles, lang), '',
                    '<div class="community-group"><div class="community-grid">'])
        out.extend(card(p, 'project', lang, data['images']) for p in selected)
        out.extend(['</div></div>', ''])
    out.extend(['## ' + t['share'], '', t['contribute'], '',
                f'[{t["suggest"]}](https://github.com/Vector-Wangel/XLeRobot/issues/new)', '',
                '<p class="community-credit">' + t['snapshot'] + '</p>', ''])
    return '\n\n'.join(out)


def validate(data):
    ids = [p['id'] for p in data['papers'] + data['projects']]
    if len(ids) != len(set(ids)):
        raise ValueError('Entry IDs must be unique across papers and projects')
    for item in data['papers'] + data['projects']:
        for key in ('summary_en', 'summary_zh', 'evidence_url'):
            if not item.get(key):
                raise ValueError(f'{item["id"]}: missing {key}')
        for link in item.get('links', []):
            if not link['url'].startswith('https://'):
                raise ValueError('Source links must use HTTPS: ' + link['url'])
    for image in data['images'].values():
        if not (ROOT/'static/community'/image['filename']).is_file():
            raise ValueError('Missing image: ' + image['filename'])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Fail if generated pages are stale')
    args = parser.parse_args()
    data = json.loads((ROOT/'data.json').read_text(encoding='utf-8'))
    validate(data)
    for lang in TEXT:
        target = ROOT.parent/lang/'source/relatedworks/index.md'
        generated = render(data, lang)
        if args.check:
            if not target.exists() or target.read_text(encoding='utf-8') != generated:
                raise SystemExit('Generated page is stale: ' + str(target))
        else:
            target.write_text(generated, encoding='utf-8')
        print(('Checked ' if args.check else 'Wrote ') + str(target))


if __name__ == '__main__':
    main()
