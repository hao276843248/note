# GitBook

- [x] 增加一个例子，像官方文档那样
- [ ] GitBook怎么做todolist
- [x] 是不是只需要SUMMARY.md 和 README.md 就可以serve了，那自己添加好后就不需要再init了？
- [ ] 看看哪部分是可以拿出来的，直接能运行的

[GitBook项目](https://github.com/GitbookIO/gitbook)

## 什么是GitBook

现在看到的这些笔记就是通过GitBook呈现出来的，而笔记作者所需的仅仅是编写markdown格式的笔记

[GitBook百度百科](https://baike.baidu.com/item/GitBook/17969908)

GitBook 是一个基于 Node.js 的命令行工具，可使用 Github/Git 和 Markdown 来制作精美的电子书，GitBook 并非关于 Git 的教程。
> GitBook is a command line tool (and Node.js library) for building beautiful books using GitHub/Git and Markdown (or AsciiDoc).

GitBook支持输出多种文档格式：

- 静态站点：GitBook默认输出该种格式，生成的静态站点可直接托管搭载Github Pages服务上；
- PDF：需要安装gitbook-pdf依赖；
- eBook：需要安装ebook-convert；
- 单HTML网页：支持将内容输出为单页的HTML，不过一般用在将电子书格式转换为PDF或eBook的中间过程；
- JSON：一般用于电子书的调试或元数据提取。
