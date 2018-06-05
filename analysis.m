%I've assumed that you've already loaded the data Da gave us and named the precipitation 
%field "prec" and it's dimensions are x and time.

%this just finds points that are >= every surrounding point in prec
%room_x and room_time are the sizes of the window around each precipitation "event"
%in x and in time
%the last argument in imregionalmax can either be 4 or 8
% if 4 it compares the target grid "-" to the 0's
%x0x
%0-0
%x0x
% if 8 it compares the target grid "-" to all surroundings
%000
%0-0
%000

prec = ncread("E:/ATM115 Data/SST300k-selected/sam2d.nc","Prec");
x = ncread("E:/ATM115 Data/SST300k-selected/sam2d.nc","x");
t = ncread("E:/ATM115 Data/SST300k-selected/sam2d.nc","t");

room_x = 100
room_y = 100

BW = imregionalmax(prec(room_x:end-room_x, room_time:end-room_time),4);

%this finds the row and column indicies where BW is true, that is greater than either 4
%or eight of it's surrounding points
[row, col] = find(BW>0);
ind_cent = [row, col];