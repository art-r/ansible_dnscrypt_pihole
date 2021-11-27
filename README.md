# ansible_dnscrypt_pihole
An automated pihole installation with dnscrypt-proxy2 as a dns upstream resolver using ansible

## Features:
Automated installation of:
- [Pi-hole](https://github.com/pi-hole/pi-hole)
- [dnscrypt-proxy](https://github.com/DNSCrypt/dnscrypt-proxy)
- Automated adlist setting and updating by installing and the script from [this awesome project](https://github.com/jacklul/pihole-updatelists) using all ticked and unticked adlists from [fireborg.net](https://firebog.net/)
- Automated whitelist setting and updating from [this awesome project](https://github.com/anudeepND/whitelist) using only the most common domains [whitelist.txt](https://raw.githubusercontent.com/anudeepND/whitelist/master/domains/whitelist.txt)


## How to run this:
1. Make sure ansible is installed on your system
> See https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html for further info
2. Copy the `hosts.example` file and rename the copy to `hosts`
3. Open the `hosts` file and edit the ip address to match the device that you want to install all of the stuff onto
4. Edit the `group_vars/all` file to match your preferences
> The default upstream server for dnscrypt-proxy will be [Quad9](https://www.quad9.net/) - you can change this by opening and editing line 32 in the file `files/dnscrypt-proxy/dnscrypt-proxy.toml` in accordance with this [tutorial](https://github.com/DNSCrypt/dnscrypt-proxy/wiki/Configuration-Sources). If however you are fine with quad9 (because it is awesome!) you do not have to touch that file
5. Replace the file `files/dnscrypt-proxy/dnscrypt-proxy` with the according binary for your target system from [here](https://github.com/DNSCrypt/dnscrypt-proxy/releases/tag/2.1.1)
> You will download a zip archive. Unzip it and **only** copy the file named `dnscrypt-proxy` to the `files/dnscrypt-proxy` directory. **Do not rename it!**
6. Make sure that your target system(s) are reachable via ssh from your local computer and that you can login there with your local ssh key (as explained [here](https://serverpilot.io/docs/how-to-use-ssh-public-key-authentication/)) or else modify the ansible-playbook as explained [here](https://docs.ansible.com/ansible/latest/user_guide/connection_details.html#) (this is however not recommended and if not done properly less secure than using the ssh-key-approach)
7. Run the playbook with the command:
```bash
ansible-playbook -i hosts playbook.yml
```
8. No you should connect to your target system(s) via ssh and also make the pihole web interface temporarily available on your local computer
> For security reasons the target machine will only have port 53 (dns) and port 22 (ssh) open - you will have to modify this if you want to always be able to access the pihole web interface or if you want to use the target machine for other purposes as well (e.g. use it as a DHCP server etc.)
```bash
ssh -L 8080:127.0.0.1:80 {remote-user}@{target machines address}
```
9. Open your browser and navigate to http://localhost:8080/admin and login to the pihole web interface (see [this](https://discourse.pi-hole.net/t/how-do-i-set-or-reset-the-web-interface-password/1328) if you do not know how to set a password)
10. Configure the pihole according to your needs. The following things are already configured:
- adlists (see Features) [they are updated every night via a cron job]
- whitelist (see Features) [they are updated every week via a cron job as they do not change very often]
- dns upstream to dnscrypt-proxy which is listening only locally on the target machine(s) and using quad9 as the upstream dns by default
11. Done
