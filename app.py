import streamlit as st
import database
import survey
import chatbot
import pandas as pd

# Setup
database.create_tables()
st.set_page_config(page_title="MindCare", layout="wide")
st.title("🧠 MindCare ")

if "user" not in st.session_state:
    st.session_state.user = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Sidebar
menu = ["Login", "Register"]
choice = st.sidebar.selectbox("Menu", menu)

# --- REGISTER ---
if choice == "Register":
    st.subheader("Register")
    u = st.text_input("Username", key="reg_user")
    p = st.text_input("Password", type="password", key="reg_pass")
    if st.button("Create Account"):
        if database.add_user(u, p):
            st.success("✅ Account created! Please login.")
        else:
            st.error("❌ Username already exists")

# --- LOGIN ---
if choice == "Login":
    st.subheader("Login")
    u = st.text_input("Username", key="login_user")
    p = st.text_input("Password", type="password", key="login_pass")
    if st.button("Login"):
        if database.login_user(u, p):
            st.session_state.user = u
            st.success(f"Welcome {st.session_state.user}!")
        else:
            st.error("❌ Invalid credentials")

# --- AFTER LOGIN ---
if st.session_state.user:

    # --- SURVEY ---
    st.subheader("📝 Take Mental Health Survey")
    phq, gad = survey.survey()

    if st.button("Submit Survey"):
        database.save_score(st.session_state.user, phq, gad)
        st.success(f"Survey saved! PHQ-9 Risk: {survey.risk_level(phq)}, GAD-7 Risk: {survey.risk_level(gad, 'GAD')}")

    # --- SCORE CHART ---
    scores = database.get_scores(st.session_state.user)
    if scores:
        df = pd.DataFrame(scores, columns=["PHQ","GAD","Date"])
        df["PHQ_Risk"] = df["PHQ"].apply(lambda x: survey.risk_level(x))
        df["GAD_Risk"] = df["GAD"].apply(lambda x: survey.risk_level(x,"GAD"))
        st.subheader("📈 Score Progress Over Time")
        st.line_chart(df.set_index("Date")[["PHQ","GAD"]])

    # --- CHATBOT ---
    st.subheader("💬 MindCare Companion Chat")
    user_text = st.text_input("Talk to me", key="chat_input")
    if st.button("Send"):
        if user_text.strip() != "":
            reply, emotion = chatbot.chatbot_reply(user_text)
            database.save_chat(st.session_state.user, user_text, emotion)
            st.session_state.chat_history.append(("You", user_text))
            st.session_state.chat_history.append(("MindCare", reply))
            # Show chat like WhatsApp/ChatGPT
            for sender, msg in st.session_state.chat_history[-20:]:
                if sender=="You":
                    st.markdown(f"**You:** {msg}")
                else:
                    st.markdown(f"**🤖 MindCare:** {msg}")

            if emotion=="negative":
                st.warning("You seem low today. Try breathing, walking, or talking to someone you trust 💙")
            else:
                st.success("You sound positive today 🌱")

    # --- WEEKLY REPORT ---
    st.subheader("🗓️ Weekly Summary")
    scores_week, chats_week = database.get_weekly_report(st.session_state.user)
    if scores_week:
        df_week = pd.DataFrame(scores_week, columns=["PHQ","GAD","Date"])
        df_week["PHQ_Risk"] = df_week["PHQ"].apply(lambda x: survey.risk_level(x))
        df_week["GAD_Risk"] = df_week["GAD"].apply(lambda x: survey.risk_level(x,"GAD"))
        st.markdown("**Your scores this week:**")
        st.dataframe(df_week)
    if chats_week:
        st.markdown("**Your chat emotions this week:**")
        df_chat = pd.DataFrame(chats_week, columns=["Message","Emotion","Date"])
        st.dataframe(df_chat)
