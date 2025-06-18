# ACME Corp Multi-Agent Service - Enhanced Receptionist System

**An advanced enhancement of the ACME Corp receptionist from v1-sdk-basics**

This multi-agent service builds upon the basic ACME Corp receptionist with specialized agents for comprehensive customer service. The system provides seamless routing between a receptionist and specialized sales and support agents for ACME's phone repair business.

**🔍 Debug Mode Always Enabled** - This service runs with comprehensive debugging and monitoring always active for optimal troubleshooting and performance insights.

## 🏢 About ACME Corp

ACME Corp is the premier provider of professional phone repair services designed to get your device back to perfect working condition. Our enhanced receptionist system ensures every customer gets connected to the right specialist for their phone repair needs.

## 🎯 Service Overview

### **Enhanced Multi-Agent Architecture**

| Agent | Endpoint | Description | Enhancement over v1 |
|-------|----------|-------------|-------------------|
| **Receptionist** | `/` | Enhanced v1 receptionist with intelligent routing | ✨ Multi-agent routing, secure context storage |
| **Sales Specialist** | `/sales` | ACME phone repair service quotes and recommendations | ✨ Service expertise, pricing, device compatibility |
| **Support Specialist** | `/support` | Technical support for phone repair services | ✨ Diagnostics, repair status, service tickets |

## 🚀 Quick Start

### **Prerequisites**
- Python 3.8+
- SignalWire account and credentials
- Environment configuration (same as v1-sdk-basics)

### **Running the Service**

```bash
# Linux/Mac
./run_acme_service.sh

# Windows
run_acme_service.bat

# Debug mode (with enhanced debugging)
./debug_run.sh
```

**Service Endpoints:**
- **Receptionist**: `http://localhost:3001/` - Enhanced v1 receptionist
- **Sales Specialist**: `http://localhost:3001/sales` - ACME phone repair quotes
- **Support Specialist**: `http://localhost:3001/support` - Phone repair technical support
- **Service Info**: `http://localhost:3001/info` - Service information
- **🔍 Debug Info**: `http://localhost:3001/debug` - Always available debug information

## 🔍 Debug Features (Always Active)

This service runs with comprehensive debugging always enabled:

### **Built-in Debug Capabilities**
- ✅ **Function Tracing**: Entry/exit logging for all SWAIG functions
- ✅ **Global Data Monitoring**: Real-time context state tracking
- ✅ **Timestamped Output**: Precise timing for all debug messages
- ✅ **Structured Logging**: Multiple log levels and formatted output
- ✅ **Performance Monitoring**: Response caching and usage accounting
- ✅ **SignalWire AI Debugging**: Audible debugging and latency monitoring

### **Debug Configuration**
While debug mode is always on, you can customize the level of debugging:

```bash
# Optional: Customize debug behavior
export DEBUG_WEBHOOK_URL="https://your-webhook-url/debug"  # Real-time monitoring
export DEBUG_WEBHOOK_LEVEL=2  # 0=disabled, 1=basic, 2=verbose
export VERBOSE_LOGS=true      # Detailed logging
export AUDIBLE_DEBUG=true     # AI announces function execution
export AUDIBLE_LATENCY=true   # AI announces latency info
```

### **Debug Endpoints**
- **GET /debug** - Comprehensive debug status and configuration
- **GET /info** - Service information and status

## 🔧 Configuration

### **Environment Variables** (same as v1-sdk-basics)
Create a `.env` file with your ACME Corp configuration:

```bash
# SignalWire Credentials (required)
SIGNALWIRE_PROJECT_ID=your_project_id
SIGNALWIRE_AUTH_TOKEN=your_auth_token

# ACME Corp Configuration (optional - defaults provided)
COMPANY_NAME=Acme Corp
COMPANY_SPECIALTY=Professional Phone Repair Services
COMPANY_PHONE=+1-555-ACME-CORP

# Agent Configuration (optional)
AGENT_HOST=0.0.0.0
AGENT_PORT=3001
AGENT_ROUTE=/
```

You can use the `.env.example` from `v1-sdk-basics` as a reference.

## 📋 Files Overview

### **Essential Files**
- `acme_multi_agent_service.py` - Main enhanced receptionist service
- `requirements.txt` - Dependencies (SignalWire SDK + dotenv)
- `run_acme_service.sh` / `.bat` - Startup scripts
- `README.md` - This documentation
- `TRANSFER_GUIDE.md` - Comprehensive transfer functionality guide

### **Knowledge Bases**
- `acme_products_knowledge.md` - ACME phone repair services catalog
- `acme_support_knowledge.md` - Technical support procedures

