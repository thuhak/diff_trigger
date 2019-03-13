## 变更触发器

### 应用场景

周期性的执行某个任务， 将任务的结果存储于磁盘中。 当每次检测到结果和上次不同时， 更新外部存储的结果并触发回调任务

### 安装

```cmd
pip install diff_trigger
```


### 使用

#### 举个栗子

```python
from diff_trigger import watchdiff
import requests
import logging

def trigger(old, new):
    logging.info('data change from {} to {}'.format(old, new))

@watchdiff(dbpath='/var/cache/pythonjob', callback=trigger, key='somekey')
def job(url):
    r = requests.get(url)
    return r.content

class SomeClass:
    @watchdiff(dbpath='/var/cache/pythonjob', callback=trigger)
    def job(self, url):
        r = requests.get(url)
        return r.content
```

#### 说明

- 定义一个有两个参数的回调函数，第一个参数会被传递为旧的结果，第二个参数会被传递为新的结果。根据实际情况使用这个数据
- 使用watchdiff作为装饰器，填入本地的数据地址，以及所要指定的触发函数名。可以手工指定一个键，函数结果会存放在这个键下面。如果不指定键名，会根据函数的调用参数来生成一个键
- 在类中使用时，整个函数的签名计算会有整个实例的序列化信息， 因此尽量不要在体积较大的类中使用。或者使用staticmethod
- 如果在类中作为装饰器使用，需要注意的是实例的改变会更改本地数据库中的键值，导致无法触发回调函数。只有在实例不变的情况下才会有效。或者使用staticmethod
