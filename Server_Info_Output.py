import os
import subprocess



#os.system("mkdir /basic_parse")
''' 압축 해제'''
def unzip_parse(): 
    parse_tar_path = subprocess.check_output('find / -name "B_parse.tar"',shell = True)
    os.system("tar -xvf "+parse_tar_path)
    print("unzip_finish")

''' byte to string'''
def String_Cook(row_string): 
    row_string = row_string.decode('utf-8')
    cook_string = row_string.split("\n")
    return cook_string

port = []
port_name = []
with open("wellknownport.txt",'r')as f:
    lines = f.readlines()
    for line in lines:
        split_line = line.split('  ')
        split_line[2] = split_line[2].replace('\n','')
        port.append(split_line[1])
        port_name.append(split_line[2])




    

class System_Info():
    passwd_result_user = []
    passwd_result_UID = []
    passwd_result_GID = []
    passwd_result_homedir = []
    def passwd():
        passwd_result = subprocess.check_output('cat /basic_parse/accounts/passwd | grep /bin/bash',shell = True)
        passwd_result = String_Cook(passwd_result)
        passwd_result.remove('')
        #print(passwd_result)
        for i in passwd_result:
            System_Info.passwd_result_user.append(i.split(":")[0]) #
            System_Info.passwd_result_UID.append(i.split(":")[2])
            System_Info.passwd_result_GID.append(i.split(":")[3])
            System_Info.passwd_result_homedir.append(i.split(":")[5])
        #print(System_Info.passwd_result_user)
        #print(System_Info.passwd_result_UID)
        #print(System_Info.passwd_result_GID)
        #print(System_Info.passwd_result_homedir)
        return System_Info.passwd_result_user,System_Info.passwd_result_UID,System_Info.passwd_result_GID,System_Info.passwd_result_homedir


    def lastlog():
        user_factor = '|'.join(System_Info.passwd_result_user)
        lastlog_result = subprocess.check_output('cat /basic_parse/accounts/lastlog | grep -E '+'\''+user_factor+'\'',shell = True)
        lastlog_result = String_Cook(lastlog_result)
        #print(lastlog_result)
        
        return lastlog_result
    def history():
        history_list = subprocess.check_output("find /basic_parse/accounts/ -name 'history_*'",shell = True )
        history_list = String_Cook(history_list)
        history_list.remove('')
        history_owner = []
        history_command = []
        #print(history_lists)
        for i in history_list:
            history_owner_splitlist = i.split('/')
            history_owner.append(history_owner_splitlist[-1])
        for e,v in enumerate(history_owner):
            history_command2 = (subprocess.check_output("cat "+ history_list[e],shell=True))
            history_command.append(String_Cook(history_command2))
            

        
        return history_owner,history_command


    def live_process():
        process_list = subprocess.check_output('''cat /basic_parse/process/ps_aux | awk ' BEGIN { ORS = "";} { printf "\\\"user\\\": \\\"%s\\\", \\\"pid\\\": \\\"%s\\\", \\\"START\\\": \\\"%s\\\", \\\"TIME\\\": \\\"%s\\\", \\\"COMMAND\\\": \\\"%s\\\"\\n",$1, $2, $9, $10, $11} END { print "" }' ''',shell=True)
        process_list = String_Cook(process_list)
        process_list.remove('')
        return process_list
    def netstat_anpt():
        Cook_netstat_box = []
        netstat_anpt_result = subprocess.check_output('cat /basic_parse/network/netstat_an',shell = True)
        netstat_anpt_result = String_Cook(netstat_anpt_result)
        del netstat_anpt_result[0:2]
        del netstat_anpt_result[-1]
        for i in netstat_anpt_result:
            result = i.split(' ')
            while '' in result:
                result.remove("")
            if result[0] == 'tcp':
                Local_info = result[3].split(":")
                Fore_info = result[4].split(":")
                result[3] = Local_info
                result[4] = Fore_info
                Cook_netstat_box.append(result[0:6])
            elif result[0] == 'tcp6':
                pass
        #for b in Cook_netstat_box:
        #    print(b)
        return Cook_netstat_box

    def simple_info_data(): #System date, hostname, user_a 정보 출력
        date_info = subprocess.check_output("cat /basic_parse/osinfo/date",shell = True)
        date_info = String_Cook(date_info)
        hostname_info = subprocess.check_output('cat /basic_parse/osinfo/hostname',shell = True)
        hostname_info = String_Cook(hostname_info)
        uname_info = subprocess.check_output('cat /basic_parse/osinfo/uname_a',shell = True)
        uname_info = String_Cook(uname_info)
        HostName_info = subprocess.check_output('cat /basic_parse/network/HostName_I',shell = True)
        HostName_info = String_Cook(HostName_info)
        return date_info[0], hostname_info[0], uname_info[0] , HostName_info[0]

    def crontab(): # Return [Clon 명령어],[Clon 주석 ]

        crontab_result = subprocess.check_output('cat /basic_parse/process/crontab',shell = True)
        crontab_result = String_Cook(crontab_result)
        #print(crontab_result)
        ClontabRemark = []
        ClontabCommand = []
        #print(crontab_result)
        for word in crontab_result:
            if word.startswith('#'):
                ClontabRemark.append(word) #ClonTab 주석 저장 
            else:
                ClontabCommand.append(word) #ClonTab 명령어 저장
            while '' in ClontabCommand:
                ClontabCommand.remove('')
        #print(ClontabCommand)
        #print(ClontabRemark)
        return ClontabCommand, ClontabRemark

