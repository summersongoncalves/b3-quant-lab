// The markdown files link to each other with repo-relative paths (they are
// written to be read in the editor). This maps them to the app's own pages.

// Agents often write links from the repo root (like the editor does), not relative to the file.
const ROOT_PREFIXES = ['src/', 'research/', 'reports/', 'docs/', 'knowledge/', 'tests/', '.claude/', 'CLAUDE.md', 'README.md']

/** Repo-relative path a link points to, resolved against the document that holds it. */
export function repoPath(href: string, docPath: string): string | null {
  if (/^[a-z][a-z0-9+.-]*:/i.test(href) || href.startsWith('#') || href.startsWith('//')) return null
  href = href.replaceAll('\\', '/')
  const base = ROOT_PREFIXES.some((p) => href.startsWith(p)) ? 'http://repo/' : `http://repo/${docPath}`
  const url = new URL(href, base)
  return decodeURIComponent(url.pathname).replace(/^\/+/, '') + url.hash
}

/** App route for a repo path: hypotheses, cycles and reports have their own pages, the rest opens in the file viewer. */
export function routeFor(path: string): string {
  const [file, hash = ''] = path.split('#')
  const anchor = hash ? `#${hash}` : ''
  let m = file.match(/^research\/hypotheses\/([^/]+)\.md$/)
  if (m) return `/hypotheses/${m[1]}${anchor}`
  m = file.match(/^reports\/ciclos\/([^/]+)\.md$/)
  if (m) return `/cycles/${m[1]}${anchor}`
  m = file.match(/^reports\/([^/]+)(\/(report\.(md|json))?)?\/?$/)
  if (m && m[1] !== 'ciclos') return `/reports/${m[1]}`
  return `/files/${file}${anchor}`
}
