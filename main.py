#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'nunosilva'
__author__ = 'github.com/craked5'

from httputil import SteamBotHttp
from json_recent import SteamJsonRecent
from json_item import SteamJsonItem
from json_recent_thread import SteamJsonRecentThreading
import time
import sys
import os
import signal

list_median_prices = {}
print 'HAI WELCOME TO THIS SHITTY BOT!!!!!!!!!!!!!! :D'
http_interval = raw_input('What time interval do you want the queries to be on RECENT? (number only please)\n')
http_interval = float(http_interval)
http_interval_item = raw_input('And on an individual item: \n')
http_interval_item = float(http_interval_item)
n_threads = raw_input('How many threads do you wish to run? \n')
print '\n'
print "OK now time one of the following commands: startsell ,startnosell ,buy ,sell , showlist, add, delete, login\n"
http = SteamBotHttp()
js = SteamJsonRecent()
fork_list = []
commands = ['startsell','buyinditem','howmanyprocs','showlistprocs','killproc','add','login','showlist','delete','quit','sell','loadmedianprices','getmedianprices']

'''
#STARTBUYINGSELL NUMBER 2 NO BULLSHIT CODES
#temp_resp e a resposta do seeifbuy
#temp[0] = True
#temp[1] = assetid
#temp[2] = price
'''

def startbuyinditem(item_buy,proc_name):
    jsind = SteamJsonItem(item_buy)
    i = 0
    sleep_time_down = 165
    while True:
        #start = time.time()
        item = jsind.urlqueryspecificitemind(item_buy)
        if item == False:
            jsind.setdownstate(1)
            if jsind.getdownstate() == 1:
                sleep_time_down += 15
                print "CONN REFUSED" + ' on item ' + item_buy + ' at try ' + str(i)+ ', sleeping for ' + str(sleep_time_down)
                time.sleep(sleep_time_down)
            pass
        elif type(item) == dict:
            jsind.setdownstate(0)
            sleep_time_down = 165
            jsind.getitemtotalready(item)
            jsind.getfinalitem()
            resp = jsind.seeifbuyinggood()
            if resp[0] is True:
                price_sell = temp[1]
                price_sell = float(price_sell*0.90)
                price_sell = "{0:.2f}".format(price_sell)
                print "OK SELLING ITEM"
                temp_one = jsind.getpositiononeiteminv()
                sell_response = jsind.sellitem(temp_one,temp[1])
                if sell_response[0] == 200:
                    jsind.writetowalletadd(price_sell)
                    jsind.writetosellfile(sell_response[0],sell_response[1],resp[2],price_sell,js.getwalletbalance())
                elif sell_response[0] == 502:
                    jsind.writetosellfile(sell_response[0],sell_response[1],resp[2],price_sell,js.getwalletbalance())
            if i % 10 == 0:
                print proc_name + ' is still kicking ass, let me work please! ty<3'
            i += 1
            time.sleep(http_interval_item)
            #elapsed = time.time()
            #elapsed = elapsed - start
            #print 'O TEMPO DO '+ proc_name + ' FOI DE ' + str(elapsed)
        else:
            if i % 10 == 0:
                print proc_name + ' is still kicking ass, let me work please! ty<3'
            i += 1
            time.sleep(http_interval_item)
            #elapsed = time.time()
            #elapsed = elapsed - start
            #print 'O TEMPO DO '+ proc_name + ' FOI DE ' + str(elapsed)


try:
    process_items = {}
    while True:
        try:
            temp = raw_input('Insira o comando que pretende usar: ')
            temp = temp.split(' ')

            if temp[0] == 'login':
                http.login()

            elif temp[0] == 'logout':
                http.logout()

            elif temp[0] == 'getmedianprices':
                list_median_prices = js.getmedianitemlist()
                print list_median_prices

            elif temp[0] == 'loadmedianprices':
                list_median_prices = js.loadmedianpricesfromfile()
                print list_median_prices

            elif temp[0] == 'dump':
                js.exportJsonToFile(js.list_median_prices)

            elif temp[0] == 'startsell':
                print "STARTING BUYING AND SELLING MODE"
                print "CTRL+C to stop!!!!!"
                newpid = os.fork()
                fork_list.append(newpid)
                if newpid == 0:
                    time.sleep(2)
                    js.startbuyingsell(http_interval)
                else:
                    pids = (os.getpid(), newpid)
                    print "parent: %d, child: %d" % pids

            elif temp[0] == 'startsellt':
                print "STARTING BUYING AND SELLING MODE"
                print "CTRL+C to stop!!!!!"
                jst = SteamJsonRecentThreading(list_median_prices)
                jst.list_median_prices
                newpid = os.fork()
                fork_list.append(newpid)
                if newpid == 0:
                    time.sleep(2)
                    jst.executethreads(n_threads,http_interval)
                else:
                    pids = (os.getpid(), newpid)
                    print "parent: %d, child: %d" % pids

            elif temp[0] == 'showlist':
                print 'This is the item list: '
                print js.getlistbuyitems()

            elif temp[0] == 'delete':
                item_rem = raw_input('Item to remove from the list: ')
                js.delInItemsTxt(item_rem)

            elif temp[0] == 'add':
                item_add = raw_input('Item to add to the list: ')
                js.writeInItemsTxt(item_add)

            elif temp[0] == 'sell':
                js.sellitemtest(temp[1], float(temp[2]))

            elif temp[0] == 'balance':
                print js.getwalletbalance()

            elif temp[0] == 'buy':
                js.buyitemtest(temp[1],temp[2],int(temp[3]),int(temp[4]),int(temp[5]))

            elif temp[0] == 'procs':
                for n_proc in process_items:
                    print n_proc + '  ' + str(process_items[n_proc])
                print fork_list

            elif temp[0] == 'killproc':
                proctokill = raw_input('Insira o nome do processo para matar (faca showlistproc se nao souber): ')
                for proc in process_items.keys():
                    if proc == proctokill:
                        os.kill(int(process_items[proc]),signal.SIGKILL)
                        fork_list.remove(process_items[proc])
                        process_items.pop(proc)
                        print "MATOU O PROCESSO PARA COMPRAR e VENDER O ITEM " + proc
                        break

            elif temp[0] == 'howmanyprocs':
                print 'EXISTEM ' + str(len(process_items.keys())) + ' PROCESSOS A FUNCIONAR\n'

            elif temp[0] == 'buyinditem':
                proc_name = raw_input("Insira o nome do processo (normalmente algo relacionado com a arma: \n")
                item_name = raw_input('Insira o nome da arma a comprar: \n')
                process_items[proc_name] = os.fork()
                fork_list.append(process_items[proc_name])
                print process_items
                if process_items[proc_name] == 0:
                    time.sleep(2)
                    startbuyinditem(item_name,proc_name)
                else:
                    pids = (os.getpid(), process_items[proc_name])
                    print "parent: %d, child: %d" % pids

            elif temp[0] == 'quit':
                print "User saiu"
                for p in fork_list:
                    os.kill(p,signal.SIGKILL)
                    print 'MATEI O PROCESSO ' + str(p)
                sys.exit()
            else:
                print "Command not valid, please try again!"
        except KeyboardInterrupt:
            print '\n'
            print "User saiu"
            for p in fork_list:
                os.kill(p,signal.SIGKILL)
                sys.exit()
except KeyboardInterrupt:
    print '\n'
    print "user saiu"

