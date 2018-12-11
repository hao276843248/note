import sys
import os

# Do not change.
SUMMARY = 'SUMMARY.md'  # Name of "summary".

# Customizable.
SUMMARY_FILE_NAME = 'SUMMARY'  # Name of "summary" display in gitbook.
SUMMARY_CONT = '{s}* [{name}]({link})\n'  # Content template of "summary".
README = 'README.md'  # Name of "readme".
README_CONT = '# Introduction\n'  # The content in the "readme" created via program while there isn't a "readme".
EXTENDS = {'_book', 'gitbook_gen_summary.py'}  # File that do not belong to gitbook or want to be ignored.


def get_path() -> str:
    return sys.argv[1] if len(sys.argv) > 1 else input('Please input the path of your GitBook files:')


def gen_tree(path) -> list:
    """
    Generate lists of names and links.
    :param path:
    :return: [(name, link), ...]
        Name may contain path separators.
        List is better than Dict because there may be cases where .md files have the same name as folders.
    """
    # listdir
    dirs = [d for d in os.listdir(path) if d not in EXTENDS and not d.startswith('.')]

    # Check "readme" file.
    if README in dirs:
        dirs.remove(README)
    else:
        with open(os.path.join(path, README), 'w') as f:
            f.write(README_CONT)

    # :return: [(name, link), ...]
    tree = []
    while dirs:
        d = dirs.pop(0)

        # <d> is a *.md file.
        if d.endswith('.md'):
            tree.append((d[:-3], d))
            continue

        # <d> is a folder.
        low_dirs = os.listdir(os.path.join(path, d))
        # Check "readme" file.
        if README in low_dirs:
            low_dirs.remove(README)
        else:
            with open(os.path.join(path, os.path.join(d, README))) as f:
                f.write(README_CONT)
        tree.append((d, os.path.join(d, README)))
        # Add files under d to dirs.
        dirs.extend((os.path.join(d, ld) for ld in low_dirs if ld not in EXTENDS and not ld.startswith('.')))
    return sorted(tree, key=lambda e: e[0])  # If use depth-first traversal, you don't need to sort.


def gen_summary(path, tree):
    with open(os.path.join(path, SUMMARY), 'w') as f:
        f.write('# ' + SUMMARY[:-3] + '\n\n')
        f.write(SUMMARY_CONT.format(s='', name=README_CONT[2:README_CONT.find('\n')], link=README))
        link_temp = {link: i for i, (n, link) in enumerate(tree)}
        if SUMMARY in link_temp:
            f.write(SUMMARY_CONT.format(s='', name=SUMMARY_FILE_NAME, link=SUMMARY) + '\n\n')
            tree = tree[:link_temp[SUMMARY]] + tree[link_temp[SUMMARY] + 1:]  # Avoid changing the original <tree>.
        f.writelines((SUMMARY_CONT.format(s=' ' * 2 * name.count(os.path.sep), link=link,
                                          # Remove the contents before the last path separator in name.
                                          name=name[name.rindex(os.path.sep) + 1:] if os.path.sep in name else name)
                      for name, link in tree))


def main():
    path = get_path()
    gen_summary(path, gen_tree(path))


if __name__ == '__main__':
    main()
