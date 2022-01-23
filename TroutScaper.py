import requests
import http.client, urllib
from datetime import date
from bs4 import BeautifulSoup

#Variables
td_list = []
row_text = ""
final_text = ""
Current_Date = ""
AnotherBreakFlag = False
URL = "https://dwr.virginia.gov/fishing/trout-stocking-schedule/"
HaveSentNotificationToday = False

#Tries to read first line of TrouotInfoSaveFile, if does not exist go to exception
try:
    SaveFile = open("TroutInfoSaveFile.txt", "r+")
    FileDate = SaveFile.readline()
    NotificationToday = SaveFile.readline()

#Since files does not exist, create the file and open it in writeable mode
#and set FileDate to an empty string so the next if statement fails
except:
    SaveFile = open("TroutInfoSaveFile.txt", "w+")
    FileDate = ""

#Grabs current date and formats it to just the month and day without leading zeros ex December 7, December 8, December 9
Current_Date = date.today()
Current_Date = Current_Date.strftime("%B %-d")

#Check if new day if so then next line in save file may be "true" and it needs to be false so we set it to false
if Current_Date not in FileDate:
    HaveSentNotificationToday = False

elif NotificationToday.strip() == "True":
    HaveSentNotificationToday = True

#If we have sent a notification today then do not run the rest of the script
if Current_Date in FileDate and HaveSentNotificationToday:
    print("Already Checked today")
    SaveFile.close()
    quit()

#creates a TLS connection to the pushover API
conn = http.client.HTTPSConnection("api.pushover.net:443")

#requestes the page with the URL given in the URL variable
page = requests.get(URL) #Requests the webpage located at the URL

#Initialized the Beautiful Soup framework
soup = BeautifulSoup(page.content, "html.parser")

table = soup.find(id="stocking-table") #Finds the table called "stocking-table" located on the webpage
tr = table.find_all('tr') #Finds all the rows of the table

#go through each row and grab each column and store it as an array within an array
for row in tr:
    td_list.append(row.find_all("td"))

#Iterates through the column array
for i in range(len(td_list)):

    #Iterates through the column subarray
    for j in range(len(td_list[i])):

        #Check if there is an anything at the given elemennt
        if td_list[i]:

            #Only grab td tags that contain today's date
            if Current_Date not in str(td_list[i][0]):
                print(str(td_list[i][0])) 
                AnotherBreakFlag = True
                SaveFile.seek(0)
                SaveFile.write(Current_Date + "\n")
                SaveFile.write("False" + "\n")
                SaveFile.truncate()
                print("file written to")
                break
            
            #If the column subarray has the <li> tag then find the <li> tags and format it and add it to output
            if str(td_list[i][j]).find("<li>") != -1:
                li = td_list[i][j].find_all("li")
                
                for k in li:
                    row_text = row_text + k.text + " "

            #Add the text from the subcolumn array to the output        
            else:
                row_text = row_text + td_list[i][j].get_text() + " | "
        

    #Only add the rows with these key words in them to the final text to send off as notification
    if "Wise County" in row_text or "Scott County" in row_text or "City of Norton" in row_text:
        final_text = final_text + "\n" + row_text
    
    if AnotherBreakFlag:
        break
         
    row_text = ""

print(final_text)

#If the final text has text in it then send the final text to the pushover api to make the notification
if final_text != "":

    try:
        conn.request("POST", "/1/messages.json",
        urllib.parse.urlencode({
        "token": "a8v7xt7itd38en48ext5n3kfcb57pf",
        "user": "u58nfv6yfmrmjdwbywix3fk92hedzv",
        "message": final_text,
        }), { "Content-type": "application/x-www-form-urlencoded" })
        conn.getresponse()
        SaveFile.seek(0)
        SaveFile.write(Current_Date + "\n")
        SaveFile.write("True" + "\n")
        SaveFile.truncate()

    except:
        row_text = ""

SaveFile.close()
