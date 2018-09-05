
def echo(bot, event):
    parsed_text = event.text.split(' ', 2)

    #check for text after echo command
    if(len(parsed_text) > 2):
        message = parsed_text[2]
        bot.message(message, event.where)
    else:
        bot.message('?', event.where)

