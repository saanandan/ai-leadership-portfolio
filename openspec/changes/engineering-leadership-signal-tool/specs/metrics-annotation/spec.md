## ADDED Requirements

### Requirement: Metric setup and management
The system SHALL allow managers to set up operational 
metrics they are responsible for tracking and reporting.

#### Scenario: Pre-populated default metrics
- **WHEN** manager opens the metrics section for the first time
- **THEN** system SHALL pre-populate four default metrics:
  Release Frequency, Vuln Remediation, CICD Health, 
  Deployment Success Rate

#### Scenario: Add custom metric
- **WHEN** manager needs to track a metric not in the defaults
- **THEN** system SHALL allow adding a custom metric by 
  entering a name and optional description
- **AND** system SHALL display help text: "Add any metric 
  your leadership tracks that isn't in the default list"

#### Scenario: Remove metric
- **WHEN** manager no longer needs to track a metric
- **THEN** system SHALL allow removing it from the active 
  metrics list
- **AND** system SHALL retain historical annotations for 
  that metric even after removal

---

### Requirement: Annotate operational metrics
The system SHALL allow managers to attach human context 
and classification to any operational metric at the point 
of observation.

#### Scenario: Log metric annotation
- **WHEN** manager selects a metric and adds an annotation
- **THEN** system SHALL save the annotation with metric name, 
  current value, timestamp, classification, plain English 
  explanation, and expected resolution date if applicable

#### Scenario: Metric classification
- **WHEN** manager annotates a metric
- **THEN** system SHALL provide three classification options:
  - 🔴 Red — Genuine Red: this is a real problem 
    that needs immediate action
  - 🟠 Orange — Contextual Red: looks bad but here 
    is why it is not alarming
  - ⚠️ Amber — Temporary Red: will resolve by a 
    specific date because of a known reason
- **AND** system SHALL display help text: "Not all red 
  metrics are equally urgent. This classification helps 
  leadership understand what actually needs attention 
  and what is already being managed."

#### Scenario: Plain English explanation
- **WHEN** manager classifies a metric
- **THEN** system SHALL require a plain English explanation 
  of why the metric looks the way it does
- **AND** system SHALL display help text: "Explain the context 
  behind this metric in plain English. This becomes part of 
  your weekly brief."
- **AND** system SHALL enforce a maximum of 1000 characters

#### Scenario: Expected resolution date
- **WHEN** manager classifies a metric as Orange or Amber
- **THEN** system SHALL provide an optional expected 
  resolution date field
- **AND** system SHALL display help text: "When do you 
  expect this metric to normalize? Giving a date builds 
  credibility with leadership."

#### Scenario: Remediation owner
- **WHEN** manager annotates a metric that is Genuine Red
- **THEN** system SHALL require selecting an engineer 
  from the pre-loaded team dropdown as the remediation owner
- **AND** system SHALL display help text: "Who on your team 
  owns the fix? Accountability drives resolution."

#### Scenario: Validation
- **WHEN** manager submits a metric annotation
- **THEN** system SHALL require metric name, current value, 
  classification, and plain English explanation
- **AND** system SHALL require remediation owner if 
  classification is Red
- **AND** expected resolution date SHALL be optional 
  for Orange and Amber

---

### Requirement: Historical metric tracking
The system SHALL maintain historical records of all 
metric annotations over time.

#### Scenario: View metric history
- **WHEN** manager selects a metric from the history view
- **THEN** system SHALL display all annotations for that 
  metric in reverse chronological order showing date, 
  value, classification, explanation, and resolution date

#### Scenario: Metric trend pattern
- **WHEN** a metric has been classified as Red for 2 or 
  more consecutive annotations
- **THEN** system SHALL automatically flag that metric 
  as a sustained issue in the dashboard
- **AND** system SHALL include it in the trends section 
  of the next generated weekly brief

#### Scenario: Add strategic context to metric
- **WHEN** manager sets up or edits a metric
- **THEN** system SHALL provide an optional Strategic Context 
  field for standing explanations that apply across multiple 
  annotation periods
- **AND** system SHALL display help text: "Use this for 
  standing context that explains why this metric may look 
  a certain way over an extended period — such as resource 
  constraints, system retirement, or shifting priorities. 
  This context will appear alongside every annotation for 
  this metric."
- **AND** system SHALL display the Strategic Context 
  prominently whenever this metric is viewed or annotated
- **AND** Strategic Context SHALL be optional and 
  editable at any time
- **AND** system SHALL timestamp every change to 
  Strategic Context and retain the full history of 
  previous versions
- **AND** system SHALL display help text on the history 
  view: "Strategic context history shows how the standing 
  explanation for this metric has evolved over time."

#### Scenario: Historical baseline comparison
- **WHEN** manager views a metric
- **THEN** system SHALL display the last three annotations 
  for context — showing whether the situation is improving, 
  stable, or worsening
