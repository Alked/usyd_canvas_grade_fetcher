from modules.reqlib import *
import json
from modules.THE_GAME import *


class Assignment:
    def __init__(self):
        self.assignment_id = 'null'
        self.assignment_name = 'null'
        self.mark = 'N/A'
        self.full_mark = 'N/A'


class Course:
    def __init__(self, course_id, name):
        self.id = course_id
        self.name = name
        self.assignments = []
        self.hasAssignments = False

    def get_assignments(self):
        url = 'https://canvas.sydney.edu.au/courses/' + self.id + '/grades'  # Canvas standard mark URL
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/605.1.15 (KHTML, like Gecko) '
                          'Version/12.0.1 Safari/605.1.15',
            'Referer': 'https://canvas.sydney.edu.au/',
            'Connection': 'keep-alive'}
        raw_mark_page = get_page(url, headers)  # Get mark page text

        raw_mark_data_head = re.compile('\s*ENV = ')
        raw_mark_data_tail = re.compile(';\s*</script>')
        raw_mark_data = get_pat(raw_mark_data_head, raw_mark_data_tail, raw_mark_page)
        mark_data = json.loads(raw_mark_data)
        # All marks are saved inside section 'submissions', which is followed by section 'assignment_groups'.
        usr_id = mark_data['current_user']['id']
        for assignment in mark_data['submissions']:
            assignment_instance = Assignment()

            # Insert ID
            assignment_instance.assignment_id = assignment['assignment_id']

            # Insert mark
            mark = assignment['score']
            try:
                assignment_instance.mark = float(mark)
            except TypeError:
                assignment_instance.mark = 'Null'

            # Insert assignment name
            ass_name_head = '<a href=\"/courses/' + self.id + '/assignments/'
            ass_name_head += str(assignment_instance.assignment_id) + '/submissions/' + usr_id + '\">'
            ass_name_tail = '</a>'
            try:
                assignment_instance.assignment_name = (get_pat(ass_name_head, ass_name_tail, raw_mark_page))
            except AttributeError:
                assignment_instance.assignment_name = 'Hidden or unavailable mark'

            # Insert possible points, which are saved inside section 'assignment_groups'.
            for group in mark_data['assignment_groups']:
                for assignment_ in group['assignments']:
                    if assignment_instance.assignment_id == assignment_['id']:
                        full_mark = assignment_['points_possible']
                        try:
                            assignment_instance.full_mark = float(full_mark)
                        except ValueError:
                            assignment_instance.full_mark = full_mark
                        self.assignments.append(assignment_instance)
                        break
        self.hasAssignments = True

    def display_grades(self, usr_name, show_grade=True, show_null=True, show_full=True, show_individual=False, g=False):
        if g:
            show_individual = True
        if show_individual:
            tmp_aid = 0
            tmp_aid_to_ass_id_ls = []
            for assignment in self.assignments:
                tmp_aid += 1
                tmp_aid_to_ass_id_ls.append([tmp_aid, assignment.assignment_id])
                print(tmp_aid, '\t', end='')
                print(assignment.assignment_name)

            if g:
                game_stat = 1
                while game_stat:
                    print("Pick an assignment")
                    try:
                        usr_cmd = input(usr_name + ' | ' + self.name + ' > ')
                        current_assignment_id = None
                        display_ass_id = int(usr_cmd)
                        for pair in tmp_aid_to_ass_id_ls:  # Get current assignment ID
                            if pair[0] == display_ass_id:
                                current_assignment_id = pair[1]
                                break
                        if current_assignment_id is None:
                            print('Please check Assignment ID')
                            continue
                        for assignment in self.assignments:
                            if assignment.assignment_id == current_assignment_id:
                                game_stat = the_game(assignment.mark, assignment.full_mark)
                                break
                    except ValueError:
                        print('Please check Assignment ID')

            print('Enter \"quit\" to quit i mode')
            while True:
                usr_cmd = input(usr_name + ' | ' + self.name + ' > ')
                if usr_cmd == 'quit':
                    break
                try:
                    current_assignment_id = None
                    display_ass_id = int(usr_cmd)
                    for pair in tmp_aid_to_ass_id_ls:  # Get current assignment ID
                        if pair[0] == display_ass_id:
                            current_assignment_id = pair[1]
                            break
                    if current_assignment_id is None:
                        print('Please check Assignment ID')
                        continue
                    for assignment in self.assignments:
                        if assignment.assignment_id == current_assignment_id:
                            print(assignment.mark, '\t', assignment.assignment_name)
                            break
                except ValueError:
                    print('Please check Assignment ID')
                    continue
        if show_grade and show_null and show_full:
            for assignment in self.assignments:
                print(assignment.mark, ' out of ', assignment.full_mark, '\t', assignment.assignment_name)

        elif show_grade and not show_null and show_full:
            for assignment in self.assignments:
                if assignment.mark != 'Null':
                    print(assignment.mark, '\tout of\t', assignment.full_mark, '\t', assignment.assignment_name)

        elif show_grade and show_null and not show_full:
            for assignment in self.assignments:
                print(assignment.mark, '\t', assignment.assignment_name)

        elif not show_grade:
            for assignment in self.assignments:
                print('*\t', assignment.assignment_name)

        elif show_grade and not show_null and not show_full:
            for assignment in self.assignments:
                if assignment.mark != 'Null':
                    print(assignment.mark, '\t', assignment.assignment_name)
