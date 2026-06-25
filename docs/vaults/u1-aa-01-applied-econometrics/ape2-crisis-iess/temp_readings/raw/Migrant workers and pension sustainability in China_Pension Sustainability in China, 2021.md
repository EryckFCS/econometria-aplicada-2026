## Página 1

Contents lists available at ScienceDirect
Economic Modelling
journal homepage: www.journals.elsevier.com/economic-modelling
Reforming China’s public pension system: Fiscal sustainability and the 
challenge of formality-based inequality$,$$
Han Gao
∗, Bei Lu
UNSW School of Economics, Australia
A R T I C L E  I N F O
Dataset link: Replication Package for Reforming
China’s Public Pension System: Fiscal Sustainab
ility and the Challenge of Formality-Based Ineq
uality (Original data)
JEL classification:
D15
H55
O17
Keywords:
China
Pension reform
Informality
A B S T R A C T
This paper examines the design of China’s public pension system, addressing two major challenges: fiscal 
unsustainability caused by population aging and significant pension disparities between formal and informal 
workers. Using a dynamic quantitative model with long-run macro and demographic trends, we assess the 
effects of the ongoing reforms and offer several options to deepen the reform: indexing pension benefits solely 
to the CPI, raising the resident pensions, and replacing pension financing from payroll tax with consumption 
tax. Our findings indicate that the delayed retirement policy announced in September 2024 could substantially 
mitigate fiscal deficits in the coming decades. Among the options evaluated, raising resident pension alleviates 
the formality-based pension inequality but increases fiscal burden; altering benefit indexation or the tax base 
for pension financing enhances both fiscal sustainability and welfare outcomes; the effects of consumption tax 
are particularly pronounced in the long run.
1. Introduction
China’s pension system plays a vital role in social and economic 
policy and has been fundamentally transformed in recent decades. 
Although significant progress has been made in expanding coverage, it 
remains a system where different groups of workers (formal/informal, 
migrant/local, urban/rural, men/women) have significantly different 
levels of financial protection. And, like other countries that are rapidly 
ageing, China’s pension system is subject to growing fiscal pressures 
with implications not only for the well-being of older people, but also 
for overall fiscal balances.
In this paper, we build a dynamic quantitative model to understand 
how reforming the public pension system can help address the sustain-
ability and equity of the system. We first examine the impacts of the 
2024 reform and examine its impact on public finance and household 
behavior responses including labor supply and savings. Building on
$ This article is part of a Special issue entitled: ‘Population aging’ published in Economic Modelling.
$$ We thank the editor Sushanta Mallick and anonymous referees for their constructive suggestions. We also thank John Piggot and Philip O’Keefe for their useful 
insights when preparing for the DRC/ADB research program on high quality growth in China, Charles Yuji Horioka and Aiko Kikkawa for helpful discussions, 
and the support of the computational facility of the National Computational Infrastructure (NCI) through the UNSW HPC Scheme (DOI:10.26190/PMN5-7J50).
∗Corresponding author.
E-mail addresses: han.gao6@unsw.edu.au (H. Gao), lubei@unsw.edu.au (B. Lu).
1 We use EBPS to refer to the newly merged one that covers employees in for-profit enterprises and non-profit government institutions. Prior to 2015, the EBPS 
only covered workers employed in for-profit enterprises, and the PEP(Public Employee Pension) covered civil servants and employees in non-profit government 
institutions. In 2015, the PEP was merged with the old EBPS, making the new EBPS the uniform program for all employees in urban sectors.
the 2024 policy as the new baseline, we propose and evaluate several 
options aimed at further addressing policy concerns.
In the past 30 years, China has successfully expanded its pension 
coverage to nearly the entire population through two major schemes: 
the Enterprise Basic Pension Scheme (EBPS) and the Rural and Urban 
Residents Pension Scheme (RURPS).1 Adjustments to these schemes 
have followed trends in ageing and the need for economic development 
in the country. By 2023, more than 521 million were enrolled in EBPS 
(including 142 million retirees), representing approximately half of the 
labor force. The remainder were enrolled in RURPS, which had 545 
million members, including 173 million retirees.
The EBPS system is challenged by the increasing fiscal budget 
pressure driven by legacy costs and an ageing demographic structure. 
Although the pension system includes an individual account com-
ponent, it primarily operates on a pay-as-you-go (PAYG) basis. The 
individual accounts function as notional defined contribution accounts,
https://doi.org/10.1016/j.econmod.2025.107336
Received 11 January 2025; Received in revised form 16 September 2025; Accepted 29 September 2025
Economic Modelling 153 (2025) 107336
Available online 3 October 2025 
0264-9993/© 2025 The Authors. Published by Elsevier B.V. This is an open access article under the CC BY license ( http://creativecommons.org/licenses/by/4.0/ ).

## Página 2

H. Gao and B. Lu
offering a credit rate of return that has exceeded bank fixed interest 
rates over the past decade. Social pooling contributions are based 
on a formula that incorporates the average wage factor and years of 
contribution.
Although EBPS coverage has made notable progress in the past 
decade, increasing from 25% in 2010 to more than half of the work-
force, further expansion faces several hurdles. The labor force has been 
shrinking since 2018, while the number of retirees is increasing signif-
icantly. Slower economic growth may put a pressure on firms, which 
face high pension costs, to employ fewer high-cost workers. In addi-
tion, advances in technology, particularly artificial intelligence, may 
replace certain jobs, further complicating efforts to expand the formal 
employment sector. In addition to overall budgetary challenges (Sin, 
2005; Song et al., 2015), regional disparities in economic conditions 
pose a significant fiscal challenge for local governments (Li and Lin, 
2019).
To maintain fiscal sustainability of EBPS, the government
announced plans to gradually increase the pension eligibility age for 
formal workers in September 2024. The retirement age will increase 
from 50 to 55 for blue-collar female workers, from 55 to 58 for white-
collar female workers, and from 60 to 63 for male workers. Early or 
late retirement options, allowing flexibility of up to three years, will 
also be introduced. Although much progress has been made, significant 
inequality remains between formal and informal workers. Currently, 
the benefits provided by RURPS are only about 6% of those provided by 
EBPS. Therefore, further reforms are expected to address the financial 
sustainability of EBPS and the disparity between EBPS and RURPS.
To understand how pension reform options can affect the aggregate 
economy and household behavior, we conduct long-run simulation 
experiments using a quantitative model. Building on a heterogeneous 
agent model where households make endogenous choices of labor 
supply and consumption subject to idiosyncratic shocks and incomplete 
markets, the model is extended to allow features that match the salient 
characteristics of China, such as intergenerational transfers between 
generations, labor income processes that differ by formal and infor-
mal and formality-based public pension policy. The model is further 
extended to include long-run macro- and demographic trends, including 
population aging, productivity slowdown, and formalization of the 
population.
Our policy experiments are conducted in three steps. First, we eval-
uate the impacts of the delaying retirement policy announced in 2024 
on government budget, household savings, and labor supply. Second, 
we treat the new policy as the baseline and propose several options 
of further reforms as possible solutions to maintain long-term fiscal 
sustainability and alleviate the disparities between formal and informal 
workers. In the first option, we consider a change in pension indexation 
from a combination of full CPI indexation and partial wage indexation 
to CPI-indexation only. Option 2 involves an increase in the resident 
pension, i.e., a higher pension replacement ratio for the informal work-
ers. In option 3, we consider an alternative pension financing scheme 
where the current wage contribution rate of 16% for social pooling 
and 8% for individual accounts is replaced with individual accounts 
funded by consumption tax at the rate of 25%. In all experiments, we 
examine the impacts on aggregates, such as government fiscal balances, 
the impacts on welfare by formality, and the impacts on household 
behaviors such as labor supply, consumption, and savings. Finally, to 
shed further light on the role of model assumptions in shaping the 
results, we conduct robustness checks of policy impact on government 
budget and welfare along several dimensions: fertility rate projection, 
intergenerational transfers, long-run wage growth, internal returns of 
pension accounts, and preference parameters.
We show that the delaying retirement policy recently announced in 
September 2024 can significantly alleviate the issue of fiscal deficits 
in the next few decades. While the reform only modestly mitigates 
overall demographic trends by increasing employment by 30 million 
(6% of employment), it substantially affects the fiscal budget. To be
more specific, the pension deficit still grows, but the annual deficit will 
fall from 9.5% to 5.8% of GDP by 2075. Discounted using the market 
rate, the cumulative discounted present value (DPV) of the government 
balance will be lowered from 390% to 210% of GDP.
Among the three further reform options, we find that further remov-
ing wage indexation of pension benefits improves the welfare the most 
under our baseline specification. When pension benefits are indexed 
to CPI only, the government runs smaller deficits and thus can reim-
burse the saved revenue to households either in the form of lump-sum 
transfers or a reduced pension tax rate, under which agents make better 
intertemporal decisions when they are young. Raising pension benefits 
for informal workers redistributes from formal to informal workers, 
which inevitably worsens formal workers’ welfare. Yet, it still improves 
overall welfare for cohorts born before 2020 since informal workers 
have a higher marginal utility of consumption. The consumption tax 
financing scheme increases the disposable income for formal workers 
and equitably includes informal workers into the system. Despite its 
distortion to intertemporal decisions, it still improves the welfare of 
both groups in the long run. As these options address different aspects 
of the system, policy makers can consider a combination of them.
We perform thorough robustness checks along several dimensions 
of the model to verify the validity of the results. Under the low fertility 
rate projection, the government runs larger deficits, and the fiscal costs 
saved by further reform options are also expanded, leading to larger 
welfare effects. The presence of intergenerational transfers weakens 
the insurance value of public pension programs, in particular, for the 
informal workers, who rely more on the transfers from their children. 
As a consequence, removing intergenerational transfers leads to an 
overestimation of welfare gains of reforms, especially for informal 
workers. A lower long-run wage growth will decrease the contribution 
of the latter cohorts, exacerbating the pension fund deficits under a 
PAYG system and having an impact of welfare through its impact on 
the size of transfers and contribution taxes to facilitate the transition. 
A lower discount factor or a higher risk aversion imply a stronger 
incentive for agents to receive transfers or contribution tax cuts as 
young as possible, altering the welfare effects of several reform options 
as well.
Related literature and contribution. We make three contributions to 
the literature. First, we build a framework with incomplete market 
and endogenous savings and labor supply choices by heterogeneous 
households that suits the empirical background of China. We enrich 
the stylized model (İmrohoroğlu and Kitao, 2012; Kitao, 2014) in two 
dimensions: the large disparity between formal and informal workers 
and the long-run challenges faced by the public pension system due 
to the aging of the population and the slowdown of productivity. 
Previous literature on Chinese pension reform has highlighted the roles 
of elements such as endogenous fertility (Coeurdacier et al., 2014), 
rural–urban mobility (Bairoliya and Miller, 2021), and health (Deng 
et al., 2023), but they only focus on steady-state comparisons and, 
therefore, are not suitable for evaluating policy in a long-run tran-
sitional dynamic environment. An exception is (Song et al., 2015), 
which highlights the role of productivity growth in shaping the welfare 
effects between cohorts. Relative to Song et al. (2015), we incorporate 
richer elements such as formality-based inequality, intergenerational 
transfers, and long-run demographic and macro trends.
Second, we study the pension reform that was recently announced 
in September 2024 demonstrating the strong policy relevance of our 
study. We provide timely estimates on impacts of the reform and 
evaluate several routes for deepening the reform. Similar works have 
been carried out in countries such as the United States (Conesa and 
Krueger, 1999; İmrohoroğlu and Kitao, 2012), Spain Díaz-Giménez and 
Díaz-Saavedra (2009), and Japan (Kitao, 2014, 2015). Compared to 
them, we make policy proposals that are deeply rooted in Chinese 
characteristics—a representative emerging economy featuring large in-
equality and unsustainability of the public pension system in transition.
Economic Modelling 153 (2025) 107336
2

## Página 3

H. Gao and B. Lu
For example, the option to change pension benefits indexation is pro-
posed as a continuation of the reform previously implemented in 2005, 
and the option to increase resident pension is aimed at addressing 
the formality-based inequality that is unique in developing countries 
including China.
Lastly, we conduct thorough sensitivity checks along the dimen-
sions of various aspects of the model. Our results highlight the quan-
titative importance of incorporating elements with Chinese features 
such as fertility and intergenerational transfers (Banerjee et al., 2023; 
Choukhmane et al., 2023) and long-run productivity growth (Song 
et al., 2015). We also provide estimates of policy impact under alter-
native choices of pension account returns and preference parameters, 
establishing the quantitative validity of our results.
The structure of the paper is as follows. Section 2 provides a brief 
review of the transformation of the Chinese public pension system 
and raises the two key challenges facing it. Section 3 then presents 
an overlapping generations (OLG) model with long-run dynamics of 
demographic and macro trends. In Section 4, we use the model to 
project the future trajectory of the pension system in a pre-2024 reform 
scenario and compare it to the 2024 reform in terms of impacts on 
public finances and household decisions. Section 5 discusses the policy 
implications of the analysis and suggests several options to deepen the 
reform of the Chinese pension system. Section 6 checks the robustness 
under alternative assumptions of model elements such as fertility, 
intergenerational transfers, and long-run trends. Section 7 concludes.
2. The Chinese public pension system: Transformation and chal-
lenges
The Chinese public pension system has undergone several rounds 
of reform in recent decades that have fundamentally transformed the 
landscape of pensions in the country.2
From 1951, pensions, or ‘‘labor insurance’’—were provided on an 
unfunded basis by SOEs and collectively owned enterprises in urban ar-
eas, with a parallel Public Employee Pension scheme. Although finances 
were pooled at the local level during the 1980s, enterprises continued 
to be the source of funding, and the system was PAYG.3 However, 
the market transition and SOE restructuring increasingly made the 
enterprise-based model unsuitable for China’s needs.
In this context, the 1997 reform was a major milestone for China’s 
pension system, moving to a social insurance model for urban workers 
with a PAYG pooled defined benefit (DB) pillar and a defined contribu-
tion (DC) individual account (EBPS). Civil servants continued to have a 
parallel scheme. However, these schemes covered only workers in the 
formal urban sector and the public sector, leaving a major coverage gap 
for workers in the informal urban and rural sectors. Migrant workers 
were also not included in the early years of the urban workers’ scheme 
until the 2008 Labor Contract Law and the 2011 Social Insurance 
Law introduced an in-principle mandate for employers to pay their 
contributions (Meng, 2017). In addition to the core schemes for urban 
workers, firms were encouraged to provide enterprise annuities (sup-
plementary occupational schemes), and in recent years the authorities 
have promoted voluntary third-pillar private pensions. The other major 
development of the system was the introduction from 2009 of a unique 
hybrid scheme, first for rural workers and then urban informal workers, 
and now merged for the two groups, the RURPS. The scheme design 
combines elements of a matching defined contribution scheme (MDC) 
with an individual account, and a basic or social pension, and to our 
knowledge is unique in the world.
Coverage expansion has been substantial, both in the core EBPS and 
in the newer RURPS. As a result, by 2023, over 750 million workers —
2 See O’Keefe et al. (2025) for a detailed summary of the policy background 
on the evolution and current situation of the Chinese pension system.
3 See Fang and Feng (2018) for more details about the reforms.
over 80 percent of the working age population — were contributing 
to one of the country’s pension schemes. While significant progress 
has been made, two major challenges remain for the Chinese public 
pension system: fiscal unsustainability due to population ageing and 
large pension inequality between formal and informal workers.

### 2.1. Challenge 1: Population ageing

The first apparent challenge is the increasing dependency ratio due 
to population ageing. In Fig. 1(a), we plot the demographic process 
projected by the United Nations under the medium fertility scenario.
As Fig. 1(a) clearly shows, more than 15 million people will retire 
each year in the next 50 years. In particular, a massive increase in the 
number of pension fund recipients is projected to take place between 
2020 and 2030 as the baby boomers born in the 1960s start to retire. 
The next two spikes are projected to occur in the 2050’s and 2070’s. In 
Fig. 1(b), we plot the ratio of age 60 and 65 years of age above to the 
total population. As Fig. 1(b) shows, the share of the population over 
60 years of age was only around 10% in the early 2000s. In fact, the 
high growth in the past two decades has long been attributed to a low 
dependency ratio—the so-called ‘‘population dividend’’. Eventually, the 
share of seniors has increased rapidly. By the end of the century, around 
half of the population will be over 60 years of age.

### 2.2. Challenge 2: Rural-urban disparity

Another prominent feature of the Chinese economy is the wide gap 
between the rural and urban regions in terms of many dimensions, 
including labor market returns and opportunities for participation in 
social programs.
The key indicators for EBPS and RURPS as of 2023 are outlined 
in Table 1.4 The figures highlight the massive size of the Chinese 
pension system (easily the largest in the world) and the impressive level 
of coverage achieved, but also the major remaining gap in financial 
protection between workers in the urban formal sector and those in 
the rural and urban informal sectors.
By 2023, the EBPS program had 521 million participants and the 
RURPS program had 545 million participants. Although the govern-
ment has made efforts to promote universal coverage for all citi-
zens, the gap in pension between urban and rural populations remains 
significant.
According to the 2010 census, right before the RURPS was estab-
lished, only 10% of the rural elderly relied on public pension programs 
as their main source of income, which is in sharp contrast to the fact 
that 70% of the urban elderly received public pension. After the launch 
of RURPS, the public pension coverage for the rural elderly increased 
rapidly to 60% by 2018. However, the pension benefit level of RURPS 
still falls short compared to that of EBPS. As shown by Table 1, in 
the year 2023, the RP recipients, presumably mainly rural, received an 
amount of pension income that is only 6% of that of the EBPS recipients 
(2671/44,912). Compared to the generous benefit of the EBPS with a 
replacement ratio as high as 70% of wage income, the RURPS so far can 
only be considered as an old-age assistance to meet basic consumption 
needs.
For EBPS members, the generosity of pension benefits has declined 
over time. While average nominal benefits increased sharply during 
the first two decades of the century, the average replacement rate 
declined from a high starting point, falling rather sharply between 2000 
and around 2011, before stabilizing at around 45 percent of average 
wages during the subsequent decade (Fig. 2(a)). Although the Ministry
4 We categorize participants in the pension system into formal and informal 
groups regardless of rural or urban Hukou registration status. The formal sector 
includes those enrolled in EBPS, while the informal sector consists of RURPS 
members.
Economic Modelling 153 (2025) 107336
3

## Página 4

H. Gao and B. Lu
Fig. 1. Old age population over time.
Note: Data after 2023 are projected by World Population Prospects 2023 under the medium fertility scenario published by the United Nations.
Table 1
Disposable incomes, pension, and consumption by formality in financial year 2023.
Data source: 2023 Statistical Bulletin on the Development of Human Resources and Social Security.
 
Formal/EBPS
Informal/RURPS
 Population, million
521.21
545.22
Contributors
Population, million
379.25
372.54
 
 
Total contribution, billion CNY
70,506
6185
 
 
Annual ave. contribution, CNY
18,590
1660
Recipients
Population, million
141.96
172.68
 
 
Total benefits, billion CNY
63,757
4613
 
 
Annual ave. benefits, CNY
44,912
2671
Incomes/consumption
Annual disposable incomes, CNY
51,821
21,691
 
 
Annual wage incomes, CNY
31,321
9163
 
 
Annual business & farm incomes, CNY
5903
7431
 
 
Annual consumption, CNY
32,994
18,175
Notes: (i) Monetary variables are denominated in 2023 CNY. (ii) The average contribution is calculated per contributor, and 
the average benefit is calculated per benefit recipient. Variables in the income and consumption block, taken directly from 
the national bureau of statistics (NBS) of China, is denominated as per capita which includes all working and non-working 
population.
of Human Resources and Social Security(MOHRSS) had announced a 
target replacement rate of 59 percent of local average wage in 2005 
for someone with 35 years of contributions (Fang and Feng, 2018), the 
average replacement rate by the early 2020s was still above the ILO 
minimum guidance of 40 percent.
One driver of the steady decline in the average replacement rate 
has been the way EBPS pension benefits have been adjusted over time. 
China has no strict indexation formula, but both prices and wages 
are taken into account in pension adjustments.5 Fig. 2(b) shows the 
trajectory of adjustments for 2005–2020, with adjustments in nearly 
all years markedly below average wage increases but well above CPI 
changes and until 2017 usually above the mean of wages and prices.

### 2.3. The 2024 reform

To maintain fiscal sustainability, the 11th Session of the Standing 
Committee of the 14th National People’s Congress announcement was 
released in September 2024. Starting in 2025, retirement age will 
gradually be raised from 60 to 63 for men, from 50 to 55 for blue-collar 
women, and from 55 to 58 for white-collar women. Fig. 3(a) plots the
5 The 2005 reform changed the benefits formula from a multiplication of 
the target replacement ratio by the local average wage at retirement to a 
weighted average of the local average wage and the retiree’s life-cycle average 
monthly wage. The average monthly wage is similar to the average indexed 
monthly earnings (AIME) in the US pension system. See Salditt et al. (2007) 
and He et al. (2019) for more details of the 2005 reform.
change in retirement age under the 2024 reform. Furthermore, starting 
in 2030, the minimum vesting period will be raised from 15 to 20 years 
by 2040. Fig. 3(b) provides the details.
3. Model
We develop an overlapping generation model with long-run dy-
namics, incorporated with demographic and macro labour and capital 
prices. Our framework closely follows earlier literature in this field, 
such as Conesa and Krueger (1999), İmrohoroğlu and Kitao (2009, 
2012) and Kitao (2014) and extends their framework by introducing 
the formal and informal sectors and sector-contingent public pension 
system.
The model unit of analysis is the average of a representative house-
hold member, which takes the average of a man and a woman within 
the same household.6 Agents are heterogeneous with a permanent 
formality status, stochastic income shocks and endogenous wealth.7
6 Modeling individual as the decision unit apparently brings advantage in 
describing individuals with richer heterogeneity, such as gender, but it may 
still fail to account for the transfers across generations and across household 
members. See Gao (2025) for a model with costless transfers across generations 
and men and women household members.
7 We make this modeling choice because formality is tightly linked to local 
‘hukou’ status that is fixed for an individual over life. Most of the change in 
‘hukou’ status is achieved by acquiring more advanced education.
Economic Modelling 153 (2025) 107336
4

## Página 5

H. Gao and B. Lu
Fig. 2. EBPS pension benefits and indexation over time. Note: Data sources: (Wang and Feng, 2021), based on NBS, MOHRSS and State Council data.
Fig. 3. Retirement age and vesting years under the new policy announced in 2024.
Income and policies are contingent on the formality status of the indi-
viduals. The model is estimated to match the empirical data moments 
as of 2023.

### 3.1. Simulation of long-run dynamics

In order to project the long-run dynamics of the Chinese economy 
under different scenarios of policy reforms, we simulate the economy 
with the parameterization of the benchmark and the evolution of long-
run factors. In particular, we feed into the model the long-run trends 
in three main aspects: (i) demographics, including the population size 
of cohorts and conditional survival probability by age; (ii) population 
share by formality; (iii) prices, including the interest rates and wage 
growth rates. We further assume that the infinitely-lived government 
has commitment to policies for each cohort, so that each individual acts 
as if they have perfect foresight of policies throughout their lifetime.
The time-varying factors mean that agents of different cohorts are 
faced with different parameters to make life-cycle decisions. Given 
cohort-specific parameters, we solve the life cycle optimization problem 
for each cohort, simulate the life cycle of each cohort, and aggregate 
up cohorts coexisting in a given year with proper weights induced 
by the demographic process to construct time series of variables. The 
government’s pension policies may also change over time, conditional 
on the policy scenario we consider.
As the problem for an individual is cohort-specific, in the following 
presentation of the model, we drop the time subscript in the problem 
and describe the problem from the perspective of a life cycle. For the 
sake of space, we delineate the environment of the model and delegate
the details of the recursive problem of individuals and the calibration 
of the model parameters and the corresponding moments to Section A 
of Online Appendix.

### 3.2. Demographics

The economy is populated by overlapping generations of individu-
als. Individuals enter the economy at age 1 and face uncertainty about 
their lifespan. The conditional probability of survival from age 𝑗 to age 
𝑗+ 1 is denoted 𝜓𝑗. The maximum possible age is 𝑗= 𝐽, with 𝜓𝐽= 0. 
The size of the cohort is given exogenously. Individuals derive utility 
from leaving a bequest at death, denoted (.). Bequests are assumed 
to be collected and distributed as a lump sum transfer to the entire 
population. Individuals enter the economy with no assets except for 
the transfer of the lump sum bequests.
Upon entering the labor market, an individual is associated with a 
state of informality 𝑠∈{1, 2} that is fixed for an individual throughout 
the life cycle. 𝑠= 1 refers to the informal sector and 𝑠= 2 refers 
to the formal sector. Workers in different sectors differ in their labor 
productivity and in the public pension system that they enroll. Our 
choice of modeling formality status as a permanent state is motivated 
by Chinese data that formality status is tightly linked to one’s education 
and urban household registration status, which makes formality status 
very predictable and also unlikely to change over the life cycle.8 The 
share of the formal population in a cohort is given exogenously. As will
8 Esteban-Pretel and Kitao (2021) use a search and matching framework to 
model worker transition across the formal and informal sectors over the life
Economic Modelling 153 (2025) 107336
5

## Página 6

H. Gao and B. Lu
be clear in the projection section, formality has gradually increased to 
around 50% in 2024 and is projected to continue increasing. To account 
for this fact, we assume that the formal population share is gradually 
increasing from older to later cohorts. Over time, older cohorts with a 
higher informal share exit and younger cohorts with a higher formal 
share enter; this drives the increase in overall formality.

### 3.3. Preferences

Without further information on the heterogeneity of preferences 
between formal and informal workers, we assume that all individuals 
share the common preference structure and have the same parameters. 
Individuals maximize the expected utility function over sequences of 
utility flow 𝑢(.) over consumption and leisure {𝑐𝑗, 𝑙𝑗
}𝐽
𝑗=1 and warm-glow 
bequest utility (.) over assets 𝑎𝑗:
E{
𝐽
∑
𝑗=1
𝛽𝑗−1(
𝑗−1
∏
𝑎=0
(1 −𝜓𝑎))[(1 −𝜓𝑗)𝑢(𝑐𝑗, 𝑙𝑗
) + 𝜓𝑗(𝑎𝑗)]},
(1)
where 𝛽 is the discount factor. The expectation is taken with respect to 
the stochastic processes governing idiosyncratic labor productivity.
We assume that the flow utility takes Cobb–Douglas functional form:
𝑢(𝑐, 𝑙) = (𝑐𝛾𝑙1−𝛾)1−𝜎
1 −𝜎
where 𝜎 is the risk aversion of households and 𝛾 is the utility weight 
of consumption.

### 3.4. Incomes, intergenerational transfers, and budget constraint

The markets are incomplete, and there are no state-contingent 
assets to insure against the idiosyncratic labor income and mortality 
risks. Individuals can, however, imperfectly self-insure against risks by 
accumulating one-period risk-free assets. Individuals are not allowed to 
borrow against future income and transfers, i.e., 𝑎𝑗≥0 for all 𝑗.
Each individual can allocate one unit of disposable time to leisure 
(𝑙) or market work (ℎ). Individuals’ earnings are given by 𝑦𝑤=
̃𝑤ℎ, 
where ̃𝑤 denotes the wage rate per work hour ℎ for each individual 
and is given as
log ̃𝑤= 𝜔+ 𝜃𝐴
𝑗+ 𝜃𝑆
𝑠+ 𝜃𝐸
𝑖𝑗,
where 𝜔 is a general equilibrium wage component, 𝜃𝐴
𝑗 is the age 
component, 𝜃𝑆
𝑠 is sector labor productivity, and 𝜃𝐸
𝑖𝑗 is an idiosyncratic 
wage income shock that evolves stochastically. The wage income is 
therefore given as 𝑦𝑤= ̃𝑤ℎ.
Adult children in China — as well as in many other developing 
countries — are supposed to provide financial support to their parents. 
As the private transfers constitute a major part of old-age support 
in particular for the rural population who have low public pension 
benefits, we explicit model the intergenerational monetary transfers to 
account for the potential role of private transfers for policy effects. We 
denote the transfers made by an agent to her parent generation as 𝑦𝑚
and the transfers received from her child generation as 𝑦𝑟.
As we do not explicitly model the fertility process, therefore, the 
identity of parent and children generations, we assume that agents are 
children of the generation born 25 years ahead of them. Agents make 
transfers to their parents once they enter the labor market (age 20) 
and until the parent generation completely exits the economy (age 75). 
Agents receive transfers starting from age 45 — when their children 
generation enter the economy — to the end of their life. The size of 
the transfers made is proportional to their income, which is affected by 
the age and formality status of the agent. The size of transfers received
cycle. Gao and McKiernan (2023) further endogenize job arrival rates with a 
firm vacancy posting problem.
is computed by dividing the total amount of transfers made by their 
children generation by the size of the cohort.
Assets evolve according to the law of motion:
𝑎′ + 𝑐= 𝑎(1 + 𝑟) + 𝑦𝑤+ 𝑦𝑏+ 𝑦𝑟−𝑦𝑚−T
(2)
where 𝑦𝑏 denotes public pension income and T denotes the sum of all 
taxes. Individuals are not allowed to borrow against future income and 
transfers, i.e., 𝑎𝑗≥0 for all 𝑗.

### 3.5. Public pension system

To model the two-tier pension system in China, we assume that the 
government operates a pay-as-you-go pension system that covers only 
formal workers and an old-age pension system that covers informal 
workers.
Formal sector. A proportional public pension contribution tax 𝜏𝑠𝑙 is 
imposed on the earnings of formal workers until age 𝐽𝑅−1., Agents 
start to receive public pension benefits once they reach retirement age 
𝐽𝑅.
To approximate the Chinese pension system, we introduce the cu-
mulative pension contribution 𝑏 as a state variable to the problem of 
the household. 𝑏 evolves over the life cycle and determines the level of 
pension benefits after retirement. In every working period, the existing 
cumulative contribution stock grows at the market deposit rate 𝑟 and 
the formal workers make contributions that are 𝜏𝑠𝑙 fraction of wage 
income, i.e.,
𝑏𝑗= (1 + 𝑟)𝑏𝑗−1 + 𝜏𝑠𝑙𝑦𝑤.
(3)
The pension benefit that an individual receives is contingent on con-
tribution 𝑏𝐽𝑅, i.e., total pension contributions made up till age 𝐽𝑅. 
Under the current rule, contributions will be deposited into a social-
pooling and an individual account by a fixed fraction, and the benefit 
is calculated as the sum of withdrawals from the two accounts. The 
social pooling account is redistributive and the individual account is 
only tied to the total contribution made. To capture the fact that the 
current pension system depends on both the contribution years and the 
total contribution and is redistributive in nature, we approximate the 
benefit in the first year of retirement as
𝑦𝑏= 𝛽1𝐽𝑅+ 𝛽2𝑏𝐽𝑅
(4)
With specification (4), we implicitly assume that the social pooling and 
individual accounts have the same internal rate of returns.
Based on the formula of pension benefits, pension income is effec-
tively fully indexed to price changes but only partially indexed to wage 
growth. For current cohorts, we assume that the benefit level increases 
by 2% per year in addition to inflation, which is consistent with 
evidence of Fig. 2. We further assume that the growth rate gradually 
decreases to 1% in the long run, due to the slowdown of aggregate wage 
growth. We calibrate the parameters 𝛽1 and 𝛽2 to match the average and 
the interquantile gap of the public pension benefits paid in the year 
2023.
As there is no ex-ante heterogeneity for agents within the formal 
sector, we assume a common retirement age for all formal workers. We 
set it to be age 56, which is the average effective retirement age before 
2023.9 For simplicity, we assume that formal workers retire once they 
reach the pension eligibility age and there is no recall after retirement.
9 Apparently, age 56 is calculated by pooling population who are eligible 
for different retirement ages (50, 55, or 60 for policy before 2023). See Gao 
(2025) for a framework that evaluates the effects of the policy for individuals 
with different characteristics.
Economic Modelling 153 (2025) 107336
6

## Página 7

H. Gao and B. Lu
Informal sector. We assume that informal workers start collecting pen-
sion benefits at the same age at a fixed age of 60. The informal workers 
may continue to work while collecting the old age pension benefits. 
The maximum age at which an informal worker can work is 65 years 
and is independent of their pension eligibility age. The informal worker 
can change their labor supply at older ages in response to changes in 
their pension policy. This allows us to study the response of informal 
workers’ labor supply at older ages to policy reforms.
Under current policy, informal workers are only eligible for old-
age assistance programs that have much lower benefit levels compared 
with their formal peers. We assume that informal workers contribute 
2.5% of their wage income to the RURPS before retirement and receive 
pension benefits that are 6% of the average pension income of EBPS 
pension recipients. These numbers reproduce in the model the average 
contribution for RURPS participants before retirement and the average 
benefit level after retirement in 2023 as in Table 1.

### 3.6. Fiscal policy

The government spends an exogenous amount of 𝐺 on public pur-
chases of goods and services and issues one-period riskless debt 𝐷′, 
which pays the annual interest rate of 𝑟. In addition to payroll pension 
contribution taxes, revenues are raised from taxation on wage income, 
capital income, and consumption. The wage income tax schedule 𝜏𝑤(.)
is progressive and is applied to all workers. Capital income and con-
sumption are taxed at proportional rates, each denoted as 𝜏𝑎 and 𝜏𝑐, 
respectively. The government budget constraint is satisfied for every 
period:
∑
𝜒
[𝜏𝑠𝑙𝑦𝑤(𝜒) + 𝑙(𝑦𝑡(𝜒))]1[𝑠=2]𝜇(𝜒)
+
∑
𝜒
[𝑟𝑎(𝜒)𝜏𝑎+ 𝜏𝑐𝑐(𝜒)]𝜇(𝜒) + 𝐷′ = 𝐺+
∑
𝜒
𝑤𝑟(𝜒)𝜇(𝜒) + (1 + 𝑟)𝐷
(5)
where the taxable income 𝑦𝑡(𝜒) = 𝑦𝑤(𝜒) −𝜏𝑠𝑙𝑦𝑤(𝜒) for formal workers 
captures the fact that the pension contribution is tax deductible, and 
𝑦𝑡(𝜒) = 0 for informal workers, i.e., informal workers do not pay 
personal income taxes. This choice of modeling is motivated by the fact 
that the personal income tax in China constitutes a very small source 
of government tax revenues.10

### 3.7. Parameterization and model fit

We set the risk aversion parameter 𝜎= 4 and set the discount factor 
𝛽= 0.96 such that the capital-to-output ratio is 1.6 as in the data. We 
set 𝛾= 0.4 to match the mean work hours. As in Choukhmane et al. 
(2023) and Banerjee et al. (2023), we assume that transfers made to 
their parents amount to 9% of income for both formal and informal 
workers.
The statutory contribution is 24% of the wage, based on the social 
pooling 16% and the individual accounts 8%. However, since self-
employed members only contribute 12% to social pooling accounts, 
and compliance is significantly below perfect, we calibrate the effective 
contribution as 21% of wage income that reproduces the national 
account statistics reported in Table 1.11 The current pension benefit in
10 According to the State Administration of Taxation of the People’s Republic 
of China, over 70% of Chinese wage earners are exempted from individual 
taxes, and only around 10% of the wage earners pay income taxes above 
the 3% marginal rate. See https://www.chinatax.gov.cn/chinatax/n810219/
n810780/c5235243/content.html for more details.
11 According to The Report on the Inspection of the Implementation of the
Social Insurance Law of the People’s Republic of China by The National Peo-
ple’s Congress Standing Committee Law Enforcement Inspection Group, The 
compliance rate of employee pension insurance (the proportion of contributors 
to insured persons) was 80.8% in 2022.
terms of the replacement rate at retirement is 50% of the average wage; 
the pension is indexed to the real wage growth, which is 2%.
In Table 2, we present the fit of the model in the cross section of 
2023. As the upper panel of Table 2 shows, our model provides good 
fitness of the levels of earnings, consumption, pension contribution, and 
benefits. In the lower panel, we further present distribution moments, 
including the standard deviation of log earnings and wages, and the 
mean household net savings rate. In the data, the overall dispersion 
of earnings and wages is larger than that by group, which is also well 
captured by our model. Our model correctly predicts that the savings 
rate for informal workers is lower than that of formal workers, which 
is consistent with the data. However, the level is lower than that in the 
data. This suggests that our model may miss some factors that affect the 
incentive to save for Chinese households.12 Despite its vital importance, 
explaining the savings puzzle of Chinese households by projecting the 
long-run trend of asset prices is challenging and far beyond the scope of 
our studies. As an alternative approach, we perform sensitivity checks 
with alternative values of preference parameters to investigate the role 
of the savings incentive in the following sections.
4. Long-run projections of policy reforms
To project the trends of variables from 2024 to 2100, we consider 
157 cohorts, starting from the cohort entering the labor market in year 
1944 (born in 1924) and ending the life cycle in year 2024, to the 
cohort entering the labor market in year 2100. In 2021, the population 
of China reached its historical peak of 1.412 billion. We only model 
the population above the age of 20, which is around 76% of the total 
population (1.08 billion).

### 4.1. Inputs of long-run factors

We take the projection of the population size by age for each 
cohort directly from the World Population Prospects 2024.13 We use the 
projection in the medium fertility scenario as our baseline and check 
the robustness of the results in other scenarios..14 Fertility rates from 
1950 to 2023 are taken directly from data. Recent years have seen a 
historically low fertility rate, hitting less than 0.9 births per woman. 
The WPP projects that the fertility rate will gradually recover to 1.35 
by 2150.
Motivated by the fact that the formality share is largely affected by 
the urbanization process, we assume that the formality share by region 
is a constant over time and project the urban population share over 
time using experience from countries with comparable backgrounds. 
As shown in Fig. 4(d), the share of urban population in 2023 was 64%. 
It is projected to rise to 80% in 2045 and further to 90% in 2072. 
Assuming that 80% of the urban population is formal and 30% of the 
rural population is formal, we obtain that the share of formal employees 
in the total working population is projected to reach 70% by 2050 and 
stabilize at the level of 80% after 2075.
The real wage growth up to 2023 is extracted from the National 
Bureau of Statistics website and is projected to be reduced to 2% 
by 2050 and then to remain constant thereafter. In Section B of the
12 For example, we only consider the general form of asset holding, while 
the housing boom in China plays a key role in shaping the rapidly increasing 
trend of the household savings rate, particularly in the urban sector (Chamon 
and Prasad, 2010; Wang and Wen, 2012; Chen and Wen, 2017).
13 Data can be found at https://population.un.org/wpp/.
14 According to definition of WPP, ‘‘the medium scenario projection corre-
sponds to the mean fertility and mortality and median net migration of several 
thousand distinct trajectories of each demographic component derived using 
the probabilistic model of the variability in changes over time. Prediction 
intervals reflect the spread in the distribution of outcomes across the projected 
trajectories and thus provide an assessment of the uncertainty inherent in the 
medium scenario projection’’.
Economic Modelling 153 (2025) 107336
7

## Página 8

H. Gao and B. Lu
Table 2
Model fitness: Cross-section of 2023.
 
Data
Model
 
All
Informal
Formal
All
Informal
Formal
 Annual earnings per worker, CNY
69,429
51,875
88,524
68,042
46,373
90,490 
 Consumption per worker, CNY
18,175
32,994
27,100
38,444 
 Pension contribution per worker, CNY
1660
18,590
1325
19,003 
 Pension benefit per retiree, CNY
2671
44,912
2645
44,777 
 S.d. of log wage
0.71
0.65
0.58
0.41
0.33
0.30  
 Net saving rate
0.30
0.16
0.36
0.14
0.10
0.16
Fig. 4. Model inputs for projection.
Online Appendix, we provide more details on the data sources and the 
imputation and forecasting of these variables.
In the following, we start with the scenario before the newly-
announced reform in October 2024, and then examine the effects of the 
reform by comparing the outcomes under the new policy with those 
under the scenario that the old policy is continued into the future. 
Next, we examine the effects of several policy proposals that aim to 
achieve better fiscal sustainability and reduce inequality among formal 
and informal workers. In all experiments, we study the impact of policy 
on household welfare and household behaviors, including consumption, 
savings, and labor supply, and the impact on the government fiscal 
budget.

### 4.2. Effects of the 2024 reform

Since we treat the average household member as the unit of eco-
nomic analysis in the model, we take the average retirement age 
proposed by 2024 over men and women to approximate the effect of 
the reform. Fig. 5 plots the change in retirement age over time in the 
model.15 Also note that our formulation (4) captures the policy effect 
that the annual pension income increases as agents’ contribution years 
increase.
Not surprisingly, the increase in retirement age increases the size 
of the labor force, as shown by Fig. 6(a). By 2037, the labor force is 
projected to increase by 40 million and remain stable in the next couple 
of decades. The change in retirement age reduces the dependency ratio 
from around 1.6 to 1.5 in 2050, as shown in Fig. 6(b).
15 As in the benchmark policy, we compute the average retirement of the 
population. In reality, the average retirement age, which does not necessarily 
take an integer value, will increase year by year. However, since our model 
period is a year, we can only approximate the gradual increase as a step 
function.
Fig. 5. Retirement age in the model.
In Fig. 7, we plot the net public pension budget in the current year 
and in cumulative terms up to 2065. In both panels, the blue solid 
lines refer to the projection under the scenario of continuing the policy 
before the 2024 reform, and the red solid lines refer to the projection 
under the 2024 reform.
As is consistent with the data, the Chinese public pension budget 
still ran slightly a net surplus in 2023. As our projection shows, it 
quickly runs into a net deficit by 2025. By 2065, the net pension 
deficit of the pre-reform scenario is projected to reach approximately 32 
trillion CNY in 2023 prices, equivalent to 12% of GDP in that year. We 
compute the discounted present value of debt using the market deposit 
rate, the interest rate given in Fig. 4(e). The cumulative net deficit of 
the public pension system is expected to be 110% of GDP in 2023 by 
2050 and 270% of GDP in 2023 by 2065.
Economic Modelling 153 (2025) 107336
8

## Página 9

H. Gao and B. Lu
Fig. 6. Impact of the 2024 reform on the size of labor force.
Fig. 7. Impact of the 2024 reform on government revenue.
Note: The cumulative present value of public pension deficits is discounted using the market deposit rate.
Despite the increase in annual pension income after the reform, 
the reform greatly reduces the financial burden, as the overall effect 
is dominated by reduced public pension reception years. As the red 
line in Fig. 7 clearly shows, the 2024 reform can prolong the net non-
deficit period into the 2030s. Furthermore, the 2024 reform will reduce 
the annual public pension deficits from 12% of GDP to 8% and the 
cumulative discounted present value of deficits by around half by 2065.
One may wonder what contribution rate can prevent the govern-
ment from running a deficit in the long run. We find that under our 
assumption of the benchmark scenario, the government has to impose 
a 36% contribution rate to maintain ‘‘revenue balancing’’ of the pension 
system over the long run, i.e., up to 2100. Given that the direction 
of contribution rate adjustments in the past decade has been largely 
downward, this seems both unlikely and undesirable from a labor 
market perspective, both in terms of the global competitiveness of 
Chinese urban workers and in terms of the extent of distortions between 
factors of production within China.
Through the lens of the model, the aggregate savings rate will 
respond to all three trends—the demographic, employment, and growth 
trends if the old policy is continued. First, as the formal population 
share continues to increase, it can mechanically decrease the aggregate 
savings rate, as formal workers have a lower savings rate relative to 
their informal peers, since they have better social insurance. Second, 
the ageing process may lead to mechanical shifts of population compo-
sition and behavioral responses through life cycle re-optimization. On 
the one hand, the aging process increases the share of retired in the 
population. This tends to decrease the savings rate, as retirees are net 
negative savers. On the other hand, given a fixed retirement age, the
ageing process means each individual has longer retirement periods to 
finance, which will incentivize agents to save more in their early life. 
Third, the slowdown of wage growth, as reflected by the changing age 
profile for different cohorts, will affect agents’ incentive to save as well.
The impact on the aggregate savings rate is apparently the result of 
all these factors. As the blue line in Fig. 8(a) shows, the savings rate 
increases slightly over the next 15 to 20 years, mainly due to a decrease 
in aggregate growth. In the long run, the savings rate decreases as the 
increase in the share of the formal and retired population dominates.
We further investigate how the 2024 reform may affect the savings 
rate. The 2024 reform may affect the formal workers’ savings incentive 
through three channels. First, it increases the ratio of working time rel-
ative to retirement time for an individual, or alternatively, it increases 
the ratio of the employed population to the retired population, which 
increases the aggregate savings rate. Second, since each individual 
expects to work for longer periods to accumulate enough assets for 
retirement, they may save less in each period. Third, though the benefit 
rule adjusts for longer contribution years, it on net is still a decrease 
in pension wealth. Using several earlier reforms of the Chinese pension 
system as quasi-experiments, Feng et al. (2011) and He et al. (2019) 
find that a decrease in pension wealth has led to more household 
savings and labor supply. As the red line in Fig. 8(a) shows, relative 
to the pre-reform scenario, the savings rate slightly decreases in the 
long run.
In addition, we examine the trend of aggregate working hours 
under the scenario of old policy and the 2024 reform. In Fig. 8(b), we 
report the ratio of aggregate labor supply under the 2024 reform to 
that under the case without reform. As Fig. 8(b) shows, the aggregate
Economic Modelling 153 (2025) 107336
9

## Página 10

H. Gao and B. Lu
Fig. 8. Impact of the 2024 reform on household savings rate and aggregate labor supply.
working hours increase by up to 6% by 2050, and the increase is mainly 
explained by an increase in employment (the extensive margin) as 
shown in Fig. 6(a).16 Fig. 8(b) also shows that the reform decreases the 
average working hours despite increasing total employment, as shown 
in Fig. 6(a). This is also mechanical, as the delaying retirement policy 
increases the amount of older workers, who are associated with lower 
hours. The trend of total working hours is driven by the extensive 
margin, that is, the increase in labor force participation.
5. Further reform options
To address the main challenges documented in Section 2, namely, 
fiscal unsustainability due to ageing and the wide gap between formal 
and informal workers, we evaluate several potential follow-up policy 
proposals. The first proposal aims to enhance fiscal sustainability of the 
formal pension system, therefore only involving the change of policies 
for formal workers. The last aims to alleviate disparity by formality and 
the last proposal aims to address both inequality and unsustainability 
issues.
For each policy proposal, we consider two ways of implementation. 
First, we simply change the public pension policy without rebalancing 
the government budget using other policy tools. This gives us a sense 
of how the policy would affect the fiscal budget on its own. Second, we 
ensure that the government budget is rebalanced in the long run with 
either lump-sum transfers or tax reimbursement to examine the welfare 
effects of the policy reforms. The reference point for the government 
balance is the accumulated government debt by the year 2100 under 
the scenario that the 2024 new reform is implemented.
For each reform, we assume that the reform starts to take place 
from 2025 and that the government has a commitment to the pension 
wealth accumulated before 2025. To be more specific, cohorts that have 
retired before 2025 collect pension benefits with the rule under the 
2024 reform; cohorts that have already started working, but not yet 
retired, have two phases of pension wealth accumulation. Therefore, 
each cohort may be affected by the policy reform to a different extent, 
and it takes full working years of a life cycle to see the cohort that is 
covered by the new policy over his/her all life.

### 5.1. Reform options

1. Alternative indexation of pensions in payment In the first
scenario, we propose further altering the indexation of pension 
benefits from the baseline, which is partially indexed to real
16 The average hours change to a small extent, slightly increasing in the 
short run but eventually decreasing in the long run, mainly driven by the 
compositional effect that the share of informal workers decreases.
wage growth, to a one that is indexed to CPI only. The current 
policy guidelines allow indexation based on a range between 
price, wage, and GDP growth. The CPI indexation usually repre-
sents a minimum indexation scenario, which shall significantly 
reduce the benefits when the retirees age. In the model, we 
simply set the agent’s pension income to be fixed at the level 
given by Eq. (4).
2. Increasing level of residents’ pension To address the pension
inequality between formal and informal workers, we evaluate 
how increasing the level of benefits for informal workers can add 
to the financial burden of fiscal sustainability. Earlier studies, 
such as Jung and Tran (2012), show that extending public 
pension coverage to informal workers leads to welfare gains 
by providing better insurance to disadvantaged groups despite 
potential efficiency losses. To proceed, we set the contribution 
to be the same as in the baseline but increase the replacement 
ratio from the current level of 6% of the formal pension ben-
efit to 30%, or equivalently 2% of GDP per capita to 15% of 
GDP per capita, which is more consistent with the prevailing 
international practice (Chomik et al., 2024). Increasing pension 
benefits can potentially lead to better outcomes for the informal 
population in many other dimensions, such as better health, 
as shown by Huang and Zhang (2021). In this paper, we limit 
our exploration only up to consumption and labor supply of 
households and leave the exploration on health consequences 
for future research.17 In practice, the government can consider 
richer way of implementing the policy such as means-tested 
pension benefits as considered in Wheadon et al. (2024).
3. Consumption tax based financing The final option that we
model is to replace the contribution of the effective 21% of 
pre-tax wage with a post-tax consumption contribution rate of 
𝜏𝑠𝑐
=
25%. Similar proposals have been made in countries 
such as Mexico (Hernández et al., 2017) and Germany (Ruppert 
et al., 2024). By using consumption tax instead of a payroll tax, 
the link between formality and public pension contribution is 
weakened, in the sense that the consumption tax-based public 
pension system is able to cover the entire population regardless 
of their formality status. Furthermore, we assume that the old 
age resident pension for the informal sector gradually phases out 
as the consumption tax gradually phases in.
We further assume that all contributions go to an individual 
account but up to a notional base without considering the fiscal
17 To evaluate the welfare consequences through health, one will need a 
framework as in Deng et al. (2023).
Economic Modelling 153 (2025) 107336
10

## Página 11

H. Gao and B. Lu
Fig. 9. Impact of further reform options on government revenue, ratio to 2023 GDP.
transition cost.18 In the model, the state variable of pension 
contribution then evolves following
𝑏𝑗= (1 + 𝑟)𝑏𝑗−1 + 𝜏𝑠𝑐𝑐.
(6)
By assuming that the return is the same as the average return 
under the current policy, we obtain the formula for benefit level 
as
𝑦𝑏= ̃𝛽2𝑏𝐽𝑅
(7)
where ̃𝛽2 is the factor that matches the mean benefit level 
given the total contribution in the data of 2023. Relative to (4), 
specification (7) apparently does not feature redistribution.

### 5.2. Impact on government budget

First, we examine the impact of policy reforms on the government 
budget. In evaluating the impact of the policies, we assume that there 
are no accompanying tax or transfer policies. We plot the impacts on 
the government budget in the current year as a share of GDP in Fig. 
9(a) and on the cumulative government budget in Fig. 9(b). In both 
panels, the benchmark scenario without further reforms is plotted in 
solid blue lines.
We first evaluate how the proposed policy change would affect the 
fiscal budget without accommodation of other policy changes. As the 
dashed lines in Fig. 9(a) show, indexing the benefits to the CPI only 
reduces the deficits to 4% of GDP by 2075. In terms of the accumulated 
government budget, it reduces the fiscal deficit from 250% of GDP to 
200% in 2065. As the green lines with circle markers in Fig. 9 show, 
increasing the level of resident pension benefit for informal workers 
from 6% of the average formal pension income to 30% of the average 
formal pension income will increase the public finance deficit to 7% 
of GDP in 2075 at prices of 2023, with accumulated debt reaching 
320% of GDP of 2023 compared to 250% in the baseline scenario. 
However, due to the foreseeable decrease in the share of informal 
workers, further increasing the benefits for informal workers does not 
add too much of a fiscal financial burden. The consumption tax case 
is trickier, as it involves both a decrease in the contribution and the 
payout of the pension benefits. As a result, in the first two decades 
of consumption tax-based contribution, it exhibits a deficit similar to 
the 2024 reform scenario in the first stage, as existing pensioners
18 We only analyze the economic impact of the policy reform with the 
assumption of full commitment and perfect information. Further exten-
sion to consider behavioral responses subject to information frictions in 
implementation such a policy, though, is beyond the scope of our analysis.
still receive high benefits, as the purple lines with triangle markers 
Fig. 9 show. However, by around 2065, the accumulated reduction in 
expenditures exceeds the revenue gap compared to the normal wage-
based contribution scheme, leading to a smaller budget deficit. By 
2075, the consumption tax reduces the annual government deficit to 
less than 4% of GDP and the cumulative deficit would drop to 210% of 
GDP in 2023.

### 5.3. Impact on welfare

Welfare calculation. In the previous subsection, we focus on the impact 
of alternative reform schemes on the government budget by being 
agnostic about how the government raises the funds to finance the extra 
deficits or spend the extra revenue. In order to compare welfare across 
the schemes, we need to hold the government budget fixed and make 
assumptions on how the extra revenues are raised/distributed.
We assume that the government can use lump-sum transfers or 
adjust the pension contribution rate to maintain the same deficit level 
as under the policy environment of the 2024 reform, i.e., the deficit 
of government fiscal revenue to GDP ratio is 300% by year 2100. We 
further assume that the size of the lump-sum transfer is indexed by 
the average wage level by year and will be applied to all individuals 
regardless of their age and formality status. This effectively introduces 
redistribution across the formal and informal workers as they have 
different income levels. In addition, it also leads to redistribution for 
individuals at different stages of life. Another way of rebalancing the 
long-run government budget is to change the contribution rate, which 
is easier to implement compared to lump-sum transfer in practice, but is 
not compatible with all reform options. For example, when we want to 
replace the payroll tax with the consumption tax (option 3). Therefore, 
we consider lump-sum transfer as the benchmark implementation for 
all cases and consider alternative implementation of changing contri-
bution rate for options 1 and 2. The choice of lump-sum taxes/transfers 
is intended for ease of interpretation and no distortion to individuals’ 
decision-making. Apparently, a more complicated way of controlling 
the aggregate fiscal budget under alternative assumptions, such as 
taxing or redistributing to specific households, may produce different 
outcomes. The lump-sum tax/transfer approach serves as a simplified 
basis for comparison.
The government would run a surplus relative to the benchmark 
in several cases. When the pension benefits are indexed to inflation 
only, the government would reimburse households with annually 3098 
CNY at the wage level of year 2023. Alternatively, the government 
can reduce the pension contribution rate from 21% to 13.5%. The 
government runs a deficit if the replacement rate of informal workers’ 
benefits is raised. In this case, the government imposes a 1269 CNY
Economic Modelling 153 (2025) 107336
11

## Página 12

H. Gao and B. Lu
Fig. 10. Overall welfare change under further reform options.
lump sum tax on all households at the wage level of year 2023. For 
more details on the compensation that government needs to make to 
maintain government budget position as in the benchmark by 2100, 
see Section C of the Online Appendix.
Following Conesa et al. (2009), we measure welfare using Consump-
tion Equivalent Variation (CEV), which quantifies changes in average 
lifetime utility as the percentage change in consumption needed to 
make individuals indifferent between a baseline policy and an alterna-
tive policy scenario. To be more specific, given the form of the utility 
function, the welfare consequences of switching from a steady-state 
consumption-labor allocation (𝑐0, 𝑙0) to (𝑐∗, 𝑙∗) are given by
CEV = [ 𝑊(𝑐∗, 𝑙∗)
𝑊(𝑐0, 𝑙0) ]
1
𝛾(1−𝜎) −1
where 𝑊(𝑐, 𝑙) is the expected lifetime utility at birth of a household, 
given a policy system.
The aggregate social welfare is assumed to be ex ante utilitarian 
utility that weights each individual equally, in spite of their formality 
status, i.e.,
𝑆𝑊𝐹() = ∫𝑉(𝑎= 0, 𝑠, 𝑗= 1|)𝑑𝜇(),
where  refers to a set of government public pension and lump-sum 
tax/transfer policies, 𝜇 is the distribution of agents, and the value 
function 𝑉(𝑎= 0, 𝑠, 𝑗= 1|) refers to agents’ ex-ante utility when they 
enter the labor market. Using a similar way, we can also define welfare 
change for a permanent group—in our specification, the formal and 
informal sectors, with the CEV of the ex-ante utility.
Results. Fig. 10 presents the overall welfare changes. The 𝑥-axis lists 
the cohorts by their year of birth, and the 𝑦-axis represents the changes 
in welfare for each cohort. As Fig. 10 demonstrates, for cohorts born 
after 2000, the scenario of CPI indexation only reimbursed with lump-
sum transfers provides the most substantial welfare gains—amounting 
to 4% increase in annual consumption. The increase in the informal 
replacement rate or the use of the consumption tax also records a 
welfare gain of 2% CEV in the short run. For future cohorts born after 
2010, while all other scenarios present flat welfare gains, the gains from 
increasing resident pension option diminish to slightly negative for the 
cohort born in 2040.
As policy reforms may affect the formal and informal sectors dif-
ferently, in Fig. 11, we report welfare changes for the formal and 
informal sectors using the same assumptions as in the construction of 
Fig. 10. Also note that the weights of the aggregate welfare function 
over the two sectors are changing by cohort based on our projection of 
the formalization process, where the formal sector is expected to grow 
rapidly in the next decades, but stabilize in the long run.
As the solid lines with triangle markers in Fig. 11(a) show, indexing 
pension benefits to the CPI only leads to welfare gains for both the 
informal and formal sectors, with an overall effect of approximately 
2% for the cohort born in 1980 and around 4% for the cohort born 
in 2040. Not surprisingly, since the lump-sum transfer is independent 
of workers’ formality status, the informal workers experience a more 
substantial welfare gain relative to their formal peers. However, this 
policy also leads to better outcomes for the formal population in spite of 
a loss of pension wealth. This is because a lump-sum transfer at younger 
ages helps agents make better intertemporal decisions over the life 
cycle. When agents are young, they are subject to liquidity constraint; 
the lump-sum transfer received at younger ages allows individuals to 
increase consumption earlier on. In this policy scenario, the welfare 
gain is reaching 4.5% for the informal population in the long run, while 
the gain for the formal sector is 3%.
If, instead, a lower contribution rate is implemented, the over-
all welfare impact is less. As the dotted lines in Fig. 11(a) show, 
a lower contribution rate would only affect formal workers, while 
keeping informal workers unchanged, thus not helping to improve the 
redistribution between formal and informal workers. Therefore, the 
overall welfare gain is smaller than balancing government budget with 
lump-sum transfers, although the formal population has similar gains.
An adequate resident pension is a common option to reduce the 
income inequality of the elderly (Lu et al., 2014). Increasing the social 
replacement rate for informal pensions, by nature, leads to welfare 
gains for the informal population. However, the welfare gain for the 
informal population comes at the expense of reduced welfare for the 
formal sector, as the government will need to use a lump-sum tax 
or increase the contribution rate for formal workers to finance the 
increase in resident pension. Since the lump-sum transfer is imposed 
on the whole population while the contribution rate applies only to 
the formal workers, the welfare gain for informal workers is larger 
when it is implemented with government adjusting the contribution 
rate, as the dotted green line shows. As the green lines in Fig. 11(b) 
show, apparently, the welfare gain for informal workers increases the 
longer they experience the expansion of pension benefits, making the 
welfare gain greater for later cohorts. When implemented with a lump-
sum transfer to rebalance government budget, increasing the informal 
pension benefit replacement rate to 30% of the formal pension level 
results in a welfare gain of as high as 3.5% CEV for the informal sector 
in the long run, although this comes at the expense of a welfare loss of 
almost the same size for formal workers in the same cohort. However, 
with adjustment of the contribution rate, the welfare gain for informal 
workers amounts to 7. 5% of CEV, while the welfare loss to formal 
workers is only 3% of CEV, leading to smaller overall welfare losses 
when evaluated as a whole. As the share of the formal population con-
tinues to increase, the aggregate welfare gain from increasing benefits 
for the informal becomes less, but the costs to finance the increase in 
resident pension also decrease per formal worker. Therefore, we expect 
the welfare change to remain slightly negative in the long run.
Fig. 11(c) evaluates the welfare effects under the policy scenario 
of using consumption tax-based financing. The welfare change for this 
scenario is not monotone as we see in other scenarios. Despite the 
fact that it can distort intertemporal consumption-savings decisions of 
individuals, the consumption tax at 25% is a reduction in the overall 
burden of the pension contribution tax. As the consumption tax is 
uniform, it is a relaxation of the pension contribution tax burden for the 
formal sector, while it increases the tax burden for informal workers. 
In addition, consumption tax-based financing is implemented with a 
lump-sum transfer. Therefore, the formal sector experiences increasing 
welfare gains until the cohort born around 1995, reaching 4.7%, after 
which it drops to a flat 3.8% for cohorts born after 2020. In contrast, 
the informal sector faces initial welfare loss until those born after the 
mid-1980s, the welfare loss gets smaller for the following cohorts and 
stays flat at about 2% welfare loss for those born after 2020.
Economic Modelling 153 (2025) 107336
12

## Página 13

H. Gao and B. Lu
Fig. 11. Welfare change by formality.
Note: In panels (a) and (b), results under the assumption of government reimbursement in the form of lump-sum transfer are depicted in solid lines, and results 
under government tax reimbursement are depicted in dotted lines.
Fig. 12. Impact of reforms on households savings and labor supply.

### 5.4. Impact on household decisions

In Fig. 12, we report the impacts of policy reforms on household 
behavioral responses in terms of their savings and labor supply. For 
each policy, we plot both the impacts under scenarios with and without 
a lump-sum transfer/tax.
As column 1 in panels (a) and (b) shows, removing the partial index-
ation of wage growth is a decrease in pension wealth for formal workers 
and an increase in incomes earlier on. Therefore, formal workers would 
want to increase their labor supply and savings to insure themselves 
against the negative wealth effect. However, if lump-sum transfer is 
introduced, labor supply decreases. The labor supply does not decrease 
if a lower contribution is implemented. Informal workers experience a 
pure wealth effect, while formal workers achieve better intertemporal 
allocation with more transfer at younger ages. Overall, the impact on 
the household savings rate is negligible.
In column 2 of panels (a) and (b), we examine the impact when 
the government increases the pension benefits for informal workers.
The policy reform achieves better reallocation across formal and infor-
mal workers, but will affect formal and informal workers’ behaviors 
differently. The impact on savings is dominated by the effect that 
the informal workers are better insured with public pension therefore 
reduce their savings. This is also evident as the impact on the savings 
rate in the long run diminishes. Furthermore, the wealth effect also 
incentivizes informal workers to work less. If the government finances 
the increase in resident pension with an increase in contribution rate, 
formal workers also reduce labor supply. If instead a lump-sum tax 
is imposed, formal workers are incentivized to increase labor supply, 
which leads to a lower decrease in aggregate labor supply.
Finally, in column 3, we examine the impact of consumption-tax-
based financing. The consumption tax would alter agents’ intertem-
poral decisions by encouraging them to consume less and save more. 
However, this only happens to formal workers. After the reform, the 
informal population, who have a lower disposable income and decrease 
their savings. As column 3 in panel (b) shows, the net household 
savings rate increases as the impact on the formal sector dominates.
Economic Modelling 153 (2025) 107336
13

## Página 14

H. Gao and B. Lu
Fig. 13. Impact on welfare under alternative reference years of government budget balance.
Note: The red solid lines with triangular markers refer to results under baseline reference year of 2100, the blue dotted lines refer to results under the reference 
year 2060, and the green solid line refer to results under the reference year 2080.
Furthermore, agents reduce their labor supply due to the positive 
wealth effect of lump-sum transfers.
6. Sensitivity of results
In order to test the robustness of our findings for the baseline 
model, we conduct robustness along several dimensions by relaxing 
the assumptions made for the baseline in terms of model features 
or parameter values. These exercises, strongly motivated by policy 
concerns, illustrate the role of each of the model elements and provide 
an error bound of our benchmark estimates.

### 6.1. Sensitivity to reference year of balancing government budget

In the benchmark, we set the reference year for the government to 
balance the budget to 2100, before which the government can issue 
bonds at the market rate to smooth fluctuations in government revenue 
across different years. In this section, we consider two alternatives, 
2060 and 2080 as reference years.
As shown in Fig. 9, the cost-saving effect of options 1 and 3 is more 
significant in the long run. Therefore, using a reference year in a shorter 
horizon will lead to lower lump-sum transfers or lower contribution 
tax cuts to maintain the government budget balanced. For example, 
under option 1, the lump-sum transfer is annually 3098 CNY at the 
wage level of year 2023 using reference year 2100, which reduces 
to 2005 CNY if using 2080 and further reduces to 775 CNY if using 
2060. If alternatively implemented with adjustment of contribution 
tax rates, the contribution rate reduces to 19.2% using reference year 
2100, but only to 19.6% using reference year 2080 and to 20.3% using 
reference year 2060. For the same reason, the size of negative transfer 
or the increase in contribution rate also decreases under option 2 where 
the government needs to increase revenue to finance the expansion of 
resident pension.
Since using an alternative reference year only involves the size of 
the policy to rebalance the government budget, the change in welfare 
effects hinges on the direction in which the rebalancing policy is 
headed, as shown in Fig. 13. Compared to using 2100, the welfare gains 
are smaller for option 1 using alternative reference years. Similarly, the 
welfare gain for the informal workers and the welfare loss for formal 
workers are smaller using alternative reference years, which drives up 
the overall welfare gain to positive if reference year 2060 is used. As 
shown in Fig. 9, it is only until 2055 that the consumption tax scheme 
makes a difference in the government budget compared to the baseline 
policy. As a result, the effect of distortion on intertemporal allocation 
dominates if an earlier reference year is used, making the consumption 
tax least favorable among all options. As can be expected, the impacts 
on household behavior move in the direction under which a smaller 
scale of rebalancing policy is used and are qualitatively similar.

### 6.2. Sensitivity to fertility rate projection

In our benchmark, we take the demographic process projected by 
the UN under the assumption of the medium fertility scenario. How-
ever, as the fertility rate in China hits its historically low level in recent 
years, doubts are raised as to whether the fertility rate can bounce back 
to 1.35% in the long run, as projected by the medium fertility scenario 
which is represented as the blue solid line in Fig. 14(a).
A lower fertility ratio leads to an increase in the dependency ratio of 
the population and a rapid decline of the total population, exacerbating 
the sustainability of pension policy. To address this concern, we present 
results under the low fertility scenario. As shown in the dashed red line 
of Fig. 14(a), the fertility rate is projected to increase only to 0.8% in 
the long run. As Fig. 14(b) shows, the population in 2100 is projected to 
be 400 million, which is only around 2/3 under the medium scenario.
In Fig. 15, we plot the impact of policy reforms on the government 
budget in both the benchmark and the low fertility scenarios. Panel (a)
Economic Modelling 153 (2025) 107336
14

## Página 15

H. Gao and B. Lu
Fig. 14. WPP projection fertility variants.
Fig. 15. Impact on government budget under alternative low fertility scenario.
Note: (i) The cumulative present value of public pension deficits is discounted using the market deposit rate. (ii) The solid lines with triangle markers refer to 
the results under baseline model, and the dotted lines are results under the alternative model assumptions.
Fig. 16. Impact on welfare under low and medium fertility scenarios.
Note: The solid and dotted lines refer to the case of medium and low fertility variants, respectively.
Economic Modelling 153 (2025) 107336
15

## Página 16

H. Gao and B. Lu
Fig. 17. Impact on government budget under alternative assumptions of intergenerational transfers.
Note: (i) The cumulative present value of public pension deficits is discounted using the market deposit rate. (ii) The solid lines with triangular markers refer to 
the results under baseline model, and the dotted lines are results under the alternative assumptions of intergenerational transfers.
presents the impact on the government deficit in each year, and panel 
(b) presents the impact on the cumulative deficit. As Fig. 15 shows, 
low fertility would exacerbate the government deficit to a large extent. 
For example, on an annual basis, the government deficit increases from 
5.8% to 8% of GDP in year 2075 when we assume a lower fertility 
instead of the benchmark fertility scenario, as the comparison between 
the solid blue line with triangle marker and the dashed blue line 
shows. As a consequence, the cumulative deficit increases from 200% 
to 270% of GDP. In the low fertility scenario, the ‘‘revenue balancing’’ 
contribution rate increases to 49%. Although the magnitude is much 
larger under the low fertility scenario, the impact of policy reforms 
has the same direction between the two fertility scenarios. To be more 
specific, indexing benefits to CPI only and the consumption tax-based 
financing reduce government deficits, while increasing the benefits for 
the informal workers worsens the government budget.
Given the considerably worse fiscal trajectory of the pension system 
under the low fertility scenario, the magnitude of fiscal savings from 
the simulated reforms is larger under the low fertility scenario than 
the medium. However, the broad direction and pattern of policy reform 
impacts is similar between the two fertility scenarios.
We compare the welfare impacts of each reform option individually 
in medium and low fertility scenarios, both overall and for formal and 
informal sectors separately in Fig. 16. As in the baseline, removing the 
wage indexation of pension benefits and the consumption tax leads 
to the large welfare gains among all options, while increasing the 
resident pension leads to minor overall welfare changes, as it leads 
to changes in opposite directions for formal and informal workers. 
Our results illustrate that the welfare effects of the pension reforms
are qualitatively similar between the benchmark and the low fertility 
scenarios.

### 6.3. Sensitivity to intergenerational transfers

In our baseline, we assume that agents transfer part of their income 
to their parent generation when they are young and receive transfers 
from their children generation when they are old. To shed further 
light on the role of intergenerational monetary transfers, we consider 
two alternatives. First, we assume that there are no intergenerational 
transfers between generations. As informal workers rely more on in-
tergenerational transfer when they get old, this is likely to have a 
major impact on their savings behavior and welfare. Second, instead 
of assuming that the transfer-to-income ratio is 9% for both formal 
and informal workers, we assume that formal workers transfer a higher 
fraction of income to their parents. To be more specific, we assume that 
formal workers transfer 12% of their income, while informal workers 
only transfer 6% of their income. This check aims to provide a better 
understanding of the relative importance of transfers for formal and 
informal workers in their savings and labor supply decisions when they 
are young.
In Fig. 17, we present the impact of reforms on the government bud-
get. The left panel of panel (a) shows that removing intergenerational 
transfers leads to an almost negligible impact on the annual deficit. In 
panel (b), we further show that the impact on cumulative deficit is also 
very small. In the left panels of panel (a) and (b), we present results 
under the assumption of larger intergenerational transfer obligations
Economic Modelling 153 (2025) 107336
16

## Página 17

H. Gao and B. Lu
Fig. 18. Impact on welfare under alternative assumptions of intergenerational transfers.
Note: The red solid lines with triangular markers refer to results under baseline model, the blue dotted lines refer to results without intergenerational transfers, 
and the green solid line refer to results under the assumption of larger intergenerational transfers made by formal workers.
for formal workers. As both figures show, this assumption affects the 
projection of government deficit to a lesser extent.
Although the assumption of intergenerational transfers has little 
impact on the government budget, it plays an important role in af-
fecting the evaluation of welfare effects. To be more specific, once 
the intergenerational transfers are shut down, agents, in particular 
the informal agents, are subject to a large loss of old-age incomes. 
Therefore, the welfare effects for informal workers will be amplified.
In panels (a), (b), and (c) of Fig. 18, we present the welfare impacts 
for the whole population, the formal population, and the informal 
population, respectively. Within each panel, we list five columns, each 
corresponding to a specific reform option and a specific way to main-
tain government budget balance. In all figures, we use the solid red 
line with triangle markers for results under the baseline assumption 
of transfers, the dotted blue line for results without transfers, and the 
solid green line for results with larger transfer obligations for formal 
workers.
As panel (a) shows, the overall welfare gain increases for all options 
when intergenerational transfers are shut down, in particular when 
the resident pension is increased, indicating the importance of incor-
porating intergenerational transfers into the framework. Furthermore, 
panel (b) shows that when there are no transfers, the policy experi-
ments yield slightly larger government surplus for the scenario of CPI 
indexation and raising resident pension, leading to small welfare gains 
for formal workers. However, the welfare gain under the consumption 
tax is reduced. The most significant welfare changes occur in informal 
workers, as panel (c) shows. This is because when intergenerational 
transfers are shut down, the old informal workers rely more on the 
public pension. Therefore, the long-run welfare gain increases from 3% 
to 7.5% if the increase in resident pension is financed with a lump-
sum tax, and from 7% to 10% if it is financed with an increase in the 
contribution rate for formal workers. Interestingly, due to the relative 
more important role of pension income for old-age support, the welfare
impact of consumption tax for informal workers also turns positive in 
the long run when transfers are not modeled, as opposed to long-run 
welfare loss in the baseline model.

### 6.4. Sensitivity to long-run wage growth and internal rates of return

In this subsection, we relax two assumptions that may directly 
affect the fiscal burden. First, we relax the assumption that wage 
growth converges to 2% in the long run and consider alternatively 
a higher level 2.5% and a lower level 1.5%. As pension benefits are 
only partially indexed to wage growth, a higher wage growth leads 
to lower pension budget deficits with a higher contribution relative to 
pension expenditure. Second, in our benchmark, we assume that the 
internal rate of return is the same for social-pooling account (SPA) 
and individual account (IA). Estimating the actual returns of the two 
accounts is empirically challenging, as the rates differ by region and 
are only available for a limited time window. In Section B of the Online 
Appendix, we present data on the returns and show that there is a trend 
of convergence in the returns to these accounts. To understand how the 
assumption of returns may affect our results, we alternatively consider 
two cases where the return to IA (𝑅𝐼) is different from return to SPA 
(𝑅𝑆). To be more specific, we calibrate separately for the return to IA 
and SPA so that the return to IA is 20% lower or higher than the SPA 
when the total return — or equivalently, the total pension incomes — 
for cohorts who are pension recipients in 2024 are controlled the same 
as in the baseline.
A lower long-run wage growth will decrease the contribution of 
the latter cohort, exacerbating the pension fund deficits under a PAYG 
system. As column 1 of panel (a) in Fig. 19 shows, under the new 
policy in 2024 without further reform implemented, when the long-
run wage grow rate is 1.5%, the annual deficit is projected to be 8% of 
GDP, as opposed to around 6% in the baseline under the assumption 
of a 2% long-run growth. In panel (b) column 1, we show that the
Economic Modelling 153 (2025) 107336
17

## Página 18

H. Gao and B. Lu
Fig. 19. Impact on government budget under alternative assumptions of long run wage growth and internal returns.
Note: (i) The cumulative present value of public pension deficits is discounted using the market deposit rate. (ii) The solid lines with triangular markers refer to 
the results under baseline model, and the dotted lines are results under the alternative model assumptions.
cumulative deficits will increase to 350% of GDP if the 1.5% wage 
growth is assumed. In addition, lower long-run wage growth will lead 
to slightly smaller pension fund savings with reform options 1 and 
3 and larger deficits with reform 2. In contrast, when long-run wage 
growth is 2.5%, the public pension system becomes more sustainable. 
As panel (a) column 2 shows, the annual deficit will reduce to 4% by 
the year 2075. Panel (b) column 2 further shows that the public pension 
system will run a net cumulative surplus until 2050, and the cumulative 
deficit is only 100% of GDP by year 2075.
While the assumption of long-run wage growth has a large impact 
on the sustainability of public pension, the assumption of internal 
return of pension accounts appears to affect pension deficits to a lesser 
extent, as shown in columns 3 and 4 of Fig. 19. Yet, it still has important 
implications for the choice of further reform options. When the return 
of IA is 20% higher than the SPA, the public pension deficit is projected 
to be lower, since a larger share of pension funds have been invested in 
the social-pooling account. This happens in the cases where the 2024 
policy is continued, or with further reform options 1 or 2. However, as 
the consumption-tax scheme changes the pension system to be complete 
individual account-based, the deficit under option 3 is assumed to be 
larger. The opposite happens when the return to the SPA is 20% higher 
than the IA, as Fig. 19 column 4 shows.
As in previous subsections, we present the welfare impacts for the 
whole population and the formal and informal population separately in 
Fig. 20. In all panels, the welfare change under the baseline model is 
depicted with a solid red line with triangle markers; welfare changes 
under the assumption of 1.5% and 2.5% long-run wage growth are de-
picted in solid and dotted blue lines, respectively; and welfare changes 
under the assumption of a higher return for IA and a lower return for 
IA are depicted in solid and dotted green lines, respectively. As shown 
in column 1 of Fig. 19, the assumption of lower wage growth will 
exacerbate the government deficit, therefore, suggesting greater cost 
savings for options 1 and greater deficit for option 3. As a consequence, 
the welfare gain is larger when option 1 is implemented, in particular 
if it is accompanied by a lump-sum transfer, as column 1 of Fig. 20 
shows. For the same reason, the welfare loss is larger when the RP is 
increased, as columns 3 and 4 of Fig. 20 show. Column 5 shows that the 
welfare gain for consumption tax is smaller if a lower long-run wage
growth is assumed. Not surprisingly, the assumption of 2.5% long-run 
wage growth leads to welfare changes in opposite directions.
Interestingly, the assumption of internal returns for the SPA and the 
IA has a great impact on the welfare effects of the consumption tax but 
does not seem to have an impact on the welfare changes of options 1 
and 2. To be more specific, under option 3 with consumption tax, as the 
government runs a larger deficit when the return to IA is assumed to 
be higher than SPA, the welfare gain is largely weakened, as the solid 
lines in column 5 show. In addition, this happens to both the formal 
and informal workers, leading to an overall welfare loss for cohorts 
born before 2040 and neutral welfare impacts for cohorts born after. 
In contrast, if the IA is 20% lower than the SPA, the consumption tax 
yields larger welfare gains, and all cohorts experience welfare gains. 
This exercise indicates the importance of pension account returns in 
evaluating the welfare effects of policy reforms.

### 6.5. Sensitivity to preference parameters

The final check involves the assumption of preference parameters 
in the model. In our baseline, we set the discount factor 𝛽= 0.96
and the risk aversion parameter 𝜎= 4. As discussed in the previous 
section, the savings behavior of Chinese households may be explained 
by other factors that are not captured by our model. To illustrate 
how introducing these additional factors may affect the validity of our 
results, we consider alternative parameters for the preference. To be 
more specific, we consider a higher and lower level for the discount 
factor 𝛽= 0.92 and 1, and for risk aversion 𝜎= 2 and 8.
In Fig. 21, we present the impact of policy reforms on the govern-
ment budget. As in the previous sections, panel (a) presents the impact 
on the annual government budget and panel (b) presents the impact on 
the cumulative budget using the market rate. As can be seen in Fig. 21, 
the government deficit would reduce if we use a lower risk aversion 
(𝜎= 2) or a higher discount factor (𝛽= 1) since both choices imply a 
weaker role for public insurance. The deficit will increase slightly if we 
use a higher risk aversion (𝜎= 8) or a lower discount factor (𝛽= 0.92) 
although the effects are quite insignificant. In general, the preference 
parameters have a limited impact on the labor supply and thus a limit 
impact on the contribution and expenditure of the public pension funds.
Economic Modelling 153 (2025) 107336
18

## Página 19

H. Gao and B. Lu
Fig. 20. Impact on welfare under alternative assumptions of long run wage growth and internal returns.
Note: The red solid lines with triangular markers refer to results under baseline model; the blue solid and blue dotted lines refer to results under the assumption 
of long run wage growth 1.5% and 2.5%, respectively; the green solid and green dotted lines refer to results under the assumption of the internal return of 
individual account is 20% higher or lower than the return of social-pooling account, respectively.
Fig. 21. Impact on Government budget under alternative assumptions of preference parameters.
Note: (i) The cumulative present value of public pension deficits is discounted using the market deposit rate. (ii) The solid lines with triangular markers refer to 
the results under baseline model, and the dotted lines are results under the alternative model assumptions.
Economic Modelling 153 (2025) 107336
19

## Página 20

H. Gao and B. Lu
Fig. 22. Impact on welfare under alternative assumptions of preference parameters.
Note: The red solid lines with triangular markers refer to results under baseline model; the blue solid and blue dotted lines refer to results under the assumption 
of 𝛽= 0.92 and 𝛽= 1, respectively; the green solid and green dotted lines refer to results under the assumption of 𝜎= 2 and 𝜎= 8, respectively.
As a result, the choices of preference parameters do not seem to have 
a large impact on the government budget.
In Fig. 22, we next evaluate the welfare impacts of the reforms by 
the choice of preference parameters. As shown in columns 1 and 2, a 
lower discount factor or a higher risk aversion leads to slightly welfare 
gains, because both cases imply a stronger incentive for agents to re-
ceive transfer or contribution tax cuts as young as possible. Apparently, 
a lower risk aversion or a higher discount factor work in the opposite 
way. For option 2, the rebalancing of government budget comes in an 
opposite way, i.e., government needs to increase the contribution rate 
or use negative lump-sum transfers to finance the increase in resident 
pensions. As a result, a higher risk aversion or a lower discount factor 
will reduce welfare gains, in particular, for the informal sector. These 
effects are also magnified with slightly larger government deficits under 
a high risk aversion and a low discount factor, as shown in Fig. 21. 
The consumption tax works in a more complicated way. As discussed 
before, for formal workers, the consumption tax leads to distortion 
of intertemporal substitution and a reduction in pension contribution 
obligations, but the second effect dominates. These effects are amplified 
with a low discount factor and a higher risk aversion, leading to greater 
welfare gains, as column 5 of panel (b) shows. The opposite happens 
when a high discount factor or a low risk aversion is assumed. For 
the informal sector, a consumption tax means that they finance old-
age benefits with contribution at younger ages. Therefore, welfare loss 
increases when they are more impatient with a lower discount factor 
or when they care less about uncertainty, i.e., when risk aversion is 
lower. The overall effects are dominated by the formal sector, as shown 
in column 5 of panel (a).

### 6.6. Discussion of other model assumptions

As a final remark, we discuss how we can address several elements 
that are not explicitly modeled in our framework. In Section 6.2,
we present the sensitivity of our results under the UN projection 
of the low fertility variant and show that both government deficits 
and welfare effects will be amplified. This, however, does not fully 
account for the endogenous nature of the fertility choice, in particular 
the quantity-quality trade-off of children (Becker and Lewis, 1973). 
Therefore, our model does not take into account the impact of depen-
dent children on adult household members’ labor supply and savings 
behaviors (Curtis et al., 2015; Choukhmane et al., 2023). A change in 
demographic structure can also lead to strategic behavioral responses 
such as competition in savings (Wei and Zhang, 2011), human capital 
investment (Choukhmane et al., 2023), and education (Kim et al., 
2024). As these effects are interrelated, below we provide a brief 
discussion of the channels through which these may alter the results 
and how we can address these issues in our framework.
First, less generous Social Security benefits can encourage the sup-
ply of labor among older workers and the investment in human capital 
during the early stages of their careers, as shown by Iskhakov and 
Keane (2021) and Fan et al. (2024). In light of this mechanism, it 
is likely that option 1 where pension benefits are effectively reduced 
can stimulate human capital investment, which further improves the 
welfare effects. Through the lens of model, the impact on human 
capital, in particular, the extensive margin, can be addressed with an 
alternative projection of faster formalization of the population.
Second, behavioral responses in the human capital and asset market 
may propagate with an impact on factor prices of capital and labor 
through general equilibrium effects. This, however, depends on the 
quantitative strength of the incentive to accumulate physical or human 
capital. We provide sensitivity checks along two relevant margins, 
i.e., long-run wage growth in Section 6.4 and preference parameters 
in Section 6.5. We can extend the work once a better identification of 
the impact of reforms on aggregate factor supply is obtained.
Economic Modelling 153 (2025) 107336
20

## Página 21

H. Gao and B. Lu
7. Conclusion
In this paper, we construct a dynamic quantitative model with char-
acteristics of Chinese economy to evaluate the long-run impacts of the 
public pension reform on government fiscal sustainability, household 
behaviors, and welfare. We also perform sensitivity checks to examine 
the role of various model elements in affecting the results, establishing 
the validity of our results.
We show that the 2024 reform can greatly reduce the fiscal financial 
burden and have a large impact on household savings and labor supply. 
We propose a few more reform options that aim to further address 
the sustainability and equity of the pension system. Gradually shifting 
the pension benefits to CPI indexation can save fiscal expenditure 
and lead to large welfare gains. Increasing the benefits of informal 
workers leads to overall welfare gains with better redistribution, but 
the gains diminish as the share of informal workers decreases in the 
total population.
The general applicability of results is established through vari-
ous sensitivity checks, demonstrating the validity of results to rich
environment and policy concerns. We show that if a low fertility 
rate becomes more likely, policies aimed at increasing social pen-
sion benefits should be approached with caution. Welfare improves 
when intergenerational transfers are reduced from their current levels. 
While higher wage growth helps contain the government budget, its 
welfare impact depends on policy design: it reduces welfare under CPI-
indexed benefits but enhances it if social pensions are increased or 
if a consumption-based contribution mechanism is used. The policy 
setting for internal rate of return is also critical. Delaying retirement 
age without changing the social-pooling benefit formula effectively 
lowers the internal rate of return for social pooling relative to in-
dividual accounts. If individual accounts receive higher credited re-
turns to preserve current benefit levels, this adjustment can reduce 
government deficits without significantly harming welfare. However, 
under a consumption-based contribution model, where all contributions 
fund individual accounts, a higher individual account credited return 
increases government deficits and reduces welfare.
It seems encouraging that the 2024 reform and the potential follow-
up reform options can greatly improve the situation. However, there are 
still several dimensions that the model is overly simplified that need 
attention from both academic and policy perspectives.
First, it will take considerably longer for the impacts of long-run 
technological progress, in particular, automation, to emerge. It raises 
a concern for both researchers and policy makers to fully understand 
as fast automation can change factor prices, working opportunities, 
and working arrangements for workers, and thus the effectiveness of 
government policies. Furthermore, it will also have an impact on peo-
ple’s education and migration decisions, both of which have significant 
implications for the design of pension policy. Despite we have made 
original contributions in examining the effects through its impact on 
the demographic change (formality share) and factor prices (long-term 
wage growth), it still remains a question how to design a flexible 
pension policy to accommodate this change with more data and bet-
ter understanding of the channels that technological progress affects 
household behavior.
Second, we simplified the compliance issue, in particular, from the 
firm side. However, in policy practice, there is a very strong sorting 
pattern between firm and worker, which implies that firms play an 
important role in increasing coverage to these informal workers. In this 
paper, we follow the convention of this field to introduce a representa-
tive firm. However, more efforts are needed to better understand how 
firms may respond to these reforms. We leave these avenues for future 
works.
Declaration of competing interest
The author acknowledge financial support from the Australian Re-
search Council under grants DP210103319 and CE170100005 for the 
paper. The author declare that they have no relevant or material 
financial interests that relate to the research described in this paper.
Appendix A. Supplementary data
Supplementary material related to this article can be found online 
at https://doi.org/10.1016/j.econmod.2025.107336.
Data availability
I have shared the link to my data and code at the attached file step.
Replication Package for Reforming China’s Public Pension System: Fis
cal Sustainability and the Challenge of Formality-Based Inequality (Or
iginal data) (Mendeley Data)
References
Bairoliya, N., Miller, R., 2021. Social insurance, demographics, and rural-urban
migration in China. Reg. Sci. Urban Econ. 91, 103615.
Banerjee, A., Meng, X., Porzio, T., Qian, N., 2023. Aggregate fertility and household
savings in China. Working Paper.
Becker, G.S., Lewis, H.G., 1973. On the interaction between the quantity and quality
of children. J. Political Econ. 81 (2, Part 2), S279–S288.
Chamon, M.D., Prasad, E.S., 2010. Why are saving rates of urban households in China
rising? Am. Econ. J.: Macroecon. 2 (1), 93–130.
Chen, K., Wen, Y., 2017. The great housing boom of China. Am. Econ. J.: Macroecon.
9 (2), 73–114.
Chomik, R., O’Keefe, P., Piggott, J., 2024. Pensions in aging Asia and the Pacific: Policy
insights and priorities. ADB Economics Working Paper Series.
Choukhmane, T., Coeurdacier, N., Jin, K., 2023. The one-child policy and household
saving. J. Eur. Econ. Assoc. 21 (3), 987–1032.
Coeurdacier, N., Guibaud, S., Jin, K., 2014. Fertility policies and social security reforms
in China. IMF Econ. Rev. 62 (3), 371–408.
Conesa, J.C., Kitao, S., Krueger, D., 2009. Taxing capital? Not a bad idea after all!.
Am. Econ. Rev. 99 (1), 25–48.
Conesa, J.C., Krueger, D., 1999. Social security reform with heterogeneous agents. Rev.
Econ. Dyn. 2 (4), 757–795.
Curtis, C.C., Lugauer, S., Mark, N.C., 2015. Demographic patterns and household saving
in China. Am. Econ. J.: Macroecon. 7 (2), 58–94.
Deng, Y., Fang, H., Hanewald, K., Wu, S., 2023. Delay the pension age or adjust the
pension benefit? Implications for labor supply and individual welfare in China. J. 
Econ. Behav. Organ. 212, 1192–1215.
Díaz-Giménez, J., Díaz-Saavedra, J., 2009. Delaying retirement in Spain. Rev. Econ.
Dyn. 12 (1), 147–167.
Esteban-Pretel, J., Kitao, S., 2021. Labor market policies in a dual economy. Labour
Econ. 68, 101956.
Fan, X., Seshadri, A., Taber, C., 2024. Estimation of a life-cycle model with human
capital, labor supply, and retirement. J. Political Econ. 132 (1), 48–95.
Fang, H., Feng, J., 2018. The Chinese pension system. NBER Working Paper No.
w25088, National Bureau of Economic Research.
Feng, J., He, L., Sato, H., 2011. Public pension and household saving: Evidence from
urban China. J. Comp. Econ. 39 (4), 470–485.
Gao, H., 2025. Social security and female labor supply in China. J. Econ. Behav. Organ.
238, 107203.
Gao, H., McKiernan, K., 2023. Labor market sorting and public pensions in developing
economies. Working Paper.
He, H., Ning, L., Zhu, D., 2019. The impact of rapid aging and pension reform on
savings and the labor supply: The case of China. IMF Working Paper, Vol. 2019, 
International Monetary Fund.
Hernández, A., López, J., Galindo, F., Salas, F., 2017. Miles for retirement. Working
Paper.
Huang, W., Zhang, C., 2021. The power of social pensions: Evidence from China’s new
rural pension scheme. Am. Econ. J.: Appl. Econ. 13 (2), 179–205.
İmrohoroğlu, S., Kitao, S., 2009. Labor supply elasticity and social security reform. J.
Public Econ. 93 (7–8), 867–878.
İmrohoroğlu, S., Kitao, S., 2012. Social security reforms: Benefit claiming, labor force
participation, and long-run sustainability. Am. Econ. J.: Macroecon. 4 (3), 96–127.
Iskhakov, F., Keane, M., 2021. Effects of taxes and safety net pensions on life-cycle
labor supply, savings and human capital: The case of Australia. J. Econometrics 
223 (2), 401–432.
Jung, J., Tran, C., 2012. The extension of social security coverage in developing
countries. J. Dev. Econ. 99 (2), 439–458.
Kim, S., Tertilt, M., Yum, M., 2024. Status externalities in education and low birth
rates in Korea. Am. Econ. Rev. 114 (6), 1576–1611.
Economic Modelling 153 (2025) 107336
21

## Página 22

H. Gao and B. Lu
Kitao, S., 2014. Sustainable social security: Four options. Rev. Econ. Dyn. 17 (4),
756–779.
Kitao, S., 2015. Fiscal cost of demographic transition in Japan. J. Econom. Dynam.
Control 54, 37–58.
Li, C., Lin, S., 2019. China’s explicit social security debt: How large? China Econ. Rev.
53, 128–139.
Lu, B., He, W., Piggott, J., 2014. Should China introduce a social pension? J. Econ.
Ageing 4, 76–87.
Meng, X., 2017. The labor contract law, macro conditions, self-selection, and labor
market outcomes for migrants in China. Asian Econ. Policy Rev. 12 (1), 45–65.
O’Keefe, P., Gao, H., Lu, B., Piggot, J., 2025. The dynamic evolution of China’s pension
system and future prospects and policy issues. Working Paper.
Ruppert, K., Schön, M., Stähler, N., 2024. Consumption taxation to finance pension
payments. Econ. Model. 130, 106570.
Salditt, F., Whiteford, P., Adema, W., 2007. Pension reform in China: Progress and
prospects. OECD Social, Employment and Migration Working Papers No. 53, OECD.
Sin, Y., 2005. Pension Liabilities and reform options for old age insurance. World Bank
Working Paper 2005-01, 1, pp. 1–71.
Song, Z., Storesletten, K., Wang, Y., Zilibotti, F., 2015. Sharing high growth across gen-
erations: Pensions and demographic transition in China. Am. Econ. J.: Macroecon. 
7 (2), 1–39.
Wang, D., Feng, J., 2021. Chinese Pension Reform: Progress, Challenges and Prospects.
World Bank Working Paper.
Wang, X., Wen, Y., 2012. Housing prices and the high Chinese saving rate puzzle.
China Econ. Rev. 23 (2), 265–283.
Wei, S.-J., Zhang, X., 2011. The competitive saving motive: Evidence from rising sex
ratios and savings rates in China. J. Political Econ. 119 (3), 511–564.
Wheadon, D., Castex, G., Kudrna, G., Woodland, A., 2024. Non-linear means-tested
pensions: Welfare and distributional analyses. Econ. Model. 138, 106759.
Economic Modelling 153 (2025) 107336
22