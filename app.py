import streamlit as st
import pandas as pd

# הגדרת כותרת האתר בלשונית ואייקון מותאם אישית (📚)
st.set_page_config(
    page_title="מערכת שעות",
    page_icon="📚",
    layout="centered"
)

# עיצוב CSS מלא ליישור מימין לשמאל, תיקון טבלאות והקטנת כותרות
st.markdown(
    """
    <style>
    .stApp {
        direction: RTL;
        text-align: right;
    }
    /* יישור הטבלאות והתאים מימין לשמאל */
    table {
        direction: RTL;
    }
    th, td {
        text-align: right !important;
    }
    /* הקטנת כל הכותרות באפליקציה */
    h1 {
        font-size: 1.6rem !important;
    }
    h2 {
        font-size: 1.3rem !important;
    }
    h3 {
        font-size: 1.1rem !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("📚 מערכת ניהול שעות")

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

# שימוש בלשוניות ראשיות במסך המרכזי
main_tab1, main_tab2 = st.tabs(["📅 צפייה במערכת השעות", "✍️ ניהול והזנת תלמידים"])

with main_tab1:
    st.subheader("לוח שיעורים שבועי")
    day_tab_sun, day_tab_tue, day_tab_thu = st.tabs(["יום ראשון", "יום שלישי", "יום חמישי"])
    
    days_mapping = {
        "ראשון": day_tab_sun,
        "שלישי": day_tab_tue,
        "חמישי": day_tab_thu
    }
    
    for day_name, tab in days_mapping.items():
        with tab:
            st.markdown(f"### מערכת שעות - יום {day_name}")
            day_data = st.session_state.schedule[day_name]
            
            df_data = []
            for h in HOURS:
                student = day_data[h]
                # סדר העמודות: קודם "שעה" (מימין) ואז "שם התלמיד" (משמאל)
                df_data.append({
                    "שעה": h,
                    "שם התלמיד": student if student else "--- פנוי ---"
                })
            
            df = pd.DataFrame(df_data)
            st.table(df)

with main_tab2:
    st.subheader("ניהול תלמידים (הוספה, שינוי או פינוי שעה)")
    
    action = st.radio("בחר פעולה:", ["הוספת / עדכון תלמיד", "איפוס שעה"])
    
    if action == "הוספת / עדכון תלמיד":
        st.markdown("#### הזנה או שינוי שעה לתלמיד")
        student_name = st.text_input("שם התלמיד:")
        selected_day = st.selectbox("בחר יום:", DAYS)
        selected_hour = st.selectbox("בחר שעה:", HOURS)
        
        if st.button("שמור שיבוץ"):
            if not student_name.strip():
                st.error("נא להזין שם תלמיד.")
            else:
                current_occupant = st.session_state.schedule[selected_day][selected_hour]
                if current_occupant and current_occupant != student_name:
                    st.warning(f"שים לב: השעה כבר תפוסה על ידי {current_occupant}. השיבוץ יעודכן.")
                
                # ניקוי שיבוץ קודם של התלמיד אם קיים במקום אחר
                for d in DAYS:
                    for h, stud in st.session_state.schedule[d].items():
                        if stud == student_name:
                            st.session_state.schedule[d][h] = ""
                
                st.session_state.schedule[selected_day][selected_hour] = student_name.strip()
                st.success(f"התלמיד {student_name} שובץ בהצלחה ביום {selected_day} בשעה {selected_hour}!")

    elif action == "איפוס שעה":
        st.markdown("#### פנוי שעה קיימת")
        reset_day = st.selectbox("יום:", DAYS, key="reset_day")
        reset_hour = st.selectbox("שעה פנויה:", HOURS, key="reset_hour")
        
        if st.button("פנה שעה זו"):
            current = st.session_state.schedule[reset_day][reset_hour]
            if current:
                st.session_state.schedule[reset_day][reset_hour] = ""
                st.success(f"השעה פונתה בהצלחה (היה משובץ: {current}).")
            else:
                st.info("השעה כבר פנויה.")

# סיכום כללי בתחתית
st.markdown("---")
total_booked = sum(1 for d in DAYS for h, s in st.session_state.schedule[d].items() if s)
st.info(f"📊 סיכום מערכת: סך הכל {total_booked} תלמידים משובצים מתוך 18 שעות אפשריות.")
