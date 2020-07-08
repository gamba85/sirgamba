# -*- coding: utf-8 -*-
from datetime import datetime
from stat import *
import io
import os
import re
import sys

import xbmc
import xbmcaddon


addon = xbmcaddon.Addon()
profile = xbmc.translatePath(addon.getAddonInfo('profile').decode('utf-8'))

if not os.path.exists(profile):
    os.makedirs(profile)


def convertContent(fileContents2):
    fileContents = fileContents2.encode('utf-8')
    fileContents = fileContents.split('\n')
    srt_fileContents = ''
    counter = 1
    cue_flag = False
    cue = ''

    # iterate through every line
    for line in fileContents:
        if isTimingLine(line) and not cue_flag:
            line_clean = cleanTimingLine(line)
            if line_clean != '':
                cue_flag = True
                srt_fileContents += str(counter) + '\n' + line_clean + '\n'
                counter += 1
        elif cue_flag:
            if isTimingLine(line) or str(line) == '':
                srt_fileContents += cleanCueLine(cue)
                srt_fileContents += '\n'
                cue_flag = False
                cue = ''
            else:
                cue += line + '\n'

    try:
        srt_fileContents = srt_fileContents.encode('utf-8')
    except:
        pass

    return srt_fileContents


def isTimingLine(line):
    if len(line) > 6 and '-->' in line:
        # return True if the line starts like a timing line and conatins an
        # '-->'
        return (line[0].isdigit() and ':' in line and '-->' in line)
    else:
        return False

# removes any extra stuff that is not required


def cleanTimingLine(line):
    clean_line = ""
    times_str = re.findall(
        '\s*([\d\:\.]{1,})\s*-->\s*([\d\:\.]{1,})\s*', line, re.I)
    if len(times_str) == 1:
        times_str = times_str[0]
        if len(times_str) == 2:
            times_i = '00:00:00,000'
            times_i = times_i[0:12 - len(times_str[0])] + \
                times_str[0].replace('.', ',')
            times_f = '00:00:00,000'
            times_f = times_f[0:12 - len(times_str[1])] + \
                times_str[1].replace('.', ',')
            return times_i + ' --> ' + times_f
    return ''

# removes the '\n' in the cue, removes any tags
# and returns the cue as single line with a '\n' at the end


def cleanCueLine(lines):
    tag_flag = False
    lines = lines.replace('&amp;', '&').replace('&lt;', '<').replace(
        '&gt;', '>').replace('&lrm;', '').replace('&rlm;', '').replace('&nbsp;', ' ')
    return lines.strip('\n') + '\n'
