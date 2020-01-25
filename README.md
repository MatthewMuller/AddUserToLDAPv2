
# Add User to LDAP  
  
This repository is a project that contains a program used to add users to the LDAP on the babbage server at Augsburg University.  
  
## Contents  
  
* Background  
  * Add New User to the Ubuntu Operating System  
  * Add the user to the LDAP  
  * Add a new group to the LDAP that matches the new user  
  * Add the user to the new group  
      
  
  
# Background 

### What has to be done to add a user to the LDAP?  
  
**Note:** This is a background of what the program is doing. It is written in a way to appear these are the steps we will be taking to add a user so you can know the process. The program this repository contains DOES NOT follow these directions! The background information is for your knowledge and to help you understand what is happening behind the scenes when you run this program.   
  
**Also:** Prompts to enter the LDAP administrative password have been omitted in this guide. There will be times when this is needed, so be prepared to be able to answer this question.  
  
To add a user to the LDAP, a few things must be done:  
* Add new user to the ubuntu operating system  
* Add the user to the LDAP  
* Add a new group to the LDAP that matches the new user  
* Add the user to the new group  
  
####Add New User to the Ubuntu Operating System  
First, we have to create a user on the server where the LDAP is being hosted. This is not adding a user to the LDAP, but a user of the same name to the ubuntu operating system on the server that is hosting the LDAP. We are adding this user because this LDAP is run in conjunction with a NFS mount.   
  
Why do we need this user on the OS in addition to the LDAP?  
* We are going to use LDAP to not only authenticate login, but to grant access to a specific NFS mount. Having a specific user on the server hosting the LDAP (Babbage) enables us to restrict access inside the folders that are to be mounted. For example, one user will have access to their specific NFS folder, but not others.   
  
#### Add the User to the LDAP  
  
Next, we will add the user to the LDAP. The process of adding users to the LDAP explained in this README was heavily influenced by the guide written by Karthikeyan Sadhasivam [[1]]. The explanation in this background section is an adaptation of that guide. (See footnotes for more information).  
  
To add a user to the LDAP, we need to create a LDIF file that will hold all the information the LDAP server needs to add a user. An example of what this file looks like is contained below.   
  
```  
dn: uid=doej,ou=users,dc=babbage,dc=augsburg,dc=edu  
objectClass: posixAccount  
objectClass: inetOrgPerson  
objectClass: organizationalPerson  
objectClass: Person  
loginShell: /bin/bash  
uid: doej  
cn: doej  
gecos: John Doe  
uidNumber: 1000  
gidNumber: 1000  
sn: Doe  
givenName: John  
homeDirectory: /nfs/home/doej  
```  
  
**Notice:**  
* uid and cn match  
* uidNumber and gidNumber match - This is important for the NFS file access and for the LDAP grouping  
* homeDirectory is /nfs/home/[uid]. This is the folder that the NFS will mount. This folder and its privileges are set by Ubuntu when you created the username in Ubuntu.  
  
Once this file has been created, we will actually add this user to the LDAP. We will use the command below and feed it the file we created (Pretend the file we created above is named ldapUserToAdd.ldif).  
  
``` bash
ldapadd -x -W -D "cn=doej,dc=babbage,dc=augsburg,dc=edu" -f ldapUserToAdd.ldif  
```  
  
You have now successfully added a user to the LDAP!  
  
#### Add a New Group to the LDAP That Matches the New User (FIX COMMAND INFO! NEEDS TO BE ADMINISTRATOR, NOT doej!)  
  
Now we will have to add a group to the LDAP that matches the user. This is because Ubuntu files have access based upon user and groups. We want the files being mounted by the NFS to have the same user and group and having the LDAP user and group match make this simple. **Summary:** We are assigning each user to their own group in the LDAP and files mounted by NFS will all have matching User and Group attributes.   
  
To add a new group, we must create a LDIF file that will hold all the information the LDAP requires to to add a group.  
  
``` 
dn: cn=doej,ou=groups,dc=babbage,dc=augsburg,dc=edu  
objectClass: top  
objectClass: posixGroup  
gidNumber: 1000  
```  
  
**Notice:**  
* "ou=groups" is correct. This is because the group we are creating is a group inside of a group. Change "cn=doej" to "cn=[username]" to change the name of the group you are adding.  
* gidNumber in this example is 1000, but this number needs to match the gidNumber of the user you are creating the group for. Otherwise, they will not be able to be added to this group.   
  
Once this file has been created, we will run the command below to actually add the group the LDAP server (Pretend the file we created above is named ldapGroupToAdd.ldif).  
  
``` bash
ldapadd -x -W -D "cn=doej,dc=babbage,dc=augsburg,dc=edu" -f ldapGroupToadd.ldif  
```  
You have now successfully added a group to the LDAP!  
  
####  Add the User to the New Group (FIX COMMAND INFO! NEEDS TO BE ADMINISTRATOR, NOT doej!)  
  
Now we will add the user we created to the group we created. Again we will make an LDIF file that will let the LDAP know we are modifying the group to add a user to it. Below is an example of what the LDIF file will look like.  
  
``` 
dn: cn=doej,ou=groups,dc=babbage,dc=augsburg,dc=edu  
changetype: modify  
add: memberuid  
memberuid: doej  
```  
  
**Notice:** * We say "add: memberuid" and then define the memberuid in the line below. Don't change the line "add: memberuid".  
* "cn=[groupname] in the first line should match the group you are trying to add the user to.  
* Do not change "ou=groups". This is identifying the fact the group we are adding a memeber to is inside of the group "groups".  
* The memberuid should be the same as the group and the user you added in the previous steps.  
  
Once this file has been created, we will run the command below to actually add the user the group (Pretend the file we created above is named addUserToGroup.ldif).  
  
``` bash
ldapmodify -x -W -D "cn=doej,dc=babbage,dc=augsburg,dc=edu" -f addUserToGroup.ldif  
```  
  
## ldapFilemaker  
  
This program is used to generate 3 files the LDAP will need in order to add a user to the LDAP.   
  
  
  
## Footnotes  
  
[1]: https://www.thegeekstuff.com/2015/02/openldap-add-users-groups.  
  
Sadhasivam, Karthikeyan. “How to Add LDAP Users and Groups in OpenLDAP on Linux.” The Geek Stuff, 24 Feb. 2015, www.thegeekstuff.com/2015/02/openldap-add-users-groups.
