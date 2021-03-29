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
  * *Reaction roles:*
    * Reaction roles are reactions that give you a role set by the admins of the server. Once you react with it, you get it. Once you unreact with it, it's gone. You obviously can't put an emote that the bot can't reach (emotes out of the server), but you can put custom emotes in the server along with default emotes. There's a bug that doesn't allow for animated emotes though, so don't use that.
  * *Interacting with Elements:*
    * You can make the bot send messages, DM's, edit messages, reply to messages, edit replies, react to a message, unreact to a message, and make it send an embed. One of my friends' server admins love this feature so I think it's a good one.
  * *Poll System:*
    * This doesn't need any configuration, just tell it where to send, what title to set, and the options! And you'll have a poll ready with reactions.
  * *Private Admin Communication System **(PACS)**:*
    * If users have a problem or want to report someone, it's good to have a private environment with the admins of the server, so I've made a system for that! No need to ping an admin for something, then not respond, then ping another one, and by the time they're both back, the problem's already solved. Just use the **PACS**!
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
* `.updates`: Sends the latest update that Captain Ravioli sent.

More shit's coming later, I have no time for this.
