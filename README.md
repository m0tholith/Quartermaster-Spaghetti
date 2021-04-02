# This is Quartermaster Spaghetti!
Quartermaster Spaghetti is ~~my brother~~ a bot created by me. It has a variety of commands and features, which I'll be going through here.

**Features:**
  * *The XP System:*
    * This XP system is used with a custom Level system and an arguably lazy database system that I'll explain later. The XP system doesn't count every message sent by a member and gives XP. Instead, it gets their ID into a dictionary for `x` amount of seconds and then removes it. Once another message is sent, the bot checks if the sender's ID is in that dictionary. If it's not, then it adds some XP to that user and goes over the dictionary process I explained earlier. 
  * *The Leveling System:*
    * The leveling system is a system that depends on the XP system and the database for giving leveling roles to users. On every message and after XP is added, the bot checks the sender's XP and adds all levels that are available and removes the ones that arent (The reason for this is that admins can remove XP from a member, so some levels may need to be removed).
  * *Games:*
    * Currently, there are 3 realeased games: Tic Tac Toe, Battleship, and Minesweeper. There's currently one that I'm working on which is Hangman, but it'll take a bit to release. 
  * *The Warning System:*
    * This is one that's pretty straight-forward. You can add a warning to someone, remove it, clear their warnings, and check their warnings. That's it.
  * *The Updates System:*
    * The updates system is only usable by me, what it does is just enable me to notify people for 5 minutes about an update. Look for the command `newupdate` with the Search in your IDE or Notepad or whatever, to find the set ID and change it if you want.
  * *Interacting with Elements:*
    * You can make the bot send messages, DM's, edit messages, reply to messages, edit replies, react to a message, unreact to a message, and make it send an embed. One of my friends' server admins love this feature so I think it's a good one.
  * *Poll System:*
    * This doesn't need any configuration, just tell it where to send, what title to set, and the options! And you'll have a poll ready with reactions.
  * *Private Staff Communication System **(PSCS)**:*
    * If users have a problem or want to report someone, it's good to have a private environment with the admins of the server, so I've made a system for that! No need to ping an admin for something, then not respond, then ping another one, and by the time they're both back, the problem's already solved. Just use the **PSCS**!
    * **TL;DR:** ModMail with a fancier name.
    
## Now that we're done with the features, let's get to **every single command!**

