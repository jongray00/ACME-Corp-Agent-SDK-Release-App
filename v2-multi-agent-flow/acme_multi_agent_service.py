#!/usr/bin/env python3
"""
ACME Corp Multi-Agent Service - Enhanced Receptionist System
An advanced enhancement of the basic ACME Corp receptionist from v1-sdk-basics

This service provides specialized assistance through three dedicated agents:
- Receptionist Agent (/) - Enhanced version of v1 receptionist with intelligent routing
- Sales Agent (/sales) - Handles service inquiries and quotes for ACME phone repair services
- Support Agent (/support) - Provides technical support and diagnostics for phone repair customers

Key enhancements over v1:
- Multi-agent architecture with specialized expertise
- Secure session-level context storage using global_data
- Seamless agent transfers with automatic context passing
- Native vector search for knowledge bases
- POM (Prompt Object Model) for structured prompts
"""

import os
import json
from datetime import datetime
from typing import Dict, Any, Optional
from dotenv import load_dotenv

from signalwire_agents import AgentBase, AgentServer
from signalwire_agents.core.function_result import SwaigFunctionResult
from signalwire_agents.core.logging_config import get_logger

# Import debug configuration
from debug_config import (
    get_debug_params, 
    format_debug_message, 
    log_function_entry, 
    log_function_exit,
    debug_print_global_data
)

# Load environment variables
load_dotenv()

# Set up logger
logger = get_logger(__name__)

# Debug mode is always enabled for comprehensive monitoring
DEBUG_MODE = True


