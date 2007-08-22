#coding=utf-8
"""
test keywords
"""
from zhpy import convertor

def test_print():
    """
    test output statement and string types
    """
    assert convertor("打印 'hello'") == "print 'hello'"
    assert convertor('打印 "hello"') == 'print "hello"'
    assert convertor("""打印 'hello'""") == "print 'hello'"

def test_input():
    """
    test input statement
    """
    assert convertor("name = 输入字符串('your name:')") == \
                    "name = raw_input('your name:')"

def test_variable():
    """
    variable is tested in keywords_tw
    """
    pass

def test_operators():
    """
    test operators
    """
    assert convertor("a 等于 b") == "a == b"
    assert convertor("a 不等于 b") == "a != b"

def test_def():
    """
    test definition
    """
    assert convertor("定义 hello(): 打印 'hello'") == "def hello(): print 'hello'"

def test_class():
    """
    test class
    """
    assert convertor("类 hello: 定义 hello(): 打印 'hello'") == \
                    "class hello: def hello(): print 'hello'"

def test_import():
    """
    test import statement with from/import/as
    """
    assert convertor("载入 sys") == "import sys"
    assert convertor("载入 sys 取名 unix") == "import sys as unix"
    assert convertor("从 os 载入 path 取名 url") == "from os import path as url"