### Global Commands:
* `.help / .about`: Displays the help command and some links to useful resources, like the [invite link](https://discord.com/api/oauth2/authorize?client_id=800620274609160192&permissions=470281334&scope=bot) and [support server invite](https://discord.gg/meHhGmKAqR) ***~~don't forget your [free nitro!](https://bit.ly/IqT6zt)~~***
* `.ping / .pong`: Displays the bot's latency from the host's device to Discord's API.
* `.avatar <(optional) user_ping>`: Sends the avatar of either the sender or the mentioned user.
* `.userinfo / .ui <(optional) user_ping>`: Shows some information about either the sender or the mentioned user.
* `.serverinfo / .si`: Sends some info about the server in which the command was sent.
* `.showwarns / .warns / .warnings / .showwarnings <(optional) user_ping>`: Shows the warnings of either the sender or the mentioned user.
* `.leaderboard`: Shows the leaderboard of the server in which the command was sent.
* `.level`: Shows the sender's level information.
* `.covid <country_name>`: Sends some COVID-19 information about the country. By default, the global information is chosen.
* `.covidcountrylist`: Shows a list of supported country names.
* `.ascii <(optional) user_ping>`: Converts the sender's logo to an ASCII text file.
* `.updates`: Sends the latest update that Captain Ravioli sent.

### Admin Commands 1:
* `changenick / .nick <user_to_change_nickname_mention> <new_nickname>`: Changes the mentioned user's nickname.
* `.mute <user_ping> <time_to_mute><timespan_abbreviation> <reason>`: Mutes the mentioned user for a specified amount of time. `<timespan_abbreviation>` can be `s`, `min`, `h`, `d`, `wk`, `mon`, and `y`.
* `.unmute <user_ping>`: Unmutes the mentioned user.
* `.warn <user_ping> <reason>`: Warns the mentioned user.
* `.removewarn / .remwarn <user_ping> <index>`: Removes the n'th warning of the mentioned user.
* `.clearwarns <user_ping>`: Clears all warnings of the mentioned user.
* `.addxp <user_mention> <xp_num>`: Adds the specified number of XP to the mentioned user.
* `.removexp / .remxp <user_mention> <xp_num>`: Removes the specified number of XP from the mentioned user.
* `.clearxp <user_mention>`: Resets the mentioned user's XP to 0.
* `.clearallxp`: Clears everyone's XP in the server.
* `.addreactionrole <message_link> <role_id/name> <emoji>`: Adds a reaction role to the message. There's a bug that doesn't check for animated emojis, so don't use them. Other custom emojis in the server or unicode emojis are okay.
* `.remreactionrole <role_id/name>`: Removes the reaction role. If you pass in a role that doesn't exist, there won't be any problems.
* `.reactionroles`: Gets the reaction roles. Gives "None" if none are set.
* `.clearreactionroles`: Clears all of the reaction roles in the server.

### Admin Commands 2:
* `.sendmessage / .sendmsg <channel_mention> <message_to_send>`: Sends the desired message in the mentioned channel.
* `.editmessage / .editmsg <message_link> <new_message>`: Edits the linked messsage to the new message.
* `.senddm <user_ping>`: Sends a DM to the mentioned user.
* `.embed / .sendembed <channel_mention> <r> <g> <b> <description_indicator> <title> <description_indicator> <description>`: Sends an embed to the mentioned channel with the specified RGB values, and the title and description known with the indicator. Each element must have "" around it.
* `.poll / .sendpoll <channel_ping> "<title>" "<option_1>" "<option_2>" (optional:) "<option_3-10>"`: Sends a poll to the mentioned channel with the title and options. Each element must have "" around it.
* `.react <message_link> <emoji>`: Reacts to the linked message. You can only use defaule emojis.
* `.unreact <message_link> <emoji>`: Removes the bot's reaction from the linked message. You can only use default emojis or emojis in the server.
* `.slowmode <slowmode>`: Sets the slowmode in the channel in which the command was sent in.
* `.purge <amount>`: Deletes the latest amount of messages in the channel that the command was called in.
* `.kick <user_ping> <reason>`: Kicks the mentioned user.
* `.ban <user_ping> <reason>`: Bans the mentioned user.
* `.lockdown <reason>`: Locks all server channels, making admins the only people able to send messages.
* `.unlock`: Unlocks the channel the command was sent in, making everyone but muted users able to send messages.

### PSCS:
* `.mail <server_id>`: Sends a message to the admins of the server.
* `.closemail <server_id>`: Closes the conversation between the sender and the admins of the server.
##### Detailed Explanation:
* What's an ID and how do I get it?
  * An ID is a unique number for every message, member, role, server, etc. and is used to identify certain things. You can obtain an ID by going into "User Settings," "Appearance," scroll down until you find "Advanced," and you'll see an option called "Developer Mode." Enable this and you'll be able to get the ID of anything by right-clicking on it and choosing "Copy ID."
* Admins will see a new category called "Mail," and inside it is a channel with your ID. They can send any message in the channel and it will get sent to you as a DM. You can reply with .mail <server_id> in DM's as I said before.
After you're done with mailing the admins, you can close the mail with the .closemail <server_id> command in the bot's DM's, which will delete the channel with your ID.

### Games:
* *Tic Tac Toe:*
  * `.tictactoe / .ttt <user_ping>`: Challenges the mentioned user to a Tic Tac Toe game.
  * `.accepttictactoe / .acceptttt`: Accepts the challenge and starts a Tic Tac Toe Game.
  * `.canceltictactoe / .cancelttt`: Declines the challenge.
  
  * You can't challenge someone that's already challenged. You can't challenge someone while you're already challenged. You can't chllenge a bot. You can't "challenge yourself, dumbass."

* *Single-Player Battleship:*
* `.battleship / .bs`: Starts a new Battleship Game and abandons the previous one.
* `.shoot / .shootbs / .bsshoot <x_position> <y_position>`: Shoots at the specified position.

* The board is 6x6 units. There are 4 1x1 ships. You have 20 chances to get all ships. The X and Y input of .shoot should be numbers that are more than 0 and less than or equal to 6.

* *Minesweeper:*
  * `.minesweeper <dimension_size (default: 10)> <num_bombs (default: 10)>`: Starts a new Minesweeper game and abandons any previous games.
  * `.d <x> <y>`: Digs at that position.
  * `.f <x> <y>`: Toggles a flag at that position.
  * `.end`: Ends the game.

  * The minimum dimension size is 5, and the maximun is 12 due to Discord limitations. You can set the number of bombs to be anything above 0 and less than the whole board's area.

* *Hangman:*
  * `.hangman`: Starts a new Hangman game.

  * To play, start a game and guess a letter or word by sending one. That's it!

# Have fun stealing my shit code!
