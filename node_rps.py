

# -*- coding: utf-8 -*-
class Node():
    def __init__(self,digit):
        self.infoSet = ''
        self.util = 0
        self.count = 0
        self.NA = 3
        self.regretSum =  [0 for _ in range(self.NA)]
        self.strategySum =  [0 for _ in range(self.NA)]
        self.digit = digit
        self.averageStrategy = [0 for _ in range(self.NA)]
        self.pruned_count = [0 for _ in range(self.NA)]
        self.strategy_update = 0
        self.p = 1
        
    ## nodeに紐づけられたregretSumのリストから、strategyを求める関数 
    def getStrategy(self):
        ## normalizingSumはstrategyの要素の和 割って合計を1にする。CFR(5)の式に対応している。    
        normalizingSum = 0
        strategy =  [0 for _ in range(self.NA)]
        for a in range(self.NA):
            strategy[a] = self.regretSum[a] if self.regretSum[a] > 0 else 0
            normalizingSum += strategy[a]
        
        for a in range(self.NA):
            if normalizingSum > 0:
                strategy[a] /= normalizingSum
            else:
                strategy[a]  = 1.0 / self.NA
        
        return strategy 

    ## strategySumの要素の和を1にして、最終的な平均戦略を求める関数 
    ## 11/30 残りカードが1枚しかないなら、そこの要素だけ1のリストを返せば良い。例：残りの手札が2だけ → strategyは[0,1,0]
    def getAverageStrategy(self):
        normalizingSum = 0
        for a in range(self.NA):
            normalizingSum += self.strategySum[a]
            
        for a in range(self.NA):
            if normalizingSum > 0:
                self.averageStrategy[a] = self.strategySum[a] / normalizingSum
            else:
                self.averageStrategy[a] = 1.0 / self.NA
        
        return self.averageStrategy
    
    ## 出力するための関数
    def toString(self):
        self.getAverageStrategy()
        avgStrategy = [round(self.averageStrategy[n], self.digit) for n in range(len(self.averageStrategy))]
        if self.count > 0:
            self.util = round(self.util / self.count, self.digit)
        return str(self.infoSet) + ' avgstrategy: ' + str(avgStrategy)  + ' regretSum: ' + str(self.regretSum)  + ' strategySum: ' + str(self.strategySum) + ' count: ' + str(self.count) + ' pruned_count: ' + str(self.pruned_count)

    ##hashとして保存するための関数
    def toHash(self):
        self.getAverageStrategy()
        node_hash = {}
        node_hash['infoSet'] = self.infoSet
        node_hash['avgStrategy'] = self.averageStrategy
        node_hash['util'] = self.util
        node_hash['regretSum'] = self.regretSum
        node_hash['strategySum'] = self.strategySum
        node_hash['pruned_count'] = self.pruned_count
        return node_hash
