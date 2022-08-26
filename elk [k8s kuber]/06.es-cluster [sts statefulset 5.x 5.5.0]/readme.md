1. 预先确定 sts replicas 数量;
2. 规定 headless service 名称与 sts 名称相同, 以便于确定各节点的 node.name 与 discovery 地址.
3. 修改 es sts 的 replicas 数量同时修改 elasticsearch.yml 配置文件.
