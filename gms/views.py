from .models import Courses
from django.shortcuts import render,redirect,render_to_response
from django.contrib.auth import login,logout,authenticate
#from django.core.context_processors import csrf
from .models import Faculty,Student,Exam,Result,Total_Marks,global_var
from django.http import Http404 
from django import template
register = template.Library()

from django.views.decorators.cache import cache_control

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def log_in(request):
	if request.user.is_authenticated():
		return redirect('/authenticated/')
	else:
		if request.method=='POST':
			#request.POST['user_name']
			user_name=request.POST['user_name']
			password=request.POST['password']
			role=request.POST['role']
			userTemp=None
			if (role == "faculty"):
				try:
					userTemp=Faculty.objects.get(username=user_name,password=password)
				except Faculty.DoesNotExist:
					userTemp=None
			elif (role == "student"):
				try:
					userTemp=Student.objects.get(username=user_name,password=password)
				except Student.DoesNotExist:
					userTemp=None
			else:
				user = authenticate(username=user_name, password=password)
				if user is not None:					
					if (user.is_staff == False):
						error=request.session.pop('error',True)
						return render(request, "login.html", {'error':error})
					else:
						login(request, user)
						return redirect("/admin/")	
			if userTemp is None:
				#request.session['error']=True
				error=request.session.pop('error',True)
				return render(request, "login.html", {'error':error})
			else:
				login(request, userTemp)
				return redirect("/authenticated/",{'uname':userTemp.username})						
		else:
			return render(request, "login.html")
	