class ACMEReceptionistAgent(AgentBase):
    """
    Enhanced ACME Corp Receptionist Agent - v2 Multi-Agent Enhancement
    
    This agent builds upon the basic v1 receptionist with enhanced capabilities:
    - Intelligent routing to specialized agents
    - Secure context storage using global_data
    - Professional ACME Corp branding and messaging
    - POM-structured prompts for consistency
    """
    
    def __init__(self):
        # Get company configuration from environment (same as v1)
        self.company_name = os.getenv("COMPANY_NAME", "Acme Corp")
        self.company_specialty = os.getenv("COMPANY_SPECIALTY", "Professional Phone Repair Services")
        self.company_phone = os.getenv("COMPANY_PHONE", "+1-555-ACME-CORP")
        
        super().__init__(
            name="ACME Receptionist Agent v2",
            route="/",
            host="0.0.0.0",
            port=3001,
            auto_answer=True,
            use_pom=True,  # Enable Prompt Object Model
            basic_auth=("", "")
        )
        
        # Set debug parameters after initialization (always enabled)
        debug_params = get_debug_params()
        self.set_params(debug_params)
        
        # Monkey-patch to disable all auth for this demo so it can be
        # easily tested without credentials.  Production deployments
        # should implement proper authentication.
        def _no_auth(self, *a, **k):
            return True

        self._check_basic_auth = _no_auth.__get__(self, self.__class__)
        
        # Setup POM-structured personality and register functions
        self._setup_personality()
        self._setup_functions()
        
        # Set post-prompt for conversation analysis
        self.set_post_prompt("""
        Analyze this conversation and provide a summary including:
        1. Caller's name and inquiry type
        2. Key issues or requests discussed
        3. Actions taken (functions called)
        4. Whether the caller was successfully transferred to a specialist
        5. Overall conversation outcome
        
        Format as JSON for easy processing.
        """)
        
        # Set post-prompt URL for debugging and monitoring
        self.set_post_prompt_url("https://webhook.site/afef5994-294f-4916-b3d6-51bfe27d04a6")
        
        # Set up dynamic configuration for specialist routing
        self.set_dynamic_config_callback(self.configure_routing)
        
        logger.info("acme_receptionist_v2_initialized", 
                   company=self.company_name,
                   route="/",
                   port=3001)
    
    def _setup_personality(self):
        """Configure the enhanced receptionist personality using POM"""
        
        # Define core personality (enhanced from v1)
        self.prompt_add_section(
            "Personality",
            body=f"You are a friendly, professional AI receptionist for {self.company_name}, enhanced with intelligent routing capabilities."
        )
        
        # Define enhanced goals
        self.prompt_add_section(
            "Goal", 
            body="Greet callers warmly, capture their information, determine their needs, and route them to the appropriate specialist."
        )
        
        # Structured instructions using POM
        self.prompt_add_section(
            "Instructions",
            bullets=[
                "Greet callers professionally and ask for their name",
                "Determine if they need sales assistance or technical support",
                "Capture relevant details about their inquiry",
                "Use save_caller_info to store their information securely",
                "Route them to the appropriate specialist with transfer_to_specialist",
                "For external transfers, use transfer_to_phone for PSTN or transfer_to_sip for SIP addresses"
            ]
        )
        
        # Company information (enhanced from v1)
        self.prompt_add_section(
            "Company Information",
            body=f"""
Company: {self.company_name}
Specialty: {self.company_specialty}
Phone: {self.company_phone}

Our Specialists:
- Sales Team: Phone repair service quotes, pricing inquiries, device assessments
- Support Team: Technical issues, repair status, troubleshooting device problems

Transfer Options:
- Internal Specialists: Use transfer_to_specialist for sales or support
- External Numbers: Use transfer_to_phone for PSTN transfers
- SIP/VoIP: Use transfer_to_sip for call fabric routing

We are the premier provider of professional phone repair services designed to get your device back to perfect working condition."""
        )
        
        # Available context information
        self.prompt_add_section(
            "Context Available",
            body="You can access caller information using: ${global_data.caller_name}, ${global_data.inquiry_type}, ${global_data.details}"
        )
        
    def _setup_functions(self):
        """Set up SWAIG functions for enhanced receptionist capabilities"""
        
        # Store reference to self for use in tool functions
        agent_instance = self
        
        @self.tool(
            name="save_caller_info",
            description="Save caller information before routing to specialist",
            parameters={
                "caller_name": {"type": "string", "description": "Caller's name"},
                "inquiry_type": {"type": "string", "description": "Type of inquiry (sales or support)"},
                "details": {"type": "string", "description": "Additional details about their needs"}
            }
        )
        def save_caller_info(args, raw_data):
            """Enhanced caller info capture with secure storage"""
            # Function entry logging (always enabled)
            log_function_entry("ACMEReceptionistAgent", "save_caller_info", 
                             args=args, raw_data_present=raw_data is not None)
            
            caller_name = args.get("caller_name", "")
            inquiry_type = args.get("inquiry_type", "")
            details = args.get("details", "")
        
            # Enhanced logging for debugging (same as v1 but with more detail)
            agent_instance.log.info("caller_captured", 
                         caller=caller_name, 
                         inquiry=inquiry_type, 
                         details=details,
                         timestamp=datetime.now().isoformat())
            
            # Enhanced debug output (always enabled)
            agent_instance.debug_print("Caller Info Captured", 
                           name=caller_name,
                           inquiry_type=inquiry_type,
                           details=details)
            
            # Store in global_data for specialist access (v2 enhancement)
            global_data_update = {
                "caller_name": caller_name,
                "inquiry_type": inquiry_type,
                "details": details,
                "reception_completed": True,
                "agent_path": ["receptionist"],
                "timestamp": datetime.now().isoformat(),
                "company_context": {
                    "name": agent_instance.company_name,
                    "specialty": agent_instance.company_specialty
                }
            }
            
            result = (
                SwaigFunctionResult(f"Thank you {caller_name}! I've noted your {inquiry_type} inquiry. Let me connect you with the right specialist.")
                .update_global_data(global_data_update)
            )
            
            # Debug global data update (always enabled)
            agent_instance.debug_print("Global Data Updated", **global_data_update)
            log_function_exit("ACMEReceptionistAgent", "save_caller_info", result)
            
            return result
    
        # New v2 transfer capability
        @self.tool(
            name="transfer_to_specialist",
            description="Transfer caller to appropriate specialist",
            parameters={
                "specialist_type": {"type": "string", "description": "Specialist to transfer to: 'sales' or 'support'"}
            }
        )
        def transfer_to_specialist(args, raw_data=None):
            """Route caller to appropriate specialist with context"""
            # Enhanced function entry logging
            log_function_entry("ACMEReceptionistAgent", "transfer_to_specialist", 
                             args=args, raw_data_present=raw_data is not None)
            
            # Debug the transfer request
            agent_instance.debug_print("Transfer request received", 
                           args=args, 
                           raw_data_present=raw_data is not None)
            
            specialist_type = args.get("specialist_type", "").lower()
            
            # Get current global data for transfer URLs from raw_data
            global_data = raw_data.get("global_data", {}) if raw_data else {}
            
            # Get the URLs from global_data
            sales_url = global_data.get("sales_url")
            support_url = global_data.get("support_url")
            
            agent_instance.debug_print("Available transfer URLs", 
                           sales_url=sales_url,
                           support_url=support_url)
            
            if specialist_type == "sales":
                agent_instance.debug_print("Sales transfer requested", transfer_url=sales_url)
                
                if not sales_url:
                    error_msg = "Sales URL not found in global data"
                    agent_instance.debug_print("Transfer error", error=error_msg)
                    return SwaigFunctionResult("I'm having trouble connecting to our sales team. Let me try again.")
                
                # Create transfer result with enhanced debugging
                agent_instance.debug_print("Creating sales transfer", 
                               destination=sales_url,
                               transfer_type="sales")
                
                result = (
                    SwaigFunctionResult("Connecting you with our sales specialist now. They'll have all your information and can help with product inquiries.")
                    .swml_transfer(
                        dest=sales_url,
                        ai_response="You're back with our main reception. How else can I assist you today?"
                    )
                    .set_post_process(True)
                )
                
                agent_instance.debug_print("Sales transfer result created", 
                               result_type=type(result).__name__,
                               has_swml=hasattr(result, '_swml_data'))
                
                log_function_exit("ACMEReceptionistAgent", "transfer_to_specialist", result)
                return result
                
            elif specialist_type == "support":
                agent_instance.debug_print("Support transfer requested", transfer_url=support_url)
                
                if not support_url:
                    error_msg = "Support URL not found in global data"
                    agent_instance.debug_print("Transfer error", error=error_msg)
                    return SwaigFunctionResult("I'm having trouble connecting to our support team. Let me try again.")
                
                # Create transfer result with enhanced debugging
                agent_instance.debug_print("Creating support transfer", 
                               destination=support_url,
                               transfer_type="support")
                
                result = (
                    SwaigFunctionResult("Connecting you with our technical support specialist now. They'll have all your information and can help resolve your issue.")
                    .swml_transfer(
                        dest=support_url,
                        ai_response="You're back with our main reception. How else can I assist you today?"
                    )
                    .set_post_process(True)
                )
                
                agent_instance.debug_print("Support transfer result created", 
                               result_type=type(result).__name__,
                               has_swml=hasattr(result, '_swml_data'))
                
                log_function_exit("ACMEReceptionistAgent", "transfer_to_specialist", result)
                return result
            
            # Unknown specialist type
            error_msg = f"Unknown specialist type: {specialist_type}"
            agent_instance.debug_print("Transfer error", error=error_msg, specialist_type=specialist_type)
            
            result = SwaigFunctionResult("I apologize, but I couldn't determine which specialist you need. Please let me know if you need sales or support assistance.")
            log_function_exit("ACMEReceptionistAgent", "transfer_to_specialist", result)
            return result

        # Add PSTN transfer capability
        @self.tool(
            name="transfer_to_phone",
            description="Transfer caller to a phone number",
            parameters={
                "phone_number": {"type": "string", "description": "Phone number to transfer to (e.g., +15551234567)"},
                "department": {"type": "string", "description": "Department being transferred to"}
            }
        )
        def transfer_to_phone(args, raw_data):
            """Transfer to PSTN phone number"""
            log_function_entry("ACMEReceptionistAgent", "transfer_to_phone", 
                             args=args, raw_data_present=raw_data is not None)
            
            phone_number = args.get("phone_number", "")
            department = args.get("department", "")
            
            agent_instance.debug_print("PSTN transfer requested", 
                           phone_number=phone_number,
                           department=department)
            
            # Example PSTN numbers for different departments
            dept_numbers = {
                "sales": "+15555551234",
                "support": "+15555555678",
                "billing": "+15555559012"
            }
            
            # Use provided number or department default
            transfer_number = phone_number or dept_numbers.get(department.lower(), "")
            
            if not transfer_number:
                return SwaigFunctionResult("I need a valid phone number or department to transfer you.")
            
            result = (
                SwaigFunctionResult(f"Transferring you to {department} at {transfer_number}. One moment please.")
                .connect(transfer_number, final=True, from_addr=agent_instance.company_phone)
            )
            
            log_function_exit("ACMEReceptionistAgent", "transfer_to_phone", result)
            return result

        # Add SIP/Call Fabric transfer capability
        @self.tool(
            name="transfer_to_sip",
            description="Transfer caller to SIP address or call fabric endpoint",
            parameters={
                "sip_address": {"type": "string", "description": "SIP address (e.g., sales@company.com)"},
                "return_on_hangup": {"type": "boolean", "description": "Whether call should return if far end hangs up"}
            }
        )
        def transfer_to_sip(args, raw_data):
            """Transfer to SIP/Call Fabric address"""
            log_function_entry("ACMEReceptionistAgent", "transfer_to_sip", 
                             args=args, raw_data_present=raw_data is not None)
            
            sip_address = args.get("sip_address", "")
            return_on_hangup = args.get("return_on_hangup", False)
            
            agent_instance.debug_print("SIP transfer requested", 
                           sip_address=sip_address,
                           return_on_hangup=return_on_hangup)
            
            # Example SIP addresses for your call fabric
            sip_endpoints = {
                "sales": "sales@acmecorp.sw.com",
                "support": "support@acmecorp.sw.com",
                "escalation": "supervisor@acmecorp.sw.com"
            }
            
            if not sip_address:
                return SwaigFunctionResult("I need a valid SIP address to transfer you.")
            
            # Determine if this is a final or non-final transfer
            final_transfer = not return_on_hangup
            
            if final_transfer:
                # Permanent transfer using connect
                result = (
                    SwaigFunctionResult(f"Transferring you to {sip_address}. Have a great day!")
                    .connect(sip_address, final=True)
                )
            else:
                # Temporary transfer with return capability
                result = (
                    SwaigFunctionResult(f"Connecting you to {sip_address}. You'll return here if disconnected.")
                    .swml_transfer(
                        dest=sip_address,
                        ai_response="You're back with reception. How else can I help you?"
                    )
                )
            
            log_function_exit("ACMEReceptionistAgent", "transfer_to_sip", result)
            return result

    def configure_routing(self, query_params, body_params, headers, agent):
        """Configure agent with specialist routing capabilities"""
        # Enhanced debug logging for routing configuration
        self.debug_print("Configuring routing", 
                       query_params=query_params,
                       body_params=body_params,
                       headers=dict(headers) if headers else None)
        
        # Build transfer URLs for specialists
        base_url = self.get_full_url(include_auth=False).rstrip('/')
        sales_url = f"{base_url}/sales"
        support_url = f"{base_url}/support"
        
        self.debug_print("Generated transfer URLs", 
                       base_url=base_url,
                       sales_url=sales_url,
                       support_url=support_url)
        
        # Store routing information in global data using self instead of agent parameter
        routing_data = {
            "sales_url": sales_url,
            "support_url": support_url,
            "agent_type": "receptionist",
            "session_start": datetime.now().isoformat(),
            "company_info": {
                "name": self.company_name,
                "specialty": self.company_specialty,
                "phone": self.company_phone
            }
        }
        
        self.set_global_data(routing_data)
        
        # Verify global data was set correctly
        verification_data = self.get_global_data()
        self.debug_print("Routing configuration complete", 
                       data_set=routing_data,
                       data_verified=verification_data,
                       urls_match=verification_data.get("sales_url") == sales_url and verification_data.get("support_url") == support_url)

    def debug_print(self, message: str, **kwargs):
        """Enhanced debug output with timestamp and consistent formatting (always enabled)"""
        debug_msg = format_debug_message(self.__class__.__name__, message, **kwargs)
        print(debug_msg)
        # Also log to structured logger
        self.log.debug(message.replace(" ", "_").lower(), **kwargs)


