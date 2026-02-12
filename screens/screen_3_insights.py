import json
import streamlit as st
from utils.navigation import go_to
from utils.insight_selector import select_insights, get_available_pool

def screen_insights():
    # Header
    st.markdown(
        """
        <div class="app-header">
            <span class="title-emoji floating-emoji">✨</span>
            <span class="app-title-text">Know Your Child</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        "<h2 style='text-align:center'>Your Child at a Glance</h2>",
        unsafe_allow_html=True
    )

    # 1. Initialize Session State Pools
    if "selected_insights" not in st.session_state:
        # First time loading: Select suggestions from database
        suggestions = select_insights(st.session_state.child_data)
        st.session_state.selected_insights = suggestions

    # 2. Main Display: Suggested Insights
    st.markdown("🌟 Suggested Insights")
    
    if not st.session_state.selected_insights:
        st.info("No insights selected. Choose some from the dropdown below! 👇")
    
    # Display Cards
    for idx, glance in enumerate(st.session_state.selected_insights):
        col1, col2 = st.columns([0.88, 0.12])
        
        category = glance.get("category", "INSIGHT")
        
        with col1:
             st.markdown(
                f"""
                <div class="insight-card" style="margin-bottom:0.8rem; padding:1.2rem; background:white; border-radius:15px; border-left: 5px solid #7c3aed; box-shadow: 0 4px 12px rgba(0,0,0,0.05)">
                    <div style="font-size:0.75rem; font-weight:700; color:#7c3aed; text-transform:uppercase; letter-spacing:0.05em; margin-bottom:0.3rem">
                        {category}
                    </div>
                    <div style="font-size:1.15rem; font-weight:700; color:#1f2937; margin-bottom:0.5rem">
                        {glance.get("title", "Insight")}
                    </div>
                    <div style="font-size:1rem; color:#4b5563; line-height:1.6">
                        {glance.get("description", "")}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        with col2:
            st.markdown("<div style='height:30px'></div>", unsafe_allow_html=True)
            if st.button("✖", key=f"rm_{glance.get('id')}_{idx}", help="Remove this insight"):
                # Move from selected to pool (automatic since we filter pool by selection)
                st.session_state.selected_insights = [
                    item for item in st.session_state.selected_insights 
                    if item.get("id") != glance.get("id")
                ]
                st.rerun()

    st.markdown("<div style='margin-bottom:2.5rem'></div>", unsafe_allow_html=True)

    # 3. Add Insight Section (Dropdown Pool)
    st.markdown("### ➕ Explore More Traits")
    
    country = st.session_state.child_data.get("country", "India")
    selected_ids = [item.get("id") for item in st.session_state.selected_insights]
    available_pool = get_available_pool(country, selected_ids)
    
    # Categorize pool for better UX
    pool_options = {item.get("title"): item for item in available_pool}
    
    selected_title = st.selectbox(
        "Choose a trait to add:",
        ["Search and select a trait..."] + sorted(list(pool_options.keys()))
    )
    
    if selected_title != "Search and select a trait...":
        if st.button("✨ Add to Results", type="primary"):
            new_item = pool_options[selected_title]
            st.session_state.selected_insights.append(new_item)
            st.rerun()
    
    # 4. Navigation
    st.markdown("<div style='margin-top:2rem'></div>", unsafe_allow_html=True)
    cols = st.columns(2)
    
    with cols[0]:
        if st.button("← Back", key="btn_insights_back"):
            go_to("child_details")

    with cols[1]:
        if st.button("Personalize My Tips →", key="btn_insights_tips", type="primary"):
            if not st.session_state.selected_insights:
                st.error("Please pick at least one insight to proceed! 🙏")
            else:
                from ai.tips_generator import generate_parenting_tips
                
                # Clear old tips to force a fresh, fast load
                st.session_state.pop("parenting_tips", None)
                st.session_state.pop("daily_tasks", None)

                st.session_state.transition_job = {
                    "title": "Crafting Your Parenting Tips",
                    "emoji": "👨‍👩‍👧",
                    "run": lambda: st.session_state.update({
                        "parenting_tips": generate_parenting_tips(
                            st.session_state.child_data,
                            st.session_state.selected_insights
                        )
                    }),
                    "next": "parenting_tips",
                }
                go_to("transition")
