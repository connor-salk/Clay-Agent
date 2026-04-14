# Clay Workflows

Use this file to document practical Clay workflows the agent should understand.

## Notes

- Prospect sourcing workflows
- Enrichment workflows
- Qualification and segmentation workflows

## Global Bucket Separation Rules

Each Cresting Wave targeting bucket must be mutually exclusive.

- Bucket 1 owns engineering, data, AI, and developer platforms.
- Bucket 2 owns infrastructure, cloud, and IT operations.
- Bucket 3 owns cybersecurity and risk.

### Operating Rules

- Do not allow the same title to appear in multiple buckets.
- If a title could belong to multiple areas, assign it to the bucket where it most directly owns systems and budget.
- When uncertain, exclude rather than duplicate.
- The goal is clean separation of contact lists across the three buckets.

## Refresh 2026-04-14
- Sources Docs: Every Clay table begins with a source. Sources are the foundation of how data gets into your tables.; Sources are the foundation of Clay and determine how data flows into your table—think of them as the roots of a tree feeding information into your database. Just like a tree needs strong roots to grow and thrive, every Clay table needs well-configured sources to function effectively.; Every Clay table starts with a source. You can import customer data from a CSV file, connect to your CRM system, or receive real-time updates through webhooks. Sources are your gateway to organizing and managing data in Clay.
- Enrichments Docs: Learn how to run an enrichment within Clay.; Enrichments in Clay transform your data by pulling in additional information from various sources. Whether you need to verify email addresses, gather company details, or find social media profiles, Clay's enrichment tools enhance your data quickly and efficiently.; You can run enrichments individually, use pre-built templates, or create powerful recipes to automate complex workflows.
- HTTP API Docs: Facilitate seamless integration and connectivity with any APIs.; HTTP API helps you send or retrieve data from any tool or database using an API endpoint. From pulling Gong transcripts into your Clay table to referencing Marketo's API, you can call any API, even if Clay does not offer a native integration.; An HTTP API uses HTTP methods (GET, POST, PUT, DELETE) to enable communication between different systems. An API is a set of defined rules that allow applications to interact with each other, while HTTP is the protocol that defines how these requests and responses are formatted and transmitted.
- Webhooks Docs: Real-time data updates enabling application integrations and automated workflows.; Webhooks enable Clay to automatically receive data from other applications through HTTP POST requests in JSON format whenever specific events occur.; Your table updates instantly with new data, eliminating manual entry. This feature is particularly valuable for real-time updates, such as when adding new leads or modifying records based on external triggers.

## Cybersecurity Targeting Rules

When building cybersecurity prospect lists in Clay, do not use `security` by itself as a title anchor. Generic security titles often pull in physical security, facilities, corporate security, and other non-technical roles.

### High-Confidence Cyber Roles

Always include these when targeting cybersecurity decision-makers:
- CISO
- Deputy CISO
- Chief Information Security Officer
- Head of Information Security
- Head of Cybersecurity
- Director of Information Security
- Director of Cybersecurity
- Head of Security Engineering
- Director of Security Engineering
- Head of Security Operations (SecOps)
- Director of Security Operations (SecOps)
- Head of Application Security
- Director of Application Security
- Head of Cloud Security
- Director of Cloud Security
- Head of IAM / Identity
- Director of IAM / Identity
- VP Information Security
- VP Cybersecurity

### Conditional Roles

Include these carefully and only when context shows technical security ownership:
- VP Security, only when clearly tied to IT, cybersecurity, product security, or information security
- Head of Security, only when clearly tied to IT, cybersecurity, product security, or information security
- GRC leaders
- Risk technology leaders
- IT risk leaders
- Infrastructure or platform leaders with security ownership

### Exclusions

Explicitly exclude:
- Physical Security
- Corporate Security
- Facilities Security
- Safety & Security
- Loss Prevention
- Non-technical compliance roles
- Security roles not tied to IT or cybersecurity

### Operating Rules

