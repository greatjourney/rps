# -*- coding: utf-8 -*-
import random
import copy
import datetime
import math
import time
import json
from node_rps import Node
from func_rps import make_infoset
from func_rps import make_action
from func_rps import judge
from func_rps import judge_2
from func_rps import train_pluribus
from func_rps import display_order
from func_rps import dump_hash
from func_rps import mccfr
from func_rps import cfr

## 12/1 モジュール化
digit = 5
iterations = 100
NA = 3

if __name__ == '__main__':
    ## logのアウトプット用ファイル作成
    for i in range(3,4):
        players = i
        dt_now = str(datetime.date.today()) + ' ' + str(datetime.datetime.now().hour) + ':' + str(datetime.datetime.now().minute) + ':' + str(datetime.datetime.now().second) 
        # logのアウトプット用ファイル作成
        file1 = "./学習記録3/" +  str(dt_now) +  " iterations: " + str(iterations) + " players: " + str(players)  + ".txt"
        file2 = "./log_Player_3/NA_" + str(NA) + "debug"  + str(dt_now) +" iterations: " + str(iterations) + " players: " + str(players) + ".txt"
        file3 = "./hash記録/" + str(dt_now)   + " players: " + str(players) + "iterations: " + str(iterations) +  ".json"
        f = open(file1, 'w')
        f.close()
        f = open(file3, 'w')
        f.close()
        ## ファイルの先頭に何かコメントをつけるなら。
        with open(file1, 'a') as f:
            print("実験 MCCFR strategy_intervalとLCFR_threshold, Discount_Intervalを使わない", file=f)
            print("iterations: " + str(iterations) + " NA: " + str(NA) + " players: " + str(players) + " : " + str(dt_now)  ,file=f)
        nodeMap = {}
        util = train_pluribus(iterations, players, file1, file2, NA, digit, nodeMap)
        display_order(iterations, players,util, digit, file1, file2, NA, nodeMap)
        dump_hash(file3, nodeMap)