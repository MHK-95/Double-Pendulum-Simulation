#!/bin/bash
#----------------------------------------------------------------------------------------------------------------------#
#                                                       run.sh                                                         #
#----------------------------------------------------------------------------------------------------------------------#
# A simple script to either run the program or run the tests.


#------------------------------------------------------------------------------#
# echo_bold()                                                                  #
# Simply echos argument 1 as bold.                                             #
#------------------------------------------------------------------------------#
echo_bold() {
  echo -e "\033[1m$1\033[0m"
}

if [ "$1" == "--test" ]; then
  echo_bold "\nRunning the mypy tests."
  python3 -m mypy app --ignore-missing-imports
  echo_bold "\nRunning the pytest tests."
  python3 -m pytest --cov=app tests
else
  echo_bold "Running the program."
  python3 app/main.py "$@"
fi
