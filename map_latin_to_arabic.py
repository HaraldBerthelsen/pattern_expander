#-*- coding: utf-8 -*- 


import sys, re



la2ar = {
    "<DisplayItemNo>":"<ديسبلاييتيمنومبير>",
    "<DynN-BestSelection>":"<ذذذذ>",
    "<SMS_templates>":"<ضضضض>",
    "<phone_types>":"<صصصص>",
    "<Title_USB>":"<ثثثث>",
    "<Title_iPod>":"<قققق>",
    "<Title_Jukebox>":"<فففف>",
    "<DisplayedN-BestSongs>":"<غغغغ>",
    "<DisplayedN-BestAlbums>":"<عععع>",
    "<ChannelName>":"<هههه>",
    "<FMChannelName>":"<خخخخ>",
    "<DigitalChannel>":"<حححح>",
    "<PresetNumber>":"<جججج>",
    "<AudioInput>":"<دددد>",
    "<DialogMode>":"<شششش>",
    "<UserProfileName>":"<سسسس>",
    "<PreferredAddress>":"<يييي>",
    "<LastDestinations>":"<بببب>",
    "<Artist_USB>":"<لللل>",
    "<Artist_Jukebox>":"<اااا>",
    "<Artist_iPod>":"<تتتت>",
    "<Album_USB>":"<نننن>",
    "<Album_iPod>":"<مممم>",
    "<Album_Jukebox>":"<كككك>",
    "<Contact>":"<طططط>",
    "<Address>":"<ئئئئ>",
    "<CityName>":"<ءءءء>",
    "<POIType>":"<ؤؤؤؤ>",
    "<POI>":"<رررر>",
    "<phone_number>":"<ﻻﻻﻻﻻ>",
    "<ArtistName>":"<ىىىى>",
    "<SongName>":"<ةةةة>",
    "<Province>":"<وووو>",
    "<distance>":"<زززز>",
    "<units>":"<ظظظظ>",
    "<minutes>":"<ذذضض>",
    "<hours>":"<صصثث>",
    "<time>":"<ققفف>",
    "<FM_Frequency>":"<غغعع>",
    "<AM_Frequency>":"<ههخخ>",
    "<AllMusic>":"<ححجج>",
    "<Song>":"<ددشش>",
    "<Artist>":"<سسيي>",
    "<Album>":"<ببلل>",
    "<StreetName1>":"<ااتت>",
    "<StreetName2>":"<ننمم>",
    "<Dictated_Text>":"<ككطط>",
    "<temperature>":"<ئئءء>"
}


ar2la = {}
for key in la2ar.keys():
    ar2la[la2ar[key]] = key






lines = sys.stdin.readlines()
for line in lines:
    line = line.strip()

    for key in la2ar.keys():
        line = re.sub(key, la2ar[key], line)

    print line
