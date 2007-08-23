#!/usr/bin/python
# -*- coding: utf-8 -*-
"""zhpy is an convertor to translate chinese python code to nature python 
code (english) and vice versa.

zhpy refactored the origin code from HYRY.

fredlin 2007, gasolin+mopowg@gmail.com

This is the MIT license:
http://www.opensource.org/licenses/mit-license.php

Copyright (c) 2007 Fred Lin and contributors. zhpy is a trademark of Fred Lin.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
from pyparsing import *

# Traditional chinese and simplized chinese keywords
worddict = {"印出":"print", "輸入":"raw_input", #io
            "打印":"print", "输入字符串":"raw_input",
            "定義":"def", "類別":"class", #def
            "定义":"def", "类":"class",
            "共用":"global", "全局变量":"global", #global
            "從":"from", "導入":"import", "取名":"as", #import
            "从":"from", "载入":"import",
            "返回":"return", "傳回":"return", "略過":"pass", 
            "示警":"raise", "繼續":"continue", #flow
            "传回":"return", "略过":"pass", "继续":"continue",
            "如果":"if", "假使":"elif", "否則如果":"elif", "否則":"else",#control
            "若":"if", "否则如果":"elif", "否则":"else",
            "取":"for", "自":"in", "在":"in", "不在":"not in",#for loop
            "當":"while", "跳出":"break", "中止":"break",#while loop
            "当":"while", "中断":"break",
            "嘗試":"try", "異常":"except", "最後":"finally", #try
            "试运行":"try", "错误处理":"except",
            "宣告":"assert", "刪除":"del", "執行":"exec", #else
            "方程式":"lambda", "產生":"yield", "伴隨":"with",
            "函数":"lambda", "产生":"yield",
            "等於":"==", "不等於":"!=", "等于":"==", "不等于":"!=", #operators
            "是":"is", "為":"is", "不是":"is not", 
            "或":"or", "和":"and", "且":"and", #boolean
            "真": "True", "假":"False", "實": "True", "虛":"False", "空":"None",
            "实": "True",
            "型別":"type", "类型":"type",#build in methods
            "長度":"len" ,"长度":"len",
            "字串":"str", "字符串":"str", # build-in types
            "列表": "list", "字典":"dict", "數組":"tuple", "類組":"set",
            "数组":"tuple", "类组":"set",
            "整數":"int", "浮點數":"float",
            "整数":"int", "小数":"float",
            "開啟":"open", "打開":"open",
            "开启":"open", "打开":"open",
            "讀取":"read", "寫入":"write", #file methods
            "读取":"read", "写入":"write",
            "讀一行":"readline", "讀多行":"readlines",
            "读一行":"readline", "读多行":"readlines",
            "關閉":"close", "关闭":"close",
            "加入":"append", "追加":"append", #list methods
            "開始字串":"startswith", "結束字串":"endswith", #string methods
            "开始为":"startswith","结束为":"endswith",
            "接合":"join", "分離":"split",
            "分离":"split",
            "列出關鍵字":"keys","列出值":"values", "列出項目": "items", #dict methods
            "关键字列表":"keys", "值列表":"values", "项目列表":"items",
            "編碼":"encoding", "解碼":"decoding", #encoding
            "编码":"encoding", "解码":"decoding",
            "範圍":"range", "范围":"range", # preloaded modules
            }

replacedict = {
    "（":"(",
    "）":")",
    "。":".",
    """:'"',
    """:'"',
    "'":"'",
    "'":"'",
    "，":",",
    "：":":",
    "！":"!",
    }

def merger(anno_dict):
    """
    merge extra bindings into worddict
    
    merge could accept list input:
    
    >>> keys = [('遊戲', 'pygame'), ('系統', 'sys')]
    >>> merger(keys)
    add 遊戲=pygame
    add 系統=sys
    >>> '遊戲' in worddict
    True
    
    merge could accept dict input:
    
    >>> keydic = {'作業系統':'os', '路徑':'path'}
    >>> merger(keydic)
    add 路徑=path
    add 作業系統=os
    >>> '系統' in worddict
    True
    """
    if type(anno_dict) == type([]):
        for k,v in anno_dict:
            if k not in worddict:
                worddict[k] = v
                print "add %s=%s"%(k, v)
            else:
                print "already has key: %s, %s" % (k, v)
            
    if type(anno_dict) == type({}):
        for tmp in anno_dict.keys():
            if tmp not in worddict:
                worddict[tmp] = anno_dict[tmp]
                print "add %s=%s"%(tmp, anno_dict[tmp])
            else:
                print "already has key: %s, %s" % (tmp, anno_dict[tmp])

import os
import ConfigParser

def annotator():
    """
    provide two ways to expand the worddict:
    
    1. inifiles
        find ini files and use keywords defined in ini during 
        convertion progress.
    
    2. head docsting annotator（TODO）
    """
    #inifiles = [x for x in os.listdir(".") if x.endswith(".ini")]
    inifiles = []
    for x in os.listdir("."):
        if x.endswith(".ini"):
            inifiles.append(x)
    for f in inifiles:
        print "file", f
        conf = ConfigParser.ConfigParser()
        conf.read(f)
        sects = conf.sections()
        for sect in sects:
            print "sect:", sect
            merger(conf.items(sect))

def variable_to_number(tmp):
    """
    convert variable to hex number
    
    >>> '範例'.decode("utf8")
    u'\u7bc4\u4f8b'
    >>> s = '範例'.decode("utf8")
    >>> variable_to_number(s)
    '7bc4_4f8b'
    """
    #return 'p_' + '_'.join(map(lambda i:str(ord(i)), t[0])) + '_v'
    word_list=[]
    for i in tmp:
        ori = str(hex(ord(i)))[2:]
        word_list.append(ori)
    return "_".join(word_list)

#vnum = 0

def convertToEnglish(s,l,t):
    """search worddict to match keywords
    
    if not in keyword, replace the chinese variable/argument/
    function name/class name/method name to a variable with prefix 'p'
    
    TODO: able to convert code by annotate dict
    """
    #global vnum
    tmp = t[0].encode("utf8")
    """if tmp not in worddict:
        worddict[tmp] = "p_" + str(vnum)
        vnum += 1
    english = worddict[tmp]
    return english.decode("utf8")"""
    if tmp in worddict:
        return worddict[tmp].decode("utf8")
    else:
        return 'p_' + variable_to_number(t[0]) + '_v'
    
chineseChars = srange(r"[\0x0080-\0xfe00]")
#chineseChars = srange(r"[\0x2E80-\0x2FA1D]")
chineseWord = Word(chineseChars)
chineseWord.setParseAction(convertToEnglish)
pythonWord = quotedString | chineseWord

def convertor(test):
    """
    convert Chinese source to Python Source 
    
    >>> convertor("印出 'hello'")
    "print 'hello'"
    
    more keyword test cases are in /tests folder.
    """
    for k, v in replacedict.items():
        test = test.replace(k,v)
    
    utest = test.decode("utf8")
    result = pythonWord.transformString(utest)
    result = result.encode("utf8")
    return result

def try_run(result):
    """
    execute result and catch exceptions
    
    >>> try_run("print 'hello'")
    hello
    """
    try:
        exec result
    except Exception, e:
        print result
        s = str(e)
        print s
        for k, v in worddict.items():
            if "'" + v + "'" in s:
                print unicode(k,"utf8"), v
            if '"' + v + '"' in s:
                print unicode(k,"utf8"), v

def zh_exec(content):
    """
    the zhpy exec
    
    >>> zh_exec("印出 'hello'")
    hello
    """
    annotator()
    result = convertor(content)
    try_run(result)

def commandtool():
    """command line tool method
    
    input:
        speficy the input source
    output:
        speficy the output source
    python:
        compile to python and run
    raw:
        input raw zhpy source and run
    """
    import os
    import sys
    from optparse import OptionParser
    parser = OptionParser(
            usage="zhpy source [output]")
    parser.add_option("-i", "--input", 
            help="speficy the input source",
            dest="input", default = None)
    parser.add_option("-o", "--output", 
            help="speficy the output source",
            dest="output", default = None)
    parser.add_option("-p", "--python", 
            help="compile to python and run",
            dest="compile", default = None)
    parser.add_option("-r", "--raw", 
            help="input raw zhpy source and run",
            dest="raw", default = None)
    (options, args) = parser.parse_args()
    
    os.chdir(os.getcwd())
    #run as script
    if options.raw:
        test = options.raw
        annotator()
        result = convertor(test)
        try_run(result)
        return
    #run as command
    if len(sys.argv) >= 2:
        if (options.input is None) and sys.argv[1].endswith(".py"):
            options.input = sys.argv[1]
        if options.compile:
            options.input = options.compile
        #if options.input:
        test = file(options.input, "r").read()
        annotator()
        result = convertor(test)
        if len(sys.argv) == 3:
            if sys.argv[1].endswith(".py") and sys.argv[2].endswith(".py"):
                options.output = sys.argv[2]
            if options.compile:
                file("n_"+options.compile,"w").write(result)
                print "compile to python and run: %s"%("n_"+options.compile)
        if options.output:
            file(options.output,"w").write(result)
        else:
            try_run(result)
    else:
        print """please type "zhpy --help" for help"""
  
if __name__=="__main__":
    commandtool()