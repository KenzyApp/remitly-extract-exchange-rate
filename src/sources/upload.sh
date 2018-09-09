#!/bin/bash


echo ""
echo "=================================================================="
echo "UPLOADING THE FILES TO SERVER."
echo "=================================================================="
echo ""





echo -e "\n"
echo "Local: Delete temporaly files."
echo "------------------------------------------------------------------"
echo ""

find /Users/mcs/Documents/Ubuntu-Server/remitly/ -iname *.pyc -type f -delete
find /Users/mcs/Documents/Ubuntu-Server/remitly/ -iname *.pyo -type f -delete
find /Users/mcs/Documents/Ubuntu-Server/remitly/ -iname *.pyd -type f -delete
find /Users/mcs/Documents/Ubuntu-Server/remitly/ -iname .DS_Store -type f -delete
#~ rm -fR /Users/mcs/Documents/Ubuntu-Server/remitly/resources/





echo -e "\n"
echo "Server: Delete all files."
echo "------------------------------------------------------------------"
echo ""

ssh \
   -i ~/.ssh/mcs_mac_pro \
   rovisof1@rovisoft.net rm -fR /home4/rovisof1/public_html/project/remitly/*





#~ echo -e "\n"
#~ echo "Server-Local: Download files."
#~ echo "------------------------------------------------------------------"

#~ echo ""

#~ scp \
   #~ -r \
   #~ -i ~/.ssh/mcs_mac_pro \
   #~ rovisof1@rovisoft.net:/home4/rovisof1/public_html/project/remitly/hi.html \
   #~ /Users/mcs/Documents/Ubuntu-Server/remitly/





echo -e "\n"
echo "Local-Server: Upload files."
echo "------------------------------------------------------------------"
echo ""

scp \
   -r \
   -i ~/.ssh/mcs_mac_pro \
   /Users/mcs/Documents/Ubuntu-Server/remitly/* \
   rovisof1@rovisoft.net:/home4/rovisof1/public_html/project/remitly/





echo -e "\n"
echo "Server: Print the main and mysql directory."
echo "------------------------------------------------------------------"
echo ""

ssh rovisof1@rovisoft.net \
   ls -lh \
      /home4/rovisof1/public_html/project/remitly/. \
      /home4/rovisof1/public_html/project/remitly/pakages/dbs/mysql/





echo -e "\n"
echo "------------------------------------------------------------------"
echo "FINISHED: THE FILES WERE UPLOADED TO SERVER."
echo "------------------------------------------------------------------"
echo -e "\n\n\n"








