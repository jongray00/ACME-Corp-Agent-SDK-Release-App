# Acme Corp IVR - Version 1: Basic AI Agent

This is the first version of the Acme Corp IVR system, implementing a simple AI receptionist agent using the SignalWire SDK.

## Overview

Version 1 demonstrates the fundamentals of creating an AI agent with SignalWire:
- Basic agent setup and configuration
- Simple greeting and interaction flow
- Connection to SignalWire platform
- Environment-based configuration

## Features

- **AI Receptionist**: Greets callers with personalized messaging
- **Name Collection**: Captures caller's name and uses it in conversation
- **Company Introduction**: Introduces Acme Corp and its specialties
- **Basic Intent Recognition**: Simple keyword-based intent detection
- **Professional Personality**: Warm and efficient AI receptionist persona

## Project Structure

```
v1_ai_agent_sdk/
├── README.md              # This file
├── requirements.txt       # Python dependencies
├── env.example           # Environment variables template
├── .env                  # Your local environment (not committed)
├── receptionist.py       # Main receptionist agent
└── run_server.py         # Server runner
```

## Prerequisites

- Python 3.8 or higher
- SignalWire accountc (SignalWire Space URL and authentication tokens)

## Installation

1. Clone or download this folder
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Copy `env.example` to `.env` and fill in your SignalWire credentials:
   ```bash
   cp env.example .env
   ```

5. Edit `.env` with your SignalWire details

## Configuration

Edit the `.env` file with your SignalWire credentials:

```env
# SignalWire Configuration
SIGNALWIRE_SPACE_URL=your-space.signalwire.com
SIGNALWIRE_PROJECT_KEY=your-project-key
SIGNALWIRE_TOKEN=your-auth-token

# Agent Configuration
AGENT_HOST=0.0.0.0
AGENT_PORT=3000
AGENT_ROUTE=/receptionist

# Company Configuration
COMPANY_NAME=Acme Corp
COMPANY_SPECIALTY=Widgets for Roadrunners
COMPANY_PHONE=+1-555-ACME-CORP
```

## Running the Agent

1. Start the agent server:
   ```bash
   python run_server.py
   ```

2. The agent will be available at `http://localhost:3000/receptionist`

3. Configure your SignalWire phone number to point to your agent endpoint

## Testing

You can test the agent using the SignalWire CLI:

```bash
# List available functions
swaig-test receptionist.py --list-tools

# Test the greeting function
swaig-test receptionist.py --exec greet_caller --param "John Doe"

# Dump SWML configuration
swaig-test receptionist.py --dump-swml
```

## How It Works

1. **Agent Initialization**: The receptionist agent is created with SignalWire SDK
2. **Personality Setup**: Uses Prompt Object Model (POM) to define agent behavior
3. **Function Registration**: Defines SWAIG functions for interaction
4. **Call Handling**: Processes incoming calls with greeting and name collection
5. **Intent Detection**: Basic keyword matching to understand caller needs

## Key Components

### Receptionist Agent (`receptionist.py`)
- Main agent class extending `AgentBase`
- Personality configuration using POM
- SWAIG function definitions
- Basic intent classification

### Server Runner (`run_server.py`)
- Starts the HTTP server
- Loads environment configuration
- Initializes and runs the agent

## Next Steps

In Version 2, we'll extend this to:
- Add multiple agents (support and sales)
- Implement context transfer between agents
- Create agent routing logic
- Enhance intent classification

## Troubleshooting

- **Connection Issues**: Verify your SignalWire credentials in `.env`
- **Port Conflicts**: Change `AGENT_PORT` if 3000 is already in use
- **Import Errors**: Ensure all dependencies are installed via `pip install -r requirements.txt`

## Support

For questions about SignalWire AI Agents:
- [SignalWire AI Documentation](https://developer.signalwire.com/ai)
- [SignalWire Community Forum](https://signalwire.community)
- [SignalWire Discord](https://discord.gg/signalwire) 