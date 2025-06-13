"""Acme Corp Receptionist Agent - Version 1

This demo agent greets callers, collects their name, and performs
very light intent classification.  The example follows the
`Agents SDK` documentation so each step mirrors the tutorials
found in the SignalWire docs.
"""
import os
from typing import Dict, Any, Optional  # used for type annotations
from signalwire_agents import AgentBase  # base class for all SignalWire agents
from signalwire_agents.core.function_result import SwaigFunctionResult  # helper for returning results to the caller
from dotenv import load_dotenv
import structlog

# Load variables from the optional `.env` file so the script can be
# configured without code changes.  This mirrors the approach used
# throughout the Agents SDK examples.
load_dotenv()

# Configure structured logging so all log lines include timestamps and
# context information useful for debugging agent behavior.
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
        # Get configuration from environment variables. These allow the
        # same code to run locally or in the cloud by simply changing the
        # `.env` file.
        agent_host = os.getenv("AGENT_HOST", "0.0.0.0")
        agent_port = int(os.getenv("AGENT_PORT", "3000"))
        agent_route = os.getenv("AGENT_ROUTE", "/receptionist")
        
        # Company configuration used to personalize the prompt.
        self.company_name = os.getenv("COMPANY_NAME", "Acme Corp")
        self.company_specialty = os.getenv("COMPANY_SPECIALTY", "Widgets for Roadrunners")
        self.company_phone = os.getenv("COMPANY_PHONE", "+1-555-ACME-CORP")
        
        # Initialize parent class.  `use_pom=True` enables the Prompt
        # Object Model which keeps prompt content structured.
        super().__init__(
            name="acme-receptionist-v1",
            route=agent_route,
            host=agent_host,
            port=agent_port,
            use_pom=True,
            basic_auth=("", ""))
        
        # Monkey-patch to disable all auth for this demo so it can be
        # easily tested without credentials.  Production deployments
        # should implement proper authentication.
        def _no_auth(self, *a, **k):
            return True

        self._check_basic_auth = _no_auth.__get__(self, self.__class__)
        
        # Store caller information so it can be reused across multiple
        # SWAIG function calls during the conversation.
        self.caller_info = {}
        
        # Setup agent personality and register SWAIG tools
        self._setup_personality()
        self._setup_functions()
        
        logger.info("receptionist_initialized", 
                   company=self.company_name,
                   route=agent_route,
                   port=agent_port)
    
    def _setup_personality(self):
        """Configure the receptionist's personality using POM.

        The Prompt Object Model lets us break the prompt into structured
        sections which the SDK merges into the final prompt delivered to
        the LLM.
        """
        
        # Define agent personality describing how the assistant should sound
        self.prompt_add_section(
            "Personality",
            body="You are a friendly, efficient AI receptionist for Acme Corp."
        )
        # Define the high level goal so the LLM stays on task
        self.prompt_add_section(
            "Goal",
            body="Capture the caller's name and reason for calling, then print them."
        )
        # Provide explicit instructions in bullet form. The Agents SDK
        # automatically formats these for the model.
        self.prompt_add_section(
            "Instructions",
            bullets=[
                "Politely ask for the caller's name and reason for calling",
                "Print all gathered information to the console",
                "Respond concisely and professionally",
            ]
        )
        
        # Add static company information that the agent can reference
        self.prompt_add_section(
            "Company Information",
            body=f"""
Company: {self.company_name}
Specialty: {self.company_specialty}
Phone: {self.company_phone}

We help customers with:
- Technical support for existing products
- Information about new products and pricing
- General inquiries about our widgets"""
        )
    
    def _setup_functions(self):
        """Register SWAIG functions for the receptionist agent.

        SWAIG (SignalWire AI Gateway) functions define explicit
        capabilities the agent exposes.  They can be executed from
        the SignalWire CLI or other tools for testing.
        """

        # Function to capture caller name
        self.define_tool(
            name="capture_caller_name",
            description="Capture caller's name and reason for calling.",
            parameters={
                "caller_name": {"type": "string", "description": "The caller's name"},
                "reason": {"type": "string", "description": "Reason for calling"}
            },
            handler=self._handle_capture_caller_name,
        )
    
    def _print_caller_info(self, caller_name: str, reason: str) -> None:
        """Print caller details in a simple format.

        In a real application this could be stored in a database or sent
        to another service for follow-up.
        """
        print(f"Caller: {caller_name}, Reason: {reason}")

    def _handle_capture_caller_name(self, args, raw=None):
        # Retrieve parameters passed from the LLM invocation
        caller_name = args.get("caller_name", "")
        reason = args.get("reason", "")

        # Log and display the captured information for debugging
        logger.info("caller_captured", caller=caller_name, reason=reason)
        self._print_caller_info(caller_name, reason)
        return SwaigFunctionResult(
            f"Thank you {caller_name}, we have noted your reason: '{reason}'."
        )

# Create the agent instance
agent = ReceptionistAgent()

# For CLI testing
if __name__ == "__main__":
    # Running this module directly prints helpful information so you can
    # verify the environment variables are loaded correctly.
    print("Acme Corp Receptionist Agent v1 - Ready for testing")
    print(f"Company: {agent.company_name}")
    print(f"Specialty: {agent.company_specialty}")
    print(f"Route: {os.getenv('AGENT_ROUTE', '/receptionist')}")
