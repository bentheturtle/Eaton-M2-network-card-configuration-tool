import requests
import tkinter as tk
import os
import time
import urllib
from PIL import ImageTk, Image 
from restStuff import *

requests.packages.urllib3.disable_warnings()

def pharseData(): #function that runs after parameter subbmition  
    errorlabel['text'] = "submitting information"
    userinput.get()#username
    passinput.get()#password
    devinput.get()#device name
    netinput.get()#netmask
    gateinput.get()#gateway
    newipinput.get()#new ip to set
    locinput.get()#location of device

    cardIp = "169.254.0.1"
    

    # update the password to allow ssh access // Password tempPasswd@3.0.5 can be changed as the password you need
    os.environ["BIOS_URL"] = "https://" + cardIp + "/rest/mbdetnrs/1.0"

    restClient = BiosClient()


    restClient.changePassword("admin", "admin", passinput.get())
    # Authenticate with the credentials you used on the first script

    url = 'https://{host}/rest/mbdetnrs/1.0/oauth2/token'.format(host=cardIp)

    json = {'username':userinput.get(),'password':passinput.get(),'grant_type':'password','scope':'GUIAccess'}

    response = requests.post(url, verify=False, json=json)
    print(response)
    if response.status_code != 200:
        os.system('mshta vbscript:Execute("msgbox ""There was an ERROR while submitting"":close")')
        errorlabel['text'] = 'ERROR'
        errorlabel.config(fg='red')
        return

    access_token = response.json()['access_token']
    print(access_token)


    # Update UPS identification
    url = 'https://{host}/rest/mbdetnrs/1.0/managers/1/identification'.format(host=cardIp)

    headers = {'Authorization':  'Bearer ' + access_token}

    json = {"location":locinput.get(),"contact":"","name":devinput.get()} #devinput, name of contact= username?, upsname??
    # single parameter json is allowed at each endpoint
    #json = {"location":"location1"}

    response = requests.put(url, verify=False, headers=headers, json=json)
    print(response)
    if response.status_code != 200:
        os.system('mshta vbscript:Execute("msgbox ""There was an ERROR while submitting"":close")')
        errorlabel['text'] = 'ERROR'
        errorlabel.config(fg='red')
        return

    # Settings First SNMP v1 community 

    url = 'https://{host}/rest/mbdetnrs/1.0/managers/1/networkService/protocols/snmp/v1/communities/1'.format(host=cardIp)
    headers = {'Authorization':  'Bearer ' + access_token}
    json = {"name":"Testingpublic","allowWrite":"false","enabled":"true"}
    response = requests.put(url, verify=False, headers=headers, json=json)
    print(response)
    if response.status_code != 200:
        os.system('mshta vbscript:Execute("msgbox ""There was an ERROR while submitting"":close")')
        errorlabel['text'] = 'ERROR'
        errorlabel.config(fg='red')
        return

    # Settings 2nd SNMP v1 community 

    url = 'https://{host}/rest/mbdetnrs/1.0/managers/1/networkService/protocols/snmp/v1/communities/2'.format(host=cardIp)
    headers = {'Authorization':  'Bearer ' + access_token}
    json = {"name":"TestingReadwrite","allowWrite":"true","enabled":"true"}
    response = requests.put(url, verify=False, headers=headers, json=json)
    print(response)
    if response.status_code != 200:
        os.system('mshta vbscript:Execute("msgbox ""There was an ERROR while submitting"":close")')
        errorlabel['text'] = 'ERROR'
        errorlabel.config(fg='red')
        return

   #enableing SNMP
    url = 'https://{host}/rest/mbdetnrs/1.0/managers/1/networkService/protocols'.format(host=cardIp)
    headers = {'Authorization':  'Bearer ' + access_token}
    json = {"snmp":{"enabled":"true","port":161,"v1":{"enabled":"true"},"v3":{"enabled":"true"}}}
    response = requests.put(url, verify=False, headers=headers, json=json)
    print(response)
    if response.status_code != 200:
        os.system('mshta vbscript:Execute("msgbox ""There was an ERROR while submitting"":close")')
        errorlabel['text'] = 'ERROR'
        errorlabel.config(fg='red')
        return

    #setting up trap reciver
    url = 'https://{host}/rest/mbdetnrs/1.0/managers/1/networkService/protocols/snmp/traps/receivers'.format(host=cardIp)
    headers = {'Authorization':  'Bearer ' + access_token}
    json = {"name":"Eaton UPS","enabled":"true","host":trapinput.get(),"protocol":1,"port":"162","community":"public"}
    response = requests.post(url, verify=False, headers=headers, json=json)
    print(response)
    if response.status_code != 200:
        os.system('mshta vbscript:Execute("msgbox ""There was an ERROR while submitting"":close")')
        errorlabel['text'] = 'ERROR'
        errorlabel.config(fg='red')
        return

    #Settings DNS 
    url = 'https://{host}/rest/mbdetnrs/1.0/managers/1/networkService/networkInterfaces/1/domain/dns'.format(host=cardIp)
    headers = {'Authorization':  'Bearer ' + access_token}
    json = {"preferredServer":"10.130.32.2","alternateServer":"10.130.32.6"}
    response = requests.put(url, verify=False, headers=headers, json=json)
    print(response)
    if response.status_code != 200:
        os.system('mshta vbscript:Execute("msgbox ""There was an ERROR while submitting"":close")')
        errorlabel['text'] = 'ERROR'
        errorlabel.config(fg='red')
        return

    #Setting FQDN
    url = 'https://{host}/rest/mbdetnrs/1.0/managers/1/networkService/networkInterfaces/1/domain'.format(host=cardIp)
    headers = {'Authorization':  'Bearer ' + access_token}
    json = {"fqdn":"CustomerUPS.customer.domain.name"}
    response = requests.put(url, verify=False, headers=headers, json=json)
    print(response)
    if response.status_code != 200:
        os.system('mshta vbscript:Execute("msgbox ""There was an ERROR while submitting"":close")')
        errorlabel['text'] = 'ERROR'
        errorlabel.config(fg='red')
        return

    #Settings FQDN part 2
    url = 'https://{host}/rest/mbdetnrs/1.0/managers/1/networkService/networkInterfaces/1/domain/settings'.format(host=cardIp)
    headers = {'Authorization':  'Bearer ' + access_token}
    json = {"hostname":"CustomerUPS", "mode":"0"}
    response = requests.put(url, verify=False, headers=headers, json=json)
    print(response)
    if response.status_code != 200:
        os.system('mshta vbscript:Execute("msgbox ""There was an ERROR while submitting"":close")')
        errorlabel['text'] = 'ERROR'
        errorlabel.config(fg='red')
        return

    #Settings FQDN part 3
    url = 'https://{host}/rest/mbdetnrs/1.0/managers/1/networkService/networkInterfaces/1/domain/settings/manual/'.format(host=cardIp)
    headers = {'Authorization':  'Bearer ' + access_token}
    json = {"domainName":"customer.domain.name"}
    response = requests.put(url, verify=False, headers=headers, json=json)
    print(response)
    if response.status_code != 200:
        os.system('mshta vbscript:Execute("msgbox ""There was an ERROR while submitting"":close")')
        errorlabel['text'] = 'ERROR'
        errorlabel.config(fg='red')
        return

    #Settings FQDN part 4
    url = 'https://{host}/rest/mbdetnrs/1.0/managers/1/networkService/networkInterfaces/1/domain/settings/manual/dns'.format(host=cardIp)
    headers = {'Authorization':  'Bearer ' + access_token}
    json = {"preferredServer":"8.8.8.8","alternateServer":"8.8.4.4"}
    response = requests.put(url, verify=False, headers=headers, json=json)
    print(response)
    if response.status_code != 200:
        os.system('mshta vbscript:Execute("msgbox ""There was an ERROR while submitting"":close")')
        errorlabel['text'] = 'ERROR'
        errorlabel.config(fg='red')
        return

    #Change IPv4 address
    url = 'https://{host}/rest/mbdetnrs/1.0/managers/1/networkService/networkInterfaces/1/ipv4/settings/manual'.format(host=cardIp)
    headers = {'Authorization':  'Bearer ' + access_token}
    json = {"address":newipinput.get(),"subnetMask":netinput.get(),"gateway":gateinput.get()}
    response = requests.put(url, verify=False, headers=headers, json=json)
    print(response)
    if response.status_code != 200:
        os.system('mshta vbscript:Execute("msgbox ""There was an ERROR while submitting"":close")')
        errorlabel['text'] = 'ERROR'
        errorlabel.config(fg='red')
        return

    #Apply Manual settings
    url = 'https://{host}/rest/mbdetnrs/1.0/managers/1/networkService/networkInterfaces/1/ipv4/settings'.format(host=cardIp)
    headers = {'Authorization':  'Bearer ' + access_token}
    json = {"dhcpEnabled":"False"}
    response = requests.put(url, verify=False, headers=headers, json=json)
    print(response)
    if response.status_code != 200:
        os.system('mshta vbscript:Execute("msgbox ""There was an ERROR while submitting"":close")')
        errorlabel['text'] = 'ERROR'
        errorlabel.config(fg='red')
        return
    
    
    os.system('mshta vbscript:Execute("msgbox ""Done"":close")')
    errorlabel['text'] = 'Done'
    errorlabel.config(fg='green')


