#!/bin/bash
ps -ef | grep segment_server | awk '{print $2}' | xargs -I FF kill FF

