#!/usr/bin/env python3
"""Utility script to inspect the generated SWML.

SWML (SignalWire Markup Language) is the intermediate JSON document
describing the agent.  This script mirrors the validation steps shown
in the Agents SDK documentation.
"""

import json
import sys
import os

# Add current directory to path so "receptionist" can be imported when
# running this script directly
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from receptionist import agent

def test_swml_generation():
    """Test SWML generation and check for issues.

    Useful when iterating on an agent to ensure that the generated
    markup contains the expected SWAIG functions.
    """
    
    print("Testing SWML generation for Receptionist Agent v1...")
    print("-" * 60)
    
    try:
        # Get the SWML document produced by the agent
        swml_json = agent._render_swml()
        swml_data = json.loads(swml_json)
        
        # Pretty print the SWML
        print("Generated SWML:")
        print(json.dumps(swml_data, indent=2))
        print("-" * 60)
        
        # Check for AI section which holds the SWAIG function definitions
        if "sections" in swml_data and "main" in swml_data["sections"]:
            main_section = swml_data["sections"]["main"]
            
            # Find AI section within the main section list
            ai_section = None
            for section in main_section:
                if "ai" in section:
                    ai_section = section["ai"]
                    break
            
            if ai_section and "SWAIG" in ai_section and "functions" in ai_section["SWAIG"]:
                functions = ai_section["SWAIG"]["functions"]
                
                print(f"Found {len(functions)} functions:")
                for func in functions:
                    # Display each SWAIG function name
                    print(f"\n  Function: {func.get('function', 'unknown')}")
                    
                    # Check parameter structure
                    if "parameters" in func:
                        params = func["parameters"]
                        print(f"    Parameters structure: {json.dumps(params, indent=6)}")
                        
                        # Check for double-nesting issue
                        if ("properties" in params and
                            isinstance(params["properties"], dict) and
                            "properties" in params["properties"]):
                            print("    ⚠️  WARNING: Double-nested properties detected!")
                        
                        # Check for empty required array
                        if "required" in params and params["required"] == []:
                            print("    ⚠️  WARNING: Empty required array detected!")
                            
                print("\n" + "-" * 60)
                print("SWML generation complete.")
            else:
                print("ERROR: No SWAIG functions found in SWML!")
        else:
            print("ERROR: Invalid SWML structure!")
            
    except Exception as e:
        print(f"ERROR generating SWML: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_swml_generation() 