def refreshfunc():
    connectionlabel.config(text="didnt detect", bg="red")

    response = os.popen(f"ping 169.254.0.1").read()

    if "Destination host unreachable" not in response:
        connectionlabel.config(text="detected", bg="green")

# =+=+=+= GUI code starts =+=+=+=
window = tk.Tk()
window.title("9SX Quick Network Card Configurator")
window.geometry("600x650")
window.resizable(False,False)

photo = ImageTk.PhotoImage(file = "origin.png")
window.iconphoto(False, photo)

notelabel = tk.Label(text="Note: Make sure that the UPS is ON and connecting the USB cable to the network card.\nplease configure the RNDIS TCP/IPv4 to IP = 169.254.0.150 and mask = 255.255.0.0")
logo = Image.open("eaton logo.png")
logo = ImageTk.PhotoImage(logo)

logolabel = tk.Label(image=logo)
logolabel.image = logo
logolabel.pack()

notelabel.pack()
userlabel = tk.Label(text="User name")
userlabel.pack()
userinput = tk.Entry(width=40)
userinput.insert(0,"admin")
userinput.config(state='disabled')
userinput.pack()

passlabel = tk.Label(text="Set Password")
passlabel.pack()
passinput = tk.Entry(width=40)
passinput.pack()

netlabel = tk.Label(text="Set Netmask")
netlabel.pack()
netinput = tk.Entry(width=40)
netinput.insert(0,"255.255.255.0")
netinput.pack()

