import redis
import json
import uuid
from datetime import datetime, date, timedelta


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (uuid.UUID,)):
            # 将 UUID 转换为字符串
            return str(obj)
        elif isinstance(obj, (datetime, date)):
            # 将 datetime 和 date 转换为 ISO 8601 格式的字符串
            return obj.isoformat()
        elif isinstance(obj, timedelta):
            # 将 timedelta 转换为总秒数
            return obj.total_seconds()
        # 调用父类的 default 方法处理其他类型
        return json.JSONEncoder.default(self, obj)


# 不适用于模糊搜索
class RedisPool(CustomJSONEncoder):
    def __init__(self, *args, **kwargs):
        host = kwargs.get('host')
        port = kwargs.get('port')  # 注意：端口应该是一个整数
        password = kwargs.get('password')
        pools = redis.ConnectionPool(host=host,
                                     port=port,
                                     password=password,
                                     decode_responses=True)
        self.__redis = redis.StrictRedis(connection_pool=pools)


    # 在 Redis 中设置值，默认，不存在则创建，存在则修改。
    def set(self, key, value, expire=None):
        if isinstance(value, (dict, list)):
            value = json.dumps(value, cls=CustomJSONEncoder,ensure_ascii=False)

        if expire is not None:
            return self.__redis.setex(key, expire, value)  # 使用 setex 设置过期时间
        else:
            return self.__redis.set(key, value)

    # 取出键对应的值
    def get(self, key):
        value = self.__redis.get(key)
        if value is not None:
            # 如果存储的是字典的序列化字符串，则反序列化为字典
            try:
                value = json.loads(value)
            except json.JSONDecodeError:
                # 如果不是字典的序列化字符串，则直接返回原值
                pass
        return value

    # 获取有序集合中所有元素
    def zrange(self, key):
        if self.__redis.exists(key):
            return self.__redis.zrange(key, 0, -1, desc=False, withscores=True)
        else:
            return None

    # 获取值的索引号
    def zrank(self, key):
        if self.__redis.exists(key):
            return self.__redis.zrank(key)
        else:
            return None

    # 按照分数范围获取name对应的有序集合的元素
    def zrangebyscore(self, key):
        if self.__redis.exists(key):
            return self.__redis.zrangebyscore(key, 0, -1, withscores=True)
        else:
            return None

    # 按照分数范围获取有序集合的元素并排序（默认从大到小排序）
    def zrevrange(self, key):
        if self.__redis.exists(key):
            return self.__redis.zrevrange(key, 0, -1)
        else:
            return None

    # 删除键值对
    def delete(self, key):
        if self.__redis.exists(key):
            return self.__redis.delete(key)
        else:
            return None

    # def hgetall_by_pattern(self, pattern):
    #     keys = self.scan_keys(pattern)
    #     if not keys:
    #         return {}
    #
    #     # 关键修正：移除 .decode()，因为 type 返回的已是字符串
    #     hash_keys = [key for key in keys if self.__redis.type(key) == "hash"]
    #
    #     result = {key: self.hgetall(key) for key in hash_keys}
    #     return result
    def hgetall_by_pattern_str_sync(self,pattern):
        """同步版本的 hgetall_by_pattern_str 替代方法，支持多种数据类型"""
        keys = self.scan_keys(pattern)
        result = {}
        for key in keys:
            try:
                # 检查键的类型
                key_type = self._RedisPool__redis.type(key)
                if key_type == 'hash':
                    value = self.hgetall(key)
                    if value:
                        result[key] = value
                elif key_type == 'string':
                    value = self.get(key)
                    if value:
                        result[key] = value
                else:
                    print(f"警告: 键 {key} 是 {key_type} 类型，当前不支持获取此类数据")
            except Exception as e:
                print(f"错误: 获取键 {key} 的值时出错 - {str(e)}")
        return result

    def hgetall_by_pattern_str(self, pattern):
        keys = self.scan_keys(pattern)
        if not keys:
            return {}

        # 步骤1：用管道批量获取所有key的类型，减少网络往返
        pipe = self.__redis.pipeline()
        for key in keys:
            pipe.type(key)  # 批量添加TYPE命令
        type_results = pipe.execute()  # 一次性执行所有命令

        # 过滤出hash类型的key
        hash_keys = [key for key, type_ in zip(keys, type_results) if type_ == 'string']
        if not hash_keys:
            return {}

        # 步骤2：用管道批量获取所有hash数据，减少网络往返
        pipe = self.__redis.pipeline()
        for key in hash_keys:
            pipe.get(key)  # 批量添加HGETALL命令
        hash_results = pipe.execute()  # 一次性执行所有命令

        # 组装结果
        result = dict(zip(hash_keys, hash_results))
        return result

    def hgetall_by_pattern(self, pattern):
        keys = self.scan_keys(pattern)
        if not keys:
            return {}

        # 步骤1：用管道批量获取所有key的类型，减少网络往返
        pipe = self.__redis.pipeline()
        for key in keys:
            pipe.type(key)  # 批量添加TYPE命令
        type_results = pipe.execute()  # 一次性执行所有命令

        # 过滤出hash类型的key
        hash_keys = [key for key, type_ in zip(keys, type_results) if type_ == "hash"]
        if not hash_keys:
            return {}

        # 步骤2：用管道批量获取所有hash数据，减少网络往返
        pipe = self.__redis.pipeline()
        for key in hash_keys:
            pipe.hgetall(key)  # 批量添加HGETALL命令
        hash_results = pipe.execute()  # 一次性执行所有命令

        # 组装结果
        result = dict(zip(hash_keys, hash_results))
        return result

    # 获取key对应hash的所有键值
    def hgetall(self, key):
        if self.__redis.exists(key):
            return self.__redis.hgetall(key)
        else:
            return None

    # 统计返回的总个数
    def rcount(self, re, key):
        if self.__redis.exists(key):
            sum = 0
            for i in re:
                print(i)
                sum += 1
            print("总共有%s个" % (sum))

    # 管道方法
    def pipeline_set(self, data_dict):
        with self.__redis.pipeline() as pipe:
            for key, value in data_dict.items():
                if isinstance(value, (dict, list)):
                    value = json.dumps(value, cls=CustomJSONEncoder, ensure_ascii=False)
                pipe.set(key, value)
            pipe.execute()

    def scan_keys(self, pattern):
        keys = []
        cursor = 0
        while True:
            cursor, partial_keys = self.__redis.scan(cursor, match=pattern)
            keys.extend(partial_keys)
            if cursor == 0:
                break
        return keys

    def scan_keys_with_values(self, pattern):
        keys = []
        values = []
        cursor = 0

        while True:
            cursor, partial_keys = self.__redis.scan(cursor, match=pattern)
            keys.extend(partial_keys)
            if cursor == 0:
                break

        if keys:
            # 使用 MGET 一次性获取所有键的值
            values = self.__redis.mget(keys)

        return dict(zip(keys, values))  # 返回键值对字典

    # 获取所有的值
    def mget(self, key):
        keys = self.scan_keys(key)
        if keys is not None:
            # 如果存储的是字典的序列化字符串，则反序列化为字典
            try:
                value = self.__redis.mget(keys)
            except Exception:
                # 如果不是字典的序列化字符串，则直接返回原值
                pass
        return value

    def lrange(self, key, start=0, end=-1):
        """
        获取 Redis 列表中指定范围的元素，尝试将每个元素反序列化为 JSON 对象
        :param key: 列表的键
        :param start: 起始索引（默认 0，即第一个元素）
        :param end: 结束索引（默认 -1，即最后一个元素）
        :return: 反序列化后的元素列表
        """
        # 调用 Redis 原生 lrange 命令
        raw_list = self.__redis.lrange(key, start, end)
        # 对每个元素尝试 JSON 反序列化（与 get 方法逻辑保持一致）
        deserialized_list = []
        for item in raw_list:
            try:
                deserialized_list.append(json.loads(item))
            except json.JSONDecodeError:
                deserialized_list.append(item)
        return deserialized_list


# redis_pool = RedisPool()

