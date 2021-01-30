# poketwo-autocatcher
 
Automatically catch pokemon from the poketwo discord bot (https://github.com/oliver-ni/poketwo)

Keep the main exe file and the information.txt in the same folder

SETUP:

Channel ID: 
  Enable discord developer mode 
  Right click the channel where you want to catch pokemon and click copy ID
  Paste the ID in the Channel ID section in the information.txt file

Authorization:
  Open any place in discord where you can send a message
  Press CTRL + SHIFT + I to open up the inspect panel.
  Navigate to the "Network" tab at the top
  Send any message into discord
  Click on the "message" item that appears
  Navigate to the tab "Headers" that shows up after clicking "message"
  Look for "authorization: <some string of characters here>" under the "Request Headers" tab
  Copy the string of characters and paste it into the Authorization section in the information.txt file
 
Bot Token:
  Go to https://discord.com/developers
  Create a new application and name it whatever you want (This will be the name of your bot)
  Navigate to the "Bot" section of the application and create a new bot
  Copy the token and paste it into the information.txt file
  
 Go to the "OAuth2" section of the application
 Select the "Bot" checkbox in the "Scopes" section
 Copy the url that is generated
 Use this URL to invite your bot to your server
 
Invite poketwo in your server as well and start the exe file.
