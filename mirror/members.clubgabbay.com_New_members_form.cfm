<! -- Copyright 1996 Mohave Mirage Company, Long Beach, CA 90814 (310) 433-9303 >
<! DYNAMIC Database Driven Website Development>
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2//EN">
<HTML>
<HEAD>
<TITLE>clubgabbay</TITLE>
   
</HEAD>
<body background="http://www.clubgabbay.com/images/bg/home_bg.jpg">

<H1 ALIGN=CENTER>ClubGabbay Membership Request</H1>




<FORM ACTION="New_members.CFM" METHOD="POST">
<INPUT TYPE="hidden" NAME="firstname_required" VALUE="You cannot leave the field (First name) empty.">
<INPUT TYPE="hidden" NAME="lastname_required" VALUE="You cannot leave the field (Last name) empty.">
<INPUT TYPE="hidden" NAME="address_required" VALUE="You cannot leave the field (Street Address) empty.">
<INPUT TYPE="hidden" NAME="city_required" VALUE="You cannot leave the field (City) empty.">
<INPUT TYPE="hidden" NAME="state_region_required" VALUE="You cannot leave the field (state_region) empty.">
<INPUT TYPE="hidden" NAME="country_required" VALUE="You cannot leave the field (Country) empty.">
<INPUT TYPE="hidden" NAME="dob_date" VALUE="The value in the field DATE OF BIRTH must be a valid date.">
<INPUT TYPE="hidden" NAME="dob_required" VALUE="You cannot leave the DATE OF BIRTH empty.">
<INPUT TYPE="hidden" NAME="email_required" VALUE="You cannot leave the EMAIL empty.">
<INPUT TYPE="hidden" NAME="gender_required" VALUE="You cannot leave GENDER empty.">
<INPUT TYPE="hidden" NAME="username_required" VALUE="You cannot leave USERNAME empty.">
<INPUT TYPE="hidden" NAME="password_required" VALUE="You cannot leave PASSWORD empty.">
<INPUT TYPE="hidden" NAME="password2_required" VALUE="You cannot leave PASSWORD CONFIRMATION empty.">
<INPUT TYPE="hidden" NAME="maidenname_required" VALUE="You cannot leave the Mother's maiden name empty.">
<INPUT TYPE="hidden" NAME="height_centimeters_integer" VALUE="The value in the field (Height in centimeters) must be an integer.">
<INPUT TYPE="hidden" NAME="height_feet_integer" VALUE="The value in the field (Height -- Feet) must be an integer.">
<INPUT TYPE="hidden" NAME="height_inches_integer" VALUE="The value in the field (Height --Inches) must be an integer.">
<INPUT TYPE="hidden" NAME="bodytype" VALUE="">
<INPUT TYPE="hidden" NAME="religion" VALUE="">
<INPUT TYPE="hidden" NAME="ethnicity" VALUE="">


<HR Size=5>
<B><EM><BIG>
<P>
Welcome to ClubGabbay!  We are sure that you will enjoy being a member of the Club and we are very happy to have you join us.
<P> 
</EM></BIG></B>
<HR SIZE=5>
<h2>FIRST -- THE REQUIRED INFORMATION</h2>
<B>This information is for internal Club use only.  Information entered here will not be available to other members of the club.<BR>
<HR SIZE=5>

<TABLE>

<TR>
<TD ALIGN=RIGHT WIDTH="20%"><B>First name</B></TD>

<TD><INPUT TYPE="text" NAME="firstname" SIZE="30" MAXLENGTH="40"></TD>
</TR>

<TR>
<TD ALIGN="right"><B>Last name</B></TD>

<TD><INPUT TYPE="text" NAME="lastname" SIZE="30" MAXLENGTH="40"></TD>
</TR>

<TR>
<TD ALIGN="right"><B>Middle Name/Initial</B></TD>

<TD><INPUT TYPE="text" NAME="middlename" SIZE="20" MAXLENGTH="50"></TD>
</TR>

<TR>
<TD ALIGN="right"><B>Street Address</B></TD>

<TD><INPUT TYPE="text" NAME="address" SIZE="50" MAXLENGTH="50"></TD>
</TR>

<TR>
<TD ALIGN="right"><B>City</B></TD>

<TD><INPUT TYPE="text" NAME="city" SIZE="50" MAXLENGTH="50"></TD>
</TR>

