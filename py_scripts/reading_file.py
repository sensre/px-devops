#!/usr/bin/env python3

with open("example.txt") as file:
    for line in file:
        print(line.strip().upper())
