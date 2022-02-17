import subprocess
import os


os.system("mkdir /basic_parse") #디렉토리 생성


def accouts_parse():
    os.system("mkdir /basic_parse/accounts") #디렉토리 생성
    os.system("cat /etc/group > /basic_parse/accounts/group") #group 정보 수집
    history_path = subprocess.check_output('find / -name ".bash_history"',shell = True) #-bash_history 존재 확인
    os.system("cat /var/log/syslog > /basic_parse/accounts/syslog") #syslog 수집
    os.system("cat /var/log/auth.log > /basic_parse/accounts/auth_log")
    history_path = history_path.decode('utf-8')
    history_paths = history_path.split("\n")
    for num,historys in enumerate(history_paths):
        if historys != "":
            history_name = historys.split('/')
            history_name2 = history_name[-2]
            print(history_name2)
            os.system("cat "+historys+" >  /basic_parse/accounts/history"+"_"+history_name2)
    os.system("last > /basic_parse/accounts/last")
    os.system('lastlog > /basic_parse/accounts/lastlog')
    os.system("cat /etc/passwd > /basic_parse/accounts/passwd")
    os.system("cat /etc/shadow > /basic_parse/accounts/shadow")
    os.system("w > /basic_parse/accounts/w.txt")
    print("==accounts parming==")


def network_parse():
    os.system("mkdir /basic_parse/network")
    os.system("ifconfig > /basic_parse/network/ifconfig")
    os.system("arp -an > /basic_parse/network/arp")
    os.system("lsof > /basic_parse/network/lsof")
    os.system("hostname -I > /basic_parse/network/HostName_I")
    os.system("netstat -anpt > /basic_parse/network/netstat_an")
    print("==network parming==")

def osinfo_parse():
    os.system("mkdir /basic_parse/osinfo")
    os.system("date > /basic_parse/osinfo/date")
    os.system("df -T > /basic_parse/osinfo/df_T")
    os.system("hostname > /basic_parse/osinfo/hostname")
    os.system("ifconfig -a > /basic_parse/osinfo/ifconfig_a")
    os.system("uname -a > /basic_parse/osinfo/uname_a")
    os.system("find / -printf '%T+\\t%p\\n' | sort > /basic_parse/osinfo/create_file_time" )
    os.system("find / -user root -perm -4000 -print > /basic_parse/osinfo/Root_UID") 
    os.system("find / -user root -perm -2000 -print > /basic_parse/osinfo/Root_GID")
    print("==osinfo parming==")

def process_pasre(): #
    os.system("mkdir /basic_parse/process")
    os.system("crontab -l > /basic_parse/process/crontab")
    os.system("ipcs -u > /basic_parse/process/ipcs_u")
    os.system("lsmod > /basic_parse/process/lsmod")
    os.system("ps -eaf > /basic_parse/process/ps_eaf")
    os.system("ps -auxf > /basic_parse/process/ps_auxf")
    os.system("ps -aux > /basic_parse/process/ps_aux")
    os.system("pstree -a > /basic_parse/process/pstree_a")
    os.system("apt list --installed > /basic_parse/process/apt_list")
    print("== process parming ==")

def weblog_parse():
    os.system("mkdir /basic_parse/weblog")
    access_path = subprocess.check_output('find / -name "access.log"',shell = True)
    access_path = access_path.decode('utf-8')
    access_path = access_path.split("\n")
    os.system("cat "+access_path[0]+" > /basic_parse/weblog/access_log")
    print("== weblog parming ==")



def RecoverBash():  #RECOVER 파일
    passwd = subprocess.check_output("cat /etc/passwd",shell=True)
    passwd = passwd.decode('utf-8')
    lines = passwd.split("\n")
    user_list = []
    for line in lines:
        if "/bin/bash" in line: #bash 계정 확인
            user_list.append(line.split(":")[0])

    
    for user in user_list:
        getBhCmd = "cat /home/{}/.bash_history".format(user)
        print(subprocess.call(getBhCmd, shell=True))

    os.system("yes |sudo apt-get install extundelete")
    #path = "/dev/sdb1"
    paths = subprocess.check_output("df -T | awk '{print $1}'| awk '/dev\/sd/'",shell=True) # df-T 리스트 
    paths = paths.decode('utf-8')
    paths = paths.split("\n")
    


    for path in paths:
        ext = ("yes | sudo extundelete {} --restore-all").format(path)
        os.system(ext)
    os.system("tar -zcf /basic_parse/REC.tar RECOVERED_FILES")


def RootKit_Check():
    os.system("sudo apt-get install lynis -y")
    os.system("sudo lynis --check-all -Q > /basic_parse/RootKit")

accouts_parse()
network_parse()
osinfo_parse()
process_pasre()
weblog_parse()
RecoverBash()
RootKit_Check()
os.system("tar -cvf /basic_parse/var_log /var/log")
os.system("tar -cvf /B_parse.tar /basic_parse")
print("COMPLETE!!!!")
