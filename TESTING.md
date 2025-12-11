# Testing Touchline Tactician in Cursor Terminal

## Quick Start Testing

### 1. Activate Virtual Environment

In the Cursor Terminal, navigate to the project and activate the virtual environment:

```bash
cd /Users/slavin22/Documents/Overclock/Projects/touchline_tactician
source tt_env/bin/activate
```

You should see `(tt_env)` in your terminal prompt.

### 2. Set API Key

**Important**: Never commit your API key to the repository. Use one of these methods:

**Option A: Environment Variable (Recommended for Testing)**
```bash
export ANTHROPIC_API_KEY=your_api_key_here
```

**Option B: .env File (Recommended for Development)**
Create a `.env` file in the project root (this file is already in .gitignore):
```bash
echo "ANTHROPIC_API_KEY=your_api_key_here" > .env
```

Then load it in your terminal:
```bash
export $(cat .env | xargs)
```

**Option C: Add to Shell Profile (For Persistent Use)**
Add to your `~/.zshrc` or `~/.bash_profile`:
```bash
export ANTHROPIC_API_KEY=your_api_key_here
```

Then reload: `source ~/.zshrc`

### 3. Run the Application

```bash
python main.py
```

You should see the Touchline Tactician banner and a command prompt.

## Testing Workflow

### Test 1: Basic Commands

```
Touchline Tactician> help
```

This should display the help menu with available commands.

### Test 2: Create a Tactical Plan (New Interview Workflow)

```
Touchline Tactician> create
```

The orchestrator will now ask you ALL 13 questions at once in a consistent format:

1. Plan name
2. Your team name
3. Your team's formation
4. Your team's tactical style
5. Your key players and positions
6. Your team's strengths
7. Your team's weaknesses
8. Opponent team name
9. Opponent's formation
10. Opponent's tactical style
11. Opponent's key players
12. Opponent's strengths
13. Opponent's weaknesses

**Example answers for testing:**
1. Test Match Plan
2. Manchester United
3. 4-3-3
4. High press
5. Player 10 (CAM), Player 7 (LW), Player 9 (ST)
6. Fast wingers, strong midfield
7. Vulnerable on counter-attacks
8. Liverpool
9. 4-4-2
10. Possession-based
11. Their number 9 (ST) and number 10 (CAM)
12. Strong midfield control
13. Slow fullbacks, vulnerable to pace

**After answering all questions:**
- The orchestrator will process all answers together (faster!)
- PlanBuilder will create the tactical plan
- You'll see a description of the plan
- You'll be asked if you want to make changes
- If you say "no" or "looks good", it will generate visualization and report automatically

### Test 3: List Plans

```
Touchline Tactician> list
```

This should show all saved tactical plans.

### Test 4: Visualize a Plan

After creating a plan, visualize it:

```
Touchline Tactician> visualize [plan_id]
```

Replace `[plan_id]` with the actual plan filename (e.g., `plan_abc123.json`).

### Test 5: Edit a Plan

```
Touchline Tactician> edit [plan_id] move player 10 to left wing
```

### Test 6: Generate Reports

**Note**: Reports are now automatically generated after plan creation (if you confirm no changes are needed). You can also generate them manually:

```
Touchline Tactician> generate [plan_id]
```

This will create a single-page report with:
- Top half: Descriptive summary of the tactical plan
- Bottom half: Embedded ASCII visualization

The report will be saved in `storage/reports/`

## Expected Behavior

### On Startup

- Banner displays correctly
- System initialization message appears
- Command prompt is ready

### During Operation

- Commands are processed by the orchestrator team
- Agents coordinate to handle requests
- Responses are displayed in markdown format
- Plans are saved to `storage/plans/`
- Reports are saved to `storage/reports/`

### Error Handling

- Invalid commands show helpful error messages
- Missing plans are reported clearly
- Validation errors explain what needs to be fixed

## Troubleshooting

### Import Errors

If you see import errors, make sure:
- Virtual environment is activated
- You're in the project root directory
- All dependencies are installed: `pip install -r requirements.txt`

### API Errors

If you see API errors:
- Verify `ANTHROPIC_API_KEY` is set correctly
- Check you have API credits available
- Ensure internet connection is working

### File Not Found Errors

If plans aren't found:
- Check `storage/plans/` directory exists
- Use `list` command to see available plans
- Verify plan filenames are correct

## Quick Test Script

You can also test individual components:

```bash
# Test imports
python -c "from agents.orchestrator import create_orchestrator_team; print('✓ Imports work')"

# Test data models
python -c "from models.tactical_plan import TacticalPlan; print('✓ Models work')"

# Test file operations
python -c "from tools.file_operations import TacticalPlanFileTools; print('✓ Tools work')"
```

## Interactive Testing Tips

1. **Start Simple**: Begin with basic commands like `help` and `list`
2. **Create One Plan**: Make a simple plan first to understand the flow
3. **Test Each Feature**: Try each major feature (create, visualize, edit, generate)
4. **Check Files**: Look in `storage/plans/` and `storage/reports/` to verify outputs
5. **Read Responses**: The AI agents provide detailed feedback - read their responses

## Example Test Session

```bash
# Start the app
python main.py

# In the app:
Touchline Tactician> help
Touchline Tactician> create

# The orchestrator will ask all 13 questions at once:
# Answer all questions in your response, for example:
# "1. Test Match Plan
#  2. Manchester United
#  3. 4-3-3
#  4. High press
#  5. Player 10 (CAM), Player 7 (LW), Player 9 (ST)
#  6. Fast wingers, strong midfield
#  7. Vulnerable on counter-attacks
#  8. Liverpool
#  9. 4-4-2
#  10. Possession-based
#  11. Their number 9 and 10
#  12. Strong midfield control
#  13. Slow fullbacks, vulnerable to pace"

# After the plan is created, you'll see the description
# Respond with "looks good" or "no changes" to proceed
# The system will automatically generate visualization and report

Touchline Tactician> list
Touchline Tactician> visualize [your_plan_id]
Touchline Tactician> exit
```

## New Workflow Testing Checklist

- [ ] **Interview Phase**: All 13 questions asked at once in consistent format (fast!)
- [ ] **Question Consistency**: Same 13 questions in same order every time
- [ ] **Answer Collection**: Can provide all answers in one response (numbered 1-13)
- [ ] **Plan Building**: Plan is created from structured information including team names
- [ ] **Plan Presentation**: Clear description of the plan is shown (includes team names)
- [ ] **Feedback Loop**: Can request changes and see updated plan
- [ ] **Finalization**: Saying "no changes" triggers visualization and report
- [ ] **Report Generation**: Single-page report with embedded visualization is created
- [ ] **File Output**: Report saved in `storage/reports/` directory

## Next Steps After Testing

Once basic testing works:
1. Test with different formations (4-4-2, 3-5-2, etc.)
2. Test editing various aspects of plans
3. Test all three report types
4. Test error cases (invalid commands, missing plans)
5. Verify file persistence (exit and restart, plans should still be there)

