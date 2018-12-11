"""
    通过已有文件自动生成 SUMMARY.md 文件内容。

    使用：启动时传入gitbook所在路径即可。
"""
import sys
import os

SUMMARY = 'SUMMARY.md'  # SUMMARY.md 的文件名

# 以下变量可以根据需要自定义
SUMMARY_FILE_NAME = 'SUMMARY'  # SUMMARY.md 在电子书目录中的显示名
SUMMARY_CONT = '{s}* [{name}]({link})\n'  # SUMMARY.md 中的内容格式，可以自定义 * 为 - ，其他不能动
README = 'README.md'  # readme文件的名字，程序会检索各级文件夹，如果其中没有这个名字的readme文件，会自动生成一个
README_CONT = '# Introduction'  # 程序自动生成readme文件时，其中的内容
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
            with open(os.path.join(path, os.path.join(d, README))) as f:
                f.write(README_CONT)
        tree.append((d, os.path.join(d, README)))
        # 把下一层文件名(带部分路径)放到dirs中去
        dirs.extend((os.path.join(d, ld) for ld in low_dirs if ld not in EXTENDS and not ld.startswith('.')))
    return sorted(tree, key=lambda e: e[0])  # 如果使用深度优先遍历就无需排序了


def gen_summary(path, tree):
    with open(os.path.join(path, SUMMARY), 'w') as f:
        f.write('# ' + SUMMARY[:-3] + '\n\n')
        f.write(SUMMARY_CONT.format(s='', name=README_CONT[2:README_CONT.find('\n')], link=README))
        link_temp = {link: i for i, (n, link) in enumerate(tree)}
        if SUMMARY in link_temp:
            f.write(SUMMARY_CONT.format(s='', name=SUMMARY_FILE_NAME, link=SUMMARY) + '\n\n')
            tree = tree[:link_temp[SUMMARY]] + tree[link_temp[SUMMARY] + 1:]  # 防止原变量被更改
        f.writelines((SUMMARY_CONT.format(s=' ' * 2 * name.count(os.path.sep), link=link,
                                          # 把名字中路径分隔符之前的部分去掉
                                          name=name[name.rindex(os.path.sep) + 1:] if os.path.sep in name else name)
                      for name, link in tree))


def main():
    path = get_path()
    gen_summary(path, gen_tree(path))


if __name__ == '__main__':
    main()
