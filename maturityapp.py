import json

from maturityoptions import MaturityOptions

maturityoption = MaturityOptions()

finished = False
while not finished:
    action_option = maturityoption.pick_action()

    if action_option == "1":
        return_to_main_menu = maturityoption.store_data()
        if not return_to_main_menu:
            finished = True

    if action_option == "2":
        return_to_main_menu = maturityoption.get_data()
        if not return_to_main_menu:
            finished = True



    if action_option == "3":
        return_to_main_menu = maturityoption.update_data()
        if not return_to_main_menu:
            finished = True
        

    if action_option == "4":
        return_to_main_menu = maturityoption.get_all()
        if not return_to_main_menu:
            finished = True

    if action_option == "5":
        return_to_main_menu = maturityoption.delete_question()
        if not return_to_main_menu:
            finished = True
    if action_option == "6":
        return_to_main_menu = maturityoption.try_sample()
        if not return_to_main_menu:
            finished = True


