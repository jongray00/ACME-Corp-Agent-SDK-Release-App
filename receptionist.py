"""
Acme Corp Receptionist Agent - Version 1
A basic AI receptionist that greets callers, captures their name,
and performs simple intent classification.
"""
import os
from typing import Dict, Any, Optional
from signalwire_agents import AgentBase
from signalwire_agents.core.function_result import SwaigFunctionResult
from dotenv import load_dotenv
import structlog
# Load environment variables
load_dotenv()
# Configure structured logging
logger = structlog.get_logger()
class ReceptionistAgent(AgentBase):
    """
    Basic AI Receptionist Agent for Acme Corp.
    This agent demonstrates fundamental SignalWire agent capabilities:
    - Greeting callers with company information
    - Capturing caller names
    - Basic intent classification
    - Professional personality using POM
    """
    
    def __init__(self):
        """Initialize the Receptionist Agent with configuration from environment."""
        # Get configuration from environment
        agent_host = os.getenv("AGENT_HOST", "0.0.0.0")
        agent_port = int(os.getenv("AGENT_PORT", "3000"))
        agent_route = os.getenv("AGENT_ROUTE", "/receptionist")
        
        # Company configuration
        self.company_name = os.getenv("COMPANY_NAME", "Acme Corp")
        self.company_specialty = os.getenv("COMPANY_SPECIALTY", "Widgets for Roadrunners")
        self.company_phone = os.getenv("COMPANY_PHONE", "+1-555-ACME-CORP")
        
        # Initialize parent class
        super().__init__(
            name="acme-receptionist-v1",
            route=agent_route,
            host=agent_host,
            port=agent_port,
            use_pom=True,
            basic_auth=("", ""))
        
        # Monkey-patch to disable all auth
        def _no_auth(self, *a, **k): return True
        self._check_basic_auth = _no_auth.__get__(self, self.__class__)
        
        # Store caller information
        self.caller_info = {}
        
        # Setup agent personality and functions
        self._setup_personality()
        self._setup_functions()
        
        logger.info("receptionist_initialized", 
                   company=self.company_name,
                   route=agent_route,
                   port=agent_port)
    
    def _setup_personality(self):
        """Configure the receptionist's personality using POM."""
        
        # Define agent personality
        self.prompt_add_section("Personality", body="You are a friendly, efficient AI receptionist for Acme Corp.")
        # Define agent goal
        self.prompt_add_section("Goal", body="Capture the caller's name, reason for calling, and call ID, then print them.")
        # Define agent instructions
        self.prompt_add_section("Instructions", bullets=[
            "Politely ask for the caller's name and reason for calling",
            "Record the call ID for every interaction",
            "Print all gathered information to the console",
            "Respond concisely and professionally"
        ])
        
        # Add company information
        self.prompt_add_section("Company Information", body=f"""
Company: {self.company_name}
Specialty: {self.company_specialty}
Phone: {self.company_phone}

We help customers with:
- Technical support for existing products
- Information about new products and pricing
- General inquiries about our widgets""")
    
    def _setup_functions(self):
        """Register SWAIG functions for the receptionist agent."""
        
        # Function to capture caller name
        self.define_tool(
            name="capture_caller_name",
            description="Capture caller's name, reason for calling, and call ID.",
            parameters={
                "caller_name": {"type": "string", "description": "The caller's name"},
                "reason": {"type": "string", "description": "Reason for calling"},
                "call_id": {"type": "string", "description": "Unique call identifier"}
            },
            handler=self._handle_capture_caller_name
        )
    
    def _handle_capture_caller_name(self, args, raw=None):
        caller_name = args.get("caller_name", "")
        reason = args.get("reason", "")
        call_id = args.get("call_id", "")
        print(f"[CALL] Name: {caller_name} | Reason: {reason} | CallID: {call_id}")
        return SwaigFunctionResult(f"Thank you {caller_name}, we have noted your reason: '{reason}'.")

# Create the agent instance
agent = ReceptionistAgent()

# For CLI testing
if __name__ == "__main__":
    print("Acme Corp Receptionist Agent v1 - Ready for testing")
    print(f"Company: {agent.company_name}")
    print(f"Specialty: {agent.company_specialty}")
    print(f"Route: {os.getenv('AGENT_ROUTE', '/receptionist')}") 