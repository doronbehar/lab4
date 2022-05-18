thickness_d = 1*10^-9
length_l = 20*10^(-9)
width_w = 10*10^(-9)

%%% {{{ PART 0 - measurement of R_0
nt_part0_I = (linspace(-30,30,13))';
nt_part0_U_p = [
	% {{{ data
	-1.264
	-1.063
	-0.8595
	-0.653
	-0.479
	-0.2572
	0
	0.1748
	0.3714
	0.5913
	0.7218
	0.9548
	1.1202
	% }}}
];

part0_fig = figure;
hold on;
% Generated code
clear xData yData;
[xData, yData] = prepareCurveData( nt_part0_I, nt_part0_U_p );
ft = fittype( 'poly1' );
opts = fitoptions( 'Method', 'LinearLeastSquares' );
opts.Lower = [-Inf 0];
opts.Upper = [Inf 0];
[fitresult, gof] = fit( xData, yData, ft, opts );
nt_part0_fitresult = fitresult
nt_part0_gof = gof
clear xData yData;

plot(nt_part0_I, nt_part0_U_p, 'o')
nt_part0_U_p_err = ones(1,length(nt_part0_U_p)).*0.005;
nt_part0_I_err = ones(1,length(nt_part0_I)).*0.5;
errorbar(nt_part0_I, nt_part0_U_p, nt_part0_U_p_err, nt_part0_U_p_err, nt_part0_I_err, nt_part0_I_err, '.');
plot(nt_part0_I, ...
	polyval([nt_part0_fitresult.p1, nt_part0_fitresult.p2], nt_part0_I))
legend( ...
	'Measurements', ...
	'Errors', ...
	'fit - $U_p = R_0 I$', ...
	'Location', 'North', 'Interpreter', 'Latex' );
xlabel('$I [mA]$', 'Interpreter', 'Latex' );
ylabel('$U_p [mV]$', 'Interpreter', 'Latex' );
print('part0 - R_0.png', '-dpng')
close(part0_fig)

nt_R_0 = abs(nt_part0_fitresult.p1*(10^3))
% First referenced in part 1
nt_sigma_0 = (1.6*10^6)/nt_R_0

%%% }}}

%%% {{{ PART 1 - Measurement of R_h - I_p changing, B constant

nt_part1_magnetic_field = 214; % [mT]
nt_part1_I = (linspace(-30,30,13))';
nt_part1_U_h = [
	% {{{ data
	43.95
	36.56
	29.52
	22.53
	15.27
	8.63 
	0.263
	-7.59  
	-14.14 
	-20.97 
	-28.03 
	-34.32 
	-42.24 
	% }}}
] - 0.7256; % The shift of U_h due to hall voltage compensation

part1_fig = figure;
hold on;
% Generated code
clear xData yData;
[xData, yData] = prepareCurveData( nt_part1_I, nt_part1_U_h );
ft = fittype( 'poly1' );
opts = fitoptions( 'Method', 'LinearLeastSquares' );
opts.Lower = [-Inf 0];
opts.Upper = [Inf 0];
[fitresult, gof] = fit( xData, yData, ft, opts );
nt_part1_fitresult = fitresult
nt_part1_gof = gof
clear xData yData;

nt_part1_R_h = nt_part1_fitresult.p1/nt_part1_magnetic_field
% concentration of charges in matter, according to n = (R_h * q)^-1 with q as
% the electron charge in columbs
nt_number_of_charges = (nt_part1_R_h * 1.602*10^(-19))^(-1)
nt_part1_mu = nt_part1_R_h * nt_sigma_0

plot(nt_part1_I, nt_part1_U_h, 'o')
nt_part1_U_h_err = ones(1,length(nt_part1_U_h)).*0.005;
nt_part1_I_err = ones(1,length(nt_part1_I)).*0.5;
errorbar(nt_part1_I, nt_part1_U_h, nt_part1_U_h_err, nt_part1_U_h_err, nt_part1_I_err, nt_part1_I_err, '.');
plot(nt_part1_I, polyval([nt_part1_fitresult.p1, nt_part1_fitresult.p2], nt_part1_I))
legend( ...
	'Measurements', ...
	'Error', ...
	'fit - $U_h = \frac{R_H\cdot B}{d} I$', ...
	'Location', 'North', 'Interpreter', 'Latex' ...
);
xlabel('$I [mA]$', 'Interpreter', 'Latex' );
ylabel('$U_h [mV]$', 'Interpreter', 'Latex' );
print('part1 - R_h.png', '-dpng')
close(part1_fig)


%%% }}}

