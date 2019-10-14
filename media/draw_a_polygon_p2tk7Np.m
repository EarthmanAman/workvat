%Drawing a Polygon.

%Define the number of sides you want.
sides = 8;
all = 2*sides;

angle = (1/all:1/sides:1)'*2*pi;

x = sin(angle);

y = cos(angle);
fill(x,y,'r')

axis square