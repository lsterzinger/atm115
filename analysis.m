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
room_x = 100;
room_time = 100;

prec = ncread('~/Documents/ATM115-Data/SST310k-selected/sam2d.nc','Prec');
rh  = ncread('~/Desktop/atm115/310K_vars.nc','rh_col_av');
BW = imregionalmax(prec(room_x:end-room_x, room_time:end-room_time),4);

%this finds the row and column indicies where BW is true, that is greater than either 4
%or eight of it's surrounding points
[row, col] = find(BW>0);
ind_cent = [row, col];

%to composite the precipitation events = 0;
prec_tot = 0;
rh_tot = 0;

for i = 1: size(ind_cent,1)
	prec_tot = prec_tot + prec(ind_cent(i,1):ind_cent(i,1)+2*room_x-1, ind_cent(i,2):ind_cent(i,2)+2*room_time-1);
   	rh_tot = rh_tot + rh(ind_cent(i,1):ind_cent(i,1)+2*room_x-1, ind_cent(i,2):ind_cent(i,2)+2*room_time-1);

end

%it also might be useful to smooth the events in x and time

for i = 1:size(prec_tot,1)            %smooth in X
    prec_tot(i,:) = smooth(prec_tot(i,:));
    rh_tot(i,:) = smooth(rh_tot(i,:));
end

for i = 1:size(prec_tot,2)            %smooth in time 
    prec_tot(:,i) = smooth(prec_tot(:,i));
    rh_tot(:,i) = smooth(rh_tot(:,i));
end

prec_av = prec_tot/size(ind_cent,1);
rh_av = rh_tot/size(ind_cent,1);


output = netcdf.create('310K_composite.nc','NOCLOBBER');
x = netcdf.defDim(output, 'x', 200);
time = netcdf.defDim(output, 'time', 200);
prec_tot_out = netcdf.defVar(output, 'prec_tot', 'NC_DOUBLE', [time x]);
prec_av_out = netcdf.defVar(output, 'prec_av', 'NC_DOUBLE', [time x]);
rh_tot_out = netcdf.defVar(output, 'rh_tot', 'NC_DOUBLE', [time x]);
rh_av_out = netcdf.defVar(output, 'rh_av', 'NC_DOUBLE', [time x]);

netcdf.endDef(output)

netcdf.putVar(output, prec_tot_out, prec_tot);
netcdf.putVar(output, prec_av_out, prec_av);


netcdf.putVar(output, prec_tot_out, prec_tot);
netcdf.putVar(output, prec_av_out, prec_av);

netcdf.close(output)


%makes an average
%makes an anomaly
% for i = 1:size(prec_tot,1)
% 	prec_tot(i,:) = prec_tot(i,:) - mean(prec_tot(i,:));
% end