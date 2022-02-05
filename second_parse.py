import os
import subprocess

def unzip_parse():
    parse_tar_path = subprocess.check_output('find / -name "B_parse.tar"',shell = True)
    os.system("tar -xvf "+parse_tar_path)
    print("unzip_finish")


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
    