%%% {{{ PART 2 - measurement of R_H - B changing, I_p constant

nt_part2_const_current = 30; % [mA]
nt_part2_U_h_vs_teslameter = [
	% {{{ data
	-3.03    22.2
	-6.07    38.3
	-10.45   60.9
	-14.12   79.9
	-18.8    101.1
	-21.75   129.8
	-25.5    141.2
	-28.42   159.7
	-31.81   181
	-35.36   203
	% }}}
];
nt_part2_teslameter = nt_part2_U_h_vs_teslameter(:, 2);
nt_part2_U_h = nt_part2_U_h_vs_teslameter(:, 1);

part2_fig = figure;
hold on;
% Generated code
clear xData yData;
[xData, yData] = prepareCurveData( nt_part2_teslameter, nt_part2_U_h );
ft = fittype( 'poly1' );
opts = fitoptions( 'Method', 'LinearLeastSquares' );
opts.Lower = [-Inf 0];
opts.Upper = [Inf 0];
[fitresult, gof] = fit( xData, yData, ft, opts );
nt_part2_fitresult = fitresult
nt_part2_gof = gof
clear xData yData;

nt_part2_R_h = nt_part2_fitresult.p1/nt_part2_const_current

nt_part2_U_h_err = ones(1,length(nt_part2_U_h)).*0.005;
nt_part2_teslameter_err = ones(1,length(nt_part2_teslameter)).*0.5;
errorbar(nt_part2_teslameter, nt_part2_U_h, nt_part2_U_h_err, nt_part2_U_h_err, nt_part2_teslameter_err, nt_part2_teslameter_err, '.');
plot(nt_part2_teslameter, nt_part2_U_h, 'o')
plot(linspace(-10, 230, 10000), ...
	polyval([nt_part2_fitresult.p1, nt_part2_fitresult.p2], linspace(-10, 230, 10000)))
legend( ...
	'Measurements', ...
	'Error', ...
	'fit - $U_h = \frac{R_H\cdot B}{d} I$', ...
	'Location', 'East', 'Interpreter', 'Latex' ...
);
xlabel('$B [mT]$', 'Interpreter', 'Latex' );
ylabel('$U_h [mV]$', 'Interpreter', 'Latex' );
print('part2 - R_h.png', '-dpng')
close(part2_fig)

% concentration of charges in matter, according to n = (R_h * q)^-1 with q as
% the electron charge in columbs
nt_number_of_charges = (nt_part2_R_h * 1.602*10^(-19))^(-1)
nt_part2_mu = nt_part2_R_h * nt_sigma_0

%%% }}}

