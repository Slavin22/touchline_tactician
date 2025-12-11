"""
Touchline Tactician - Multi-Agent Tactical Planning System

A CLI application for soccer coaches to create, visualize, edit, and document tactical plans.
"""
import sys
from pathlib import Path

# Try to enable better terminal input handling (readline support)
try:
    import readline
    # Enable history and better editing on macOS/Linux
    readline.parse_and_bind("bind ^I rl_complete")  # Tab completion
except ImportError:
    # readline not available (Windows)
    pass

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
  create          - Create a new tactical plan (prompts for name and description)
  visualize       - Show ASCII tactical board for a plan
  edit <plan>     - Edit a tactical plan with free-text instructions
  tweak <plan>    - Alias for edit - tweak a plan with free-text instructions
  generate        - Generate reports (executive, coach, or player)
  list            - List all saved tactical plans
  help            - Show this help message
  exit/quit       - Exit the application

Workflow:
  1. Type 'create' to start creating a plan
  2. Enter plan name when prompted
  3. Describe your tactical idea when prompted
  4. System will create the plan, show description, and display the board
  5. Enter free-text instructions to tweak (e.g., "make player 10 wider" or "change to 4-4-2")
  6. System will update plan, save it, and show updated board
  7. Continue tweaking as needed

Examples:
  create
  edit plan_123.json move player 10 to left wing and make pressing more aggressive
  tweak plan_123.json change formation to 4-4-2
  visualize plan_123.json
  generate executive plan_123.json
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
            
            # Handle create command with special workflow
            if user_input.lower() == 'create':
                plan_name = input("Plan Name: ").strip()
                if not plan_name:
                    print("Plan name is required. Cancelling plan creation.\n")
                    continue
                
                print("\nDescribe your tactical plan idea:")
                print("(You can describe formation, style, key players, tactics, etc.)")
                plan_description = input("> ").strip()
                if not plan_description:
                    print("Plan description is required. Cancelling plan creation.\n")
                    continue
                
                # Create the request for the orchestrator
                user_input = f"Create a tactical plan named '{plan_name}' with the following description: {plan_description}"
            
            # Handle edit/tweak commands - extract plan identifier if provided
            elif user_input.lower().startswith('edit ') or user_input.lower().startswith('tweak '):
                # If user provided plan identifier, keep it; otherwise let orchestrator figure it out
                # Format: "edit plan_123.json instructions" or "tweak plan_123.json instructions"
                pass  # Let orchestrator handle it
            
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
            print("\n\n⚠️  Request interrupted. You can:")
            print("  - Continue with a new request")
            print("  - Type 'exit' to quit")
            print("  - Press Ctrl+C again to force exit\n")
            continue
        except Exception as e:
            print(f"\n✗ Error: {e}")
            print("Please try again or type 'help' for assistance.\n")


if __name__ == "__main__":
    main()
