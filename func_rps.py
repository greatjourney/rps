import random
import copy
import time
import json
import datetime
import random
from node_rps import Node

## 0がグー 1がパー　2がチョキ'

def make_infoset(player):
    return 'for player ' + str(player)

def make_action(strategy):
        r = random.random()
        sum = 0
        for i in range(len(strategy)):
            if sum < r < sum + strategy[i]:
                return i 
            sum += strategy[i]

## 全員手を出し終えた後に得点を振り分ける関数
def judge(history, i):
    players = len(history)
    index_list = [[], [], []]
    for a in range(players):
        index_list[history[a]].append(a)
    ## グーをだした場合
    if history[i] == 0:
        if len(index_list[1]) == 0 and len(index_list[2]) == 0:
            return 0
        elif len(index_list[1]) == 0:
            return 1 / len(index_list[0])
        elif len(index_list[2]) == 0:
            return (- 1) / len(index_list[0])
        else:
            return 0
    ## パーをだした場合
    elif history[i] == 1:
        if len(index_list[0]) == 0 and len(index_list[2]) == 0:
            return 0
        elif len(index_list[2]) == 0:
            return 1 / len(index_list[1])
        elif len(index_list[0]) == 0:
            return (- 1) / len(index_list[1])
        else:
            return 0
    ## チョキをだした場合
    else:
        if len(index_list[0]) == 0 and len(index_list[1]) == 0:
            return 0
        elif len(index_list[0]) == 0:
            return 1 / len(index_list[2])
        elif len(index_list[1]) == 0:
            return (- 1) / len(index_list[2])
        else:
            return 0

#グーで勝ったら得点2倍　逆にチョキ出してグーに負けても失う点２倍
def judge_2(history, i):
    players = len(history)
    index_list = [[], [], []]
    for a in range(players):
        index_list[history[a]].append(a)
    ## グーをだした場合
    if history[i] == 0:
        if len(index_list[1]) == 0 and len(index_list[2]) == 0:
            return 0
        elif len(index_list[1]) == 0:
            return 2 / len(index_list[0])
        elif len(index_list[2]) == 0:
            return (- 1) / len(index_list[0])
        else:
            return 0
    ## パーをだした場合
    elif history[i] == 1:
        if len(index_list[0]) == 0 and len(index_list[2]) == 0:
            return 0
        elif len(index_list[2]) == 0:
            return 1 / len(index_list[1])
        elif len(index_list[0]) == 0:
            return (- 1) / len(index_list[1])
        else:
            return 0
    ## チョキをだした場合
    else:
        if len(index_list[0]) == 0 and len(index_list[1]) == 0:
            return 0
        elif len(index_list[0]) == 0:
            return 1 / len(index_list[2])
        elif len(index_list[1]) == 0:
            return (- 2) / len(index_list[2])
        else:
            return 0


def train_pluribus(iterations, players, file1, file2, NA, digit, nodeMap):
    util = [0 for _ in range(players)]
    strategyMap = {}
    start = time.time()
    for t in range(iterations):
        for i in range(players):               
            history = []
            p_list = [1 for _ in range(players)]
            util[i] += mccfr(history, i, t, p_list, nodeMap, strategyMap, players, digit, file1, file2,  NA)

    elapsed_time = time.time() - start
    with open(file1, 'a') as f:
        print('elapsed_time: ' + str(elapsed_time),file=f)
    return util

## 結果を出力するための関数
def display_order(iterations, players,util, digit, file1, file2, NA, nodeMap):
    diff = 0
    count_sum = 0
    strategy_update_count = 0
    nash = [1/3,1/3,1/3]
    for i in util:
        diff += pow((i / iterations) , 2)
    with open(file1, 'a') as f:
        for i in range(players):
            print("Average game values for player " + str(i) + ' : ' + str(round(util[i] / iterations, digit)) , file = f)
        for n in nodeMap.values():
            n.getAverageStrategy()
            count_sum += n.count
            strategy_update_count += n.strategy_update
        print("ナッシュ均衡との差 " + str(diff) ,file = f)
        print("総訪問回数 " + str(count_sum) ,file = f)
        print("strategy更新回数 " + str(strategy_update_count) ,file = f)
        for n in nodeMap.values():    
            print(n.toString(), file = f)

