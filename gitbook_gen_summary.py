"""
    通过已有文件自动生成 SUMMARY.md 文件内容。

    使用：启动时传入gitbook所在路径即可。
"""
import sys
import os

SUMMARY = 'SUMMARY.md'  # SUMMARY.md 的文件名

# 以下变量可以根据需要自定义
SUMMARY_TITLE = '# 目录'  # SUMMARY.md 文件中的开头
SUMMARY_CONT = '{s}* [{name}]({link})\n'  # SUMMARY.md 中的内容格式，可以自定义 * 为 - ，其他不能动
README = 'README.md'  # readme文件的名字，程序会检索各级文件夹，如果其中没有这个名字的readme文件，会自动生成一个
README_CONT = '# 说明'  # 程序自动生成readme文件时，其中的内容
EXTENDS = {'_book', 'gitbook_gen_summary.py'}  # 不属于电子书的文件(夹)或者不想显示在电子书中的文件(夹)


def get_path() -> str:
    return sys.argv[1] if len(sys.argv) > 1 else input('请输入书籍所在目录：')


def gen_tree(path) -> list:
    """
    生成书籍目录中的 显示值 和 md文件位置 相对应的列表
    :return: [(name, link), ...]
        name中可能有路径分隔符
        list比dict好，因为可以放心处理md文件和文件夹同名的情况
    """
    # listdir
    dirs = [d for d in os.listdir(path) if d not in EXTENDS and not d.startswith('.')]  # 以 . 开头的就忽略掉

    # 检查是否有readme文件
    if README in dirs:
        dirs.remove(README)
    else:
        with open(os.path.join(path, README), 'w') as f:
            f.write(README_CONT)

    # 结果
    tree = []
    while dirs:
        d = dirs.pop(0)

        # 如果是一个md文件
        if d.endswith('.md'):
            tree.append((d[:-3], d))
            continue

        # 如果是一个文件夹
        low_dirs = os.listdir(os.path.join(path, d))
        # 检查是否有readme文件
        if README in low_dirs:
            low_dirs.remove(README)
        else:
            with open(os.path.join(path, os.path.join(d, README)), 'w') as f:
                f.write(README_CONT)
        tree.append((d, os.path.join(d, README)))
        # 把下一层文件名(带部分路径)放到dirs中去
        dirs.extend((os.path.join(d, ld) for ld in low_dirs if ld not in EXTENDS and not ld.startswith('.')))
    return sorted(tree, key=lambda e: e[0])  # 如果使用深度优先遍历就无需排序了


def gen_summary(path, tree):
    with open(os.path.join(path, SUMMARY), 'w') as f:
        # 标题
        f.write(SUMMARY_TITLE + '\n\n')
        # readme
        f.write(SUMMARY_CONT.format(s='', name=(README_CONT + ' ')[2:README_CONT.find('\n')], link=README))
        link_temp = {link: i for i, (n, link) in enumerate(tree)}
        # 是否增加summary
        if SUMMARY in link_temp:
            f.write(SUMMARY_CONT.format(s='', name=(SUMMARY_TITLE + ' ')[2:SUMMARY_TITLE.find('\n')], link=SUMMARY) + '\n\n')
            tree = tree[:link_temp[SUMMARY]] + tree[link_temp[SUMMARY] + 1:]  # 防止原变量被更改
        # 增加主要目录内容
        for name, link in tree:
            with open(os.path.join(path, link), 'r') as fi:
                line1 = fi.readlines(1)[0]
                name1 = (line1 + ' ')[2:line1.find('\n')]
            if README in link:
                with open(os.path.join(path, link), 'r') as fi:
                    if README_CONT == fi.read():
                        name1 = name[name.rfind(os.path.sep) + 1:]
            f.write(SUMMARY_CONT.format(s=' ' * 2 * name.count(os.path.sep), name=name1, link=link))


def main():
    path = get_path()
    gen_summary(path, gen_tree(path))


if __name__ == '__main__':
    main()
