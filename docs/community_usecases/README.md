# Community Use Cases page

`data.json` is the shared source for the English and Chinese pages. Entries focus
on research and projects that use or extend XLeRobot. Platform introductions,
generic robotics links, citation-only papers, unverified compatibility claims,
and withdrawn papers are excluded.

Each record has an explicit use category, a concise description in both languages,
and links to primary sources. Simulation and hardware derivatives are identified
as such. Do not treat a project's result as a result for every XLeRobot build.
The collection date and targeted verification date are recorded separately.

From the repository root, run:

```sh
python docs/community_usecases/build.py
python docs/community_usecases/build.py --check
python -m sphinx -b html docs/en/source /tmp/xlerobot-docs-en
python -m sphinx -b html docs/zh/source /tmp/xlerobot-docs-zh
```

Install the relevant documentation requirements before building Sphinx. The page
generator itself uses only the Python standard library and supports Python 3.9+.
Both `relatedworks/index.md` files are generated; edit the shared data instead.
The URL is retained for existing bookmarks, while page titles and navigation use
Community Use Cases / 社区应用案例.

Shared CSS, JavaScript, and attributed project images live in `static/`, included
by both Sphinx configurations. All entries remain readable without JavaScript.
Client-side search supports English and Chinese keywords and intersects with the
paper/project filter. Theme styles are scoped to this page's components.

To add a case, supply both summaries, primary evidence, the actual use category,
and a stable ID. Link companion code and demonstrations from the same record
rather than counting each link as another project. Record image sources in the
`images` object and preserve any embedded attribution.
