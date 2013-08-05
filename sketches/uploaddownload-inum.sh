#!/bin/sh
# author: Matt Svensson
# Copy a file to/from a mounted devices home folder and the local home dir (~/) where the script should be
# From mounted device, to local storage
#    - You are asked to identify the mounted drive to copy from
#    - You are asked for the name if the file (should be in the home directory)
#    - The file name is modified to be a randomly generated number
#    - Following the copy to the local storage home directory, a inum is given to you for the file
# From local storage to the mounted device
#    - You are asked to identify the mounted drive to copy to
#    - You are asked to provide the inum of the file to download
#    - The file is downloaded (right now as a generic 'outputfile') to the mounted drive's home folder
getdrives=$(df | grep -Po '(?<=dev/).*')
base=/dev/


## Infinite Loop ##
while true; do
  clear

  ## Request input to start program ##
  read -p "Press 'u' to upload to DD or 'd' to download from DD : " tocontinue
  case "$tocontinue" in

    ############################################################################################
    ##                                  Executes upload                                       ##
    ############################################################################################
    u|U)
      echo
      $getdrives
      df | grep -Po '(?<=dev/).*'  #Print all mounted volumes
      echo

      #Request identification of your drive
      read -p "Which drive is yours? (e.g. sda1 or sdb1): " driveletter
        drive=$base$driveletter         #Store your drive into $drive
      #echo Your drive is: /dev/sd$driveletter
      echo

      #Gets the path to your drive and prints it
      path=$(df | grep $drive | grep -Po '(?<=% ).*')
      echo "The drive path is: $path"
      echo

         #Error handling if drive is not identified (e.g. path="")

      #Asks for the file to copy (from the home directory)
      read -p "What file do you want to copy from your drive's home directory to the Dead Drop: " filetocopy
         echo
         #Check to see if the file exists and copy it does
         if [ -e $path/$filetocopy ]
          then
             #Generate random number for file name
	     RANDOM=$$$$	#10 digit number, random
             #RANDOM=$$$(date +%s | head -c 5)   #Seed + sec since 1/1/1970
             newfilename=$RANDOM

             echo "Copying file...this may take a while so do not cancel the script."
             cp $path/$filetocopy ~/$newfilename 

             echo "Copy complete"
             echo
             echo "Your new filename: $newfilename"
             echo
             inum=$(ls -li | grep $newfilename | awk '{print substr($0,0,8);}')
             echo "The inum is: $inum"
             echo

          else
             echo Error: file \'$filetocopy\' not found
             echo
         fi
 
      read -p "Press [ENTER] to continue" enter
      continue
    ;;

    ############################################################################################
    ##                                  Executes download                                     ##
    ############################################################################################
    d|D)
      echo
      $getdrives
      df | grep -Po '(?<=dev/).*'  #Print all mounted volumes
      echo

      #Request identification of your drive
      read -p "Which drive is yours? (e.g. sda1 or sdb1): " driveletter
        drive=$base$driveletter         #Store your drive into $drive
      #echo Your drive is: /dev/sd$driveletter
      echo

      #Gets the path to your drive and prints it
      path=$(df | grep $drive | grep -Po '(?<=% ).*')
      echo "The drive path is: $path"
      echo

         #Error handling if drive is not identified (e.g. path="")

      #Asks for the inum to copy (from the home directory)
      read -p "What inum do you want to copy: " inumtocopy
         echo
         #Check to see if the file exists by checking for the inum
         ls -li | grep $inumtocopy >/dev/null 
         
         #If it exists, copy the file, if not give error
         if [ $? -eq 0 ]
          then
             copyinum=$(find ./ -inum $inumtocopy  -exec cp {} $path/outputfile \;)
             echo "Copy complete"
          else
             echo Error: inum \'$inumtocopy\' not found
             echo
         fi
 
      read -p "Press [ENTER] to continue" enter
      continue
    ;;

    ############################################################################################
    ##                              Loops if d/u aren't entered                               ##
    ############################################################################################
    *)
    ;;
    esac

done
