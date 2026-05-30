import streamlit as st
from components.navigation import show_navigation


def show_about():
    st.set_page_config(
        page_title="About - Engineering Leadership Signal Tool",
        page_icon="ℹ️",
        layout="wide",
    )
    show_navigation()

    st.markdown("# ℹ️ About")
    st.markdown("---")

    st.markdown("## What this tool is")
    st.markdown(
        '<p style="font-size: 16px; line-height: 1.6">'
        "A lightweight tool for engineering leaders to capture human signals, add context to operational metrics, "
        "and generate AI-powered briefs that tell the complete story of their team — not just the numbers."
        "</p>",
        unsafe_allow_html=True,
    )

    st.markdown("---")

    st.markdown("## The principles behind it")

    st.markdown("### People leadership still matters.")
    st.markdown(
        '<p style="font-size: 16px; line-height: 1.6">'
        "AI is changing how fast we build. It is not changing the fact that humans build it. "
        "The signals that predict team health — energy, stress, uncertainty, growth — live in 1:1 conversations, "
        "not dashboards. This tool captures them consistently so nothing gets lost."
        "</p>",
        unsafe_allow_html=True,
    )

    st.markdown("### Context is what makes data useful.")
    st.markdown(
        '<p style="font-size: 16px; line-height: 1.6">'
        "A metric without context is just a number. 60% vuln remediation looks alarming. "
        "It looks different when you know the system is being retired next quarter. "
        "This tool lets you attach the human context to every metric at the point of observation "
        "— so leadership sees the story, not just the number."
        "</p>",
        unsafe_allow_html=True,
    )

    st.markdown("### If everything is equally important, nothing is.")
    st.markdown(
        '<p style="font-size: 16px; line-height: 1.6">'
        "This tool automatically detects patterns that matter — sustained stress, aging blockers, "
        "metrics that have been red for the same reason three times in a row. "
        "It surfaces what needs attention so you can focus your energy on the right things."
        "</p>",
        unsafe_allow_html=True,
    )

    st.markdown("---")

    st.markdown("## What it does")
    st.markdown(
        '<ul style="font-size: 16px; line-height: 1.6">'
        "<li><strong>Log human signals after 1:1s</strong> — 2 minutes per engineer per week</li>"
        "<li><strong>Annotate operational metrics</strong> with context and classification</li>"
        "<li><strong>Generate a weekly brief</strong> that synthesizes everything</li>"
        "<li><strong>Build organizational memory</strong> that gets smarter over time</li>"
        "</ul>",
        unsafe_allow_html=True,
    )

    st.markdown("---")

    st.markdown("## Who it's for")
    st.markdown(
        '<p style="font-size: 16px; line-height: 1.6">'
        "Any engineering leader who is tired of spending 45 minutes preparing for a check-in, "
        "tired of explaining red metrics from memory under pressure, and tired of having no evidence "
        "when something outside their control causes a slip."
        "</p>",
        unsafe_allow_html=True,
    )

    st.markdown("---")

    st.markdown("## From One Team to the Whole Org")
    st.markdown(
        '<p style="font-size: 16px; line-height: 1.6">'
        "One manager. One director's team. One consolidated view. One VP-level picture of engineering health "
        "— built from the ground up by the people closest to the work."
        "</p>",
        unsafe_allow_html=True,
    )

    st.markdown("---")

    st.markdown(
        '<p style="font-size: 14px; line-height: 1.6">'
        "Built with spec-driven development using OpenSpec, Windsurf, and the Anthropic Claude API."
        "</p>",
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    show_about()
