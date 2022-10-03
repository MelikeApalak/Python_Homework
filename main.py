def divide_students(studends):
    groups = [[],[]]

    for index,student in enumerate(studends):
        if index % 2 == 0:
            groups[0].append(student)
        else:
            groups[1].append(student)
    return groups

"""students = ["ali","veli","mehmet","fatih"]
divide_students(students)"""


#CIFT INDEX BUYUK TEK INDEX KUCUK HARF YAPIYOR.
def alternating_with_enumerate(string):
    new_string = ""
    for i,letter in enumerate(string):
        if i % 2 == 0:
            new_string += letter.upper()
        else:
            new_string += letter.lower()
    print(new_string)


alternating_with_enumerate("hi my name is melike and i am learning python")




def summer(a,b):
    return a+b

summer(1,3) * 9

new_sum = lambda a,b : a+b
new_sum(4,5)


#map
salaries = [1000,2000,3000,4000,5000]

def new_salary(x):
    return x * 20 / 100 + x

for salary in salaries:
    print(new_salary(salary))

list(map(lambda x:x*20/100+x ,salaries))
# bir fonksiyon ve üstünde gezinebileceği bir liste verdik.