%%% {{{ PART 3 - different U_p as a a function of B

nt_part3_B_vs_U_p = [
	% {{{ data
	230 1.1501
	225 1.1494
	220 1.1485
	215 1.1479
	210 1.1474
	205 1.1469
	200 1.1464
	195 1.1459
	190 1.1455
	185 1.1449
	180 1.1446
	175 1.1439
	170 1.1436
	165 1.1431
	160 1.1427
	155 1.1423
	149 1.1418
	145.5 1.1412
	139 1.1407
	135 1.1406
	130.5 1.1400
	125 1.1396
	120 1.1391
	115 1.1388
	109.5 1.1384
	105 1.1381
	100 1.1378
	95.5 1.1375
	88.5  1.1371
	85 1.1369
	80  1.1367
	74.5 1.1364
	70.5  1.1362
	65  1.1359
	60.5 1.1357
	55 1.1354
	49.5 1.1352
	46  1.1351
	41  1.1349
	35  1.1348
	30  1.1347
	25  1.1347
	20  1.1347
	% }}}
];
nt_part3_U_p = nt_part3_B_vs_U_p(:, 2);
nt_part3_B = nt_part3_B_vs_U_p(:, 1);

% Generated code
ft = fittype( 'poly2' );
[xData, yData] = prepareCurveData( nt_part3_B, nt_part3_U_p );
[nt_part3_fitresult, nt_part3_gof] = fit( xData, yData, ft );

part3_fig = figure;
hold on;
plot(nt_part3_B, nt_part3_U_p, 'o')
nt_part3_U_p_err = ones(1,length(nt_part3_U_p)).*0.002;
nt_part3_B_err = ones(1,length(nt_part3_B)).*0.5;
errorbar(nt_part3_B, nt_part3_U_p, nt_part3_U_p_err, nt_part3_U_p_err, nt_part3_B_err, nt_part3_B_err, '.');
plot(linspace(-50, 350, 1000), ...
	polyval([nt_part3_fitresult.p1 nt_part3_fitresult.p2 nt_part3_fitresult.p3], linspace(-50, 350, 1000)))
legend( ...
	'Measurements', ...
	'Errors', ...
	'fit - $U_p(B) = a_1 + a_2 \cdot B^2$', ...
	'Location', 'NorthWest', 'Interpreter', 'Latex' );
xlabel('$B [mT]$', 'Interpreter', 'Latex' );
ylabel('$U_p [mV]$', 'Interpreter', 'Latex' );
print("part3 - B-squared relation.png", "-dpng")
close(part3_fig)

%%% }}}

%%% {{{ PART 4 - Measurement of Energy Gap - no magnetic field

nt_part4_U_p = [
	%%% {{{ data
	0.3913
	0.4041
	0.4204
	0.4429
	0.46
	0.4828
	0.5022
	0.529
	0.5535
	0.5815
	0.6143
	0.7564
	0.927
	1.1096
	1.2278
	1.3015
	1.312
	1.284
	1.237
	1.1817
	0.844
	1.0809
	1.1735
	1.2799
	1.3134
	1.3016
	1.2642
	1.21
	% }}}
];
nt_part4_tempratures = [
	%%% {{{ data
	140
	138
	136
	134
	132
	130
	128
	126
	124
	122
	120
	110
	100
	90
	80
	70
	60
	50
	40
	30
	105
	95
	85
	75
	65
	55
	45
	35
	% }}}
];
nt_part4_const_current = 30;


nt_part4_x_data = (nt_part4_tempratures + 273.15).^(-1);
nt_part4_y_data = -log(nt_part4_U_p);

% Generated code
clear xData yData;
[xData, yData] = prepareCurveData( nt_part4_x_data, nt_part4_y_data );
ft = fittype( 'poly1' );
excludedPoints = excludedata( xData, yData, 'Indices', [14 15 16 17 18 19 20 23 24 25 26 27 28] );
nt_part4_opts = fitoptions( 'Method', 'LinearLeastSquares' );
nt_part4_opts.Exclude = excludedPoints;
[fitresult, gof] = fit( xData, yData, ft, nt_part4_opts );
nt_part4_fitresult = fitresult
nt_part4_gof = gof
clear xData yData;

nt_part4_energy_gap = nt_part4_fitresult.p1 * 2 * 8.625*10^-5

part4_fig = figure;
hold on;
plot(nt_part4_x_data, nt_part4_y_data, 'o')
nt_part4_U_p_err = 0.005.*nt_part4_U_p.^(-1);
nt_part4_tempratures_err = .5.*(nt_part4_tempratures + 273.15).^(-2);
errorbar(nt_part4_x_data, nt_part4_y_data, ...
	nt_part4_U_p_err, nt_part4_U_p_err, ...
	nt_part4_tempratures_err, nt_part4_tempratures_err, '.');

nt_part4_fit_x_data = nt_part4_x_data(not(nt_part4_opts.Exclude));
plot(nt_part4_fit_x_data, ...
	polyval([nt_part4_fitresult.p1 nt_part4_fitresult.p2], nt_part4_fit_x_data), ...
	'LineWidth', 2 ...
)
legend( ...
	'Measurements', ...
	'Errors', ...
	'fit: $\sigma \sim exp\left(-\frac{E_g}{2 K_B T}\right)$, $R^2 = 0.999$', ...
	'Location', 'NorthEast', 'Interpreter', 'Latex' ...
)
xlabel( '$T^{-1} [C^{-1}]$', 'Interpreter', 'Latex' );
ylabel( '$Log(\sigma)$', 'Interpreter', 'Latex' );
print('part4 - E_g.png', '-dpng')
close(part4_fig)

%%% }}}

