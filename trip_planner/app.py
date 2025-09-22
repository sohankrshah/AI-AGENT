import os
import streamlit as st
import sys
__import__('pysqlite3')
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
from src.trip_agent import TripAgent, TripTasks, TripCrew
import time

st.set_page_config(
    page_title="AI Travel Planner", 
    page_icon="🌍", 
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown('<h1 class="main-header">🌍 AI Travel Planner</h1>', unsafe_allow_html=True)
st.sidebar.markdown("# 🧭 Plan Your Dream Trip")
st.sidebar.markdown("---")

travel_types = [
    "🏔️ Adventure & Outdoor",
    "🏛️ Cultural & Heritage", 
    "💎 Luxury & Comfort",
    "🎒 Budget & Backpacking",
    "👨‍👩‍👧‍👦 Family & Kid-Friendly",
    "💼 Business & Work",
    "🧘 Wellness & Relaxation",
    "🍽️ Culinary & Foodie",
    "🎉 Festival & Events",
    "📚 Educational & Learning"
]
travel_type = st.sidebar.selectbox("✈️ Travel Style", travel_types)

st.sidebar.markdown("### 🚗 Transportation Preferences")
transport_preferences = st.sidebar.multiselect(
    "How do you prefer to travel?",
    [
        "✈️ Flight + Local transport",
        "🚗 Road trip (Car/Motorcycle)", 
        "🚂 Train travel",
        "🚌 Bus/Coach travel",
        "🚴 Cycling/Bike touring",
        "🚶 Walking & Hiking focused",
        "🚢 Ferry/Boat travel",
        "🚇 Public transport focused"
    ],
    default=["✈️ Flight + Local transport"]
)
st.sidebar.markdown("### 👥 Group Details")
group_size = st.sidebar.number_input("Number of Travelers", min_value=1, max_value=10, value=2)
group_type = st.sidebar.selectbox(
    "Group Type",
    ["👫 Couple", "👤 Solo", "👨‍👩‍👧‍👦 Family", "👥 Friends", "💼 Business group"]
)

st.sidebar.markdown("### 📍 Your Location")
origin = st.sidebar.text_input("🏠 Your Origin (City/Country)", placeholder="e.g., New York, USA")
origin_zip = st.sidebar.text_input("📮 ZIP/Postal Code", placeholder="e.g., 10001")

st.sidebar.markdown("### 🌎 Where To?")
destination_options = [
    "🇳🇵 Nepal", "🇮🇳 India", "🇨🇭 Switzerland", "🇩🇪 Germany",
    "🇫🇷 France", "🇮🇹 Italy", "🇦🇪 Dubai", "🇹🇭 Thailand",
    "🇯🇵 Japan", "🇦🇺 Australia", "🇺🇸 USA", "🇨🇦 Canada",
    "🇧🇷 Brazil", "🇿🇦 South Africa", "🇳🇿 New Zealand", "🇮🇸 Iceland",
    "🇬🇷 Greece", "🇪🇸 Spain", "🇬🇧 United Kingdom", "🇰🇷 South Korea",
    "🇻🇳 Vietnam", "🇲🇾 Malaysia", "🇸🇬 Singapore", "🇪🇬 Egypt"
]
destination = st.sidebar.selectbox("🌍 Destination", destination_options)

st.sidebar.markdown("### 🎯 Your Interests")
interest_options = [
    "🏛️ Museums & Art Galleries",
    "🍜 Food & Culinary Experiences", 
    "🥾 Hiking / Trekking / Outdoor Adventure",
    "🏖️ Beaches & Water Sports",
    "🦁 Wildlife / Safari",
    "🌃 Nightlife / Clubs / Bars",
    "🏰 Historical Sites & Architecture",
    "🛍️ Shopping / Markets",
    "🎵 Music / Concerts / Festivals",
    "⚡ Sports / Adventure Activities",
    "💆 Relaxation / Wellness",
    "📸 Photography / Scenic Locations",
    "🤝 Cultural Immersion / Local Experiences",
    "🎨 Arts & Crafts Workshops",
    "📚 Educational Tours / Learning",
    "Others"
]
selected_interests = st.sidebar.multiselect("Select your interests", interest_options)

if "Others" in selected_interests:
    other_interest = st.sidebar.text_input("Please specify other interests")
    if other_interest:
        selected_interests = [i for i in selected_interests if i != "Others"]
        selected_interests.append(other_interest)

st.sidebar.markdown("### 📅 Trip Details")
season = st.sidebar.selectbox("🌤️ Preferred Season", ["🌸 Spring", "☀️ Summer", "🍂 Autumn", "❄️ Winter"])
duration = st.sidebar.slider("📅 Trip Duration (days)", min_value=1, max_value=30, value=7, step=1)
budget = st.sidebar.slider("💰 Budget (USD)", min_value=200, max_value=15000, value=2000, step=100)

generate_plan = st.sidebar.button("🚀 Generate Travel Plan", type="primary")

def validate_inputs():
    errors = []
    if not origin:
        errors.append("Please enter your origin location")
    if not destination:
        errors.append("Please select a destination")
    if not selected_interests:
        errors.append("Please select at least one interest")
    if duration < 1:
        errors.append("Trip duration must be at least 1 day")
    return errors

if generate_plan:
    errors = validate_inputs()
    
    if errors:
        st.error("⚠️ Please fix the following issues:")
        for error in errors:
            st.write(f"• {error}")
    else:
        inputs = {
            "travel_type": travel_type.split(" ", 1)[1] if " " in travel_type else travel_type,
            "origin": origin,
            "origin_zip": origin_zip,
            "destination": destination.split(" ", 1)[1] if " " in destination else destination,
            "interests": [interest.split(" ", 1)[1] if " " in interest else interest for interest in selected_interests],
            "season": season.split(" ", 1)[1] if " " in season else season,
            "duration": duration,
            "budget": f"${budget}"
        }
        
        progress_placeholder = st.empty()
        status_placeholder = st.empty()
        
        try:
            with st.spinner("🧠 AI agents are planning your perfect trip..."):
                progress_steps = [
                    ("🔍 Analyzing your preferences...", 10),
                    ("🌍 Researching destinations...", 25),
                    ("🏨 Finding accommodations...", 40),
                    ("🗓️ Creating itinerary...", 60),
                    ("💰 Calculating budget...", 80),
                    ("📋 Finalizing recommendations...", 100)
                ]
                
                for step_text, progress_value in progress_steps:
                    status_placeholder.info(step_text)
                    progress_placeholder.progress(progress_value / 100)
                    time.sleep(1)
                
                crew = TripCrew(inputs)
                result = crew.run_crew()
                
                progress_placeholder.empty()
                status_placeholder.empty()
                
                if result:
                    st.success("✅ Your personalized travel plan is ready!")
                    
                    st.markdown("## 🧳 Your Personalized Travel Plan")
                    
                    tabs = st.tabs([
                        "🌆 Destinations", 
                        "🔍 City Insights",  
                        "💸 Budget",
                        "🏨 Accommodation",
                        "🚗 Transportation",
                        "🌆 Overview", 
                        "💱 Budget & Currency",
                        "📋 Documents & Visa",
                        "✈️ Transportation", 
                        "🗓️ Detailed Itinerary",
                        "🛡️ Safety & Emergency",
                        "🎒 Packing List"
                    ])
                    
                    with tabs[0]:
                        st.markdown("### 🌆 Recommended Destinations")
                        st.markdown('<div class="trip-card">', unsafe_allow_html=True)
                        if hasattr(result, 'tasks_output') and len(result.tasks_output) > 0:
                            st.write(result.tasks_output[0].raw)
                        else:
                            st.write("Destination recommendations will appear here.")
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    with tabs[1]:
                        st.markdown("### 🔍 Detailed City Research")
                        st.markdown('<div class="trip-card">', unsafe_allow_html=True)
                        if hasattr(result, 'tasks_output') and len(result.tasks_output) > 1:
                            st.write(result.tasks_output[1].raw)
                        else:
                            st.write("City research information will appear here.")
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    with tabs[2]:
                        st.markdown("### 🗓️ Day-by-Day Itinerary")
                        st.markdown('<div class="trip-card">', unsafe_allow_html=True)
                        if hasattr(result, 'tasks_output') and len(result.tasks_output) > 2:
                            st.write(result.tasks_output[2].raw)
                        else:
                            st.write("Detailed itinerary will appear here.")
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    with tabs[3]:
                        st.markdown("### 💸 Budget Breakdown")
                        st.markdown('<div class="trip-card">', unsafe_allow_html=True)
                        if hasattr(result, 'tasks_output') and len(result.tasks_output) > 3:
                            st.write(result.tasks_output[3].raw)
                        else:
                            st.write("Budget analysis will appear here.")
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    with tabs[4]:
                        st.markdown("### 🏨 Accommodation Options")
                        st.markdown('<div class="trip-card">', unsafe_allow_html=True)
                        if hasattr(result, 'tasks_output') and len(result.tasks_output) > 4:
                            st.write(result.tasks_output[4].raw)
                        else:
                            st.write("Accommodation recommendations will appear here.")
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    with tabs[5]:
                        st.markdown("### 🚗 Transportation Guide")
                        st.markdown('<div class="trip-card">', unsafe_allow_html=True)
                        if hasattr(result, 'tasks_output') and len(result.tasks_output) > 5:
                            st.write(result.tasks_output[5].raw)
                        else:
                            st.write("Transportation options will appear here.")
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    st.markdown("---")
                    st.markdown("### 📤 Export Your Plan")
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        if st.button("📄 Download as PDF"):
                            st.info("PDF download feature coming soon!")
                    
                    with col2:
                        if st.button("📧 Email to Me"):
                            st.info("Email feature coming soon!")
                    
                    with col3:
                        if st.button("📱 Share Plan"):
                            st.info("Share feature coming soon!")
                
                else:
                    st.error("❌ Sorry, we couldn't generate your travel plan. Please try again.")
                    
        except Exception as e:
            progress_placeholder.empty()
            status_placeholder.empty()
            st.error(f"❌ Something went wrong: {str(e)}")

            st.info("💡 Try refreshing the page or check your internet connection.")