class ACMESalesAgent(AgentBase):
    """
    ACME Corp Sales Specialist Agent
    
    Specialized agent for handling ACME widget sales inquiries,
    product recommendations, and pricing information.
    """
    
    def __init__(self):
        super().__init__(
            name="ACME Sales Agent",
            route="/sales",
            host="0.0.0.0",
            port=3001,
            auto_answer=True,
            use_pom=True,  # Enable Prompt Object Model
            basic_auth=("", "")
        )
        
        # Set a distinct voice for sales
        self.add_language("English", "en-US", "josh")
        
        # Set debug parameters after initialization (always enabled)
        debug_params = get_debug_params()
        self.set_params(debug_params)
        
        # Monkey-patch to disable all auth for this demo so it can be
        # easily tested without credentials.  Production deployments
        # should implement proper authentication.
        def _no_auth(self, *a, **k):
            return True

        self._check_basic_auth = _no_auth.__get__(self, self.__class__)
        
        # Add native vector search for ACME product knowledge
        self.add_skill("native_vector_search", {
            "tool_name": "search_product_knowledge",
            "description": "Search ACME product catalog and pricing information",
            "index_file": "acme_products_knowledge.swsearch",
            "count": 3
        })
        
        self._setup_personality()
        
        # Set post-prompt for sales conversation analysis
        self.set_post_prompt("""
        Analyze this sales conversation and provide a summary including:
        1. Customer's name and device information
        2. Repair services discussed or recommended
        3. Pricing information provided
        4. Customer's decision or next steps
        5. Overall sales outcome
        
        Format as JSON for easy processing.
        """)
        
        # Set post-prompt URL for debugging and monitoring
        self.set_post_prompt_url("https://webhook.site/afef5994-294f-4916-b3d6-51bfe27d04a6")
        
        self.set_dynamic_config_callback(self.configure_sales_agent)
    
    def _setup_personality(self):
        """Configure sales specialist personality using POM"""
        
        self.prompt_add_section(
            "Personality",
            body="You are a knowledgeable and helpful sales specialist for ACME Corp, expert in phone repair services and device diagnostics. You have a friendly, professional voice that helps put customers at ease."
        )
        
        self.prompt_add_section(
            "Goal",
            body="Help customers understand their phone repair options, provide accurate pricing information, and guide them through the repair service process."
        )
        
        self.prompt_add_section(
            "Instructions",
            bullets=[
                "Welcome the caller warmly and acknowledge you have their information from reception",
                "Reference their specific issue (available in global_data.details) in your greeting",
                "Use caller context from global_data (${global_data.caller_name}, ${global_data.details})",
                "Ask detailed questions about their device and repair needs",
                "Search the product knowledge base for current pricing and service information",
                "Provide personalized repair recommendations with accurate pricing",
                "Help them understand repair options, timelines, and warranty coverage"
            ]
        )
        
        self.prompt_add_section(
            "Initial Greeting",
            body="Start your conversation by saying: 'Hello ${global_data.caller_name}, I'm your ACME Corp sales specialist. I understand you're having an issue with ${global_data.details}. I'll help you understand your repair options and costs.'"
        )
        
        self.prompt_add_section(
            "Context Available",
            body="Caller information: ${global_data.caller_name}, ${global_data.inquiry_type}, ${global_data.details}, ${global_data.agent_path}"
        )
    
    def configure_sales_agent(self, query_params, body_params, headers, agent):
        """Configure sales agent with caller context"""
        self.debug_print("Configuring sales agent", 
                       query_params=query_params,
                       body_params=body_params)
        
        current_data = self.get_global_data() or {}
        self.debug_print("Sales agent initial global data", 
                       data_keys=list(current_data.keys()) if current_data else None,
                       has_caller_info="caller_name" in current_data)
        
        current_data.update({
            "agent_type": "sales",
            "specialist_start": datetime.now().isoformat()
        })
        
        # Update agent path
        agent_path = current_data.get("agent_path", [])
        if "sales" not in agent_path:
            agent_path.append("sales")
            current_data["agent_path"] = agent_path
        
        self.set_global_data(current_data)
        
        # Verify configuration
        verification_data = self.get_global_data()
        self.debug_print("Sales agent configuration complete", 
                       final_data_keys=list(verification_data.keys()) if verification_data else None,
                       agent_path=verification_data.get("agent_path"),
                       caller_name=verification_data.get("caller_name"))
    
    def debug_print(self, message: str, **kwargs):
        """Enhanced debug output for Sales Agent (always enabled)"""
        debug_msg = format_debug_message(self.__class__.__name__, message, **kwargs)
        print(debug_msg)
        # Also log to structured logger
        self.log.debug(message.replace(" ", "_").lower(), **kwargs)
    
    @AgentBase.tool(
        name="create_repair_recommendation",
        description="Create personalized phone repair recommendations for customer needs",
        parameters={
            "device_info": {"type": "string", "description": "Customer's device make, model, and condition"},
            "repair_needs": {"type": "string", "description": "Specific repair requirements or issues"},
            "budget": {"type": "string", "description": "Budget range if mentioned"}
        }
    )
    def create_repair_recommendation(self, args, raw_data):
        """Generate personalized repair service recommendations"""
        device_info = args.get("device_info", "")
        repair_needs = args.get("repair_needs", "")
        budget = args.get("budget", "")
        
        # Get caller context
        global_data = self.get_global_data()
        caller_name = global_data.get("caller_name", "")
        
        # Store recommendation details
        recommendation_data = {
            "device_info": device_info,
            "repair_needs": repair_needs,
            "budget": budget,
            "recommendation_created": datetime.now().isoformat()
        }
        
        response = f"Based on your {device_info} device condition, here are my ACME repair service recommendations:\n\n"
        response += "[Specific repair services and pricing would be provided here based on current service catalog]\n\n"
        response += f"These services address the repair needs you mentioned: {repair_needs}"
        
        if budget:
            response += f"\n\nThis recommendation fits within your {budget} budget range."
        
        return (
            SwaigFunctionResult(response)
            .update_global_data({"last_recommendation": recommendation_data})
        )
    
    @AgentBase.tool(
        name="check_repair_feasibility",
        description="Check repair feasibility and cost-effectiveness for customer's device",
        parameters={
            "device_model": {"type": "string", "description": "Device model and age to check"},
            "damage_details": {"type": "string", "description": "Specific damage or issues described"}
        }
    )
    def check_repair_feasibility(self, args, raw_data):
        """Verify repair feasibility for customer's device"""
        device_model = args.get("device_model", "")
        damage_details = args.get("damage_details", "")
        
        feasibility_data = {
            "device_checked": device_model,
            "damage_assessed": damage_details,
            "check_time": datetime.now().isoformat()
        }
        
        response = f"Repair feasibility analysis for device: {device_model}\n\n"
        response += f"For the issues described: {damage_details}\n\n"
        response += "[Detailed feasibility analysis would include:]"
        response += "\n• Parts availability and cost"
        response += "\n• Repair complexity and time requirements"  
        response += "\n• Cost-effectiveness vs device replacement"
        response += "\n• Warranty coverage and service guarantees"
        
        return (
            SwaigFunctionResult(response)
            .update_global_data({"last_feasibility_check": feasibility_data})
        )


