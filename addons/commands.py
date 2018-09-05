from .echo import echo

def help(bot, event):
    """
    Gives list of bot commands and their usage - usage: @[bot] help
    """
    helplist = ''
    for k,v in commands_ref.items():
        helplist += "{}: {}\n".format(k, v.__doc__)

    helplist += "source: https://github.com/radderic/Improved-SlackBot\n"
    bot.message(helplist, event.where)

commands_ref = {
    "echo": echo,
    "help": help,
}


