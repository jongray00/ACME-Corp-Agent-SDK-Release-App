# Acme Corp Multi-Agent IVR Demo

This repository showcases three progressive versions of an AI-driven IVR system built with SignalWire Agents SDK. Each version demonstrates new capabilities, from basic agent creation to multi-agent coordination and external API integrations.

## Repository Structure

- **v1-sdk-basics** – Single receptionist agent introducing the SDK fundamentals.
- **v2-multi-agent-flow** – Expanded demo with receptionist, sales, and support agents working together.
- **v3-plugging-in-external-apis** – Placeholder for examples integrating additional APIs.

## Overview
This project implements a three-agent AI-powered IVR system for Acme Corp, designed to automate and enhance customer interaction flows. The agents each perform distinct roles and pass contextual information between one another to deliver a seamless caller experience.

### Goals
- Build a multi-agent IVR demo capable of handling real-time routing, context transfer, and automated actions.
- Provide support, sales, and reception functionality via AI agents.
- Complete demo implementation by June 17, 2025, or earlier to allow time for video iteration.

### Architecture and Agent Roles
1. **Receptionist Agent (Agent 1)** – Greets callers, captures intent, and routes to support or sales.
2. **Support Agent (Agent 2)** – Answers questions using search or internal knowledge bases and can open tickets.
3. **Sales Agent (Agent 3)** – Delivers product information, handles purchases, and greets the caller using gathered context.

Context is preserved and passed between agents to maintain a natural conversation flow. Calls are routed through SignalWire Fusion/FreeSWITCH, using the call SID to collate the full conversation thread.

### Getting Started
Each version contains its own README with setup instructions. Start with the **v1-sdk-basics** folder to learn how to build a simple SignalWire agent, then explore **v2-multi-agent-flow** to see multiple agents working together. The **v3-plugging-in-external-apis** folder will illustrate extending agents with outside services.

## License
This project is provided for demo purposes by Acme Corp. See individual folders for additional details.
