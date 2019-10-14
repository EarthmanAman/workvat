%Original rectangle
rectangle=[1 7 7 1 1; 1 1 4 4 1;1 1 1 1 1];

%x and y of original rectangle
x = rectangle(1,:);
y = rectangle(2,:);

%Let dx = 3, dy = 4. Calculate Translation
T = [1 0 3; 0 1 4; 0 0 1] * rectangle;

%Value of x and y of translated image
x1 = T(1,:);
y2 = T(2,:);

%Plot the 2 rectangles
plot(x,y,x1,y2)

%Grid measurements
axis([0 12 0 10]);

%Figure's title
title('Rectangle and its translate')