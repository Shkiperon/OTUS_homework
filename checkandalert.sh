#!/bin/bash
if (( $# != 1 )); then
  echo "Need only one parameter (name of service)."
  exit 1
fi

command -v mutt >/dev/null 2>&1 || { echo >&2 "This script need mutt but it's not installed. Aborting execution."; exit 1; }

adminemail="admin-email@domain.com"

createMuttRc() {
username="UserName"
password="SuperMegaPasswOrd"
  {
    echo 'set record = "/dev/null"';
    echo 'set trash = "/dev/null"';
    echo "set from = \"$username@yandex.ru\"";
    echo 'set realname = "Alarm script"';
    echo 'set use_from = yes';
    echo "set imap_user = \"$username@yandex.ru\"";
    echo "set imap_pass = \"$password\"";
    echo 'set folder = "imaps://imap.yandex.ru:993';
    echo "set spoolfile = \"imaps://$username@imap.yandex.ru\"";
    echo "set smtp_url = \"smtps://$username@smtp.yandex.ru:465/\"";
    echo "set smtp_pass = \"$password\"";
    echo 'unset imap_passive';
    echo 'set imap_check_subscribed';
    echo 'set mail_check = 60';
    echo 'set ssl_starttls = yes';
    echo 'set ssl_force_tls=yes';
  } > ./muttrc
}

trapAlert() {
  echo "Script was stopped. Reason is $1 exit-code. Timestamp of event (taked from system clock) $(date +'%Y-%m-%d %H:%M:%S')"
  createMuttRc
  ( printf "HIGH ALARM! Looks like process %s was killed by some terrorist on server or died by another user.\nReason of dead of process: %s\nTimestamp of event (taked from system clock) $(date +'%Y-%m-%d %H:%M:%S').\n" "$3" "$1" ) | mutt "$adminemail" -F "./muttrc" -s "High alarm while monitoring of $3"
  rm ./muttrc
  exit "$2"
}

trap 'trapAlert "SIGHUP" "1" "$1"' 1
trap 'trapAlert "SIGINT" "2" "$1"' 2
trap 'trapAlert "SIGQUIT" "3" "$1"' 3
trap 'trapAlert "SIGFPE" "8" "$1"' 8
trap 'trapAlert "SIGKILL" "9" "$1"' 9
trap 'trapAlert "SIGALARM" "14" "$1"' 14
trap 'trapAlert "SIGTERM" "15" "$1"' 15
trap 'trapAlert "SIGSTOP" "19" "$1"' 19

echo "Sending test message for check installation."
createMuttRc
( printf "Message from $(hostname) at $(date +'%Y-%m-%d %H:%M:%S').\nStarting monitoring of %s" "$1" ) | mutt "$adminemail" -F "./muttrc" -s "Start monitoring of $1 on $(hostname)" || { echo "ALARM AND STOP. It seems that packages openssl, libsasl2 and gnutls-bin are NOT installed"; exit 1; }
rm ./muttrc

CommandCount=$(pgrep -f "$1" -c)
if (( CommandCount < 2 )); then
  echo "No process with name like $1 was found. Stopping script..."
  exit 1
fi

echo "Start of monitoring loop"
while :
do
  if (( CommandCount < 2 )); then
    echo "ALARM! Looks like process $1 was killed or died. Sending message to monitoring and stop..."
    createMuttRc
    ( printf "ALARM! Looks like process %s was killed or died.\nTimestamp of event (taked from system clock) $(date +'%Y-%m-%d %H:%M:%S').\n" "$1" ) | mutt "$adminemail" -F "./muttrc" -s "Alarm while monitoring of $1"
    rm ./muttrc
    exit 3
  fi
  sleep 10s
done