<TR>
<TD ALIGN="right"><B>State</B></TD>

<TD><SELECT NAME="state_region">
<OPTION VALUE="OU">OUTSIDE THE US
<OPTION VALUE="AL">ALABAMA
<OPTION VALUE="AK">ALASKA
<OPTION VALUE="AS">AMERICAN SAMOA
<OPTION VALUE="AZ">ARIZONA 
<OPTION VALUE="AR">ARKANSAS 
<OPTION VALUE="CA">CALIFORNIA
<OPTION VALUE="CO">COLORADO 
<OPTION VALUE="CT">CONNECTICUT
<OPTION VALUE="DE">DELAWARE
<OPTION VALUE="DC">DISTRICT OF COLUMBIA
<OPTION VALUE="FM">FEDERATED STATES OF MICRONESIA
<OPTION VALUE="FL">FLORIDA
<OPTION VALUE="GA">GEORGIA
<OPTION VALUE="GU">GUAM
<OPTION VALUE="HI">HAWAII
<OPTION VALUE="ID">IDAHO
<OPTION VALUE="IL">ILLINOIS
<OPTION VALUE="IN">INDIANA
<OPTION VALUE="IA">IOWA
<OPTION VALUE="KS">KANSAS
<OPTION VALUE="KY">KENTUCKY
<OPTION VALUE="LA">LOUISIANA
<OPTION VALUE="ME">MAINE
<OPTION VALUE="MH">MARSHALL ISLANDS
<OPTION VALUE="MD">MARYLAND
<OPTION VALUE="MA">MASSACHUSETTS
<OPTION VALUE="MI">MICHIGAN
<OPTION VALUE="MN">MINNESOTA
<OPTION VALUE="MS">MISSISSIPPI
<OPTION VALUE="MO">MISSOURI
<OPTION VALUE="MT">MONTANA
<OPTION VALUE="NE">NEBRASKA
<OPTION VALUE="NV">NEVADA
<OPTION VALUE="NH">NEW HAMPSHIRE
<OPTION VALUE="NJ">NEW JERSEY
<OPTION VALUE="NM">NEW MEXICO
<OPTION VALUE="NY">NEW YORK
<OPTION VALUE="NC">NORTH CAROLINA
<OPTION VALUE="ND">NORTH DAKOTA
<OPTION VALUE="MP">NORTHERN MARIANA ISLANDS
<OPTION VALUE="OH">OHIO
<OPTION VALUE="OK">OKLAHOMA
<OPTION VALUE="OR">OREGON
<OPTION VALUE="PW">PALAU
<OPTION VALUE="PA">PENNSYLVANIA
<OPTION VALUE="PR">PUERTO RICO
<OPTION VALUE="RI">RHODE ISLAND
<OPTION VALUE="SC">SOUTH CAROLINA
<OPTION VALUE="SD">SOUTH DAKOTA
<OPTION VALUE="TN">TENNESSEE
<OPTION VALUE="TX">TEXAS
<OPTION VALUE="TT">TRUST TERRITORIES
<OPTION VALUE="UT">UTAH
<OPTION VALUE="VT">VERMONT
<OPTION VALUE="VI">VIRGIN ISLANDS
<OPTION VALUE="VA">VIRGINIA
<OPTION VALUE="WA">WASHINGTON
<OPTION VALUE="WV">WEST VIRGINIA
<OPTION VALUE="WI">WISCONSIN
<OPTION VALUE="WY">WYOMING
</SELECT></TD>
</TR>


<tr>
            <td align="right"><b>5 digit ZIP code - USA residents
            only</b></td>
            <td><input type="text" size="5" maxlength="5"
            name="zip">(used to calculate your distance from
            other members and RainBEAUs)</td>
        </tr>
        <tr>
            <td align="right"><b><font color="red">OR </font>select the International location closest to you
            </b></td>
            <td>
<select name="zip">(used to calculate your distance from
            other members and WebDates matches)
<OPTION>

<Option>Afghanistan/Kabul

<Option>Alberta/Cold Lake

<Option>Alberta/Edmonton

<Option>Alberta/Fort McMurray

<Option>Alberta/Jasper

<Option>Alberta/Lethbridge

<Option>Alberta/Medicine Hat

<Option>Alberta/Peace River

