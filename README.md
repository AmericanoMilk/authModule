## 前置说明

1. Token无特殊说明则都为 Bearer Token 形式

```json
headers = {
  'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6InhGM2VFYUdVb2UyaFBtNERzbmp4WGIiLCJpbnN0YW5jZVR5cGUiOiJ0ZW5hbnQiLCJ2ZXJzaW9uIjoia0RHTUVvNERmVll3cW1jVDMyZEFwbSIsInRpbWUiOiIyMDIyLTEwLTIxVDIzOjE2OjEwLjAxNTg4N1oiLCJleHAiOjE2NjY1NjY5NzB9.9GyRxqEq5NF4b7iUE8nbaHFhsTQrG343CEKtmT3jSUs',
  'Cookie': 'csrftoken=ctKVjswnggXjYrrkdc8tE4rKEtTUxJuolJeUepS7ROrlP1UpNSM5yO6Aw7ZgGKrZ; sessionid=gx7anmdtyxv4aukw553ior5tiqn0t9an'
}

```



## 租户管理



### 新增租户

| 请求方法 | POST                |
| -------- | ------------------- |
| 请求URL  | /v1/tenant/register |
| 参数类型 | Body                |

##### Request

| 参数     | 类型          | 是否必须 | 备注             |
| -------- | ------------- | -------- | ---------------- |
| tenant   | string        | 是       | 租户账号[unique] |
| password | Any From Json | 是       | 弱密码拦截       |
| name     | Any From Json | 否       | 租户名称         |

```json
{
    "tenant":"testTenant",
    "password": "1234567123ff."
    "name" : "测试123test"
}
```



##### Response / Json

```json
{
    "code": 200,
    "msg": "create testTenant  success",
    "data": {}
}
```



### 租户登陆

| 请求方法 | POST             |
| -------- | ---------------- |
| 请求URL  | /v1/tenant/login |
| 参数类型 | Body             |



##### Request

| 参数     | 类型          | 是否必须 | 备注 |
| -------- | ------------- | -------- | ---- |
| tenant   | string        | 是       |      |
| password | Any From Json | 是       |      |

```json
{
    "tenant": "testTenant",
    "password":"1234567123ff.",
}
```

##### Response / Json

| 参数         | 类型    | 是否必须 | 备注         |
| ------------ | ------- | -------- | ------------ |
| access_token | Strings | 是       | Token        |
| tenantId     | Strings | 是       | 租户ID       |
| name         | Strings | 是       | 租户名称     |
| isAdmin      | Boolen  | 是       | 是否管理员   |
| isActive     | Boolen  | 是       | 是否活跃账户 |
| lastLogin    | Inter   | 是       | 最后登陆时间 |



```json
{
    "code": 200,
    "msg": "",
    "data": {
        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6InhGM2VFYUdVb2UyaFBtNERzbmp4WGIiLCJ2ZXJzaW9uIjoia0RHTUVvNERmVll3cW1jVDMyZEFwbSIsInRpbWUiOiIyMDIyLTEwLTE4VDA5OjI5OjA4LjA0MDc4NloiLCJleHAiOjE2NjYyNTgxNDh9.FqxonC1COMdERCvO0dInn9947jan6-yOFYXvdaoN-I8",
        "tenantId": "xF3eEaGUoe2hPm4DsnjxXb",
        "name": null,
        "isAdmin": false,
        "isActive": true,
        "lastLogin": 1666085463
    }
}
```

### 租户信息

| 请求方法 | GET             |
| -------- | ---------------- |
| 请求URL  | /v1/tenant/tenants |
| 参数类型 | Params             |


##### Request

| 参数     | 类型          | 是否必须 | 备注 |
| -------- | ------------- | -------- | ---- |
| tenant   | string        | 否       |      |
| password | Any From Json | 否       |      |
| page | Int | 否       | 默认：1 |
| size | Int | 否       | 默认：20 |

##### Response / Json

```json
{
    "code": 200,
    "msg": "",
    "data": {
        "page": 1,
        "size": 1,
        "totalPage": 1,
        "result": [
            {
                "id": 1,
                "creationTime": 1666397319,
                "updatedTime": 1666397319,
                "uuid": "xF3eEaGUoe2hPm4DsnjxXb",
                "tenant": "absdcscsjk2ss",
                "name": null,
                "status": "NORMAL",
                "is_superuser": false,
                "last_login": 1666397319,
                "token_version": "kDGMEo4DfVYwqmcT32dApm",
                "is_active": true
            }
        ]
    }
}
```








### 获取Token