gatelabel = tk.Label(text="Set GateWay")
gatelabel.pack()
gateinput = tk.Entry(width=40 )
gateinput.insert(0,"169.254.0.254")
gateinput.pack()

newiplabel = tk.Label(text="Set New IP Address")
newiplabel.pack()
newipinput = tk.Entry(width=40 )
newipinput.insert(0,"169.254.0.1")
newipinput.pack()

devlabel = tk.Label(text="Set Device Network Name")
devlabel.pack()
devinput = tk.Entry(width=40)
devinput.pack()

loclabel = tk.Label(text="Set Location")
loclabel.pack()
locinput = tk.Entry(width=40)
locinput.pack()

traplabel = tk.Label(text="Set Trap Ip")
traplabel.pack()
trapinput = tk.Entry(width=40)
trapinput.pack()

errorlabel = tk.Label(text="")
errorlabel.pack()

image1 = Image.open("unnamed.png")
test = ImageTk.PhotoImage(image1)

piclabel = tk.Label(image=test)
piclabel.image = test
piclabel.pack()

connectionlabel = tk.Label(text="didnt detect", bg="red")

response = os.popen(f"ping 169.254.0.1").read()

if "Destination host unreachable" not in response:
    connectionlabel = tk.Label(text="detected", bg="green")
connectionlabel.pack()

refreshbtn = tk.Button(text="refresh", command=refreshfunc)
refreshbtn.pack()

btn = tk.Button(width=30, height=10, bg="green", text="submit", command=pharseData)
btn.pack(pady=(2, 5) , side=tk.BOTTOM)
window.mainloop()
# =+=+=+= GUI code ends =+=+=+=
