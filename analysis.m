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

BW = imregionalmax(prec(room_x:end-room_x, room_time:end-room_time),4);

%this finds the row and column indicies where BW is true, that is greater than either 4
%or eight of it's surrounding points
[row, col] = find(BW>0);
ind_cent = [row, col];

%to composite the precipitation events
aa = 0;
for i = 1: size(ind_cent,1)
	aa = aa + prec(ind_cent(i,1):ind_cent(i,1)+2*room_x-1, ind_cent(i,2):ind_cent(i,2)+2*room_time-1);
end

%it also might be useful to smooth the events in x and time

for i = 1:size(aa,1)            %smooth in X
    aa(i,:) = smooth(aa(i,:));
end

for i = 1:size(aa,2)            %smooth in time 
    aa(:,i) = smooth(aa(:,i));
end

%makes an average
% aa = aa/size(ind_cent,1);

%makes an anomaly
% for i = 1:size(aa,1)
% 	aa(i,:) = aa(i,:) - mean(aa(i,:));
% end