- Never use `security` alone as a targeting anchor.
- Always pair `security` with technical qualifiers such as `cybersecurity`, `information security`, `application security`, `cloud security`, `security engineering`, `security operations`, `product security`, or `identity`.
- When uncertain, exclude rather than include.
- Optimize for decision-makers involved in cybersecurity tooling and vendor evaluation.
- Do not place clearly cyber titles into other Cresting Wave buckets.

## AI, Data, and Developer Platform Targeting Rules

When building AI, data, and developer platform prospect lists in Clay, avoid generic `data`, `AI`, or `developer` titles. Those often pull in individual contributors, analysts, non-technical strategy roles, or adjacent teams without tooling ownership.

This bucket must be limited to engineering leadership, data platform leadership, AI / ML platform leadership, and developer platform ownership. Do not include IT, infrastructure, or cybersecurity roles in this bucket.

### High-Confidence Roles

Always include these when targeting decision-makers for developer, data, or AI tooling:
- CTO
- Chief Data Officer (CDO)
- VP Engineering
- VP Data
- VP Machine Learning
- VP AI
- Head of Engineering
- Head of Data
- Head of Data Platform
- Head of Machine Learning
- Head of AI
- Head of Platform Engineering
- Head of Developer Platform
- Director of Engineering
- Director of Data Engineering
- Director of Platform Engineering
- Director of Machine Learning
- Director of AI

### Conditional Roles

Include these carefully and only when context shows platform or system ownership:
- Head of Analytics, only if tied to infrastructure, data platform, or engineering
- Data Science leadership, only if platform ownership exists
- Enterprise Architect or Data Architect roles, only if tied to platform ownership
- DevOps leadership only when tied to developer platform or internal tooling, not infrastructure

### Exclusions

Explicitly exclude:
- Data Analyst
- Business Intelligence roles without platform ownership
- Individual contributor engineers or developers
- Product managers without platform ownership
- Marketing or `AI strategy` roles with no technical ownership
- IT, infrastructure, or security roles

### Operating Rules

- Avoid using `data` or `AI` alone as a targeting anchor.
- Always anchor on engineering, platform, or system ownership.
- Prioritize leaders responsible for building and maintaining systems.
- Do not include infrastructure or security roles in this bucket.
- Optimize for people evaluating developer, data, or AI tooling.

## Cloud and IT Infrastructure Optimization Targeting Rules

When building Cloud and IT Infrastructure Optimization prospect lists in Clay, avoid generic `IT` titles. Those often pull in support roles, help desk staff, or low-influence operators without architectural or budget ownership.

This bucket must be limited to infrastructure leadership, cloud leadership, IT operations leadership, and enterprise systems ownership. Do not include engineering or platform roles from Bucket 1, and do not include cybersecurity roles from Bucket 3.

### High-Confidence Roles

Always include these when targeting infrastructure, cloud, and optimization decision-makers:
- CIO
- VP IT
- VP Infrastructure
- VP Cloud
- VP IT Operations
- Head of IT
- Head of Infrastructure
- Head of Cloud
- Head of IT Operations
- Head of End User Services, only when tied to infrastructure ownership
- Director of IT
- Director of Infrastructure
- Director of Cloud Operations
- Director of IT Operations

### Conditional Roles

Include these carefully and only when context shows infrastructure ownership:
- DevOps leadership, only when focused on infrastructure, not developer platforms
- SRE leadership, only when tied to infrastructure reliability
- Network leadership roles
- Platform operations leaders tied to infrastructure
- IT leaders with hybrid cloud or infrastructure responsibilities

### Exclusions

Explicitly exclude:
- Help desk or service desk roles
- IT support specialists
- Desktop support or endpoint-only roles
- Junior system administrators
- Engineering leadership, which belongs in Bucket 1
- Cybersecurity roles, which belong in Bucket 3

### Operating Rules

- Do not rely on `IT` alone as a targeting keyword.
- Always anchor on infrastructure, cloud, or operations ownership.
- Prioritize leaders responsible for systems, budgets, and architecture.
- Do not include engineering or platform roles from Bucket 1.
- Do not include cybersecurity roles from Bucket 3.
- Optimize for people evaluating infrastructure, cloud, and optimization tools.
