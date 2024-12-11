此程序可以直接替代git提交，将变动直接提交到Gitbook网页上

对于Ubuntu，请先安装wine，再运行exe程序
```shell
sudo apt install wine
```

运行此程序，应将目录以以下层级放置
- CSBlogGitbook
  - _book
- CSGitbook
  - _book
- KnowGitbook
  - _book
- Gitbook
  - know
  - cs
  - csblog
- KnowGitbook
  - Gitbook
    - gitbook_cicd.py
- Python-Automation