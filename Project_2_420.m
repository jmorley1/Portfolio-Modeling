%% Loading historical data:
% Daily Adjusted Close

%Group A:
VFINX = 'VFINX_03_17_P2.csv';
VFINX = csvread(VFINX,1,5,[1,5,3777,5]);
VBTIX = 'VBTIX_03_17_P2.csv';
VBTIX = csvread(VBTIX,1,5,[1,5,3777,5]);
VGSLX = 'VGSLX_03_17_P2.csv';
VGSLX = csvread(VGSLX,1,5,[1,5,3777,5]);
%Group B:
VWIGX = 'VWIGX_03_17_P2.csv';
VWIGX = csvread(VWIGX,1,5,[1,5,3777,5]);
VFICX = 'VFICX_03_17_P2.csv';
VFICX = csvread(VFICX,1,5,[1,5,3777,5]);
VFSTX = 'VFSTX_03_17_P2.csv';
VFSTX = csvread(VFSTX,1,5,[1,5,3777,5]);
%Group C:
INTC = 'INTC_03_17_P2.csv';
INTC = csvread(INTC,1,5,[1,5,3777,5]);
JPM  = 'JPM_03_17_P2.csv';
JPM = csvread(JPM,1,5,[1,5,3777,5]);
GE   = 'GE_03_17_P2.csv';
GE = csvread(GE,1,5,[1,5,3777,5]);

group_A = {VFINX,VBTIX,VGSLX};
group_AB = {VFINX,VBTIX,VGSLX,VWIGX,VFICX,VFSTX};
group_ABC = {VFINX,VBTIX,VGSLX,VWIGX,VFICX,VFSTX, INTC, JPM,GE};
groups  = {group_A, group_AB, group_ABC};

% Trading day year indices:
% Last day of 2012: 
% 2003: 2    - 253
% 2004: 254    - 505
% 2005: 506    - 757
% 2006: 758    - 1008
% 2007: 1009    - 1259
% 2008: 1260    - 1512
% 2009: 1513    - 1764
% 2010: 1765    - 2016
% 2011: 2017    - 2268
% 2012: 2692    - 2518
% 2013: 2519    - 2770
% 2014: 2771  - 3022
% 2015: 3023  - 3274
% 2016: 3275  - 3526
% 2017: 3527 - 3777
trading_day_indices = [1 253; 253 505; 505 757; 757 1008; 1008 1259; ...
                       1259 1512; 1512 1764; 1764 2016; 2016 2268; 2268 2518;...
                       2518 2770; 2770 3022; 3022 3274; 3274 3526; 3526 3777];

%trading days per year
d_2003 = 1:1:252; d_2004 = 1:1:252; d_2005 = 1:1:252;
d_2006 = 1:1:251; d_2007 = 1:1:251; d_2008 = 1:1:253;
d_2009 = 1:1:252; d_2010 = 1:1:252; d_2011 = 1:1:252;
d_2012 = 1:1:250; d_2013 = 1:1:252; d_2014 = 1:1:252;
d_2015 = 1:1:252; d_2016 = 1:1:252; d_2017 = 1:1:251;

years = {d_2003,d_2004,d_2005,d_2006,d_2007, ...
         d_2008,d_2009,d_2010,d_2011,d_2012,...
         d_2013,d_2014,d_2015,d_2016,d_2017};

     
%%  Means, Covariances, & Min Risk Portfolio Allocations
return_history_cell = cell(15,3);
return_mean_cell    = cell(15,3);
return_cov_cell     = cell(15,3);
return_mean_min_cell= cell(15,3);
return_mean_max_cell= cell(15,3);