class ACMESupportAgent(AgentBase):
    """
    ACME Corp Technical Support Specialist Agent
    
    Specialized agent for technical support, troubleshooting,
    and warranty services for existing ACME widgets.
    """
    
    def __init__(self):
        super().__init__(
            name="ACME Support Agent",
            route="/support",
            host="0.0.0.0",
            port=3001,
            auto_answer=True,
            use_pom=True,  # Enable Prompt Object Model
            basic_auth=("", "")
        )
        
        # Set a distinct voice for support with proper configuration
        self.add_language({
            "name": "English",
            "code": "en-US",
            "voice": "sally",
            "rate": 1.0,
            "pitch": 1.0
        })
        
        # Set debug parameters after initialization (always enabled)
        debug_params = get_debug_params()
        self.set_params(debug_params)
        
        # Monkey-patch to disable all auth for this demo so it can be
        # easily tested without credentials.  Production deployments
        # should implement proper authentication.
        def _no_auth(self, *a, **k):
            return True

        self._check_basic_auth = _no_auth.__get__(self, self.__class__)
        
        # Add native vector search for ACME support knowledge
        self.add_skill("native_vector_search", {
            "tool_name": "search_support_knowledge",
            "description": "Search ACME technical support and troubleshooting information",
            "index_file": "acme_support_knowledge.swsearch",
            "count": 3
        })
        
        self._setup_personality()
        
        # Set post-prompt for support conversation analysis
        self.set_post_prompt("""
        Analyze this support conversation and provide a summary including:
        1. Customer's name and device/issue details
        2. Diagnostic steps performed
        3. Support tickets created
        4. Technical solutions provided
        5. Issue resolution status
        
        Format as JSON for easy processing.
        """)
        
        # Set post-prompt URL for debugging and monitoring
        self.set_post_prompt_url("https://webhook.site/afef5994-294f-4916-b3d6-51bfe27d04a6")
        
        self.set_dynamic_config_callback(self.configure_support_agent)
    
    def _setup_personality(self):
        """Configure support specialist personality using POM"""
        
        self.prompt_add_section(
            "Personality",
            body="You are a patient, knowledgeable technical support specialist for ACME Corp, expert in phone diagnostics and repair guidance. You have a calm, reassuring voice that helps customers feel confident their issues will be resolved."
        )
        
        self.prompt_add_section(
            "Goal",
            body="Diagnose and resolve technical issues with customer devices, provide repair status updates, and create support tickets when needed."
        )
        
        self.prompt_add_section(
            "Instructions",
            bullets=[
                "Welcome the caller warmly and acknowledge you have their information from reception",
                "Reference their specific issue (available in global_data.details) in your greeting",
                "Use caller context from global_data (${global_data.caller_name}, ${global_data.details})",
                "Ask detailed questions about their device issues and symptoms",
                "Search the support knowledge base for diagnostic procedures",
                "Provide step-by-step troubleshooting and repair guidance",
                "Create support tickets for complex repairs requiring escalation"
            ]
        )
        
        self.prompt_add_section(
            "Initial Greeting",
            body="Start your conversation by saying: 'Hello ${global_data.caller_name}, I'm your ACME Corp technical support specialist. I understand you're experiencing an issue with ${global_data.details}. I'm here to help diagnose and resolve this problem.'"
        )
        
        self.prompt_add_section(
            "Context Available",
            body="Caller information: ${global_data.caller_name}, ${global_data.inquiry_type}, ${global_data.details}, ${global_data.agent_path}"
        )
    
    def configure_support_agent(self, query_params, body_params, headers, agent):
        """Configure support agent with caller context"""
        self.debug_print("Configuring support agent", 
                       query_params=query_params,
                       body_params=body_params)
        
        current_data = self.get_global_data() or {}
        self.debug_print("Support agent initial global data", 
                       data_keys=list(current_data.keys()) if current_data else None,
                       has_caller_info="caller_name" in current_data)
        
        current_data.update({
            "agent_type": "support",
            "specialist_start": datetime.now().isoformat()
        })
        
        # Update agent path
        agent_path = current_data.get("agent_path", [])
        if "support" not in agent_path:
            agent_path.append("support")
            current_data["agent_path"] = agent_path
        
        self.set_global_data(current_data)
        
        # Verify configuration
        verification_data = self.get_global_data()
        self.debug_print("Support agent configuration complete", 
                       final_data_keys=list(verification_data.keys()) if verification_data else None,
                       agent_path=verification_data.get("agent_path"),
                       caller_name=verification_data.get("caller_name"))
    
    def debug_print(self, message: str, **kwargs):
        """Enhanced debug output for Support Agent (always enabled)"""
        debug_msg = format_debug_message(self.__class__.__name__, message, **kwargs)
        print(debug_msg)
        # Also log to structured logger
        self.log.debug(message.replace(" ", "_").lower(), **kwargs)
    
    @AgentBase.tool(
        name="diagnose_device_issue",
        description="Help diagnose phone device problems with step-by-step guidance",
        parameters={
            "issue_description": {"type": "string", "description": "Description of the device issue"},
            "device_model": {"type": "string", "description": "Phone device model if known"}
        }
    )
    def diagnose_device_issue(self, args, raw_data):
        """Provide diagnostic assistance for device issues"""
        issue_description = args.get("issue_description", "")
        device_model = args.get("device_model", "")
        
        # Get caller context
        global_data = self.get_global_data()
        caller_name = global_data.get("caller_name", "")
        
        # Store diagnostic session
        diagnostic_data = {
            "issue": issue_description,
            "device_model": device_model,
            "diagnostic_started": datetime.now().isoformat()
        }
        
        response = f"Let me help you diagnose the device issue, {caller_name}.\n\n"
        response += f"Issue described: '{issue_description}'\n"
        if device_model:
            response += f"Device model: {device_model}\n\n"
        
        response += "Here are the diagnostic steps I recommend:\n"
        response += "[Step-by-step diagnostic process would include:]"
        response += "\n1. Visual inspection of widget components"
        response += "\n2. Performance testing procedures"
        response += "\n3. Environmental factor checks"
        response += "\n4. Integration point verification"
        response += "\n\nPlease follow these steps and let me know what you find."
        
        return (
            SwaigFunctionResult(response)
            .update_global_data({"current_diagnostic": diagnostic_data})
        )
    
    @AgentBase.tool(
        name="create_support_ticket",
        description="Create support ticket for complex issues requiring escalation",
        parameters={
            "issue_summary": {"type": "string", "description": "Brief summary of the issue"},
            "priority": {"type": "string", "description": "Priority level: low, medium, high, urgent"}
        }
    )
    def create_support_ticket(self, args, raw_data):
        """Create and track support tickets"""
        issue_summary = args.get("issue_summary", "")
        priority = args.get("priority", "medium").lower()
        
        # Get caller context
        global_data = self.get_global_data()
        caller_name = global_data.get("caller_name", "Unknown")
        
        # Generate ticket ID
        ticket_id = f"ACME-SUP-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        
        # Store ticket information
        ticket_data = {
            "ticket_id": ticket_id,
            "caller_name": caller_name,
            "issue_summary": issue_summary,
            "priority": priority,
            "created": datetime.now().isoformat(),
            "status": "open"
        }
        
        response = f"I've created support ticket {ticket_id} for you.\n\n"
        response += f"Issue: {issue_summary}\n"
        response += f"Priority: {priority.title()}\n"
        response += f"Customer: {caller_name}\n\n"
        
        if priority in ["high", "urgent"]:
            response += "Due to the high priority, our technical team will contact you within 2 hours."
        else:
            response += "Our technical team will follow up within 24 hours."
        
        return (
            SwaigFunctionResult(response)
            .update_global_data({"support_ticket": ticket_data})
        )


