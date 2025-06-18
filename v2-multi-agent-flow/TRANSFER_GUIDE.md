# SignalWire Transfer Functionality Guide

## Overview

The SignalWire AI Agent SDK supports multiple types of call transfers, allowing you to route calls to various destinations including other AI agents, PSTN numbers, and SIP/Call Fabric addresses.

## Transfer Destination Types

### 1. **HTTP/Webhook URLs** (Agent-to-Agent)
Transfer to another AI agent running on a web server.

```python
# Current implementation in v2-multi-agent-flow
result.swml_transfer(
    dest="http://localhost:3001/sales",
    ai_response="You're back with reception if needed."
)
```

**Use Cases:**
- Routing between specialized AI agents
- Maintaining conversation context across transfers
- Building multi-agent workflows

### 2. **PSTN Numbers** (Traditional Phone Lines)
Transfer to regular phone numbers.

```python
# Transfer to phone number
result.connect("+15551234567", final=True)  # Permanent transfer
result.connect("+18005551212", final=False) # Returns if far end hangs up

# With caller ID override
result.connect("+15551234567", final=True, from_addr="+15559876543")
```

**Use Cases:**
- Escalating to human agents
- Routing to external call centers
- Connecting to third-party services

### 3. **SIP/Call Fabric Addresses**
Transfer to SIP endpoints or SignalWire Call Fabric addresses.

```python
# Transfer to SIP address
result.connect("sales@company.com", final=True)
result.connect("support@acme.sw.com", final=False)

# Using swml_transfer for temporary transfers
result.swml_transfer(
    dest="supervisor@company.sw.com",
    ai_response="Welcome back. How else can I help?"
)
```

**Use Cases:**
- Internal VoIP systems
- SignalWire Call Fabric routing
- Cloud-based contact centers

## Transfer Methods Comparison

| Method | Purpose | Return Capability | Best For |
|--------|---------|-------------------|----------|
| `connect()` | Direct transfer | `final` parameter controls | PSTN, SIP, permanent transfers |
| `swml_transfer()` | SWML-based transfer | Built-in return handling | Agent-to-agent, temporary transfers |
| `sip_refer()` | SIP REFER transfer | No | Advanced SIP scenarios |

## Implementation Examples

### Basic PSTN Transfer
```python
@self.tool(
    name="transfer_to_support_line",
    description="Transfer to human support",
    parameters={
        "urgent": {"type": "boolean", "description": "Is this urgent?"}
    }
)
def transfer_to_support_line(self, args, raw_data):
    urgent = args.get("urgent", False)
    
    if urgent:
        number = "+15555550911"  # Urgent support line
    else:
        number = "+15555551234"  # Regular support
    
    return (
        SwaigFunctionResult("Transferring you to our support team.")
        .connect(number, final=True)
    )
```

### Intelligent SIP Routing
```python
@self.tool(
    name="route_to_specialist",
    description="Route to appropriate specialist",
    parameters={
        "specialty": {"type": "string", "description": "Type of specialist needed"}
    }
)
def route_to_specialist(self, args, raw_data):
    specialty = args.get("specialty", "general")
    
    # SIP routing map
    specialists = {
        "technical": "tech@support.acme.com",
        "billing": "billing@finance.acme.com",
        "sales": "sales@revenue.acme.com",
        "general": "agent@support.acme.com"
    }
    
    sip_address = specialists.get(specialty, specialists["general"])
    
    # Non-final transfer - returns if specialist unavailable
    return (
        SwaigFunctionResult(f"Connecting you to our {specialty} specialist.")
        .connect(sip_address, final=False)
    )
```

