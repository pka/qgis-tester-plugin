lessons = []

def addLessonsModule(module):
	if "lessons" in dir(module):
		lessons.extend(module.lessons())

def addLessonFolder(path):
	pass