%%% {{{ PART 5 - Measurement of Energy Gap - with magnetic field

nt_part5_U_p_and_U_h_vs_tempratures = [
	% {{{ data
	0.4430	-4.410	140
	0.4503	-4.610	138
	0.4700	-5.040	136
	0.4952	-5.310	134
	0.5158	-5.790	132
	0.5337	-6.270	130
	0.5633	-6.660	128
	0.5973	-7.140	126
	0.6280	-7.720	124
	0.6500	-8.200	122
	0.6802	-8.890	120
	0.7577	-10.56	115
	0.8319	-12.43	110
	0.9101	-14.76	105
	1.0009	-17.81	100
	1.0898	-20.84	95
	1.1678	-24.18	90
	1.2143	-27.30	85
	1.2664	-29.82	80
	1.3014	-32.04	75
	1.3147	-34.01	70
	1.3186	-35.25	65
	1.3134	-36.18	60
	1.3004	-36.90	55
	1.2803	-37.23	50
	1.2403	-37.39	45
	1.2300	-37.43	40
	1.2099	-37.38	35
	1.1807	-37.28	30
	% }}}
];
nt_part5_U_p = nt_part5_U_p_and_U_h_vs_tempratures(:, 1);
nt_part5_U_h = nt_part5_U_p_and_U_h_vs_tempratures(:, 2);
nt_part5_tempratures = nt_part5_U_p_and_U_h_vs_tempratures(:, 3);

nt_part5_x_data = (nt_part5_tempratures + 273.15).^(-1);
nt_part5_y_data = -log(nt_part5_U_p);
% nt_part5_y_data = -log(abs(nt_part5_U_h));

ft = fittype( 'poly1' );
[xData, yData] = prepareCurveData( nt_part5_x_data, nt_part5_y_data );
% excludedPoints = excludedata( xData, yData, 'Indices', [17 18 19 20 21 22 23 24 25 26 27 28 29] );
excludedPoints = excludedata( xData, yData, 'Indices', [16 17 18 19 20 21 22 23 24 25 26 27 28 29] );
nt_part5_opts = fitoptions( 'Method', 'LinearLeastSquares' );
nt_part5_opts.Exclude = excludedPoints;
[nt_part5_fitresult, nt_part5_gof] = fit( xData, yData, ft, nt_part5_opts );

nt_part5_energy_gap = nt_part5_fitresult.p1 * 2 * 8.625*10^-5

part5_fig = figure;
hold on;
plot(nt_part5_x_data, nt_part5_y_data, 'o')
nt_part5_U_p_err = 0.05.*nt_part5_U_p.^(-1);
nt_part5_tempratures_err = .5.*(nt_part5_tempratures + 273.15).^(-2);
errorbar(nt_part5_x_data, nt_part5_y_data, ...
	nt_part5_U_p_err, nt_part5_U_p_err, ...
	nt_part5_tempratures_err, nt_part5_tempratures_err, '.');
nt_part5_fit_x_data = nt_part5_x_data(not(nt_part5_opts.Exclude));
plot(nt_part5_fit_x_data, ...
	polyval([nt_part5_fitresult.p1 nt_part5_fitresult.p2], nt_part5_fit_x_data), ...
	'LineWidth', 2 ...
)
legend( ...
	'Measurements', ...
	'Errors', ...
	'fit: $\sigma \sim exp\left(-\frac{E_g}{2 K_B T}\right)$, $R^2 = 0.994$', ...
	'Location', 'NorthEast', 'Interpreter', 'Latex' ...
)
xlabel( '$T^{-1} [C^{-1}]$', 'Interpreter', 'Latex' );
ylabel( '$Log(\sigma)$', 'Interpreter', 'Latex' );
print("part5 - E_g with magnetic field.png", "-dpng")
bla
close(part5_fig)

%%% }}}

% vim:foldmethod=marker
