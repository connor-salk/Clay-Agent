"""Run the Clay refresh pipeline end to end."""

from clay_refresh import run_refresh


def main() -> None:
    result = run_refresh()
    print(
        f"[done] checked {result['source_count']} sources, "
        f"meaningful changes: {result['meaningful_change_count']}"
    )


if __name__ == "__main__":
    main()

