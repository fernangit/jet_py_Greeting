import random
import time
import jtalk
import utterance
import transfer

#起動時
def opening():
    jtalk.jtalk('えむず　あいさつユニット　しどうっ')

#独り言
def monologue(now_time, nxt_h, nxt_m):
    if now_time.hour == nxt_h and now_time.minute == nxt_m:
        #独り言再生
        mono = random.randint(0, len_utterance_mono_lst() - 1)
        jtalk.jtalk(utterance.mono_lst[mono])
#        print(monologue, utterance.mono_lst[monologue])
        #モーションズレ補正
        time.sleep(0.5)
        #口パク
        transfer.transfer_utterance(utterance.mono_lst[mono])
        time.sleep(3)
        nxt_h = now_time.hour + 1
        nxt_m = random.randint(0, 59)

    return nxt_h, nxt_m

#挨拶
def greeting(now_time, name, op):
    rnd = random.randint(0, 40)
    if (now_time.hour > 5) and (now_time.hour < 12):
        #午前
        if rnd > (len(utterance.mng_lst) - 1):
            utter = name + '　' + utterance.morning + '　' + op
        else:
            utter = name + '　' + utterance.mng_lst[rnd] + '　' + op
    else:
        #午後
        if rnd > (len(utterance.evg_lst) - 1):
            utter = name + '　' + utterance.evening + '　' + op
        else:
            utter = name + '　' + utterance.evg_lst[rnd] + '　' + op

    jtalk.jtalk(utter)
    return utter

def percentage_to_level(per, thresh, motion_num):
    return transfer.transfer_percentage(per, thresh, motion_num)

def level_to_utterance(level):
    return utterance.op_lst[level]

def len_utterance_mng_lst():
    return len(utterance.mng_lst)

def len_utterance_evg_lst():
    return len(utterance.evg_lst)

def len_utterance_mono_lst():
    return len(utterance.mono_lst)

def len_utterance_op_lst():
    return len(utterance.op_lst)

