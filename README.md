# 小语机器人FAQ引擎

本项目基于百度开源FAQ引擎[Anyq](https://github.com/baidu/AnyQ)。旨在为小语智能问答机器人平台提供FAQ技术支持。

## 快速开始
由于Anyq编译复杂，本项目只支持使用容器进行部署。

构建镜像
```
docker build -t xiaoyu_faq:latest .
```

运行容器在`10000`端口
```
docker run --name xiaoyu_faq -p 10000:8080 -v xiaoyu_faq:/home/AnyQ/build/solr-4.10.3-anyq/example/solr/collection1 -d xiaoyu_faq
```
`/home/AnyQ/build/solr-4.10.3-anyq/example/solr/collection1`为solr保存`collection`的路径，需要映射出去

## API接口
API接口文档请查看[Web API文档](docs/WebAPI文档.md)
