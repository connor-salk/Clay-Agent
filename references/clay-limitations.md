# Clay Limitations

Use this file to document known limits, tradeoffs, and edge cases.

## Notes

- Missing data cases
- Workflow constraints
- Reliability or maintenance concerns

## Global Bucket Separation Caveat

Some leadership titles can appear adjacent to multiple functional areas. The advisor should not duplicate those titles across buckets.

For bucket assignment:
- keep Bucket 1 limited to engineering, data, AI, and developer platforms
- keep Bucket 2 limited to infrastructure, cloud, and IT operations
- keep Bucket 3 limited to cybersecurity and risk
- if ownership is ambiguous, prefer exclusion over cross-bucket duplication

## Refresh 2026-04-14
- Bulk Enrichment Docs: Enrich millions of rows quickly, securely, and at scale. No row limits, no slowdown.; Bulk enrichment makes it easy to process massive datasets—no row limits, no slowdown. Enrich millions of rows quickly, securely, and at scale.; You'll get the full power of Clay's enrichment engine without storing data inside Clay. Results are sent directly to your external destinations, like Salesforce, Snowflake, or Google Sheets, keeping your systems continuously enriched and in sync.

## Cybersecurity Targeting Caveat

`Security` is an overloaded title family and is not reliable by itself for Clay targeting. It frequently returns irrelevant non-technical roles such as physical security, corporate security, facilities security, safety, and loss prevention.

For cybersecurity targeting:
- treat generic `security` titles as ambiguous by default
- require technical qualifiers or adjacent evidence of IT/cyber ownership
- prefer false negatives over false positives when list quality is at risk
- avoid using shared title families that could overlap with other Cresting Wave buckets

## AI, Data, and Developer Platform Targeting Caveat

`Data`, `AI`, and `developer` are broad title families and are not reliable by themselves for Clay targeting. They often pull in analysts, individual contributors, non-technical strategy roles, and adjacent teams without ownership of engineering systems or internal platforms.

For this bucket:
- require evidence of engineering, platform, or system ownership
- exclude IT, infrastructure, and cybersecurity roles even when titles sound technical
- prefer false negatives over false positives when ownership is unclear
- avoid shared title families that could overlap with other Cresting Wave buckets

## Cloud and IT Infrastructure Optimization Targeting Caveat

`IT` is a broad title family and is not reliable by itself for Clay targeting. It often pulls in support roles, service desk teams, endpoint specialists, and other low-influence operators without infrastructure ownership.

For this bucket:
- require evidence of infrastructure, cloud, systems, or operations ownership
- exclude engineering and developer platform roles that belong in Bucket 1
- exclude cybersecurity roles that belong in Bucket 3
- prefer false negatives over false positives when ownership is unclear
- avoid shared title families that could overlap with other Cresting Wave buckets