### Multi-Destination Transfer Logic
```python
@self.tool(
    name="smart_transfer",
    description="Intelligently route based on availability",
    parameters={
        "department": {"type": "string", "description": "Target department"}
    }
)
def smart_transfer(self, args, raw_data):
    department = args.get("department", "").lower()
    
    # Priority order: AI Agent → SIP → PSTN
    routing_map = {
        "sales": {
            "agent_url": "https://api.acme.com/sales-agent",
            "sip": "sales@acme.sw.com",
            "pstn": "+15555551234"
        },
        "support": {
            "agent_url": "https://api.acme.com/support-agent",
            "sip": "support@acme.sw.com", 
            "pstn": "+15555555678"
        }
    }
    
    if department not in routing_map:
        return SwaigFunctionResult("I'm not sure which department you need.")
    
    routes = routing_map[department]
    
    # Try AI agent first (non-blocking check could be added)
    if routes.get("agent_url"):
        return (
            SwaigFunctionResult(f"Connecting you to our {department} AI specialist.")
            .swml_transfer(
                dest=routes["agent_url"],
                ai_response="Welcome back. How else can I assist?"
            )
        )
    
    # Fallback to SIP
    elif routes.get("sip"):
        return (
            SwaigFunctionResult(f"Routing you to {department}.")
            .connect(routes["sip"], final=False)
        )
    
    # Final fallback to PSTN
    else:
        return (
            SwaigFunctionResult(f"Transferring to {department}.")
            .connect(routes["pstn"], final=True)
        )
```

## Best Practices

### 1. **Choose the Right Transfer Type**
- **Agent-to-Agent**: Use HTTP URLs with `swml_transfer()`
- **Human Agents**: Use PSTN numbers with `connect()`
- **Internal Systems**: Use SIP addresses

### 2. **Handle Transfer Failures**
```python
# Always provide context before transfer
result = SwaigFunctionResult("Let me transfer you to our specialist.")

# Add error handling in your prompts
self.prompt_add_section(
    "Transfer Failures",
    body="If a transfer fails, apologize and offer alternatives."
)
```

### 3. **Preserve Context**
```python
# Store context before transfer
result.update_global_data({
    "transfer_reason": "billing inquiry",
    "previous_agent": "receptionist",
    "customer_sentiment": "frustrated"
})
```

### 4. **Set Appropriate Return Behavior**
- Use `final=True` when escalating to human agents
- Use `final=False` for specialist consultations
- Use `swml_transfer()` for agent-to-agent with return

### 5. **Provide Clear Expectations**
```python
# Be specific about what's happening
"Transferring you to our billing department. This will take about 10 seconds."

# vs vague
"Transferring you now."
```

## Configuration Requirements

### For PSTN Transfers
- Valid SignalWire phone number for outbound calls
- Proper billing configuration
- Optional: Custom caller ID setup

### For SIP/Call Fabric
- SIP domain configuration
- Proper authentication if required
- Network connectivity to SIP endpoints

### For Agent-to-Agent
- Accessible HTTP endpoints
- Proper authentication between agents
- Shared context storage (global_data)

## Troubleshooting

### Common Issues

1. **Transfer fails immediately**
   - Check destination format
   - Verify network connectivity
   - Ensure proper authentication

2. **Context not preserved**
   - Confirm global_data is set before transfer
   - Verify receiving agent reads global_data

3. **Call doesn't return**
   - Check `final` parameter setting
   - Verify `ai_response` is set for returns

4. **Audio issues after transfer**
   - Check codec compatibility
   - Verify network quality
   - Test with different destination types

## Testing Transfers

### Test Commands
```bash
# Test PSTN transfer
curl -X POST http://localhost:3001/swaig \
  -H "Content-Type: application/json" \
  -d '{
    "function": "transfer_to_phone",
    "argument": {
      "parsed": ["department", "phone_number"],
      "department": "sales",
      "phone_number": "+15551234567"
    }
  }'

# Test SIP transfer
curl -X POST http://localhost:3001/swaig \
  -H "Content-Type: application/json" \
  -d '{
    "function": "transfer_to_sip",
    "argument": {
      "parsed": ["sip_address", "return_on_hangup"],
      "sip_address": "sales@company.com",
      "return_on_hangup": false
    }
  }'
```

## Summary

The SignalWire transfer functionality is flexible and supports multiple destination types:

- **Current Implementation**: HTTP/webhook transfers between AI agents
- **PSTN Support**: Transfer to any phone number worldwide
- **SIP/Call Fabric**: Integration with VoIP and cloud systems

Choose the appropriate transfer method based on your use case, and always consider the user experience when designing transfer flows. 