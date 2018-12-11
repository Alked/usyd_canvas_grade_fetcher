import re


def get_pat(head, tail, sample, recur=False):
    head_ind = re.search(re.compile(head), sample).span()[-1]
    tail_ind = re.search(re.compile(tail), sample[head_ind:]).span()[0]
    if recur:
        return head_ind, tail_ind + head_ind
    else:
        return sample[head_ind: tail_ind + head_ind]


def help_info():
    print('-------------------Help Information-------------------')
    print('Commands\t\tUsage\t\t\tDescription')
    print('help\t\thelp\t\t\tShow this information')
    print('courses\t\tcourses\t\t\tShow all courses you have enrolled in')
    print('grade\t\tgrade [course ID]\tShow all grades published under such course')
    print('exit\t\texit\t\t\tTerminate this script')
