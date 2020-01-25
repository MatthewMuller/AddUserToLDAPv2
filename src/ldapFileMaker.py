import sys
import os


##############################################################################
# This function is used to take in information about someone to add to the
# LDAP and then create the text file LDAP needs when adding a user.
##############################################################################
def ldap_user_file_maker(first_name, last_name, username, uid, gid):

    try:
        f = open("ldapUserEntry.ldif", "x")      # creates the file if needed
    except IOError:
        f = open("ldapUserEntry.ldif", "w")      # opens the file if it exist

    f.write("dn: uid=" + username + ",ou=users,dc=babbage,dc=augsburg,dc=edu" + "\n")
    f.write("objectClass: posixAccount" + "\n")
    f.write("objectClass: inetOrgPerson" + "\n")
    f.write("objectClass: organizationalPerson" + "\n")
    f.write("objectClass: Person" + "\n")
    f.write("loginShell: /bin/bash" + "\n")
    f.write("uid: " + username + "\n")
    f.write("cn: " + username + "\n")
    f.write("gecos: " + first_name + " " + last_name + "\n")
    f.write("uidNumber: " + uid + "\n")
    f.write("gidNumber: " + gid + "\n")
    f.write("sn: " + last_name + "\n")
    f.write("givenName: " + first_name + "\n")
    f.write("homeDirectory: /nfs/home/" + username)


##############################################################################
# This function is used to take in information about a group to add to the
# LDAP and then create the text file LDAP needs when adding a group.
##############################################################################
def ldap_group_file_maker(username, gid):

    try:
        f = open("ldapGroupEntry.ldif", "x")     # creates the file if needed
    except IOError:
        f = open("ldapGroupEntry.ldif", "w")     # opens the file if it exist

    f.write("dn: cn=" + username + ",ou=groups,dc=babbage,dc=augsburg,dc=edu\n")
    f.write("objectClass: top\n")
    f.write("objectClass: posixGroup\n")
    f.write("gidNumber: " + gid)


##############################################################################
# This function is used to take in information about a group to add to the
# LDAP and then create the text file LDAP needs when adding a group.
##############################################################################
def add_user_to_group(username):

    try:
        f = open("ldapAddToGroup.ldif", "x")     # creates the file if needed
    except IOError:
        f = open("ldapAddToGroup.ldif", "w")     # opens the file if it exist

    f.write("dn: cn=" + username + ",ou=groups,dc=babbage,dc=augsburg,dc=edu\n")
    f.write("changetype: modify\n")


##############################################################################
# This function is used to make the bash script that contains the commands
# to actually add the new ldap user to the ldap database
##############################################################################
def ldap_script_for_babbage(username, pw, apw):

    try:
        f = open("addToLDAP.sh", "x")      # creates the file if needed
    except IOError:
        f = open("addToLDAP.sh", "w")      # opens the file if it exist

    f.write("\necho \"\n\n-Add User-\"\n")
    f.write("ldapadd -x -w " + apw + " -D \"cn=admin,dc=babbage,dc=augsburg,dc=edu\" -f /home/administrator/LDIFFiles/ldapUserEntry.ldif;" + "\n")
    f.write("\necho \"-Set User PW-\"\n")
    f.write("ldappasswd -s " + pw + " -w " + apw + " -D \"cn=admin,dc=babbage,dc=augsburg,dc=edu\" -x \"uid=" + username + ",ou=users,dc=babbage,dc=augsburg,dc=edu\";" + "\n")
    f.write("\necho \"-Add Group-\"\n")
    f.write("ldapadd -x -w " + apw + " -D \"cn=admin,dc=babbage,dc=augsburg,dc=edu\" -f /home/administrator/LDIFFiles/ldapGroupEntry.ldif;" + "\n")
    f.write("\necho \"-Add User to Group-\"\n")
    f.write("ldapmodify -x -w " + apw + " -D \"cn=admin,dc=babbage,dc=augsburg,dc=edu\" -f /home/administrator/LDIFFiles/ldapAddToGroup.ldif;" + "\n")
    f.write("\necho \"-Removing LDIF Files-\"\n")
    f.write("echo $apw | sudo -S rm -fr /home/administrator/LDIFFiles" + "\n")



##############################################################################
# This function creates output based upon the parameters handed into the
# python script. This function is to be called when the parameters are not
# good.
##############################################################################
def bad_parameters():

    # The lines below build a string called args of all
    # the command line arguments
    args = ""
    for i in range(1, len(sys.argv)):
        if i + 1 == len(sys.argv):  # if its the last arg
            args += sys.argv[i]  # append only arg
        else:
            args += sys.argv[i] + ", "  # append arg and comma

    num_args = len(sys.argv) - 1

    print("-----------")
    print("INPUT ERROR in ldapFileMaker.py")
    print("Received " + str(num_args) + " argument/s")
    print("Arguments - " + args)
    print("Require 7 arguments to make files for adding user/group to LDAP")


##############################################################################
#
##############################################################################
def main():

    #################################################
    #                     DEBUG                     #
    # Uncomment the functions below to have         #
    # files made of the canned data in the methods  #
    # being called.                                 #
    #################################################

    # test_ldap_user_file_maker()     # Test the user file maker to see output
    # test_ldap_group_file_maker()    # Test the group file maker to see output
    # test_add_user_to_group()        # Test the add user to group file maker

    # if the number of params are correct, make the ldif files
    if len(sys.argv) == 7:

        ############################
        # System args - what it is #
        # sys.argv[1] - first name #
        # sys.argv[2] - last name  #
        # sys.argv[3] - userName   #
        # sys.argv[4] - uid/gid    #
        # sys.argv[5] - user pw    #
        # sys.argv[6] - admin pw   #
        ############################

        # For debug only. Will show admin and user pw in console
        # print("args : " + str(sys.argv))

        ldap_user_file_maker(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[4])
        ldap_group_file_maker(sys.argv[3], sys.argv[4])
        add_user_to_group(sys.argv[3])
        ldap_script_for_babbage(sys.argv[3], sys.argv[5], sys.argv[6])

        os.rename("ldapAddToGroup.ldif", "LDIFFiles/ldapAddToGroup.ldif")
        os.rename("ldapGroupEntry.ldif", "LDIFFiles/ldapGroupEntry.ldif")
        os.rename("ldapUserEntry.ldif", "LDIFFiles/ldapUserEntry.ldif")
        os.rename("addToLDAP.sh", "LDIFFiles/addToLDAP.sh")
        print("-ldif files have been created-")
    else:
        bad_parameters()


if __name__ == '__main__':
    main()
