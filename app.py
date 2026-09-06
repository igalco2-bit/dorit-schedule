
import streamlit as st
import pandas as pd

# הגדרת תצורת העמוד בעברית ומימין לשמאל
st.set_page_config(page_title="ניהול מערכת שעות - תלמידי דורית", layout="wide")

# עיצוב CSS מתקדם שמותאם במיוחד למסכי טלפון נייד וליישור מימין לשמאל
st.markdown(
    """
    <style>
    /* יישור כללי לימין */
    .stApp {
        direction: RTL;
        text-align: right;
    }
    /* התאמת תפריט צד למסכים ניידים */
    [data-testid="stSidebar"] {
        direction: RTL;
        text-align: right;
    }
    /* תיקון יישור בטבלאות */
    table {
        direction: RTL;
        text-align: right;
    }
    th, td {
        text-align: right !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("📚 מערכת ניהול שעות - תלמידי דורית")

# הגדרת ימים ושעות אפשריות
DAYS = ["ראשון", "שלישי", "חמישי"]
HOURS = [
    "13:00 - 14:00",
    "14:00 - 15:00",
    "15:00 - 16:00",
    "16:00 - 17:00",
    "17:00 - 18:00",
    "18:00 - 19:00"
]

# אתחול מבנה הנתונים ב-Session State
if "schedule" not in st.session_state:
    st.session_state.schedule = {
        day: {hour: "" for hour in HOURS} for day in DAYS
    }

# תפריט צדדי לפעולות
st.sidebar.header("ניהול תלמידים")
action = st.sidebar.radio("בחר פעולה:", ["הוספת / עדכון תלמיד", "איפוס שעה"])

if action == "הוספת / עדכון תלמיד":
    st.sidebar.subheader("הזנה או שינוי שעה")
    student_name = st.sidebar.text_input("שם התלמיד:")
    selected_day = st.sidebar.selectbox("בחר יום:", DAYS)
    selected_hour = st.sidebar.selectbox("בחר שעה:", HOURS)
    
    if st.sidebar.button("שמור שיבוץ"):
        if not student_name.strip():
            st.sidebar.error("נא להזין שם תלמיד.")
        else:
            current_occupant = st.session_state.schedule[selected_day][selected_hour]
            if current_occupant and current_occupant != student_name:
                st.sidebar.warning(f"שים לב: השעה כבר תפוסה על ידי {current_occupant}. השיבוץ יעודכן.")
            
            # ניקוי שיבוץ קודם של התלמיד אם קיים
            for d in DAYS:
                for h, stud in st.session_state.schedule[d].items():
                    if stud == student_name:
                        st.session_state.schedule[d][h] = ""
            
            st.session_state.schedule[selected_day][selected_hour] = student_name.strip()
            st.sidebar.success(f"התלמיד {student_name} שובץ בהצלחה ביום {selected_day} בשעה {selected_hour}!")

elif action == "איפוס שעה":
    st.sidebar.subheader("פנוי שעה / הסרת תלמיד")
    reset_day = st.sidebar.selectbox("יום:", DAYS, key="reset_day")
    reset_hour = st.sidebar.selectbox("שעה פנויה:", HOURS, key="reset_hour")
    
    if st.sidebar.button("פנה שעה זו"):
        current = st.session_state.schedule[reset_day][reset_hour]
        if current:
            st.session_state.schedule[reset_day][reset_hour] = ""
            st.sidebar.success(f"השעה פונתה בהצלחה (היה משובץ: {current}).")
        else:
            st.sidebar.info("השעה כבר פנויה.")

# הצגת הלוחות לפי ימים בלשוניות
st.markdown("---")
st.subheader("לוח שיעורים שבועי")

tab_sun, tab_tue, tab_thu = st.tabs(["📅 ראשון", "📅 שלישי", "📅 חמישי"])

tabs_mapping = {
    "ראשון": tab_sun,
    "שלישי": tab_tue,
    "חמישי": tab_thu
}

for day_name, tab in tabs_mapping.items():
    with tab:
        st.markdown(f"### יום {day_name}")
        day_data = st.session_state.schedule[day_name]
        
        df_data = []
        for h in HOURS:
            student = day_data[h]
            df_data.append({
                "שעה": h,
                "שם התלמיד": student if student else "--- פנוי ---"
            })
        
        df = pd.DataFrame(df_data)
        st.dataframe(df, use_container_width=True)

# סיכום כללי
with st.expander("📊 סיכום כללי"):
    total_booked = sum(1 for d in DAYS for h, s in st.session_state.schedule[d].items() if s)
    st.write(f"סך הכל תלמידים משובצים: {total_booked} מתוך 18 שעות אפשריות.")
