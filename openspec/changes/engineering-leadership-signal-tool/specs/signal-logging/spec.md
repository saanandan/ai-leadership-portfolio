## ADDED Requirements

### Requirement: Onboarding experience
The system SHALL provide a first-time onboarding screen 
that explains the tool and each signal before the manager 
starts logging.

#### Scenario: First launch onboarding
- **WHEN** manager opens the tool for the first time
- **THEN** system SHALL display a welcome screen explaining:
  - What the tool is and why it exists
  - What each of the five signals means and why it matters
  - How automatic trend detection works
  - How to get started
- **AND** system SHALL record onboarding completion in 
  SQLite so the screen never appears again

#### Scenario: Returning user
- **WHEN** manager opens the tool after completing onboarding
- **THEN** system SHALL skip the onboarding screen and go 
  directly to the main dashboard

---

### Requirement: Capture human signals from 1:1 meetings
The system SHALL allow managers to log human signals 
captured during 1:1 meetings with individual engineers.

#### Scenario: Log signal for engineer
- **WHEN** manager selects an engineer from the pre-loaded 
  dropdown and submits a signal entry
- **THEN** system SHALL save the signal with timestamp, 
  engineer name, energy level, delivery signal, growth 
  signal, stress level, stress source, uncertainty level, 
  uncertainty source, and free text observation

#### Scenario: Energy level capture
- **WHEN** manager logs a signal
- **THEN** system SHALL provide an energy level selector 
  with values 1 through 5
- **AND** system SHALL display help text: "How present and 
  energized is this engineer today? 1 = depleted, 
  5 = highly energized"

#### Scenario: Delivery signal capture
- **WHEN** manager logs a signal
- **THEN** system SHALL provide a delivery signal dropdown 
  with three options: On Track, At Risk, Blocked
- **AND** system SHALL display help text: "Are they on track 
  with their current commitments?"

#### Scenario: Growth signal capture
- **WHEN** manager logs a signal
- **THEN** system SHALL provide a growth signal dropdown 
  with three options: Growing, Coasting, Struggling
- **AND** system SHALL display help text: "Are they developing 
  professionally or showing signs of stagnation?"

#### Scenario: Stress signal capture
- **WHEN** manager logs a signal
- **THEN** system SHALL provide a stress level dropdown 
  with three options: Low, Moderate, High
- **AND** system SHALL display help text: "Is this engineer 
  under pressure beyond normal levels?"
- **AND** system SHALL provide a stress source dropdown 
  with four options: Workload, Team dynamics, 
  Organizational pressure, Personal
- **AND** system SHALL display help text: "What is driving 
  the stress? This determines your management response."
- **AND** stress source SHALL only be required when 
  stress level is Moderate or High

#### Scenario: Uncertainty signal capture
- **WHEN** manager logs a signal
- **THEN** system SHALL provide an uncertainty level dropdown 
  with three options: Low, Moderate, High
- **AND** system SHALL display help text: "Does this engineer 
  feel unclear about direction or priorities?"
- **AND** system SHALL provide an uncertainty source dropdown 
  with four options: Team direction, Company direction, 
  Shifting priorities, Role clarity
- **AND** system SHALL display help text: "What specifically 
  is unclear? This helps you decide whether to act locally 
  or escalate."
- **AND** uncertainty source SHALL only be required when 
  uncertainty level is Moderate or High

#### Scenario: Free text observation
- **WHEN** manager logs a signal
- **THEN** system SHALL provide an optional free text field 
  for one observation from the 1:1
- **AND** system SHALL display help text: "One thing you 
  noticed in this 1:1 that isn't captured above. Optional."
- **AND** system SHALL enforce a maximum of 500 characters

#### Scenario: Validation
- **WHEN** manager submits a signal entry
- **THEN** system SHALL require engineer name, energy level, 
  delivery signal, growth signal, and stress level before saving
- **AND** system SHALL require stress source if stress level 
  is Moderate or High
- **AND** system SHALL require uncertainty source if 
  uncertainty level is Moderate or High
- **AND** free text observation SHALL be optional

---

### Requirement: Automatic trend detection
The system SHALL automatically detect sustained negative 
signal patterns and flag them without requiring manual 
input from the manager.

#### Scenario: Stress trend detection
- **WHEN** an engineer has logged a stress level of High 
  for 3 or more consecutive check-ins
- **THEN** system SHALL automatically flag that engineer 
  as a stress trend in the dashboard
- **AND** system SHALL include that engineer in the 
  trends section of the next generated weekly brief
  with duration and stress source history

#### Scenario: Uncertainty trend detection
- **WHEN** an engineer has logged an uncertainty level 
  of High for 2 or more consecutive check-ins
- **THEN** system SHALL automatically flag that engineer 
  as an uncertainty trend in the dashboard
- **AND** system SHALL include that engineer in the 
  trends section of the next generated weekly brief
  with duration and uncertainty source history

#### Scenario: Delivery trend detection
- **WHEN** an engineer has logged a delivery signal of 
  Blocked or At Risk for 2 or more consecutive check-ins
- **THEN** system SHALL automatically flag that engineer 
  as a delivery trend in the dashboard
- **AND** system SHALL include that engineer in the 
  trends section of the next generated weekly brief

#### Scenario: Energy trend detection
- **WHEN** an engineer's average energy level is below 3 
  across 3 or more check-ins within a 30 day period
- **THEN** system SHALL automatically flag that engineer 
  as an energy trend in the dashboard
- **AND** system SHALL include that engineer in the 
  trends section of the next generated weekly brief

---

### Requirement: Signal history and filtering
The system SHALL allow managers to view and filter 
historical signals for pattern analysis.

#### Scenario: View signals by engineer
- **WHEN** manager selects an engineer from the history view
- **THEN** system SHALL display all signals for that engineer 
  in reverse chronological order showing date, energy level, 
  delivery signal, growth signal, stress level, uncertainty 
  level, and observation

#### Scenario: Filter signals by date range
- **WHEN** manager filters signals by date range
- **THEN** system SHALL show only signals within 
  the specified date range

#### Scenario: Filter signals by delivery status
- **WHEN** manager filters by delivery signal value
- **THEN** system SHALL show only engineers with that 
  delivery status in the selected period

#### Scenario: Filter signals by stress or uncertainty level
- **WHEN** manager filters by stress level or uncertainty level
- **THEN** system SHALL show only engineers matching 
  that level in the selected period