
close all
clear all
clc
    
data = xlsread("samples_102.csv");
data = data(:,2) - data(:,1);

C = data;
data3 = readtable('samples.csv');
data3 = data3(:,1);

V = C(0.075 * size(C, 1) +1 :0.075 * size(C, 1) * 2);

  
    
    
V_window = data(1:31);
 
E = [];
x = [-15,-14,-13,-12,-11,-10,-9,-8,-7,-6,-5,-4,-3,-2,-1,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15];
x = diag(x' * x);
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
V_window = V(window_start:window_end);
a1 = m * sum(diag(x' * V_window)) - sum(x) * sum(V_window);
a2 = m * sum(diag(x' * x)) - (sum(x))^ 2;

a = a1 / a2;

        
v1 = sum(diag(x' * x)) * sum(V_window) - sum(diag(x' * V_window)) * sum(x);
v2 = m * sum(diag(x' * x)) - (sum(x))^ 2;

v = v1 / v2;

V_prime = (a * x) + v;

E_vector = (1 / 31)* diag((V_prime - V_window)' * (V_prime - V_window));
E_l = sum(E_vector);
 
window_start = window_start + 1;
window_end = window_end + 1;

E(l) = E_l;
A_vector(l) = a;     

end
E_thresh = 0.01;
A_thresh = 10^-4;
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
% baseline_average = (1 / size_baseline) * sum(baseline);
% baseline = baseline - baseline_average;
constant_isoelectric_line = zeros(1, size(V, 1));

samples_plot3 = linspace(1,size(baseline, 1),size(baseline, 1));
% [baseline_upper, baseline_lower] = envelope(baseline);

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
    
constant_isoelectric_line(16:(end-15)) = V(16:(end-15)) -  baseline_temporary(:);
% V_restorefilter = ones(1, size(baseline_filter, 1));
% V_restorefilter = V_restorefilter - baseline_filter';
% V_restore = diag(V(16:(end-15)) * V_restorefilter);
% constant_isoelectric_line(16:(end-15)) = constant_isoelectric_line(16:(end-15)) + V_restore';


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
                                                                             
                                                                                
                                                                                 
                                                                                 

    while (counter < size(peaks, 1))

        if (peaks(counter) ~= 0)
            sample(count) = peaks(counter);
            counts_for_peaks(count) = counter;
            counter = counter + 1;
            count = count + 1;    
        else
            counter = counter + 1;
        end
    end

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

output = zeros(number_of_beats,counter_period);
last_output = zeros(1,counter_period);

peak_position1 = 0;
max_peak = max(sample(1:3));
if sample(1) == max_peak
    peak_position1 = counts_for_peaks(1);
end
if sample(2) == max_peak
    peak_position1 = counts_for_peaks(2);
else 
    peak_position1 = counts_for_peaks(3);

end

peak_position1 = round( 0.9 * peak_position1);
constant_isoelectric_line2 = constant_isoelectric_line;
constant_isoelectric_line2(1:end - peak_position1) = constant_isoelectric_line(peak_position1 + 1:end);

for l2 = 1:1:number_of_beats
    if l2 == number_of_beats
        last = constant_isoelectric_line(counter_period * (l2 - 1) + 1: end);
        final = size(last,2);
        last_output(1:final) = last;
        output(l2, :) = last_output;
        
    else
        output(l2, :) = constant_isoelectric_line((counter_period * (l2 - 1) + 1):(counter_period * l2));
    
    end
    
end    




output1 = output(1:end-1, :);
samples_plot1 = linspace(1,size(V', 1),size(V', 1));
samples_plot2 = linspace(1,size(output', 1),size(output', 1));
peaks_overlap = zeros(1, size(V', 1));
peaks_overlap(16:(end-15)) = peaks';
figure
plot(samples_plot1(1,:), V(1,:));
hold on


% 
% plot(samples_plot2(1,:), output1(1,:));
% hold on
% plot(samples_plot2(1,:), output1(2,:));
% hold on
% 
% plot(samples_plot2(1,:), output1(3,:));
% hold on
% 
% plot(samples_plot2(1,:), output1(4,:));
% hold on
% 
% plot(samples_plot2(1,:), output1(5,:));
% hold on
% 
% 
% plot(samples_plot2(1,:), output1(6,:));
% hold on
% % 
% 


hold on

plot(samples_plot1(1,:), E(:,1));


plot(samples_plot1(1,:), peaks_overlap);

% plot(samples_plot3(1,:), baseline_temporary);

hold on
plot(samples_plot1(1,:), constant_isoelectric_line);




