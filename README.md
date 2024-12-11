完成一次完整的Gitbook CICD



- 配置仓库的push--webhook---> server端入口
- server端接收到http post, 执行python utils
- python utils
  - 压缩图片
  - 为让Gitbook网页展示图片，格式化md文件中的图片引用
- gitbook build 生成网页？
- 更新网页到gitbook仓库？