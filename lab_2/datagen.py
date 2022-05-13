

z_min = 0
z_max = 4
z_step = 1

y_min = -1.0
y_max = 1.0
y_step = 0.5

x_min = -1.0
x_max = 1.0
x_step = 0.5


flag = 0

f = open("output.txt", "w")

for z in range(z_min, z_max, z_step):
	f.write("					z=" + str(z) + '\n')
	f.write("y/x")
	for x in range(x_min, x_max, x_step):
		f.write(" " + str(x))
	f.write('\n')

	for y in range(y_min, y_max, y_step):
		f.write(str(y))
		for x int range(x_min, x_max, x_step):

