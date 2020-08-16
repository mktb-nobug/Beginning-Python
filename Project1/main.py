import sys, re
from handlers import *
from util import *
from rules import *


class Parser:
    """
    Parser读取文本文件，应用规则并控制处理程序
    """

    def __init__(self, handler):
        self.handler = handler
        self.rules = []
        self.filters = []

    def addRule(self, rule):
        self.rules.append(rule)

    def addFilter(self, pattern, name):
        def filter(block, handler):
            return re.sub(pattern, handler.sub(name), block)

        self.filters.append(filter)

    def parse(self, file):
        self.handler.start('document')
        for block in blocks(file):
            for filter in self.filters:
                block = filter(block, self.handler)
            for rule in self.rules:
                if rule.condition(block):
                    if rule.action(block, self.handler):
                        break

        self.handler.end('document')


class BasicTextParser(Parser):
    """
    在构造函数中添加规则和过滤器的Paraser子类
    """

    def __init__(self, handler):
        Parser.__init__(self, handler)
        self.addRule(ListRule())
        self.addRule(ListItemRule())
        self.addRule(TitleRule())
        self.addRule(HeadingRule())
        self.addRule(ParagraphRule())

        self.addFilter(r'\*(.+?)\*', 'emphasis')
        self.addFilter(r'(http://[\.a-zA-Z/]+)', 'url')
        self.addFilter(r'([\.a-zA-Z]+@[\.a-zA-Z]+[a-zA-Z])', 'mail')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    fin = open('test_input.txt', 'r')
    old_in = sys.stdin
    sys.stdin = fin

    fout = open('test_output.html', 'w')
    old_out = sys.stdout
    sys.stdout = fout

    handler = HTMLRenderer()
    parser = BasicTextParser(handler)

    parser.parse(sys.stdin)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