@cache_control(no_cache=True, must_revalidate=True, no_store=True)	
def authenticated(request):
	usertype="NULL"
	if request.user.is_authenticated():
		try:
			userTemp=Faculty.objects.get(username=request.user.username,password=request.user.password)
			usertype="Faculty"
		except Faculty.DoesNotExist:
			userTemp=None

		if (userTemp==None):
			try:
				userTemp=Student.objects.get(username=request.user.username,password=request.user.password)
				usertype="Student"
			except Student.DoesNotExist:
				userTemp=None
		if (usertype=="Faculty"):
			return render_to_response("faculty.html",{'faculty':userTemp})
		elif (usertype=="Student"):
			grade_arr = []
			courses = userTemp.courses_set.all()
			for course in courses :
				total=course.total_marks_set.get(student=userTemp).total_marks
				if total>course.a :
					grade_arr.append(10)
				elif total>course.b :
					grade_arr.append(8)
				elif total>course.c :
					grade_arr.append(6)
				elif total>course.d :
					grade_arr.append(4)
				else :
					grade_arr.append(0)
			count=0
			sgpa=0
			credits=0
			for course in courses :
				sgpa+=int(course.credit)*int(grade_arr[count])
				count+=1
				credits+=course.credit

			sgpa=float(sgpa)/float(credits)
			sgpa = round(sgpa,2)
			pr=global_var.objects.get(pk=3).publish_result

			return render_to_response("student.html",{'student':userTemp,'courses':courses,'credits':credits,'grade_arr':grade_arr,'sgpa':sgpa,'pr':pr})
		else :
			return redirect('/logout/')
	else:
		return redirect('/logout/')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def log_out(request):
	logout(request)

	return redirect('/login/')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def course(request,course_no):
	if request.method=="POST":
		if request.user.is_authenticated():
			try:
				userTemp=Faculty.objects.get(username=request.user.username,password=request.user.password)
			except Faculty.DoesNotExist:
				return redirect('/logout/')

			courses=userTemp.courses_set.all()
			course=courses[int(course_no)-1] 
			
			for std in course.students.all():
				total_marks=std.total_marks_set.get(course=course)
				total_marks.total_marks=0.0
				for exam1 in course.exam_set.all():
					marks=request.POST[std.username+"_"+exam1.name]
					result=Result.objects.get(student=std,exam=exam1,course=course)
					result.gained_marks=marks
					result.save()
					total_marks.total_marks+=float(marks)*(float(exam1.weightage))/(float(exam1.total_marks))
					total_marks.save()
			return redirect('/authenticated/'+str(course_no)+'/')


	else:
		if request.user.is_authenticated():
			try:
				userTemp=Faculty.objects.get(username=request.user.username,password=request.user.password)
			except Faculty.DoesNotExist:
				return redirect('/logout/')
			
			courses=userTemp.courses_set.all()
			course=courses[int(course_no)-1]
			total=0
			for std in Student.objects.all():
				for c in std.courses_set.all():
					try:
						r=Total_Marks.objects.get(student=std,course=c)
					except Total_Marks.DoesNotExist:
						r=Total_Marks(student=std,course=c)
						r.save()
			for exam in course.exam_set.all():
				total+=exam.weightage
			for std in course.students.all():
				for exam1 in course.exam_set.all():
					try:
						r=Result.objects.get(student=std,exam=exam1,course=course)
					except Result.DoesNotExist:
						r=Result(student=std,exam=exam1,course=course,gained_marks=0)
						r.save()
			results=Result.objects.filter(course=course)
			print course.exam_set.all
			return render(request,"course.html",{'total':total,'faculty':userTemp, 'course1':course,'course_no':int(course_no),'result':results})
		else:
			return redirect('/logout/')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def addexam(request,course_no):
	usertype="NULL"
	if request.user.is_authenticated():
		try:
			userTemp=Faculty.objects.get(username=request.user.username,password=request.user.password)
			usertype="Faculty"
		except Faculty.DoesNotExist:
			return redirect('/logout/')
		courses=userTemp.courses_set.all()
		course=courses[int(course_no)-1]
		if request.method=='POST':
			
			if (usertype=="Faculty"):
				totalmarks=request.POST['total_marks']
				examName=request.POST['examname']
				weightage=request.POST['weightage']
				if examName=='':
					error=request.session.pop('error',True)
					return render(request, "addexam.html", {'error':error})
				e=Exam()
				e.name=examName
				e.total_marks=totalmarks
				e.weightage=weightage
				
				
				e.course=course
				e.save()
				for student in course.students.all() :
					r=Result()
					r.exam=e
					r.course=course
					r.student=student
					r.save()
				return redirect("/authenticated/" + str(course_no)+"/",{'faculty':userTemp, 'course':course,'course_no':int(course_no)}) 
			else :
				return redirect('/logout/')
		else :			
			return render(request, "addexam.html" ,{'course_no':course_no,'course':course})
	else :
		return redirect('/logout/')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def setcriteria(request,course_no):	
	usertype="NULL"
	if request.user.is_authenticated():
		try:
			userTemp=Faculty.objects.get(username=request.user.username,password=request.user.password)
			usertype="Faculty"
		except Faculty.DoesNotExist:
			return redirect('/logout/')
		if (usertype=="Faculty"):
			courses=userTemp.courses_set.all()
			course=courses[int(course_no)-1]
			if request.method=='POST':
				grade_a=request.POST['grade_a']
				grade_b=request.POST['grade_b']
				grade_c=request.POST['grade_c']
				grade_d=request.POST['grade_d']
				if (grade_a<=grade_b or grade_b<=grade_c or grade_c<=grade_d):
					error=request.session.pop('error',True)
					return render(request, "setcriteria.html", {'error':error, 'course':course, 'course_no':int(course_no)})
				else :
					course.a=grade_a
					course.b=grade_b
					course.c=grade_c
					course.d=grade_d
					course.save()
					return redirect("/authenticated/" + str(course_no)+"/",{'faculty':userTemp, 'course':course,'course_no':int(course_no)}) 
			else :
				return render(request, "setcriteria.html",{'course':course,'course_no':int(course_no)})
				
		else:
			return redirect('/logout/');
	else:
		return redirect('/logout/')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def update_exam(request,course_no,exam_no):
	usertype="NULL"
	if request.user.is_authenticated():
		try:
			userTemp=Faculty.objects.get(username=request.user.username,password=request.user.password)
			usertype="Faculty"
		except Faculty.DoesNotExist:
			return redirect('/logout/')
		if (usertype=="Faculty"):
			courses=userTemp.courses_set.all()
			course=courses[int(course_no)-1]
			exam=Exam.objects.get(pk=exam_no)
			if request.method=='POST':
				for std in course.students.all():
					total_marks=std.total_marks_set.get(course=course)
					total_marks.total_marks=total_marks.total_marks-((exam.weightage)/(exam.total_marks))*(Result.objects.get(student=std,course=course,exam=exam)).gained_marks
					total_marks.save()
				exam.name=request.POST['exam_name']
				exam.total_marks=request.POST['total_marks']
				exam.weightage=request.POST['weightage']
				exam.save()
				for std in course.students.all():
					total_marks=std.total_marks_set.get(course=course)
					total_marks.total_marks=total_marks.total_marks+(float(exam.weightage)/float(exam.total_marks))*float((Result.objects.get(student=std,course=course,exam=exam)).gained_marks)
					total_marks.save()
				return redirect("/authenticated/" + str(course_no)+"/",{'faculty':userTemp, 'course':course,'course_no':int(course_no)}) 
			else :
				return render(request, "update_exam.html",{'course_no':course_no,'exam':exam,'course':course})
		else :
			return redirect('/logout/')
	else :
			return redirect('/logout/')
