#!/usr/bin/python3

import os
import re

EPG_LIST = ( "https://iptv-org.github.io/epg/guides/bd.xml",
           )

class Channel():

    def __init__(self, group, md_line):
        self.group = group
        md_line = md_line.strip()
        try:
            (before, number, name, url, logo, epg, after) = md_line.split("|")
        except ValueError:
            (before, number, name, url, logo, after) = md_line.split("|")
            epg = None
        self.number = number.strip()
        self.name = name.strip()
        self.url = url.strip()
        self.url = self.url[self.url.find("(")+1:self.url.rfind(")")]
        self.logo = logo.strip()
        self.logo = self.logo[self.logo.find('src="')+5:self.logo.rfind('"')]
        self.epg = epg.strip() if epg else None

    def to_m3u_line(self):
        if self.epg is None:
            return (f'#EXTINF:-1 tvg-name="{self.name}" tvg-logo="{self.logo}" group-title="{self.group}",{self.name}\n{self.url}')
        else:
            return (f'#EXTINF:-1 tvg-name="{self.name}" tvg-logo="{self.logo}" tvg-id="{self.epg}" group-title="{self.group}",{self.name}\n{self.url}')

if __name__ == "__main__":
    with open("playlist.m3u8", "w", encoding='utf-8') as playlist:
        print(f'#EXTM3U x-tvg-url="{",".join(EPG_LIST)}"', file=playlist)
        os.chdir("lists")
        for filename in sorted(os.listdir(".")):
            if filename == "README.md" or not filename.endswith(".md"):
                continue
            with open(filename, encoding='utf-8') as markup_file:
                group = filename.replace(".md", "").title()
                print(f"Generating {group}")
                for line in markup_file:
                    if "<h1>" in line.lower() and "</h1>" in line.lower():
                        group = re.sub('<[^<>]+>', '', line.strip())
                    if not "[>]" in line:
                        continue
                    channel = Channel(group, line)
                    print(channel.to_m3u_line(), file=playlist)
