import base64
import streamlit as st
import streamlit.components.v1 as components
from datetime import date, timedelta, datetime
import anthropic

from database import (
    get_brief_data, save_brief, update_brief_edited_content, get_all_briefs,
)
from prompts.brief_prompt import build_brief_prompt
from components.navigation import show_navigation


SYSTEM_PROMPT = """You are an expert engineering leadership coach helping a manager communicate clearly and confidently with senior leadership.

Your job is to turn raw team signal data into a structured, honest, and actionable leadership brief. The brief should help leadership understand:
- What is actually happening with the team (not just the metrics)
- What requires immediate attention
- What the manager is doing about it
- What they should watch for next

Write in a clear, professional tone. Be specific — name engineers, name metrics, quote values. Avoid vague summaries. If something is a problem, say so directly and pair it with a concrete action. If something is going well, highlight it — bright spots matter for morale and credibility.

Do not pad the brief with generic statements. Every sentence should add information that a senior leader could not have inferred from raw data alone."""


def _fmt_period_date(iso_str):
    """Format a stored ISO date string (YYYY-MM-DD) into a readable label."""
    try:
        return datetime.strptime(iso_str, '%Y-%m-%d').strftime('%b %d, %Y')
    except Exception:
        return iso_str


def _brief_period_label(brief):
    return f"{_fmt_period_date(brief['period_start'])} — {_fmt_period_date(brief['period_end'])}"


def _auto_save():
    """on_change callback for the text area. Saves edited content with a 2-second debounce."""
    now = datetime.now()
    last_saved = st.session_state.get('brief_last_saved_at')

    if last_saved and (now - last_saved).total_seconds() < 2:
        return

    brief_id = st.session_state.get('brief_db_id')
    edited = st.session_state.get('brief_text_area', '')

    if brief_id and edited:
        update_brief_edited_content(brief_id, edited)
        st.session_state.brief_last_saved_at = now


def _copy_button(text: str):
    """Render a Copy to Clipboard button via JavaScript inside a components.html iframe."""
    if not text:
        return
    encoded = base64.b64encode(text.encode('utf-8')).decode('ascii')
    components.html(
        f"""
        <script>
        async function doCopy() {{
            const raw = atob('{encoded}');
            const bytes = Uint8Array.from(raw, c => c.charCodeAt(0));
            const decoded = new TextDecoder('utf-8').decode(bytes);
            const btn = document.getElementById('cpbtn');
            try {{
                await navigator.clipboard.writeText(decoded);
                btn.textContent = '✅ Copied!';
            }} catch (_) {{
                const ta = document.createElement('textarea');
                ta.value = decoded;
                ta.style.cssText = 'position:fixed;opacity:0;top:0;left:0';
                document.body.appendChild(ta);
                ta.focus();
                ta.select();
                try {{
                    document.execCommand('copy');
                    btn.textContent = '✅ Copied!';
                }} catch (_2) {{
                    btn.textContent = '❌ Copy failed — select and copy manually';
                }}
                document.body.removeChild(ta);
            }}
            setTimeout(() => btn.textContent = '\U0001f4cb Copy to Clipboard', 2000);
        }}
        </script>
        <button id="cpbtn" onclick="doCopy()" style="
            background: #1f77b4;
            color: #ffffff;
            border: none;
            padding: 8px 20px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 14px;
            font-family: sans-serif;
            margin-top: 4px;
        ">\U0001f4cb Copy to Clipboard</button>
        """,
        height=55,
    )


