#!/usr/bin/env python3
"""
Run the Acme Corp Receptionist Agent Server - Version 1

This script starts the HTTP server for the receptionist agent,
making it available to receive calls from SignalWire.
"""

import os
import sys
import signal
from dotenv import load_dotenv
import structlog
from receptionist import agent

# Load environment variables
load_dotenv()

# Configure structured logging
log_level = os.getenv("LOG_LEVEL", "INFO")
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.dev.ConsoleRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()

def signal_handler(sig, frame):
    """Handle shutdown signals gracefully."""
    logger.info("shutdown_signal_received", signal=sig)
    sys.exit(0)


def validate_environment():
    """Validate required environment variables are set."""
    required_vars = [
        "SIGNALWIRE_SPACE_URL",
        "SIGNALWIRE_PROJECT_KEY", 
        "SIGNALWIRE_TOKEN"
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        logger.error("missing_required_environment_variables", 
                    missing=missing_vars)
        print("\n⚠️  Missing required environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\nPlease copy env.example to .env and fill in your SignalWire credentials.")
        return False
    
    return True


def main():
    print("Starting Acme Corp Receptionist Agent v1 (no auth)...")
    agent.serve()


if __name__ == "__main__":
    main() 