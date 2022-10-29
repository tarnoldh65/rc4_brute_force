# rc4_brute_force
RC4 brute force python script

This script can be used to decrypt a line of RC4 encrypted data in hex format and any word/password list of choice.

I tested the script using the rockyou.txt word list.
```
Script usage:
main.py <options>
-h --help: This help output
-f --filename: Name of password dictionary file (required)
-c --ciphertext: Hex string to bruteforce decrypt (required)
example:
   main.py -f libraryfile.txt -c 9e87fc9a...
```
