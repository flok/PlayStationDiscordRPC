# PlayStationDiscordRPC

# **Project Abandoned due to the official release PlayStation Network for Discord as a connection Service**



-------------------------------------------------------------------------------------------------------------------

PlayStation Discord RPC Client is a Qt TrayIcon application that fetches the current gaming status of the associated account and display the GameTitle and Image on your Discord Profile using the RPC Framework.

# Supported Games

Since the latest discord update it allowes the usage of image links as a image_id which results in support for all available games on the PS network without keeping a seperate database available.

# Installation

You can find the latest version of PlayStationDiscordRPC under [Releases](https://github.com/flok/PlayStationDiscordRPC/releases). Just download the executable and place it in some folder. Start the app and you will be directed to the settings page. At the same time a tray icon will appear which gives you the options to stop the service or head to the settings page again.

# How it works

The app continously fetched the current status of your PSN profile from the PSN site and displays the game as a Discord status.

Below you see a game displayed as a status inside discord including the game icon picture and the status popup which is also availabe from double clicking the tray icon

|         Discord Status                      |                Status Popup                 |
|---------------------------------------------|---------------------------------------------|
| <img src="https://i.imgur.com/kVRAESs.png"> | <img src="https://i.imgur.com/7nxJDrh.png"> |
