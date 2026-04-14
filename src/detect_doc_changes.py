"""Fetch Clay sources, snapshot them, and analyze changes."""

from clay_refresh import analyze_snapshots, fetch_sources, now_utc


def main() -> None:
    run_at = now_utc()
    snapshots = fetch_sources(run_at=run_at)
    analysis = analyze_snapshots(snapshots, run_at=run_at)
    print(
        f"[done] analyzed {analysis['source_count']} sources, "
        f"meaningful changes: {analysis['meaningful_change_count']}"
    )


if __name__ == "__main__":
    main()

