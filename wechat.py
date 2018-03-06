# This simple script is aimed to solve the problem that wechat has no auto-reply
# function for a specific timespan. The wechat api--itchat is in PyPI, so just
# install it with pip.

import os
import itchat
import datetime
from itchat.content import PICTURE, RECORDING, ATTACHMENT, VIDEO


message = "亲们[Joyful]我们现在下班啦。如有需要，请给我们留言，我们会尽快回复。谢谢！"
folder = os.path.join(os.path.expanduser('~'), "Desktop", "wechat_folder")
if not os.path.exists(folder):
    os.makedirs(folder)


@itchat.msg_register(itchat.content.TEXT)
def text_reply(msg, start=22, end=8, message=message):
    """
    Auto reply in a specific timespan for individual chat.

    Parameters
    ----------
    msg: dict
        A variable that comes from the wrapper function.
    start: int
        hour of the day in 24hr format representing the start of the auto reply.
    end: int
        hour of the day in 24hr format representing the end of the auto reply.
    message: str
        auto replied message.

    Returns
    -------
    a string of the auto-replied message.
    """

    now = datetime.datetime.now().time()
    starttime_for_auto_reply = datetime.time(hour=start)
    endtime_for_auto_reply = datetime.time(hour=end)

    if now >= starttime_for_auto_reply or now < endtime_for_auto_reply:
        return message


@itchat.msg_register(itchat.content.TEXT, isGroupChat=True)
def group_reply(msg, start=22, end=8, message=message):
    """
    Auto reply in a specific timespan for group chat.

    """

    now = datetime.datetime.now().time()
    starttime_for_auto_reply = datetime.time(hour=start)
    endtime_for_auto_reply = datetime.time(hour=end)

    if now >= starttime_for_auto_reply or now < endtime_for_auto_reply:
        if msg.isAt:
            return message


@itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO])
def download_files(msg):
    filepath = os.path.join(folder, msg.fileName)
    msg.download(filepath)

itchat.auto_login()
itchat.run()
