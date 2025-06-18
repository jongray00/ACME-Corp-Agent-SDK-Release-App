# ACME Corp Multi-Agent Service - Debug Guide

This guide covers all available debugging and logging methods for the ACME Corp v2 multi-agent service, including SignalWire AI debugging features.

**🔍 DEBUG MODE IS ALWAYS ENABLED** - This service runs with comprehensive debugging active by default for optimal troubleshooting and monitoring.

## 🔍 Debug Methods Available

### 1. **Always-On Debug Mode**

Debug mode is permanently enabled with sensible defaults. You can customize the level of debugging by setting environment variables:

```bash
# Optional: Customize debug behavior (defaults shown)
export DEBUG_WEBHOOK_LEVEL=2  # 0=disabled, 1=basic, 2=verbose
export VERBOSE_LOGS=true      # Detailed logging (default: enabled)
export AUDIBLE_DEBUG=true     # AI announces function execution (default: enabled)
export AUDIBLE_LATENCY=true   # AI announces latency info (default: enabled)

# Optional: Debug webhook for real-time monitoring
export DEBUG_WEBHOOK_URL="https://your-webhook-url/debug"

# Run the service (debug always active)
./run_acme_service.sh

# Or use enhanced debug runner for additional output
./debug_run.sh
```

### 2. **Built-in Structured Logging**

Every agent has access to structured logging via `self.log` (always active):

```python
# Debug level - detailed information (always enabled)
self.log.debug("function_called", args=args, timestamp=datetime.now())

# Info level - general information  
self.log.info("caller_captured", caller="John", inquiry="support")

# Warning level - potential issues
self.log.warning("transfer_url_missing", specialist="sales")

# Error level - actual errors
self.log.error("function_failed", error=str(e), function="save_caller_info")
```

### 3. **Enhanced Console Debug Output**

Timestamped console output with visual markers (always active):

```python
# Using the built-in debug_print helper (always enabled)
self.debug_print("Transfer request received", 
                args=args, 
                specialist_type="sales")

# Manual debug prints are also enhanced
print(f"🔍 DEBUG - Caller Info Captured:")
print(f"   Name: {caller_name}")
print(f"   Type: {inquiry_type}")
```

### 4. **SignalWire AI Debug Features**

The following SignalWire AI debugging features are automatically configured:

- **Debug Webhook**: Real-time interaction logging to external webhook (if configured)
- **Audible Debug**: AI announces function execution during calls (default: enabled)
- **Audible Latency**: AI announces latency information for performance monitoring (default: enabled)
- **Verbose Logs**: Detailed logging for all AI operations (default: enabled)
- **Performance Caching**: Enables response caching for repeated queries (always enabled)
- **Usage Accounting**: Tracks usage for billing and analytics (always enabled)

### 5. **Debug Endpoints**

Debug endpoints are always available:

- **GET /debug** - Comprehensive debug information and environment status
- **GET /info** - Service information (always available)

```bash
# Check debug status with all parameters (always available)
curl http://localhost:3001/debug

# Check service info
curl http://localhost:3001/info
```

## 🛠️ Available Debugging Features

### Function Call Tracing

All SWAIG functions now include detailed tracing with entry/exit logging:

```python
## 📋 Debug Output Examples

### Console Debug Output

When debug mode is enabled, you'll see enhanced console output like this:

```
🔍 DEBUG [2024-01-15 14:30:25.123] ACMEReceptionistAgent: Entering function: save_caller_info
   args: {'caller_name': 'John Smith', 'inquiry_type': 'support', 'details': 'Phone screen cracked'}
   raw_data_present: True

🔍 DEBUG [2024-01-15 14:30:25.145] ACMEReceptionistAgent: Caller Info Captured
   name: John Smith
   inquiry_type: support
   details: Phone screen cracked

🔍 DEBUG [2024-01-15 14:30:25.167] ACMEReceptionistAgent: Global Data Updated
   caller_name: John Smith
   inquiry_type: support
   details: Phone screen cracked
   reception_completed: True
   agent_path: ['receptionist']
   timestamp: 2024-01-15T14:30:25.167890

🔍 DEBUG [2024-01-15 14:30:25.189] ACMEReceptionistAgent: Exiting function: save_caller_info
   result: <signalwire_agents.core.function_result.SwaigFunctionResult object>
