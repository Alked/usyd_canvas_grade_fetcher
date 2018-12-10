from clslib import *
import getpass


# Login
login_check = False
while not login_check:
    credentials = input('Unikey > '), getpass.getpass('Password > ')

    # Credentials upload
    ref = get_referer('https://canvas.sydney.edu.au')
    cred_headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version'
                      '/12.''0.1 Safari/605.1.15',
        'Referer': ref,
        'Connection': 'keep-alive'}
    cred_data = {
        'UserName': 'shared\\' + credentials[0],
        'Password': credentials[1],
        'AuthMethod': 'FormsAuthentication'}

    redir_content, login_check = get_page(ref, cred_headers, cred_data, login_check=True)
    if login_check == 'DENY':
        print('Wrong Unikey / Password. Check again.')
        login_check = False
    else:
        login_check = True


# Redirect info process and get to Canvas Dashboard
redir_target = get_pat("action=\"", "\"><input", redir_content)
redir_data = {'SAMLResponse': get_pat("<input type=\"hidden\" name=\"SAMLResponse\" value=\"", "\" />", redir_content)}
redir_headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.'
                  '0.1 Safari/605.1.15',
    'Connection': 'keep-alive'}
dashboard_content = get_page(redir_target, redir_headers, redir_data, prompt='Redirecting')


# Collect course details
course_raw_content = get_pat('\"STUDENT_PLANNER_COURSES\":', '],\"STUDENT_PLANNER_GROUPS\"', dashboard_content)

# Construct Course instances
course_ls = []
courses = []
course_num = 0
for char in course_raw_content:
    if char == '{':
        course_num += 1
for char_ind in range(0, len(course_raw_content)):
    if course_raw_content[char_ind] == '{':
        for end_brak_ind in range(1, len(course_raw_content[char_ind:])):
            if course_raw_content[char_ind:][end_brak_ind] == '}':
                course_detail = course_raw_content[char_ind + 1:][:end_brak_ind].split(',')
                new_course_detail = []
                for item in course_detail:
                    item = item.split(':')
                    new_course_detail.append(item)
                course_ls.append(new_course_detail)
                break

for course in course_ls:
    course_name = course[1][1]
    course_id = course[9][1][1:-1]
    courses.append(Course(course_id, course_name[1:-1]))

print('------------- Login was successful ------------\n\n')
help_info()

while True:
    print()
    usr_cmd = input(credentials[0] + ' > ')

    tmp_cid = 0
    tmp_cid_to_course_id_ls = []
    for course in courses:
        tmp_cid += 1
        tmp_cid_to_course_id_ls.append([tmp_cid, course.id])

    if len(usr_cmd) >= 4 and usr_cmd[:4] == 'help':
        cmd_ls = usr_cmd.split(' ')
        if len(cmd_ls) == 1:
            help_info()
        elif len(cmd_ls) > 2:
            print('Too many arguments. Try help [command]')
            continue
        else:
            if cmd_ls[1] == 'courses':
                print('To show the list of unit of study you are enrolled in.')
                print('Course ID is the integer at the beginning of each line.')
                continue
            elif cmd_ls[1] == 'grade':
                print('To display all marks corresponded to the course specified.')
                print('A [Course ID] must follow.')
                print('If a flag is claimed, it must be typed before Course ID.')
                print('Flag \"f\" hides full marks (points possible to get).')
                print('Flag \"n\" filters out null marks')
                print('Flag \"m\" hides all marks, i.e. show only assignment names.')
                print('Flag \"i\" allows you to check assignment individually by ID until \"quit\" is entered.')
                print('e.g. grade fn 4')
                print('e,g, grade m 4')
                print('e.g. grade i 5')
                print('e.g. grade 3')
                continue
            else:
                print('Unsupported command.')

    elif usr_cmd == 'exit':
        print('Terminated')
        print()
        exit(0)

    elif usr_cmd == 'courses':
        print('Course ID\tCourse Name')
        for pair in tmp_cid_to_course_id_ls:
            print(pair[0], end='')
            print('\t', end='')
            for course in courses:
                if course.id == pair[1]:
                    print(course.name)

    elif len(usr_cmd) >= 6 and usr_cmd[:6] == 'grade ':
            cmd_ls = usr_cmd.split(' ')
            if len(cmd_ls) > 1:  # Possible valid command
                try:
                    current_course_id = None
                    display_course_id = int(usr_cmd[-1])  # Get tmp_cid
                    for pair in tmp_cid_to_course_id_ls:  # Get current course ID
                        if pair[0] == display_course_id:
                            current_course_id = pair[1]
                            break
                    if current_course_id is None:
                        print('Please check [Course ID]')
                        continue

                    course_instance = None
                    for course in courses:  # Get course instance
                        if course.id == current_course_id:
                            course_instance = course
                            break

                    if course_instance.hasAssignments:
                        pass
                    else:
                        course_instance.get_assignments()

                    if len(cmd_ls) > 2:  # Check flags
                        flags = cmd_ls[1:-1]
                        flags = str(flags)
                        # Display parameters initialization
                        show_grade = True
                        show_null = True
                        show_full = True
                        show_individual = False
                        if 'f' in flags:
                            show_full = False
                        elif 'n' in flags:
                            show_null = False
                        elif 'm' in flags:
                            show_grade = False
                        elif 'i' in flags:
                            show_individual = True
                        course_instance.display_grades(credentials[0], show_grade, show_null, show_full, show_individual)
                        continue

                    elif len(cmd_ls) == 2:
                        course_instance.display_grades(credentials[0])
                        continue
                except IndexError or TypeError:
                    print('Please check [Course ID]')
            else:
                print('Missing [Course ID]')
    else:
        print('Unsupported or wrong command')
