from StudentHouse.register.views import *
from django.conf.urls import url
from django.urls import path
from StudentHouse.user.views import *
from StudentHouse.organization.views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from StudentHouse.api.views import *

urlpatterns = [
    # path("password-reset/<str:encoded_pk>/<str:token>/", ResetPassword.as_view(), name='reset-password'),  # Hii baadae tutaibadilisha...
    url(r'payment/$', payment, name="payment"),
    url(r'password_reset/$', password_reset, name="password_reset_api"),
    url(r'deleteoldevents/$', delete_old, name="deleteoldevents"),
    url(r'deleteexcuse/$', delete_excuse, name="deleteexcuse"),
    url(r'editsubjectresult/$', edit_subject_result, name="editsubjectresult"),
    url(r'editattendancy/$', edit_attendancy, name="editattendancy"),
    url(r'editstudent/$', edit_student, name="editstudent"),
    url(r'editexcuse/$', edit_excuse, name="editexcuse"),
    url(r'editclassexamtimetable/$', edit_class_exam_timetable, name="editclassexamtimetable"),
    url(r'editschoolexamtimetable/$', edit_school_exam_timetable, name="editschoolexamtimetable"),
    url(r'editorganization/$', edit_organization, name="editorganization"),
    url(r'editevent/$', edit_event, name="editevent"),
    url(r'editclasstimetable/$', edit_class_timetable, name="editclasstimetable"),
    url(r'editmwalimu/$', edit_mwalimu, name="editmwalimu"),
    url(r'deletemkondo/$', delete_mkondo, name="deletemkondo"),
    url(r'editmkondo/$', edit_mkondo, name="editmkondo"),
    url(r'addmkondo/$', add_mkondo, name="addmkondo"),
    url(r'editdarasa/$', edit_darasa, name="editdarasa"),
    url(r'editsubject/$', edit_subject, name="editsubject"),
    url(r'orgresults/$', org_results, name="orgresults"),
    url(r'studentsubjectresults/$', student_subject_results, name="studentsubjectresults"),
    url(r'orgattendancy/$', org_attendencies, name="orgattendancy"),
    url(r'parentcompleteprofile/$', parent_complete_profile, name="completeparentprofile"),
    url(r'projectmetadata/$', project_metadata, name="projectmetadata"),
    url(r'teacherattendancy/$', teacher_attendancy, name="teacherattendancy"),
    url(r'mwalimusubjectresults/$', mwalimu_subject_results, name="mwalimusubjectresults"),
    url(r'orgexcuses/$', org_excuses, name="orgexcuses"),
    url(r'createxcuse/$', create_excuse, name="createxcuse"),
    url(r'orgstudents/$', org_students, name="orgstudents"),
    url(r'mwalimuinfo/$', mwalimu_info, name="mwalimuinfo"),
    url(r'fetchorgexamtimetable/$', fetch_org_exam_timetable, name="fetchorgexamtimetable"), # i mean org exam time tables, im deleting with this
    url(r'orgexamtimetable/$', org_examtimetable, name="orgexamtimetable"),
    url(r'orgevents/$', org_events, name="orgevents"),
    url(r'fetchorgtimetables/$', org_timetables, name="fetchorgtimetables"),  # i mean org classes time tables
    url(r'fetchorgteachers/$', org_teachers, name="fetchorgteachers"),
    url(r'orgclasses/$', org_classes, name="orgclasses"),
    url(r'orgsubjects/$', org_subjects, name="orgsubjects"),
    url(r'addresult', add_subject_results, name="addresult"),
    url(r'createattendancy/$', create_attendacy, name="createattendancy"),
    url(r'disableschoolexamtimetable/$', disable_school_exam_timetable, name="disableschoolexamtimetable"),
    url(r'createschooltimetable/$', create_school_timetable, name="createschoolexamtimetable"),  # school exam timetable
    url(r'createclasstimetable/$', create_class_timetable, name="createclassexamtimetable"), # individual class timetable
    url(r'create_classtimetable/$', create_timetable, name="createclasstimetable"),
    url(r'addstudent/$', add_student, name="addstudent"),
    url(r'completemzaziprofile', complete_mzazi_profile, name="completemzaziprofile"),
    url(r'addsubject/$', create_subject, name='addsubject'),
    url(r'createsubjectresult/$', create_subject_result, name="createsubjectresult"),
    url(r'createevent/$', create_event, name="createevent"),
    # url(r'createtimetable/$', create_timetable, name="createtimetable"),
    url(r'completeinstituteprofile/$', complete_institute_profile, name='completeinstitute'),
    url(r'createmkondo/$', create_mkondo, name="createmkondo"),
    url(r'addclass/$', add_class, name="addclass"),
    url(r'completeteacherprofile/$', teacher_profile, name="teacher_complete"),
    url(r'admin_addteacher/$', admin_addteacher, name="admin_addteacher"),
    url(r'userdetail/$', user_details, name="userdetails"),
    url(r'register/$', register, name="register"),
    url(r'token/$', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    url(r'token/refresh/$', TokenRefreshView.as_view(), name='token_refresh'),
]