<Option>Argentina/Buenos Aires

<Option>Ascension Island

<Option>Austral/Alice Springs

<Option>Australia/Adelaide

<Option>Australia/Avalon

<Option>Australia/Brisbane

<Option>Australia/Canberra

<Option>Australia/Darwin

<Option>Australia/Ipswich

<Option>Australia/Kings Beach

<Option>Australia/Latham

<Option>Australia/Learmonth

<Option>Australia/Melbourne

<Option>Australia/New Castle

<Option>Australia/Pearce

<Option>Australia/Perth

<Option>Australia/Richmond

<Option>Australia/Sale

<Option>Australia/Sydney

<Option>Australia/Townsville

<Option>Austria/Innsbruck

<Option>Austria/Linz

<Option>Austria/Salzburg

<Option>Austria/Vandans

<Option>Austria/Vienna

<Option>Austria/Vols

<Option>Azores/Lajes

<Option>Babelthuap Island

<Option>Bahamas/Freeport

<Option>Bahamas/Nassau

<Option>Bahrain/Al Manamah

<Option>Bali

<Option>Bangladesh/Chittagong

<Option>Bangladesh/Dacca

<Option>Barbados

<Option>Belgium/Antwerp

<Option>Belgium/Brussels

<Option>Belgium/Oostende

<Option>Belize City

<Option>Bermuda

<Option>Bolivia/La Paz

<Option>Bolivia/Santa Cruz

<Option>Bosnia/Sarajevo

<Option>Brazil/Belem

<Option>Brazil/Brasilia

<Option>Brazil/Manaus

<Option>Brazil/Natal

<Option>Brazil/Recife

<Option>Brazil/Rio de Janeiro

<Option>Brazil/Sao Paulo

<Option>British Columbia/Abbotsford

<Option>British Columbia/Comox

<Option>British Columbia/Cranbrook

<Option>British Columbia/Fort Nelson

<Option>British Columbia/Kamloops

<Option>British Columbia/Prince George

<Option>British Columbia/Prince Rupert

<Option>British Columbia/Terrace

<Option>British Columbia/Vancouver

<Option>British Columbia/Victoria

<Option>Brunei

<Option>Bulgaria/Sofia

<Option>Cameroon/Douala

<Option>Canary Island/Las Palmas

<Option>Chad/N'djamina

<Option>Chile/Antofagasta

<Option>Chile/Arica

<Option>Chile/Concepcion

<Option>Chile/Puerto Montt

<Option>Chile/Santiago

<Option>Chile/Valparaiso

<Option>China/Beijing

<Option>China/Canton

<Option>China/Shanghai

<Option>Christmas Island

<Option>Cuba/Guantanamo Bay

<Option>Cuba/Havana

<Option>Cyprus/Nicosia

<Option>Czech Republic/Prague

<Option>Denmark/Aalborg

<Option>Denmark/Copenhagen

<Option>Denmark/Soeborg

<Option>Diego Garcia

<Option>Djibouti

<Option>Dominican Republic/Santo Domingo

<Option>Ecuador/Guayaquil

<Option>Ecuador/Quito

<Option>Egypt/Alexandria

<Option>Egypt/Aswan

<Option>Egypt/Cairo

<Option>El Salvador/San Salvador

<Option>England/Aldermaston

<Option>England/Birmingham

<Option>England/Blackpool

<Option>England/Bristol

<Option>England/Brize Norton

<Option>England/Cambridge

<Option>England/Derby

<Option>England/Dover

<Option>England/Farnborough

<Option>England/Finningley

<Option>England/Greenwich

<Option>England/Honington

<Option>England/Leeds

<Option>England/Liverpool

<Option>England/London

<Option>England/Manchester

<Option>England/Melksham

<Option>England/Newcastle

<Option>England/Nottingham

<Option>England/Portsmouth

<Option>England/Rochdale

<Option>England/Sandhurst

<Option>England/Sheffield

<Option>England/Southampton

<Option>England/Teignmouth

<Option>Ethiopia/Addis Ababa

<Option>Ethiopia/Asmara

<Option>Falkland Island/Stanley

<Option>Fiji/Nandi

<Option>Finland/Dalsbruk

<Option>Finland/Helsinki

<Option>France/Bordeaux

<Option>France/Brest

