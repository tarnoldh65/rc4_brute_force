from arc4 import ARC4
from math import log
import sys, getopt

# This is where all the work gets done
def main(argv):
    wordlibrary = ""
    ciphertext = ""

    # Get command line options
    try:
        opts, args = getopt.getopt(argv, "hf:c:", ["help", "filename=", "ciphertext="])
    except getopt.GetoptError:
        print (
            '''
            main.py -h -f <filename> -c <cipher text>
            try main.py -h for more options
            '''
        )
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(
            '''
            main.py <options>
            -h --help: This help output
            -f --filename: Name of password dictionary file (required)
            -c --ciphertext: Hex string to bruteforce decrypt (required)
            example:
              main.py -f libraryfile.txt -c 9e87fc9a...
            '''
            )
            sys.exit()
        elif opt in ("-f", "--filename"):
            wordlibrary = arg
        elif opt in ("-c", "--ciphertext"):
            ciphertext = bytes.fromhex(arg)

    # if no word library is provided end the program
    if wordlibrary == "":
        print(
            '''
            main.py -h -f <filename> -c <cipher text>
            try main.py -h for more options
            '''
        )
        sys.exit(3)
    else:
        # Open the word library and create a word list for brute force cracking
        wordfile = open(wordlibrary, 'r', encoding='ISO-8859-1')
        words = wordfile.readlines()

    # Iterate through the word list and test entropy - if 5 or below print results
    for word in words:
        decryptdata = decrypt_data(ciphertext, word.strip())

        try:
            entrpy = calc_shannon_entropy(decryptdata.decode())
        except:
            entrpy = calc_shannon_entropy(decryptdata)

        if entrpy <= 5:
            print ("Decrypted: ",decryptdata.decode())
            print ("Key: ",word.strip())
            print ("Entropy: ",entrpy)
            print ("-----------------------------------")

# Decrypt function
def decrypt_data(cipher_text, password):
    if len(password) > 0:
        arc4 = ARC4(bytes(password, 'ISO-8859-1'))
        return arc4.decrypt(cipher_text)
    else:
        return False

# Calculate entropy function
def calc_shannon_entropy(decryptedtext):
    """
    if entropy is between 3.5 and 5 this should be human text
    0 is no randomness. At 8 is encrypted/compressed.
    """
    try:
        if isinstance(decryptedtext, str):
            string = decryptedtext.encode("ascii")
        ent = 0.0
        if len(decryptedtext) < 2:
            return ent
        size = float(len(decryptedtext))
        for b in range(128):
            freq = decryptedtext.count(chr(b))
            if freq > 0:
                freq = float(freq) / size
                ent = ent + freq * log(freq, 2)
        return -ent
    except:
        return 8

# main
if __name__ == '__main__':
    main(sys.argv[1:])
