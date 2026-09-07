#!/bin/bash

### This scripts renders the real address of a bit.ly link
### The link is supposed to be valid, no error gestion
### Allowed cmd = curl, grep, cut
### TEst link = https://bit.ly/46bE38J

url=$1
curl -sI "$url" | grep -i '^location:' | cut -d' ' -f2-