<Option>France/Calais/Dunkirk

<Option>France/Cannes

<Option>France/Cherbourg

<Option>France/Dijon

<Option>France/Gaillac

<Option>France/Grenoble

<Option>France/La Rochelle

<Option>France/Le Havre

<Option>France/Lyon

<Option>France/Marseille

<Option>France/Montpellier

<Option>France/Nice

<Option>France/Nouan

<Option>France/Orleans

<Option>France/Paris

<Option>France/Reims

<Option>France/Rennes

<Option>France/Rouen

<Option>France/St. Nazaire

<Option>France/Strasbourg

<Option>France/Toulouse

<Option>France/Tours

<Option>French Polynesia/Hao Alberta

<Option>Gabon/Libreville

<Option>Gambia/Banjul

<Option>Germ/Oberpfaffenhofen

<Option>Germany/Altenstadt

<Option>Germany/Ansbach

<Option>Germany/Bamberg

<Option>Germany/Berlin

<Option>Germany/Bitburg

<Option>Germany/Bonn

<Option>Germany/Bremen

<Option>Germany/Buckeburg

<Option>Germany/Cologne

<Option>Germany/Dortmund

<Option>Germany/Dusseldorf

<Option>Germany/Erding

<Option>Germany/Erfurt

<Option>Germany/Frankfurt

<Option>Germany/Freiburg

<Option>Germany/Furth

<Option>Germany/Gars_am_Inn

<Option>Germany/Geilenkirchen

<Option>Germany/Gera

<Option>Germany/Gutersloh

<Option>Germany/Hamburg

<Option>Germany/Hannover

<Option>Germany/Helgoland

<Option>Germany/Kassel

<Option>Germany/Kiel

<Option>Germany/Koln

<Option>Germany/Lahr

<Option>Germany/Leck

<Option>Germany/Leipzig

<Option>Germany/Ludwigshafen

<Option>Germany/Mannheim

<Option>Germany/Munich

<Option>Germany/Nurnberg

<Option>Germany/Oldendorf

<Option>Germany/Ramstein Alberta

<Option>Germany/Regensburg

<Option>Germany/Rostock

<Option>Germany/Selter

<Option>Germany/Stuttgart

<Option>Germany/Uelzen

<Option>Germany/Wurzburg

<Option>Germany/Zwickau

<Option>Ghana/Accra

<Option>Gibraltar

<Option>Grand Cayman Island

<Option>Grand Turk Island

<Option>Greece/Athens

<Option>Greece/Khania

<Option>Greenland/Godthab

<Option>Greenland/Sondrestrom

<Option>Greenland/Thule

<Option>Guadalcanal/Honiara

<Option>Guam/Agana

<Option>Guatemala City

<Option>Guernsey

<Option>Guyana/Georgetown

<Option>Honduras/Tegucigalpa

<Option>Hong Kong

<Option>Hong Kong/Tai Tam

<Option>Hungary/Budapest

<Option>Iceland/Keflavik

<Option>Iceland/Reykjavik

<Option>India/Bangalore

<Option>India/Bombay

<Option>India/Calcutta

<Option>India/Madras

<Option>India/Nagpur

<Option>India/New_Delhi

<Option>Indones/Ujung_Pandang

<Option>Indonesia/Djakarta

<Option>Indonesia/Jakarta

<Option>Indonesia/Jatiluhur

<Option>Indonesia/Palembang

<Option>Iran/Bandar Abbass

<Option>Iran/Bandar Lengeh

<Option>Iran/Basrah

<Option>Iran/Esfahan

<Option>Iran/Shiraz

<Option>Iran/Tabriz

<Option>Iran/Tehran

<Option>Iraq/Baghdad

<Option>Iraq/Samarrah

<Option>Ireland/Belfast

<Option>Ireland/Dublin

<Option>Ireland/Shannon

<Option>Israel/Jerusalem

<Option>Israel/Raanana

<Option>Israel/Tel Aviv

<Option>Italy/Arese

<Option>Italy/Aviano

<Option>Italy/Bologna

<Option>Italy/Decimomannu

<Option>Italy/Genoa

<Option>Italy/Istrana

<Option>Italy/Milan

<Option>Italy/Naples

<Option>Italy/Rome

<Option>Italy/Venice

<Option>Jamaica/Kingston

