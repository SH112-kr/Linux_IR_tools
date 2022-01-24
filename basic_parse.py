import subprocess
import os


os.system("mkdir /basic_parse") #디렉토리 생성


def accouts_parse():
    os.system("mkdir /basic_parse/accounts") #디렉토리 생성
    os.system("cat /etc/group > /basic_parse/accounts/group") #group 정보 수집
    history_path = subprocess.check_output('find / -name ".bash_history"',shell = True) #-bash_history 존재 확인
    os.system("cat var/log/syslog > /basic_parse/accounts/syslog") #syslog 수집
    print(history_path)
    history_paths = history_path.split("\n")
    for num,historys in enumerate(history_paths):
        print(type(historys))
        if historys != "":
	        os.system("cat "+historys+" >  /basic_parse/accounts/history"+str(num))
    os.system("last > /basic_parse/accounts/last")
    os.system('lastlog > /basic_parse/accounts/lastlog')
    os.system("cat /etc/passwd > /basic_parse/accounts/passwd")
    os.system("cat /etc/shadow > /basic_parse/accounts/shadow")
    os.system("w > /basic_parse/accounts/w.txt")
    print("==accounts parming==")


def network_parse():
    os.system("mkdir /basic_parse/network")
    os.system("ifconfig > /basic_parse/network/ifconfig")
    os.system("arp > /basic_parse/network/arp")
    os.system("lsof > /basic_parse/network/lsof")
    os.system("netstat -an > /basic_parse/network/netstat_an")
    print("==network parming==")

def osinfo_parse():
    os.system("mkdir /basic_parse/osinfo")
    os.system("date > /basic_parse/osinfo/date")
    os.system("df -T > /basic_parse/osinfo/df_T")
    os.system("hostname > /basic_parse/osinfo/hostname")
    os.system("ifconfig -a > /basic_parse/osinfo/ifconfig_a")
    os.system("uname -a > /basic_parse/osinfo/uname_a")
    print("==osinfo parming==")

def process_pasre():
    os.system("mkdir /basic_parse/process")
    os.system("cat /etc/crontab > /basic_parse/process/crontab")
    os.system("ipcs -u > /basic_parse/process/ipcs_u")
    os.system("lsmod > /basic_parse/process/lsmod")
    os.system("ps -eaf > /basic_parse/process/ps_eaf")
    os.system("pstree -a > /basic_parse/process/pstree_a")
    print("== process parming ==")

def weblog_parse():
    os.system("mkdir /basic_parse/weblog")
    access_path = subprocess.check_output('find / -name "access.log"',shell = True)
    access_path = access_path.split("\n")
    for i,access_paths in enumerate(access_path):
   	 os.system("cat "+access_paths+" > /basic_parse/weblog/access_log"+str(i))
    print("== weblog parming ==")


def RecoverBash():  #RECOVER 파일
    passwd = subprocess.check_output("cat /etc/passwd",shell=True)
    lines = passwd.split("\n")
    user_list = []
    for line in lines:
        if "/bin/bash" in line: #bash 계정 확인
            user_list.append(line.split(":")[0])

    
    for user in user_list:
        getBhCmd = "cat /home/{}/.bash_history".format(user)
        print(subprocess.call(getBhCmd, shell=True))

    os.system("sudo apt-get install extundelete")
    #path = "/dev/sdb1"
    paths = subprocess.check_output("df -T",shell=True)
    paths = paths.split("\n")
    SUsers = []

    for path in paths:
        if "/home/{}".format(user) in path:
            SUsers.append(path.split()[0])
    print(SUsers)
    print(type(path))
    for s in SUsers:
        ext = ("yes | sudo extundelete {} --restore-all").format(s)
        os.system(ext)
        os.system("tar -zcf REC.tar RECOVERED_FILES")


accouts_parse()
network_parse()
osinfo_parse()
process_pasre()
weblog_parse()
os.system("tar -cvf /B_parse.tar /basic_parse")
print("COMPLETE!!!!")
