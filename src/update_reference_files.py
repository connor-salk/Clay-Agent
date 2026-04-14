"""Apply the latest change analysis to reference markdown files."""

import json

from clay_refresh import LATEST_ANALYSIS_FILE, update_reference_files


def main() -> None:
    if not LATEST_ANALYSIS_FILE.exists():
        raise FileNotFoundError(
            "No analysis file found. Run detect_doc_changes.py or refresh_clay_knowledge.py first."
        )
    analysis = json.loads(LATEST_ANALYSIS_FILE.read_text(encoding="utf-8"))
    updated = update_reference_files(analysis)
    if updated:
        print(f"[done] updated {', '.join(updated)}")
    else:
        print("[done] no reference updates were needed")


if __name__ == "__main__":
    main()
