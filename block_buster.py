from line_split import LineSplitter
import os
import get_hotspot

class BlockBuster:

    def block_handler(game_path, b_list, hotspot_dict):
        image_dict = {'DHB+"':'"images/defaults/home/backgrounds/',
                        'DHH+"':'"images/defaults/home/hotspot_hover/',
                        'DHI+"':'"images/defaults/home/hotspot_idle/',

                        'DSB+"':'"images/defaults/school/backgrounds/',
                        'DSH+"':'"images/defaults/school/hotspots_hover/',
                        'DSI+"':'"images/defaults/school/hotspots_idle/',

                        'EP1B+"':'"images/episode1_GS/backgrounds/',
                        'EP1H+"':'"images/episode1_GS/hotspots_hover/',
                        'EP1I+"':'"images/episode1_GS/hotspots_idle/',

                        'EP2B+"':'"images/episode2_GS/backgrounds/',
                        'EP2H+"':'"images/episode2_GS/hotspots_hover/',
                        'EP2I+"':'"images/episode2_GS/hotspots_idle/',

                        'EP3B+"':'"images/episode3_GS/backgrounds/',
                        'EP3H+"':'"images/episode3_GS/hotspots_hover/',
                        'EP3I+"':'"images/episode3_GS/hotspots_idle/',

                        'EP4B+"':'"images/episode4_GS/backgrounds/',
                        'EP4H+"':'"images/episode4_GS/hotspot_hover/',
                        'EP4I+"':'"images/episode4_GS/hotspot_idle/',

                        'EP5B+"':'"images/episode5_GS/backgrounds/',
                        'EP5H+"':'"images/episode5_GS/hotspot_hover/',
                        'EP5I+"':'"images/episode5_GS/hotspot_idle/',

                        'EP6B+"':'"images/episode6_GS/backgrounds/',
                        'EP6H+"':'"images/episode6_GS/hotspot_hover/',
                        'EP6I+"':'"images/episode6_GS/hotspot_idle/',

                        'EP7B+"':'"images/episode7_GS/backgrounds/',
                        'EP7H+"':'"images/episode7_GS/hotspot_hover/',
                        'EP7I+"':'"images/episode7_GS/hotspot_idle/',

                        'EP8B+"':'"images/episode8_GS/backgrounds/',
                        'EP8H+"':'"images/episode8_GS/hotspot_hover/',
                        'EP8I+"':'"images/episode8_GS/hotspot_idle/',

                        'EP9B+"':'"images/episode9_GS/backgrounds/'
                        }
        showerblock_destinations = {
                        "zone_complete":"images/showerblock01/showerblock_gui/showerblock01_zone_complete_%s.png",
                        "move_on":"images/showerblock01/showerblock_gui/showerblock01_move_on_%s.png",
                        "landing_to_shower":"images/showerblock01/showerblock_gui/showerblock01_landing_to_showers_%s.png",
                        "landing_to_door":"images/showerblock01/showerblock_gui/showerblock01_landing_to_door_%s.png",
                        "landing_to_basins":"images/showerblock01/showerblock_gui/showerblock01_landing_to_basins_%s.png",
                        "landing_to_lockers":"images/showerblock01/showerblock_gui/showerblock01_landing_to_lockers_%s.png",
                        "shower_to_lockers":"images/showerblock01/showerblock_gui/showerblock01_showers_to_lockers_%s.png",
                        "shower_to_basins":"images/showerblock01/showerblock_gui/showerblock01_showers_to_basins_%s.png",
                        "lockers_to_basins":"images/showerblock01/showerblock_gui/showerblock01_lockers_to_basins_%s.png",
                        "lockers_to_showers":"images/showerblock01/showerblock_gui/showerblock01_lockers_to_showers_%s.png",
                        "lockers_to_next_isle":"images/showerblock01/showerblock_gui/showerblock01_lockers_to_next_isle_%s.png"
                        }
        showerblock_chars = {
                        "basin_sexy_alien":"images/showerblock01/showerblock_gui/showerblock01_basins_sexy_alien_%s.png",
                        "basin_geek":"images/showerblock01/showerblock_gui/showerblock01_basins_geek_%s.png",
                        "shower_dude":"images/showerblock01/showerblock_gui/showerblock01_shower_dude_%s.png",
                        "shower_blonde":"images/showerblock01/showerblock_gui/showerblock01_shower_blonde_%s.png",
                        "shower_sexy_aliens":"images/showerblock01/showerblock_gui/showerblock01_shower_sexy_aliens_%s.png",
                        "lockers_jock":"images/showerblock01/showerblock_gui/showerblock01_locker_jock_%s.png",
                        "lockers_perv":"images/showerblock01/showerblock_gui/showerblock01_locker_perv_%s.png",
                        "lockers_purple":"images/showerblock01/showerblock_gui/showerblock01_locker_purple_%s.png",
                        "lockers_jock_peep":"images/showerblock01/showerblock_gui/showerblock01_locker_jock_peep_%s.png",
                        "lockers_perv_peep":"images/showerblock01/showerblock_gui/showerblock01_locker_perv_peep_%s.png",
                        "lockers_purple_peep":"images/showerblock01/showerblock_gui/showerblock01_locker_purple_peep_%s.png"
                        }
        tab = "    "
        indent = (len(b_list[0])-len(b_list[0].lstrip())) * " " + tab
        same_indent = indent
        action_indent = indent + tab
        empty_list = []
        hovered_list =[]
        unhovered_list =[]
        action_list = []
        condition_list = []
        xalign_index = None
        xpos_index = None
        ypos_index = None
        idle_index = None
        hover_index = None
        focus_index = None
        tooltip_index = None
        activate_sound_index = None
        hotspot = None

        for index,item in enumerate(b_list):
            if "xpos" in item:
                if "#" in item.split("xpos")[0]:
                    print("xpos line commented out")
                    continue
                else:
                    print("xpos {}".format(index))
                    xpos_index = index
            elif "ypos" in item:
                if "#" in item.split("ypos")[0]:
                    print("ypos line commented out")
                    continue
                else:
                    print("ypos {}".format(index))
                    ypos_index = index
            elif "xalign" in item:
                if "#" in item.split("xalign")[0]:
                    print("xalign line commented out")
                    continue
                else:
                    print("xalign {}".format(index))
                    xalign_index = index
            elif "action" in item:
                print("action {}".format(index))
                if index == 0:
                    print("imagebutton and action in same line of block")
                    indent, idle, hover, action_lst = LineSplitter.line_splitter(item)
                    if len(action_lst) == 1:
                        action = action_lst[0]
                    else:
                        action = " ".join(action_lst)
                    b_list[0] = "{}imagebutton:\n".format(indent)
                    b_list.insert(1, "{0}{1}{2}\n".format(indent,tab,action))
                    print(b_list)
                    b_list.insert(1, '{0}{1}hover "{2}"\n'.format(indent,tab,hover))
                    print(b_list)
                    b_list.insert(1, '{0}{1}idle "{2}"\n'.format(indent,tab,idle))
                    print(b_list)
                else:
                    action_list.append(index)


            elif "clicked" in item:
                print("clicked {}".format(index))
                action_list.append(index)
            elif "auto " in item:
                print("auto {}".format(index))
                hover_index = index
            elif " if " in item:
                print("conditions {}".format(index))
                condition_list.append(index)
            elif "else:" in item:
                print("conditions {}".format(index))
                condition_list.append(index)
            elif "unhovered" in item:
                print("unhovered {}".format(index))
                unhovered_list.append(index)
            elif "hovered" in item:
                print("hovered {}".format(index))
                hovered_list.append(index)
            elif "hover " in item:
                print("hover {}".format(index))
                hover_index = index
            elif "idle" in item:
                print("idle {}".format(index))
                idle_index = index
            elif "focus" in item:
                print("focus {}".format(index))
                focus_index = index
            elif "style" in item:
                print("style {}".format(index))
                focus_index = index
            elif "tooltip" in item:
                print("tooltip {}".format(index))
                tooltip_index = index
            elif "activate_sound" in item:
                print("activate_sound {}".format(index))
                activate_sound_index = index

        if hovered_list:
            print ("hovered_list: {}".format(len(hovered_list)))
        if unhovered_list:
            print ("unhovered_list: {}".format(len(unhovered_list)))
        if action_list:
            print ("action_list: {}".format(len(action_list)))
        if condition_list:
            print ("condition_list: {}".format(len(condition_list)))

        if xpos_index == None and ypos_index == None:
            xpos_index = 0
            ypos_index = 0

        if xalign_index is not None:
            xalign_value = b_list[xalign_index].split()[1]
            print(xalign_value)
            if xalign_value == "0.0" or xalign_value == "0.5":
                xpos_index = 0
                ypos_index = 0
            else:
                xpos_index = None

        if xpos_index is not None:
            if "imagebutton" in b_list[xpos_index] or ("xpos 0" in b_list[xpos_index] and "ypos 0" in b_list[ypos_index]) or ("xpos 0" in b_list[xpos_index] and "ypos -1" in b_list[ypos_index]):
                print("Yeah")
                print(''.join(b_list))
                if action_list:
                    if idle_index is not None:
                        if hover_index == None:
                            hover_index = idle_index
                    if hover_index is not None:
                        hover_line = b_list[hover_index]
                        if not '"' in hover_line:
                            print("No hover image")
                            return empty_list
                        ############ No more secrets ###########################
                        for k,v in image_dict.items():
                            if k in hover_line:
                                print(k, 'corresponds to', v)
                                hover_line = hover_line.replace(k,v)
                                break
                        ########################################################
                        image = hover_line.split('"')[1]
                        ############## Spacecorps XXX ##########################
                        if "showerblock_destinations" in hover_line:
                            for k,v in showerblock_destinations.items():
                                if k in hover_line:
                                    image = v
                                    break
                        if "showerblock_chars" in hover_line:
                            for k,v in showerblock_chars.items():
                                if k in hover_line:
                                    image = v
                                    break
                        ########################################################

                        image = image.lstrip("/")
                        print(image)
                        ############## Lylas Curse #############################
                        if "BG_" in image:
                            image_split = image.split("_")
                            print(image_split)
                            image = image.replace("BG_","images/Environments/")+".png"
                            print (image)
                            env_dirs = next(os.walk(os.path.join(game_path,"images/Environments/")))[1]
                            if env_dirs:
                                for i in image_split:
                                    if i in env_dirs:
                                        image = image.replace(i+"_",i+"/")
                                        print (image)
                                        break
                                second_dirs = next(os.walk(os.path.join(game_path,"images/Environments/",i+"/")))[1]
                                if second_dirs:
                                    print (second_dirs)
                                    second_dirs.sort(key=len, reverse=True)
                                    print (second_dirs)
                                    for s in second_dirs:
                                        if s in image:
                                            image = image.replace(s+"_",s+"/")
                                            print (image)
                                            break
                        if "PShop_" in image:
                            image = image.replace("PShop_","images/PShop/")+".png"
                            env_dirs = next(os.walk(os.path.join(game_path,"images/PShop/")))[1]
                            if env_dirs:
                                print (env_dirs)
                                env_dirs.sort(key=len, reverse=True)
                                print (env_dirs)
                                for e in env_dirs:
                                    if e in image:
                                        image = image.replace(e+"_",e+"/")
                                        second_dirs = next(os.walk(os.path.join(game_path,"images/PShop/",e+"/")))[1]
                                        if second_dirs:
                                            print (second_dirs)
                                            second_dirs.sort(key=len, reverse=True)
                                            print (second_dirs)
                                            for s in second_dirs:
                                                if s in image:
                                                    image = image.replace(s+"_",s+"/")
                                                    break
                                        break
                        ########################################################

                        image = image.replace(r"%s",'hover')
                        image = image.replace("[Timeday]",'2')
                        extens_list = [".png",".webp",".jpg"]
                        if not any(extens in image for extens in extens_list):
                            image = image+".png"

                        print(image)
                        gamedirs = next(os.walk(game_path))[1]
                        print(gamedirs)
                        found_image = os.path.join(game_path,"images",image)
                        for g in gamedirs:
                            if g in image:
                                found_image = os.path.join(game_path,image)

                        print(found_image)
                        if os.path.isfile(found_image):
                            print("The image exists")
                        else:
                            for f in gamedirs:
                                vidi = os.path.join(game_path,f,image)
                                if os.path.isfile(vidi):
                                    found_image = vidi
                                    print("found the image in:{}".format(vidi))
                                    break
                                # break
                            # break
                        if found_image in hotspot_dict:
                            hotspot = hotspot_dict.get(found_image)
                        else:
                            hotspot = get_hotspot.main(found_image, image)
                            hotspot_dict[found_image] = hotspot
                            # print(hotspot_dict)
                        print(hotspot)

                    if hotspot is not None:
                        if action_list:
                            if condition_list and condition_list[0] == action_list[0]-1:
                                print("changing indent")
                                indent = action_indent
                                action_indent = action_indent + "    "
                            for action_index in action_list:
                                b_list[action_index] = '{0}hotspot{1}:\n{2}{3}'.format(indent, hotspot,action_indent, b_list[action_index].lstrip())

                            if activate_sound_index is not None:
                                b_list[activate_sound_index] = "{0}{1}".format(action_indent,b_list[activate_sound_index].lstrip())

                            if tooltip_index is not None:
                                b_list[tooltip_index] = "{0}{1}".format(action_indent,b_list[tooltip_index].lstrip())

                            if focus_index is not None:
                                b_list[focus_index] = "{0}# {1}".format(same_indent,b_list[focus_index].lstrip())

                            # if hover_index is not None:
                            #     if 'auto' in b_list[hover_index]:
                            #         idle_line = b_list[hover_index].replace('auto','idle')
                            #         idle_line = idle_line.replace(r'%s','idle')
                            #         hover_line = idle_line.replace('idle','hover')
                            #         b_list[hover_index] = "{0}{1}".format(idle_line,hover_line)

                            b_list[0] = b_list[0].replace("imagebutton","imagemap")

                            if condition_list:
                                for condition_index in condition_list:
                                    # print(condition_list[0], hovered_list[0]-1)
                                    if condition_list[0] == action_list[0]-1:
                                        b_list[condition_index] = "{0}{1}".format(same_indent,b_list[condition_index].lstrip())
                                    elif len(condition_list) == len(hovered_list) or len(condition_list) == len(unhovered_list):
                                        if hovered_list:
                                            if condition_list[0] == hovered_list[0]-1:
                                                b_list[condition_index] = "{0}{1}".format(action_indent,b_list[condition_index].lstrip())
                                        if unhovered_list:
                                            if condition_list[0] == unhovered_list[0]-1:
                                                print("condition before unhovered")
                                                b_list[condition_index] = "{0}{1}".format(action_indent,b_list[condition_index].lstrip())
                                    else:
                                        condition_indent = (len(b_list[condition_index])-len(b_list[condition_index].lstrip())) * " "
                                        b_list[condition_index] = "{0}{1}".format(condition_indent,b_list[condition_index].lstrip())

                            if hovered_list:
                                for hovered_index in hovered_list:
                                    if len(condition_list) == len(hovered_list) and condition_list[0] == hovered_list[0]-1:
                                        b_list[hovered_index] = "{0}{1}".format(action_indent+"    ",b_list[hovered_index].lstrip())
                                    else:
                                        b_list[hovered_index] = "{0}{1}".format(action_indent,b_list[hovered_index].lstrip())

                            if unhovered_list:
                                for unhovered_index in unhovered_list:
                                    if len(condition_list) == len(unhovered_list) and condition_list[0] == unhovered_list[0]-1:
                                        b_list[unhovered_index] = "{0}{1}".format(action_indent+"    ",b_list[unhovered_index].lstrip())
                                    else:
                                        b_list[unhovered_index] = "{0}{1}".format(action_indent,b_list[unhovered_index].lstrip())

                            if hovered_list:
                                if hover_index < action_index:
                                    if condition_list and condition_list[0] == action_list[0]-1:
                                        extracted_condition = b_list.pop(condition_index)
                                        b_list.insert(hover_index+1, extracted_condition)
                                        extracted_action = b_list.pop(action_index)
                                        b_list.insert(hover_index+2, extracted_action)
                                        action_index = hover_index+2
                                    else:
                                        extracted_action = b_list.pop(action_index)
                                        b_list.insert(hover_index+1, extracted_action)
                                        action_index = hover_index+1

                            if activate_sound_index is not None:
                                if activate_sound_index < action_index:
                                    extracted_activate_sound = b_list.pop(activate_sound_index)
                                    b_list.insert(action_index+1, extracted_activate_sound)

                            if tooltip_index is not None:
                                if tooltip_index < action_index:
                                    extracted_tooltip = b_list.pop(tooltip_index)
                                    b_list.insert(action_index+1, extracted_tooltip)

                        else:
                            return empty_list
                    else:
                        return empty_list


                print(''.join(b_list))
                return b_list
        else:
            return empty_list
