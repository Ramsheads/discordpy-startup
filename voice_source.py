import discord
import re

def raw_or(s):
    if not isinstance(s, (list, tuple)):
        raise TypeError("Require list or tuple. Receive {}".format(type(s)))
    ret = r""
    for i, d in enumerate(s):
        if (i+1) == len(s):
            break
        ret = ret + r"{}|".format(d)
    ret = ret + r"{}".format(s[-1])
    return ret

class VoiceSource:
    def __init__(self, bot, path, default_vol=0.25, pattern="", msg=""):
        self.bot=bot

        if not isinstance(path, str):
            raise TypeError("path should be str")
        self.path=path

        if not isinstance(default_vol, (int, float)):
            raise TypeError("default_vol should be int or float")
        if default_vol < 0 or default_vol > 1:
            raise ValueError("default_vol should be 0.0 ~ 1.0")
        self.default_vol=default_vol

        if not isinstance(pattern, str):
            raise TypeError("pattern should be str")
        self.pattern=pattern
    
        if not isinstance(msg, str):
            raise TypeError("msg should be str")
        self.msg=msg

        self.__set_src__()
        self.__set_regex__()
    
    def __set_src__(self):
        self._file=open(self.path, "rb")
        self._src=discord.PCMVolumeTransformer(
            discord.PCMAudio(self._file),
            volume=self.default_vol
        )
    
    def __set_regex__(self):
        self._regex=re.compile(self.pattern)

    #FIXME: Need to use on multiple servers
    def play(self):
        for vc in self.bot.voice_clients:
            if vc.is_playing():
                vc.stop()
            self._src.cleanup()
            self._file.seek(0)
            vc.play(
                self._src,
                after=lambda e: print(
                    "ERROR {}: {}".format(self.path, e)))
    
    def check_play(self, ctx):
        if re.search(self._regex, ctx.content):
            if self.bot.voice_clients:
                self.play()
            return True
        return False
