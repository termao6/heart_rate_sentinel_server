# Heart Rate Sentinel Server
## As of 11/16 Midnight: - tagged release 1.0.0
* server.py has API endpoints that work locally (as tested through Postman)
## Update 3:00 - master branch
* added tests for API endpoints
  * there is something funny going on with importing functions from server.py that I'll look into again later (maybe)
## Update 11/17 Just before midnight - sendgrid branch
* should send an email when a new heart_rate entry shows that the patient is tachycardic
  * it works when the API key is directly inputted, but I haven't been able to figure out how to get the value from the environmental variables
  * Because it doesn't work exactly, this is on a branch without a new release tag.
* Next: Get server on VM
  * hopefully this can also solve the enviromental variable problem?
  * however, as of 11/17 10 PM, I have not been able to connect to the VCM even though I was able to yesterday.
  * This may be because I am off Duke wifi
  * Though it doesn't work even through the Duke VPN (if that's supposed to help?)
  * Because I am out of town with limited time to work, this may be looked at later (as in on Monday/Tuesday - if not for credit, then at least to absolve my own frustrations)
