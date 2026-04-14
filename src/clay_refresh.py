"""Lightweight Clay refresh pipeline helpers."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from difflib import SequenceMatcher
from html.parser import HTMLParser
import json
from pathlib import Path
import re
from typing import Iterable
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parent.parent
REFERENCES_DIR = ROOT / "references"
SNAPSHOT_DIR = ROOT / "data" / "snapshots"
RUNS_DIR = ROOT / "data" / "runs"
LOG_FILE = ROOT / "logs" / "refresh_log.md"
SOURCES_FILE = REFERENCES_DIR / "clay-sources.md"
LATEST_ANALYSIS_FILE = RUNS_DIR / "latest_analysis.json"
SUMMARY_PROMPT_FILE = ROOT / "prompts" / "summarize_clay_update.md"

USER_AGENT = "Clay-Agent/1.0 (+https://www.clay.com)"
TIMESTAMP_FORMAT = "%Y%m%dT%H%M%SZ"
ALLOWED_SOURCE_HOSTS = {"clay.com", "www.clay.com", "university.clay.com"}
NOISE_PATTERNS = (
    "the go-to-market conference by clay",
    "skip to main",
    "get a demo",
    "sign up",
    "log in",
    "pricing",
    "careers",
    "about",
    "image",
    "copied!",
    "downloaded!",
    "download brand assets",
    "copy logo to clipboard",
    "copy icon to clipboard",
    "clay logo",
    "resources",
    "solutions",
    "use cases",
    "social media",
    "additional help",
    "learn with cohorts",
    "find clay experts",
    "university home page",
    "review your year with clay on clayback.clay.com",
    "open workspace",
    "clay.com",
    "docs",
    "courses",
    "overview",
    "certifications",
    "cohorts",
    "customers",
)


@dataclass
class Source:
    name: str
    kind: str
    url: str
    slug: str
    routes: list[str]


@dataclass
class SourceSnapshot:
    source: Source
    fetched_at: str
    previous_snapshot: str | None
    current_snapshot: str
    previous_text: str
    current_text: str
    previous_hash: str | None
    current_hash: str
    status: str
    error: str | None = None


class TextExtractor(HTMLParser):
    """Extract visible text from HTML."""

    def __init__(self) -> None:
        super().__init__()
        self._chunks: list[str] = []
        self._skip_depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in {"script", "style", "noscript", "svg"}:
            self._skip_depth += 1
            return
        if tag in {"p", "br", "li", "section", "article", "div", "main", "h1", "h2", "h3", "h4", "h5", "h6"}:
            self._chunks.append("\n")

    def handle_endtag(self, tag: str) -> None:
        if tag in {"script", "style", "noscript", "svg"} and self._skip_depth:
            self._skip_depth -= 1
            return
        if tag in {"p", "li", "section", "article", "div", "main", "h1", "h2", "h3", "h4", "h5", "h6"}:
            self._chunks.append("\n")

    def handle_data(self, data: str) -> None:
        if self._skip_depth:
            return
        text = data.strip()
        if text:
            self._chunks.append(text + " ")

    def text(self) -> str:
        return "".join(self._chunks)


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


def format_run_timestamp(value: datetime) -> str:
    return value.strftime(TIMESTAMP_FORMAT)


def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def load_sources(path: Path = SOURCES_FILE) -> list[Source]:
    sources: list[Source] = []
    if not path.exists():
        raise FileNotFoundError(f"Missing source file: {path}")
    in_manifest = False
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if line.startswith("## "):
            in_manifest = line == "## Monitored Sources"
            continue
        if not in_manifest or not line.startswith("- "):
            continue
        parts = [part.strip() for part in line[2:].split("|")]
        if len(parts) != 4:
            continue
        name, kind, url, routes_blob = parts
        validate_source_url(url)
        routes = [normalize_route_name(route) for route in routes_blob.split(",") if route.strip()]
        if not routes:
            raise ValueError(f"No reference routes configured for source '{name}'")
        sources.append(Source(name=name, kind=kind, url=url, slug=slugify(name), routes=routes))
    if not sources:
        raise ValueError(f"No sources configured in {path}")
    return sources


def validate_source_url(url: str) -> None:
    parsed = urlparse(url)
    if parsed.scheme != "https":
        raise ValueError(f"Source must use https: {url}")
    if parsed.netloc not in ALLOWED_SOURCE_HOSTS:
        raise ValueError(f"Source host is not an official Clay domain: {url}")


def normalize_route_name(route: str) -> str:
    filename = route.strip().replace(".md", "")
    filename = filename.removeprefix("references/")
    return f"{filename}.md"


def source_snapshot_dir(source: Source) -> Path:
    return SNAPSHOT_DIR / source.slug


def snapshot_text_path(source: Source, stamp: str) -> Path:
    return source_snapshot_dir(source) / f"{stamp}.txt"


def snapshot_html_path(source: Source, stamp: str) -> Path:
    return source_snapshot_dir(source) / f"{stamp}.html"


def latest_text_path(source: Source) -> Path:
    return source_snapshot_dir(source) / "latest.txt"


def latest_html_path(source: Source) -> Path:
    return source_snapshot_dir(source) / "latest.html"


def latest_meta_path(source: Source) -> Path:
    return source_snapshot_dir(source) / "latest.meta.json"


def previous_latest_meta(source: Source) -> dict[str, object] | None:
    path = latest_meta_path(source)
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def fetch_url(url: str) -> str:
    request = Request(url, headers={"User-Agent": USER_AGENT})
    with urlopen(request, timeout=30) as response:
        charset = response.headers.get_content_charset() or "utf-8"
        return response.read().decode(charset, errors="replace")


def slice_relevant_lines(source: Source, lines: list[str]) -> list[str]:
    start_markers: list[str] = []
    stop_markers: list[str] = []

    if source.kind in {"sources", "enrichments", "bulk-enrichment", "webhooks"}:
        start_markers = ["Overview", "What it does", "How it works", "In Clay", "Setup", "How to use"]
        stop_markers = ["Other popular resources", "Explore, practice and master Clay"]
    elif source.kind == "http-api":
        start_markers = ["HTTP API", "Overview", "In this lesson", "How it works"]
        stop_markers = ["Other popular resources", "Explore, practice and master Clay"]

    start_index = 0
    for index, line in enumerate(lines):
        if line in start_markers or any(marker in line for marker in start_markers):
            start_index = index
            break

    end_index = len(lines)
    for index, line in enumerate(lines[start_index:], start=start_index):
        if any(marker in line for marker in stop_markers):
            end_index = index
            break

    return lines[start_index:end_index]


def html_to_text(source: Source, html: str) -> str:
    parser = TextExtractor()
    parser.feed(html)
    text = parser.text()
    text = text.replace("\xa0", " ")
    lines = []
    for raw_line in text.splitlines():
        line = normalize_line(raw_line)
        if keep_line(line):
            lines.append(line)
    lines = slice_relevant_lines(source, lines)
    return "\n".join(lines).strip() + "\n"


def normalize_line(value: str) -> str:
    value = re.sub(r"\s+", " ", value).strip()
    value = value.replace("•", "-")
    return value


def keep_line(line: str) -> bool:
    if not line:
        return False
    if len(line) < 4:
        return False
    lowered = line.lower()
    if lowered in NOISE_PATTERNS:
        return False
    if any(lowered.startswith(pattern) for pattern in NOISE_PATTERNS):
        return False
    if re.fullmatch(r"[0-9]{1,2}:[0-9]{2}", line):
        return False
    return True


def route_keywords() -> dict[str, tuple[str, ...]]:
    return {
        "clay-capabilities.md": (
            "can",
            "supports",
            "integration",
            "source",
            "enrichment",
            "action",
            "webhook",
            "api",
            "bulk",
        ),
        "clay-workflows.md": (
            "step",
            "steps",
            "setup",
            "create",
            "add",
            "configure",
            "run",
            "table",
            "workflow",
            "import",
            "export",
            "webhook",
            "http api",
        ),
        "clay-limitations.md": (
            "limit",
            "limits",
            "only",
            "requires",
            "must",
            "cannot",
            "can't",
            "warning",
            "constraint",
            "enterprise",
            "not available",
        ),
    }


def detect_ambiguity(lines: Iterable[str]) -> bool:
    blob = " ".join(lines).lower()
    ambiguity_terms = (
        "may",
        "might",
        "depending",
        "varies",
        "if needed",
        "for some",
        "beta",
        "preview",
        "contact support",
        "learn more",
    )
    return any(term in blob for term in ambiguity_terms)


def stable_lines(text: str) -> list[str]:
    return [line for line in (normalize_line(part) for part in text.splitlines()) if keep_line(line)]


def calculate_hash(text: str) -> str:
    import hashlib

    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def fetch_sources(run_at: datetime | None = None) -> list[SourceSnapshot]:
    run_at = run_at or now_utc()
    stamp = format_run_timestamp(run_at)
    snapshots: list[SourceSnapshot] = []
    for source in load_sources():
        print(f"[fetch] {source.name}")
        source_dir = source_snapshot_dir(source)
        source_dir.mkdir(parents=True, exist_ok=True)
        previous_meta = previous_latest_meta(source)
        previous_text = ""
        previous_hash = None
        previous_snapshot = None
        if previous_meta:
            previous_snapshot = str(previous_meta.get("snapshot", "")) or None
            previous_hash = str(previous_meta.get("sha256", "")) or None
            latest_text = latest_text_path(source)
            if latest_text.exists():
                previous_text = latest_text.read_text(encoding="utf-8")
        try:
            html = fetch_url(source.url)
            text = html_to_text(source, html)
            current_hash = calculate_hash(text)
            snapshot_html = snapshot_html_path(source, stamp)
            snapshot_text = snapshot_text_path(source, stamp)
            snapshot_html.write_text(html, encoding="utf-8")
            snapshot_text.write_text(text, encoding="utf-8")
            latest_html_path(source).write_text(html, encoding="utf-8")
            latest_text_path(source).write_text(text, encoding="utf-8")
            latest_meta_path(source).write_text(
                json.dumps(
                    {
                        "name": source.name,
                        "kind": source.kind,
                        "url": source.url,
                        "fetched_at": run_at.isoformat(),
                        "snapshot": snapshot_text.name,
                        "sha256": current_hash,
                    },
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )
            snapshots.append(
                SourceSnapshot(
                    source=source,
                    fetched_at=run_at.isoformat(),
                    previous_snapshot=previous_snapshot,
                    current_snapshot=snapshot_text.name,
                    previous_text=previous_text,
                    current_text=text,
                    previous_hash=previous_hash,
                    current_hash=current_hash,
                    status="ok",
                )
            )
            print(f"[fetch] saved {snapshot_text}")
        except (HTTPError, URLError, TimeoutError, ValueError) as exc:
            error = f"{type(exc).__name__}: {exc}"
            snapshots.append(
                SourceSnapshot(
                    source=source,
                    fetched_at=run_at.isoformat(),
                    previous_snapshot=previous_snapshot,
                    current_snapshot="",
                    previous_text=previous_text,
                    current_text="",
                    previous_hash=previous_hash,
                    current_hash="",
                    status="error",
                    error=error,
                )
            )
            print(f"[fetch] failed for {source.name}: {error}")
    return snapshots


def summarize_lines(lines: Iterable[str], limit: int = 5) -> list[str]:
    items: list[str] = []
    for line in lines:
        candidate = line.lstrip("- ").strip()
        if len(candidate) < 24:
            continue
        if len(candidate.split()) < 5:
            continue
        lowered = candidate.lower()
        if any(
            noise in lowered
            for noise in (
                "search university",
                "use case templates",
                "skip to main",
                "view lesson",
                "view course",
                "learn more",
                "clay docs",
                "clay university",
                "new at clay | clay.com",
                "conference by clay",
                "feature highlight",
                "all docs",
                "all courses",
            )
        ):
            continue
        if candidate in items:
            continue
        items.append(candidate)
        if len(items) >= limit:
            break
    return items


def detect_meaningful_change(previous_text: str, current_text: str) -> dict[str, object]:
    previous_lines = stable_lines(previous_text)
    current_lines = stable_lines(current_text)
    previous_set = set(previous_lines)
    current_set = set(current_lines)
    added = [line for line in current_lines if line not in previous_set]
    removed = [line for line in previous_lines if line not in current_set]
    similarity = SequenceMatcher(None, "\n".join(previous_lines), "\n".join(current_lines)).ratio()

    meaningful = bool(current_lines)
    reason = "initial baseline captured"
    if previous_text:
        changed_line_count = len(added) + len(removed)
        meaningful = changed_line_count >= 3 and similarity < 0.995
        reason = "content changed" if meaningful else "only minor or boilerplate changes"

    summary_bits: list[str] = []
    top_added = summarize_lines(added, limit=3)
    top_removed = summarize_lines(removed, limit=2)
    current_highlights = summarize_lines(current_lines, limit=3)
    if not top_added and meaningful:
        top_added = current_highlights
    if top_added:
        summary_bits.append("Added: " + "; ".join(top_added))
    if top_removed:
        summary_bits.append("Removed: " + "; ".join(top_removed))

    return {
        "meaningful": meaningful,
        "reason": reason,
        "similarity": round(similarity, 5),
        "added_count": len(added),
        "removed_count": len(removed),
        "top_added": top_added,
        "top_removed": top_removed,
        "summary": " ".join(summary_bits).strip(),
    }


def classify_reference_targets(source: Source, change: dict[str, object], current_text: str) -> list[str]:
    allowed = set(source.routes)
    targets = {"clay-changelog-notes.md"} & allowed
    blob_lines = list(change.get("top_added", [])) + list(change.get("top_removed", []))
    if not blob_lines:
        blob_lines = summarize_lines(stable_lines(current_text), limit=8)
    blob = " ".join(blob_lines).lower()

    for route, keywords in route_keywords().items():
        if route in allowed and any(keyword in blob for keyword in keywords):
            targets.add(route)

    if "clay-open-questions.md" in allowed and detect_ambiguity(blob_lines):
        targets.add("clay-open-questions.md")

    if not targets:
        targets = {"clay-changelog-notes.md"} if "clay-changelog-notes.md" in allowed else set()
    return sorted(targets)


def analyze_snapshots(snapshots: list[SourceSnapshot], run_at: datetime | None = None) -> dict[str, object]:
    run_at = run_at or now_utc()
    results: list[dict[str, object]] = []
    meaningful_sources = 0
    for snapshot in snapshots:
        if snapshot.status != "ok":
            results.append(
                {
                    "name": snapshot.source.name,
                    "kind": snapshot.source.kind,
                    "url": snapshot.source.url,
                    "status": snapshot.status,
                    "error": snapshot.error,
                }
            )
            continue
        change = detect_meaningful_change(snapshot.previous_text, snapshot.current_text)
        targets = (
            classify_reference_targets(snapshot.source, change, snapshot.current_text)
            if change["meaningful"]
            else []
        )
        if change["meaningful"]:
            meaningful_sources += 1
        results.append(
            {
                "name": snapshot.source.name,
                "kind": snapshot.source.kind,
                "url": snapshot.source.url,
                "status": snapshot.status,
                "previous_snapshot": snapshot.previous_snapshot,
                "current_snapshot": snapshot.current_snapshot,
                "previous_hash": snapshot.previous_hash,
                "current_hash": snapshot.current_hash,
                "meaningful_change": change["meaningful"],
                "reason": change["reason"],
                "similarity": change["similarity"],
                "added_count": change["added_count"],
                "removed_count": change["removed_count"],
                "summary": change["summary"],
                "top_added": change["top_added"],
                "top_removed": change["top_removed"],
                "reference_targets": targets,
                "source_routes": snapshot.source.routes,
            }
        )
    payload = {
        "run_at": run_at.isoformat(),
        "source_count": len(results),
        "meaningful_change_count": meaningful_sources,
        "sources": results,
    }
    RUNS_DIR.mkdir(parents=True, exist_ok=True)
    stamp = format_run_timestamp(run_at)
    run_file = RUNS_DIR / f"{stamp}_analysis.json"
    run_file.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    LATEST_ANALYSIS_FILE.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"[analyze] wrote {run_file}")
    return payload


def append_markdown_section(path: Path, heading: str, body_lines: list[str]) -> None:
    existing = path.read_text(encoding="utf-8") if path.exists() else f"# {path.stem.replace('-', ' ').title()}\n"
    block = "\n".join([f"## {heading}", *body_lines]).strip() + "\n"
    if block in existing:
        return
    updated = existing.rstrip() + "\n\n" + block + "\n"
    path.write_text(updated, encoding="utf-8")


def summary_for_reference_record(source_record: dict[str, object]) -> str:
    slug = slugify(str(source_record["name"]))
    snapshot_name = str(source_record.get("current_snapshot") or "")
    if snapshot_name:
        snapshot_path = SNAPSHOT_DIR / slug / snapshot_name
        if snapshot_path.exists():
            text = snapshot_path.read_text(encoding="utf-8")
            highlights = summarize_lines(stable_lines(text), limit=3)
            if highlights:
                return "; ".join(highlights)
    return str(source_record.get("summary") or source_record.get("reason") or "").strip()


def update_reference_files(analysis: dict[str, object], references_dir: Path = REFERENCES_DIR) -> list[str]:
    references_dir.mkdir(parents=True, exist_ok=True)
    run_label = datetime.fromisoformat(str(analysis["run_at"])).date().isoformat()
    updated: list[str] = []

    meaningful_sources = [source for source in analysis["sources"] if source.get("meaningful_change")]
    if not meaningful_sources:
        return updated

    append_markdown_section(
        references_dir / "clay-changelog-notes.md",
        f"Refresh {run_label}",
        [
            f"- {source['name']}: {summary_for_reference_record(source)}"
            for source in meaningful_sources
        ],
    )
    updated.append("clay-changelog-notes.md")

    capability_lines = [
        f"- {source['name']}: {summary_for_reference_record(source)}"
        for source in meaningful_sources
        if "clay-capabilities.md" in source.get("reference_targets", [])
    ]
    if capability_lines:
        append_markdown_section(references_dir / "clay-capabilities.md", f"Refresh {run_label}", capability_lines)
        updated.append("clay-capabilities.md")

    workflow_lines = [
        f"- {source['name']}: {summary_for_reference_record(source)}"
        for source in meaningful_sources
        if "clay-workflows.md" in source.get("reference_targets", [])
    ]
    if workflow_lines:
        append_markdown_section(references_dir / "clay-workflows.md", f"Refresh {run_label}", workflow_lines)
        updated.append("clay-workflows.md")

    limitation_lines = [
        f"- {source['name']}: {summary_for_reference_record(source)}"
        for source in meaningful_sources
        if "clay-limitations.md" in source.get("reference_targets", [])
    ]
    if limitation_lines:
        append_markdown_section(references_dir / "clay-limitations.md", f"Refresh {run_label}", limitation_lines)
        updated.append("clay-limitations.md")

    question_lines = [
        f"- Validate follow-up for {source['name']}: review beta-only or limitation-oriented changes before adopting them."
        for source in meaningful_sources
        if "clay-open-questions.md" in source.get("reference_targets", [])
    ]
    if question_lines:
        append_markdown_section(references_dir / "clay-open-questions.md", f"Refresh {run_label}", question_lines)
        updated.append("clay-open-questions.md")

    return updated


def append_refresh_log(
    analysis: dict[str, object],
    updated_files: list[str],
    log_file: Path = LOG_FILE,
) -> None:
    log_file.parent.mkdir(parents=True, exist_ok=True)
    run_at = str(analysis["run_at"])
    lines = [
        f"## Refresh Run {run_at}",
        f"- Sources checked: {analysis['source_count']}",
        f"- Meaningful changes: {analysis['meaningful_change_count']}",
    ]
    if updated_files:
        lines.append(f"- Reference files updated: {', '.join(updated_files)}")
    else:
        lines.append("- Reference files updated: none")

    if analysis["meaningful_change_count"]:
        lines.append("- Result summary:")
        for source in analysis["sources"]:
            if source.get("meaningful_change"):
                summary = source.get("summary") or source.get("reason")
                lines.append(f"  - {source['name']}: {summary}")
    else:
        lines.append("- Result summary: no meaningful changes found.")

    errors = [source for source in analysis["sources"] if source.get("status") == "error"]
    if errors:
        lines.append("- Source errors:")
        for source in errors:
            lines.append(f"  - {source['name']}: {source['error']}")

    with log_file.open("a", encoding="utf-8") as handle:
        handle.write("\n" + "\n".join(lines) + "\n")


def run_refresh(run_at: datetime | None = None) -> dict[str, object]:
    run_at = run_at or now_utc()
    print(f"[refresh] started at {run_at.isoformat()}")
    snapshots = fetch_sources(run_at=run_at)
    analysis = analyze_snapshots(snapshots, run_at=run_at)
    if analysis["meaningful_change_count"]:
        print("[update] meaningful changes found, updating references")
        updated = update_reference_files(analysis)
    else:
        print("[update] no meaningful changes found")
        updated = []
    append_refresh_log(analysis, updated)
    print(f"[log] appended structured result to {LOG_FILE}")
    if SUMMARY_PROMPT_FILE.exists():
        print("[summary] v1 uses heuristic summarization; summarize_clay_update.md is reserved for a future prompt-driven v2")
    analysis["updated_files"] = updated
    return analysis
