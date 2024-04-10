#!/usr/bin/env python3
import sys

def main():
    if len(sys.argv) == 1: # if no arg
        print ("Usage: python ... [e|d]")
        sys.exit(0)

    is_encrypt = sys.argv[1].upper() == 'E'

    cipher_file = "cipher_file.csv"
    cipher_dict = {}

    with open(cipher_file,'r') as f:
        if is_encrypt:
            cipher_dict = dict([[x.strip() for x in line.split(',')] for line in f])
        else:
            cipher_dict = dict([reversed([x.strip() for x in line.split(',')]) for line in f])

    for line in sys.stdin:
        outline = ""
        for c in line.strip():
            outline += cipher_dict.get(c, c)
        print(outline)

if __name__ == '__main__':
    main()