## ✨ Enhancement Features over v1

### **1. Multi-Agent Architecture**
- **v1**: Single receptionist agent with basic caller info capture
- **v2**: Enhanced receptionist + specialized sales and support agents

### **2. Intelligent Routing**
- **v1**: Basic caller name and reason capture
- **v2**: Context-aware routing with preserved conversation history

### **3. Secure Context Storage**
- **v1**: Simple caller info printing  
- **v2**: Secure `global_data` session storage with automatic context passing

### **4. Specialized Expertise**
- **v1**: General ACME Corp information
- **v2**: Dedicated specialists with service knowledge and technical support

### **5. POM-Structured Prompts**
- **v1**: Manual prompt construction
- **v2**: Structured Prompt Object Model for consistency

## 🔄 How It Works

### **Customer Journey Flow**
```
1. Customer calls → Receptionist Agent (enhanced v1)
   ↓
2. Receptionist captures: name, inquiry type, details
   ↓  
3. Context stored securely in global_data
   ↓
4. Transfer to appropriate specialist:
   • Sales: Service inquiries, pricing, repair quotes
   • Support: Technical issues, repair status, existing services
   ↓
5. Specialist has full context from receptionist conversation
   ↓
6. Specialized assistance with knowledge base search
```

### **Context Preservation**
- Caller information automatically passed between agents
- No need to repeat details when transferred
- Secure session-level storage (not exposed to other calls)

## 🛠️ Technical Architecture

### **Built on v1 Foundation**
- Same environment configuration as v1-sdk-basics
- Enhanced version of the basic receptionist agent
- POM (Prompt Object Model) for structured prompts
- Official SignalWire Agents SDK patterns

### **Key Technologies**
- **SignalWire Agents SDK**: Official SDK with native capabilities
- **Global Data**: Session-level context storage (replaces custom databases)
- **SWML Transfer**: Seamless agent-to-agent transfers
- **Native Vector Search**: Knowledge base integration for specialists
- **POM**: Structured prompt management

## 📞 Testing the Service

### **Basic Flow Test**
```bash
# Test receptionist (enhanced v1)
curl -X POST http://localhost:3001/ \
  -H "Content-Type: application/json" \
  -d '{"message": "Hi, my name is John Smith and I need help with my phone repair"}'

# Test specialist with context preservation
curl -X POST http://localhost:3001/sales \
  -H "Content-Type: application/json" \
  -d '{"message": "What phone repair services do you recommend for a cracked screen?"}'
```

### **Service Health Check**
```bash
curl http://localhost:3001/info
```

## 🔍 Troubleshooting

### **Common Issues**

**Service won't start:**
- Check `.env` file exists with proper credentials
- Verify Python 3.8+ installed
- Run `pip install -r requirements.txt`

**Context not transferring:**
- Ensure agents use `save_caller_info` before transfer
- Check `global_data` is properly set

**Knowledge search not working:**
- Verify knowledge base files exist
- Check search index files are generated

**Transfer not working:**
- See `TRANSFER_GUIDE.md` for comprehensive transfer documentation
- Verify destination format (HTTP URL, PSTN number, or SIP address)
- Check network connectivity to destination

## 📈 Monitoring & Analytics

### **Built-in Logging**
- Caller information captured and logged
- Agent transfer tracking
- Performance metrics available

### **Available Endpoints**
- `/info` - Service status and configuration
- `/` - Enhanced receptionist (main entry point)
- `/sales` - Sales specialist with service expertise  
- `/support` - Support specialist with technical knowledge

## 🎉 Success Metrics

### **Enhanced Customer Experience**
- **Intelligent Routing**: Customers reach the right specialist faster
- **Context Preservation**: No need to repeat information after transfer
- **Specialized Knowledge**: Expert assistance for specific phone repair needs
- **Professional Service**: Consistent ACME Corp branding and messaging

### **Operational Benefits**
- **Simplified Architecture**: Uses official SDK patterns
- **Reduced Maintenance**: No custom databases or complex state management
- **Better Reliability**: Built-in session management and error handling
- **Scalable Design**: Easy to add new specialists or modify routing logic

## 📞 ACME Corp Contact

- **Sales**: +1-555-ACME-CORP (1-555-226-3267)
- **Support**: +1-555-TECH-SUP (1-555-832-4787)  
- **Website**: www.acmecorp.com
- **Founded**: 1949 - Over 75 years of phone repair excellence

---

*This enhanced receptionist system demonstrates the evolution from basic customer service (v1) to sophisticated multi-agent architecture (v2) while maintaining the familiar ACME Corp experience.*
