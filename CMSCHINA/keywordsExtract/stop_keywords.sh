#!/bin/bash
ps -ef | grep keywords_server  | awk '{print $2}' | xargs -I FF kill FF
