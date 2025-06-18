@echo off
REM ACME Corp Multi-Agent Service - Enhanced Receptionist System (Windows)
REM 
REM This script starts the enhanced ACME Corp multi-agent receptionist service
REM built on the v1-sdk-basics foundation using the official SignalWire Agents SDK.

echo 🏢 Starting ACME Corp Multi-Agent Service - Enhanced Receptionist System
echo =========================================================================

REM Check if virtual environment exists
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate

REM Install/upgrade requirements
echo ⬇️  Installing requirements...
pip install -r requirements.txt

REM Check for .env file
if not exist ".env" (
    echo ⚠️  Warning: .env file not found.
    echo    Please create one with your SignalWire credentials and ACME Corp configuration.
    echo    You can use the .env.example from v1-sdk-basics as a reference.
    echo.
    echo    Required variables:
    echo    - COMPANY_NAME ^(default: 'Acme Corp'^)
    echo    - COMPANY_SPECIALTY ^(default: 'Widgets for Roadrunners'^)
    echo    - COMPANY_PHONE ^(default: '+1-555-ACME-CORP'^)
)

REM Start the service
echo 🎯 Starting ACME Corp enhanced receptionist service...
echo.
echo Available endpoints:
echo   • Receptionist ^(v1 enhanced^): http://localhost:3001/
echo   • Sales Specialist:           http://localhost:3001/sales
echo   • Support Specialist:         http://localhost:3001/support
echo   • Service Info:               http://localhost:3001/info
echo.
echo Enhancement over v1:
echo   ✨ Multi-agent architecture with specialized routing
echo   ✨ Secure context preservation between agents
echo   ✨ POM-structured prompts for consistency
echo.
echo Press Ctrl+C to stop the service
echo =========================================================================

python acme_multi_agent_service.py

pause 