def show_generate_brief():
    """Display leadership brief generation screen"""
    st.set_page_config(
        page_title="Leadership Brief - Engineering Leadership Signal Tool",
        page_icon="📋",
        layout="wide"
    )
    show_navigation()

    for key, default in [
        ('brief_content', None),
        ('brief_error', None),
        ('brief_db_id', None),
        ('brief_last_saved_at', None),
    ]:
        if key not in st.session_state:
            st.session_state[key] = default

    st.markdown("# 📋 Leadership Brief")
    st.markdown("Generate a structured brief from your logged signals, metric annotations, and blockers.")
    st.markdown("---")

    today = date.today()
    default_start = today - timedelta(days=7)

    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input(
            "Start date",
            value=default_start,
            max_value=today,
            key="brief_start_date",
        )
    with col2:
        end_date = st.date_input(
            "End date",
            value=today,
            max_value=today,
            key="brief_end_date",
        )

    st.caption("Select any date range — typically the last 7-14 days for a regular check-in, or a longer period for a quarterly review.")

    if start_date > end_date:
        st.error("❌ Start date must be before end date.")
        st.stop()

    st.markdown("---")

    if st.button("Generate Brief", type="primary"):
        st.session_state.brief_error = None
        with st.spinner("Generating your leadership brief..."):
            try:
                data = get_brief_data(start_date, end_date)
                prompt = build_brief_prompt(data)

                client = anthropic.Anthropic()
                response = client.messages.create(
                    model="claude-sonnet-4-6",
                    max_tokens=4096,
                    system=[{
                        "type": "text",
                        "text": SYSTEM_PROMPT,
                        "cache_control": {"type": "ephemeral"},
                    }],
                    messages=[{"role": "user", "content": prompt}],
                )
                content = response.content[0].text

                st.session_state.brief_content = content
                st.session_state['brief_text_area'] = content
                st.session_state.brief_last_saved_at = None

                brief_id = save_brief(start_date, end_date, content, edited_content=None)
                st.session_state.brief_db_id = brief_id

            except anthropic.AuthenticationError:
                st.session_state.brief_error = (
                    "Authentication failed. Please check that the ANTHROPIC_API_KEY "
                    "environment variable is set correctly."
                )
            except anthropic.RateLimitError:
                st.session_state.brief_error = (
                    "Rate limit reached. Please wait a moment and try again."
                )
            except anthropic.APIConnectionError:
                st.session_state.brief_error = (
                    "Could not connect to the Anthropic API. "
                    "Please check your internet connection and try again."
                )
            except Exception as e:
                st.session_state.brief_error = f"An unexpected error occurred: {e}"

    if st.session_state.brief_error:
        st.error(f"❌ {st.session_state.brief_error}")

    if st.session_state.brief_content:
        st.markdown("---")
        st.markdown("### Generated Brief")

        st.text_area(
            "Leadership Brief",
            height=700,
            key="brief_text_area",
            on_change=_auto_save,
            label_visibility="collapsed",
        )

        st.caption("This brief is a starting point. Review it, adjust the language, and make it yours before sending.")

        if st.session_state.brief_last_saved_at:
            saved_time = st.session_state.brief_last_saved_at.strftime("%-I:%M %p")
            st.caption(f"✓ Auto-saved at {saved_time}")

        current_text = st.session_state.get('brief_text_area') or st.session_state.brief_content
        _copy_button(current_text)
        st.caption("Copy and paste into your manager's Google Doc, email, or Confluence page.")

    elif not st.session_state.brief_error:
        st.info("Select a date range and click Generate to create your leadership brief.")

    # ── Brief History ─────────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("## Brief History")

    briefs = get_all_briefs()

    if not briefs:
        st.info("No briefs generated yet. Generate your first brief above.")
    else:
        for brief in briefs:
            display_content = brief['edited_content'] or brief['generated_content']
            is_edited = (
                brief['edited_content'] is not None
                and brief['edited_content'] != brief['generated_content']
            )

            try:
                gen_dt = datetime.fromisoformat(brief['generated_at']).strftime("%b %d, %Y at %-I:%M %p")
            except Exception:
                gen_dt = brief['generated_at']

            preview = display_content[:200].rstrip()
            if len(display_content) > 200:
                preview += "..."

            with st.container(border=True):
                h_col, badge_col = st.columns([5, 1])
                with h_col:
                    st.markdown(f"**{_brief_period_label(brief)}**")
                    st.caption(f"Generated {gen_dt}")
                with badge_col:
                    if is_edited:
                        st.markdown("**Edited**")
                    else:
                        st.caption("Unedited")

                st.caption(preview)

                with st.expander("View full brief"):
                    st.markdown(display_content)

                with st.expander("View Original AI Output"):
                    st.markdown(brief['generated_content'])

    # ── Compare Briefs ────────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("## Compare Briefs")

    if len(briefs) < 2:
        st.info("Generate at least two briefs to use the comparison view.")
    else:
        sel_col1, sel_col2 = st.columns(2)
        with sel_col1:
            left_idx = st.selectbox(
                "First brief",
                options=range(len(briefs)),
                format_func=lambda i: _brief_period_label(briefs[i]),
                key="compare_left_select",
            )
        with sel_col2:
            right_idx = st.selectbox(
                "Second brief",
                options=range(len(briefs)),
                format_func=lambda i: _brief_period_label(briefs[i]),
                index=1,
                key="compare_right_select",
            )

        left_brief = briefs[left_idx]
        right_brief = briefs[right_idx]

        left_content = left_brief['edited_content'] or left_brief['generated_content']
        right_content = right_brief['edited_content'] or right_brief['generated_content']

        cmp_col1, cmp_col2 = st.columns(2)
        with cmp_col1:
            st.markdown(f"**{_brief_period_label(left_brief)}**")
            st.text_area(
                "Left brief",
                value=left_content,
                height=600,
                key=f"cmp_left_{left_brief['id']}",
                disabled=True,
                label_visibility="collapsed",
            )
        with cmp_col2:
            st.markdown(f"**{_brief_period_label(right_brief)}**")
            st.text_area(
                "Right brief",
                value=right_content,
                height=600,
                key=f"cmp_right_{right_brief['id']}",
                disabled=True,
                label_visibility="collapsed",
            )


if __name__ == "__main__":
    show_generate_brief()
