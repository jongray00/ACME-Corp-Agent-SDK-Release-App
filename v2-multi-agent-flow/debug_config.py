"""
Debug configuration and utilities for ACME Corp Multi-Agent Service
Debug mode is always enabled for comprehensive monitoring and troubleshooting.
"""

import os
from datetime import datetime
from typing import Any, Dict, Optional

# Debug configuration with sensible defaults for always-on debug mode
DEBUG_WEBHOOK_URL = os.getenv("DEBUG_WEBHOOK_URL")
DEBUG_WEBHOOK_LEVEL = int(os.getenv("DEBUG_WEBHOOK_LEVEL", "2"))  # Default to verbose
VERBOSE_LOGS = os.getenv("VERBOSE_LOGS", "true").lower() == "true"  # Default to enabled
AUDIBLE_DEBUG = os.getenv("AUDIBLE_DEBUG", "true").lower() == "true"  # Default to enabled
AUDIBLE_LATENCY = os.getenv("AUDIBLE_LATENCY", "false").lower() == "true"  # Default to disabled

def get_debug_params() -> Dict[str, Any]:
    """Get debug parameters for AI agent configuration (always enabled)"""
    params = {
        "verbose_logs": VERBOSE_LOGS,
        "audible_debug": AUDIBLE_DEBUG,
        "audible_latency": AUDIBLE_LATENCY,
        "cache_mode": True,  # Enable caching for better performance
        "enable_accounting": True  # Track usage for analytics
    }
    
    # Only add webhook params if URL is configured
    if DEBUG_WEBHOOK_URL:
        params.update({
            "debug_webhook_url": DEBUG_WEBHOOK_URL,
            "debug_webhook_level": DEBUG_WEBHOOK_LEVEL
        })
    
    return params

def format_debug_message(agent_name: str, message: str, **kwargs) -> str:
    """Format debug message with consistent styling"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    debug_msg = f"🔍 DEBUG [{timestamp}] {agent_name}: {message}"
    
    if kwargs:
        for key, value in kwargs.items():
            debug_msg += f"\n   {key}: {value}"
    
    return debug_msg

def log_function_entry(agent_name: str, func_name: str, **kwargs) -> None:
    """Log function entry with parameters"""
    msg = format_debug_message(
        agent_name,
        f"Entering function: {func_name}",
        **kwargs
    )
    print(msg)

def log_function_exit(agent_name: str, func_name: str, result: Optional[Any] = None) -> None:
    """Log function exit with result"""
    kwargs = {"result": str(result)} if result else {}
    msg = format_debug_message(
        agent_name,
        f"Exiting function: {func_name}",
        **kwargs
    )
    print(msg)

def debug_print_global_data(agent_name: str, global_data: Dict[str, Any]) -> None:
    """Print global data in a structured format"""
    msg = format_debug_message(
        agent_name,
        "Global Data State:",
        **{k: str(v) for k, v in global_data.items()}
    )
    print(msg) 