## ADDED Requirements

### Requirement: Team health overview dashboard
The system SHALL provide a single screen dashboard 
that gives the manager a complete picture of team 
health at a glance.

#### Scenario: Dashboard on launch
- **WHEN** manager opens the tool after completing 
  onboarding
- **THEN** system SHALL display the main dashboard 
  as the default landing screen
- **AND** dashboard SHALL show four panels: Team 
  Signal Status, Metric Status, Active Flags, 
  and Quick Actions

#### Scenario: Dashboard data freshness
- **WHEN** manager navigates to the dashboard
- **THEN** system SHALL display the most recently 
  logged data for all engineers and metrics
- **AND** system SHALL display the date of the 
  most recent signal log for each engineer so 
  the manager knows how current the data is

---

### Requirement: Team signal status panel
The system SHALL display the current signal status 
of every engineer on the team in a single view.

#### Scenario: Engineer signal table
- **WHEN** manager views the team signal status panel
- **THEN** system SHALL display a table with one 
  row per engineer showing:
  - Engineer name
  - Most recent energy level (1-5)
  - Most recent delivery signal (On Track / At Risk / Blocked)
  - Most recent growth signal (Growing / Coasting / Struggling)
  - Most recent stress level (Low / Moderate / High)
  - Most recent uncertainty level (Low / Moderate / High)
  - Date of most recent signal log
  - Active trend flags if any

#### Scenario: Trend flag indicators
- **WHEN** an engineer has one or more active trend flags
- **THEN** system SHALL display a visual indicator 
  on that engineer's row in the table
- **AND** hovering over the indicator SHALL show 
  which signals are flagged and for how long

#### Scenario: Engineer drill-down
- **WHEN** manager clicks on an engineer in the table
- **THEN** system SHALL display that engineer's 
  full signal history with trend charts for energy, 
  delivery, stress, and uncertainty over time

#### Scenario: Team-wide alert banner
- **WHEN** a team-wide stress or uncertainty pattern 
  is detected
- **THEN** system SHALL display a prominent alert 
  banner at the top of the dashboard
- **AND** banner SHALL describe the pattern: 
  "X of Y engineers have logged elevated stress 
  for Z weeks"

---

### Requirement: Metric status panel
The system SHALL display the current status of all 
active metrics in a single view.

#### Scenario: Metric status table
- **WHEN** manager views the metric status panel
- **THEN** system SHALL display a table with one 
  row per metric showing:
  - Metric name
  - Most recent value
  - Current classification (🔴 Red / 🟠 Orange / ⚠️ Amber)
  - Date of most recent annotation
  - Strategic context if set (truncated to one line)
  - Active trend flags or improvement badges

#### Scenario: Metric drill-down
- **WHEN** manager clicks on a metric in the table
- **THEN** system SHALL display that metric's full 
  annotation history with classification progression 
  over time

#### Scenario: Positive trend badge
- **WHEN** a metric has a sustained improvement badge
- **THEN** system SHALL display it prominently on 
  the metric row with the number of consecutive 
  improving annotations

---

### Requirement: Active flags panel
The system SHALL consolidate all items requiring 
attention into a single panel.

#### Scenario: Active flags list
- **WHEN** manager views the active flags panel
- **THEN** system SHALL display a consolidated list of:
  - Engineers with active trend flags — signal type 
    and duration
  - Metrics with sustained Red classification — 
    metric name and duration
  - Aging manager blockers — blocker description 
    and days open
  - Team-wide pattern alerts if any

#### Scenario: Empty active flags
- **WHEN** no active flags exist
- **THEN** system SHALL display: "No active flags — 
  your team is in good shape this week."

---

### Requirement: Quick actions panel
The system SHALL provide one-click access to the 
most common actions from the dashboard.

#### Scenario: Quick action buttons
- **WHEN** manager views the quick actions panel
- **THEN** system SHALL display four buttons:
  - Log a Signal
  - Annotate a Metric
  - Log a Blocker
  - Generate Weekly Brief

#### Scenario: Quick action navigation
- **WHEN** manager clicks any quick action button
- **THEN** system SHALL navigate directly to that 
  feature with the form ready to fill in
