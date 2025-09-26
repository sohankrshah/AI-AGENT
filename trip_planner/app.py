import os
import time
import re
import sys
import streamlit as st
from dotenv import load_dotenv
__import__('pysqlite3')
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
sys.path.append('src')
from src.trip_agent import TripAgent, TripTasks, TripCrew

load_dotenv()

st.set_page_config(
    page_title="AI Travel Planner", 
    page_icon="🌍", 
    layout="wide",
    initial_sidebar_state="expanded"
)



def clean_html_content(content):
    if not content:
        return "No content available"
    content = re.sub(r'<[^>]+>', '', content)
    content = re.sub(r'\*\*([^*]+)\*\*', r'**\1**', content)
    content = re.sub(r'\*([^*]+)\*', r'*\1*', content)
    content = content.replace('```html', '').replace('```', '')
    return content.strip()

st.markdown('<h1 class="main-header">🌍 AI Travel Planner</h1>', unsafe_allow_html=True)

with st.sidebar:
    st.markdown('<div class="sidebar-title">Your Journey Begins Here! 🌟</div>', unsafe_allow_html=True)
    st.markdown("---")
    
    budget_styles = [
        "💎 Luxury & Comfort",
        "🎒 Budget & Backpacking",
        "👨‍👩‍👧‍👦 Family & Kid-Friendly",
        "💼 Business & Work",
        "🎲 Mystery Travel"
    ]
    travel_type = st.selectbox("💰 Travel Budget Style", budget_styles)
    
    st.markdown("### 🚗 Transportation")
    transport_preferences = st.multiselect(
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
    
    st.markdown("### 👥 Group Details")
    group_size = st.number_input("Number of Travelers", min_value=1, max_value=10, value=2)
    group_type = st.selectbox(
        "Group Type",
        ["💫 Couple", "👤 Solo", "👨‍👩‍👧‍👦 Family", "👥 Friends", "💼 Business group"]
    )
    
    st.markdown("### 📍 Your Location")
    origin = st.text_input("🏠 Origin City/Country", placeholder="e.g., New York, USA")
    origin_zip = st.text_input("📮 ZIP Code", placeholder="e.g., 10001")
    
    st.markdown("### 🌎 Destination")
    destination_options = [
        "🇳🇵 Nepal", "🇮🇳 India", "🇨🇭 Switzerland", "🇩🇪 Germany",
        "🇫🇷 France", "🇮🇹 Italy", "🇦🇪 Dubai", "🇹🇭 Thailand",
        "🇯🇵 Japan", "🇦🇺 Australia", "🇺🇸 USA", "🇨🇦 Canada",
        "🇧🇷 Brazil", "🇿🇦 South Africa", "🇳🇿 New Zealand", "🇮🇸 Iceland",
        "🇬🇷 Greece", "🇪🇸 Spain", "🇬🇧 United Kingdom", "🇰🇷 South Korea",
        "🇻🇳 Vietnam", "🇲🇾 Malaysia", "🇸🇬 Singapore", "🇪🇬 Egypt"
    ]
    destination = st.selectbox("🌍 Choose Destination", destination_options)
    
    st.markdown("### 🎯 What You Want to Experience")
    experience_categories = [
        "🏛️ Art, Culture & History",
        "🍜 Food & Local Cuisine", 
        "🥾 Adventure & Outdoor Activities",
        "🏖️ Beaches & Water Sports",
        "🦁 Wildlife & Nature",
        "🌃 Nightlife & Entertainment",
        "🛍️ Shopping & Local Markets",
        "🎵 Music, Festivals & Events",
        "💆 Wellness & Relaxation",
        "📸 Photography & Scenic Views",
        "🤝 Local Culture & People",
        "🎨 Creative Workshops & Classes",
        "📚 Learning & Educational Tours",
        "Others"
    ]
    selected_interests = st.multiselect("What experiences do you want?", experience_categories)
    
    if "Others" in selected_interests:
        other_interest = st.text_input("Specify other experiences")
        if other_interest:
            selected_interests = [i for i in selected_interests if i != "Others"]
            selected_interests.append(other_interest)
    
    st.markdown("### 📅 Trip Details")
    season = st.selectbox("🌤️ Season", ["🌸 Spring", "☀️ Summer", "🍂 Autumn", "❄️ Winter"])
    duration = st.slider("📅 Duration (days)", min_value=1, max_value=30, value=7, step=1)
    budget = st.slider("💰 Budget (USD)", min_value=200, max_value=15000, value=2000, step=100)
    
    generate_plan = st.button("🚀 Generate Travel Plan", type="primary", use_container_width=True)

def validate_inputs():
    errors = []
    if not origin:
        errors.append("Please enter your origin location")
    if not destination:
        errors.append("Please select a destination")
    if not selected_interests:
        errors.append("Please select at least one experience")
    if duration < 1:
        errors.append("Trip duration must be at least 1 day")
    return errors

def clean_emoji_text(text):
    if " " in text:
        return text.split(" ", 1)[1]
    return text

if generate_plan:
    errors = validate_inputs()
    
    if errors:
        st.error("⚠️ Please fix the following issues:")
        for error in errors:
            st.write(f"• {error}")
    else:
        inputs = {
            "travel_type": clean_emoji_text(travel_type),
            "origin": origin,
            "origin_zip": origin_zip,
            "destination": clean_emoji_text(destination),
            "interests": [clean_emoji_text(interest) for interest in selected_interests],
            "season": clean_emoji_text(season),
            "duration": duration,
            "budget": f"${budget}",
            "group_size": group_size,
            "group_type": clean_emoji_text(group_type),
            "transport_preferences": [clean_emoji_text(pref) for pref in transport_preferences]
        }
        
        progress_placeholder = st.empty()
        status_placeholder = st.empty()
        
        try:
            with st.spinner("🧠 AI agents are planning your perfect trip..."):
                progress_steps = [
                    ("🔍 Analyzing preferences...", 12),
                    ("🌍 Researching destinations...", 25),
                    ("📊 Gathering local insights...", 38),
                    ("🗓️ Creating itinerary...", 52),
                    ("🏨 Finding accommodations...", 65),
                    ("🚗 Planning transportation...", 78),
                    ("💰 Calculating budget...", 88),
                    ("✨ Finalizing recommendations...", 100)
                ]
                
                for step_text, progress_value in progress_steps:
                    with status_placeholder.container():
                        st.markdown(f'<div class="progress-container">{step_text}</div>', unsafe_allow_html=True)
                    progress_placeholder.progress(progress_value / 100)
                    time.sleep(0.7)
                
                crew = TripCrew(inputs)
                result = crew.run_crew()
                
                progress_placeholder.empty()
                status_placeholder.empty()
                
                if result and hasattr(result, 'tasks_output') and len(result.tasks_output) > 0:
                    st.markdown('<div class="success-banner">✅ Your personalized travel plan is ready!</div>', unsafe_allow_html=True)
                    
                    st.markdown('<h2 class="travel-plan-header">🧳 Your Personalized Travel Plan</h2>', unsafe_allow_html=True)
                    
                    tabs = st.tabs([
                        "🌆 Destinations", 
                        "🔍 City Research",  
                        "🗓️ Itinerary",
                        "💸 Budget",
                        "🏨 Accommodation",
                        "🚗 Transportation",
                        "💱 Currency & Visa",
                        "🛡️ Safety Guide",
                        "🎒 Packing List"
                    ])
                    
                    task_outputs = result.tasks_output
                    
                    with tabs[0]:
                        st.markdown("### 🌆 Recommended Destinations")
                        st.markdown('<div class="trip-card">', unsafe_allow_html=True)
                        if len(task_outputs) > 0:
                            content = clean_html_content(task_outputs[0].raw)
                            st.markdown(content)
                        else:
                            st.info("Destination recommendations will appear here.")
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    with tabs[1]:
                        st.markdown("### 🔍 Detailed City Research")
                        st.markdown('<div class="trip-card">', unsafe_allow_html=True)
                        if len(task_outputs) > 1:
                            content = clean_html_content(task_outputs[1].raw)
                            st.markdown(content)
                        else:
                            st.info("City research information will appear here.")
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    with tabs[2]:
                        st.markdown("### 🗓️ Day-by-Day Itinerary")
                        st.markdown('<div class="trip-card">', unsafe_allow_html=True)
                        itinerary_found = False
                        for i, output in enumerate(task_outputs):
                            if hasattr(output, 'name') and 'itinerary' in output.name.lower():
                                content = clean_html_content(output.raw)
                                st.markdown(content)
                                itinerary_found = True
                                break
                        if not itinerary_found and len(task_outputs) > 2:
                            content = clean_html_content(task_outputs[2].raw)
                            st.markdown(content)
                        elif not itinerary_found:
                            st.info("Detailed itinerary will appear here.")
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    with tabs[3]:
                        st.markdown("### 💸 Budget Breakdown")
                        st.markdown('<div class="trip-card">', unsafe_allow_html=True)
                        budget_found = False
                        for i, output in enumerate(task_outputs):
                            if hasattr(output, 'name') and 'budget' in output.name.lower():
                                content = clean_html_content(output.raw)
                                st.markdown(content)
                                budget_found = True
                                break
                        if not budget_found and len(task_outputs) > 3:
                            content = clean_html_content(task_outputs[3].raw)
                            st.markdown(content)
                        elif not budget_found:
                            st.info("Budget analysis will appear here.")
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    with tabs[4]:
                        st.markdown("### 🏨 Accommodation Options")
                        st.markdown('<div class="trip-card">', unsafe_allow_html=True)
                        accommodation_found = False
                        for i, output in enumerate(task_outputs):
                            if hasattr(output, 'name') and 'accommodation' in output.name.lower():
                                content = clean_html_content(output.raw)
                                st.markdown(content)
                                accommodation_found = True
                                break
                        if not accommodation_found and len(task_outputs) > 4:
                            content = clean_html_content(task_outputs[4].raw)
                            st.markdown(content)
                        elif not accommodation_found:
                            st.info("Accommodation recommendations will appear here.")
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    with tabs[5]:
                        st.markdown("### 🚗 Transportation Guide")
                        st.markdown('<div class="trip-card">', unsafe_allow_html=True)
                        transport_found = False
                        for i, output in enumerate(task_outputs):
                            if hasattr(output, 'name') and 'transport' in output.name.lower():
                                content = clean_html_content(output.raw)
                                st.markdown(content)
                                transport_found = True
                                break
                        if not transport_found and len(task_outputs) > 5:
                            content = clean_html_content(task_outputs[5].raw)
                            st.markdown(content)
                        elif not transport_found:
                            st.info("Transportation options will appear here.")
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    with tabs[6]:
                        st.markdown("### 💱 Currency & Visa Information")
                        st.markdown('<div class="trip-card">', unsafe_allow_html=True)
                        found_info = False
                        for i, output in enumerate(task_outputs):
                            if hasattr(output, 'name') and ('currency' in output.name.lower() or 'visa' in output.name.lower()):
                                content = clean_html_content(output.raw)
                                st.markdown(content)
                                found_info = True
                                break
                        if not found_info and len(task_outputs) > 6:
                            content = clean_html_content(task_outputs[6].raw)
                            st.markdown(content)
                        elif not found_info:
                            st.info("Currency and visa information will appear here.")
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    with tabs[7]:
                        st.markdown("### 🛡️ Safety & Emergency Information")
                        st.markdown('<div class="trip-card">', unsafe_allow_html=True)
                        safety_found = False
                        for i, output in enumerate(task_outputs):
                            if hasattr(output, 'name') and ('safety' in output.name.lower() or 'emergency' in output.name.lower()):
                                content = clean_html_content(output.raw)
                                st.markdown(content)
                                safety_found = True
                                break
                        if not safety_found and len(task_outputs) > 7:
                            content = clean_html_content(task_outputs[7].raw)
                            st.markdown(content)
                        elif not safety_found:
                            st.info("Safety and emergency information will appear here.")
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    with tabs[8]:
                        st.markdown("### 🎒 Packing List")
                        st.markdown('<div class="trip-card">', unsafe_allow_html=True)
                        packing_found = False
                        for i, output in enumerate(task_outputs):
                            if hasattr(output, 'name') and 'packing' in output.name.lower():
                                content = clean_html_content(output.raw)
                                st.markdown(content)
                                packing_found = True
                                break
                        if not packing_found and len(task_outputs) > 8:
                            content = clean_html_content(task_outputs[8].raw)
                            st.markdown(content)
                        elif not packing_found:
                            st.info("Packing list will appear here.")
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    st.markdown("---")
                    st.markdown("### 📤 Export Your Plan")
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        if st.button("📄 Download PDF", key="pdf", use_container_width=True):
                            st.info("PDF download feature coming soon!")
                    
                    with col2:
                        if st.button("📧 Email Plan", key="email", use_container_width=True):
                            st.info("Email feature coming soon!")
                    
                    with col3:
                        if st.button("📱 Share Link", key="share", use_container_width=True):
                            st.info("Share feature coming soon!")
                
                else:
                    st.error("❌ Sorry, we couldn't generate your travel plan. Please try again.")
                    st.info("💡 This might be due to API limitations or network issues.")
                    
        except Exception as e:
            progress_placeholder.empty()
            status_placeholder.empty()
            st.error(f"❌ Something went wrong: {str(e)}")
            st.info("💡 Try refreshing the page or check your API configuration.")

if not generate_plan:
    st.markdown("---")
    st.markdown('<div class="info-section">', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
