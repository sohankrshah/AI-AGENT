from crewai import Task
from api_services import APIIntegrationService

class TripTasks:
    def __init__(self):
        try:
            self.api_service = APIIntegrationService()
        except ValueError:
            self.api_service = None

    def country_selector_task(self, agent, inputs):
        return Task(
            name="destination_selection",
            description=(
                f"Analyze user preferences and select best destinations:\n"
                f"Travel Type: {inputs['travel_type']}\n"
                f"Interests: {inputs.get('interests', [])}\n"
                f"Season: {inputs['season']}\n"
                f"Destination: {inputs['destination']}\n"
                f"Duration: {inputs['duration']} days\n"
                f"Budget: {inputs['budget']}\n"
                f"Group: {inputs.get('group_type', 'Not specified')}\n"
                "Consider cultural attractions, adventure opportunities, gastronomy, entertainment, and seasonal factors.\n"
                "Output: Provide 3-5 city/location recommendations with detailed rationale."
            ),
            agent=agent,
            expected_output="Detailed list of 3-5 destinations with explanations of why each fits user preferences, seasonal considerations, and highlight activities matching their interests."
        )

    def mystery_mode_task(self, agent, inputs):
        return Task(
            name="serendipity_destination",
            description=(
                f"Generate random destination selection from world's top destinations:\n"
                f"- Select from 20 most incredible global destinations\n"
                f"- Provide compelling reasons why random choice is perfect\n"
                f"- Consider user's travel type: {inputs['travel_type']}\n"
                f"- Budget range: {inputs['budget']}\n"
                f"- Duration: {inputs['duration']} days\n"
                f"Make the random selection feel like destiny with persuasive rationale."
            ),
            agent=agent,
            expected_output="Single surprise destination with passionate explanation of why this random choice is the perfect adventure for the traveler."
        )

    def city_research_task(self, agent, inputs):
        return Task(
            name="destination_research",
            description=(
                f"Provide comprehensive insights about {inputs['destination']}:\n"
                f"Focus areas based on interests: {inputs.get('interests', [])}\n"
                f"Season considerations: {inputs['season']}\n"
                "Cover:\n"
                "- Top 15-20 attractions with timing recommendations\n"
                "- Local cuisine and must-try dishes with restaurant suggestions\n"
                "- Cultural norms, etiquette, and local customs\n"
                "- Best neighborhoods for different budgets\n"
                "- Transportation systems and navigation tips\n"
                "- Safety considerations and common scams\n"
                "- Hidden gems and authentic local experiences\n"
                "- Shopping districts and local markets\n"
                "- Seasonal events and festivals\n"
                "- Photography spots and scenic locations\n"
                "- Local language basics and useful phrases"
            ),
            agent=agent,
            expected_output="Comprehensive destination guide with organized sections, insider tips, and practical information for authentic local experiences."
        )

    def itinerary_creation_task(self, agent, inputs):
        return Task(
            name="detailed_itinerary",
            description=(
                f"Create optimized {inputs['duration']}-day itinerary for {inputs['destination']}:\n"
                f"Interests focus: {inputs.get('interests', [])}\n"
                f"Season: {inputs['season']}\n"
                f"Budget level: {inputs['travel_type']}\n"
                f"Group type: {inputs.get('group_type', 'general')}\n"
                "Include:\n"
                "- Hour-by-hour daily schedules with buffer time\n"
                "- Logical activity sequencing by location and opening hours\n"
                "- Transportation between locations with travel times\n"
                "- Meal planning with restaurant recommendations and costs\n"
                "- Rest periods and flexibility for spontaneous exploration\n"
                "- Weather-dependent backup activities\n"
                "- Photo opportunities and scenic viewpoints\n"
                "- Cultural immersion opportunities\n"
                "- Shopping time and local market visits\n"
                "- Evening entertainment options"
            ),
            agent=agent,
            expected_output="Day-by-day detailed itinerary with time slots, specific locations, estimated costs, and practical logistics for seamless travel experience."
        )

    def budget_planning_task(self, agent, inputs, context_tasks=None):
        return Task(
            name="comprehensive_budget",
            description=(
                f"Create detailed budget breakdown for {inputs['destination']} trip:\n"
                f"Total budget: {inputs['budget']}\n"
                f"Duration: {inputs['duration']} days\n"
                f"Travel style: {inputs['travel_type']}\n"
                f"Origin: {inputs.get('origin', 'Not specified')}\n"
                "Budget categories:\n"
                "- International flights (round trip)\n"
                "- Accommodation (per night breakdown)\n"
                "- Local transportation (daily estimates)\n"
                "- Activities and attraction fees\n"
                "- Food and dining (breakfast, lunch, dinner)\n"
                "- Shopping and souvenirs budget\n"
                "- Travel insurance and visas\n"
                "- Emergency fund (15% of total)\n"
                "- Tips and miscellaneous expenses\n"
                "Provide cost-saving strategies and budget optimization tips."
            ),
            agent=agent,
            context=context_tasks if context_tasks else [],
            expected_output="Itemized budget with daily costs, category totals, cost-saving recommendations, and contingency planning."
        )

    def accommodation_task(self, agent, inputs):
        return Task(
            name="accommodation_recommendations",
            description=(
                f"Find optimal accommodation for {inputs['destination']}:\n"
                f"Budget: {inputs['budget']}\n"
                f"Duration: {inputs['duration']} nights\n"
                f"Travel style: {inputs['travel_type']}\n"
                f"Group size: {inputs.get('group_size', 2)}\n"
                f"Group type: {inputs.get('group_type', 'couple')}\n"
                "Provide 4-6 options across different categories:\n"
                "- Luxury hotels with premium amenities\n"
                "- Mid-range hotels with good value\n"
                "- Budget-friendly options (hostels, guesthouses)\n"
                "- Unique stays (boutique, heritage properties)\n"
                "- Alternative accommodations (Airbnb, apartments)\n"
                "For each option include: location benefits, amenities, estimated costs, booking tips, and pros/cons."
            ),
            agent=agent,
            expected_output="Detailed accommodation guide with diverse options, location analysis, amenity comparisons, and booking strategies for different budgets."
        )

    def transportation_task(self, agent, inputs):
        return Task(
            name="transportation_planning",
            description=(
                f"Plan complete transportation for {inputs['destination']} trip:\n"
                f"Origin: {inputs.get('origin', 'Not specified')}\n"
                f"Duration: {inputs['duration']} days\n"
                f"Budget: {inputs['budget']}\n"
                f"Transport preferences: {inputs.get('transport_preferences', [])}\n"
                "Cover all transportation needs:\n"
                "- International flight options and booking strategies\n"
                "- Airport transfers and costs\n"
                "- Local public transport systems and passes\n"
                "- Taxi and ride-sharing options\n"
                "- Car rental possibilities and driving tips\n"
                "- Walking and cycling options\n"
                "- Inter-city transportation if needed\n"
                "- Transportation apps and digital passes\n"
                "- Cost comparisons and time efficiency analysis"
            ),
            agent=agent,
            expected_output="Comprehensive transportation guide with cost comparisons, efficiency analysis, and practical booking recommendations."
        )

    def currency_conversion_task(self, agent, inputs):
        return Task(
            name="currency_management",
            description=(
                f"Provide currency conversion and money management for {inputs['destination']}:\n"
                f"Budget: {inputs['budget']} USD\n"
                f"Origin: {inputs.get('origin', 'USA')}\n"
                "Include:\n"
                "- Real-time exchange rate conversion\n"
                "- Historical rate trends and forecasts\n"
                "- Best currency exchange methods and locations\n"
                "- ATM strategies and fee avoidance\n"
                "- Credit card recommendations for international use\n"
                "- Mobile payment options and digital wallets\n"
                "- Tipping customs and cash requirements\n"
                "- Money safety and security tips\n"
                "- Budget allocation in local currency"
            ),
            agent=agent,
            expected_output="Complete currency guide with converted amounts, exchange strategies, payment method recommendations, and financial safety tips."
        )

    def visa_documentation_task(self, agent, inputs):
        return Task(
            name="visa_requirements",
            description=(
                f"Research visa and documentation for travel to {inputs['destination']}:\n"
                f"Traveler origin: {inputs.get('origin', 'USA')}\n"
                f"Trip duration: {inputs['duration']} days\n"
                f"Travel purpose: Tourism\n"
                "Provide comprehensive information:\n"
                "- Current visa requirements and exemptions\n"
                "- Required documents checklist\n"
                "- Application process step-by-step\n"
                "- Processing times and fees\n"
                "- Embassy/consulate locations and contact information\n"
                "- Vaccination requirements\n"
                "- Travel insurance requirements\n"
                "- Passport validity requirements\n"
                "- Entry/exit requirements and restrictions\n"
                "- Tips for successful application"
            ),
            agent=agent,
            expected_output="Complete visa and documentation guide with requirements, application process, embassy information, and success tips."
        )

    def flight_finder_task(self, agent, inputs):
        return Task(
            name="flight_optimization",
            description=(
                f"Find optimal flights from {inputs.get('origin', 'origin')} to {inputs['destination']}:\n"
                f"Budget consideration: {inputs['budget']}\n"
                f"Duration: {inputs['duration']} days\n"
                f"Season: {inputs['season']}\n"
                f"Passengers: {inputs.get('group_size', 2)}\n"
                "Research and compare:\n"
                "- Direct vs connecting flights\n"
                "- Multiple airline options and pricing\n"
                "- Flexible date savings opportunities\n"
                "- Different booking platforms\n"
                "- Seat selection and upgrade options\n"
                "- Baggage policies and fees\n"
                "- Travel insurance options\n"
                "- Optimal booking timing\n"
                "- Alternative airports if applicable\n"
                "- Loyalty program benefits"
            ),
            agent=agent,
            expected_output="Detailed flight recommendations with price comparisons, booking strategies, and travel optimization tips."
        )

    def hotel_finder_task(self, agent, inputs):
        return Task(
            name="hotel_optimization",
            description=(
                f"Find best hotels in {inputs['destination']}:\n"
                f"Budget range: {inputs['budget']}\n"
                f"Duration: {inputs['duration']} nights\n"
                f"Group: {inputs.get('group_size', 2)} guests\n"
                f"Travel style: {inputs['travel_type']}\n"
                "Research and analyze:\n"
                "- Hotels across different price tiers\n"
                "- Location advantages and neighborhood analysis\n"
                "- Amenities and facilities comparison\n"
                "- Guest reviews and ratings analysis\n"
                "- Booking platform comparisons\n"
                "- Seasonal pricing variations\n"
                "- Cancellation policies and flexibility\n"
                "- Special offers and package deals\n"
                "- Alternative accommodation types\n"
                "- Proximity to attractions and transport"
            ),
            agent=agent,
            expected_output="Comprehensive hotel guide with detailed comparisons, location analysis, and booking optimization strategies."
        )

    def local_transport_optimization_task(self, agent, inputs):
        return Task(
            name="local_transport_mastery",
            description=(
                f"Optimize local transportation in {inputs['destination']}:\n"
                f"Duration: {inputs['duration']} days\n"
                f"Budget considerations: {inputs['budget']}\n"
                f"Interests: {inputs.get('interests', [])}\n"
                "Create comprehensive local transport strategy:\n"
                "- Efficient routes between major attractions\n"
                "- Public transport system deep-dive\n"
                "- Transportation apps and digital solutions\n"
                "- Real-time navigation and updates\n"
                "- Cost-effective travel passes and cards\n"
                "- Peak hour traffic patterns\n"
                "- Alternative transport modes (bikes, scooters)\n"
                "- Accessibility options\n"
                "- Local transport etiquette\n"
                "- Emergency transport options"
            ),
            agent=agent,
            expected_output="Master guide for local transportation with optimal routes, cost analysis, and real-time navigation strategies."
        )

    def emergency_safety_task(self, agent, inputs):
        return Task(
            name="safety_security_planning",
            description=(
                f"Comprehensive safety planning for {inputs['destination']}:\n"
                f"Trip duration: {inputs['duration']} days\n"
                f"Group type: {inputs.get('group_type', 'general')}\n"
                f"Season: {inputs['season']}\n"
                "Cover all safety aspects:\n"
                "- Emergency contact numbers (local and international)\n"
                "- Medical facilities and hospitals locations\n"
                "- Embassy/consulate information\n"
                "- Common scams and how to avoid them\n"
                "- Safe vs unsafe areas and neighborhoods\n"
                "- Cultural sensitivity and local laws\n"
                "- Natural disaster preparedness\n"
                "- Personal safety protocols\n"
                "- Travel insurance recommendations\n"
                "- Emergency communication methods\n"
                "- Legal considerations and restrictions\n"
                "- Health precautions and vaccinations"
            ),
            agent=agent,
            expected_output="Complete safety and security guide with emergency protocols, risk mitigation, and local safety intelligence."
        )

    def story_narrative_task(self, agent, inputs):
        return Task(
            name="travel_story_creation",
            description=(
                f"Transform the trip plan into an engaging adventure narrative:\n"
                f"Destination: {inputs['destination']}\n"
                f"Duration: {inputs['duration']} days\n"
                f"Travel style: {inputs['travel_type']}\n"
                f"Key interests: {inputs.get('interests', [])}\n"
                f"Season setting: {inputs['season']}\n"
                "Create compelling travel story:\n"
                "- Opening that sets adventure tone\n"
                "- Daily adventures with narrative flow\n"
                "- Cultural discovery moments\n"
                "- Character development through travel\n"
                "- Memorable scenes and experiences\n"
                "- Local interactions and connections\n"
                "- Challenges and how to overcome them\n"
                "- Climactic experiences and revelations\n"
                "- Satisfying conclusion with transformation\n"
                "Make the itinerary feel like an epic journey."
            ),
            agent=agent,
            expected_output="Engaging travel narrative that transforms the practical itinerary into an inspiring adventure story with emotional depth."
        )

    def packing_list_task(self, agent, inputs):
        return Task(
            name="smart_packing_guide",
            description=(
                f"Create comprehensive packing list for {inputs['destination']}:\n"
                f"Season: {inputs['season']}\n"
                f"Duration: {inputs['duration']} days\n"
                f"Activities: {inputs.get('interests', [])}\n"
                f"Travel style: {inputs['travel_type']}\n"
                f"Group type: {inputs.get('group_type', 'general')}\n"
                "Include:\n"
                "- Climate-appropriate clothing\n"
                "- Activity-specific gear\n"
                "- Electronics and adapters\n"
                "- Documents and important papers\n"
                "- Health and medication items\n"
                "- Personal care and toiletries\n"
                "- Safety and security items\n"
                "- Comfort and convenience items\n"
                "- Local shopping opportunities\n"
                "- Packing strategies and tips"
            ),
            agent=agent,
            expected_output="Detailed packing checklist organized by category with climate considerations, activity requirements, and packing optimization tips."
        )

    def weather_analysis_task(self, agent, inputs):
        return Task(
            name="weather_analysis",
            description=(
                f"Analyze weather conditions for {inputs['destination']} during {inputs['season']}:\n"
                f"Trip dates: {inputs['duration']} days\n"
                f"Activities planned: {inputs.get('interests', [])}\n"
                "Provide:\n"
                "- Seasonal weather patterns and temperatures\n"
                "- Rainfall and humidity expectations\n"
                "- Best and worst weather days for activities\n"
                "- Weather-appropriate clothing recommendations\n"
                "- Backup indoor activities for bad weather\n"
                "- Seasonal events affected by weather\n"
                "- Health considerations (UV, altitude, etc.)\n"
                "- Weather apps and local forecasting resources"
            ),
            agent=agent,
            expected_output="Comprehensive weather analysis with seasonal patterns, activity recommendations, and weather preparation strategies."
        )

    def cultural_immersion_task(self, agent, inputs):
        return Task(
            name="cultural_immersion",
            description=(
                f"Design cultural immersion experiences for {inputs['destination']}:\n"
                f"Interests: {inputs.get('interests', [])}\n"
                f"Duration: {inputs['duration']} days\n"
                f"Group type: {inputs.get('group_type', 'general')}\n"
                "Include:\n"
                "- Authentic local experiences and interactions\n"
                "- Traditional ceremonies or festivals during visit\n"
                "- Local family dining or homestay opportunities\n"
                "- Traditional craft workshops and classes\n"
                "- Language learning basics and useful phrases\n"
                "- Religious and spiritual sites with proper etiquette\n"
                "- Local volunteer opportunities\n"
                "- Off-the-beaten-path cultural sites\n"
                "- Traditional music and dance experiences\n"
                "- Cultural dos and don'ts for respectful travel"
            ),
            agent=agent,
            expected_output="Rich cultural immersion guide with authentic experiences, local connections, and respectful cultural engagement strategies."
        )