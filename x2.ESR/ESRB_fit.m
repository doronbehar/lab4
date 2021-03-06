%CREATEFIT(I_MODULATION,ABSORPTION_DERIVIATIVE)
%  Create a fit.
%
%  Data for 'lorenzian_deriviative' fit:
%      X Input: I_modulation
%      Y Output: absorption_deriviative
%  Output:
%      fitresult : a fit object representing the fit.
%      gof : structure with goodness-of fit info.
%
%  See also FIT, CFIT, SFIT.

%  Auto-generated by MATLAB on 29-Apr-2022 15:46:31

absorption_deriviative = [0.053125, 0.0625, 0.06875, 0.076875, 0.08437499999999999, 0.078125, 0.09250000000000001, 0.103125, 0.11875, 0.13125, 0.2, 0.2375, 0.31875000000000003, 0.38125, 0.4625, 0.56875, 0.68125, 0.81875, 0.9375, 1.0, 0.99375, 0.8875, 0.696875, 0.4625, 0.20625, -0.11249999999999999, -0.38125, -0.6312500000000001, -0.81875, -0.9687499999999999, -1.0, -0.94375, -0.84375, -0.7125, -0.5875, -0.5, -0.33749999999999997, -0.28125, -0.2375, -0.2, -0.17500000000000002, -0.15, -0.11875, -0.08750000000000001, -0.075, -0.0625];
I_modulation = [0.4250121951219512, 0.42999972899729, 0.4349872628726288, 0.4399747967479675, 0.4449623306233063, 0.449949864498645, 0.4549373983739837, 0.45992493224932246, 0.46491246612466125, 0.46990000000000004, 0.4748875338753388, 0.47987506775067756, 0.4848626016260163, 0.4898501355013551, 0.4948376693766937, 0.4998252032520325, 0.5048127371273713, 0.5098002710027101, 0.5147878048780488, 0.5197753387533876, 0.5247628726287263, 0.529750406504065, 0.5347379403794038, 0.5397254742547425, 0.5447130081300814, 0.5497005420054201, 0.5546880758807587, 0.5596756097560975, 0.5646631436314363, 0.5696506775067751, 0.5746382113821138, 0.5796257452574527, 0.5846132791327913, 0.5896008130081302, 0.5945883468834688, 0.5995758807588075, 0.6045634146341463, 0.6095509485094851, 0.6145384823848239, 0.6195260162601626, 0.6245135501355015, 0.62950108401084, 0.6344886178861789, 0.6394761517615176, 0.6444636856368564, 0.6494512195121951];

%% Fit: 'lorenzian_deriviative'.
[xData, yData] = prepareCurveData( I_modulation, absorption_deriviative );

% Set up fittype and options.
ft = fittype( 'amplitude*(-2*(gamma^2)*(I-I0))/(gamma^2+(I-I0)^2)^2', 'independent', 'I', 'dependent', 'ld' );
opts = fitoptions( 'Method', 'NonlinearLeastSquares' );
opts.Display = 'Off';
opts.StartPoint = [0.655740699156587 0.0357116785741896 0.849129305868777];

% Fit model to data.
[fitresult, gof] = fit( xData, yData, ft, opts );

% Plot fit with data.
figure( 'Name', 'lorenzian_deriviative' );
h = plot( fitresult, xData, yData );
legend( h, 'absorption_deriviative vs. I_modulation', 'lorenzian_deriviative', 'Location', 'NorthEast', 'Interpreter', 'none' );
% Label axes
xlabel( 'I_modulation', 'Interpreter', 'none' );
ylabel( 'absorption_deriviative', 'Interpreter', 'none' );
grid on