System_Info.passwd()
System_Info.lastlog()
System_Info.netstat_anpt()        

dic1 = {}
def JsonSeverData():
    date_info, hostname_info, uname_info, HostName_I = System_Info.simple_info_data() 
    ClontabCommand, ClontabRemark = System_Info.crontab()
    netstat_anpt = System_Info.netstat_anpt()
    lastlog_result = System_Info.lastlog()
    #passwd_result_user, passwd_result_UID, passwd_result_GID, passwd_result_homedir = System_Info.passwd()

    return {"IP":HostName_I,
    "DATE":date_info,
    "HostName":hostname_info,
    "uname_ifno" : uname_info,
    "ClontabCommand":ClontabCommand,
    "netstat_anpt" : netstat_anpt,
    "lastlog_result" : lastlog_result,
    "user" : [
        {'name' : System_Info.passwd_result_user,
        'UID' :System_Info.passwd_result_UID, 
        'GID' : System_Info.passwd_result_GID, 
        'home_dir':System_Info.passwd_result_homedir}]
    #"user_UID" : passwd_result_UID,
    #"user_GId" : passwd_result_GID,
    #"user_homedir" : passwd_result_homedir
    }


date_info, hostname_info, uname_info, HostName_I = System_Info.simple_info_data() 
User_Name = System_Info.passwd_result_user,
User_UID = System_Info.passwd_result_UID, 
User_GID = System_Info.passwd_result_GID, 
User_HomeDir = System_Info.passwd_result_homedir
ClontabCommand, ClontabRemark = System_Info.crontab()
netstat_anpt = System_Info.netstat_anpt()
lastlog_result = System_Info.lastlog()


print("시간 : " + date_info)
print("호스트 이름: " + hostname_info)
print('시스템 정보 : '+ uname_info)
print("IP 정보 : " + HostName_I)

for a,e in enumerate(User_Name):
    print("계정명 :",User_Name,'\n',"UID ,",User_UID,"\n","GID :",User_GID,"\n","홈디렉토리 :",User_HomeDir)

print("\n시스템 네트워크 정보 ")

for i in netstat_anpt:
    Local_Address = False
    Foreign_Address = False
    print("=================="+i[5]+"=========================")
    print("Local Address : " + i[3][0]+':'+i[3][1])
    for a,e in enumerate(port):
        if i[3][1] == e:  
            print("Port :" ,port_name[a] )
            Local_Address = True
        #elif i[3][1] == '*':
        #    print("Port : *" )
    if i[3][1] == '*':
        print("Port : *" )
    elif Local_Address == False :
        print("Port : UnKnown Port")
        
            

    print("Foreign Address" + i[4][0]+':'+i[4][1])
    for a,e in enumerate(port):
        if i[4][1] == e:  
            print("Port :" ,port_name[a] )
        #elif i[4][1] == '*':
        #    print("Port : *" )
    if i[4][1] == '*':
        print("Port : *" )
    elif Foreign_Address == False :
        print("Port : UnKnown Port")

print("\n================================Bash 계정 최근 기록================================")
for a in lastlog_result:
    print(a)

print("================================Crontab 상태================================")
print(ClontabCommand,"\n")

print("================================History 로그================================")
history_name , history_command =System_Info.history()
for e,j in enumerate(history_name):
    print("히스토리 계정 :"+ j)
    for i in history_command[e]:
        print(i)

print("================================Live Process List================================")
Live_Process = System_Info.live_process()
for i in Live_Process:
    print(i)

