% MO
offset = 5; %%
impulseRate = 200; % counts/sec
angle = 3.2; 
figure
A=[895,2211,415,986,964,895,831];
B=[2293.2, 17374,4507,4931,8624,8047,7478.2];

plot(A,B,'.')
figure
%E_g_MO = findpeaks(Impulses_MO);
plot(energy_MO, Impulses_MO)
title("Mo")
legend()
peak_MO = [895,2211];
energies_MO = [2293.2, 17374 ];

figure
E_g_Ti = findpeaks(Impulses_MO, 'MinPeakHeight',15);
plot(energy_ti, Impulses_ti);
legend()
title("Ti")
peak_Ti = [415,986];
energies_Ti = [4507,4931];

figure
E_g_Zn = findpeaks(Impulses_ZN);
plot(energy_ZN, Impulses_ZN);
title("Zn")
peak_Zn = [964];
energies_Zn = [8624];

figure
E_g_Cu = findpeaks(Impulses_Cu);
plot(energy_Cu, Impulses_Cu);
title("Cu")
peak_Cu = [895];
energies_Cu = [8047];

figure
plot(energy_Ni, Impulses_Ni);
title("Ni")
peak_Ni= [831];
energies_Ni = [7478.2];
%--------------------------
figure
hold on
plot(peak_MO,energies_MO,'o');
plot(peak_Ti,energies_Ti,'o');
plot(peak_Zn,energies_Zn,'o');
plot(peak_Cu,energies_Cu,'o');
plot(peak_Ni,energies_Ni,'o');
legend('MO','Ti','Zn','Cu','Ni')
%10 Descloizit - PbZn(OH)VO_4

figure
plot(energy_Unknown, Impulses_unknown);
title("Unknown")
peak_unknown= [895]; 

figure
E_g_coin = findpeaks(Impulses_coin);
plot(energy_coin, Impulses_coin);
title("coin")
peak_coin = [895];
