import os
#from src import ldapFileMaker
import ldapFileMaker


def test_ldap_group_file_maker():
    """
    This function test the output of the ldapuserfilemaker() function. It has
    canned data and will populate the output file and then assert the file made
    is correct. It will give feedback and also delete the ldif file created for
    the test.
    """

    # Canned data for test
    username = "doej"
    gid = "1000"

    # Make ldif file
    ldapFileMaker.ldap_group_file_maker(username, gid)  # Make file
    print("Testing ldap_group_file_maker  ", end="")

    # Perform the test
    try:
        f = open("ldapGroupEntry.ldif")
        assert f.read() == "dn: cn=doej,ou=groups,dc=babbage,dc=augsburg,dc=edu\n" \
                           "objectClass: top\n" \
                           "objectClass: posixGroup\n" \
                           "gidNumber: 1000"
        print_green("--Test passed")
    except IOError:
        print_red("--The file ldapGroupEntry.ldif could not be found by test")
    except AssertionError:
        print_red("--ldap_group_file_maker() failed")

    # Cleanup - delete canned data ldif
    try:
        os.remove("ldapGroupEntry.ldif")
    except OSError:
        print_red("--ldapGroupEntry.ldif could not be deleted or doesn't exist")


def test_ldap_user_file_maker():
    """
    This function test the output of the ldapuserfilemaker() function. It has
    canned data and will populate the output file with it so you can see how
    the layout will look.
    """

    # Canned data for test
    first_name = "John"
    last_name = "Doe"
    user_name = "doej"
    uid = "1000"
    gid = "1000"

    # Make ldif file
    ldapFileMaker.ldap_user_file_maker(first_name, last_name, user_name, uid, gid)
    print("Testing ldap_user_file_maker  ", end="")

    try:
        f = open("ldapUserEntry.ldif")
        assert f.read() == "dn: uid=doej,ou=users,dc=babbage,dc=augsburg,dc=edu\n" \
                           "objectClass: posixAccount\n" \
                           "objectClass: inetOrgPerson\n" \
                           "objectClass: organizationalPerson\n" \
                           "objectClass: Person\n" \
                           "loginShell: /bin/bash\n" \
                           "uid: doej\n" \
                           "cn: doej\n" \
                           "gecos: John Doe\n" \
                           "uidNumber: 1000\n" \
                           "gidNumber: 1000\n" \
                           "sn: Doe\n" \
                           "givenName: John\n" \
                           "homeDirectory: /nfs/home/doej"
        print_green("--Test passed")
    except IOError:
        print_red("--The file ldapUserEntry.ldif could not be found by test")
    except AssertionError:
        print_red("--ldap_user_file_maker() failed")

    # Cleanup - delete canned data ldif
    try:
        os.remove("ldapUserEntry.ldif")
    except OSError:
        print_red("--ldapUserEntry.ldif could not be deleted or doesn't exist")


def test_add_user_to_group():
    """
    This function test the output of the addUserToGroup() function. It has
    canned data and will populate the output file with it so you can see how
    the layout will look.
    """

    # Canned data for test
    username = "doej"

    # make ldif file
    ldapFileMaker.add_user_to_group(username)
    print("Testing add_user_to_group  ", end="")

    # Perform the test
    try:
        f = open("ldapAddToGroup.ldif")
        assert f.read() == "dn: cn=doej,ou=groups,dc=babbage,dc=augsburg,dc=edu\n" \
                           "changetype: modify\n" \
                           "add: uid\n" \
                           "uid: doej"
        print_green("--Test passed")
    except IOError:
        print_red("--The file ldapAddToGroup.ldif could not be found by test")
    except AssertionError:
        print_red("--ldap_group_file_maker() failed")

    # Cleanup - delete canned data ldif
    try:
        os.remove("ldapAddToGroup.ldif")
    except OSError:
        print_red("--ldapAddToGroup.ldif could not be deleted or doesn't exist")


def print_green(input):
    """
    This function will print text with a green background and white text.
    :param input: String to be printed with green background and white text
    """
    print('\x1b[6;30;42m' + input + '\x1b[0m')


def print_red(input):
    """
    This function will print text with a red background and white text.
    :param input: String to be printed with red background and white text
    """

    print('\x1b[6;30;41m' + input + '\x1b[0m')


def main():
    """
    This function called the test in testldapfilemaker
    :return:
    """

    print("\n***BEGINNING TEST***\n")
    test_ldap_group_file_maker()  # Test the group file maker to see output
    test_ldap_user_file_maker()  # Test the user file maker to see output
    test_add_user_to_group()  # Test the add user to group file maker


if __name__ == '__main__':
    main()
