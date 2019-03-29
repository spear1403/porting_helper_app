class LineSplitter:

    def line_splitter(line):
        indent= idle= hover= action= pattern=None
        action = []
        line_lst = []
        line_content = line
        print(line_content)

        #count indentation spaces
        space = len(line_content) - len(line_content.lstrip(' '))
        indent = space * ' '

        line_lst = line_content.split()
        line_lst = [w.replace("'", '"') for w in line_lst]

        if "action" in line_content:
            print("found action")
            firstsplit = line_content.split('action')
            proba = firstsplit[0].split()
            print(proba)
            act = firstsplit[1].rstrip()
            act = act.rstrip(":")
            print(act)
            if 'focus_mask' in act:
                # action_split = action.split('focus_mask')
                # action = action_split[0]
                print("focus mask found after action")
                act = act.replace(' focus_mask True','')
            else:
                print("no focus mask")
            action.append('action {}'.format(act))

            for i,j in enumerate(proba):
                if 'unhovered' in j:
                    print('{0} {1}'.format(j,proba[i+1]))
                    action.append('{0} {1}'.format(j,proba[i+1]))
                elif 'hovered' in j:
                    print('{0} {1}'.format(j,proba[i+1]))
                    action.append('{0} {1}'.format(j,proba[i+1]))
            print(action)


            #find the image file

            for index,item in enumerate(line_lst):
                if 'xpos' in item:
                    if line_lst[index+1] != "0":
                        print("xpos has a value that is not 0")
                        action = None
                        print(action)
                        return indent, idle, hover, action
                elif 'xalign' in item:
                    if line_lst[index+1] != "0":
                        print("ypos has a value that is not 0")
                        action = None
                        print(action)
                        return indent, idle, hover, action
                elif item.strip() == "auto":
                    print("auto image")
                    image_string = line_lst[index+1]

                    if image_string.count('"') < 2:
                        index_number = 1
                        while image_string.count('"') < 2:
                            index_number += 1
                            image_string = "{0} {1}".format(image_string, line_lst[index+index_number])

                    image_string = image_string.strip('"')
                    idle = image_string.replace(r"%s", "idle")
                    print("idle:{}".format(idle))
                    hover = image_string.replace(r"%s", "hover")
                    print("hover:{}".format(hover))
                elif item.strip() == "hover":
                    print("found hover image")
                    hover = line_lst[index+1]
                    hover = hover.replace("'", '"')
                    hover = hover.strip('"')
                elif item.strip() == "idle":
                    print("found idle image")
                    idle = line_lst[index+1]
                    idle = idle.replace("'", '"')
                    idle = idle.strip('"')
                    if hover is None:
                        hover = idle

            print(hover)
        else:
            print("Fuck")
            indent= idle= hover= action= pattern=None

        print(action)
        return indent, idle, hover, action

if __name__ == '__main__':
    line = 'imagebutton auto "main_menu_sis_%s" focus_mask True action NullAction()'
    LineSplitter.line_splitter(line)
