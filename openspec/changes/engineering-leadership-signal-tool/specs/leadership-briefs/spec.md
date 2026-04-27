## ADDED Requirements

### Requirement: Manager blocker logging
The system SHALL allow managers to log blockers they 
are actively working to resolve but cannot unblock alone.

#### Scenario: Log a manager blocker
- **WHEN** manager adds a new blocker entry
- **THEN** system SHALL save the blocker with timestamp, 
  description, open since date, what has been tried, 
  what options remain, escalation type, and specific ask

#### Scenario: Escalation type selection
- **WHEN** manager logs a blocker
- **THEN** system SHALL require selecting one of four 
  escalation types:
  - Approval to proceed with my proposed solution
  - Nudge someone who is not responding to me
  - Choose between two equally good options
  - Choose between two equally bad options
- **AND** system SHALL display help text: "You should 
  only escalate when you need an approval, a nudge, 
  or a decision between equally weighted options. 
  Come with the problem, everything you have tried, 
  and one specific ask."

#### Scenario: What I have already tried
- **WHEN** manager logs a blocker
- **THEN** system SHALL require a free text field 
  describing everything already attempted
- **AND** system SHALL display help text: "Document 
  everything you have already tried. This shows your 
  manager you have exhausted your options before escalating."
- **AND** system SHALL enforce a maximum of 500 characters

#### Scenario: What options remain
- **WHEN** manager logs a blocker
- **THEN** system SHALL require a free text field 
  describing what options are left to try
- **AND** system SHALL display help text: "What options 
  remain that are within your control? If none — 
  that is when escalation is appropriate."
- **AND** system SHALL enforce a maximum of 500 characters

#### Scenario: Specific ask
- **WHEN** manager logs a blocker
- **THEN** system SHALL require a free text field 
  with the one precise thing needed from the manager
- **AND** system SHALL display help text: "Be specific. 
  Your manager needs to know exactly what action 
  you are asking them to take."
- **AND** system SHALL enforce a maximum of 300 characters

#### Scenario: Blocker resolution
- **WHEN** a blocker is resolved
- **THEN** system SHALL allow manager to mark it as 
  resolved with a resolution date and brief description 
  of how it was resolved
- **AND** system SHALL retain resolved blockers in 
  history for reference

#### Scenario: Blocker aging
- **WHEN** a blocker has been open for 2 or more weeks
- **THEN** system SHALL automatically highlight it 
  in the dashboard as an aging blocker
- **AND** system SHALL include it prominently in 
  the weekly briefs

---

### Requirement: Weekly leadership brief generation
The system SHALL generate a weekly leadership brief 
that synthesizes all logged signals, metric annotations, 
and manager blockers into a structured narrative for 
the manager.

#### Scenario: Generate weekly brief
- **WHEN** manager clicks the Generate Weekly Brief button
- **THEN** system SHALL call the Anthropic Claude API 
  with all signals, metric annotations, strategic contexts, 
  trend flags, and manager blockers logged in the 
  selected time period
- **AND** system SHALL generate a brief following the 
  defined section structure
- **AND** system SHALL save the generated brief to 
  SQLite with a timestamp

#### Scenario: Time period selection
- **WHEN** manager generates a brief
- **THEN** system SHALL default to the past 7 days
- **AND** system SHALL allow manager to select a 
  custom date range if needed

#### Scenario: Brief section structure
- **WHEN** system generates a brief
- **THEN** brief SHALL contain the following sections 
  in order:

  **Section 1 — Team Overview**
  A short narrative paragraph summarizing the overall 
  state of the team. Energy, momentum, and delivery 
  status at a glance. Tone should be direct and 
  factual — not defensive.

  **Section 2 — Delivery Status**
  For each engineer — delivery signal, current project, 
  and any blockers. Combination of bullet points and 
  short narrative. Highlights engineers who are blocked 
  or at risk.

  **Section 3 — Operational Metrics**
  For each annotated metric — current value, 
  classification (🔴 Red / 🟠 Orange / ⚠️ Amber), 
  plain English explanation, strategic context if set, 
  remediation owner if Red, and expected resolution 
  date if applicable.

  **Section 4 — Trends Requiring Attention**
  Automatically populated from trend detection. 
  Engineers and metrics that have been flagged as 
  sustained patterns. Includes signal type, duration, 
  and source history. This section is empty if no 
  trends are detected.

  **Section 5 — Bright Spots**
  Engineers showing strong growth signals, high energy, 
  or notable achievements captured in free text 
  observations. At least one bright spot per brief 
  where data supports it.

  **Section 6 — Manager Blockers**
  All open blockers formatted as: what is blocked, 
  how long open, what has been tried, what options 
  remain, escalation type, and specific ask. Aging 
  blockers highlighted prominently.

  **Section 7 — Manager Actions**
  AI-generated list of specific actions the manager 
  should take this week based on signals and metrics 
  logged. Each action is concrete and assigned to 
  a specific situation.

  **Section 8 — Looking Ahead**
  Expected resolution dates coming up, risks on the 
  horizon based on current trends, and any upcoming 
  decisions that need leadership attention.

#### Scenario: Brief tone and format
- **WHEN** system generates a brief
- **THEN** brief SHALL use a combination of short 
  narrative paragraphs and bullet points
- **AND** brief SHALL use clear section headers
- **AND** tone SHALL be direct, factual, and 
  solution-oriented — never defensive or apologetic
- **AND** brief SHALL be readable in under 5 minutes

#### Scenario: AI prompt construction
- **WHEN** system calls the Anthropic Claude API
- **THEN** system SHALL construct a prompt that includes:
  - All engineer signals from the selected period
  - All metric annotations and strategic contexts
  - All trend flags with duration and history
  - All open manager blockers
  - Instructions to follow the eight section structure
  - Instructions to maintain direct factual tone
  - Instructions to highlight risks without alarm 
    and bright spots without exaggeration

---

### Requirement: Brief review and editing
The system SHALL allow managers to review and edit 
the generated brief before sending to their manager.

#### Scenario: Review generated brief
- **WHEN** brief is generated
- **THEN** system SHALL display the full brief in 
  an editable text area
- **AND** system SHALL display help text: "This brief 
  is a starting point. Review it, adjust the language, 
  and make it yours before sending."

#### Scenario: Edit generated brief
- **WHEN** manager edits the brief in the text area
- **THEN** system SHALL save the edited version 
  automatically as the manager types
- **AND** system SHALL retain both the original 
  AI-generated version and the edited version in SQLite

#### Scenario: Copy brief
- **WHEN** manager is satisfied with the brief
- **THEN** system SHALL provide a Copy to Clipboard button
- **AND** system SHALL display help text: "Copy and 
  paste into your manager's Google Doc, email, 
  or Confluence page."

---

### Requirement: Historical brief storage
The system SHALL store all generated briefs for 
future reference and comparison.

#### Scenario: View past briefs
- **WHEN** manager opens the brief history view
- **THEN** system SHALL display all past briefs in 
  reverse chronological order with generation date 
  and time period covered

#### Scenario: Compare briefs
- **WHEN** manager selects two past briefs
- **THEN** system SHALL display them side by side 
  for comparison

#### Scenario: Brief retention
- **WHEN** briefs are stored in SQLite
- **THEN** system SHALL retain all briefs indefinitely 
  unless manually deleted by the manager