| 请求方法 | POST       |
| -------- | ---------- |
| 请求URL  | /api/token |
| 参数类型 | Body       |



##### Request

| 参数     | 类型   | 是否必须 | 备注     |
| -------- | ------ | -------- | -------- |
| tenant   | String | 是       | 租户账号 |
| user     | String | 是       | 用户账号 |
| password | String | 是       | 用户密码 |

```json
{
    "tenant" : "absdcscsjk2ss",
    "user" : "abc",
    "password": "12312312."
}
```



##### Response / Json

| 参数          | 类型          | 是否必须 | 备注                |
| ------------- | ------------- | -------- | ------------------- |
| access_token  | String        | 是       | Token               |
| refresh_token | String        | 是       | 刷新Token的Token    |
| user          | Any From Json | 是       | 用户账号            |
| tenant        | Any From Json | 是       | 租户账号            |
| currentTime   | Inter         | 是       | Token生成时间时间戳 |
| expireTime    | Inter         | 是       | Token过期时间       |
| tokenType     | String        | 是       | 默认 refresh        |



```json
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjY2MjU2OTIyLCJpYXQiOjE2NjYwODQxMjIsImp0aSI6ImRmMWViNmNjNTg5NTRmMmQ5OTJiYTU4OTFkNGFiMjAyIiwidXNlcl9pZCI6MSwidmVyc2lvbiI6IjEifQ.NBM904htlOw5d2Fv8mxDAs-EEXaZUCfIjxb9r6QIU94",
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY2NjM0MzMyMiwiaWF0IjoxNjY2MDg0MTIyLCJqdGkiOiI5OGI5YjcyYWQ0MDU0NjNlYjEwNmE2MmIzMWJkZTc5ZSIsInVzZXJfaWQiOjEsInZlcnNpb24iOiIxIn0.wGt-UfddHoE2qvUO95GHsICc2x1osZVvWLVi_V74KLI",
    "user": "abc",
    "currentTime": 1666397319,
    "expireTime": 1666397319,
    "tokenType": "refresh"
}
```





### 刷新Token

| 请求方法 | POST               |
| -------- | ------------------ |
| 请求URL  | /api/token/refresh |
| 参数类型 | Body               |



##### Request

| 参数          | 类型   | 是否必须 | 备注 |
| ------------- | ------ | -------- | ---- |
| refresh_token | String | 是       |      |

```json

{
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY2NjU0MzAwNywiaWF0IjoxNjY2MjgzODA3LCJqdGkiOiJkYWY5MjYwZjk1OWQ0ZGUxOWEzMDkwMTkzZmVlYTZjMCIsInVzZXJfaWQiOjEsInZlcnNpb24iOiIxIn0.kcwjsfONiHdfzlD7N2cMggdacwd6FebqAkAS27lbbdQ"
}
```



##### Repsonse / Json

```json
{
    "code": 200,
    "msg": "",
    "data": {
        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjY2NTY2Mzg5LCJpYXQiOjE2NjYyODM4MDcsImp0aSI6IjIxYjUxY2YzNTM5YjQwYTBhZmJlNjMzYWVkZWFmMmZlIiwidXNlcl9pZCI6MSwidmVyc2lvbiI6IjEifQ.lCvvm7Jm4hGqdl9J4ypOoEEySu6TcrbiIEuTFt2Ap8Q",
        "tokenType": "refresh",
        "currentTime": 1666397319,
        "expire_time": 1666397319
    }
}
```



### Token校验

| 请求方法 | POST               |
| -------- | ------------------ |
| 请求URL  | /api/token/refresh |
| 参数类型 | Body               |



##### Request

| 参数  | 类型   | 是否必须 | 备注 |
| ----- | ------ | -------- | ---- |
| token | String | 是       |      |

```json
{
    "token" : "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjY2NDU5MzkzLCJpYXQiOjE2NjYyODY1OTMsImp0aSI6IjBjNGQ5YTgwZTYxOTQyMGY4ZmFmY2VmNTFiNGQ0YWUxIiwidXNlcl9pZCI6MSwidmVyc2lvbiI6IjEifQ.umDS0XLjk9uw7ibIpj4jEQLf5-NuohymLOu0GW-SvwA"
}
```



##### Repsonse / Json

正确

```json
{
    "code": 200,
    "msg": "",
    "data": {}
}
```

无效Token

```json
{
    "code": 400,
    "msg": "{'non_field_errors': [ErrorDetail(string='Token is invalid or expired', code='token_not_valid')]}",
    "data": {}
}
```

