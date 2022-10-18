## 租户管理



### 新增租户

> POST /v1/tenant/register

##### Request

| 参数     | 类型          | 是否必须 | 备注           |
| -------- | ------------- | -------- | -------------- |
| tenant   | string        | 是       | 租户账号       |
| password | Any From Json | 是       | 已做弱密码拦截 |
| name     | Any From Json | 否       | 租户名称       |

```json
{
    "tenant":"testTenant",
    "password": "1234567123ff."
    "name" : "测试123test"
}
```



##### Response



### 租户登陆

>/v1/tenant/login

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

##### Response