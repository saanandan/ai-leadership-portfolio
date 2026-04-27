## 1. Project Setup and Infrastructure

- [ ] 1.1 Create Python virtual environment in project folder
- [ ] 1.2 Install required Python packages: streamlit, 
      anthropic, sqlite3
- [ ] 1.3 Create requirements.txt with all dependencies
- [ ] 1.4 Create main app.py as the Streamlit entry point
- [ ] 1.5 Create database.py for all SQLite operations
- [ ] 1.6 Create .env file for storing Anthropic API key
- [ ] 1.7 Add .env to .gitignore so API key is never 
      committed to GitHub
- [ ] 1.8 Create project folder structure:
      /app.py
      /database.py
      /pages/
      /components/
      /prompts/
      /data/
      /.env
      /requirements.txt
      /README.md

## 2. Database Schema

- [ ] 2.1 Create SQLite database file in /data folder
- [ ] 2.2 Create engineers table:
      id, name, role, active, created_at
- [ ] 2.3 Create signals table:
      id, engineer_id, energy_level, delivery_signal,
      growth_signal, stress_level, stress_source,
      uncertainty_level, uncertainty_source,
      observation, logged_at
- [ ] 2.4 Create metrics table:
      id, name, description, is_default, is_active,
      strategic_context, strategic_context_updated_at,
      created_at
- [ ] 2.5 Create metric_annotations table:
      id, metric_id, current_value, classification,
      explanation, remediation_owner_id,
      expected_resolution_date, annotated_at
- [ ] 2.6 Create strategic_context_history table:
      id, metric_id, previous_context, new_context,
      changed_at
- [ ] 2.7 Create manager_blockers table:
      id, description, open_since, what_tried,
      options_remaining, escalation_type,
      specific_ask, resolved, resolved_at,
      resolution_description, created_at
- [ ] 2.8 Create briefs table:
      id, period_start, period_end,
      generated_content, edited_content,
      generated_at
- [ ] 2.9 Create retrospectives table:
      id, period_start, period_end,
      content, generated_at
- [ ] 2.10 Create app_state table:
      id, key, value
      (used for onboarding completion flag 
      and other app-wide state)
- [ ] 2.11 Write database initialization function 
      that creates all tables on first run
- [ ] 2.12 Write helper functions for all 
      common database operations
- [ ] 2.13 Pre-populate four default metrics on 
      first run: Release Frequency, Vuln Remediation,
      CICD Health, Deployment Success Rate

## 3. Onboarding and Team Setup

- [ ] 3.1 Build onboarding screen that displays on 
      first launch only
- [ ] 3.2 Onboarding screen explains:
      - What the tool is and why it exists
      - What each of the five signals means
      - How automatic trend detection works
      - How to get started
- [ ] 3.3 Add Get Started button that sets 
      onboarding_complete flag in app_state table
- [ ] 3.4 Build team setup screen for adding engineers:
      - Engineer name field
      - Role field (optional)
      - Add Engineer button
      - List of current team members with remove option
- [ ] 3.5 Validate that at least one engineer exists 
      before allowing signal logging
- [ ] 3.6 Add team setup link from main navigation 
      so engineers can be added or removed at any time

## 4. Signal Logging

- [ ] 4.1 Build signal logging form with these fields:
      - Engineer dropdown (from engineers table)
      - Energy level slider (1-5) with help text
      - Delivery signal dropdown with help text
      - Growth signal dropdown with help text
      - Stress level dropdown with help text
      - Stress source dropdown — visible only when 
        stress level is Moderate or High — with help text
      - Uncertainty level dropdown with help text
      - Uncertainty source dropdown — visible only when 
        uncertainty level is Moderate or High — with help text
      - Free text observation field with help text
      - Log Signal button
- [ ] 4.2 Implement conditional field visibility:
      stress source only appears when stress is 
      Moderate or High, uncertainty source only 
      appears when uncertainty is Moderate or High
- [ ] 4.3 Implement form validation:
      engineer, energy level, delivery signal, 
      growth signal, and stress level are required.
      Stress source required if stress Moderate or High.
      Uncertainty source required if uncertainty 
      Moderate or High. Observation is optional.
- [ ] 4.4 Write save signal function to database.py
- [ ] 4.5 Display success confirmation after signal saved
- [ ] 4.6 Build signal history view:
      - Filter by engineer dropdown
      - Filter by date range
      - Filter by delivery signal value
      - Filter by stress level
      - Filter by uncertainty level
      - Results table in reverse chronological order
- [ ] 4.7 Implement trend detection function in database.py:
      - Stress High for 3+ consecutive check-ins
      - Uncertainty High for 2+ consecutive check-ins
      - Delivery Blocked or At Risk for 2+ consecutive
      - Energy average below 3 for 3+ check-ins in 30 days
- [ ] 4.8 Write get_active_trend_flags function that 
      returns all engineers with active trend flags
      and the type and duration of each flag

