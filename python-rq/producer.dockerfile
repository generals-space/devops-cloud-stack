## docker build -f producer.dockerfile -t generals/rq-producer:1.0.1 .
FROM generals/python3

WORKDIR /project
COPY ./project .

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

## 在CMD中使用环境变量时不能用数组形式
CMD tail -f /etc/profile