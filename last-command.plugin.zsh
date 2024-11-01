# Function to call Ollama and get analysis
analyze_command() {
    local cmd="$1"
    local exit_code="$2"
    
    # Prepare the prompt
    local prompt="Analyze this command and its exit code:
Command: $cmd
Exit Code: $exit_code

Provide a very brief (1-2 lines) explanation of what happened."

    # Call Ollama and get response
    local analysis=$(ollama run llama3.2 "$prompt")
    echo "$analysis"
}

# Function to be called before each command
preexec() {
    LAST_COMMAND="$1"
    COMMAND_TIME=$(date "+%H:%M:%S")
}

# Function to be called after each command
precmd() {
    local EXIT_CODE=$?
    
    if [[ -n "$LAST_COMMAND" ]]; then
        local STATUS_SYMBOL
        if [ $EXIT_CODE -eq 0 ]; then
            STATUS_SYMBOL="\033[32m✅ \033[0m"
        else
            STATUS_SYMBOL="\033[31m❌ ($EXIT_CODE)\033[0m"
        fi
        # echo "[$COMMAND_TIME] $STATUS_SYMBOL $LAST_COMMAND"

        # Only analyze non-trivial commands (exit code != 0 or complex commands)
        if [ $EXIT_CODE -ne 0 ]; then
            echo "\033[34m💡 AI Analysis:\033[0m"
            analyze_command "$LAST_COMMAND" "$EXIT_CODE"
            echo "-------------------"
        fi
    fi
    
    LAST_COMMAND=""
} 