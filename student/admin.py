from django.contrib import admin

from student.models import Student, Teacher, Attendance, Course, StudentCourse, CourseTeacher, Lecture, MyUser


# Register your models here.

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    model = Student
    list_display = ['student_no', 'student_name', 'student_surname']


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    model = Teacher
    list_display = ['teacher_no', 'teacher_name', 'teacher_surname']


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    model = Course


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    model = Attendance
    list_display = ['student_id', 'lecture_crn', 'date_attended', 'inout']


@admin.register(StudentCourse)
class StudentCourseAdmin(admin.ModelAdmin):
    model = StudentCourse
    list_display = ['student_table', 'lecture_table']


@admin.register(CourseTeacher)
class CourseTeacherAdmin(admin.ModelAdmin):
    model = CourseTeacher


@admin.register(Lecture)
class LectureAdmin(admin.ModelAdmin):
    model = Lecture
    list_display = ['course_id', 'lecture_crn', 'teacher_no']


@admin.register(MyUser)
class UserAdmin(admin.ModelAdmin):
    model = MyUser