<Option>Jamaica/Montego Bay

<Option>Japan/Amami Island

<Option>Japan/Ayase

<Option>Japan/Chitose

<Option>Japan/Fukuoka

<Option>Japan/Kyoto

<Option>Japan/Nagasaki

<Option>Japan/Nagoya

<Option>Japan/Okinawa

<Option>Japan/Osaka

<Option>Japan/Sapporo

<Option>Japan/Tokyo

<Option>Johnston Atoll

<Option>Jordan/Amman

<Option>Jordan/Aqaba

<Option>Kenya/Nairobi

<Option>Kure Island

<Option>Kuwait City

<Option>Kwajalein Atoll

<Option>Lebanon/Beirut

<Option>Liberia/Monrovia

<Option>Libya/Tripoli

<Option>Luxembourg City

<Option>Macao

<Option>Madeira Island/Funchal

<Option>Malaysia/Butterworth

<Option>Malaysia/Kota Kinabalu

<Option>Malaysia/Kuala_Lumpur

<Option>Malaysia/Kuching

<Option>Malaysia/Penang

<Option>Malaysia/Sibu

<Option>Maldive_Is./Male

<Option>Malta

<Option>Malta/Valletta

<Option>Manitoba/Brandon

<Option>Manitoba/Churchill

<Option>Manitoba/The_Pas

<Option>Manitoba/Winnipeg

<Option>Marshall Island/Ine

<Option>Marshall Island/Jaluit

<Option>Marshall Island/Kili

<Option>Marshall Island/Majuro

<Option>Marshall Island/Maloelap

<Option>Marshall Island/Mili

<Option>Marshall Island/Namorik

<Option>Marshall Island/Tinak

<Option>Marshall Island/Utirik

<Option>Marshall Island/Wotje

<Option>Mauritius/Plaisance

<Option>Micronesia/Chuuk

<Option>Micronesia/Kosrae

<Option>Micronesia/Pohnpei

<Option>Micronesia/Truk_Atoll

<Option>Micronesia/Yap Island

<Option>Midway Island

<Option>Miquelon Is.

<Option>Monaco

<Option>Morocco/Ben Guerir

<Option>Morocco/Casablanca

<Option>Morocco/Rabat

<Option>Morocco/Tangier

<Option>Myanmar/Mandalay

<Option>Myanmar/Rangoon

<Option>Myanmar/Sittwe

<Option>Nepal/Kathmandu

<Option>Netherlands/Amsterdam

<Option>Netherlands/Rotterdam

<Option>Netherlands/Wolphaartsdijk

<Option>New Brunswick/Chatham

<Option>New Brunswick/Edmundston

<Option>New Brunswick/Fredericton

<Option>New Brunswick/Moncton

<Option>New Brunswick/St. John

<Option>New Caledonia/Noumea

<Option>New Zealand/Auckland

<Option>New Zealand/Christchurch

<Option>New Zealand/Dunedin

<Option>New Zealand/Invercargill

<Option>New Zealand/Ohakea

<Option>New Zealand/Wellington

<Option>New Zealand/Whenuapai

<Option>Nfld./Goose Bay

<Option>Nfld./St. John's

<Option>Nfld/Gander

<Option>Nicaragua/Managua

<Option>Nigeria/Kano

<Option>Nigeria/Lagos

<Option>Northwest Territories/Alert

<Option>Northwest Territories/Fort_McPherson

<Option>Northwest Territories/Fort_Simpson

<Option>Northwest Territories/Inuvik

<Option>Northwest Territories/Iqaluit

<Option>Northwest Territories/Yellowknife

<Option>Norway/Bergen

<Option>Norway/Bodo

<Option>Norway/Oslo

<Option>Nova Scotia/Halifax

<Option>Nova Scotia/Sydney

<Option>Ontario/Dryden

<Option>Ontario/Guelph

<Option>Ontario/Hamilton

<Option>Ontario/Kapuskasing

<Option>Ontario/Kenora

<Option>Ontario/Kingston

<Option>Ontario/Kitchener

<Option>Ontario/London

<Option>Ontario/Mississauga

<Option>Ontario/North_Bay

<Option>Ontario/Ottawa

<Option>Ontario/Scarborough

<Option>Ontario/Sioux_Lookout

<Option>Ontario/Sioux_Narrows

