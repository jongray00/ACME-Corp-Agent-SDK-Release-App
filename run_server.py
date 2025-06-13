#!/usr/bin/env python3
"""Run the Acme Corp Receptionist Agent Server - Version 1

This small wrapper script loads configuration and exposes the
``ReceptionistAgent`` over HTTP.  It mirrors the examples provided in
the Agents SDK documentation.
"""

import os
import sys
import signal
from dotenv import load_dotenv
import structlog
from receptionist import agent

# Load environment variables from the `.env` file so the same script
# can be used in different environments without modification.
load_dotenv()

# Configure structured logging for easier debugging and tracing
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

# Obtain the root logger used throughout this example
logger = structlog.get_logger()

def signal_handler(sig, frame):
    """Handle shutdown signals gracefully."""
    # Log the signal and exit so containers or systemd can stop the service
    logger.info("shutdown_signal_received", signal=sig)
    sys.exit(0)


def validate_environment():
    """Validate required environment variables are set.

    Following the Agents SDK docs, this helper stops the server from
    starting if the key SignalWire credentials are missing.
    """
    required_vars = [
        "SIGNALWIRE_SPACE_URL",
        "SIGNALWIRE_PROJECT_KEY", 
        "SIGNALWIRE_TOKEN"
    ]
    
    missing_vars = []
    for var in required_vars:
        # Check each required variable and record any that are missing
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
    # Start the HTTP server and block until it is stopped.  The agent
    # itself listens for inbound requests on the host/port defined in
    # the environment variables.
    print("Starting Acme Corp Receptionist Agent v1 (no auth)...")
    agent.serve()


if __name__ == "__main__":
    main() 