def create_acme_service(host: str = "0.0.0.0", port: int = 3001, log_level: str = "info") -> AgentServer:
    """
    Create and configure the ACME Corp multi-agent service
    
    Enhanced version of the v1 receptionist with multi-agent capabilities.
    
    Args:
        host: Host to bind the server to
        port: Port to bind the server to  
        log_level: Logging level
    
    Returns:
        Configured AgentServer with all ACME agents registered
    """
    # Debug mode is always enabled
    debug_mode = True
    print("🔍 DEBUG MODE ALWAYS ENABLED")
    log_level = "debug"
    
    # Create the server
    server = AgentServer(host=host, port=port, log_level=log_level)
    
    # Create and register ACME agents
    receptionist = ACMEReceptionistAgent()
    sales = ACMESalesAgent()
    support = ACMESupportAgent()
    
    # Register agents with the server
    server.register(receptionist, "/")
    server.register(sales, "/sales")
    server.register(support, "/support")
    
    # Add info endpoint
    @server.app.get("/info")
    async def info():
        return {
            "message": "ACME Corp Multi-Agent Service - Enhanced Receptionist System",
            "version": "2.0.0",
            "company": "Acme Corp",
            "specialty": "Widgets for Roadrunners",
            "enhancement": "Multi-agent system built on v1 receptionist foundation",
            "debug_mode": debug_mode,
            "log_level": log_level,
            "agents": {
                "receptionist": {
                    "endpoint": "/",
                    "description": "Enhanced receptionist with intelligent routing (v1 upgrade)",
                    "features": ["Caller info capture", "Intelligent routing", "Context preservation"]
                },
                "sales": {
                    "endpoint": "/sales",
                    "description": "ACME widget sales and product specialist",
                    "features": ["Product recommendations", "Pricing", "Compatibility checks"]
                },
                "support": {
                    "endpoint": "/support",
                    "description": "Technical support for ACME widgets",
                    "features": ["Troubleshooting", "Diagnostics", "Ticket creation"]
                }
            }
        }
    
    # Add debug endpoint (always available)
    @server.app.get("/debug")
    async def debug_info():
        debug_params = get_debug_params()
        return {
            "debug_mode": True,
            "timestamp": datetime.now().isoformat(),
            "environment_vars": {
                "ACME_DEBUG": os.getenv("ACME_DEBUG"),
                "LOG_LEVEL": os.getenv("LOG_LEVEL"),
                "DEBUG_WEBHOOK_URL": os.getenv("DEBUG_WEBHOOK_URL", "Not configured"),
                "DEBUG_WEBHOOK_LEVEL": os.getenv("DEBUG_WEBHOOK_LEVEL", "1"),
                "VERBOSE_LOGS": os.getenv("VERBOSE_LOGS", "false"),
                "AUDIBLE_DEBUG": os.getenv("AUDIBLE_DEBUG", "false"),
                "AUDIBLE_LATENCY": os.getenv("AUDIBLE_LATENCY", "false"),
                "COMPANY_NAME": os.getenv("COMPANY_NAME", "Not set"),
                "COMPANY_SPECIALTY": os.getenv("COMPANY_SPECIALTY", "Not set")
            },
            "debug_params": debug_params,
            "agents_status": {
                "receptionist": "active",
                "sales": "active", 
                "support": "active"
            },
            "debug_features": {
                "webhook_debugging": debug_params.get("debug_webhook_url") is not None,
                "audible_debugging": debug_params.get("audible_debug", False),
                "latency_monitoring": debug_params.get("audible_latency", False),
                "verbose_logging": debug_params.get("verbose_logs", False),
                "performance_caching": debug_params.get("cache_mode", False),
                "usage_accounting": debug_params.get("enable_accounting", False)
            },
            "endpoints": [
                "GET /info - Service information",
                "GET /debug - Debug information (this endpoint)",
                "POST / - Receptionist agent",
                "POST /sales - Sales agent",
                "POST /support - Support agent"
            ]
        }
    
    return server


