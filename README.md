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
    "currentTime": 1666084122,
    "expireTime": 1666343322,
    "tokenType": "refresh"
}
```