## 学習したnodeをjson形式で書き込む関数
def dump_hash(file3, nodeMap):
    has = {}
    for k in nodeMap.keys():
        has[k] = nodeMap[k].toHash()
    with open(file3, 'a') as f:
        print(json.dumps(has), file = f)

## external sampling MCCFRのアルゴリズム
def mccfr(history, i, t, p_list , nodeMap, strategyMap, players, digit, file1, file2,  NA):
    ## 今nターン目
    n = len(history)
    player = n % players

    if n == players:
        return judge(history, i)
        
    # infoSetを作成
    infoSet = make_infoset(player)

    # nodeMapにinfosetが既にあるならそれを引っ張ってくる。なければ新たにつくる。
    if infoSet in nodeMap:
        node = nodeMap[infoSet]
    else:
        node = Node(digit)
        node.infoSet = infoSet
        nodeMap[infoSet] = node

    # strategyにinformationsetとtの変数要素を組み込ませるために追加 11/5 問題ないはず
    # strategyKey = infoSet + ' : ' + str(t)
    # if strategyKey in strategyMap:
    #     strategy = copy.deepcopy(strategyMap[strategyKey])
        
    # else:
    #     strategyMap[strategyKey] = node.getStrategy()
    #     strategy = copy.deepcopy(strategyMap[strategyKey])

    strategy = node.getStrategy()
    util = [0 for _ in range(NA)]
    nodeUtil = 0
    if player == i:
        for a in range(NA):
            nexthistory = copy.deepcopy(history)
            nexthistory.append(a)  
            p_list[player] *= strategy[a]
            util[a] =  mccfr(nexthistory, i, t,  p_list, nodeMap, strategyMap, players, digit, file1, file2,  NA)  
            nodeUtil += strategy[a] * util[a]
        node.util += nodeUtil
        node.count += 1
        temp = copy.deepcopy(p_list)
        temp.pop(player)
        b = 1
        for j in temp:
            b *= j
        for a in range(NA):
            node.regretSum[a] += (b * (util[a] - nodeUtil)) 
            node.strategySum[a] += (p_list[player] * strategy[a])
            node.strategy_update += 1
        strategyMap[infoSet + ' : ' + str(t + 1)]  = node.getStrategy()
        return nodeUtil

    else:
        a = make_action(strategy)
        nexthistory = copy.deepcopy(history)
        nexthistory.append(a) 
        p_list[player] *= strategy[a]
        return mccfr(nexthistory, i, t,  p_list, nodeMap, strategyMap, players, digit, file1, file2,  NA)  

def cfr(history, i, t, p_list , nodeMap, strategyMap, players, digit, file1, file2,  NA):
    ## 今nターン目
    n = len(history)
    player = n % players

    if n == players:
        return judge(history, i)
        
    # infoSetを作成
    infoSet = make_infoset(player)

    # nodeMapにinfosetが既にあるならそれを引っ張ってくる。なければ新たにつくる。
    if infoSet in nodeMap:
        node = nodeMap[infoSet]
    else:
        node = Node(digit)
        node.infoSet = infoSet
        nodeMap[infoSet] = node

    # # strategyにinformationsetとtの変数要素を組み込ませるために追加 11/5 問題ないはず
    # strategyKey = infoSet + ' : ' + str(t)
    # if strategyKey in strategyMap:
    #     strategy = copy.deepcopy(strategyMap[strategyKey])
        
    # else:
    #     strategyMap[strategyKey] = node.getStrategy()
    #     strategy = copy.deepcopy(strategyMap[strategyKey])
    strategy = node.getStrategy()
    util = [0 for _ in range(NA)]
    nodeUtil = 0
    for a in range(NA):
        nexthistory = copy.deepcopy(history)
        nexthistory.append(a)  
        p_list[player] *= strategy[a]
        util[a] =  cfr(nexthistory, i, t,  p_list, nodeMap, strategyMap, players, digit, file1, file2,  NA)  
        nodeUtil += strategy[a] * util[a]
    node.util += nodeUtil
    node.count += 1

    if player == i:
        temp = copy.deepcopy(p_list)
        temp.pop(player)
        b = 1
        for j in temp:
            b *= j
        for a in range(NA):
            node.regretSum[a] += (b * (util[a] - nodeUtil)) 
            node.strategySum[a] += (p_list[player] * strategy[a])
            node.strategy_update += 1
        # strategyMap[infoSet + ' : ' + str(t + 1)]  = node.getStrategy()
    return nodeUtil