<Option>Ontario/St. Catherines

<Option>Ontario/Sudbury

<Option>Ontario/Thunder Bay

<Option>Ontario/Timmins

<Option>Ontario/Toronto

<Option>Ontario/Waterloo

<Option>Ontario/Windsor

<Option>Pagan Island

<Option>Pakistan/Islamabad

<Option>Pakistan/Karachi

<Option>Pakistan/Lahore

<Option>Pakistan/Peshawar

<Option>Pakistan/Rawalpindi

<Option>Panama/Balboa

<Option>Panama/Colon

<Option>Panama/Panama City

<Option>Papua/Port Moresby

<Option>Paraguay/Asuncion

<Option>Peru/Chiclayo

<Option>Peru/Lima

<Option>Peru/Talara

<Option>Philippine/Cubi Point

<Option>Philippines/Bacolod

<Option>Philippines/Manila

<Option>Pitcairn_Island

<Option>Poland/Gdansk

<Option>Poland/Warsaw

<Option>Portugal/Beja

<Option>Portugal/Lisbon

<Option>Prince Edward Island/Charlottetown

<Option>Puerto Rico/Borinquen

<Option>Puerto Rico/Mayaguez

<Option>Puerto Rico/Ponce

<Option>Puerto Rico/Puerto Real

<Option>Puerto Rico/Roosevelt Roads

<Option>Puerto Rico/San Juan

<Option>Qatar/Doha

<Option>Quebec/Charlevoix

<Option>Quebec/Chibougamau

<Option>Quebec/Gaspe

<Option>Quebec/Laval

<Option>Quebec/Montreal

<Option>Quebec/Quebec

<Option>Quebec/Sherbrooke

<Option>Romania/Bucharest

<Option>Rota Island

<Option>Russia/Leningrad

<Option>Russia/Moscow

<Option>Russia/St. Petersburg

<Option>Russia/Vladivostok

<Option>Saipan Island

<Option>Samoa/Pago Pago

<Option>Saskatchewan/Moose Jaw

<Option>Saskatchewan/Saskatoon

<Option>Saskatchewan/Swift Current

<Option>Saudi_Arabia/Dhahran

<Option>Saudi_Arabia/Riyadh

<Option>Saudia_Arabia/Jeddah

<Option>Scotland/Aberdeen

<Option>Scotland/Edinburgh

<Option>Scotland/Glasgow

<Option>Scotland/Isle of Man

<Option>Senegal/Dakar

<Option>Serbia/Belgrade

<Option>Seychelles_Island

<Option>Sicily/Sigonella

<Option>Sicily/Trapani

<Option>Singapore

<Option>Singapore/Tengah

<Option>SK/Prince_Albert

<Option>SK/Regina

<Option>So_Africa/Cape_Town

<Option>South Africa/Johannesburg

<Option>South Africa/Pretoria

<Option>South Korea/Cheju

<Option>South Korea/Seoul

<Option>Spain/Barcelona

<Option>Spain/Madrid

<Option>Spain/Moron_Alberta

<Option>Spain/Seville

<Option>Spain/Zaragoza

<Option>Sri_Lanka/Colombo

<Option>St._Lucia

<Option>Sudan/Khartoum

<Option>Sweden/Hyltebruk

<Option>Sweden/Stockholm

<Option>Switzerland/Bern

<Option>Switzerland/Geneva

<Option>Switzerland/Zurich

<Option>Syria/Damascus

<Option>Tahiti

<Option>Tahiti/Papeete

<Option>Taiwan/Taipei

<Option>Tanzan./Dar_es_Salaam

<Option>Taora_Island

<Option>Thailand/Bangkok

<Option>Thailand/Chiang Mai

<Option>Thailand/Hat Yai

<Option>Thailand/Korat

<Option>Thailand/Phuket

<Option>Thailand/Ubon

<Option>Tibet/Lhasa

<Option>Tinian_Island

<Option>Trinida/Port of Spain

<Option>Tunisia/Tunis

<Option>Turkey/Ankara

<Option>Turkey/Bandirma

<Option>Turkey/Diyarbakir

<Option>Turkey/Incirlik

<Option>Turkey/Istanbul

<Option>U.A.E./Bahrain

<Option>U.A.E./Dubai

<Option>Uganda/Entebbe

