#!/usr/bin/env python3
"""
Test SWML generation for the receptionist agent
"""

import json
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from receptionist import agent

def test_swml_generation():
    """Test SWML generation and check for issues"""
    
    print("Testing SWML generation for Receptionist Agent v1...")
    print("-" * 60)
    
    try:
        # Get the SWML document
        swml_json = agent._render_swml()
        swml_data = json.loads(swml_json)
        
        # Pretty print the SWML
        print("Generated SWML:")
        print(json.dumps(swml_data, indent=2))
        print("-" * 60)
        
        # Check for AI section
        if "sections" in swml_data and "main" in swml_data["sections"]:
            main_section = swml_data["sections"]["main"]
            
            # Find AI section
            ai_section = None
            for section in main_section:
                if "ai" in section:
                    ai_section = section["ai"]
                    break
            
            if ai_section and "SWAIG" in ai_section and "functions" in ai_section["SWAIG"]:
                functions = ai_section["SWAIG"]["functions"]
                
                print(f"Found {len(functions)} functions:")
                for func in functions:
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