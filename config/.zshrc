# Zsh config para Kali Lab

# Historial
HISTSIZE=10000
SAVEHIST=10000
HISTFILE=~/.zsh_history
setopt SHARE_HISTORY
setopt HIST_IGNORE_DUPS

# Autocompletado
autoload -Uz compinit
compinit
zstyle ':completion:*' menu select
zstyle ':completion:*' matcher-list 'm:{a-zA-Z}={A-Za-z}'

# Prompt simple y funcional: [user@container dir]$
PROMPT='%F{cyan}[%n@%m %1~]%f%# '

# Alias utiles
alias ll='ls -lah --color=auto'
alias la='ls -A --color=auto'
alias l='ls -CF --color=auto'
alias grep='grep --color=auto'
alias ip='ip -c'
alias update='apt update && apt upgrade -y'
alias ..='cd ..'
alias ...='cd ../..'

# Herramientas de pentesting
alias nmap-quick='nmap -T4 --top-ports 1000 -sV'
alias nmap-full='nmap -T4 -p- -sV -sC'
alias gobuster-quick='gobuster dir -w /usr/share/wordlists/dirb/common.txt'
alias gobuster-big='gobuster dir -w /usr/share/seclists/Discovery/Web-Content/common.txt'

# Proxychains con tor
alias torsocks='proxychains'

# Colores para ls
export LS_COLORS='rs=0:di=01;34:ln=01;36:mh=00:pi=40;33:so=01;35:do=01;35:bd=40;33;01:cd=40;33;01:or=40;31;01:mi=00:su=37;41:sg=30;43:ca=30;41:tw=30;42:ow=34;42:st=37;44:ex=01;32'

# Editor por defecto
export EDITOR=micro

# Banner de inicio
echo ""
figlet -f slant "Hop-Lab" | lolcat
echo ""

# PATH
export PATH="$HOME/.local/bin:$PATH"

# Titulo de la terminal
precmd() { print -Pn "\e]0;%n@%m: %~\a" }

# Keybindings estilo emacs
bindkey -e

# Busqueda en historial con flechas
bindkey '^[[A' history-beginning-search-backward
bindkey '^[[B' history-beginning-search-forward
