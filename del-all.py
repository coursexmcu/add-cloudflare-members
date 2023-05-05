import CloudFlare
import time
import os

cf = ''
myid = ''

def getAllMemList():
    global cf
    global myid
    pagelen = 20
    pageindex = 1
    memlist = []

    onepagemem = cf.accounts.members.get(myid, params={'page': pageindex, 'per_page': pagelen})
    memlist.extend(onepagemem)
    while len(onepagemem) == pagelen:
        pageindex = pageindex + 1
        onepagemem = cf.accounts.members.get(myid, params={'page': pageindex, 'per_page': pagelen})
        memlist.extend(onepagemem)
    return memlist

def main():
    global cf
    global myid
    cf = CloudFlare.CloudFlare()
    myid = cf.accounts.get()[0]['id']
    memlist = getAllMemList()

    if os.path.isfile("mails.txt"):
        f = open("mails.txt", "r")
        lines = f.readlines()
        f.close()
        to_remove_emails = [i.strip().lower() for i in lines]
    else:
        remove_all = input("未找到 mails.txt 文件，是否要删除其他所有邮箱的授权？（y/n）：")
        if remove_all.lower() == 'y':
            to_remove_emails = [member["user"]["email"].strip().lower() for member in memlist if member["user"]["email"].strip().lower() != myid]
        else:
            print("未执行任何操作。")
            return

    for email_to_remove in to_remove_emails:
        member_to_remove = None
        for member in memlist:
            if member["user"]["email"].strip().lower() == email_to_remove:
                member_to_remove = member
                break

        if member_to_remove:
            try:
                member_id = member_to_remove['id']
                cf.accounts.members.delete(myid, member_id)
                print(f"已成功撤销 {email_to_remove} 的管理权限。")
            except CloudFlare.exceptions.CloudFlareAPIError as e:
                print(f"撤销 {email_to_remove} 的权限失败，原因：{e}")
        else:
            print(f"未找到邮箱为 {email_to_remove} 的团队成员。")

    print("完成！")

main()
