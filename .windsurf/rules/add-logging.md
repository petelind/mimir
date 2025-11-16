---
trigger: always_on
---

Always add app.log into the application and a logger and file handler which will rotate the log on every app relaunch.
Always add extensive logging on the info level so we can troubleshoot who was doing what with which data when the error X occured.
Use logs/app.log to check for errors when app is not running as expected.
For the UI functions - use console.log to show the flow - decisions made, actions taken, results received etc.