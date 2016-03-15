# ka-infection-challenge

needs networkx and matplotlib

to run use

python infection.py input_path

inputs are of the following format - 

user a b : adds a user with id a and name b to graph

edge a b : adds a relation that a is the coach of b

total a : begins a total infection with user a as the start of the infection

limited b : begins a limited infection where b is an integer representing the number of users desired to infect