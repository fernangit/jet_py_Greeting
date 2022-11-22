# -*- coding: utf-8 -*-
import os, sys, errno
import time
import jtalk
import utterance

for i in utterance.mono_lst:
    print(i)
    jtalk.jtalk(i)
    time.sleep(3)
for i in utterance.mng_lst:
    print(i)
    jtalk.jtalk(i)
    time.sleep(1)
for i in utterance.evg_lst:
    print(i)
    jtalk.jtalk(i)
    time.sleep(1)
