**[准备]**

下载releases中的prebook.exe

将本机prebook.exe的位置写入系统环境变量中



**[开始]**

在笔记仓库根路径运行命令

对全仓库扫描

```bash
prebook all
```

对未commit的文件夹进行扫描

```
prebook diff
```

使用所有功能的命令

```
prebook all -o -d -n -c
prebook diff -o -d -n -c
```



**[功能]**

| 默认功能                                   |
| ------------------------------------------ |
| 生成每个文件夹下的README.md, 用于          |
| 将txt文件转换为md文件                      |
| 将md之外的文件，如pdf等，引入到REFERS.md中 |
| 生成SUMMARY.md                             |

| 可选功能                                                  | 启动命令 |
| --------------------------------------------------------- | -------- |
| 将md文件引用的图片放置到同级目录的{md文件名称_imgs}目录下 | -o       |
| 下载md引用中的图片                                        | -d       |
| 重命名md引用中的图片                                      | -n       |
| 压缩md引用中的图片                                        | -c       |
| 输出log到文件                                             | -l       |



---



**[Preparation]**

Download `prebook.exe` from the releases section.

Add the location of `prebook.exe` on your machine to the system environment variables.

------

**[Getting Started]**

Run the command in the root directory of your notes repository:

To scan the entire repository:

```bash
prebook all
```

To scan only uncommitted folders:

```bash
prebook diff
```

To use all available features:

```bash
prebook all -o -d -n -c
prebook diff -o -d -n -c
```



**[Features]**

| Default Features                                   |
| -------------------------------------------------- |
| Generate `README.md` for each folder.              |
| Convert `.txt` files to `.md` files.               |
| Add non-`.md` files (e.g., `.pdf`) to `REFERS.md`. |
| Generate `SUMMARY.md`.                             |

| Optional Features                                            | Command |
| ------------------------------------------------------------ | ------- |
| Move images referenced in `.md` files to `{md_filename}_imgs` directories at the same level. | `-o`    |
| Download images referenced in `.md` files.                   | `-d`    |
| Rename images referenced in `.md` files.                     | `-n`    |
| Compress images referenced in `.md` files.                   | `-c`    |
| Output logs to a file.                                       | `-l`    |

