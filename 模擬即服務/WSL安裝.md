
![2025-06-19_12-23-30](/assets/2025-06-19_12-23-30.png)

```bash
sudo mkdir -p /opt/ansys/electronics/2025R1
sudo tar -xvzf ELECTRONICS_2025R1_LINX64.tgz -C /opt/ansys/electronics/2025R1
```

![2025-06-19_12-36-33](/assets/2025-06-19_12-36-33.png)


```bash
cd /opt/ansys/electronics/2025R1
sudo ./INSTALL
```

![2025-06-19_12-39-54](/assets/2025-06-19_12-39-54.png)

```bash
sudo apt update
sudo apt install libice6 libjpeg62 libsm6 libxcb-icccm4 libxcb-image0 libxcb-keysyms1 libxcb-render-util0 libxcb-shape0 libxcb-util1 libxcb-xinerama0 libxcb-xkb1 libxkbcommon-x11-0 xfonts-100dpi xfonts-75dpi
```
![2025-06-19_12-42-02](/assets/2025-06-19_12-42-02.png)




```bash
sudo apt update && sudo apt install -y \
  libgif7 libxft2 libxm4 libxmu6 libxt6 libglu1-mesa \
  lsb xsltproc libnss3
```

![2025-06-19_13-33-22](/assets/2025-06-19_13-33-22.png)

```
sudo apt update
sudo apt install -y x11-apps
```

```
grep -q 'ANSYSLMD_LICENSE_FILE' ~/.bashrc || echo -e '\n# 設定 ANSYS License Server for WSL2\nWINDOWS_IP=$(ip route | grep default | awk '"'"'{print \$3}'"'"')\nexport ANSYSLMD_LICENSE_FILE=1055@$WINDOWS_IP' >> ~/.bashrc
source ~/.bashrc
echo $ANSYSLMD_LICENSE_FILE
```


```
echo 'export ANSYSEM_ROOT251=/opt/ansys_inc/v251/AnsysEM' >> ~/.bashrc
echo 'export LD_LIBRARY_PATH=$ANSYSEM_ROOT251/common/mono/Linux64/lib64:$ANSYSEM_ROOT251/Delcross:$LD_LIBRARY_PATH' >> ~/.bashrc
source ~/.bashrc
```

```
nc -zv 172.26.192.1 50051
```


```
sudo apt-get update && sudo apt-get install -y redis-server
redis-server
```

###
```bash
# ~/.bashrc: executed by bash(1) for non-login shells.
# see /usr/share/doc/bash/examples/startup-files (in the package bash-doc)
# for examples

# If not running interactively, don't do anything
[ -z "$PS1" ] && return

# don't put duplicate lines in the history. See bash(1) for more options
# ... or force ignoredups and ignorespace
HISTCONTROL=ignoredups:ignorespace

# append to the history file, don't overwrite it
shopt -s histappend

# for setting history length see HISTSIZE and HISTFILESIZE in bash(1)
HISTSIZE=1000
HISTFILESIZE=2000

# check the window size after each command and, if necessary,
# update the values of LINES and COLUMNS.
shopt -s checkwinsize

# make less more friendly for non-text input files, see lesspipe(1)
[ -x /usr/bin/lesspipe ] && eval "$(SHELL=/bin/sh lesspipe)"

# set variable identifying the chroot you work in (used in the prompt below)
if [ -z "$debian_chroot" ] && [ -r /etc/debian_chroot ]; then
    debian_chroot=$(cat /etc/debian_chroot)
fi

# set a fancy prompt (non-color, unless we know we "want" color)
case "$TERM" in
    xterm-color) color_prompt=yes;;
esac

# uncomment for a colored prompt, if the terminal has the capability; turned
# off by default to not distract the user: the focus in a terminal window
# should be on the output of commands, not on the prompt
#force_color_prompt=yes

if [ -n "$force_color_prompt" ]; then
    if [ -x /usr/bin/tput ] && tput setaf 1 >&/dev/null; then
        # We have color support; assume it's compliant with Ecma-48
        # (ISO/IEC-6429). (Lack of such support is extremely rare, and such
        # a case would tend to support setf rather than setaf.)
        color_prompt=yes
    else
        color_prompt=
    fi
fi

if [ "$color_prompt" = yes ]; then
    PS1='${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$ '
else
    PS1='${debian_chroot:+($debian_chroot)}\u@\h:\w\$ '
fi
unset color_prompt force_color_prompt

# If this is an xterm set the title to user@host:dir
case "$TERM" in
xterm*|rxvt*)
    PS1="\[\e]0;${debian_chroot:+($debian_chroot)}\u@\h: \w\a\]$PS1"
    ;;
*)
    ;;
esac

# enable color support of ls and also add handy aliases
if [ -x /usr/bin/dircolors ]; then
    test -r ~/.dircolors && eval "$(dircolors -b ~/.dircolors)" || eval "$(dircolors -b)"
    alias ls='ls --color=auto'
    #alias dir='dir --color=auto'
    #alias vdir='vdir --color=auto'

    alias grep='grep --color=auto'
    alias fgrep='fgrep --color=auto'
    alias egrep='egrep --color=auto'
fi

# some more ls aliases
alias ll='ls -alF'
alias la='ls -A'
alias l='ls -CF'

# Alias definitions.
# You may want to put all your additions into a separate file like
# ~/.bash_aliases, instead of adding them here directly.
# See /usr/share/doc/bash-doc/examples in the bash-doc package.

if [ -f ~/.bash_aliases ]; then
    . ~/.bash_aliases
fi

# enable programmable completion features (you don't need to enable
# this, if it's already enabled in /etc/bash.bashrc and /etc/profile
# sources /etc/bash.bashrc).
#if [ -f /etc/bash_completion ] && ! shopt -oq posix; then
#    . /etc/bash_completion
#fi
export ANSYSEM_ROOT251=/opt/ansys_inc/v251/AnsysEM
export LD_LIBRARY_PATH=$ANSYSEM_ROOT251/common/mono/Linux64/lib64:$ANSYSEM_ROOT251/Delcross:$LD_LIBRARY_PATH


# 設定 ANSYS License Server for WSL2
WINDOWS_IP=$(ip route | grep default | awk '{print $3}')
export WINDOWS_IP=$WINDOWS_IP
export ANSYSLMD_LICENSE_FILE=1055@$WINDOWS_IP

export LC_ALL=C.UTF-8
export LANG=C.UTF-8
```