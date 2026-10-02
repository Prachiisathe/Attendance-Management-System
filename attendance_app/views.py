from django.shortcuts import render,redirect
from .models import Student
from .models import Student, Attendance
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404
from .forms import StudentForm
from django.utils import timezone

# Create your views here.
def home(request):
    return render(request,'attendance_app/home.html')

def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)


        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = StudentForm()


    return render(request, "attendance_app/add_student.html", {"form": form})



def view_students(request):
    students=Student.objects.all()
    return render(request,'attendance_app/view.html',{'students':students})



def delete_student(request,id):
    student1=get_object_or_404(Student,id=id)
    student1.delete()
    return redirect('view_students')


def edit_student(request, id):
    student22 = get_object_or_404(Student, id=id)

    if request.method == 'POST':
        student22.student_name = request.POST['student_name']
        student22.roll_no = request.POST['roll_no']
        student22.student_class = request.POST['student_class']
        student22.department = request.POST['department']
        student22.email = request.POST['email']
        student22.phone_no = request.POST['phone_no']

        student22.save()
        return redirect('view_students')

    return render(request, 'attendance_app/edit_student.html', {'student': student22})


def attendance(request):
    students = Student.objects.all()

    if request.method == "POST":
        print("POST RECEIVED")
        for student in students:
            status = request.POST.get(f'attendance_{student.id}')
            print(student.student_name,status)

            if status:
                Attendance.objects.create(
                    student=student,
                    status=status
                )

        return redirect('attendance')

    return render(request, 'attendance_app/attendance.html', {'students': students})


def attendance_report(request):
    query = request.GET.get('q')
    date = request.GET.get('date')
    status = request.GET.get('status')

    records = Attendance.objects.all().order_by('-date')

    if query:
        records = records.filter(
            Q(student__student_name__icontains=query) |
            Q(student__roll_no__icontains=query)
        )

    if date:
        records = records.filter(date=date)

    if status:
        records = records.filter(status=status)

    return render(
        request,
        'attendance_app/attendance_report.html',
        {
            'records': records,
            'query': query,
            'date': date,
            'status': status,
        }
    )


def dashboard(request):
    today = timezone.now().date()


    total_students = Student.objects.count()


    present_today = Attendance.objects.filter(
        date=today,
        status="Present"
    ).count()


    absent_today = Attendance.objects.filter(
        date=today,
        status="Absent"
    ).count()


    context = {
        "total_students": total_students,
        "present_today": present_today,
        "absent_today": absent_today,
    }


    return render(request, "attendance_app/dashboard.html", context)

