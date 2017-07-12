# slack-change-channel-creator

Extremely quick and dirty skript to create big channels with all relevant people when a global change happens.

Example: You update the core router and want all collueges in #operating to be informed. After the update you can Archive the channel, so nobody will be able to send messages to it anymore and you have a neat archive for alle big changes.

To use:
* Install the [slacker](https://github.com/os/slacker) library via `pip`
* [Get an API key](https://get.slack.help/hc/en-us/articles/215770388-Creating-and-regenerating-API-tokens)
* Create a file `apikey.txt`, containing your API key
* Create a file `blacklist.txt` containing the users who don't want to get invited into these channels (line seperated)
* Execute the script, passing the name of the channel where all users will be invited and the name from all users get invited, such as `./slack-change-channel-creator.py EN-1337 Operating`
* Sit back and let it do its work
