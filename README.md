# Ansible Playbook for installing PiHole with dnscrypt-proxy2
An automated pihole installation with dnscrypt-proxy2 as a dns upstream resolver using ansible

> See progress & status of this project [in the projects kanban board](https://github.com/art-r/ansible_dnscrypt_pihole/projects/1)

***

## Features:
Automated installation:
- [Pi-hole](https://github.com/pi-hole/pi-hole)
- [dnscrypt-proxy](https://github.com/DNSCrypt/dnscrypt-proxy)
- Automated adlist setting and updating by installing and the script from [this awesome project](https://github.com/jacklul/pihole-updatelists) using all ticked and unticked adlists from [fireborg.net](https://firebog.net/)
- Automated whitelist setting and updating from [this awesome project](https://github.com/anudeepND/whitelist) using only the most common domains (as found here [whitelist.txt](https://raw.githubusercontent.com/anudeepND/whitelist/master/domains/whitelist.txt))

=> Pihole will work "out of the box" and should only require very little to no post-configuration (especially regarding adlists and whitelists as they should protect you as much as possible from ads etc. while breaking as little as possible)

## How to run this:
1. Make sure ansible is installed on your system
> See https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html for further info
2. Copy the `hosts.example` file and rename the copy to `hosts`
3. Open the `hosts` file and edit the ip address(es) to match the device(s) that you want to install all of the stuff onto
4. Edit the `group_vars/all` file to match your preferences (most of the times you will only have to edit the name of the ansible_ssh_user to match the user of your target system(s))
> The default upstream server for dnscrypt-proxy will be [Quad9](https://www.quad9.net/) - you can change this by opening and editing line 32 in the file `files/dnscrypt-proxy/dnscrypt-proxy.toml` in accordance with this [tutorial](https://github.com/DNSCrypt/dnscrypt-proxy/wiki/Configuration-Sources). If however you are fine with quad9 (because it is awesome!) you do not have to touch that file
5. Replace the file `files/dnscrypt-proxy/dnscrypt-proxy` with the according binary for your target system from [here](https://github.com/DNSCrypt/dnscrypt-proxy/releases/latest)
> You will download a zip archive from that link. Unzip it and **only** copy the file named `dnscrypt-proxy` to the `files/dnscrypt-proxy` directory. **Do not rename it!**
6. Make sure that your target system(s) are reachable via ssh from your local computer and that you can login to them with your local ssh key (as explained [here](https://serverpilot.io/docs/how-to-use-ssh-public-key-authentication/)) or else modify the ansible-playbook as explained [here](https://docs.ansible.com/ansible/latest/user_guide/connection_details.html#) (**not recommended as this is less secure**)
> Note that the remote user has to be able to execute commands as root (=> be able to use sudo!)
7. Now run the playbook with the command:
```bash
ansible-playbook -i hosts playbook.yml -u {name of remote user that ansible should use}
```
8. After the playbook has finished executing all tasks you should be able to connect to your target system(s) via ssh. To access the pihole web interface make it temporarily available on your local computer via the following command:
> For security reasons the target machine will only have port 53 (dns) and port 22 (ssh) open by default - you will have to modify this manually on the machine if for example you want to always be able to access the pihole web interface or if you want to use the target machine for other purposes as well (e.g. use it as a DHCP server etc.)
```bash
ssh -L 8080:127.0.0.1:80 {remote-user}@{target machines address}
```
9. Open your browser and navigate to http://localhost:8080/admin and login to the pihole web interface (see [this](https://discourse.pi-hole.net/t/how-do-i-set-or-reset-the-web-interface-password/1328) if you do not know how to set a password)
10. Configure the pihole according to your needs. The following things are already configured:
- adlists (see Features) [they are updated every night via a cron job]
- whitelist (see Features) [they are updated every week via a cron job as they do not change very often]
- dns upstream to dnscrypt-proxy which is listening only locally on the target machine(s) and using quad9 as the upstream dns by default
11. Now configure your router(s) (or clients) to also actually use pihole as their dns server
