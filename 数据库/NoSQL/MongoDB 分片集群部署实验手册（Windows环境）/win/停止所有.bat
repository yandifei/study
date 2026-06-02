@echo off
title Kill All MongoDB Processes
echo Killing all mongod.exe and mongos.exe...
taskkill /f /im mongod.exe >nul 2>&1
taskkill /f /im mongos.exe >nul 2>&1
echo Done.