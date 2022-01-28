ANSI_RED='\033[0;31m'
ANSI_GREEN='\033[0;32m'
ANSI_RESET='\033[0m'

# This is a function to better handle paths that may contains whitespace.
lint() {
    # Track failures so we can avoid returning early.
    failed=0

    isort -c "$@" || failed=1
    black --check -l79 "$@" || failed=1
    return $failed
}

fmt() {
    isort "$@" && black -l79 "$@"
}

lint src tests
result=$?

if [ $result = 0 ]; then
    echo -e "${ANSI_GREEN}Lint passed!${ANSI_RESET}"
else
    echo -e "${ANSI_RED}Lint failed!${ANSI_RESET}"
    echo -e "\nWould you like to format the codebase? (Y/N)"
    read user_prompt
    if [ $user_prompt = Y ]; then
        echo -e "\nReformatting..."
        fmt src tests
    fi
fi

exit $result