<Option>Ukraine/Yalta

<Option>Uruguay/Montevideo

<Option>Vanuatu/Efate

<Option>Venezuela/Caracas

<Option>Venezuela/Maiquetia

<Option>Virgin Islands/St. Croix

<Option>Virgin Islands/St. Thomas

<Option>Wake_Island

<Option>Wales/Cardiff

<Option>Yemen

<Option>YT/Burwash

<Option>Yukon/Whitehorse

<Option>Zaire/Kinshasa

<Option>Zambia/Lusaka

</SELECT>
</td> </tr>


<TR>
<TD ALIGN="right"><B>Country</B></TD>

<TD><INPUT TYPE="text" NAME="country" SIZE="30" MAXLENGTH="30" VALUE="USA"></TD>
</TR>

<TR>
<TD ALIGN="right"><B>Date of Birth (MM/DD/YY)</B></TD>

<TD><INPUT TYPE="text" NAME="dob" SIZE="12" MAXLENGTH="12"></TD>
</TR>

<TR>
<TD ALIGN="center" colspan=2><B><font color="red">A VALID EMAIL ADDRESS IS REQUIRED</font> to obtain your Membership Unlock code and maintain your ClubGabbay membership</TD></TR>
<TR>
<TD ALIGN="right"><B>Email Address</B></TD>

<TD><INPUT TYPE="text" NAME="email" SIZE="50" MAXLENGTH="50"></TD>
</TR>

<TR>
<TD ALIGN="right"><B>Gender</B></TD>

