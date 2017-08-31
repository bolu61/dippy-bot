from datetime import datetime
import re

from core import *

@command(ignore_kwargs = True, ignore_carry = True)
async def help(ctx, func: str):
    """Displays the reference manual for commands and aliases
    Usage: help <func:str>"""
    
    if func in aliases:
        doc = "'{}' is an alias for '{}'".format(func, aliases[func])

    elif func in commands:
        doc = "Manual entry for '{}' is empty".format(func)
        if commands[func].doc:
            doc = "'{}': {}".format(func, commands[func].doc)

    else:
        doc = "No manual entry for '{}'".format(func)
        raise FunctionException(doc)

    await ctx.say(doc)
    return doc

@command()
async def delMsg(ctx, *args, **kwargs):
    """Deletes the command message
    Usage: delMsg
    Return: 0"""

    try:
        await ctx.bot.delete_message(ctx.message)
        return 0
    except:
        raise FunctionException()

@command(ignore_carry = True, key_aliases = {"s": "silent"})
async def ping(ctx, msg, silent = False):
    """Returns the latency between the Server and the Bot
    Usage: ping [-s or -Silent]
    Return: ping"""

    local_time = datetime.now()
    ping_latency = (local_time - ctx.message.timestamp).microseconds // 1000
    if not silent:
        pong = await ctx.say('ping({}ms)'.format(str(ping_latency)))
        pong_latency = (pong.timestamp - local_time).microseconds // 1000
        await ctx.bot.edit_message(pong, '{} pong({}ms)'.format(pong.content, str(pong_latency)))
    return ping_latency

@command(key_aliases = {"carry": "formatstr", "s": "silent", "r", "raw"})
async def echo(ctx, message: str, silent = False, raw = False, formatstr = ""):
    """Displays text
    Usage: echo <msg:str>"""
    
    message = message.strip().format(formatstr)
    if not raw:
        message = re.sub("\s+", " ", message)
    if not silent:
        await ctx.say(message)
    return message
