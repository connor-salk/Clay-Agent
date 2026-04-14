# Clay Sources

This file defines the official Clay sources the refresh pipeline is allowed to monitor.

## Rules
- Use official Clay sources only
- Prefer Clay University and Clay Docs pages
- Focus on operational guidance that helps answer:
  - how to create tables and projects
  - how sources work
  - how enrichments work
  - how signals and workflows should be structured
  - how HTTP API and webhooks are used in Clay
- Ignore third-party blogs, YouTube summaries, Reddit, and generic SEO pages

## Primary monitored sources

The list below is the canonical machine-readable manifest used by the refresh pipeline.

## Monitored Sources
- Sources Docs | sources | https://university.clay.com/docs/sources | clay-workflows,clay-limitations,clay-changelog-notes
- Enrichments Docs | enrichments | https://university.clay.com/docs/enrichments | clay-capabilities,clay-workflows,clay-limitations,clay-changelog-notes
- Bulk Enrichment Docs | bulk-enrichment | https://university.clay.com/docs/bulk-enrichment | clay-capabilities,clay-workflows,clay-limitations,clay-changelog-notes
- HTTP API Docs | http-api | https://www.clay.com/university/lesson/http-api-clay-101 | clay-capabilities,clay-workflows,clay-limitations,clay-open-questions,clay-changelog-notes
- Webhooks Docs | webhooks | https://university.clay.com/docs/webhook-integration-docs | clay-capabilities,clay-workflows,clay-limitations,clay-open-questions,clay-changelog-notes

## Notes
- Keep entries in the exact `Name | kind | url | routes` format.
- `routes` values map to files in `references/`.
- Only `https` URLs on official Clay domains are allowed by the refresh pipeline.

## Monitoring priorities
1. Changes to setup steps
2. Changes to workflow recommendations
3. New limitations or constraints
4. New capabilities
5. New terminology or UI patterns that affect how instructions should be written

## Output routing
- capability changes -> references/clay-capabilities.md
- workflow/setup changes -> references/clay-workflows.md
- constraints/limits/caveats -> references/clay-limitations.md
- uncertain or ambiguous changes -> references/clay-open-questions.md
- time-stamped summaries -> references/clay-changelog-notes.md
