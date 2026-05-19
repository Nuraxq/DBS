from relational_algebra import Relation, sigma, GreaterThan, Projection,Rename,NaturalJoin, Division,Selection,And,Equals,Difference,Or
import sqlite3

# Load the university database.
#
# Download the file from StudIP and place it in the same directory
# or adjust the path.
con = sqlite3.connect("uni-db.sqlite3")

# Register needed relations
Student = Relation("Student")
tests = Relation("tests")
Professor = Relation("Professor")
requires = Relation("requires")
Course = Relation("Course")
attends = Relation("attends")
Assistant = Relation("Assistant")


"""Exercise 5.1: 
a)
DDL: Create, Alter, Drop
DML: Insert, Delete, Update
b) 
Distinct: Braucht man nicht, da Mengen sowieso keine Duplikate enthalten, Projektion entfernt alle Duplikate
c)
Where vs Having: Having wird nach einer Group by Anweisung verwendet. Es filtert also Gruppen die Eigenschaften erfüllen. 
Where wird genutzt um Zeilen zu filtern. 
d) Null wird in Aggregatfunktionen nicht beachtet, und kann nicht für Joins benutzt werden, es ist absorbierend in allen arithmetischen Operatoren 
Vergleiche mit Null werten werden zu unknown, Tuples werden nur beachtet wenn true zurückgegeben wird, bei boolean Operationen wie z.b. dem und kann der Ausdruck 
dann nur mithilfe des anderen Eingabewerts gewertet werden. Also uknown and false = false bzw unknown or true = true. 


"""

""" Aufgabe 5.2 SQL Queries: 

1. SELECT Name from Professor WHERE Professor.Room = 310 
Ans: Kopernikus


2. SELECT Count() from attends where attends.CouNo = 5001 
Ans: 4 

3. 
SELECT Name from Student,attends where Student.StuNo = attends.StuNo and attends.CouNo = 5001
Ans: Fichte
Schopenhauer
Theophrastos
Feuerbach

4. SELECT Count(),Course.SCH from Course GROUP by Course.SCH 
Ans: 
Count SCH 
4	2 
2	3
4	4


5. Select title from Course where Title not in (SELECT Title from Course, tests where tests.CouNo = Course.CouNo)
Logic
Faith and Knowledge
Epistemology
Maeeutics
Philosophy of Science
Bioethics
The Vienna Circle

6. select avg(anzahl) from (Select p.PerNo, Count(a.perno) as anzahl from professor p left outer join assistant a on p.PerNo = a.Boss group by p.PerNo) 
answer: 0.857142857142857


5.3 
a)
Select DISTINCT Rank from Professor, Assistant where Assistant.Boss = Professor.PerNo
Answer: 
W3
W2

b)
Select name from Professor where name not in (SELECT Professor.Name from Professor,Course where course.TaughtBy = Professor.PerNo)
Answer:
Kopernikus
Curie

c) SELECT a.PerNo, a.Name FROM Assistant a WHERE (a.PerNo, a.Name) IN (SELECT s.StuNo, s.Name FROM Student s);
Leere ausgabe
"""


# d) 
query_1 = Projection(NaturalJoin(Professor,Difference(Projection(Professor,"PerNo"),Rename(Projection(Course,"TaughtBy"),{"TaughtBy":"PerNo"}))),"Name")
print(query_1.evaluate(con).tabulate())
# Kopernikus und Curie

query_2 = Projection(Selection(Assistant,Or(Equals("Assistant.Boss",2125),Equals("Assistant.Boss",2127))),"Name")
print(query_2.evaluate(con).tabulate())
# Answer: Platon Aristoteles Rhetikus Newton

"""Exercise 5.4: 
Joins in SQL: Unterschiede: 
Left/ Right / Full Outer Join: Outer join übernimmt auch die Werte für die es kein Übereinstimmendes Attribut gab. Left von der linken Menge, right von der rechten Menge, full von beiden
Inner/Natural Join: Übernimmt die Werte für die es ein paar gibt.

Select distinct title from Course left join attends on course.CouNo = attends.CouNo where attends.CouNo IS NULL 
Answer: 
The Three Critiques
Epistemology

Select distinct name from Student join attends on Student.StuNo = attends.StuNo left join tests on attends.StuNo = tests.StuNo where tests.StuNo is NULL
Answer: 
Fichte
Theophrastos
Feuerbach

Select Assistant.name from Assistant left join Professor on Assistant.Boss = Professor.PerNo where Professor.PerNo is NULL 
Answer:
Keiner 


SELECT Name,Title from attends JOIN Student on attends.StuNo = student.StuNo join Course on course.CouNo = attends.CouNo 
Answer: 
Fichte	Fundamental Principles
Schopenhauer	Fundamental Principles
Schopenhauer	Logic
Carnap	Ethics
Carnap	Philosophy of Science
Carnap	Bioethics
Carnap	The Vienna Circle
Theophrastos	Fundamental Principles
Theophrastos	Ethics
Theophrastos	Maeeutics
Feuerbach	Faith and Knowledge
Jonas	Faith and Knowledge
Feuerbach	Fundamental Principles
"""