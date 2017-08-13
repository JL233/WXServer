import itchat

itchat.auto_login(False)
friendList = itchat.get_friends(update=True)[1:]
for friend in friendList:
    itchat.send_image(r"C:\Users\jei88\Desktop\wallpaper\8ba4163865a6c651c05de22e45098374860ec81b97d66b1161842ee38d96b1d4.jpg",
                  friend['UserName'])
itchat.logout()