<TD><INPUT TYPE="radio" NAME="gender" VALUE="M" CHECKED>Male <INPUT TYPE="radio" NAME="gender" VALUE="F">Female<BR>
</TD>
</TR>
<TR>
<TD ALIGN="right"><B>Unique ID (used to look up or change your username or password - USE SOMETHING YOU WILL REMEMBER..how about your mother's maiden name?)</B></TD>

<TD><INPUT TYPE="text" NAME="maidenname" SIZE="50" MAXLENGTH="50"></TD>
</TR>
</TABLE>


<! **** OPTIONAL INFO *****>
<HR SIZE=5>
<h2>NEXT -- THE OPTIONAL STUFF</h2>
<B>This information is used in various areas throughout the Club.<BR>
<HR SIZE=5>
<TABLE>

<TR>
<TD ALIGN=RIGHT WIDTH="20%"><B>Phone(not displayed)</B></TD>

<TD><INPUT TYPE="text" NAME="phone" SIZE="20" MAXLENGTH="20"></TD>
</TR>

<TR>
<TD ALIGN="right"><B>Home Page URL</B></TD>

<TD><strong>http://</strong><INPUT TYPE="text" NAME="URL" SIZE="50" MAXLENGTH="50"><BR><strong> (if provided, will "hyperlink" your name in chat and throughout the site)</strong></TD>
</TR>

<TR>
<TD colspan=2> <B><HR SIZE=5><BR>
The following information will be displayed in your Personal Profile and may be used by the WebDates area<BR><HR SIZE=5></TD
</TR>
<TR>
<TD ALIGN="right"><B>Body type</B></TD>
<TD><INPUT TYPE="radio" NAME="bodytype" VALUE="X"><B>
Prefer not to say 
<INPUT TYPE="radio" NAME="bodytype" VALUE="S"><B>
Slim/Slender
<INPUT TYPE="radio" NAME="bodytype" VALUE="A"><B>
Average(weight &amp; height
proportional) </TD>
</TR>

<TR>
<TD></TD>

<TD><INPUT TYPE="radio" NAME="bodytype" VALUE="T"><B>
Athletic
 <INPUT TYPE="radio" NAME="bodytype" VALUE="F"><B>
A
few extra pounds 
<INPUT TYPE="radio" NAME="bodytype" VALUE="L"><B>
Lots to
Love 
</TD>
</TR>

<TR>
<TD ALIGN="right"><B>If you like, describe your body type </B></TD>

<TD><INPUT TYPE="text" NAME="bodytype_text" SIZE="50" MAXLENGTH="50"></TD>
</TR>

<TR>
<TD ALIGN="right"><B>Ethnicity</B></TD>

<TD>
<INPUT TYPE="radio" NAME="ethnicity" VALUE="X"><B>Prefer not to say/Other
<INPUT TYPE="radio" NAME="ethnicity" VALUE="B"><B> Black /African-American
<INPUT TYPE="radio" NAME="ethnicity" VALUE="A"><B> Asian
<INPUT TYPE="radio" NAME="ethnicity" VALUE="C"><B>Caucasian
<INPUT TYPE="radio" NAME="ethnicity" VALUE="H"><B> Hispanic 
</TD>
</TR>

<TR>
<TD ALIGN="right"><B>If you like, provide a further description of your
ethnicity</B></TD>

<TD><INPUT TYPE="text" NAME="ethnicity_text" SIZE="50" MAXLENGTH="50"></TD>
</TR>

<TR>
<TD ALIGN="right"><B>Height</B></TD>

<TD><INPUT TYPE="text" NAME="height_feet" SIZE="2" MAXLENGTH="2" VALUE=0>&nbsp<B>Feet
<INPUT TYPE="text" NAME="height_inches" SIZE="3" MAXLENGTH="3" VALUE=0>Inches<I>&nbsp;OR&nbsp;</I>
Height in centimeters
<INPUT TYPE="text" NAME="height_centimeters" SIZE="4" MAXLENGTH="4" VALUE=0>
</B></TD>
</TR>

<TR>
<TD ALIGN="right"><B>Religion</B></TD>

<TD>
<INPUT TYPE="radio" NAME="religion" VALUE="X"><B>Prefer not to say/Other
<INPUT TYPE="radio" NAME="religion"  VALUE="A"><B>Atheist
<INPUT TYPE="radio" NAME="religion"  VALUE="B"><B>Buddhist/Taoist 
<INPUT TYPE="radio" NAME="religion"  VALUE="R"><B>Catholic 
<BR>
<INPUT TYPE="radio" NAME="religion"  VALUE="C"><B>Christian
<INPUT TYPE="radio" NAME="religion"  VALUE="H"><B>Hindu 
<INPUT TYPE="radio" NAME="religion"  VALUE="I"><B>Islamic 
<INPUT TYPE="radio" NAME="religion"  VALUE="J"><B>Jewish
</TD>
</TR>

<TR>
<TD ALIGN="right"><B>Describe your religious beliefs</B></TD>

<TD><INPUT TYPE="text" NAME="religion_text" SIZE="50" MAXLENGTH="100"></TD>
</TR>

<TR>
<TD ALIGN="right"><B>Personal Headline</B></TD>

<TD>
<textarea NAME="headline" ROWS="2" COLS="50"></textarea>
</TD>
</TR>

<TR>
<TD ALIGN="right"><B>Show my profile</B></TD>

<TD><INPUT TYPE="checkbox" NAME="show_flag" VALUE="1" CHECKED>Uncheck this box if you don't wish your personal information to be displayed to other members of the Club.
</TD>
</TR>
</TABLE>

<! **** LOGIN INFO *****>
<HR SIZE=5>
<h2>LAST -- BUT NOT LEAST!</h2>
<B>Choose a USERNAME and PASSWORD.  Your USERNAME must be unique.  You can use up to 12 characters each. Choose a name that describes you - this is your "handle" in the Club that others will see in Chat, Webdates, and the Message Center. <em>Please, do not use SPACES or SPECIAL CHARACTERS</em> -- this will interfer with the Chat area.  You may change your username and password at any time in the Membership Services area.<em>YOUR USERNAME AND PASSWORD ARE NOT CASE SENSITIVE</em></b>
<TABLE>

<TR>
<TD ALIGN=RIGHT WIDTH="20%"><B>Username/Handle</B></TD>

<TD><INPUT TYPE="text" NAME="username" SIZE="12" MAXLENGTH="12">
</TD>
</TR>

<TR>
<TD ALIGN=RIGHT><B>Password</B></TD>
<TD><INPUT TYPE="password" NAME="password" SIZE="12" MAXLENGTH="12"></TD>
</TR>

<TR>
<TD ALIGN=RIGHT><B>CONFIRM your Password</B></TD>
<TD><INPUT TYPE="password" NAME="password2" SIZE="12" MAXLENGTH="12"></TD>
</TR>
</TABLE>

<CENTER><P><INPUT TYPE="submit" VALUE="Submit"></FORM></P></CENTER>

</BODY>
</HTML>

