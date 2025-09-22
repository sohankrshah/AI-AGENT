from crewai import Crew, Process
from trip_agents import TripAgents
from trip_tasks import TripTasks
from api_services import APIIntegrationService
import logging

# Configure logging for better debugging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EnhancedTripCrew:
    def __init__(self, inputs):
        self.inputs = inputs
        self.agents_instance = TripAgents(use_gemini=True)
        self.tasks_instance = TripTasks()
        
        # Initialize all agents
        self._initialize_agents()
        
        # Initialize all tasks based on available agents
        self._initialize_tasks()

    def _initialize_agents(self):
        """Initialize all available agents"""
        # Core travel planning agents
        self.city_selector = self.agents_instance.country_selector_agent()
        self.local_expert = self.agents_instance.local_expert_agent()
        self.travel_planner = self.agents_instance.travel_planner_agent()
        self.budget_manager = self.agents_instance.budget_manager_agent()
        self.accommodation_specialist = self.agents_instance.accommodation_agent()
        self.transportation_coordinator = self.agents_instance.transportation_agent()
        
        # Enhanced service agents
        self.currency_converter = self.agents_instance.currency_conversion_agent()
        self.visa_officer = self.agents_instance.visa_documentation_agent()
        self.flight_hunter = self.agents_instance.flight_finder_agent()
        self.hotel_expert = self.agents_instance.hotel_finder_agent()
        self.transport_optimizer = self.agents_instance.local_transport_optimizer()
        self.safety_advisor = self.agents_instance.emergency_safety_agent()
        
        # Special feature agents
        self.mystery_mode = self.agents_instance.mystery_mode_agent()
        self.story_narrator = self.agents_instance.story_narrator_agent()

    def _initialize_tasks(self):
        """Initialize tasks with proper dependencies"""
        # Phase 1: Destination Planning
        self.destination_selection = self.tasks_instance.country_selector_task(
            self.city_selector, self.inputs
        )
        
        # Phase 2: Research and Intelligence
        self.destination_research = self.tasks_instance.city_research_task(
            self.local_expert, self.inputs
        )
        
        # Phase 3: Logistics Planning
        self.currency_conversion = self.tasks_instance.currency_conversion_task(
            self.currency_converter, self.inputs
        )
        
        self.visa_requirements = self.tasks_instance.visa_documentation_task(
            self.visa_officer, self.inputs
        )
        
        # Phase 4: Transportation Planning
        self.flight_optimization = self.tasks_instance.flight_finder_task(
            self.flight_hunter, self.inputs
        )
        
        self.transportation_planning = self.tasks_instance.transportation_task(
            self.transportation_coordinator, self.inputs
        )
        
        self.local_transport_optimization = self.tasks_instance.local_transport_optimization_task(
            self.transport_optimizer, self.inputs
        )
        
        # Phase 5: Accommodation Planning
        self.hotel_optimization = self.tasks_instance.hotel_finder_task(
            self.hotel_expert, self.inputs
        )
        
        self.accommodation_planning = self.tasks_instance.accommodation_task(
            self.accommodation_specialist, self.inputs
        )
        
        # Phase 6: Itinerary Creation (depends on research and logistics)
        self.itinerary_creation = self.tasks_instance.itinerary_creation_task(
            self.travel_planner, self.inputs
        )
        
        # Phase 7: Budget Planning (depends on itinerary and accommodations)
        self.budget_planning = self.tasks_instance.budget_planning_task(
            self.budget_manager, 
            self.inputs, 
            context_tasks=[
                self.itinerary_creation, 
                self.accommodation_planning, 
                self.transportation_planning
            ]
        )
        
        # Phase 8: Safety and Security
        self.safety_planning = self.tasks_instance.emergency_safety_task(
            self.safety_advisor, self.inputs
        )
        
        # Phase 9: Additional Features
        self.packing_guide = self.tasks_instance.packing_list_task(
            self.accommodation_specialist, self.inputs  # Reusing agent for packing
        )
        
        self.travel_story = self.tasks_instance.story_narrative_task(
            self.story_narrator, self.inputs
        )
        
        # Additional enhancement tasks
        self.weather_analysis = self.tasks_instance.weather_analysis_task(
            self.local_expert, self.inputs  # Reusing local expert for weather
        )
        
        self.cultural_immersion = self.tasks_instance.cultural_immersion_task(
            self.local_expert, self.inputs
        )

    def _initialize_mystery_mode_tasks(self):
        """Initialize mystery mode specific tasks"""
        self.mystery_destination = self.tasks_instance.mystery_mode_task(
            self.mystery_mode, self.inputs
        )

    def run_crew(self, mode="full", include_enhanced_features=True):
        try:
            # Configure API services
            if include_enhanced_features:
                try:
                    self.tasks_instance.api_service = APIIntegrationService()
                except ValueError as e:
                    print(f"API Configuration Warning: {e}")
                    print("Running with limited API features...")
                    include_enhanced_features = False

            # Select execution mode
            if mode == "mystery":
                return self._run_mystery_mode()
            elif mode == "basic":
                return self._run_basic_mode()
            elif mode == "full":
                return self._run_full_mode(include_enhanced_features)
            else:
                return self._run_custom_mode(include_enhanced_features)

        except Exception as e:
            print(f"Error running crew: {e}")
            return None

    def _run_mystery_mode(self):
        """Execute mystery/serendipity mode"""
        self._initialize_mystery_mode_tasks()
        
        crew = Crew(
            agents=[self.mystery_mode, self.story_narrator],
            tasks=[self.mystery_destination, self.travel_story],
            verbose=True,
            process=Process.sequential
        )
        
        return crew.kickoff()

    def _run_basic_mode(self):
        """Execute basic trip planning without API features"""
        basic_agents = [
            self.city_selector,
            self.local_expert,
            self.travel_planner,
            self.budget_manager,
            self.accommodation_specialist,
            self.transportation_coordinator
        ]
        
        basic_tasks = [
            self.destination_selection,
            self.destination_research,
            self.itinerary_creation,
            self.accommodation_planning,
            self.transportation_planning,
            self.budget_planning
        ]
        
        crew = Crew(
            agents=basic_agents,
            tasks=basic_tasks,
            verbose=True,
            process=Process.sequential
        )
        
        return crew.kickoff()

    def _run_full_mode(self, include_enhanced_features):
        """Execute comprehensive trip planning"""
        # Core agents for all modes
        agents = [
            self.city_selector,
            self.local_expert,
            self.currency_converter,
            self.visa_officer,
            self.travel_planner,
            self.budget_manager,
            self.accommodation_specialist,
            self.transportation_coordinator,
            self.safety_advisor
        ]
        
        # Core tasks for all modes
        tasks = [
            self.destination_selection,
            self.destination_research,
            self.currency_conversion,
            self.visa_requirements,
            self.itinerary_creation,
            self.accommodation_planning,
            self.transportation_planning,
            self.budget_planning,
            self.safety_planning,
            self.packing_guide
        ]
        
        # Add enhanced features if available
        if include_enhanced_features:
            agents.extend([
                self.flight_hunter,
                self.hotel_expert,
                self.transport_optimizer,
                self.story_narrator
            ])
            
            tasks.extend([
                self.flight_optimization,
                self.hotel_optimization,
                self.local_transport_optimization,
                self.travel_story
            ])

        crew = Crew(
            agents=agents,
            tasks=tasks,
            verbose=True,
            process=Process.sequential
        )
        
        return crew.kickoff()

    def _run_custom_mode(self, include_enhanced_features):
        """Execute custom mode based on user preferences"""
        # Start with essential agents
        agents = [self.city_selector, self.local_expert, self.travel_planner]
        tasks = [self.destination_selection, self.destination_research, self.itinerary_creation]
        
        # Add agents based on user needs
        user_interests = self.inputs.get('interests', [])
        travel_type = self.inputs.get('travel_type', '').lower()
        
        # Budget-conscious travelers need budget management
        if 'budget' in travel_type or any('budget' in interest.lower() for interest in user_interests):
            agents.append(self.budget_manager)
            tasks.append(self.budget_planning)
        
        # International travelers need visa and currency services
        if self.inputs.get('origin') != self.inputs.get('destination'):
            agents.extend([self.currency_converter, self.visa_officer])
            tasks.extend([self.currency_conversion, self.visa_requirements])
        
        # All travelers need accommodation and safety
        agents.extend([self.accommodation_specialist, self.safety_advisor])
        tasks.extend([self.accommodation_planning, self.safety_planning])
        
        # Add transportation based on preferences
        transport_prefs = self.inputs.get('transport_preferences', [])
        if transport_prefs:
            agents.append(self.transportation_coordinator)
            tasks.append(self.transportation_planning)
            
            if include_enhanced_features:
                agents.extend([self.flight_hunter, self.transport_optimizer])
                tasks.extend([self.flight_optimization, self.local_transport_optimization])
        
        # Add luxury features for luxury travelers
        if 'luxury' in travel_type and include_enhanced_features:
            agents.append(self.hotel_expert)
            tasks.append(self.hotel_optimization)
        
        # Add story narration for adventure/cultural travelers
        if any(keyword in travel_type for keyword in ['adventure', 'cultural', 'educational']):
            agents.append(self.story_narrator)
            tasks.append(self.travel_story)

        crew = Crew(
            agents=agents,
            tasks=tasks,
            verbose=True,
            process=Process.sequential
        )
        
        return crew.kickoff()

    def get_available_modes(self):
        """Return list of available execution modes"""
        return {
            "basic": "Essential trip planning without API features",
            "full": "Comprehensive planning with all available features",
            "mystery": "Surprise destination with narrative storytelling",
            "custom": "Adaptive planning based on user preferences"
        }

    def get_crew_status(self):
        """Return current crew configuration status"""
        api_status = "Available" if self.tasks_instance.api_service else "Limited"
        
        return {
            "agents_initialized": 12,
            "tasks_available": 17,  # Updated count
            "api_services": api_status,
            "modes_available": list(self.get_available_modes().keys())
        }

    def validate_inputs(self):
        """Validate input parameters before crew execution"""
        errors = []
        warnings = []
        
        # Required fields
        if not self.inputs.get('destination'):
            errors.append("Destination is required")
        
        if not self.inputs.get('duration') or self.inputs['duration'] < 1:
            errors.append("Trip duration must be at least 1 day")
        
        if not self.inputs.get('budget'):
            errors.append("Budget is required")
        
        # Warnings for missing optional fields
        if not self.inputs.get('interests'):
            warnings.append("No interests specified - using general recommendations")
        
        if not self.inputs.get('origin'):
            warnings.append("Origin location not specified - limited transportation planning")
        
        # Validate budget format
        budget = str(self.inputs.get('budget', ''))
        if budget and not any(char.isdigit() for char in budget):
            errors.append("Budget must contain numeric values")
        
        return {
            'valid': len(errors) == 0,
            'errors': errors,
            'warnings': warnings
        }

    def get_execution_summary(self, mode="full"):
        """Get summary of what will be executed in specified mode"""
        mode_info = self.get_available_modes().get(mode, "Unknown mode")
        
        if mode == "basic":
            agent_count = 6
            task_list = ["Destination Selection", "Research", "Itinerary", "Accommodation", "Transportation", "Budget"]
        elif mode == "mystery":
            agent_count = 2
            task_list = ["Mystery Destination", "Adventure Story"]
        elif mode == "full":
            agent_count = 12
            task_list = ["All available tasks including API-enhanced features"]
        else:
            agent_count = "Variable"
            task_list = ["Adaptive based on preferences"]
        
        return {
            'mode': mode,
            'description': mode_info,
            'agents': agent_count,
            'estimated_tasks': task_list,
            'api_dependent': mode in ['full', 'custom']
        }

    def export_plan_data(self, result):
        """Export trip plan data in structured format"""
        if not result or not hasattr(result, 'tasks_output'):
            return None
        
        try:
            plan_data = {
                'destination': self.inputs.get('destination'),
                'duration': self.inputs.get('duration'),
                'budget': self.inputs.get('budget'),
                'generated_at': str(__import__('datetime').datetime.now()),
                'sections': {}
            }
            
            # Map task outputs to sections
            section_mapping = {
                0: 'destinations',
                1: 'city_research', 
                2: 'currency_info',
                3: 'visa_requirements',
                4: 'itinerary',
                5: 'accommodation',
                6: 'transportation',
                7: 'budget_breakdown',
                8: 'safety_guide',
                9: 'packing_list'
            }
            
            for idx, task_output in enumerate(result.tasks_output):
                if idx in section_mapping:
                    plan_data['sections'][section_mapping[idx]] = {
                        'content': task_output.raw if hasattr(task_output, 'raw') else str(task_output),
                        'task_name': getattr(task_output, 'name', f'Task {idx}')
                    }
            
            return plan_data
            
        except Exception as e:
            logger.error(f"Error exporting plan data: {e}")
            return None