for i=1:1:length(groups) % 1-3
   group_cell = cell2mat(groups{i}); %group (A,B, or C)
    for j=1:1:length(years)  %1-15
       asset_return_history = ones(length(groups{i}),length(years{j}));
       asset_mean_returns = ones(length(groups{i}),1); 
       for k=1:1:length(groups{i})     
           asset_return_history(k,:) = return_history(group_cell(:,k),trading_day_indices(j,:));
           asset_mean_returns(k)   = mean(asset_return_history(k,:));        
       end
    return_history_cell(j,i)  =  num2cell(asset_return_history,[1 2]);
    return_mean_cell(j,i)     =  num2cell(asset_mean_returns, [1 2]);
    return_cov_cell(j,i)      =  num2cell(cov(asset_return_history.'), [1 2]);
    [Min, I] = min(asset_mean_returns);
    return_mean_min_cell(j,i) =  num2cell([Min, I],[1 2]);
    [Max, I] = max(asset_mean_returns);
    return_mean_max_cell(j,i)=  num2cell([Max, I],[1 2]);
    end
end

% Minimum Risk Portfolio Allocations

 min_risk_allocation_cell = cell(15,3);
 
 for i=1:1:size(return_cov_cell,2)
   group_cell = return_cov_cell(:,i); %group (A,B, or C)
    for j=1:1:size(return_cov_cell,1)
       year_cov = cell2mat(group_cell(j));
       fmv = min_risk_port_alloc(year_cov);
       min_risk_allocation_cell(j,i) = num2cell(fmv,[1 2]);
    end
 end
 
       
disp('****** Group A: Minimum Volatility Portfolio Allocation *******')

Group_A_Min_Risk_Port_Allocation = array2table(round(reshape(cell2mat(min_risk_allocation_cell(:,1)),3, 15).',3),  ...
           'RowNames',{'2003','2004','2005','2006',...
                            '2007','2008','2009','2010','2011', ...
                            '2012','2013','2014','2015','2016','2017'}, ... 
           'VariableNames', {'VFINX','VBTIX','VGSLX'})

disp('****** Group B: Minimum Volatility Portfolio Allocation *******')       

Group_B_Min_Risk_Port_Allocation = array2table(round(reshape(cell2mat(min_risk_allocation_cell(:,2)),[6 15]).',3),  ...
            'RowNames',{'2003','2004','2005','2006',...
                            '2007','2008','2009','2010','2011', ...
                            '2012','2013','2014','2015','2016','2017'}, ...   
            'VariableNames',{'VFINX','VBTIX','VGSLX','VTRIX', 'VGTSX', 'VBTLX'} )


disp('****** Group ABC: Minimum Volatility Portfolio Allocation *******')
Group_ABC_Min_Risk_Port_Allocation = array2table(round(reshape(cell2mat(min_risk_allocation_cell(:,3)),[9 15]).',3),  ...
               'RowNames',{'2003','2004','2005','2006','2007',...
                           '2008','2009','2010','2011','2012',...
                           '2013','2014','2015','2016', '2017'},  ...   
            'VariableNames',{'VFINX','VBTIX','VGSLX','VWIGX', 'VFICX', 'VFSTX', 'INTC', 'JPM','GE'} )
         
Group_A_Min_Risk_Port_Allocation = round(reshape(cell2mat(min_risk_allocation_cell(:,1)),3, 15).',3);        
Group_AB_Min_Risk_Port_Allocation = round(reshape(cell2mat(min_risk_allocation_cell(:,2)),[6 15]).',3);   
Group_ABC_Min_Risk_Port_Allocation = round(reshape(cell2mat(min_risk_allocation_cell(:,3)),[9 15]).',3);

%%

% 1 Year Treasury Rate yeild ( Safe Investment ) at the END of year
safe_investment = [ 1.31, ... %2003
                    2.75, ... %2004
                    4.38, ... %2005
                    5.00, ... %2006
                    3.06, ... %2007
                    0.40, ... %2008
                    0.47, ... %2009
                    0.29, ... %2010
                    0.12, ... %2011
                    0.15, ... %2012
                    0.13, ... %2013
                    0.25, ... %2014
                    0.65, ... %2015
                    0.81, ... %2016
                    1.73]./100 ;  %2017
                
% Trading days per year

num_2003 = 252; num_2004 = 252; num_2005 = 252;
num_2006 = 251; num_2007 = 251; num_2008 = 253;
num_2009 = 252; num_2010 = 252; num_2011 = 252;
num_2012 = 250; num_2013 = 252; num_2014 = 252;
num_2015 = 252; num_2016 = 252; num_2017 = 251;

trd_days_per_years = [num_2003,num_2004,num_2005,num_2006,num_2007,...
                      num_2008,num_2009,num_2010,num_2011,num_2012,...
                      num_2013,num_2014,num_2015,num_2016,num_2017];

% In practice credit line annual return ~+3 points
credit_line = safe_investment + 3/100; 

% Risk Free & Credit line return per trading day 
safe_investment = safe_investment./trd_days_per_years;
credit_line = credit_line./trd_days_per_years;
            

% SHARPE RATIO CELL
sharpe_ratio_cell = cell(15,3);
optimal_kelly_bet_cell = cell(15,3);  %caution limit == 0
optimal_kelly_bet_cell_l1 = cell(15,3);
optimal_zeta_cell = cell(15,3);
optimum_zeta_performance_over_kelly_bet = [];
%% Figures
  %% GROUP A
     disp('Plots for Group A: 2003 -2017')

     close all
     marker = ['.';'o';'+';'*';'x';'s';'d';'p';'h';'^';'v';'G';'D';'P'];
     year_array = {'2003','2004','2005','2006',...
                   '2007','2008','2009','2010','2011', ...
                   '2012','2013','2014','2015','2016','2017'};
        
opt_zeta = [];
rets_hist = [];
caution_zero_return_hist = [];
optimum_zeta_port_return_hist = [];
for i=1:1:15
    
     figure(i)
     
     % 1.) the volatility and return mean for that year of each asset
     [vol, mean] = vol_and_mean(cell2mat(return_mean_cell(i,1)),...
                                cell2mat(return_cov_cell(i,1)));
     for a=1:1:length(vol)
     scatter(vol(a),mean(a),marker(a));
     hold on 
     end
     
     %? 2.) Volatility and return mean for that year of 
     %  the Markowitz portfolio with allocation that is 
     %  equidistributed within the collection of assets8
     
     [vol_mk, mean_mk] =  equi_dist_MK_alloc(cell2mat(return_cov_cell(i,1)),...
                                             cell2mat(return_mean_cell(i,1)));
     scatter(vol_mk, mean_mk,marker(a+1));
     
     
     % 3.) The volatility and return mean for that year of 
     % the minimum volatility portfolio; 
    [vol_mr, mean_mr] = min_risk_port_mean_vol(cell2mat(min_risk_allocation_cell(i,1)), ...
                                               cell2mat(return_cov_cell(i,1)),...
                                               cell2mat(return_mean_cell(i,1)));   
    scatter(vol_mr, mean_mr,marker(a+2));

    
    % 4.) The unlimited frontier that is associated with the appropriate
    % return mean and covariance
    axis([0 0.02 -.4e-3 1.1e-3])
    [mu,sig] = unlimited_markowitz(cell2mat(return_cov_cell(i,1)),...
                                    cell2mat(return_mean_cell(i,1)));
    hold on 
    plot(sig,mu,'k-')
    
    
     % 5.) the long frontier (leverage limit ` = 0) that is associated with
     % the appropriate return mean and covariance
     [mu,sig] = long_frontier(cell2mat(return_mean_cell(i,1)),cell2mat(return_cov_cell(i,1)));
     plot(sig,mu,'r-')

      
     % Computing Sharpe Ratio of Unlimited frontier
    [vol_mr, mean_mr] = min_risk_port_mean_vol(cell2mat(min_risk_allocation_cell(i,1)), ...
                                               cell2mat(return_cov_cell(i,1)),...
                                               cell2mat(return_mean_cell(i,1)));  

   [sig_tg, mu_tg,SR] = sharpe_ratio(cell2mat(min_risk_allocation_cell(i,1)),...
                                    cell2mat(return_cov_cell(i,1)),...
                                    cell2mat(return_mean_cell(i,1)),...
                                    safe_investment(i));
    %Tangent half line part of efficient frontier 
    f_lf = @(x) SR*x+safe_investment(i);
    hold on
    fplot(f_lf,[0 sig_tg],'g-');

    
   %plotting tangent port of ulimited frontier                             
   scatter(sig_tg, mu_tg,marker(a+3));

   sharpe_ratio_cell(i,1) = num2cell(SR, [1 2]);
   fprintf('Sharpe Ratio for Group A %s : %.4f \n',cell2mat(year_array(i)), cell2mat(sharpe_ratio_cell(i,1)))
  
  
  
       %Efficient Long Frontier
      
      [sigs,mus,sig,mu,slope, eff_ports]=efficient_limited_frontier(return_mean_cell(i,1),return_cov_cell(i,1),0,safe_investment(i));
      f_lf = @(x) slope*x+safe_investment(i);
      hold on
      fplot(f_lf,[0 sig],'c-.');
      hold on
      plot(sigs,mus,'c-.');
      
      
      zeta = [0, .25, .5, .75, 1, 1.25, 1.5, 1.75, 2];
      
      [index_of_interest, opt_port ] =optimal_portfolio( sigs,mus,zeta,trd_days_per_years(i),eff_ports,3);
     

       
      if i~=15
      [year_opt_zeta,max_objective,rets] = optimal_zeta(cell2mat(return_history_cell(i+1,1)),...
                                                    opt_port.', safe_investment(i));
      opt_zeta = [opt_zeta, year_opt_zeta];
      rets_hist = [rets_hist; rets];
      
      
       %%% performance of caution limit zero over next years
      caution_zero_port = opt_port(:,1);
      [caution_zero_return] = returns_for_caution_zero(cell2mat(return_history_cell(i+1,1)),...
                                                    caution_zero_port.', safe_investment(i));
                                                
      caution_zero_return_hist = [ caution_zero_return_hist, caution_zero_return];
      %%%
      
      % I use returns_for_caution_zero function but it just computes
      % returns, nothing specific to the caution zero, just pass in optimum
      % zeta port
      optimum_zeta_port_return  = returns_for_caution_zero(cell2mat(return_history_cell(i+1,1)),... 
                                                    opt_port(:,year_opt_zeta).', safe_investment(i));
                                                
      optimum_zeta_port_return_hist =[optimum_zeta_port_return_hist, optimum_zeta_port_return];
                                                
      end
      
title(year_array(i))
      
legend({'VFINX','VBTIX','VGSLX','Equi-Distributed Markowitz Portfolio',...
        'Minimum Volatility Portfolio', ...
         'Unlimited Frontier','Long Frontier','Efficient Frontier Tangent Half Line',...
         'Tangency Porfolio', 'Efficient Long Frontier','Efficient Long Frontier'},...
         'Location', 'Best')   

    
    
 grid on
end

      
optimum_zeta_performance_over_kelly_bet(1,:) = optimum_zeta_port_return_hist - caution_zero_return_hist;


%zeta_array = [0, .25, .5, .75, 1, 1.25, 1.5, 1.75, 2];
for i=1:1:length(opt_zeta)
   if opt_zeta(i) == 1 
       opt_zeta(i) = 0;
       optimal_zeta_cell(i,1) = num2cell(opt_zeta(i), [1 2]);
   elseif opt_zeta(i) == 2
       opt_zeta(i) = 0.25;
       optimal_zeta_cell(i,1) = num2cell(opt_zeta(i), [1 2]);
   elseif opt_zeta(i) == 3
       opt_zeta(i) = 0.5;
       optimal_zeta_cell(i,1) = num2cell(opt_zeta(i), [1 2]);
   elseif opt_zeta(i) == 4
       opt_zeta(i) = 0.75;
       optimal_zeta_cell(i,1) = num2cell(opt_zeta(i), [1 2]);
   elseif opt_zeta(i) == 5
       opt_zeta(i) = 1.0;    
       optimal_zeta_cell(i,1) = num2cell(opt_zeta(i), [1 2]);
   elseif opt_zeta(i) == 6
       opt_zeta(i) = 1.25; 
       optimal_zeta_cell(i,1) = num2cell(opt_zeta(i), [1 2]);
   elseif opt_zeta(i) == 7
       opt_zeta(i) = 1.5;
       optimal_zeta_cell(i,1) = num2cell(opt_zeta(i), [1 2]);
   elseif opt_zeta(i) == 8
       opt_zeta(i) = 1.75; 
       optimal_zeta_cell(i,1) = num2cell(opt_zeta(i), [1 2]);
   elseif opt_zeta(i) == 9
       opt_zeta(i) = 2.0;
       optimal_zeta_cell(i,1) = num2cell(opt_zeta(i), [1 2]);
   end
end




 %% GROUP AB
  
     disp('Plots for Group AB: 2003 -2017')

     close all
     marker = ['.';'o';'+';'*';'x';'s';'d';'p';'h';'^';'v';'G';'D';'P'];
     year_array = {'2003','2004','2005','2006',...
                   '2007','2008','2009','2010','2011', ...
                   '2012','2013','2014','2015','2016','2017'};
        
opt_zeta = [];
rets_hist = [];
caution_zero_return_hist = [];
optimum_zeta_port_return_hist = [];

for i=1:1:15
    
     figure(i)
     
     % 1.) the volatility and return mean for that year of each asset
     [vol, mean] = vol_and_mean(cell2mat(return_mean_cell(i,2)),...
                                cell2mat(return_cov_cell(i,2)));
     for a=1:1:length(vol)
     scatter(vol(a),mean(a),marker(a));
     hold on 
     end
     
     %? 2.) Volatility and return mean for that year of 
     %  the Markowitz portfolio with allocation that is 
     %  equidistributed within the collection of assets8
     
     [vol_mk, mean_mk] =  equi_dist_MK_alloc(cell2mat(return_cov_cell(i,2)),...
                                             cell2mat(return_mean_cell(i,2)));
     scatter(vol_mk, mean_mk,marker(a+1));
     
     
     % 3.) The volatility and return mean for that year of 
     % the minimum volatility portfolio; 
    [vol_mr, mean_mr] = min_risk_port_mean_vol(cell2mat(min_risk_allocation_cell(i,2)), ...
                                               cell2mat(return_cov_cell(i,2)),...
                                               cell2mat(return_mean_cell(i,2)));   
    scatter(vol_mr, mean_mr,marker(a+2));

    
    % 4.) The unlimited frontier that is associated with the appropriate
    % return mean and covariance
    axis([0 0.02 -.4e-3 1.1e-3])
    [mu,sig] = unlimited_markowitz(cell2mat(return_cov_cell(i,2)),...
                                    cell2mat(return_mean_cell(i,2)));
    hold on 
    plot(sig,mu,'k-')
    
    
     % 5.) the long frontier (leverage limit ` = 0) that is associated with
     % the appropriate return mean and covariance
     [mu,sig] = long_frontier(cell2mat(return_mean_cell(i,2)),cell2mat(return_cov_cell(i,2)));
     plot(sig,mu,'r-')

      
     % Computing Sharpe Ratio of Unlimited frontier
    [vol_mr, mean_mr] = min_risk_port_mean_vol(cell2mat(min_risk_allocation_cell(i,2)), ...
                                               cell2mat(return_cov_cell(i,2)),...
                                               cell2mat(return_mean_cell(i,2)));  

   [sig_tg, mu_tg,SR] = sharpe_ratio(cell2mat(min_risk_allocation_cell(i,2)),...
                                    cell2mat(return_cov_cell(i,2)),...
                                    cell2mat(return_mean_cell(i,2)),...
                                    safe_investment(i));
    %Tangent half line part of efficient frontier 
    f_lf = @(x) SR*x+safe_investment(i);
    hold on
    fplot(f_lf,[0 sig_tg],'g-');

    
   %plotting tangent port of ulimited frontier                             
   scatter(sig_tg, mu_tg,marker(a+3));

   sharpe_ratio_cell(i,2) = num2cell(SR, [1 2]);
   fprintf('Sharpe Ratio for Group AB %s : %.4f \n',cell2mat(year_array(i)), cell2mat(sharpe_ratio_cell(i,2)))
  
  
  
       %Efficient Long Frontier
      
      [sigs,mus,sig,mu,slope, eff_ports]=efficient_limited_frontier(return_mean_cell(i,2),return_cov_cell(i,2),0,safe_investment(i));
      f_lf = @(x) slope*x+safe_investment(i);
      hold on
      fplot(f_lf,[0 sig],'c-.');
      hold on
      plot(sigs,mus,'c-.');
      
      
      zeta = [0, .25, .5, .75, 1, 1.25, 1.5, 1.75, 2];
      
      [index_of_interest, opt_port ] =optimal_portfolio( sigs,mus,zeta,trd_days_per_years(i),eff_ports,6);
     
      
      if i~=15
      [year_opt_zeta,max_objective,rets] = optimal_zeta(cell2mat(return_history_cell(i+1,2)),...
                                                    opt_port.', safe_investment(i));
      opt_zeta = [opt_zeta, year_opt_zeta];
      rets_hist = [rets_hist; rets];
      
       %%% performance of caution limit zero over next years
      caution_zero_port = opt_port(:,1);
      [caution_zero_return] = returns_for_caution_zero(cell2mat(return_history_cell(i+1,2)),...
                                                    caution_zero_port.', safe_investment(i));

     caution_zero_return_hist = [ caution_zero_return_hist, caution_zero_return];
      %%%
      
      
       % I use returns_for_caution_zero function but it just computes
      % returns, nothing specific to the caution zero, just pass in optimum
      % zeta port
      optimum_zeta_port_return  = returns_for_caution_zero(cell2mat(return_history_cell(i+1,2)),... 
                                                    opt_port(:,year_opt_zeta).', safe_investment(i));
                                                
      optimum_zeta_port_return_hist =[optimum_zeta_port_return_hist, optimum_zeta_port_return];
      end

title(year_array(i))
      
legend({'VFINX','VBTIX','VGSLX','VTRIX', 'VGTSX', 'VBTLX',...
        'Equi-Distributed Markowitz Portfolio',...
        'Minimum Volatility Portfolio', ...
         'Unlimited Frontier','Long Frontier','Efficient Frontier Tangent Half Line',...
         'Tangency Porfolio', 'Efficient Long Frontier','Efficient Long Frontier'},...
         'Location', 'Best')   

    
    
 grid on
end

optimum_zeta_performance_over_kelly_bet(2,:) = optimum_zeta_port_return_hist - caution_zero_return_hist;


for i=1:1:length(opt_zeta)
   if opt_zeta(i) == 1 
       opt_zeta(i) = 0;
       optimal_zeta_cell(i,2) = num2cell(opt_zeta(i), [1 2]);
   elseif opt_zeta(i) == 2
       opt_zeta(i) = 0.25;
       optimal_zeta_cell(i,2) = num2cell(opt_zeta(i), [1 2]);
   elseif opt_zeta(i) == 3
       opt_zeta(i) = 0.5;
       optimal_zeta_cell(i,2) = num2cell(opt_zeta(i), [1 2]);
   elseif opt_zeta(i) == 4
       opt_zeta(i) = 0.75;
       optimal_zeta_cell(i,2) = num2cell(opt_zeta(i), [1 2]);
   elseif opt_zeta(i) == 5
       opt_zeta(i) = 1.0;    
       optimal_zeta_cell(i,2) = num2cell(opt_zeta(i), [1 2]);
   elseif opt_zeta(i) == 6
       opt_zeta(i) = 1.25; 
       optimal_zeta_cell(i,2) = num2cell(opt_zeta(i), [1 2]);
   elseif opt_zeta(i) == 7
       opt_zeta(i) = 1.5;
       optimal_zeta_cell(i,2) = num2cell(opt_zeta(i), [1 2]);
   elseif opt_zeta(i) == 8
       opt_zeta(i) = 1.75; 
       optimal_zeta_cell(i,2) = num2cell(opt_zeta(i), [1 2]);
   elseif opt_zeta(i) == 9
       opt_zeta(i) = 2.0;
       optimal_zeta_cell(i,2) = num2cell(opt_zeta(i), [1 2]);
   end
end


 %% GROUP ABC
  
     disp('Plots for Group ABC: 2003 -2017')

     close all
     marker = ['.';'o';'+';'*';'x';'s';'d';'p';'h';'^';'v';'G';'D';'P'];
     year_array = {'2003','2004','2005','2006',...
                   '2007','2008','2009','2010','2011', ...
                   '2012','2013','2014','2015','2016','2017'};
opt_zeta = [];
rets_hist = [];
caution_zero_return_hist = [];
optimum_zeta_port_return_hist = [];

for i=1:1:15
    
     figure(i)
     
     % 1.) the volatility and return mean for that year of each asset
     [vol, mean] = vol_and_mean(cell2mat(return_mean_cell(i,3)),...
                                cell2mat(return_cov_cell(i,3)));
     for a=1:1:length(vol)
     scatter(vol(a),mean(a),marker(a));
     hold on 
     end
     
     %? 2.) Volatility and return mean for that year of 
     %  the Markowitz portfolio with allocation that is 
     %  equidistributed within the collection of assets8
     
     [vol_mk, mean_mk] =  equi_dist_MK_alloc(cell2mat(return_cov_cell(i,3)),...
                                             cell2mat(return_mean_cell(i,3)));
     scatter(vol_mk, mean_mk,marker(a+1));
     
     
     % 3.) The volatility and return mean for that year of 
     % the minimum volatility portfolio; 
    [vol_mr, mean_mr] = min_risk_port_mean_vol(cell2mat(min_risk_allocation_cell(i,3)), ...
                                               cell2mat(return_cov_cell(i,3)),...
                                               cell2mat(return_mean_cell(i,3)));   
    scatter(vol_mr, mean_mr,marker(a+2));

    
    % 4.) The unlimited frontier that is associated with the appropriate
    % return mean and covariance
    axis([0 0.02 -.4e-3 1.1e-3])
    [mu,sig] = unlimited_markowitz(cell2mat(return_cov_cell(i,3)),...
                                    cell2mat(return_mean_cell(i,3)));
    hold on 
    plot(sig,mu,'k-')
    
    
     % 5.) the long frontier (leverage limit ` = 0) that is associated with
     % the appropriate return mean and covariance
     [mu,sig] = long_frontier(cell2mat(return_mean_cell(i,3)),cell2mat(return_cov_cell(i,3)));
     plot(sig,mu,'r-')

      
     % Computing Sharpe Ratio of Unlimited frontier
    [vol_mr, mean_mr] = min_risk_port_mean_vol(cell2mat(min_risk_allocation_cell(i,3)), ...
                                               cell2mat(return_cov_cell(i,3)),...
                                               cell2mat(return_mean_cell(i,3)));  

   [sig_tg, mu_tg,SR] = sharpe_ratio(cell2mat(min_risk_allocation_cell(i,3)),...
                                    cell2mat(return_cov_cell(i,3)),...
                                    cell2mat(return_mean_cell(i,3)),...
                                    safe_investment(i));
    %Tangent half line part of efficient frontier 
    f_lf = @(x) SR*x+safe_investment(i);
    hold on
    fplot(f_lf,[0 sig_tg],'g-');

    
   %plotting tangent port of ulimited frontier                             
   scatter(sig_tg, mu_tg,marker(a+3));

   sharpe_ratio_cell(i,3) = num2cell(SR, [1 2]);
   fprintf('Sharpe Ratio for Group ABC %s : %.4f \n',cell2mat(year_array(i)), cell2mat(sharpe_ratio_cell(i,3)))
  
  
  
       %Efficient Long Frontier
      
      [sigs,mus,sig,mu,slope, eff_ports]=efficient_limited_frontier(return_mean_cell(i,3),return_cov_cell(i,3),0,safe_investment(i));
      f_lf = @(x) slope*x+safe_investment(i);
      hold on
      fplot(f_lf,[0 sig],'c-.');
      hold on
      plot(sigs,mus,'c-.');
      
      
      zeta = [0, .25, .5, .75, 1, 1.25, 1.5, 1.75, 2];
      
      [index_of_interest, opt_port ] =optimal_portfolio( sigs,mus,zeta,trd_days_per_years(i),eff_ports,9);
     
      scatter(sigs(index_of_interest), mus(index_of_interest),'*');

       
      if i~=15
      [year_opt_zeta,max_objective,rets] = optimal_zeta(cell2mat(return_history_cell(i+1,3)),...
                                                    opt_port.', safe_investment(i));
      opt_zeta = [opt_zeta, year_opt_zeta];
      rets_hist = [rets_hist; rets];
      
      
      
       %%% performance of caution limit zero over next years
      caution_zero_port = opt_port(:,1);
      [caution_zero_return] = returns_for_caution_zero(cell2mat(return_history_cell(i+1,3)),...
                                                    caution_zero_port.', safe_investment(i));
                                                
      caution_zero_return_hist = [ caution_zero_return_hist, caution_zero_return];
      %%%
      
       % I use returns_for_caution_zero function but it just computes
      % returns, nothing specific to the caution zero, just pass in optimum
      % zeta port
      optimum_zeta_port_return  = returns_for_caution_zero(cell2mat(return_history_cell(i+1,3)),... 
                                                    opt_port(:,year_opt_zeta).', safe_investment(i));
                                                
      optimum_zeta_port_return_hist =[optimum_zeta_port_return_hist, optimum_zeta_port_return];
      end

      
      scatter(sigs(index_of_interest), mus(index_of_interest),'*');

title(year_array(i))
      
legend({'VFINX','VBTIX','VGSLX','VTRIX', 'VGTSX', 'VBTLX', 'INTC', 'JPM','GE',...
        'Equi-Distributed Markowitz Portfolio',...
        'Minimum Volatility Portfolio', ...
         'Unlimited Frontier','Long Frontier','Efficient Frontier Tangent Half Line',...
         'Tangency Porfolio', 'Efficient Long Frontier','Efficient Long Frontier', 'Tangent Portfolio'},...
         'Location', 'Best')   

    
    
 grid on
end

optimum_zeta_performance_over_kelly_bet(3,:) = optimum_zeta_port_return_hist - caution_zero_return_hist;

for i=1:1:length(opt_zeta)
   if opt_zeta(i) == 1 
       opt_zeta(i) = 0;
       optimal_zeta_cell(i,3) = num2cell(opt_zeta(i), [1 2]);
   elseif opt_zeta(i) == 2
       opt_zeta(i) = 0.25;
       optimal_zeta_cell(i,3) = num2cell(opt_zeta(i), [1 2]);
   elseif opt_zeta(i) == 3
       opt_zeta(i) = 0.5;
       optimal_zeta_cell(i,3) = num2cell(opt_zeta(i), [1 2]);
   elseif opt_zeta(i) == 4
       opt_zeta(i) = 0.75;
       optimal_zeta_cell(i,3) = num2cell(opt_zeta(i), [1 2]);
   elseif opt_zeta(i) == 5
       opt_zeta(i) = 1.0;    
       optimal_zeta_cell(i,3) = num2cell(opt_zeta(i), [1 2]);
   elseif opt_zeta(i) == 6
       opt_zeta(i) = 1.25; 
       optimal_zeta_cell(i,3) = num2cell(opt_zeta(i), [1 2]);
   elseif opt_zeta(i) == 7
       opt_zeta(i) = 1.5;
       optimal_zeta_cell(i,3) = num2cell(opt_zeta(i), [1 2]);
   elseif opt_zeta(i) == 8
       opt_zeta(i) = 1.75; 
       optimal_zeta_cell(i,3) = num2cell(opt_zeta(i), [1 2]);
   elseif opt_zeta(i) == 9
       opt_zeta(i) = 2.0;
       optimal_zeta_cell(i,3) = num2cell(opt_zeta(i), [1 2]);
   end
end


%% Sharpe Ratios
%% 
%  Sharpe Ratios for each group and year evaluated at the Unlimited
%  frontier tangent portfolio

disp('******   Sharpe Ratios for each group and year evaluated ******')
disp('******   at Unlimited Frontier Tangent Portfolio         ******')
sharpe_ratios_table = array2table(sharpe_ratio_cell,  ...
               'RowNames',{'2003','2004','2005','2006','2007',...
                           '2008','2009','2010','2011','2012',...
                           '2013','2014','2015','2016', '2017'},  ...   
            'VariableNames',{'Group_A','Group_AB','Group_ABC'} )

%% How much better did optimal Zeta portfolio do than the Kelly investor
zeta_kelly_performance_table = array2table(optimum_zeta_performance_over_kelly_bet.',  ...
               'RowNames',{'2004','2005','2006','2007',...
                           '2008','2009','2010','2011','2012',...
                           '2013','2014','2015','2016', '2017'},  ...   
            'VariableNames',{'Group_A','Group_AB','Group_ABC'} )



%% Function Appendix 
function r_hist = return_history(price_hist,days)
span = days(1):1:days(2);
return_hist =  ones(1,(days(2)-days(1)));
for i=1:1:length(return_hist)
    return_hist(i) = (price_hist(span(i)+1) - price_hist(span(i))) / price_hist(span(i));
end
r_hist = return_hist;
end


function  fmv =  min_risk_port_alloc(covar)
y = linsolve(covar, ones(size(covar,1),1));
a = ones(1,length(y))*y;
fmv = (1/a)*y;
end

      function [index_of_interest , opt_port ] = optimal_portfolio( sigs,mus,zeta,days_of_year,ports,num_assets)
      index_of_interest=[];
      opt_port=[];
      
      for i=1:1:length(zeta)
          caution_coeff = (1/sqrt(1-(1/days_of_year)))*(zeta(i)/sqrt(days_of_year));
           % Quadratic Estimator, caution limit = 0
           f_lf = @(x,y) (y-(0.5*y.^2)-(0.5*x.^2)-(caution_coeff*x));
           x = sigs;
           y = mus;
           z=f_lf(x,y);
           [max_z, index] = max(z);
           index_of_interest = [index_of_interest; index];
          %disp('Optimal Long Portfolio: ');
          opt_port =[opt_port ports(num_assets+1:end,index)];
          
          end
      end
    %{ 
    function [opt_zeta,max_return] = optimal_zeta(m,optimal_portfolios)
     portfolio_return = optimal_portfolios*m
     [max_return, index] = max(portfolio_return);
     opt_zeta = index;
     end
     %}
 %{
    function [opt_zeta,max_objective] = optimal_zeta(daily_return_hist_next_year,optimal_portfolios, safe_investment)
    % one risk free asset model:
    objective_array = []
    for i=1:1:size(optimal_portfolios, 1) %1-9 
       r_sum = 0;
        for j=1:1:size(daily_return_hist_next_year,2)
            
        day_return = (1-ones(length(optimal_portfolios(i,:)),1)*optimal_portfolios(i,:))*safe_investment + optimal_portfolios(i,:)*daily_return_hist_next_year(:,j);
        r_sum = r_sum + log10(1 + day_return);
        end
        objective = r_sum/size(daily_return_hist_next_year,2);
        objective_array = [objective_array objective]; %should be length 9
        
    end
    
    [max_objective, index] = max(objective_array);
     opt_zeta = index;
    end
  %} 
    function [opt_zeta,max_objective,rets] = optimal_zeta(daily_return_hist_next_year,optimal_portfolios, safe_investment)
    % one risk free asset model:
    objective_array = [];
    rets = [];
    for i=1:1:size(optimal_portfolios, 1) %1-9 
       r_sum = 0;
        for j=1:1:size(daily_return_hist_next_year,2)
            
        day_return = (1-ones(1,length(optimal_portfolios(i,:)))*optimal_portfolios(i,:).')*safe_investment + optimal_portfolios(i,:)*daily_return_hist_next_year(:,j);
       % r_sum = r_sum + log10(1 + day_return);
        r_sum = (1+r_sum)*(1 + day_return);

        end
        objective = r_sum/size(daily_return_hist_next_year,2);
        objective_array = [objective_array objective]; %should be length 9
        rets = [rets r_sum];
    end
    
    [max_objective, index] = max(objective_array);
    opt_zeta = index;
    %disp(length(objective_array));
    %objective_array;
    rets = rets-1;
    end
   
    
  function [rets] = returns_for_caution_zero(daily_return_hist_next_year,optimal_portfolios, safe_investment)
    % one risk free asset model:
    objective_array = [];
    rets = [];
    r_sum = 0;
        for j=1:1:size(daily_return_hist_next_year,2)

        day_return = (1-ones(1,length(optimal_portfolios))*optimal_portfolios.')*safe_investment + optimal_portfolios*daily_return_hist_next_year(:,j);
        r_sum = (1+r_sum)*(1 + day_return);
        end
        rets = [rets r_sum];
        rets =rets -1; 
   end
   
    
 
     
function [mu,sig] = unlimited_markowitz(covar,m)
        %covar = cell2mat(covar);
        %m = cell2mat(m);
        y=linsolve(covar,ones(length(covar),1));
        z=linsolve(covar,m);
        a=ones(1,length(y))*y;
        b=ones(1,length(z))*z;
        c=m'*z;
        mu = -5e-3:.000001:5e-3;
        sig=sqrt(1/a + (a/(a*c - b^2))*(mu - b/a).^2);

end

function [vol, mean] = vol_and_mean(m,v)
mean = m;
vars = diag(v);
vol =  sqrt(vars);
end

function [vol_mr, mean_mr] = min_risk_port_mean_vol(alloc, covar,m)
%m   = cell2mat(m);
%cov = cell2mat(cov);
%alloc = cell2mat(alloc);
mean_mr = (m.')*alloc;
vol_mr = sqrt(alloc.'*covar*alloc);
end

function [vol_mk, mean_mk] = equi_dist_MK_alloc(cov,m)
 %m = cell2mat(m);
 %cov = cell2mat(cov);
 f_mk = ones(length(cov),1);
 f_mk = f_mk/length(cov);
 mean_mk = (m.')*f_mk;
 vol_mk = sqrt(f_mk.'*cov*f_mk);
end

function [mu,sig] = long_frontier(m,v)
% pass in singel m and v
%mn = min(cell2mat(m));
%mx = max(cell2mat(m));
mn = min(m);
mx = max(m);
%m = cell2mat(m);
%v = cell2mat(v);
vars = diag(v);
min_var = min(vars);
max_var = min(vars);
in = 1;
mu = mn:.00001:mx; 
sig  = zeros(length(mu),1);
    for i=1:1:length(mu);
     options = optimoptions('quadprog','Display','off');
     f_lf = quadprog(v,zeros(length(v),1).',-eye(length(v)),zeros(length(v),1).',[ones(length(v),1).';m.'],[1; mu(i)],[],[],[],options);
     sig(i) = sqrt(f_lf.'*v*f_lf);
     in=+1;
    end
end




function [sig_low,mu_low,sig_high,mu_high] = solvent_portfolios(m,v,lev_lim,p,VR)
    mn = min(m);
    mx = max(m);
    mn_l = mn - lev_lim*(mx-mn);
    mx_l = mx + lev_lim*(mx-mn);
    vars = diag(v);
    min_var = min(vars);
    max_var = min(vars);
    mu = (mn_l:.00001:mx_l)';
    sig  = zeros(length(mu),1);
    sig_high = 1;
    mu_high = 1;
    sig_low = 1;
    mu_low = 1;
    for i=1:size(mu)
        T = [2*v,ones(size(v,1),1);ones(1,size(v,1)),0;m,0];
        x = linsolve(T,[zeros(size(v,1),1);1;mu(i)]);
        if (VR*x(1:size(v,1)) > p)
            if sig_low == 1
                sig_low = sqrt(x(1:size(v,1))'*v*x(1:size(v,1)));
                mu_low = x(1:size(v,1))'*m';
            else
                sig_high = sqrt(x(1:size(v,1))'*v*x(1:size(v,1)));
                mu_high = x(1:size(v,1))'*m';
            end
        end
    end
end



function [sig, mu, sig_t, mu_t, slope, allocs] = efficient_limited_frontier(m,v,lev_lim,rf)
% This function takes in a mean return vector, covariance matrix, leverage
% limit and safe investment risk free rate. It then computes the greatest
% slope between a portfolio on the particular limited frontier, the mu and
% sigma associated with this portfolio, and subsequent values of sigma and
% mu that produce the traditional limited frontier. 

allocs = [];
% pass in single m vector and v matrix
mn = min(cell2mat(m));
mx = max(cell2mat(m));
m = cell2mat(m);
v = cell2mat(v);
%mn = min(m);
%mx = max(m);
mn_l = mn - lev_lim*(mx-mn);
mx_l = mx + lev_lim*(mx-mn);

mu = (mn_l:.00001:mx_l)'; 
%disp('Length of mu mu in function:')
%length(mu)
sig  = zeros(length(mu),1);

for i=1:1:length(mu);
    
    options = optimoptions('quadprog','Display','off');
    % f_lf = quadprog(v,zeros(length(v),1).',[eye(length(v));-eye(length(v)) ],[sqrt((ones(length(v),1)*(1+2*lev_lim)).^2).' ; zeros(length(v),1).'],[ones(length(v),1).';m.'],[1; mu(i)],[],[],[],options);
    %test tasking out the all elements of f must be greater than zero
    
    %f_lf = quadprog([v, zeros(length(v); zeros(length(v), zeros(length(v)],zeros(length(v),1).',[eye(length(v)) ],[sqrt((ones(length(v),1)*(1+2*lev_lim)).^2).'],[ones(length(v),1).';m.'],[1; mu(i)],[],[],[],options);
    A = [v, zeros(length(v)); zeros(length(v)), zeros(length(v))];
    B = zeros(length(A),1);
    C = [-eye(length(v)), -eye(length(v)); eye(length(v)), -eye(length(v)); zeros(1,length(v)), ones(1,length(v))];
    D = [zeros(length(C)-1,1); 1+2*lev_lim];
    %[sqrt((ones(length(v)*2,1)*(1+2*lev_lim)).^2).'];
    Aeq = [ones(length(v),1).',zeros(1,length(A)-length(v)); m.', zeros(1,length(A)-length(m))];
    %[ones(length(v),1).', zeros(length(v),1).'; m.',  zeros(length(v),1).';ones(length(v),1).', zeros(length(v),1).'];
    Beq = [1; mu(i)];
    f_lf = quadprog(A ,B , C, D,Aeq ,Beq ,[],[],[],options);
    allocs = [allocs f_lf];
    sig(i) = sqrt(f_lf(1:length(v)).'*v*f_lf(1:length(v)));
    
    % slope between risk free return 
    % will you ever go insolvent if youre on any of the frontier
    % how does that change your solvency 
    % is it possible to go insolvent when holding a port on any of the
    % fonriters
            % maybe just the limited , un..
                                     % ' toom transpose off of m
    slope_temp = (f_lf(1:length(v))'*m-rf)/sqrt(f_lf(1:length(v))'*v*f_lf(1:length(v)));
    if (i == 1 || slope_temp > slope)
        slope = slope_temp;
        sig_t = sqrt(f_lf(1:length(v))'*v*f_lf(1:length(v)));
        mu_t = f_lf(1:length(v))'*m; %took transpose off of m
        idx = i;
    end
end

%sig = sig(idx:size(sig,1));
%mu = mu(idx:size(mu,1));
%allocs = allocs(idx:size(mu,1))

end



% Use the save the alloaction for each point returned by quadprog and the
% use this as the optimate... use for efficient frontier. This will give
% you the optimal

%The indices of the arrays will be the same.

function f = RA_tangency_port_alloc(vol_mr, mean_mr,covar,m,mu_rf)

% if safe_or_credit = 0: calc safe investment tangency alloc
% if safe_or_credit = 1: calc credit line tangency alloc
f = ((vol_mr^2)/(mean_mr-mu_rf))*inv(covar)*(m-mu_rf*ones(length(m),1));

end


function [sig_tg, mu_tg, SR] = sharpe_ratio(min_risk_alloc, v,m, risk_free_return)
%risk_free_return == daily return from the safe investment
[min_risk_vol, min_risk_mean] = min_risk_port_mean_vol(min_risk_alloc, v, m);

v_as = sqrt((m.'*inv(v)*m) - (((ones(length(m),1).'*inv(v)*m)^2)/(ones(length(m),1).'*inv(v)*ones(length(m),1))));

sig_tg = min_risk_vol*sqrt(1+(((v_as*min_risk_vol)/(min_risk_mean-risk_free_return))^2));
mu_tg  = min_risk_mean +(((v_as^2)*(min_risk_vol^2))/(min_risk_mean-risk_free_return));

v_tg = v_as*sqrt(1+(((min_risk_mean-risk_free_return)/(v_as*min_risk_vol))^2));

SR = v_tg;
%SR = (mu_tg - risk_free_return)/sig_tg;
end

%{
function optimal_port = kelly_bet(min_risk_alloc, v,m, risk_free_return)
%risk_free_return == daily return from the safe investment
[min_risk_vol, min_risk_mean] = min_risk_port_mean_vol(min_risk_alloc, v, m);

v_as = sqrt((m.'*inv(v)*m) - (((ones(length(m),1).'*inv(v)*m)^2)/(ones(length(m),1).'*inv(v)*ones(length(m),1))));

%sig_tg = min_risk_vol*sqrt(1+(((v_as*min_risk_vol)/(min_risk_mean-risk_free_return))^2));
%mu_tg  = min_risk_mean +(((v_as^2)*(min_risk_vol^2))/(min_risk_mean-risk_free_return));
v_tg = v_as*sqrt(1+(((min_risk_mean-risk_free_return)/(v_as*min_risk_vol))^2));
%SR = v_tg;

optimal_port = ((1-risk_free_return)/(1+(v_tg^2)))*inv(v)*(m-risk_free_return*ones(length(m),1));

end
%}

function optimal_long_port = kelly_bet(sig, mu, v, m, risk_free_return)
%v_tg is just  slope which is just sharpe.
%rise over run 
v_tg = (mu-risk_free_return)/sig;
optimal_long_port = ((1-risk_free_return)/(1+(v_tg^2)))*inv(v)*(m-risk_free_return*ones(length(m),1));

end

   


function [sig, mu] = limited_frontier(m,v,lev_lim)

% pass in single m and v
mn = min(cell2mat(m));
mx = max(cell2mat(m));

mn_l = mn - lev_lim*(mx-mn);
mx_l = mx + lev_lim*(mx-mn);

m = cell2mat(m);
v = cell2mat(v);

vars = diag(v);

min_var = min(vars);
max_var = min(vars);


mu = mn_l:.00001:mx_l; 
sig  = zeros(length(mu),1);

for i=1:1:length(mu);
    
    options = optimoptions('quadprog','Display','off');
    % f_lf = quadprog(v,zeros(length(v),1).',[eye(length(v));-eye(length(v)) ],[sqrt((ones(length(v),1)*(1+2*lev_lim)).^2).' ; zeros(length(v),1).'],[ones(length(v),1).';m.'],[1; mu(i)],[],[],[],options);
    %test tasking out the all elements of f must be greater than zero
    
    %f_lf = quadprog([v, zeros(length(v); zeros(length(v), zeros(length(v)],zeros(length(v),1).',[eye(length(v)) ],[sqrt((ones(length(v),1)*(1+2*lev_lim)).^2).'],[ones(length(v),1).';m.'],[1; mu(i)],[],[],[],options);
 
    A = [v, zeros(length(v)); zeros(length(v)), zeros(length(v))];
    
    B = zeros(length(A),1);
    
    C = [-eye(length(v)), -eye(length(v)); eye(length(v)), -eye(length(v)); zeros(1,length(v)), ones(1,length(v))];

    D = [zeros(length(C)-1,1); 1+2*lev_lim];

    %[sqrt((ones(length(v)*2,1)*(1+2*lev_lim)).^2).'];
    
    Aeq = [ones(length(v),1).',zeros(1,length(A)-length(v)); m.', zeros(1,length(A)-length(m))];
    
    %[ones(length(v),1).', zeros(length(v),1).'; m.',  zeros(length(v),1).';ones(length(v),1).', zeros(length(v),1).'];
    
    Beq = [1; mu(i)];
    
    f_lf = quadprog(A ,B , C, D,Aeq ,Beq ,[],[],[],options);
    sig(i) = sqrt(f_lf(1:length(v)).'*v*f_lf(1:length(v)));
    
    % slope between risk free return 
    % will you ever go insolvent if youre on any of the frontier
    % how does that change your solvency 
    % is it possible to go insolvent when holding a port on any of the
    % fonriters
            % maybe just the limited , un..
     
end

end

%{

[mu,sig] = unlimited_markowitz(cell2mat(return_cov_cell(i,1)),...
                                    cell2mat(return_mean_cell(i,1)));
    hold on 
    plot(sig,mu,'k-')
    
    function [tg_sig, tg_mu, slope] = max_slope(mu, sig,)
    
    
    end
%}

function  allocation =  allocation_given_mu(m,covar, mu) 
%m is vector, mu is the independent variable, the intersection mu
y = linsolve(covar, ones(size(covar,1),1));
z = linsolve(covar,m);
a = ones(1,length(y))*y;
b = ones(1,length(z))*z;
c = m.'*z;
v_as = sqrt(((a*c - (b^2)))/a);
fmv = (1/a)*y;
[vol_mr, mean_mr] = min_risk_port_mean_vol(fmv, covar,m);
allocation = fmv + ((mu-mean_mr)/(v_as^2))*inv(covar)*(m - mean_mr*ones(length(m),1));
end

