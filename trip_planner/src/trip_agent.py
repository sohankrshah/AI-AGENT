from trip_agents import TripAgents
from trip_tasks import TripTasks
from trip_crew import EnhancedTripCrew

class TripAgent:
    def __init__(self):
        self.agents = TripAgents()
    
    def get_agent(self, agent_type):
        agent_methods = {
            'country_selector': self.agents.country_selector_agent,
            'travel_planner': self.agents.travel_planner_agent,
            'local_expert': self.agents.local_expert_agent,
            'budget_manager': self.agents.budget_manager_agent,
            'accommodation': self.agents.accommodation_agent,
            'transportation': self.agents.transportation_agent,
            'currency_conversion': self.agents.currency_conversion_agent,
            'visa_documentation': self.agents.visa_documentation_agent,
            'flight_finder': self.agents.flight_finder_agent,
            'hotel_finder': self.agents.hotel_finder_agent,
            'local_transport': self.agents.local_transport_optimizer,
            'safety_advisor': self.agents.emergency_safety_agent
        }
        
        if agent_type in agent_methods:
            return agent_methods[agent_type]()
        else:
            raise ValueError(f"Unknown agent type: {agent_type}")


TripCrew = EnhancedTripCrew

