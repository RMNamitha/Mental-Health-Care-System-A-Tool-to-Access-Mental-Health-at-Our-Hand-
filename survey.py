import streamlit as st

PHQ_QUESTIONS = [
    "Little interest or pleasure in doing things",
    "Feeling down, depressed, or hopeless",
    "Trouble falling or staying asleep, or sleeping too much",
    "Feeling tired or having little energy",
    "Poor appetite or overeating",
    "Feeling bad about yourself",
    "Trouble concentrating",
    "Moving or speaking slowly or being restless",
    "Thoughts that you would be better off dead"
]

GAD_QUESTIONS = [
    "Feeling nervous, anxious, or on edge",
    "Not being able to stop worrying",
    "Worrying too much",
    "Trouble relaxing",
    "Being so restless it is hard to sit still",
    "Becoming easily annoyed",
    "Feeling afraid something awful might happen"
]

def survey():
    st.header("📝 Mental Health Assessment")
    phq_score = 0
    gad_score = 0

    st.subheader("PHQ-9 Questionnaire")
    for q in PHQ_QUESTIONS:
        phq_score += st.radio(q, [0,1,2,3], horizontal=True, key=q)

    st.subheader("GAD-7 Questionnaire")
    for q in GAD_QUESTIONS:
        gad_score += st.radio(q, [0,1,2,3], horizontal=True, key=q+"_gad")

    return phq_score, gad_score

# Risk level calculation
def risk_level(score, type="PHQ"):
    if type=="PHQ":
        if score < 5:
            return "Minimal"
        elif score < 10:
            return "Mild"
        elif score < 15:
            return "Moderate"
        else:
            return "Severe"
    else:
        if score < 5:
            return "Minimal"
        elif score < 10:
            return "Mild"
        elif score < 15:
            return "Moderate"
        else:
            return "Severe"
