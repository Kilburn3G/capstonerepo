clear all
close all
clc

% I would suggest to not try to understand the nuances of the code, I can
% give a rough idea of the algorithm and say what the variables mean but it 
% will be easier to understand it in person 

size_prev_output = 0;
size_prev_output_neg = 0;
size_prev_output_pos = 0;

% This is the importing of the data. Right now we are operating on
% samples_102.csv. The functions xlsread and readtable can be used interchangeably. 
% data = xlsread("samples_102.csv");
% data =  data(:,2) - data(:,1);%data(:,2);%data(:,2) - % Column indexing to measure the difference between columns 
%                               % 2 and 1
                              
annotations = readtable("annotations.txt");
labels = annotations(:,3).Variables;
labels = cell2mat(labels);

annotations_1 = annotations(:,1);
annotations_2 = annotations(:,2);
annotations_3 = annotations(:,3);  
annotations_4 = zeros(size(annotations(:,3),1),1);  

for i = 1:1:size(labels,1)
    if labels(i) == 'N' || labels(i) == '.' || labels(i) == '/'
        annotations_4(i) = 0;
    else
        annotations_4(i) = 1;
    end
end


% V is our voltage differences between the two leads contained in the
% dataset. Throughout most of the code, V will be indexed by sample number.
% V = data(0.075 * size(data, 1) +1 :0.075 * size(data, 1) * 2);
% num7 = 1;
% for o1 = 1:1:2
% 
% 
% str9 = sprintf("%u",num7);
% str10 = "samples_102_";
% str11 = ".csv";
% str12 = sprintf("%s",[str10,str9,str11]);

%str12
% data = xlsread("samples_212.csv");
% data =  data(:,2) - data(:,1);%data(:,2);%data(:,2) - % Column indexing to measure the difference between columns 
                              % 2 and 1
                              

for y = 1:1:32


num7 = 20000 * (y-1) +3;
num8 = 20000 * y + 2;



str9 = sprintf("%u",num7);
str99 = sprintf("%u",num8);
str10 = "B";
str101 = "C";
str11 = sprintf("%s",[str10,str9,":"]);
str12 = sprintf("%s",[str10,str99]);
str13 = sprintf("%s",[str11,str12]);
str14 = sprintf("%s",[str101,str9, ":"]);
str15 = sprintf("%s",[str101,str99]);
str16 = sprintf("%s",[str14,str15]);

V1 = xlsread("samples_102.csv",str13);
% V2 = xlsread("samples_212.csv",str16);

V =V1;

% V = data(20000 * (y-1) +1:20000 * y);
%V = data(240001:end);
% V = data;
%V = flip(V);

    
% The algorithm operates on a window (segment of samples of constant length) that
% slides over the data set from begining to end. It's not taken in "chunks"
% the starting sample number and ending sample number of the window
% increase by one every iteration. It was recommended that we use 31 points 
% by the article this is based off. 
V_window = V(1:31);

% E is a vector containing a measure of the error between the best fit quadratic to the
% window's center, and window itself. We're trying to quantify how
% "quadratic it is" around the window's centrepoint, which increases to the next sample number each 
% time. NOTE: the values in the vectors E and A each
% correspond to the window they were calculated in, and in the big picture at the window's centerpoint.
% Where the center point is located at a slope in the data, there will be a
% large value in E. Where the data is flat, where will be a very small
% value of A. Where there is a peak, the data will be quadratic and so
% there will be a small value in E and a sizeable value in A.
E = [];