## 5. Metrics Annotation

- [ ] 5.1 Build metric management screen:
      - List of active metrics with edit and remove options
      - Add custom metric form: name and description fields
      - Remove metric button with confirmation
      - Retain history warning when removing a metric
- [ ] 5.2 Build strategic context editor:
      - Text area for strategic context on each metric
      - Save context button
      - Display last updated timestamp
      - Link to view strategic context history
- [ ] 5.3 Build strategic context history view:
      - List of all previous contexts with timestamps
- [ ] 5.4 Build metric annotation form with these fields:
      - Metric dropdown (from metrics table)
      - Current value field with help text
      - Classification dropdown: 
        🔴 Red, 🟠 Orange, ⚠️ Amber with help text
      - Plain English explanation field with help text
      - Remediation owner dropdown — visible only 
        when classification is Red — with help text
      - Expected resolution date — visible only when 
        classification is Orange or Amber — with help text
      - Submit Annotation button
- [ ] 5.5 Implement conditional field visibility:
      remediation owner only when Red,
      expected resolution date only when Orange or Amber
- [ ] 5.6 Implement form validation:
      metric, current value, classification, and 
      explanation required. Remediation owner required 
      if Red. Resolution date optional.
- [ ] 5.7 Write save annotation function to database.py
- [ ] 5.8 Display success confirmation after annotation saved
- [ ] 5.9 Build metric annotation history view:
      - Select metric dropdown
      - Display all annotations in reverse 
        chronological order
      - Show last three annotations for baseline comparison
      - Display strategic context at top of view
- [ ] 5.10 Implement metric trend detection in database.py:
      - Sustained Red: metric classified Red for 
        2+ consecutive annotations
      - Improving trend: classification improving 
        across 3+ consecutive annotations
      - Sustained improvement: better classification 
        maintained for 4+ consecutive annotations

## 6. Manager Blockers

- [ ] 6.1 Build manager blocker logging form with these fields:
      - What is blocked field with help text
      - Open since date picker
      - What I have already tried field with help text
      - What options remain field with help text
      - Escalation type dropdown:
        Approval to proceed with my proposed solution /
        Nudge someone who is not responding to me /
        Choose between two equally good options /
        Choose between two equally bad options
        with help text
      - Specific ask field with help text
      - Log Blocker button
- [ ] 6.2 Implement form validation:
      all fields required except specific ask 
      which is required but limited to 300 characters
- [ ] 6.3 Write save blocker function to database.py
- [ ] 6.4 Build active blockers view:
      - List of all open blockers in reverse 
        chronological order
      - Highlight blockers open for 2+ weeks 
        as aging blockers
      - Mark as Resolved button on each blocker
- [ ] 6.5 Build blocker resolution form:
      - Resolution date (defaults to today)
      - How it was resolved field
      - Confirm Resolution button
- [ ] 6.6 Write resolve blocker function to database.py
- [ ] 6.7 Build blocker history view:
      - All resolved blockers with resolution details
- [ ] 6.8 Implement aging blocker detection:
      any blocker open for 14+ days is flagged as aging

## 7. Leadership Brief Generation

- [ ] 7.1 Build brief generation screen:
      - Date range selector defaulting to last 7 days
      - Generate Weekly Brief button
      - Loading indicator while brief is being generated
- [ ] 7.2 Write brief data aggregation function 
      in database.py that retrieves:
      - All signals in the selected period
      - All metric annotations in the selected period
      - All strategic contexts for annotated metrics
      - All active trend flags
      - All open manager blockers
      - All aging blockers
      - Team-wide pattern alerts if any
- [ ] 7.3 Write brief prompt construction function 
      in prompts/brief_prompt.py:
      - Include all aggregated data
      - Include eight section structure instructions
      - Include tone instructions: direct, factual, 
        solution-oriented, never defensive
      - Include instruction to highlight risks 
        without alarm and bright spots without exaggeration
- [ ] 7.4 Implement Anthropic Claude API call:
      - Use claude-sonnet-4-20250514 model
      - Pass constructed prompt
      - Handle API errors gracefully
      - Display error message if generation fails
- [ ] 7.5 Display generated brief in editable text area
- [ ] 7.6 Add help text below text area: "This brief 
      is a starting point. Review it, adjust the 
      language, and make it yours before sending."
- [ ] 7.7 Auto-save edited brief as manager types
- [ ] 7.8 Save both original and edited versions 
      to briefs table in SQLite
- [ ] 7.9 Add Copy to Clipboard button with help text:
      "Copy and paste into your manager's Google Doc, 
      email, or Confluence page."
- [ ] 7.10 Build brief history view:
      - All past briefs in reverse chronological order
      - Show period covered and generation date
      - Click to view full brief
- [ ] 7.11 Build side by side brief comparison view:
      - Select two briefs from dropdowns
      - Display both briefs side by side

