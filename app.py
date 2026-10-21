
import pickle
import secrets
import sqlite3
from datetime import date, datetime
from pathlib import Path

import pandas as pd

import numpy as np
import streamlit as st
import Orange as orange
from Orange.base import Model


# --------------------------------------------------
# NEUROVA FOCUS LAB
# --------------------------------------------------

st.set_page_config(
    page_title="Neurova Focus Lab",
    page_icon="🧠",
    layout="wide"
)


# --------------------------------------------------
# NEUROVA DESIGN SYSTEM — SAGE, CREAM & FOREST
# --------------------------------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');

    :root {
        --forest: #244536;
        --forest-deep: #173326;
        --sage: #789681;
        --sage-light: #e5eee5;
        --cream: #f7f6ef;
        --paper: #fffefa;
        --ink: #25372e;
        --muted: #6d7b70;
        --line: #dce5da;
    }
    html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
    .stApp {
        background:
          radial-gradient(ellipse at 8% 0%, rgba(210,226,208,.62), transparent 34%),
          linear-gradient(180deg, #f7f6ef 0%, #f4f6f0 100%);
        color: var(--ink);
    }
    [data-testid="stHeader"] { background: rgba(247,246,239,.88); }
    [data-testid="stMainBlockContainer"] { padding-top: 1.7rem; max-width: 1180px; }
    h1, h2, h3, h4 {
        font-family: 'Manrope', sans-serif !important;
        color: var(--forest) !important;
        letter-spacing: -0.035em;
    }
    h2 { margin-top: .4rem !important; }
    p, label, .stMarkdown { color: var(--ink); }
    [data-testid="stCaptionContainer"] { color: var(--muted); }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #203f30, #173326);
        border-right: 1px solid #355745;
    }
    [data-testid="stSidebar"] * { color: #f6f7ef !important; }
    [data-testid="stSidebar"] [data-testid="stRadio"] label {
        background: rgba(255,255,255,.055);
        border: 1px solid rgba(255,255,255,.10);
        padding: .55rem .7rem;
        border-radius: 12px;
        margin-bottom: .35rem;
    }
    [data-testid="stMetric"] {
        background: rgba(255,254,250,.9);
        border: 1px solid var(--line);
        padding: 18px 20px;
        border-radius: 18px;
        box-shadow: 0 8px 26px rgba(34,65,47,.055);
    }
    div[data-testid="stForm"], div[data-testid="stExpander"] {
        background: rgba(255,254,250,.74);
        border: 1px solid var(--line);
        border-radius: 18px;
        padding: 16px;
        box-shadow: 0 6px 22px rgba(34,65,47,.035);
    }
    [data-testid="stTabs"] [data-baseweb="tab-list"] {
        gap: 8px; background: #eaf5e6; padding: 6px; border-radius: 14px;
    }
    [data-testid="stTabs"] [data-baseweb="tab"] {
        border-radius: 10px; padding: 10px 16px; font-weight: 700;
        background: #e0f1dc !important; color: #17271d !important;
    }
    [data-testid="stTabs"] [aria-selected="true"] {
        background: #cfe9c8 !important; color: #17271d !important;
        box-shadow: 0 2px 8px rgba(20,50,33,.08);
    }
    .stButton > button, .stFormSubmitButton > button {
        border-radius: 12px; font-weight: 700; min-height: 2.8rem;
        background: #e0f1dc !important; color: #17271d !important;
        border: 1px solid #c7e2c1 !important;
        transition: background .18s ease, border-color .18s ease, transform .18s ease;
    }
    .stButton > button[kind="primary"], .stFormSubmitButton > button[kind="primary"] {
        background: #d5edcf !important; color: #17271d !important;
        border: 1px solid #b9dcb2 !important;
        box-shadow: 0 4px 12px rgba(36,69,54,.08);
    }
    .stButton > button:hover, .stFormSubmitButton > button:hover {
        background: #cde8c6 !important; color: #17271d !important;
        border-color: #a9d29f !important; transform: translateY(-1px);
    }
    input, textarea, [data-baseweb="select"] > div {
        border-radius: 11px !important;
    }
    [data-testid="stDataFrame"] {
        border: 1px solid var(--line); border-radius: 14px; overflow: hidden;
    }
    [data-testid="stAlert"] { border-radius: 14px; }
    .nv-hero {
        position: relative; overflow: hidden; display: flex; align-items: center;
        gap: 22px; padding: 30px 32px; border-radius: 26px;
        background: linear-gradient(120deg, #173326 0%, #294f3b 62%, #52765d 100%);
        box-shadow: 0 16px 42px rgba(26,57,39,.17); margin-bottom: 18px;
    }
    .nv-hero:after {
        content: ''; position: absolute; width: 260px; height: 260px;
        right: -55px; top: -115px; border-radius: 50%;
        border: 1px solid rgba(255,255,255,.15);
        box-shadow: 0 0 0 28px rgba(255,255,255,.035), 0 0 0 58px rgba(255,255,255,.025);
    }
    .nv-logo {
        flex: 0 0 78px; width: 78px; height: 78px; display: grid;
        place-items: center; border-radius: 23px;
        background: rgba(244,247,235,.12); border: 1px solid rgba(255,255,255,.24);
    }
    .nv-kicker { color: #c9ddc9 !important; font-size: 11px; font-weight: 800;
        letter-spacing: .22em; text-transform: uppercase; margin: 0 0 5px 0; }
    .nv-title { color: #fffdf5 !important; font-family: 'Manrope',sans-serif;
        font-size: clamp(25px, 3.6vw, 40px); font-weight: 800; line-height: 1.08;
        letter-spacing: -.045em; margin: 0; }
    .nv-subtitle { color: #e1eadf !important; margin: 9px 0 0 0;
        font-size: 14px; max-width: 610px; }
    .nv-step {
        background: #e7eee4; border: 1px solid #d7e3d5; border-radius: 14px;
        padding: 12px 15px; color: #244536; font-weight: 700; font-size: 13px;
        margin: 8px 0 18px 0;
    }
    .nv-eyebrow { color: #66816c; font-size: 11px; font-weight: 800;
        letter-spacing: .13em; text-transform: uppercase; }
    @media (max-width: 640px) {
        [data-testid="stMainBlockContainer"] { padding: 1rem .8rem 2rem; }
        .nv-hero { padding: 22px 18px; gap: 14px; border-radius: 20px; align-items: flex-start; }
        .nv-logo { width: 56px; height: 56px; flex-basis: 56px; border-radius: 17px; }
        .nv-logo svg { width: 38px; height: 38px; }
        .nv-subtitle { font-size: 13px; }
        div[data-testid="stForm"], div[data-testid="stExpander"] { padding: 11px; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "ml model (2.0).pkcls"


@st.cache_resource
def load_model():
    """Load the model exported from orange Data Mining."""
    with MODEL_PATH.open("rb") as file:
        return pickle.load(file)


def get_suggestions(answers, prediction):
    """Generate detailed, supportive, answer-aware concentration suggestions."""
    tips = []

    # Suggestions are based on reported habits, not on a medical assessment.
    if answers["sleep_hours_per_night"] < 7:
        tips.append(
            "**Sleep routine:** Your reported sleep duration is below seven hours, so begin by "
            "protecting a consistent wind-down and bedtime where your schedule allows. Try preparing "
            "your school materials earlier, dimming screens before bed, and keeping wake-up times fairly "
            "regular rather than trying to change everything in one night. Notice whether you feel more "
            "alert during your next study session; if sleep problems persist, speak with a trusted adult "
            "or health professional."
        )

    if answers["sleep_quality_1to5"] <= 2:
        tips.append(
            "**Make bedtime more restful:** You rated your sleep quality as low, which can leave studying "
            "feeling harder the next day. Create a simple repeatable routine—for example, finish demanding "
            "work a little earlier, prepare tomorrow's to-do list, and choose a quiet, comfortable activity "
            "before bed. If noise, worry, discomfort, or repeated waking is affecting your sleep, consider "
            "discussing the problem with a trusted adult instead of trying to manage it alone."
        )

    if answers["study_hours_per_day"] >= 6:
        tips.append(
            "**Make long study days more manageable:** You reported six or more study hours a day, so check "
            "whether your schedule includes enough breaks, meals, movement, and time to unwind. Divide work "
            "into clear blocks, each with one specific outcome—such as solving five questions or revising one "
            "concept—then take a short break before the next block. Quality matters as well as time spent, so "
            "use practice questions or explain a concept in your own words to check whether the session is useful."
        )

    if answers["recreational_screen_hours_per_day"] >= 5:
        tips.append(
            "**Create intentional screen breaks:** You reported substantial recreational screen time. You do "
            "not need to remove screens completely; instead, choose a few moments when you will step away, "
            "especially just before a planned study block or during a break. Keep your phone out of immediate "
            "reach while working if notifications pull your attention away, and decide in advance when you will "
            "check messages again. Try this for one session and record whether it felt easier to return to work."
        )

    if answers["physical_activity_minutes_per_day"] < 20:
        tips.append(
            "**Add a little movement to your day:** Your answers suggest that you currently get less than "
            "twenty minutes of physical activity on a typical day. If it is comfortable and possible for you, "
            "try a short walk, gentle stretching, dancing, cycling, or another activity you enjoy. You can split "
            "movement into smaller moments instead of treating it as another demanding task. Choose something "
            "that fits your routine and notice whether it helps you feel refreshed before studying."
        )

    if answers["academic_pressure_1to5"] >= 4:
        tips.append(
            "**Reduce the feeling of academic overload:** You rated academic pressure as high. Write down the "
            "tasks on your mind, then mark the one that is most urgent or that you can realistically begin today. "
            "Break that task into a first step small enough to complete in about 10–20 minutes, such as outlining "
            "an answer or attempting two questions. A short, specific plan can make the workload feel clearer; "
            "if deadlines or expectations still feel unmanageable, talk with a teacher or trusted adult about "
            "what needs prioritising."
        )

    if answers["workload_rating_1to5"] >= 4:
        tips.append(
            "**Plan around your current workload:** You described your workload as difficult or overwhelming. "
            "Instead of making a very long to-do list, separate tasks into 'must do soon', 'can do later', and "
            "'need help with'. Estimate a realistic amount of time for the first task, leave a little space for "
            "unexpected work, and review the plan after completing it. If several deadlines conflict, ask a "
            "teacher, parent, or trusted adult to help you decide the order rather than trying to handle every "
            "task at once."
        )

    if answers["mood_rating_1to5"] <= 2:
        tips.append(
            "**Support your mood while studying:** You reported a low mood, and it is okay if concentration "
            "feels less predictable on some days. Begin with a gentle goal—such as reviewing one page or "
            "completing a single question—and give yourself credit for making a start. Make room for something "
            "comforting outside study, such as music, a hobby, time outdoors, or a conversation with someone "
            "you trust. If low mood continues or starts affecting daily life, consider reaching out to a trusted "
            "adult, school counsellor, or qualified professional."
        )

    if answers["social_support_1to5"] <= 2:
        tips.append(
            "**Build in support instead of studying alone with every difficulty:** You rated your support "
            "network as limited. Consider asking a classmate to revise one topic with you, asking a teacher to "
            "clarify a difficult concept, or telling a trusted family member what kind of help would be useful. "
            "You do not have to share anything personal that you are not comfortable sharing; even a practical "
            "request, such as help planning deadlines, can make a task feel less isolating. Choose someone who "
            "listens respectfully and supports your wellbeing."
        )

    if answers["peer_pressure_1to5"] >= 4:
        tips.append(
            "**Set goals around your own learning, not other people's pace:** You reported high peer pressure. "
            "Comparing marks, study hours, or revision speed can make it harder to notice your own progress. "
            "Choose a personal target you can control, such as revising one concept or correcting mistakes from "
            "a practice paper, and track your progress against your earlier work. You can learn useful methods "
            "from classmates without copying their schedules; your plan should fit your needs, commitments, and "
            "energy."
        )

    if answers["study_breaks_per_study_day"] == 0:
        tips.append(
            "**Schedule breaks before you feel completely drained:** You reported taking no study breaks on a "
            "typical day. Try working on one defined task for a manageable period, then pause briefly to stretch, "
            "drink water, look away from your screen, or walk around. Choose a rhythm that suits the task and "
            "your attention rather than forcing a rigid timer. When you return, write down the next action so it "
            "is easier to restart without spending time deciding where to begin."
        )

    # Category-specific guidance leads the list so the result feels connected
    # to the model output, while keeping the category as an estimate.
    if prediction == "LOW":
        tips.insert(
            0,
            "**Your focus plan — start small and reduce friction:** The model placed your answers in the LOW "
            "concentration category, which is an estimate based on the information provided—not a judgement "
            "about your ability. Pick one clear, achievable task and define what 'finished' means before you "
            "start. Put away one likely distraction, keep the materials you need nearby, and try a short work "
            "period followed by a break. If your mind wanders, gently return to the next step rather than "
            "criticising yourself; use the session to learn which conditions make starting easier."
        )
    elif prediction == "MEDIUM":
        tips.insert(
            0,
            "**Your focus plan — strengthen what is already working:** The model placed your answers in the "
            "MEDIUM concentration category. Treat this as a starting point for experimentation, not a fixed "
            "label: choose one change at a time, such as setting a specific session goal, reducing notifications, "
            "or taking a planned break. After studying, note what helped, what interrupted you, and how focused "
            "you felt. Keeping the experiment small makes it easier to identify patterns without changing your "
            "whole routine at once."
        )
    elif prediction == "HIGH":
        tips.insert(
            0,
            "**Your focus plan — protect your useful habits:** The model placed your answers in the HIGH "
            "concentration category, but focus can naturally vary with the task, sleep, stress, and the day. "
            "Notice which conditions seem to support your best sessions and keep them realistic—for example, "
            "a clear goal, a comfortable study space, and planned breaks. Avoid filling every available hour just "
            "because studying is going well; keep time for rest and other parts of life. If a difficult day comes "
            "along, use the same small-step approach rather than expecting yourself to perform perfectly."
        )

    if not tips:
        tips.append(
            "**Keep building a balanced study rhythm:** Your answers did not trigger a specific habit-based tip, "
            "so choose one routine to observe this week. Before a session, set one clear goal and prepare what "
            "you need; afterwards, note what helped you stay engaged and what distracted you. Continue making "
            "space for sleep, breaks, movement, and supportive connections. You do not need to change everything "
            "at once—small experiments can help you discover what works best for you."
        )

    return tips


def predict_concentration(model, answers):
    """Create an orange data row in the model's expected feature order."""
    domain = model.domain

    # Ensure every input expected by the trained model is available.
    expected_features = [var.name for var in domain.attributes]
    missing = [name for name in expected_features if name not in answers]

    if missing:
        raise ValueError(
            "The saved model expects input columns not found in the website: "
            + ", ".join(missing)
        )

    # orange uses the model's original domain and feature order.
    row = [answers[var.name] for var in domain.attributes]

    # Supply unknown class values, if the model's domain includes a target.
    row.extend([None] * len(domain.class_vars))

    # Supply unknown meta values if any exist in the saved model's domain.
    row.extend([None] * len(domain.metas))

    table = orange.data.Table.from_list(domain, [row])

    raw_prediction = model(table, ret=Model.Value)
    value = np.asarray(raw_prediction).reshape(-1)[0]

    class_var = domain.class_var

    if class_var is None:
        raise ValueError(
            "The saved model has no class variable. Check the Target setting in orange."
        )

    if isinstance(value, (str, np.str_)):
        label = str(value)
    else:
        label_index = int(round(float(value)))
        if label_index < 0 or label_index >= len(class_var.values):
            raise ValueError("The model returned an invalid class index.")
        label = str(class_var.values[label_index])

    # Obtain class probabilities when the model supports them.
    confidence = None
    try:
        probabilities = model(table, ret=Model.Probs)
        probabilities = np.asarray(probabilities).reshape(1, -1)[0]
        labels = list(class_var.values)

        if label in labels:
            confidence = float(probabilities[labels.index(label)]) * 100
    except Exception:
        pass

    return label, confidence


# --------------------------------------------------

# --------------------------------------------------
# FIVE-PAGE NAVIGATION
# --------------------------------------------------
PAGES = [
    "Home",
    "Concentration Prediction",
    "Personal Focus Experiment",
    "My Focus Pattern Report",
    "Tiny Next-Step Planner (AI model)",
]
if "neurova_active_page" not in st.session_state:
    st.session_state["neurova_active_page"] = "Home"

active_page = st.session_state["neurova_active_page"]

st.markdown("""
<style>
.nv-nav-label { color:#66816c; font-size:11px; font-weight:800; letter-spacing:.14em;
text-transform:uppercase; margin: 0 0 8px 2px; }
div[data-testid="stHorizontalBlock"] .stButton > button {
    min-height:2.65rem; background:#e0f1dc !important; color:#17271d !important;
    border-color:#c7e2c1 !important; font-weight:700;
}
div[data-testid="stHorizontalBlock"] .stButton > button[kind="primary"] {
    background:#cfe9c8 !important; color:#17271d !important; border-color:#b9dcb2 !important;
}
.nv-home-card { background:#e5eee5; border:1px solid #dce5da; border-radius:18px;
padding:20px 22px; margin:8px 0; }
.nv-home-card h3 { margin:0 0 7px 0; color:#244536; font-size:18px; }
.nv-home-card p { margin:0; color:#607767; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="nv-nav-label">Your focus dashboard</div>', unsafe_allow_html=True)
nav_cols = st.columns(5)
for index, page in enumerate(PAGES):
    with nav_cols[index]:
        if st.button(
            page,
            key=f"nav_{index}",
            type="primary" if active_page == page else "secondary",
            use_container_width=True,
        ):
            st.session_state["neurova_active_page"] = page
            st.rerun()

st.divider()

if active_page == "Home":
    st.markdown(
        """
        <section class="nv-hero">
          <div class="nv-logo" aria-label="Neurova leaf and focus mark">
            <svg width="54" height="54" viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M32 52V27" stroke="#F7F6EF" stroke-width="3.2" stroke-linecap="round"/>
              <path d="M32 38C16 38 11 28 12 16C25 16 34 22 32 38Z" fill="#C7DEC2"/>
              <path d="M32 30C31 17 39 9 52 10C53 23 46 32 32 30Z" fill="#91B69A"/>
              <path d="M19 22L30 34M46 16L34 28" stroke="#315B43" stroke-width="2.2" stroke-linecap="round"/>
              <circle cx="32" cy="53" r="3.5" fill="#E7D9A9"/>
            </svg>
          </div>
          <div>
            <p class="nv-kicker">Student wellbeing · AI capstone · SDG 3</p>
            <h1 class="nv-title">NEUROVA FOCUS LAB</h1>
            <p class="nv-subtitle">Understand your habits. Explore your focus. Build a study rhythm that feels right for you.</p>
          </div>
        </section>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("""
    <div class="nv-home-card">
      <h3>Welcome to your personal focus space</h3>
      <p>NEUROVA FOCUS LAB helps you explore everyday study habits, estimate a concentration category,
      record focus sessions and discover small next steps. It is an educational reflection tool,
      not a medical assessment.</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("### Explore your dashboard")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="nv-home-card"><h3>Concentration Prediction</h3><p>Questionnaire and AI results</p></div>', unsafe_allow_html=True)
        st.markdown('<div class="nv-home-card"><h3>Personal Focus Experiment</h3><p>Record study sessions and habits</p></div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="nv-home-card"><h3>My Focus Pattern Report</h3><p>Charts and saved history</p></div>', unsafe_allow_html=True)
        st.markdown('<div class="nv-home-card"><h3>Tiny Next-Step Planner (AI model)</h3><p>Educational next-step predictions</p></div>', unsafe_allow_html=True)
    if st.button("Start", type="primary", key="home_start", use_container_width=True):
        st.session_state["neurova_active_page"] = "Concentration Prediction"
        st.rerun()
    st.caption("SDG 3 — Good Health and Well-being · Your routine, your reflection, your next step.")

if active_page == "Concentration Prediction":
    st.info(
        "This educational tool estimates a concentration category from your answers. "
        "It is not a medical assessment or diagnosis. You do not need to enter your name."
    )


    reset_col, reset_help_col = st.columns([1, 2])
    with reset_col:
        if st.button("Reset current results", key="reset_current_results"):
            for key in (
                "neurova_latest_prediction",
                "neurova_latest_answers",
                "neurova_all_next_steps",
            ):
                st.session_state.pop(key, None)
            st.session_state["neurova_reset_notice"] = True
            st.rerun()
    with reset_help_col:
        st.caption(
            "Clears this session's displayed concentration result and saved-in-session "
            "planner predictions. It does not delete focus check-ins."
        )
    if st.session_state.pop("neurova_reset_notice", False):
        st.success("Current results have been reset. Saved focus history is unchanged.")


    # --------------------------------------------------
    # INPUT FORM
    # --------------------------------------------------

    st.subheader("Start with your everyday routine")
    st.write(
        "Answer based on your recent, typical experience. "
        "There are no right or wrong answers."
    )

    with st.form("concentration_form"):
        left, right = st.columns(2)

        with left:
            st.markdown("#### Daily habits")

            sleep_hours = st.slider(
                "Sleep per night (hours)",
                min_value=1.0,
                max_value=10.5,
                value=7.0,
                step=0.5,
                help="Choose the approximate number of hours you usually sleep."
            )

            study_hours = st.slider(
                "Study hours per day",
                min_value=0.0,
                max_value=10.0,
                value=3.0,
                step=0.5
            )

            screen_hours = st.slider(
                "Recreational screen time per day (hours)",
                min_value=0.0,
                max_value=9.0,
                value=2.0,
                step=0.5,
                help="Include leisure screen time, not schoolwork if possible."
            )

            activity_minutes = st.slider(
                "Physical activity per day (minutes)",
                min_value=0,
                max_value=120,
                value=30,
                step=5
            )

            breaks = st.slider(
                "Study breaks on a typical study day",
                min_value=0,
                max_value=5,
                value=2,
                step=1
            )

            sleep_quality = st.slider(
                "Sleep quality  ·  1 = Very poor  |  5 = Very good",
                min_value=1,
                max_value=5,
                value=3,
            )

        with right:
            st.markdown("#### School and personal experience")

            academic_pressure = st.slider(
                "Academic pressure  ·  1 = Very low  |  5 = Very high",
                min_value=1,
                max_value=5,
                value=3,
            )

            mood = st.slider(
                "Mood rating  ·  1 = Very low  |  5 = Very positive",
                min_value=1,
                max_value=5,
                value=3,
            )


            social_support = st.slider(
                "Support network  ·  1 = Very little  |  5 = Strong support",
                min_value=1,
                max_value=5,
                value=3,
            )

            workload = st.slider(
                "Workload difficulty  ·  1 = Manageable  |  5 = Overwhelming",
                min_value=1,
                max_value=5,
                value=3,
            )

            peer_pressure = st.slider(
                "Peer pressure  ·  1 = Very low  |  5 = Very high",
                min_value=1,
                max_value=5,
                value=2,
            )

        submitted = st.form_submit_button(
            "✨ Analyse My Concentration",
            use_container_width=True,
            type="primary"
        )


    # --------------------------------------------------
    # PREDICTION AND RESULTS
    # --------------------------------------------------

    if submitted:
        answers = {
            "sleep_hours_per_night": sleep_hours,
            "study_hours_per_day": study_hours,
            "recreational_screen_hours_per_day": screen_hours,
            "physical_activity_minutes_per_day": activity_minutes,
            "academic_pressure_1to5": academic_pressure,
            "mood_rating_1to5": mood,
            "social_support_1to5": social_support,
            "sleep_quality_1to5": sleep_quality,
            "study_breaks_per_study_day": breaks,
            "workload_rating_1to5": workload,
            "peer_pressure_1to5": peer_pressure
        }

        try:
            model = load_model()
            prediction, confidence = predict_concentration(model, answers)

            st.session_state["neurova_latest_prediction"] = prediction
            st.session_state["neurova_latest_answers"] = answers.copy()

            if prediction not in {"LOW", "MEDIUM", "HIGH"}:
                st.error(
                    f"The model returned '{prediction}', which is not one of "
                    "the expected categories LOW, MEDIUM, or HIGH. "
                    "Check the target labels in orange."
                )
            else:
                st.divider()
                st.subheader("Your concentration insight")

                if prediction == "LOW":
                    st.warning("Predicted concentration category: LOW")
                    explanation = (
                        "Your answers fall into the LOW category according to "
                        "the trained model. Start with small, manageable changes."
                    )
                elif prediction == "MEDIUM":
                    st.info("Predicted concentration category: MEDIUM")
                    explanation = (
                        "Your answers fall into the MEDIUM category according "
                        "to the trained model. Small routine improvements may help."
                    )
                else:
                    st.success("Predicted concentration category: HIGH")
                    explanation = (
                        "Your answers fall into the HIGH category according "
                        "to the trained model. Keep supporting your focus with balanced habits."
                    )

                st.write(explanation)

                if confidence is not None:
                    st.caption(
                        f"Model confidence for this category: {confidence:.1f}% "
                        "(not a measure of real-world accuracy)"
                    )

                st.markdown("### Suggestions for you")

                suggestions = get_suggestions(answers, prediction)
                for suggestion in suggestions:
                    st.markdown(f"- {suggestion}")

                st.caption(
                    "These suggestions are general educational guidance, not medical advice. "
                    "Your result is an estimate and should not be used to label or judge a student."
                )

        except FileNotFoundError:
            st.error(
                "Model file not found. Put 'ml model (2.0).pkcls' in the same "
                "folder as app.py and try again."
            )
        except Exception as error:
            # Show the real failure category instead of incorrectly blaming every
            # problem on the feature count/target. Pickled orange objects can fail
            # before feature validation if they were saved with an incompatible
            # orange/Qt environment.
            error_text = str(error)
            error_lower = error_text.lower()
            if any(token in error_lower for token in ("pyqt4", "pyqt5", "pyside", "qt platform", "qt bindings")):
                st.error("The saved model cannot be loaded because its pickle requires a Qt GUI package that is unavailable in this environment.")
                st.markdown(
                    "**Fix:** In orange, reopen the workflow and save/export the trained "
                    "classification model itself (not the workflow/widget), using the same "
                    "orange version as the app environment. Then replace `ml model (2.0).pkcls`. "
                    "If you run this locally, install a compatible orange3 environment; do not "
                    "try to fix this by adding random PyQt4/PySide2 packages, which are obsolete."
                )
            elif "no class variable" in error_lower or "class variable" in error_lower or "target" in error_lower:
                st.error("The saved orange model has no usable target/class variable. Set `concentration_level` as the Target in orange, retrain, and export the trained model again.")
            elif "input columns not found" in error_lower or "unexpected model input" in error_lower:
                st.error("The saved model's input features do not match the questionnaire. Update the questionnaire to supply every required feature, or retrain the model using the app's available columns.")
            else:
                st.error("Concentration prediction failed. The detailed error is shown below so you can identify whether this is a model-file, orange/Qt, target, or feature mismatch.")
            st.code(error_text)



    # --------------------------------------------------
    # NEUROVA FOCUS LAB: PERSONAL FOCUS EXPERIMENT
    # --------------------------------------------------
DB_PATH = BASE_DIR / "neurova_focus_lab.db"
# A random, session-scoped owner token prevents visitors sharing one public app
# from seeing or deleting one another's focus records.
if "neurova_owner_token" not in st.session_state:
    st.session_state["neurova_owner_token"] = secrets.token_urlsafe(24)
OWNER_TOKEN = st.session_state["neurova_owner_token"]


def init_database():
    """Create a local database for experiment check-ins."""
    with sqlite3.connect(DB_PATH) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS focus_checkins (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                checkin_date TEXT NOT NULL,
                experiment_name TEXT NOT NULL,
                habit_to_test TEXT NOT NULL,
                focus_before INTEGER NOT NULL,
                focus_after INTEGER NOT NULL,
                sleep_hours REAL,
                study_hours REAL,
                predicted_concentration TEXT,
                notes TEXT,
                created_at TEXT NOT NULL,
                owner_id TEXT
            )
            """
        )
        # Backwards-compatible migration for databases created by older versions.
        columns = {
            row[1] for row in connection.execute("PRAGMA table_info(focus_checkins)")
        }
        if "owner_id" not in columns:
            connection.execute("ALTER TABLE focus_checkins ADD COLUMN owner_id TEXT")
        # Existing legacy rows are retained and assigned once to the session that
        # first opens this upgraded database; they are never shown to every visitor.
        connection.execute(
            "UPDATE focus_checkins SET owner_id = ? WHERE owner_id IS NULL",
            (OWNER_TOKEN,),
        )
        connection.commit()


def save_checkin(record):
    with sqlite3.connect(DB_PATH) as connection:
        connection.execute(
            """
            INSERT INTO focus_checkins (
                checkin_date, experiment_name, habit_to_test,
                focus_before, focus_after, sleep_hours, study_hours,
                predicted_concentration, notes, created_at, owner_id
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                record["checkin_date"],
                record["experiment_name"],
                record["habit_to_test"],
                record["focus_before"],
                record["focus_after"],
                record["sleep_hours"],
                record["study_hours"],
                record["predicted_concentration"],
                record["notes"],
                datetime.now().isoformat(timespec="seconds"),
                OWNER_TOKEN,
            ),
        )
        connection.commit()


def load_checkins():
    with sqlite3.connect(DB_PATH) as connection:
        return pd.read_sql_query(
            "SELECT * FROM focus_checkins WHERE owner_id = ? ORDER BY checkin_date DESC, id DESC",
            connection,
            params=(OWNER_TOKEN,),
        )


def delete_checkin(checkin_id):
    """Delete exactly one check-in by its database ID."""
    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.execute(
            "DELETE FROM focus_checkins WHERE id = ? AND owner_id = ?",
            (int(checkin_id), OWNER_TOKEN),
        )
        connection.commit()
        return cursor.rowcount


def clear_all_checkins():
    """Permanently remove all saved check-ins after explicit confirmation."""
    with sqlite3.connect(DB_PATH) as connection:
        connection.execute(
            "DELETE FROM focus_checkins WHERE owner_id = ?", (OWNER_TOKEN,)
        )
        connection.commit()


init_database()

if active_page == "Personal Focus Experiment":
    st.markdown("## Personal Focus Experiment")
    st.write("Test one small study habit and record how your session felt over time.")
    st.subheader("Record a study session")
    st.write(
        "Choose one habit to test and record your focus before and after studying. "
        "Use the same 1–5 scale each time."
    )

    latest_prediction = st.session_state.get("neurova_latest_prediction", "Not recorded")
    st.caption(f"Most recent concentration model prediction in this session: {latest_prediction}")

    with st.form("focus_experiment_form", clear_on_submit=True):
        experiment_name = st.text_input(
            "Experiment name",
            placeholder="e.g., Testing short study breaks",
        )
        habit_to_test = st.selectbox(
            "Habit you are testing",
            [
                "Take a short break between study blocks",
                "Put my phone away while studying",
                "Start with one small task",
                "Study in a quieter place",
                "Try a different study method",
                "Other / just tracking my routine",
            ],
        )
        checkin_date = st.date_input("Session date", value=date.today())
        c1, c2 = st.columns(2)
        with c1:
            focus_before = st.slider(
                "Focus before studying (1 = very low, 5 = very high)",
                min_value=1, max_value=5, value=3,
            )
            sleep_hours_checkin = st.number_input(
                "Sleep last night (hours)",
                min_value=0.0, max_value=24.0, value=7.0, step=0.5,
            )
        with c2:
            focus_after = st.slider(
                "Focus after studying (1 = very low, 5 = very high)",
                min_value=1, max_value=5, value=3,
            )
            study_hours_checkin = st.number_input(
                "Study session duration (hours)",
                min_value=0.0, max_value=24.0, value=1.0, step=0.25,
            )
        notes = st.text_area(
            "Optional notes",
            placeholder="What felt helpful or difficult during this session?",
        )
        save_button = st.form_submit_button(
            "Save Focus Check-in", type="primary", use_container_width=True
        )

    if save_button:
        if not experiment_name.strip():
            st.error("Please enter an experiment name before saving.")
        else:
            save_checkin(
                {
                    "checkin_date": checkin_date.isoformat(),
                    "experiment_name": experiment_name.strip(),
                    "habit_to_test": habit_to_test,
                    "focus_before": int(focus_before),
                    "focus_after": int(focus_after),
                    "sleep_hours": float(sleep_hours_checkin),
                    "study_hours": float(study_hours_checkin),
                    "predicted_concentration": latest_prediction,
                    "notes": notes.strip(),
                }
            )
            st.session_state.pop("neurova_all_next_steps", None)
            st.success("Your check-in has been saved on this computer.")
            st.rerun()

    st.caption(
        "Privacy note: this prototype stores check-ins in a local SQLite file named "
        "'neurova_focus_lab.db' in the project folder. Avoid entering names or other "
        "identifying information."
    )
    st.caption(
        "Privacy note: check-ins are stored in the SQLite database in this project folder. "
        "Avoid entering names or other identifying information."
    )

if active_page == "My Focus Pattern Report":
    st.markdown("## My Focus Pattern Report")
    st.subheader("Your focus patterns")
    history = load_checkins()

    if history.empty:
        data_notice = st.session_state.pop("neurova_data_notice", None)
        if data_notice == "all_cleared":
            st.success("All saved check-ins were deleted. The report has been refreshed.")
        elif data_notice == "one_deleted":
            st.success("The selected check-in was deleted. The report has been refreshed.")
        st.info(
            "No focus check-ins saved yet. Record a session in the Personal Focus "
            "Experiment tab, and your history will appear here."
        )
    else:
        st.markdown("#### Manage saved check-ins")
        delete_options = {
            f'#{int(row["id"])} · {row["checkin_date"]} · {row["experiment_name"]} '
            f'(focus {int(row["focus_before"])} → {int(row["focus_after"])})':
            int(row["id"])
            for _, row in history.iterrows()
        }
        with st.expander("Delete one check-in or clear all history", expanded=False):
            selected_label = st.selectbox(
                "Choose the single check-in to delete",
                options=list(delete_options.keys()),
                key="delete_checkin_selection",
            )
            if st.button("Delete selected check-in", key="delete_one_checkin"):
                try:
                    deleted_count = delete_checkin(delete_options[selected_label])
                    st.session_state.pop("neurova_all_next_steps", None)
                    if deleted_count == 1:
                        st.session_state["neurova_data_notice"] = "one_deleted"
                    else:
                        st.session_state["neurova_data_notice"] = "not_found"
                    st.rerun()
                except sqlite3.Error as error:
                    st.error(f"Could not delete this check-in: {error}")

            st.warning(
                "Clearing history permanently deletes every saved check-in from this "
                "database. Export or back up the database first if you may need it."
            )
            confirm_clear = st.checkbox(
                "I understand that all saved check-ins will be permanently deleted.",
                key="confirm_clear_all_history",
            )
            if st.button(
                "Clear all history",
                key="clear_all_history",
                disabled=not confirm_clear,
            ):
                try:
                    clear_all_checkins()
                    st.session_state.pop("neurova_all_next_steps", None)
                    st.session_state["neurova_data_notice"] = "all_cleared"
                    st.session_state.pop("confirm_clear_all_history", None)
                    st.rerun()
                except sqlite3.Error as error:
                    st.error(f"Could not clear history: {error}")

        data_notice = st.session_state.pop("neurova_data_notice", None)
        if data_notice == "one_deleted":
            st.success("The selected check-in was deleted. The report has been refreshed.")
        elif data_notice == "all_cleared":
            st.success("All saved check-ins were deleted. The report has been refreshed.")
        elif data_notice == "not_found":
            st.warning("That check-in was not found; the report has been refreshed.")

        total_sessions = len(history)
        avg_before = history["focus_before"].mean()
        avg_after = history["focus_after"].mean()
        change = avg_after - avg_before

        m1, m2, m3 = st.columns(3)
        m1.metric("Sessions recorded", total_sessions)
        m2.metric("Average focus before", f"{avg_before:.1f}/5")
        m3.metric("Average focus after", f"{avg_after:.1f}/5", f"{change:+.1f}")

        chart_data = history.sort_values("checkin_date").set_index("checkin_date")[
            ["focus_before", "focus_after"]
        ]
        st.markdown("#### Focus before and after each session")
        st.line_chart(chart_data)

        st.markdown("#### Saved check-ins")
        display_columns = [
            "checkin_date", "experiment_name", "habit_to_test",
            "focus_before", "focus_after", "sleep_hours", "study_hours",
            "predicted_concentration", "notes",
        ]
        st.dataframe(
            history[display_columns],
            use_container_width=True,
            hide_index=True,
        )
        st.caption(
            "These are self-reported observations. A change in focus score alone "
            "does not prove that the tested habit caused the change."
        )


    # --------------------------------------------------
# Accept either extension in case Windows hid/changed the file extension.
NEXT_STEP_MODEL_CANDIDATES = [
    BASE_DIR / "ml (new 2.0).pkcls",
    BASE_DIR / "ml (new 2.0).pkls",
]


@st.cache_resource
def load_next_step_model():
    """Load the separate orange model trained to predict next_step."""
    model_path = next((path for path in NEXT_STEP_MODEL_CANDIDATES if path.exists()), None)
    if model_path is None:
        expected = " or ".join(path.name for path in NEXT_STEP_MODEL_CANDIDATES)
        raise FileNotFoundError(f"Could not find the next-step model. Expected: {expected}")
    with model_path.open("rb") as file:
        return pickle.load(file)


def predict_next_step(
    model,
    focus_before,
    focus_after,
    sleep_hours=None,
    study_session_duration_hours=None,
):
    """Predict next_step using whichever supported inputs the orange model expects."""
    domain = model.domain
    class_var = domain.class_var
    if class_var is None:
        raise ValueError("The saved next-step model has no target. In orange, set next_step as Target and save again.")

    row = []
    for var in domain.attributes:
        name = "".join(ch for ch in var.name.lower() if ch.isalnum())
        if "before" in name:
            row.append(float(focus_before))
        elif "after" in name:
            row.append(float(focus_after))
        elif "sleep" in name and "hour" in name:
            row.append(None if pd.isna(sleep_hours) else float(sleep_hours))
        elif "study" in name and ("duration" in name or "session" in name):
            row.append(
                None
                if pd.isna(study_session_duration_hours)
                else float(study_session_duration_hours)
            )
        else:
            raise ValueError(
                f"Unexpected model input '{var.name}'. Supported inputs are focus before, focus after, "
                "sleep hours last night, and study session duration. In orange, exclude experiment_id, "
                "focus_change, and any other columns from Features unless you also add their values to the app."
            )

    row.extend([None] * len(domain.class_vars))
    row.extend([None] * len(domain.metas))
    table = orange.data.Table.from_list(domain, [row])
    raw = model(table, ret=Model.Value)
    value = np.asarray(raw).reshape(-1)[0]

    if isinstance(value, (str, np.str_)):
        return str(value)
    index = int(round(float(value)))
    if index < 0 or index >= len(class_var.values):
        raise ValueError("The model returned an invalid next_step category.")
    return str(class_var.values[index])



if active_page == "Tiny Next-Step Planner (AI model)":
    st.markdown("## Tiny Next-Step Planner (AI model)")
    st.write(
        "Predict a next study strategy for each saved focus experiment using the orange model. "
        "This is an educational prototype; suggestions are not guaranteed to improve focus."
    )
    planner_history = load_checkins()

    if planner_history.empty:
        st.session_state.pop("neurova_all_next_steps", None)
        st.info("First, save at least one session in Personal Focus Experiment. Then return here.")
    else:
        st.caption(f"Saved experiments found: {len(planner_history)}. Each row below gets its own prediction.")
        if st.button("✨ Predict Next Step for Every Experiment", type="primary", key="predict_all_next_steps"):
            try:
                next_model = load_next_step_model()
                results = []
                for _, record in planner_history.iterrows():
                    recommendation = predict_next_step(
                        next_model,
                        int(record["focus_before"]),
                        int(record["focus_after"]),
                        record.get("sleep_hours"),
                        record.get("study_hours"),
                    )
                    results.append(recommendation)
                planner_history = planner_history.copy()
                planner_history["predicted_next_step"] = results
                st.session_state["neurova_all_next_steps"] = planner_history[
                    ["checkin_date", "experiment_name", "habit_to_test", "focus_before", "focus_after", "predicted_next_step"]
                ].copy()
            except FileNotFoundError as error:
                st.error(str(error))
                st.info("Put the saved next-step model in the same folder as app.py. Check the exact extension in File Explorer.")
            except Exception as error:
                st.error("The next-step prediction could not be completed. Details:")
                st.code(str(error))

        predictions = st.session_state.get("neurova_all_next_steps")
        if predictions is not None and not predictions.empty:
            st.dataframe(predictions, use_container_width=True, hide_index=True)
            st.caption(
                "If the training labels were generated by rules, predictions reflect those rules—not proof that a strategy works for every student. "
                "Predictions are generated when you click the button, so click it again after adding new experiments."
            )


    # --------------------------------------------------

st.divider()
st.caption("NEUROVA | Student AI Capstone Project | SDG 3: Good Health and Well-being")
