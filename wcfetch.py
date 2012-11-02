#!/usr/bin/python
##requiere python-mechanize y elinks
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
# Author: Matias Kreder <mkreder@gmail.com> 

import mechanize
import time
import os
br = mechanize.Browser()

uade_user = ""
uade_pass = ""
email = ""

def webcampuschange():
    os.system("echo Chequear webcampus por paginas de promocion o encuestas | mail -s 'error!' " + email)
    exit(1)

def fetch():
    try: 
    	br.open("https://www.webcampus.uade.edu.ar/")
    except urllib2.URLError:
	return status1
    forms = [f for f in br.forms()]
    form = forms[0]
    form["ctl00$ContentPlaceHolderMain$txtUser"] = uade_user
    form["ctl00$ContentPlaceHolderMain$txtClave1"] = uade_pass
    request2 = form.click()
    try:
        response2 = mechanize.urlopen(request2)
    except mechanize.HTTPError, response2:
        pass
    if response2.geturl() == "https://www.webcampus.uade.edu.ar/Publicidad/Mensaje_Avisos.aspx":
        response2 = br.open('https://www.webcampus.uade.edu.ar/Home.aspx')
    if response2.geturl() != 'https://www.webcampus.uade.edu.ar/Home.aspx':
        webcampuschange()
    out = response2.read()
    return out

print "obteniendo estado inicial"
status1 = fetch()

while True:
    print "comparando.."
    status2 = fetch()
    if status1 != status2:
	print "webcampus cambio"
        f = open('out','w') 
        f.write(status2)  
        f.close()
        os.system("elinks --dump out | awk ' /Cursada/ {flag=1;next} /CONSULTAS/{flag=0} flag { print }' | mail -s 'webcampus change' " + email)
        status1 = status2  
    else:
	print "webcampus no cambio"
    print "durmiendo por 30 mins"
    time.sleep(1800)

