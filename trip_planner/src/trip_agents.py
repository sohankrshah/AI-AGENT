import os
from crewai import Agent
from crewai.llm import LLM
from dotenv import load_dotenv

load_dotenv()

class TripAgents:
    def __init__(self, use_gemini=True):
        self.llm = None
        self.use_gemini = use_gemini
        if self.use_gemini:
            try:
                self.llm = LLM(
                    model="gemini/gemini-2.0-flash-exp",
                    temperature=0.7,
                    api_key=os.getenv("GEMINI_API_KEY")
                )
            except Exception as e:
                print(f"Gemini initialization failed: {e}")
                self.llm = LLM(
                    model="openai/gpt-4",
                    temperature=0.7,
                    api_key=os.getenv("OPENAI_API_KEY")
                )
        else:
            self.llm = LLM(
                model="openai/gpt-4",
                temperature=0.7,
                api_key=os.getenv("OPENAI_API_KEY")
            )

    def country_selector_agent(self):
        return Agent(
            role='Location Search Expert',
            goal='Identify the best cities to visit based on the user\'s preferences and country of interest.',
            backstory="""You are an expert travel geographer with in-depth knowledge of cities worldwide. 
            You provide recommendations tailored to each user, considering culture, history, adventure, gastronomy, 
            trekking, and entertainment options. Your guidance ensures travelers discover the most enriching and memorable experiences 
            in every destination they visit.""",
            llm=self.llm,
            verbose=True
        )

    def travel_planner_agent(self):
        return Agent(
            role='Travel Itinerary Specialist',
            goal='Create detailed day-by-day travel itineraries that maximize experiences within time constraints.',
            backstory="""You are a professional travel planner with expertise in creating efficient and enjoyable itineraries. 
            You understand optimal timing, transportation logistics, and how to balance activities to create memorable travel experiences. 
            You consider factors like travel fatigue, opening hours, seasonal variations, and local events.""",
            llm=self.llm,
            verbose=True
        )

    def local_expert_agent(self):
        return Agent(
            role='Local Destination Expert',
            goal='Provide detailed insights about selected cities including top attractions, local customs, and hidden gems.',
            backstory="""A knowledgeable local guide with first-hand experience of the city's culture and attractions. 
            You know the best times to visit places, local etiquette, safety tips, and can recommend authentic experiences 
            that tourists often miss.""",
            llm=self.llm,
            verbose=True
        )

    def budget_manager_agent(self):
        return Agent(
            role='Travel Budget Specialist',
            goal='Optimize travel plans to stay within budget while maximizing experience quality.',
            backstory="""A financial planner specializing in travel budgets and cost optimization. 
            You help travelers get the most value from their money by finding the best deals, suggesting cost-effective alternatives, 
            and ensuring proper budget allocation across accommodation, food, activities, and transportation.""",
            llm=self.llm,
            verbose=True
        )

    def accommodation_agent(self):
        return Agent(
            role='Accommodation Specialist',
            goal='Find the best lodging options based on budget, location, and traveler preferences.',
            backstory="""You are an accommodation expert who knows the best hotels, hostels, Airbnb options, 
            and unique stays in destinations worldwide. You consider factors like location convenience, 
            safety, amenities, and value for money.""",
            llm=self.llm,
            verbose=True
        )

    def transportation_agent(self):
        return Agent(
            role='Transportation Coordinator',
            goal='Plan optimal transportation routes and methods for the entire trip.',
            backstory="""You specialize in transportation logistics, knowing the best ways to get around cities 
            and between destinations. You're familiar with public transport systems, ride-sharing options, 
            car rentals, and can optimize routes to save time and money.""",
            llm=self.llm,
            verbose=True
        )

    def currency_conversion_agent(self):
        return Agent(
            role='Currency Exchange Specialist',
            goal='Convert budget amounts from USD to local currency with real-time exchange rates.',
            backstory="""You are a finance and forex expert with access to real-time exchange rate data. 
            You help travelers understand the actual purchasing power of their budget in the destination country, 
            provide insights on exchange rate fluctuations, and suggest the best methods for currency exchange.""",
            llm=self.llm,
            verbose=True
        )

    def visa_documentation_agent(self):
        return Agent(
            role='Visa & Documentation Officer',
            goal='Provide comprehensive visa requirements and documentation guidance for international travel.',
            backstory="""You act like an experienced visa officer with extensive knowledge of international 
            travel documentation requirements. You stay updated on visa policies, embassy locations, 
            application processes, and can guide travelers through complex documentation requirements.""",
            llm=self.llm,
            verbose=True
        )

    def flight_finder_agent(self):
        return Agent(
            role='Flight Deal Hunter',
            goal='Find the best flight options considering price, convenience, and traveler preferences.',
            backstory="""You are an expert airline deal hunter with deep knowledge of flight booking strategies, 
            seasonal price variations, airline routes, and booking platforms. You help travelers find the most 
            cost-effective flights while considering comfort and convenience factors.""",
            llm=self.llm,
            verbose=True
        )

    def hotel_finder_agent(self):
        return Agent(
            role='Hotel Booking Expert',
            goal='Recommend the best hotel options with detailed information including images and ratings.',
            backstory="""You are a hotel expert with extensive knowledge of accommodations worldwide. 
            You understand different hotel categories, amenities, location advantages, and can match 
            hotels to specific traveler needs and budgets. You provide comprehensive hotel information 
            including visual aspects and guest reviews.""",
            llm=self.llm,
            verbose=True
        )

    def local_transport_optimizer(self):
        return Agent(
            role='Local Transportation Optimizer',
            goal='Optimize local transportation with live directions and real-time information.',
            backstory="""You are a local transport expert who knows the ins and outs of urban mobility. 
            You understand public transport systems, traffic patterns, and can provide optimal routing 
            with real-time updates. You help travelers navigate efficiently and cost-effectively.""",
            llm=self.llm,
            verbose=True
        )

    def emergency_safety_agent(self):
        return Agent(
            role='Travel Safety Advisor',
            goal='Provide comprehensive safety guidelines, emergency contacts, and local safety information.',
            backstory="""You are a experienced travel safety advisor with knowledge of global safety conditions, 
            common travel scams, emergency procedures, and local safety protocols. You help travelers stay safe 
            and prepared for various situations while maintaining their travel experience quality.""",
            llm=self.llm,
            verbose=True
        )
    def mystery_mode_agent(self):
        return Agent(
            role='Serendipity Travel Generator',
            goal='Generate random destination selections from top global destinations with compelling reasons why each choice could be perfect.',
            backstory="""You are the master of travel serendipity, specializing in random destination selection that often leads to the most 
            memorable adventures. You have intimate knowledge of the world's top 20 most incredible destinations and can make any random 
            selection feel like destiny. You understand that sometimes the best trips come from unexpected choices and can convince anyone 
            that their randomly selected destination is exactly where they need to be.""",
            llm=self.llm,
            verbose=True
        )
    
    def currency_conversion_agent(self):
        return Agent(
            role='International Finance Advisor',
            goal='Provide real-time currency conversion, exchange rate insights, and international money management strategies.',
            backstory="""You are a financial advisor specializing in international travel finance. You monitor global exchange rates, 
            understand currency trends, know the best exchange methods for different countries, and help travelers maximize their purchasing 
            power abroad. You provide practical advice on payment methods, ATM strategies, and avoiding currency exchange fees.""",
            llm=self.llm,
            verbose=True
        )

    def story_narrator_agent(self):
        return Agent(
            role='Travel Story Weaver',
            goal='Transform travel plans into engaging narrative stories that make the journey feel like an epic adventure.',
            backstory="""You are a creative storyteller who transforms ordinary travel itineraries into compelling narrative adventures. 
            You weave together destination highlights, cultural elements, historical context, and personal journey themes to create 
            travel stories that inspire and excite. Your narratives make every trip feel like the beginning of a great adventure novel, 
            complete with character development, plot twists, and memorable scenes.""",
            llm=self.llm,
            verbose=True
        )