## 8. Historical Analysis and Retrospective

- [ ] 8.1 Build team history view:
      - Date range selector
      - Display all signals, annotations, blockers, 
        and briefs from selected period 
        in chronological order
- [ ] 8.2 Build engineer history view:
      - Engineer dropdown
      - Display all signals in reverse 
        chronological order
      - Display energy level line chart over time 
        using Streamlit chart components
      - Display delivery signal timeline
      - Display stress level timeline
      - Display uncertainty level timeline
- [ ] 8.3 Build metric history view:
      - Metric dropdown
      - Display all annotations in reverse 
        chronological order
      - Display classification progression over time
- [ ] 8.4 Build team aggregate view:
      - Summary of signal health across entire team 
        for selected period
      - Highlight engineers with active trend flags
- [ ] 8.5 Implement team-wide pattern detection 
      in database.py:
      - Stress: 50% or more of team at Moderate 
        or High for 6+ consecutive weeks
      - Uncertainty: 50% or more of team at Moderate 
        or High for 3+ consecutive weeks
      - Include most common source in alert
- [ ] 8.6 Build retrospective generation screen:
      - Date range selector
      - Generate Retrospective Summary button
      - Loading indicator
- [ ] 8.7 Write retrospective prompt construction 
      function in prompts/retrospective_prompt.py:
      - Include all data from selected period
      - Include instructions to cover team health 
        evolution, consistent strength, sustained 
        risk signals, metric trends, team-wide 
        patterns, blocker resolutions, and 
        metric improvements
- [ ] 8.8 Implement Anthropic Claude API call 
      for retrospective generation
- [ ] 8.9 Display retrospective in editable text area
- [ ] 8.10 Save retrospective to retrospectives 
      table in SQLite
- [ ] 8.11 Add help text: "Use this for quarterly 
      business reviews, performance conversations, 
      or your own reflection on how the team 
      has evolved."

## 9. Team Dashboard

- [ ] 9.1 Build main dashboard layout with four panels:
      Team Signal Status, Metric Status, 
      Active Flags, Quick Actions
- [ ] 9.2 Build team signal status panel:
      - Table with one row per engineer
      - Columns: name, energy, delivery, growth, 
        stress, uncertainty, last logged, trend flags
      - Color code each signal value
      - Display trend flag indicator on flagged rows
      - Click engineer to open drill-down view
- [ ] 9.3 Build team-wide alert banner:
      - Appears at top of dashboard when team-wide 
        stress or uncertainty pattern detected
      - Displays: "X of Y engineers have logged 
        elevated [signal] for Z weeks"
      - Dismissible but reappears on next load 
        if pattern persists
- [ ] 9.4 Build metric status panel:
      - Table with one row per active metric
      - Columns: name, last value, classification, 
        last annotated, strategic context preview,
        trend flag or improvement badge
      - Click metric to open drill-down view
- [ ] 9.5 Build active flags panel:
      - List of all active items requiring attention:
        engineer trend flags with type and duration,
        metrics with sustained Red classification,
        aging manager blockers with days open,
        team-wide pattern alerts
      - Display "No active flags — your team is 
        in good shape this week." when empty
- [ ] 9.6 Build quick actions panel:
      - Four buttons: Log a Signal, Annotate a Metric,
        Log a Blocker, Generate Weekly Brief
      - Each button navigates directly to that feature
- [ ] 9.7 Set dashboard as default landing page 
      after onboarding is complete
- [ ] 9.8 Build navigation sidebar with links to 
      all main sections:
      Dashboard, Log Signal, Annotate Metric,
      Log Blocker, Generate Brief, History, 
      Retrospective, Team Setup

## 10. Deployment and Documentation

- [ ] 10.1 Test entire application locally end to end
- [ ] 10.2 Verify all trend detection functions 
      work correctly with test data
- [ ] 10.3 Verify brief generation produces 
      correct eight section output
- [ ] 10.4 Verify retrospective generation works correctly
- [ ] 10.5 Create Streamlit Community Cloud account
- [ ] 10.6 Push final code to GitHub public repository
- [ ] 10.7 Connect GitHub repo to Streamlit Community Cloud
- [ ] 10.8 Add Anthropic API key as a secret in 
      Streamlit Community Cloud settings
- [ ] 10.9 Deploy and verify app runs correctly 
      on Streamlit Community Cloud
- [ ] 10.10 Copy shareable URL for portfolio and resume
- [ ] 10.11 Write README.md covering:
      - What the tool is and the problem it solves
      - How to run it locally
      - How to set up the Anthropic API key
      - Screenshots of key screens
      - Link to live demo on Streamlit Community Cloud
      - Tech stack and architecture decisions
      - Link to OpenSpec spec folder
- [ ] 10.12 Write ENTERPRISE_ROADMAP.md covering 
      the path from local MVP to enterprise deployment


      
