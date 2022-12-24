# from ast import Try
# from audioop import add
import CloudFlare
import time
cf=''
myid=''

def getAllMemList():
    global cf
    global myid
    pagelen = 20
    pageindex = 1
    memlist = []
    
    onepagemem = cf.accounts.members.get(myid,params={'page':pageindex,'per_page':pagelen})
    memlist.extend(onepagemem)
    while len(onepagemem) == pagelen:
        pageindex = pageindex + 1
        onepagemem = cf.accounts.members.get(myid,params={'page':pageindex,'per_page':pagelen})
        memlist.extend(onepagemem)
        # print(f'请求了第{pageindex}页')
    return memlist





def main():
    global cf
    global myid
    # An authenticated call using an API Token (note the missing email)
    cf = CloudFlare.CloudFlare()
    myid = cf.accounts.get()[0]['id']
    # print(cf.memberships.get())
    # print(help(cf.accounts.get))
    # myid = cf.accounts.get()[0]['id']
    # memlist = cf.accounts.members.get(myid)
    memlist = getAllMemList()
    adminroletag = memlist[0]['roles'][0]['id']
    maillist = [i['user']['email'].strip().lower() for i in memlist]
    print(maillist)
    
    
    
    f = open("mails.txt","r")   
    # f = open("YUN20CMAIL.TXT","r") 
    lines = f.readlines()      
    f.close()
    toaddmaillist = [i.strip().lower() for i in lines]
    toaddmaillist = list(set(toaddmaillist) - set(maillist))
    while len(toaddmaillist)>0:
        print(f"remains {len(toaddmaillist)} address to add!")
        try:
            print("add ",toaddmaillist[0])
            addresult = cf.accounts.members.post(myid,data={"email":toaddmaillist[0],"roles":[adminroletag]})
        except CloudFlare.exceptions.CloudFlareAPIError as e:
            print(e)
            time.sleep(3620)
        memlist = getAllMemList()
        maillist = [i['user']['email'].strip().lower() for i in memlist]
        toaddmaillist = list(set(toaddmaillist) - set(maillist))
    print("完成！")


    # mailset = set([])

    # while 1:
    #     memlist = cf.accounts.members.get(myid)
    #     maillist = [i['user']['email'].lower() for i in memlist]
    #     print(maillist)
    #     addmail = ''
    #     for line in lines:
    #         mailadd = line.strip()
    #         if mailadd.lower() in maillist:
    #             continue
    #         else:
    #             addmail = mailadd.lower()
    #             break
    #     try:
    #         print("add ",addmail)
    #         addresult = cf.accounts.members.post(myid,data={"email":addmail,"roles":[adminroletag]})
    #     except CloudFlare.exceptions.CloudFlareAPIError as e:
    #         print(e)
    #         time.sleep(3620)


    # print(cf.accounts.members.get(myid))
    # print(cf.api_list())

main()