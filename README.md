deaddrop
========

Working repository for the dead drop project


Example Communication
=====================

Here's a communication between senders Alice and Bob (this command line tool to store/retrieve from the drive is called `deaddrop` in this example):

* alice stops by the space to drop off a file on the drive
* 30GB tarball is encrypted using bob's public key to file `ss.gpg`

        alice$ gpg --encrypt --recipient 'bob' --output ss.gpg state-secrets.tar.gz

* alice stores ss.gpg
* deaddrop stores `0xDEADBEEF`, and the filesize, 30GB, in a row in the database
* deaddrop writes the file as a raw `byte[]` starting at `0xDEADBEEF` (conceptually)

        alice$ deaddrop --store ss.gpg
        OK, locator = 0xDEADBEEF
        alice$ 

* bob gets a text from alice on his phone: `0xDEADBEEF`, which is difficult to understand out of context
* bob visits the space and hooks up to drive
* bob accesses file at locator `0xDEADBEEF`

        bob$ deaddrop --retrieve 0xDEADBEEF --output tmp.encrypted
        OK, size = 30GB
        bob$

* bob can then decrypt the file (he also knows it's a tarball ahead of time)

        bob$ gpg --decrypt --output ss.tar.gz tmp.encrypted
        bob$ tar -xzvf ss.tar.gz
        bob$ 

This way, if Eve wants to intercept `ss.tar.gz`, Eve needs to know the locator (`0xDEADBEEF`).  

Even with this information, Eve doesn't know either who uploaded the file or who the intended recipient is, so it's not possible to decrypt the file.

As a bonus, if only one of either the sender or the recipient's private keys are compromised, then the file remains encrypted to Eve (if either the sender or recipient remain unknown to Eve).
