## ADDED Requirements

### Requirement: Team history view
The system SHALL provide a unified view of all logged 
data across a selected time period for pattern review 
and retrospective analysis.

#### Scenario: View team history by date range
- **WHEN** manager selects a date range in the 
  history view
- **THEN** system SHALL display all signals, metric 
  annotations, manager blockers, and generated briefs 
  from that period in chronological order

#### Scenario: Engineer history view
- **WHEN** manager selects a specific engineer in 
  the history view
- **THEN** system SHALL display all signals logged 
  for that engineer across all time in reverse 
  chronological order
- **AND** system SHALL display a simple trend summary 
  showing how their energy, delivery, growth, stress, 
  and uncertainty signals have changed over time

#### Scenario: Metric history view
- **WHEN** manager selects a specific metric in 
  the history view
- **THEN** system SHALL display all annotations for 
  that metric across all time in reverse chronological 
  order
- **AND** system SHALL display the progression of 
  classifications over time — showing whether the 
  metric has been trending toward Red, Orange, 
  or Amber

---

### Requirement: Signal trend visualization
The system SHALL display simple visual trend indicators 
for engineer signals over time.

#### Scenario: Engineer signal trend chart
- **WHEN** manager views an engineer's history
- **THEN** system SHALL display a simple line chart 
  showing energy level over time
- **AND** system SHALL display a timeline of delivery 
  signal changes — On Track, At Risk, Blocked
- **AND** system SHALL display a timeline of stress 
  level changes — Low, Moderate, High
- **AND** system SHALL display a timeline of 
  uncertainty level changes — Low, Moderate, High

#### Scenario: Team aggregate view
- **WHEN** manager views the team history overview
- **THEN** system SHALL display aggregate signal 
  health across the entire team for the selected period
- **AND** system SHALL highlight any engineers who 
  have active trend flags during that period

---

### Requirement: Team-wide pattern detection
The system SHALL detect when a majority of the team 
shows the same sustained signal — indicating a systemic 
issue rather than an individual one.

#### Scenario: Team-wide stress pattern detection
- **WHEN** 50% or more of the team has logged a 
  stress level of Moderate or High for 6 or more 
  consecutive weeks (3 sprints)
- **THEN** system SHALL flag a team-wide stress alert 
  in the dashboard
- **AND** system SHALL generate a specific callout 
  in the weekly brief: "Team-wide stress pattern 
  detected — X of Y engineers have logged elevated 
  stress for Z weeks. This is a systemic signal 
  that may require organizational intervention."
- **AND** system SHALL include the most common stress 
  source across the flagged engineers
- **AND** system SHALL display help text in the 
  dashboard: "When a majority of your team shows 
  the same signal over an extended period, the 
  cause is likely systemic — not individual."

#### Scenario: Team-wide uncertainty pattern detection
- **WHEN** 50% or more of the team has logged an 
  uncertainty level of Moderate or High for 3 or 
  more consecutive weeks
- **THEN** system SHALL flag a team-wide uncertainty 
  alert in the dashboard
- **AND** system SHALL generate a specific callout 
  in the weekly brief: "Team-wide uncertainty pattern 
  detected — X of Y engineers have logged elevated 
  uncertainty for Z weeks. The team may need clearer 
  direction on priorities or company direction."
- **AND** system SHALL include the most common 
  uncertainty source across the flagged engineers

---

### Requirement: Positive metric trend detection
The system SHALL recognize and surface when operational 
metrics are improving over time — not just when they 
are worsening.

#### Scenario: Metric improving trend
- **WHEN** a metric has been annotated as improving 
  across 3 or more consecutive annotations — moving 
  from Red to Orange, Orange to Amber, or Amber 
  to resolved
- **THEN** system SHALL flag that metric as trending 
  positive in the dashboard
- **AND** system SHALL include it in the Bright Spots 
  section of the weekly brief: "X metric has improved 
  for Z consecutive annotations — moving from 
  [previous classification] toward resolution."

#### Scenario: Metric sustained improvement
- **WHEN** a metric has maintained a better 
  classification for 4 or more consecutive annotations
- **THEN** system SHALL display a sustained improvement 
  badge on that metric in the dashboard
- **AND** system SHALL note in the brief: "X metric 
  has sustained improvement for Z annotations — 
  the remediation plan is working."

---

### Requirement: Retrospective summary
The system SHALL allow managers to generate a 
retrospective summary for any time period — useful 
for quarterly reviews or performance conversations.

#### Scenario: Generate retrospective summary
- **WHEN** manager selects a date range and clicks 
  Generate Retrospective Summary
- **THEN** system SHALL call the Anthropic Claude API 
  with all data from that period
- **AND** system SHALL generate a narrative summary 
  covering:
  - How the team's overall health evolved during 
    the period
  - Which engineers showed consistent strength
  - Which engineers showed sustained risk signals
  - How operational metrics trended
  - What team-wide patterns were detected
  - What blockers were present and how they resolved
  - Which metrics improved and which remained 
    persistently red
- **AND** system SHALL save the retrospective to 
  SQLite with the date range and generation timestamp

#### Scenario: Retrospective use cases
- **WHEN** manager generates a retrospective
- **THEN** system SHALL display help text: "Use this 
  for quarterly business reviews, performance 
  conversations, or your own reflection on how 
  the team has evolved."