```

### Debug Endpoint Response

The `/debug` endpoint provides comprehensive debugging information:

```json
{
  "debug_mode": true,
  "timestamp": "2024-01-15T14:30:25.123456",
  "environment_vars": {
    "ACME_DEBUG": "true",
    "LOG_LEVEL": "DEBUG",
    "DEBUG_WEBHOOK_URL": "Not configured",
    "DEBUG_WEBHOOK_LEVEL": "2",
    "VERBOSE_LOGS": "true",
    "AUDIBLE_DEBUG": "true",
    "AUDIBLE_LATENCY": "true"
  },
  "debug_params": {
    "debug_webhook_url": null,
    "debug_webhook_level": 2,
    "verbose_logs": true,
    "audible_debug": true,
    "audible_latency": true,
    "cache_mode": true,
    "enable_accounting": true
  },
  "debug_features": {
    "webhook_debugging": false,
    "audible_debugging": true,
    "latency_monitoring": true,
    "verbose_logging": true,
    "performance_caching": true,
    "usage_accounting": true
  }
}
```

## 🔧 Troubleshooting

### Common Debug Scenarios

1. **Function Not Being Called**
   - Check function registration with `@self.tool()` decorator
   - Verify function parameters match AI expectations
   - Look for entry/exit logs to confirm function execution

2. **Transfer Issues**
   - Check global data for transfer URLs
   - Verify agent routing configuration
   - Look for transfer request debug logs

3. **Context Loss Between Agents**
   - Check global data updates in debug output
   - Verify agent path tracking
   - Confirm context preservation in transfers

### Debug Log Levels

- **DEBUG**: Detailed function tracing and parameter logging
- **INFO**: General operation information and caller details
- **WARNING**: Potential issues and missing configurations
- **ERROR**: Actual errors and function failures

## 🚀 Performance Monitoring

When debug mode is enabled, the following performance features are active:

- **Response Caching**: Improves performance for repeated queries
- **Usage Accounting**: Tracks API usage and costs
- **Latency Monitoring**: Measures and reports response times
- **Function Timing**: Tracks SWAIG function execution times

# Before function execution
self.debug_print("Transfer request received", 
               args=args, 
               raw_data_present=raw_data is not None)

# During function execution
self.debug_print("Global data retrieved", 
               global_data_keys=list(global_data.keys()),
               specialist_type=specialist_type)
```

### Global Data Inspection

Monitor global data flow between agents:

```python
global_data = self.get_global_data()
self.debug_print("Global data retrieved", 
               global_data_keys=list(global_data.keys()) if global_data else None)
```

### Enhanced Error Messages

Detailed error information with context:

```python
try:
    # Some operation
    pass
except Exception as e:
    self.log.error("operation_failed", 
                  error=str(e), 
                  function="function_name",
                  args=args)
```

## 📊 Log Levels and Output

### Log Levels (in order of verbosity)

1. **DEBUG** - Most verbose, shows all internal operations
2. **INFO** - General operational information  
3. **WARNING** - Potential issues or unusual conditions
4. **ERROR** - Actual errors that need attention
5. **CRITICAL** - Critical errors that may stop the service

### Setting Log Levels

```bash
# Environment variable
export LOG_LEVEL=DEBUG

# Or in code
server = create_acme_service(log_level="debug")
```

## 🚀 Quick Debug Session

To start a debug session:

1. **Enable debug mode:**
   ```bash
   ./debug_run.sh
   ```

2. **Watch the console output** for 🔍 DEBUG markers

3. **Check debug endpoint:**
   ```bash
   curl http://localhost:3001/debug | jq
   ```

4. **Monitor function calls** as they happen in real-time

## 📋 Debug Checklist

When troubleshooting issues:

- [ ] Check if debug mode is enabled (`ACME_DEBUG=true`)
- [ ] Verify log level is set appropriately (`LOG_LEVEL=DEBUG`)
- [ ] Monitor console output for 🔍 DEBUG markers
- [ ] Check the `/debug` endpoint for environment status
- [ ] Review structured logs for detailed function traces
- [ ] Verify global data flow between agents
- [ ] Check authentication bypass is working (no auth credentials generated)

## 🔧 Advanced Debugging

### Custom Debug Functions

Add your own debug functions to any agent:

```python
def debug_print(self, message: str, **kwargs):
    """Helper method for consistent debug output"""
    print(f"🔍 DEBUG [{self.__class__.__name__}]: {message}")
    if kwargs:
        for key, value in kwargs.items():
            print(f"   {key}: {value}")
    # Also log to structured logger
    self.log.debug(message.replace(" ", "_").lower(), **kwargs)
```

### Environment Variables for Debugging

```bash
# Core debug settings
ACME_DEBUG=true              # Enable debug mode
LOG_LEVEL=DEBUG              # Set log verbosity

# Service configuration  
COMPANY_NAME="Acme Corp"     # Company name
COMPANY_SPECIALTY="Phone Repair"  # Company specialty

# Disable logging completely (if needed)
SIGNALWIRE_LOG_MODE=off
```

This comprehensive debugging system provides visibility into every aspect of the multi-agent service operation. 