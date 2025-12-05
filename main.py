"""
Touchline Tactician - Multi-Agent Tactical Planning System

A CLI application for soccer coaches to create, visualize, edit, and document tactical plans.
"""
import sys
from pathlib import Path

from agents.orchestrator import create_orchestrator_team


def print_banner():
    """Print the application banner."""
    banner = """
╔═══════════════════════════════════════════════════════════╗
║         Touchline Tactician - Tactical Planning          ║
║              Multi-Agent AI Assistant                    ║
╚═══════════════════════════════════════════════════════════╝
"""
    print(banner)


def print_help():
    """Print help information."""
    help_text = """
Available Commands:
  create          - Create a new tactical plan
  visualize       - Show ASCII tactical board for a plan
  edit            - Edit an existing tactical plan
  generate        - Generate reports (executive, coach, or player)
  list            - List all saved tactical plans
  help            - Show this help message
  exit/quit       - Exit the application

Examples:
  create
  visualize plan_123.json
  edit plan_123.json move player 10 to LW
  generate executive plan_123.json
  generate coach plan_123.json
  generate player 10 plan_123.json
  list
"""
    print(help_text)


def main():
    """Main entry point for the CLI application."""
    print_banner()
    print("Welcome to Touchline Tactician!")
    print("Type 'help' for available commands or 'exit' to quit.\n")
    
    # Create the orchestrator team
    try:
        team = create_orchestrator_team()
        print("✓ System initialized. Ready to assist with tactical planning.\n")
    except Exception as e:
        print(f"✗ Error initializing system: {e}")
        sys.exit(1)
    
    # Interactive CLI loop
    while True:
        try:
            user_input = input("Touchline Tactician> ").strip()
            
            if not user_input:
                continue
            
            # Handle special commands
            if user_input.lower() in ['exit', 'quit', 'q']:
                print("\nThank you for using Touchline Tactician. Goodbye!")
                break
            
            if user_input.lower() == 'help':
                print_help()
                continue
            
            # Process the user's request through the orchestrator team
            print("\nProcessing your request...\n")
            response = team.run(user_input)
            
            # Print the response
            if response and hasattr(response, 'content'):
                print(response.content)
            elif response:
                print(str(response))
            else:
                print("No response received.")
            
            print()  # Empty line for readability
        
        except KeyboardInterrupt:
            print("\n\nInterrupted. Type 'exit' to quit or continue with your request.")
            continue
        except Exception as e:
            print(f"\n✗ Error: {e}")
            print("Please try again or type 'help' for assistance.\n")


if __name__ == "__main__":
    main()
