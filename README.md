My 17th homework in OTUS online school on course "Linux system administrator".
For test access - connect to VM "Test" and try connect to 192.168.0.2 with usernames:
1) firstuser - can access anytime.
2) seconduser - can access only in period mon-fri and non-holidays (list of holidays is listed in bash array "holidays" in pam_script).
seconduser has some root privileges listed in https://jlk.fjfi.cvut.cz/arch/manpages/man/capabilities.7 (granted via CAP_SYS_ADMIN), but for typical system administrator in office there are useless.
