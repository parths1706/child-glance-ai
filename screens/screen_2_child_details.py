import streamlit as st
import time
from utils.navigation import go_to
from datetime import date
# from datetime import datetime

def calculate_age(dob):
    today = date.today()
    years = today.year - dob.year
    months = today.month - dob.month

    if today.day < dob.day:
        months -= 1
    if months < 0:
        years -= 1
        months += 12

    return years, months


def screen_child_details():
    st.markdown(
        """
        <div class="app-header">
            <span class="title-emoji floating-emoji">✨</span>
            <span class="app-title-text">Know Your Child</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<h2>Tell Us About Your Child</h2>", unsafe_allow_html=True)

    dob = st.date_input(
        "📅 Date of Birth",
        min_value=date(2009, 1, 1),
        max_value=date.today()
    )

    from utils.location_data import get_all_countries, load_city_data, get_visitor_country, get_cities_by_country

    # 🌍 Country Selection with Search and Auto-Detection
    countries = get_all_countries()
    
    # 🕵️ Detect Visitor Country for auto-selection
    if "detected_country" not in st.session_state:
        # with st.spinner("Detecting your location..."): # Spinner here can be jarring on every rerun
        st.session_state.detected_country = get_visitor_country()

    # Find index of detected country
    default_index = 0
    if st.session_state.detected_country and st.session_state.detected_country in countries:
        default_index = countries.index(st.session_state.detected_country)
    else:
        # Fallback to India if detected fails
        try:
            default_index = countries.index("India")
        except ValueError:
            default_index = 0

    country = st.selectbox(
        "🌍 Birth Country (Search to select)",
        countries,
        index=default_index,
        help="Start typing your country name to search"
    )

    # 📍 City Selection (Seamless Search-or-Type)
    # Cache cities in session state to avoid multiple API calls during same session country choice
    if "cities_cache" not in st.session_state:
        st.session_state.cities_cache = {}
    
    if country not in st.session_state.cities_cache:
        with st.spinner(f"Getting cities for {country}..."):
            st.session_state.cities_cache[country] = sorted(get_cities_by_country(country))
    
    city_list = st.session_state.cities_cache[country]
    
    # Unified "One Box" logic
    if "city_mode" not in st.session_state:
        st.session_state.city_mode = "select"

    if st.session_state.city_mode == "select":
        city_choice = st.selectbox(
            "📍 Birth City",
            ["Search your city / write your city "] + city_list + ["✍️ My city is not listed (Type manually)"],
            help="Common cities are listed here. Start typing to search!"
        )
        
        if city_choice == "✍️ My city is not listed (Type manually)":
            st.session_state.city_mode = "text"
            st.rerun()
        elif city_choice == "Search your city / write your city name":
            city = None
        else:
            city = city_choice
    else:
        # Manual Mode
        city = st.text_input(
            "📍 Birth City (Type manually)",
            placeholder="Search your city / write your city name",
            help="Type your city name exactly as it is"
        )
        if st.button("⬅️ Switch to list", key="back_to_select"):
            st.session_state.city_mode = "select"
            st.rerun()

    st.markdown("### ⏰ Birth Time (optional)")

    col1, col2, col3 = st.columns(3)

    with col1:
        hour = st.selectbox("Hour", ["Skip"] + [str(h) for h in range(1, 13)])

    with col2:
        minute = st.selectbox(
            "Minute",
            ["00", "05", "10", "15", "20", "25", "30", "35", "40", "45", "50", "55"]
        )

    with col3:
        period = st.selectbox("AM / PM", ["AM", "PM"])

    if hour == "Skip":
        birth_time = None
    else:
        birth_time = f"{hour}:{minute} {period}"

    st.caption("Birth time helps with deeper insights. Approximate is fine — or skip it.")

    if st.button("See Insights 🧬", key="go_insights"):
        if not city:
            st.error("Wait! We need a city to calculate the insights. Please select or type one! 🙏")
            st.stop()
            
        age_years, age_months = calculate_age(dob)

        # Reset location mode for next time
        st.session_state.pop("city_input_mode", None)

        # 🔥 CLEAR OLD DATA TO ENSURE REFRESH (CRITICAL)
        keys_to_clear = [
            "insights", "parenting_tips", "daily_tasks", 
            "selected_insights", "cities_cache", "transition_job"
        ]
        for k in keys_to_clear:
            st.session_state.pop(k, None)

        st.session_state.child_data = {
            "dob": dob,
            "age_years": age_years,
            "age_months": age_months,
            "country": country,
            "city": city,
            "birth_time": birth_time,
        }

        # Simple transition to results page
        st.session_state.transition_job = {
            "title": "Identifying Unique Personality Traits",
            "emoji": "🧠",
            "run": lambda: time.sleep(1), # Small delay for "feel"
            "next": "insights",
        }

        go_to("transition")
