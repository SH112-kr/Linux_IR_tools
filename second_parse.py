import os
import subprocess
from tkinter.tix import Tree

#os.system("mkdir /basic_parse")

def unzip_parse():
    parse_tar_path = subprocess.check_output('find / -name "B_parse.tar"',shell = True)
    os.system("tar -xvf "+parse_tar_path)
    print("unzip_finish")

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



    def lastlog():
        user_factor = '|'.join(System_Info.passwd_result_user)
        lastlog_result = subprocess.check_output('cat /basic_parse/accounts/lastlog | grep -E '+'\''+user_factor+'\'',shell = True)
        lastlog_result = String_Cook(lastlog_result)
        print(lastlog_result)


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
        for b in Cook_netstat_box:
            print(b)


    def simple_info_data(): #System date, hostname, user_a 정보 출력
        date_info = subprocess.check_output("cat /basic_parse/osifno/date",shell = True)
        hostname_info = subprocess.check_output('cat /basic_parse/osifno/hostname',shell = True)
        uname_info = subprocess.check_output('cat /basic_parse/osifno/uname_a',shell = True)
        return date_info, hostname_info, uname_info

    def crontab():

        crontab_result = subprocess.check_output('cat /basic_parse/process/crontab',shell = True)
        crontab_result = String_Cook(crontab_result)
        print(crontab_result)
        ClontabRemark = []
        ClontabCommand = []
        for word in crontab_result:
            if word.startswith('#'):
                ClontabRemark.append(word) #ClonTab 주석 저장 
        else:
            ClontabCommand.append(word) #ClonTab 명령어 저장
        while '' in ClontabCommand:
            ClontabCommand.remove('')

System_Info.passwd()
System_Info.lastlog()
System_Info.netstat_anpt()        


class accounts():
    def group_json():
        os.system(''' cat group | awk -F: 'BEGIN { ORS = "";} { printf "{\\\"Name\\\":\\\"%s\\\", \\\"passwd\\\": \\\"%s\\\", \\\"GID\\\": \\\"%s\\\", \\\"Sub_Gruop\\\": \\\"%s\\\"}\\n", $1, $2 ,$3, $4} END {print "\\n" }' > json_grup''')

    def passwd_json():
        os.system('''cat passwd | awk -F: 'BEGIN { ORS = "";}{ printf "{\\\"Username\\\": \\\"%s\\\", \\\"UID\\\": \\\"%s\\\", \\\"GID\\\": \\\"%s\\\", \\\"name\\\": \\\"%s\\\", \\\"home_dir\\\": \\\"%s\\\", \\\"shell\\\": \\\"%s\\\"}\\n",$1, $3 ,$4, $5, $6, $7}END {print "\\n" }' > json_passwd ''')

    def shadow_json():
        os.system('''cat shadow | awk -F: 'BEGIN { ORS = "";}{ printf "{\\\"ShadowUserName\\\": \\\"%s\\\"}\\n",$1}END {print "\\n" }' > json_shadow ''')

    def w_json():
        os.system('''cat w | awk -F: 'BEGIN { ORS = "";} { printf "{\\\"User\\\":\\\"%s\\\", \\\"FROM\\\": \\\"%s\\\", \\\"LOGIN\\\": \\\"%s\\\", \\\"WHAT\\\": \\\"%s\\\"}\\n", $1, $3 ,$4, $8} END {print "\\n" }' > json_w''')

    def create_file_time():
        

class network():
    def netstat_json():
        os.system('''cat netstat_anpt | awk ' BEGIN { ORS = "";} { printf "{\\\"proto\\\": \\\"%s\\\", \\\"Local Address\\\": \\\"%s\\\", \\\"Foreign Address\\\": \\\"%s\\\", \\\"State\\\": \\\"%s\\\" }\\n", $1, $4, $5 ,$6} END {print "\\n" }' > json_netstat ''')

class process():
    def lsmod_json():
        os.system('''cat lsmod | awk ' BEGIN { ORS = "";} { printf "{\\\"Module\\\": \\\"%s\\\", \\\"Used_by\\\": \\\"%s\\\" }\\n", $1, $4  } END {print "\\n" }' > json_lsmod ''')

    def ps_aux_josn():
        os.system('''cat ps_aux | | awk ' BEGIN { ORS = "";} { printf "{\\\"user\\\": \\\"%s\\\", \\\"pid\\\": \\\"%s\\\", \\\"START\\\": \\\"%s\\\", \\\"TIME\\\": \\\"%s\\\", \\\"COMMAND\\\": \\\"%s\\\"}",$1, $2, $9, $10, $11} END { print "\\n " }'> json_ps_aux ''')



""" 
단일 정보는 합쳐서 json으로 출력
domain
date 
history - 명령어 , 문자 구분 
ARP IP MAC 정보
crontab
...
"""
    
