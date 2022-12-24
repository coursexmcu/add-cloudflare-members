# cloudflare批量加管理账号脚本

## 简介

用cloudflare python api给cloudflare账户批量加上管理邮箱，需要有“帐户设置:编辑”以及“成员资格:编辑, 用户详细信息:编辑”权限的api token。

会自动比较已有权限的账号，将未添加进去的账号添加进去。

## 使用方法

git clone 本repo后，cd进来。

### token修改

将```.cloudflare.cfg.sample```重命名为```.cloudflare.cfg```。

在cloudflare的[token管理界面](https://dash.cloudflare.com/profile/api-tokens)中创建一个有部分权限的api token，需要有下面权限。

```
帐户设置:编辑
所有用户 - 成员资格:编辑, 用户详细信息:编辑
```

```.cloudflare.cfg```中的XXXXXXXXXXX替代为所设置得到的api token.不要加引号

### 邮箱账号列表修改

将```mails.txt.sample```重命名为```mails.txt```。

将邮箱地址添加到该文件中，一行一个邮箱地址。

不一定是已经注册为cloudflare用户的邮箱地址，如果还未注册为cloudflare用户也可以添加成功，会发出注册邀请，接收并注册后也可以有所添加的账户权限。

### 运行

```bash
python3 -m venv .venv
source .venv/bin/activate
```

```bash
pip install -r requirements.txt
```

```
python3 main.py
```

因为cloudflare速率的限制，会提示```You have exceeded your hourly invite quota. Please try again in one hour.```，脚本会自动等待一小时后继续添加。


