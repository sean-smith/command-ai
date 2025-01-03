import os

def get_last_command_from_zsh_history():
    try:
        # Read the zsh history file
        history_file = os.path.expanduser('~/.zsh_history')
        with open(history_file, 'rb') as f:
            # Read the file in binary mode and decode as utf-8, ignoring errors
            lines = f.read().decode('utf-8', errors='ignore').splitlines()
        
        # Get the last line that contains a command
        for line in reversed(lines):
            # zsh history format typically starts with ': timestamp:0;command'
            if line.startswith(':'):
                # Extract the command part after the timestamp
                command = line.split(';', 1)[-1].strip()
                return command
                
        return 'No command found in history'
    except Exception as e:
        return f'Error reading zsh history: {str(e)}'

def get_last_exit_code():
    try:
        # Run echo $? to get the exit code of the last command
        result = os.popen('echo $?').read().strip()
        return int(result)
    except Exception as e:
        return f'Error getting exit code: {str(e)}'

# Example usage
last_command = get_last_command_from_zsh_history()
exit_code = get_last_exit_code()
print(f"Last command: {last_command}")
print(f"Exit code: {exit_code}")
