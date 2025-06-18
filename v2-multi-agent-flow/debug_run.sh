#!/bin/bash

echo "🔍 ACME Corp Debug Mode Runner"
echo "================================"
echo ""
echo "This script runs the ACME service with enhanced debugging enabled."
echo ""

# Enable debug mode and configure debug settings
export ACME_DEBUG=true
export LOG_LEVEL=DEBUG
export DEBUG_WEBHOOK_LEVEL=2  # Verbose debug info
export VERBOSE_LOGS=true
export AUDIBLE_DEBUG=true
export AUDIBLE_LATENCY=true

# Optional: Configure debug webhook if needed
# export DEBUG_WEBHOOK_URL="https://your-webhook-url/debug"

# Show environment
echo "Environment Variables:"
echo "  ACME_DEBUG: $ACME_DEBUG"
echo "  LOG_LEVEL: $LOG_LEVEL"
echo "  DEBUG_WEBHOOK_LEVEL: $DEBUG_WEBHOOK_LEVEL"
echo "  VERBOSE_LOGS: $VERBOSE_LOGS"
echo "  AUDIBLE_DEBUG: $AUDIBLE_DEBUG"
echo "  AUDIBLE_LATENCY: $AUDIBLE_LATENCY"
echo "  DEBUG_WEBHOOK_URL: ${DEBUG_WEBHOOK_URL:-Not configured}"
echo ""

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    echo "🔧 Activating virtual environment..."
    source venv/bin/activate
fi

echo "🎯 Starting ACME Corp service in DEBUG MODE..."
echo ""
echo "Debug features enabled:"
echo "  ✅ Enhanced console output with timestamps"
echo "  ✅ Structured logging with debug level"
echo "  ✅ Function call tracing with entry/exit logging"
echo "  ✅ Global data inspection"
echo "  ✅ Debug endpoint at http://localhost:3001/debug"
echo "  ✅ Audible debugging announcements"
echo "  ✅ Latency monitoring"
echo "  ✅ Performance metrics"
echo ""
echo "Available endpoints:"
echo "  • Main service:    http://localhost:3001/"
echo "  • Sales agent:     http://localhost:3001/sales"
echo "  • Support agent:   http://localhost:3001/support"
echo "  • Service info:    http://localhost:3001/info"
echo "  • Debug info:      http://localhost:3001/debug"
echo ""
echo "Debug logs will show:"
echo "  • Function entry/exit points"
echo "  • Parameter values"
echo "  • Global data state changes"
echo "  • Transfer operations"
echo "  • AI responses and decisions"
echo ""
echo "Press Ctrl+C to stop the service"
echo "================================"

# Run the service
python acme_multi_agent_service.py 