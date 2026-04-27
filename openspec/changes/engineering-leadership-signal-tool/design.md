## Context

This is a new engineering leadership tool that will be built from scratch. The current codebase appears to be empty or in early stages, so we have flexibility in architectural choices. The tool needs to serve engineering managers who want to track human signals alongside operational metrics to make better leadership decisions.

Key constraints:
- Must handle sensitive personal data (signals from 1:1 meetings)
- Needs to generate automated insights and briefs

## Goals / Non-Goals

**Goals:**
- Provide an intuitive interface for logging human signals per engineer
- Enable contextual annotation of operational metrics
- Generate meaningful weekly leadership briefs with AI-powered insights
- Support historical trend analysis and pattern recognition
- Create a visual dashboard for team health monitoring

**Non-Goals:**
- Real-time monitoring or surveillance of employees
- Performance evaluation or rating systems
- Integration with HR systems for formal processes
- Multi-tenant SaaS platform (single organization focus initially)
- Mobile applications (web-first approach)

## Decisions

**Database: SQLite**
- Rationale: Single file local database, zero setup required, no server needed, sufficient for single user MVP, persistent storage across sessions
- Alternative considered: PostgreSQL — rejected for MVP due to infrastructure complexity. Can migrate later for multi-user support.

**Backend/UI Framework: Python + Streamlit**
- Rationale: Rapid development, minimal code required for UI, built-in components for forms and charts, deployable to Streamlit Community Cloud with one command, appropriate for portfolio demo
- Alternative considered: Node.js + React — rejected for MVP due to complexity and slower development velocity for a solo builder

**AI Integration: Anthropic Claude API**
- Rationale: High quality text generation for leadership narratives, well documented API, consistent with portfolio's spec-driven development approach using Claude tooling
- Alternative considered: OpenAI API — rejected in favor of Anthropic for consistency with existing Claude Pro subscription

**Authentication: None for MVP**
- Rationale: Single user local tool, no sensitive data shared across users, adds unnecessary complexity for portfolio demo
- Future consideration: Add authentication if tool is adopted by multiple managers on the same team

**Brief Generation: User triggered**
- Rationale: User clicks "Generate Weekly Brief" button, no scheduling system required for MVP
- Future consideration: Scheduled delivery via email for production version

**Metric Entry: Manual**
- Rationale: No external API integrations for MVP, user enters metric name and value directly in the UI
- Future consideration: QuickSight API, Jira API, or Datadog integration for automatic metric ingestion

## Risks / Trade-offs

**AI Accuracy Risk** → Mitigation: User reviews generated brief before sending to manager. The brief is a starting point not a final document.

**Adoption Risk** → Mitigation: Simple single screen UI, minimal required fields, 15 minute weekly time commitment, immediate value visible after first use.

**Scope Creep Risk** → Mitigation: MVP is strictly limited to signal logging, metric annotation, and brief generation. Authentication, integrations, and multi-user support are 
explicitly deferred to future versions.

**Performance Risk (MVP)** → Mitigation: SQLite is sufficient for a single user logging signals for a team of 10-15 engineers over 12 months. No performance concerns at MVP scale.

**Performance Risk (Enterprise Scale)** → At organizational scale — multiple people leaders, hundreds of engineers, years of historical data — SQLite would not be sufficient. Migration path: PostgreSQL or AWS RDS for multi-user support, AWS Bedrock replacing Anthropic API for enterprise AI governance, QuickSight API integration for automatic metric ingestion, role-based access controls for director-level rollup views. In an AWS environment like Capital One this tool would be deployed on AWS Amplify with RDS backend and Bedrock integration — requiring no new vendor relationships since all components are within the existing AWS ecosystem.

**Data Privacy Risk (Enterprise Scale)** → Signal data contains sensitive observations about individual engineers. At enterprise scale this requires encryption at rest, audit logging, and compliance with HR data policies. For MVP — single user local tool, data stays on the manager's machine, no sharing infrastructure.

## Migration Plan

Since this is a new tool built from scratch, the plan is:

1. **Local Development**: Build and test entirely on local machine using SQLite and Streamlit
2. **Portfolio Deployment**: Deploy to Streamlit Community Cloud for a shareable public URL — used for interview demos
3. **Future Enterprise Path**: PostgreSQL migration, AWS Amplify hosting, Bedrock integration, QuickSight API connection — executed only if adopted beyond single user

Rollback strategy: SQLite database is a single file. Full backup is a file copy.

## Open Questions

**All Resolved:**
- Metric categories: Pre-populated defaults (Release Frequency, Vuln Remediation, CICD Health, Deployment Success Rate) plus user-defined custom categories
- Engineer setup: Pre-loaded once at setup, selected from dropdown thereafter
- Brief format: Combination of narrative paragraphs and bullet points with clear section headers
- Export: Copy-paste markdown for MVP. Google Docs API integration deferred to future version.
- Brief editing: User can edit the generated brief inside the tool before copying. Brief is a starting point not a final document.
- Historical briefs: All generated briefs stored in SQLite with timestamp. User can view and compare past briefs inside the tool.
- WBR Mode (Phase 2): Fixed metric set with week-over-week and year-over-year comparisons, initiative progress tracking 
with highlights and lowlights, and formal pre-read document 
generation for a broader leadership audience. Extends existing 
metric annotation and brief generation capabilities.
