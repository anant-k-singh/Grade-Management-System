from __future__ import unicode_literals
from django.db import models
from django.contrib.auth import models as md
class Courses(models.Model):
	course_name = models.CharField(max_length=30)

	#change to PositiveSmallIntegerField
	credit = models.PositiveSmallIntegerField(default=3)
	
	faculty = models.ForeignKey('Faculty',on_delete=models.PROTECT,null=True)
	students = models.ManyToManyField('Student')
	
	#change to PositiveSmallIntegerField
	a = models.PositiveSmallIntegerField(default=80)
	b = models.PositiveSmallIntegerField(default=60)
	c = models.PositiveSmallIntegerField(default=40)
	d = models.PositiveSmallIntegerField(default=20)
	
	#remove f not required anywhere
	#f = models.IntegerField(default=0)
	
	def __str__(self):
		return self.course_name
# create table models_courses ();
#insert into t
class Exam(models.Model):
	name = models.CharField(max_length=30)
 	total_marks = models.IntegerField(default=0)
 	#gained_marks = models.IntegerField(default=0)
 	course = models.ForeignKey(Courses,on_delete=models.CASCADE,null=True)
 	weightage = models.IntegerField(default=0)
 	def __str__(self):
		return self.name


class Student(md.User):

	def __str__(self):
		return self.username

class Faculty(md.User):

	def __str__(self):
		return self.username

class Result(models.Model):
	exam = models.ForeignKey(Exam,on_delete=models.CASCADE,null=True)
	course = models.ForeignKey(Courses,on_delete=models.CASCADE,null=True)
	student = models.ForeignKey(Student,on_delete=models.CASCADE,null=True)
	gained_marks = models.IntegerField(default=0)
	def __str__(self):
		return str(self.course)+' '+str(self.exam)+' '+str(self.student)

class Total_Marks(models.Model):
	course = models.ForeignKey(Courses,on_delete=models.CASCADE,null=True)
	student = models.ForeignKey(Student,on_delete=models.CASCADE,null=True)
	total_marks = models.IntegerField(default=0)
	def __str__(self):
		return str(self.course)+' '+str(self.student)

class global_var(models.Model):
	publish_result = models.BooleanField(default=False)