def lambda_handler(event, context):
    """AWS Lambda entry point"""
    server = create_acme_service()
    return server.run(event, context)


if __name__ == "__main__":
    logger.info("Starting ACME Corp Multi-Agent Service - Enhanced Receptionist System")
    logger.info("=" * 80)
    logger.info("🔍 DEBUG MODE ALWAYS ENABLED - Comprehensive monitoring active")
    logger.info("🏢 Enhanced version of ACME Corp v1 receptionist with multi-agent capabilities")
    logger.info("")
    logger.info("📞 Receptionist Agent: http://localhost:3001/")
    logger.info("   • Enhanced v1 receptionist with intelligent routing")
    logger.info("   • Captures caller info and routes to specialists")
    logger.info("   • Uses POM and global_data for secure context storage")
    logger.info("")
    logger.info("💼 Sales Agent: http://localhost:3001/sales")
    logger.info("   • ACME widget product recommendations")
    logger.info("   • Pricing and compatibility information")
    logger.info("   • Specialized roadrunner application expertise")
    logger.info("")
    logger.info("🔧 Support Agent: http://localhost:3001/support")
    logger.info("   • Technical troubleshooting for ACME widgets")
    logger.info("   • Diagnostic assistance and repair guidance")
    logger.info("   • Support ticket creation and tracking")
    logger.info("")
    logger.info("ℹ️  Service Info: http://localhost:3001/info")
    logger.info("🔍 Debug Info: http://localhost:3001/debug")
    logger.info("=" * 80)
    
    logger.info("✨ v2 Enhancements over v1:")
    logger.info("   ✅ Multi-agent architecture (receptionist + specialists)")
    logger.info("   ✅ Secure global_data context storage")
    logger.info("   ✅ Seamless agent transfers with context preservation")
    logger.info("   ✅ Native vector search for knowledge bases")
    logger.info("   ✅ POM-structured prompts for consistency")
    logger.info("   ✅ Enhanced ACME Corp branding and messaging")
    logger.info("   ✅ Always-on debugging and monitoring")
    logger.info("")
    logger.info("🔍 Debug Features Always Active:")
    logger.info("   ✅ Function entry/exit tracing")
    logger.info("   ✅ Global data state monitoring")
    logger.info("   ✅ Timestamped debug output")
    logger.info("   ✅ Structured logging")
    logger.info("   ✅ Performance monitoring")
    logger.info("   ✅ Audible debugging (if configured)")
    logger.info("")
    logger.info("🚀 Ready to serve ACME Corp customers with full debugging!")
    
    # Create and run the server
    server = create_acme_service()
    
    try:
        server.run()
    except KeyboardInterrupt:
        logger.info("Shutting down ACME Corp service...")
