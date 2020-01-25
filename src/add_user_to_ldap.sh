##########################################
# This script will add a user to the ldap

# INFO:

# The Array variables outputted from userinputgui.py
#   ${arr[0]} - First Name
#   ${arr[1]} - Last Name
#   ${arr[2]} - User Name
#   ${arr[3]} - User Password
#   ${arr[4]} - Admin Password
##########################################



# call python program to get info from user
userinput=$(python3 userinputgui.py 2>&1);

#Split the userinput into values in an array
IFS=' ' read -ra arr<<< "$userinput"

##########################################
#	SSH In to add user to babbage
##########################################

# Add the user to babbage and get back uid
sshpass -p ${arr[4]} ssh -t -o LogLevel=QUIET administrator@141.224.38.247 "echo ${arr[4]} | sudo -S adduser --gecos '' --disabled-password ${arr[2]}" > /dev/null

# get the uid of the user you just added
uid=$(sshpass -p ${arr[4]} ssh -t -o LogLevel=QUIET administrator@141.224.38.247 "id -u ${arr[2]} 2>&1");

#Update password for user (NOTE: we run a dummy command to get the admin password in, and then we can run sudo without a password needed)
sshpass -p ${arr[4]} ssh -t -o LogLevel=QUIET administrator@141.224.38.247 "echo ${arr[4]} | sudo -S echo ${arr[2]}; (echo ${arr[3]}; echo ${arr[3]};) | sudo passwd ${arr[2]}" > /dev/null 2>&1

##########################################
#	ldif file creation and addition
##########################################

# make the ldif files for the ldap server
python3 ldapFileMaker.py ${arr[0]} ${arr[1]} ${arr[2]} $uid ${arr[3]} ${arr[4]}

# copy the LDIF folder containing LDIF files and script to be executed on babbage over to babbage
# reroute stdout to null because of sudo pw prompt
sshpass -p ${arr[4]} scp -r $PWD/LDIFFiles administrator@141.224.38.247:/home/administrator > /dev/null

# run the addToLDAP.sh script on babbage that was transfered in the LDIF folder
sshpass -p ${arr[4]} ssh -t -o LogLevel=QUIET administrator@141.224.38.247 "echo ${arr[4]} | sudo -S sh /home/administrator/LDIFFiles/addToLDAP.sh"