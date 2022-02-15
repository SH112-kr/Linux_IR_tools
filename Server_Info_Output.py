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


class System_Info():
    passwd_result_user = []
    passwd_result_UID = []
    passwd_result_GID = []
    passwd_result_homedir = []
    def passwd():
        passwd_result = subprocess.check_output('cat /basic_parse/accounts/passwd | grep /bin/bash',shell = True)
        passwd_result = String_Cook(passwd_result)
        passwd_result.remove('')
        for i in passwd_result:
            System_Info.passwd_result_user.append(i.split(":")[0])
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
        for word in crontab_result:
            if word.startswith('#'):
                ClontabRemark.append(word) #ClonTab 주석 저장 
        else:
            ClontabCommand.append(word) #ClonTab 명령어 저장
        while '' in ClontabCommand:
            ClontabCommand.remove('')
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
    passwd_result_user, passwd_result_UID, passwd_result_GID, passwd_result_homedir = System_Info.passwd()

    return {"IP":HostName_I,
    "DATE":date_info,
    "HostName":hostname_info,
    "uname_ifno" : uname_info,
    "ClontabCommand":ClontabCommand,
    "netstat_anpt" : netstat_anpt,
    "lastlog_result" : lastlog_result,
    "user" : [
        {'name' : passwd_result_user,
        'UID' :passwd_result_UID, 
        'GID' : passwd_result_GID, 
        'home_dir':passwd_result_homedir}]
    #"user_UID" : passwd_result_UID,
    #"user_GId" : passwd_result_GID,
    #"user_homedir" : passwd_result_homedir
    }

print(JsonSeverData())
