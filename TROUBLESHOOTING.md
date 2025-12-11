# Troubleshooting Guide

## Restarting the Application

### If the Application is Running Slowly or Hanging

1. **Interrupt the current process:**
   - Press `Ctrl+C` (or `Cmd+C` on Mac) to interrupt
   - You may need to press it multiple times if the first doesn't work
   - This will stop the current request and return you to the prompt

2. **Exit the application:**
   - Type `exit` or `quit` to fully exit
   - Or press `Ctrl+C` when at the prompt

3. **Restart the application:**
   ```bash
   python main.py
   ```

### Force Kill (if Ctrl+C doesn't work)

If the application is completely frozen:

1. **Open a new terminal window/tab**
2. **Find the process:**
   ```bash
   ps aux | grep python
   ```
3. **Kill the process:**
   ```bash
   kill -9 <process_id>
   ```
   Replace `<process_id>` with the actual process ID from step 2

## Common Issues

### Application Taking Too Long

**Possible causes:**
- API rate limiting or slow API response
- Complex request requiring multiple agent interactions
- Network connectivity issues

**Solutions:**
1. Wait a bit longer (AI agent coordination can take time)
2. Try a simpler request first
3. Check your internet connection
4. Verify your API key is valid and has credits
5. Check API status if using Anthropic

### API Errors

**Symptoms:**
- Error messages about API keys
- Rate limit errors
- Authentication failures

**Solutions:**
1. Verify `ANTHROPIC_API_KEY` is set:
   ```bash
   echo $ANTHROPIC_API_KEY
   ```
2. Re-export if needed:
   ```bash
   export ANTHROPIC_API_KEY=your_key_here
   ```
3. Check you have API credits available
4. Verify the API key is correct

### Import Errors

**Symptoms:**
- `ModuleNotFoundError` or `ImportError`

**Solutions:**
1. Make sure virtual environment is activated:
   ```bash
   source tt_env/bin/activate
   ```
2. Reinstall dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Plan Not Found Errors

**Symptoms:**
- "Plan file not found" errors

**Solutions:**
1. List available plans:
   ```
   Touchline Tactician> list
   ```
2. Check the plan filename is correct
3. Verify plans exist in `storage/plans/` directory

### Validation Errors

**Symptoms:**
- Plan validation fails when creating/editing

**Solutions:**
1. Read the validation error message carefully
2. Common issues:
   - Missing players (need 11 players)
   - Invalid positions
   - Zone coordinates out of bounds (must be 0-100)
   - Missing phase instructions
3. Fix the issues and try again

## Performance Tips

1. **Start with simple plans** - Complex formations with many custom instructions take longer
2. **Be specific in descriptions** - Vague descriptions require more AI inference
3. **Break up large edits** - Instead of many changes at once, do them in smaller batches
4. **Check API response times** - Slow API responses will slow down the entire system

## Getting Help

If issues persist:
1. Check the error message carefully
2. Review the logs/output for clues
3. Try the command again (sometimes transient issues)
4. Restart the application
5. Check that all dependencies are installed correctly