% x is used for the summation in the algorithm
x = [-15,-14,-13,-12,-11,-10,-9,-8,-7,-6,-5,-4,-3,-2,-1,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15];
x = diag(x' * x);

% A contains the values a of the best fit quadratic for every window, a as
% in a * x^2 _ b * x + c
A_vector = [];

window_start = 1;
count = 1;
counter = 1;
counts_for_peaks = [];
sample = [];
window_end = 31;
m = 31;

peaks_threshold = 5 * 10^-4;
    

for l = 1:1:(size(V) - 30)  
    
V_window = V(window_start:window_end); % adjusting the window for the next iteration
% calculation of a 
a1 = m * sum(diag(x' * V_window)) - sum(x) * sum(V_window);
a2 = m * sum(diag(x' * x)) - (sum(x))^ 2;

a = a1 / a2;

% hard to explain, but the quadratic can be thought of as linear with respect to 
% the variable x^2. v is the constant in the quadratic approximation.        
v1 = sum(diag(x' * x)) * sum(V_window) - sum(diag(x' * V_window)) * sum(x);
v2 = m * sum(diag(x' * x)) - (sum(x))^ 2;

v = v1 / v2;

% V_prime is the quadratic approximation of the window
V_prime = (a * x) + v;

% Calculating a value for E
E_vector = (1 / 31)* diag((V_prime - V_window)' * (V_prime - V_window));
E_l = sum(E_vector);
 
window_start = window_start + 1;
window_end = window_end + 1;

% Putting the error and quadratic a values in the vectors for storage of
% this iteration
E(l) = E_l;
A_vector(l) = a;     

end

% Used to decide if E is low enough
E_thresh = 0.01;  %0.01

% Used to decide if A is high enough
A_thresh = 10-4;   %10^-4

A_vector = 0.25 * A_vector;


% Don't worry about any of this code (Up to line 154) The important
% findings are the vector peaks (containing peaks except the negative peak
% on the QRS complex ( a shortcoming of this codeI need to fix) ) and the
% vector peaks_position (containing the sample number of the entries in the
% vector peaks). I also took out the baseline in this code.

A_abs_vector = abs(A_vector);
A_filter = (A_abs_vector * (1 / A_thresh)) - 1;
baseline_filter1 = heaviside(A_filter);
E_filter = (E * (1 / E_thresh)) - 1;
E_filter = heaviside(E_filter);
baseline_filter2 = ones(1, size(E, 1)) - E_filter;
baseline_filter1 = ones(1, size(A_vector, 1)) - baseline_filter1;
baseline_filter = diag(baseline_filter1' * baseline_filter2);
baseline = diag(V(16:(end-15)) * baseline_filter');
size_baseline = sum(baseline_filter);
constant_isoelectric_line = zeros(1, size(V, 1));

constant_isoelectric_line2 = zeros(1, size(V, 1)); %

samples_plot3 = linspace(1,size(baseline, 1),size(baseline, 1));

[y_u, y_l] = envelope(baseline);
base1 = V(samples_plot3) - baseline;

baseline_temporary = samples_plot3;
baseline(1) = baseline(2);
for k = 1:1:size(samples_plot3, 2)
if abs(baseline(k)) < 0.01
    if(k == 1)
      baseline_temporary(k) = 0.1;
    else
       baseline_temporary(k) = baseline_temporary(k-1); 
    end
else
baseline_temporary(k) = baseline(k);

end
end

fit = baseline_temporary;
fit = medfilt1(fit,12);
% for i = 1:1:100
%     baseline_temporary = medfilt1(fit);
% 
% end
% constant_isoelectric_line2(16:(end-15)) = V(16:(end-15)) - y_l(:);%-  baseline_temporary(:)
constant_isoelectric_line(16:(end-15)) = V(16:(end-15)) - baseline_temporary(:);%-  baseline_temporary(:)


A_vector = (A_vector * (1 / peaks_threshold)) - 1;
peaks_filter = heaviside(A_vector); 
region_peaks = diag(peaks_filter' * E);


l_region_peaks = region_peaks;
r_region_peaks = region_peaks;


l_region_peaks(1:(end -1)) = region_peaks(2:end);
l_region_peaks(end) = region_peaks(1);
r_region_peaks(2:end)= region_peaks(1:(end - 1));
r_region_peaks(1) = region_peaks(end);

upper_max = region_peaks - l_region_peaks;
upper_max = heaviside(upper_max);
lower_max = region_peaks - r_region_peaks;                                                                                 
lower_max = heaviside(lower_max);
                                                                               
peaks_position = (upper_max + lower_max) - 1;  
peaks_position = heaviside(peaks_position - 0.1);
peaks = diag(peaks_position * E);
                                                                             
                                                                                
 % sample gives meaningful ( not approximately zero) values for peaks that would be 
 % misidentified as true peaks. Counts_for_peaks contains the index of
 % peaks from which these were extracte. Here we find sample and count's
 % for peaks
                                                                                 
 samples = [];
    while (counter < size(peaks, 1))

        if (peaks(counter) ~= 0)
            sample(count) = peaks(counter);
            samples(counter) = peaks(counter);
            counts_for_peaks(count) = counter;
            counter = counter + 1;
            count = count + 1;    
        else
            counter = counter + 1;
        end
    end

    
% This code (until 197) is no longer used. This is from when we were
% calculating the size of each waveform by taking the average period of the
% waveforms and dividing the code into these pieces from start to end. Now
% we center the waveform at the R peak and always use the same number of
% samples each side, eliminating many samples that don't contain the
% waveform. 

l_counts_for_peaks = counts_for_peaks;
l_counts_for_peaks(1:(end -3)) = counts_for_peaks(4:end);
l_counts_for_peaks((end - 2):end) = counts_for_peaks(1:3);

counter_period = (sum(abs(counts_for_peaks(1:end -3) - l_counts_for_peaks(1:end - 3))) + 3) / (count - 7);

QRS_peak = max(sample(1:3));
P_peak = min(sample(1:3));

number_of_beats = size(V,1) / counter_period;
counter_period = round(counter_period);
V = V';
number_of_beats = ceil(number_of_beats);


last_output = zeros(1,counter_period);


% this code identifies if the pattern of peaks starts at the P peak, the R
% peak, or the T peak.Peak_order_offset tells how much the R peak is offset from the other peaks. I.e.
% if the first peak is the R peak then the offset is 1
peak_position1 = 0;
max_peak = max(sample(1:3));
if sample(1) == max_peak
    peak_position1 = counts_for_peaks(1);
    peak_orderoffset = 1;
end
if sample(2) == max_peak
    peak_position1 = counts_for_peaks(2);
    peak_orderoffset = 2;
end
if sample(3) == max_peak
    peak_position1 = counts_for_peaks(3);
    peak_orderoffset = 3;
end
    
% if sample(4) == max_peak
%     peak_position1 = counts_for_peaks(4);
%     peak_orderoffset = 4;   
% end
% if sample(5) == max_peak 
%     peak_position1 = counts_for_peaks(5);
%     peak_orderoffset = 5;
% end

output = zeros(number_of_beats - 1,161);

forward_cIl = constant_isoelectric_line;
forward_cIl(1:end-1)= constant_isoelectric_line(2:end);
diff = constant_isoelectric_line - forward_cIl;
output2 = zeros(number_of_beats,161);

f = diff;
f(1:end-1) = diff(2:end);
diff2 = f -diff;
output3 = zeros(number_of_beats,161);
%R = zeros(1,floor((size(counts_for_peaks,2) / 3)));
%P = zeros(1,floor((size(counts_for_peaks,2) / 3)));
R = zeros(number_of_beats - 1,1);
P = zeros(number_of_beats - 1,1);
% This is the code that finds output, the vector containing the output
% samples, one in each row, each 161 samples long. Peak_order_offset was used so
% that we could specifically center the R peak, and not the other peaks. 

RR = R';
PP = P';
for l5 = 1:1:(floor(count / 3) - 1)
   output(l5, 81) = sample((l5 - 1) * 3 + peak_orderoffset);
   R(l5) = counts_for_peaks((l5 - 1) * 3 + peak_orderoffset);
   P(l5) = counts_for_peaks((l5 - 1) * 3 + 1);
   if l5 > 1
       RR(l5) = R(l5) - R(l5 - 1);
       PP(l5) = P(l5) - P(l5 - 1);
   end
   
   if (counts_for_peaks(3 * (l5 - 1) + peak_orderoffset)) < 81
       output(l5, 82:161) = constant_isoelectric_line(counts_for_peaks(3 * (l5 - 1) + peak_orderoffset) + 1: counts_for_peaks(3 * (l5 - 1) + peak_orderoffset) + 80);
   elseif (counts_for_peaks(3 * (l5 - 1) + peak_orderoffset)) > size(constant_isoelectric_line,2) - 81
       output(l5, 1:80) = constant_isoelectric_line( counts_for_peaks(3 * (l5 - 1) + peak_orderoffset) - 80:counts_for_peaks(3 * (l5 - 1) + peak_orderoffset) - 1);
   else
       output(l5, 1:80) = constant_isoelectric_line( counts_for_peaks(3 * (l5 - 1) + peak_orderoffset) - 80:counts_for_peaks(3 * (l5 - 1) + peak_orderoffset) - 1);
       output(l5, 82:161) = constant_isoelectric_line(counts_for_peaks(3 * (l5 - 1) + peak_orderoffset) + 1: counts_for_peaks(3 * (l5 - 1) + peak_orderoffset) + 80);     
   end
   
   
end
RR(1) = RR(2);
PP(1) = PP(2);

% for l6 = 1:1:((count - 1) / 3)
%    output2(l6, 81) = sample((l6 - 1) * 3 + peak_orderoffset);
%    output2(l6, 50:80) = diff( counts_for_peaks(3 * (l6 - 1) + peak_orderoffset) - 31:counts_for_peaks(3 * (l6 - 1) + peak_orderoffset) - 1);
%    output2(l6, 82:112) = diff(counts_for_peaks(3 * (l6 - 1) + peak_orderoffset) + 1: counts_for_peaks(3 * (l6 - 1) + peak_orderoffset) + 31);     
%     
%     
% end
% 
% for l7 = 1:1:((count - 1) / 3)
%    output3(l7, 81) = sample((l7 - 1) * 3 + peak_orderoffset);
%    output3(l7, 50:80) = diff( counts_for_peaks(3 * (l7 - 1) + peak_orderoffset) - 31:counts_for_peaks(3 * (l7 - 1) + peak_orderoffset) - 1);
%    output3(l7, 82:112) = diff(counts_for_peaks(3 * (l7 - 1) + peak_orderoffset) + 1: counts_for_peaks(3 * (l7 - 1) + peak_orderoffset) + 31);     
%     
%     
% end
samples_plot1 = linspace(1,size(E, 1),size(E, 1)); % x values for plotting E
samples_plot4 = linspace(1,size(V, 1), size(V, 1)); % x values for plotting V
samples_plot2 = linspace(1,size(output', 1),size(output', 1)); % x values for plotting output
figure
maximum_peaks = zeros(size(output,1),8);
maximum_peaks_positions = zeros(size(output,1),8);
maximums1 = zeros(size(output,1),160);
max_count = zeros(size(output,1),1);
output_slice = zeros(1,161);
energy = 0;
energies = zeros(size(output,1),161);
difference = 0;
differences = zeros(size(output,1), 160);

for j = 1:1:size(output,1)
d = 1;
for i = 1:1:161
    
    output_slice = 10 * output(j, 1:i);
    energy = sum(output_slice .* output_slice);
    energies(j,i) = energy;
    if i ~= 1
        difference = energy - energies(j,i-1);
        differences(j,i) = difference;
        if (differences(j,i) < differences(j,i-1))  && (differences(j,i-1) > differences (j,i-2)) && (differences(j,i-1) > 0.05) % change here, 0.3
        maximums1(j,i-1) = 1;
        maximum_peaks(j,d) = output(j,i-1);
        maximum_peaks_positions(j,d) = i-1;
        d = d + 1;
        max_count(j) = max_count(j) + 1;
        elseif (differences(j,i) == differences(j,i-1)) && i<160 && differences(j,i+1)<differences(j,i) && (differences(j,i-1) > differences(j,i-2)) && (differences(j,i-1) > 0.05) % change here, 0.3
        maximums1(j,i-1) = 1;
        maximum_peaks(j,d) = output(j,i-1);
        maximum_peaks_positions(j,d) = i-1;
        d = d + 1;
        max_count(j) = max_count(j) + 1;
        end
    end
    

end
end
maximum_peaks_positions1 = maximum_peaks_positions;

max_peaks = maximum_peaks;
peak = zeros(size(output,1), 4);
maximums = zeros(size(output,1),160);
maximum_peaks_1 = zeros(size(output,1), 4);
for k1 = 1:1:size(output(:,1))
for k2 = 1:1:3
[M, I] = max(maximum_peaks(k1,:));
if M ~= 0
peak(k1,k2 + 1) = maximum_peaks_positions(k1,I);  
maximums(k1,peak(k1,k2 + 1)) = 1;
maximum_peaks_1(k1,k2 + 1) = max_peaks(k1,I);
maximum_peaks(k1,I) = 0;
end
end
[M, I] = min(maximum_peaks(k1,:));
if M ~= 0
peak(k1,1) = maximum_peaks_positions(k1,I); 
maximums(k1,peak(k1,1)) = 1;
maximum_peaks_1(k1,1) = max_peaks(k1,I);
maximum_peaks(k1,I) = 0;
end
end

widths_plot = zeros(size(output,1),160);
widths = zeros(size(output(:,1),1), 4);
widths_upper = zeros(size(output(:,1),1), 4);
widths_lower = zeros(size(output(:,1),1), 4);
for k1 = 1:1:size(output(:,1))
for k2 = 1:1:4
    i2 = 1;
    i3 = 1;
    i1 = peak(k1,k2);
    if i1 ~= 0
    if output(k1,i1) < 0
        
        if i1 - i2 ~= 0
        while output(k1,i1 - i2) < 0
            if i1 - i2 == 1
                break
            else
            i2 = i2 + 1;
            end
        end
        widths_lower(k1,k2) = i1-i2;
        widths_plot(k1,i1  -i2) = 1;
        else
        widths_lower(k1,k2) = 1;
        end
        if i1 + i3 ~= 162
        while output(k1,i1 + i3) < 0
            if i1 + i3 == 161
                break
            else
            i3 = i3 + 1;
            end
        end
        widths_upper(k1,k2) = i1+i3;
        widths_plot(k1,i1 +i3) = 1;
        else
        widths_upper(k1,k2) = 161;
        end
    else
        if i1 - i2 ~= 0
        while output(k1,i1 - i2) > 0
            if i1 - i2 == 1
                break
            else
            i2 = i2 + 1;
            end
        end
        widths_lower(k1,k2) = i1-i2;
        widths_plot(k1,i1  -i2) = 1;
        else
        widths_lower(k1,k2) = 1;
        end
        if i1 + i3 ~= 162
        while output(k1,i1 + i3) > 0
            if i1 + i3 == 161
                break
            else
            i3 = i3 + 1;    
            end
        end
        widths_upper(k1,k2) = i1+i3;
        widths_plot(k1,i1 +i3) = 1;
        else
        widths_upper(k1,k2) = 161;
        end
    end
    %widths(k1,k2) = i3 + i2;
    %widths_upper(k1,k2) = i1+i3;
    %widths_lower(k1,k2) = i1-i2;
    %widths_plot(k1,i1 +i3) = 1;
    %widths_plot(k1,i1  -i2) = 1;
    end
    
end
end







% for i=3:160
%     if (differences(i) < differences(i-1))  && (differences(i-1) > differences (i-2)) && (differences(i-1) > 0.007)
%         maximums(i-1) = 1;
%         max_count = max_count + 1;
%     elseif (differences(i) == differences(i-1)) && i<160 && differences(i+1)<differences(i) && (differences(i-1) > differences (i-2)) && (differences(i-1) > 0.007)
%         maximums(i-1) = 1;
%         max_count = max_count + 1;
%     end
% end
% plot(samples_plot2(1,:), output(28,:));
% hold on
% plot(samples_plot2(1,:), output(1,:));
% hold on
% plot(samples_plot2(1,:), output(60,:));
% hold on



% plot(samples_plot1(1,:), E(1,:));
% hold on
% plot(samples_plot4(1,:), V(1,:));
% hold on


% 



% Summary: Important vectors:

% E - error in each window 
% A - quadratic "a" value in each window 
% E_thresh - used to filter values of E to be considered in the code (to extract the lower ones)
% A_thresh - used to filter values of A to be considered for finding peaks
% (not low) and for finding areas where the signal is at the baseline (low)

% V - values of the input signal potential difference


% If you have any questions let me know
% - aydan 

% [maximum_peaks_1] [peak] [RR] [PP] [RR / PP] [widths_lower] [widths_upper]
num5 = size_prev_output + 1;
num6 = size_prev_output + size(output,1);
outputs = zeros(size(output,1), 20);
outputs(:,1:4) = maximum_peaks_1;
outputs(:,5:8) = peak * (250 / 350);
outputs(:,9) = RR * (250 / 350);
outputs(:,10) = PP * (250 / 350);
outputs(:,11) = RR ./ PP;
outputs(:,12:15) = (widths_upper - widths_lower) * (250 / 350);
% outputs(:,16:19) = widths_upper * (250 / 350);
outputs(1:size(outputs,1),16) = annotations_4(num5:num6);

outputss = [];
ss1 = 1;
ss2 = 1;


for l3 = 1:1:size(outputs,1)
   if sum(output(l3,1:80)) ~= 0 && sum(output(l3,82:161)) ~= 0
       outputss(ss1,:) = outputs(ss2,:);
       ss1 = ss1 + 1;
   end
   ss2 = ss2 + 1;
end

outputs = outputss;

p1 = 1;
p2 = 1;

%insert correction for case 1
outputs_negative = [];
outputs_positive = [];
for l = 1:1:size(outputs,1)
if outputs(l,16) == 0
    outputs_negative(p1,:) = outputs(l,:);
    p1 = p1 + 1;
else
    outputs_positive(p2,:) = outputs(l,:);
    p2 = p2 + 1;
end
end





str1 = "A";
str2 = "T";
%num1 = size_prev_output + 1;
%num2 = size_prev_output + size(output,1);

num1 = size_prev_output_neg + 1;
num2 = size_prev_output_neg + size(outputs_negative,1);
num3 = size_prev_output_pos + 1;
num4 = size_prev_output_pos + size(outputs_positive,1);

str3 = sprintf("%u",num1);
str4 = sprintf( "%u",num2);
str6 = sprintf("%u",num3);
str7 = sprintf( "%u",num4);
str5 = sprintf("%s",[str1, str3,":" str2, str4]);
str8 = sprintf("%s",[str1, str6,":" str2, str7]);

if size(outputs_negative,1) ~= 0
xlswrite("Negative_samples_102_1.xlsx", outputs_negative,str5 );
end
if size(outputs_positive,1) ~= 0
xlswrite("Positive_samples_102_1.xlsx", outputs_positive,str8 );
end
size_prev_output = size_prev_output + size(outputs,1);
size_prev_output_neg = size_prev_output_neg + size(outputs_negative,1);
size_prev_output_pos = size_prev_output_pos + size(outputs_positive,1);



end
% figure
% plot(output(2,:))
% hold on
% yplot = 0.45*maximums(2,:);
% yplot(yplot==0) =nan;
% stem(yplot)
% y2plot = 0.3*widths_plot(2,:);
% y2plot(y2plot==0) = nan;
% stem(y2plot)
