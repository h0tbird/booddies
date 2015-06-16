# Helper bash functions.

#------------------------------------------------------------------------------
# Globals:
#------------------------------------------------------------------------------

readonly C_CLEAR=$(tput sgr0)
readonly C_MAIN=${C_CLEAR}$(tput bold)
readonly C_OTHER=${C_MAIN}$(tput setaf 4)
readonly C_BUSY=${C_CLEAR}$(tput setaf 6)
readonly SAVE_POSITION="\033[s"
readonly DEL_TEXT="\e[$(( $(( $(tput cols) - 13 )) + 4 ))G"

#------------------------------------------------------------------------------
# Globals:
#   DEL_TEXT
# Arguments:
#   None
# Returns:
#   None
#------------------------------------------------------------------------------

function misc::deltext() {
  printf "${DEL_TEXT}"
}

#------------------------------------------------------------------------------
# Globals:
#   C_OTHER
#   C_MAIN
#   C_CLEAR
#   SAVE_POSITION
#   C_BUSY
# Arguments:
#   Message
# Returns:
#   None
#------------------------------------------------------------------------------

function misc::stat_busy() {
  printf "${C_OTHER}:: ${C_MAIN}${1}${C_CLEAR} "
  printf "${SAVE_POSITION}"
  misc::deltext
  printf "   ${C_OTHER}[${C_BUSY}BUSY${C_OTHER}]${C_CLEAR} "
}

#------------------------------------------------------------------------------
# Globals:
#   C_OTHER
#   C_MAIN
#   C_OTHER
#   C_CLEAR
# Arguments:
#   None
# Returns:
#   None
#------------------------------------------------------------------------------

function misc::stat_done() {
  misc::deltext
  printf "   ${C_OTHER}[${C_MAIN}DONE${C_OTHER}]${C_CLEAR} \n"
}

#------------------------------------------------------------------------------
# Globals:
#   C_OTHER
#   C_FAIL
#   C_CLEAR
# Arguments:
#   None
# Returns:
#   None
#------------------------------------------------------------------------------

function misc::stat_fail() {
  misc::deltext
  printf "   ${C_OTHER}[${C_FAIL}FAIL${C_OTHER}]${C_CLEAR} \n"
}

#------------------------------------------------------------------------------
#
#------------------------------------------------------------------------------

function misc::log() {
  echo -n "$(date '+%Y-%m-%d %H:%M:%S') $@" >&2
}
