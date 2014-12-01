
# maplot
# Roy Haggerty
# 2014

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap, BoundaryNorm
import matplotlib as mpl
from mpl_toolkits.axes_grid.axislines import Subplot
from mpl_toolkits import basemap
from matrix_from_xls import matrix_from_xls as mfx
import constants as cst
import datetime
from Rectangle import np_rec_calc as nrc
from compare import compare_rows
import Image
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from movingaverage import movingaverage, binomial_window

def sample_data():
    a = [np.array([-10.35253906,  -9.23364258,  -7.73858643,  -5.3651123 ,
        -1.82159424,   1.93164062,   3.89215088,   2.84082031,
        -0.40679932,  -3.97814941,  -6.72271729,  -8.63098145,
       -10.02484131, -10.96826172, -11.3449707 , -11.10107422,
       -10.36999512,  -9.46325684,  -8.5824585 ,  -7.37890625,
        -5.09234619,  -1.59136963,   1.91772461,   4.05657959,
         5.41711426,   8.64373779,  15.53387451,  24.43457031,
        31.31500244,  33.32885742,  30.73571777,  25.48687744,
        18.91564941,  11.4664917 ,   4.18109131,  -0.68188477,
        -1.16070557,   2.3215332 ,   6.74389648,   8.85375977,
         8.01391602,   6.4161377 ,   6.23443604,   7.00646973,
         6.32342529,   2.81860352,  -2.08422852,  -5.13885498,
        -3.32965088,   4.60406494,  17.31079102,  31.01074219,
        41.27996826,  45.31994629,  43.13476562,  37.63867188,
        33.57775879,  34.28265381,  38.15704346,  39.58422852,
        34.69769287,  25.86230469,  19.70898438,  21.04803467,
        29.11975098,  39.23712158,  47.10632324,  51.40032959,
        53.04608154,  52.9251709 ,  50.41998291,  44.20306396,
        34.77319336,  25.89855957,  22.17095947,  24.36767578,
        28.25921631,  29.09973145,  26.68023682,  24.96417236,
        27.25024414,  32.67041016,  37.33056641,  38.3894043 ,
        36.83618164,  35.86157227,  36.39251709,  35.29827881,  28.87890625]), np.array([-10.07797038,  -9.4047526 ,  -8.14944255,  -5.6892985 ,
        -1.76333415,   2.59671224,   5.26510824,   4.68509115,
         1.24423421,  -3.20309245,  -6.91763102,  -9.22231852,
       -10.32363688, -10.7071818 , -10.73367106, -10.55666911,
       -10.23000895,  -9.78573405,  -9.09725749,  -7.66744792,
        -4.87490641,  -0.85201823,   3.05038656,   5.48544515,
         7.09433187,  10.37655843,  16.77420247,  24.4402181 ,
        29.77432454,  30.83133138,  28.41287435,  24.13253988,
        18.56613363,  11.7738973 ,   4.9794637 ,   0.79770101,
         1.31460775,   5.84884847,  10.84097493,  12.56411947,
        10.39114583,   7.13052572,   5.7930013 ,   6.36587728,
         6.26950277,   3.7115804 ,  -0.10201823,  -1.9859904 ,
         0.74978841,   8.68527425,  19.93503011,  30.92318929,
        38.27878011,  40.65225423,  39.10592855,  36.47842611,
        36.20065511,  39.9525472 ,  45.40475667,  47.3898641 ,
        42.68441976,  33.63247884,  26.53244222,  26.37448324,
        33.15780843,  42.82870687,  50.94558919,  55.25937093,
        55.76706136,  53.36258138,  48.53158773,  41.22451986,
        32.33004964,  24.90432943,  22.40506185,  24.9445516 ,
        28.47873128,  28.9167806 ,  26.47958577,  25.05386556,
        27.67483724,  33.43417562,  38.59781087,  40.3075887 ,
        39.17611898,  37.9905721 ,  37.72982992,  35.78573812,  28.96310628]), np.array([-6.06902669, -4.49047445, -2.74871419, -0.69530843,  1.41809489,
        2.8615153 ,  3.07373454,  2.27215983,  1.2420695 ,  0.54028727,
        0.03717448, -0.70183919, -1.70763753, -2.47704671, -2.55144857,
       -1.99914144, -1.22082113, -0.4976766 ,  0.0969279 ,  0.54895426,
        0.88769938,  1.16577555,  1.31390788,  1.20270182,  0.92999674,
        0.79095866,  0.83325602,  0.65039469, -0.18584798, -1.51592611,
       -2.5693929 , -2.68438314, -2.03289388, -1.48644613, -1.71368001,
       -2.52593587, -3.19128011, -3.30498861, -3.19854329, -3.44982503,
       -4.13647054, -4.76031087, -4.88262533, -4.60979818, -4.35753988,
       -4.33733724, -4.49248861, -4.8148763 , -5.39226888, -6.09875081,
       -6.54101156, -6.47332357, -6.09234212, -5.76494954, -5.55053304,
       -5.13628743, -4.2678182 , -3.18542074, -2.5669515 , -2.97704671,
       -4.34832357, -6.03289388, -7.36529134, -8.11925863, -8.42473958,
       -8.38073324, -7.88683675, -6.86089681, -5.52599691, -4.37310384,
       -3.80291341, -3.85161947, -4.27868245, -4.82378743, -5.31353353,
       -5.61468099, -5.61785482, -5.29540609, -4.76714681, -4.32061361,
       -4.30456136, -4.887264  , -5.87987874, -6.79845785, -7.10015462,
       -6.49566243, -5.25786947, -4.22185872, -4.2232015 ]), np.array([-12.97698568, -12.0334432 ,  -9.95867513,  -6.21593831,
        -1.28936361,   2.92255046,   4.4285319 ,   3.11578776,
         0.79986979,  -0.93017171,  -2.24511312,  -4.15478109,
        -6.79760335,  -9.19445394, -10.19677327,  -9.07531331,
        -5.53277181,  -0.02898763,   5.73212077,   9.47247721,
        10.11688639,   8.51929118,   6.1314738 ,   3.66418864,
         1.55395915,   0.82208659,   2.2488444 ,   4.89514567,
         6.72729899,   7.16028239,   7.87060954,  10.16229655,
        12.43640544,  11.70361735,   7.36847331,   2.27197673,
        -0.18108724,   0.78192546,   2.99841715,   3.73248698,
         2.25549723,   0.2556193 ,  -0.30694173,   0.45935465,
         0.59894206,  -1.26794027,  -4.42516683,  -7.0289266 ,
        -7.80346273,  -6.52105306,  -3.70586751,  -0.55773519,
         1.35602214,   1.2198527 ,   0.08453776,   0.64551188,
         5.2398112 ,  13.20624186,  20.2500651 ,  21.46728923,
        15.60705973,   6.08948161,  -2.04546712,  -5.69469808,
        -4.82940267,  -1.46337484,   2.17169596,   5.12207438,
         7.78674723,  10.47931315,  12.23767497,  11.6427653 ,
         8.89819743,   6.4674113 ,   6.96850993,  10.4163859 ,
        14.04736735,  15.12244059,  13.59943034,  11.79059245,
        11.7042277 ,  13.05078532,  13.69055583,  11.95123698,
         8.67657878,   6.64459635,   7.40692546,   9.10931803,   8.27716471]), np.array([-11.14670817, -10.35587565,  -8.46653239,  -4.82169596,
         0.26503499,   4.81343587,   6.26942952,   3.80733236,
        -0.85007731,  -5.1879069 ,  -7.9969279 ,  -9.55668132,
       -10.48423258, -10.97159831, -10.79905192,  -9.58719889,
        -7.13920085,  -3.84501139,  -0.60904948,   1.93953451,
         3.97481283,   5.77016195,   6.70418294,   5.81996663,
         3.63216146,   2.56502279,   4.7397054 ,   9.45766195,
        13.64986165,  15.0174764 ,  13.97951253,  12.10542806,
         9.63576253,   5.70015462,   0.48891195,  -4.06778971,
        -5.96763102,  -4.97214762,  -2.8049113 ,  -1.71799723,
        -2.63975016,  -4.57950846,  -5.94028727,  -6.25687663,
        -6.38688151,  -7.21488444,  -8.61466471,  -9.62119548,
        -9.16239421,  -6.6264445 ,  -2.33732096,   2.18770345,
         4.91811117,   4.90828451,   3.50154622,   3.8478597 ,
         8.58394368,  17.00417074,  24.43190511,  25.51668294,
        18.91805013,   8.47090658,  -0.22251383,  -3.81260173,
        -2.3774821 ,   1.92299398,   6.8244222 ,  11.24092611,
        15.12099202,  18.18800863,  19.19215902,  16.96632894,
        12.43355306,   9.04366048,  10.19252523,  15.70973714,
        21.56282552,  23.84242757,  22.75685628,  21.99562581,
        24.35213216,  28.61726888,  30.87434896,  28.68660482,
        23.84615072,  20.52248128,  20.54225667,  21.24269613,  18.49641927]), np.array([-6.73115234, -4.95826416, -2.74543457, -0.06324463,  2.43699951,
        3.5805542 ,  2.72911377,  0.60386963, -1.13056641, -1.22736816,
        0.04191895,  1.14384766,  0.8317749 , -0.569104  , -1.62446289,
       -1.40522461, -0.28364258,  0.75084229,  1.06920166,  0.69584961,
        0.11333008, -0.08460693,  0.36174316,  1.14128418,  1.65562744,
        1.5380127 ,  0.87156982, -0.01472168, -0.84071045, -1.42414551,
       -1.59107666, -1.3300293 , -1.09345703, -1.63172607, -3.27747803,
       -5.50343018, -7.3479126 , -8.22687988, -8.27357178, -7.99537354,
       -7.73469238, -7.48737793, -7.16804199, -6.91193848, -7.00318604,
       -7.53791504, -8.28846436, -8.92921143, -9.28760986, -9.33881836,
       -9.09541016, -8.62476807, -8.11884766, -7.81855469, -7.80946045,
       -7.89960938, -7.74506836, -7.17207031, -6.4194458 , -6.01557617,
       -6.33216553, -7.24073486, -8.23841553, -8.89606934, -9.14515381,
       -9.17011719, -9.1190918 , -8.94880371, -8.51514893, -7.80848389,
       -7.0989502 , -6.78150635, -7.02680664, -7.63880615, -8.28077393,
       -8.74464111, -8.96125488, -8.89069824, -8.55512695, -8.1560791 ,
       -8.01252441, -8.29163818, -8.82636719, -9.21680908, -9.0723999 ,
       -8.22828369, -6.93116455, -5.85206299, -5.68604736]), np.array([-11.83579915, -10.80668538,  -8.83628743,  -5.70799154,
        -2.03208822,   0.87831217,   2.13075358,   2.19026286,
         2.32710368,   3.09254557,   3.68220622,   2.99141032,
         1.0767985 ,  -0.74253743,  -1.22740072,  -0.34202474,
         1.05580241,   2.20820719,   2.82631022,   2.90400798,
         2.66981608,   2.49885661,   2.50129801,   2.36695964,
         1.82582194,   1.05824382,   0.44496257,   0.01850993,
        -0.59910482,  -1.60777181,  -2.58409017,  -2.95738118,
        -2.88908285,  -3.25987142,  -4.60453695,  -6.34202474,
        -7.3218221 ,  -7.05802816,  -6.24095052,  -5.98039144,
        -6.6308431 ,  -7.50260824,  -7.75327962,  -7.36076253,
        -7.03690999,  -7.34080404,  -8.1721639 ,  -9.07646077,
        -9.6978597 ,  -9.87278646,  -9.602889  ,  -9.1162557 ,
        -8.79276937,  -8.85490316,  -9.10850423,  -9.0093221 ,
        -8.06767171,  -6.36027425,  -4.70646566,  -4.16160482,
        -5.14073079,  -7.05479329,  -8.87553304,  -9.97813314,
       -10.38395589, -10.36845296, -10.06535238,  -9.46592611,
        -8.65128988,  -7.90959066,  -7.6018514 ,  -7.90275472,
        -8.6443929 ,  -9.41551107,  -9.85349935,  -9.87028402,
        -9.61100667,  -9.23655599,  -8.82151693,  -8.48423665,
        -8.48631185,  -9.03141683,  -9.9544515 , -10.70384115,
       -10.67777913,  -9.66746419,  -8.13511556,  -7.0449056 ,  -7.18687337]), np.array([ -7.73040365,  -6.48852132,  -5.12139486,  -3.27148031,
        -0.48089193,   2.88110758,   5.53046061,   6.50159098,
         6.05749919,   4.99267985,   3.50867106,   1.29254557,
        -1.61358236,  -4.51922201,  -6.53979085,  -7.05694173,
        -5.92473958,  -3.6171224 ,  -1.11541341,   0.78448893,
         2.1415446 ,   3.46765544,   4.60345866,   4.5389445 ,
         2.66919352,  -0.10161947,  -1.85631917,  -1.28625081,
         1.15655924,   3.6507609 ,   4.56348063,   3.59357096,
         1.44659831,  -1.1317098 ,  -3.59881185,  -5.28295492,
        -5.543514  ,  -4.47594808,  -3.1327474 ,  -2.7077596 ,
        -3.43365072,  -4.42669271,  -4.72344564,  -4.35686849,
        -4.24138997,  -5.06786702,  -6.53551839,  -7.65600179,
        -7.5716512 ,  -6.10442708,  -3.87023519,  -1.9933431 ,
        -1.3983724 ,  -2.03728841,  -2.6853597 ,  -1.57183431,
         2.36688639,   8.23724772,  13.12152507,  13.96826579,
        10.14410807,   4.07074382,  -0.74602865,  -2.24511312,
        -0.81670736,   1.43121745,   2.38251139,   1.62628581,
         0.79980876,   1.83697917,   4.65759684,   6.99579264,
         6.85138346,   4.73028971,   2.8960612 ,   2.66211344,
         3.26929118,   3.52710368,   3.59210612,   4.45801188,
         6.17425944,   7.31671549,   6.30731608,   2.99786784,
        -1.12347005,  -4.21715902,  -5.54558919,  -5.75512288,  -5.96215413]), np.array([-10.89642741,  -9.45373942,  -7.42255046,  -4.50207926,
        -0.82770182,   2.46923421,   4.04900716,   3.95226644,
         3.60638021,   3.82177327,   3.5916097 ,   1.49779867,
        -2.33575846,  -6.31604411,  -8.91034342,  -9.51086833,
        -8.18005778,  -5.36041667,  -1.953007  ,   0.96136068,
         2.86901449,   3.93499349,   4.19842122,   3.33056234,
         1.65972493,   0.74547933,   2.02172445,   5.02209066,
         7.80614827,   9.30065511,  10.30517171,  11.59850667,
        11.98052572,   9.45605062,   4.14605306,  -1.0792277 ,
        -3.13251139,  -1.50323893,   1.41357015,   2.59167074,
         1.17711995,  -0.90826823,  -1.3446696 ,  -0.15607096,
         0.42809652,  -1.30798747,  -4.64178874,  -7.15454508,
        -6.66235758,  -2.4866984 ,   4.0646932 ,  10.00890706,
        12.37194417,  10.47057699,   6.67748617,   4.87853597,
         7.77831624,  14.64287923,  21.14220785,  22.29717611,
        16.57891439,   7.16472982,  -0.8290446 ,  -4.08246257,
        -2.64783122,   0.97967122,   4.09350179,   5.7601888 ,
         6.94054769,   8.61254476,  10.13134359,  10.01952718,
         8.35399984,   7.55773519,  10.00194906,  14.97985433,
        19.04436849,  19.74541829,  18.2680013 ,  17.78515218,
        19.73937581,  22.33983968,  22.52843831,  19.21007894,
        14.60204671,  12.10461019,  12.59740804,  13.3381307 ,  10.921993  ]), np.array([-4.54287516, -3.01711833, -1.04525553,  1.39425863,  3.81778158,
        5.36117757,  5.50894368,  4.59878743,  3.50107015,  2.84250081,
        2.55032552,  2.09964193,  1.17886556,  0.05935872, -0.73800456,
       -1.01992594, -1.00851237, -0.96896159, -0.97512614, -0.97775065,
       -0.89944255, -0.71957194, -0.6054362 , -0.84646403, -1.52871501,
       -2.38778483, -3.08187663, -3.50808512, -3.77779948, -3.97720133,
       -4.06728923, -4.03072917, -4.03268229, -4.33120524, -5.00710856,
       -5.84805094, -6.5283488 , -6.86086833, -6.8710612 , -6.70181071,
       -6.49972331, -6.36282145, -6.33675944, -6.428007  , -6.6144694 ,
       -6.84908854, -7.0688151 , -7.21572673, -7.25295817, -7.16659342,
       -6.97598063, -6.7528361 , -6.59652507, -6.54592692, -6.5129069 ,
       -6.33913981, -5.95590007, -5.49966227, -5.24715983, -5.39712321,
       -5.89950358, -6.50570475, -6.97768962, -7.23379313, -7.31912028,
       -7.29043376, -7.14974772, -6.86666667, -6.44851481, -5.993986  ,
       -5.67257487, -5.62020671, -5.83370768, -6.17782389, -6.49996745,
       -6.71981608, -6.8165568 , -6.78463542, -6.64425456, -6.47799479,
       -6.40487467, -6.48892008, -6.68819987, -6.90640055, -7.07223307,
       -7.1611613 , -7.17996012, -7.16091715, -7.15163981]), np.array([-13.33425293, -12.52010498, -10.55117187,  -7.21431885,
        -3.18099365,   0.33048096,   2.69876709,   4.40128174,
         6.00742188,   6.94785156,   5.86459961,   2.2538208 ,
        -2.6713501 ,  -6.92440186,  -9.17061768,  -8.98800049,
        -6.32253418,  -1.63277588,   3.40585938,   6.45731201,
         6.51352539,   4.73477783,   2.80301514,   1.23258057,
        -0.02468262,  -0.26418457,   1.35098877,   4.10056152,
         6.01914063,   6.32126465,   6.34781494,   7.26834717,
         7.86789551,   5.9213623 ,   1.35678711,  -3.06191406,
        -4.25765381,  -1.67086182,   2.18833008,   3.84927979,
         1.90317383,  -1.94716797,  -4.96236572,  -6.15010986,
        -6.63863525,  -7.76387939,  -9.51522217, -10.75435791,
       -10.27675781,  -7.57924805,  -3.25380859,   1.02573242,
         3.35166016,   3.01114502,   1.38760986,   1.45792236,
         5.74527588,  13.69211426,  20.94974365,  22.40860596,
        16.67386475,   7.28006592,  -0.49678955,  -3.59591064,
        -2.51998291,  -0.02486572,   1.3052124 ,   1.02060547,
         0.75870361,   2.00266113,   4.03494873,   4.71079102,
         3.31400146,   1.90921631,   3.24759521,   7.52322998,
        11.82163086,  12.99259033,  10.63181152,   6.91959229,
         4.07211914,   2.57895508,   1.58994141,   0.3956665 ,
        -0.46035156,   0.43717041,   3.43656006,   6.45157471,   6.43057861]), np.array([-11.40517171, -10.63020833,  -9.28139242,  -6.79732259,
        -2.95314535,   1.34604899,   4.38816325,   5.15207926,
         4.10459391,   2.2304484 ,  -0.14662679,  -3.10909017,
        -6.25990804,  -8.75069173, -10.01936849, -10.09956868,
        -9.34883626,  -8.17305501,  -6.85408529,  -5.32430013,
        -3.24550374,  -0.69020589,   1.38621012,   2.00614421,
         1.7892863 ,   3.12168376,   7.88767497,  14.9858195 ,
        20.85447184,  22.88132731,  21.6523234 ,  19.25303141,
        16.22770182,  11.54233805,   5.27079264,  -0.14339193,
        -1.89088949,   0.3731486 ,   3.98716227,   5.63785807,
         4.415507  ,   2.41330973,   2.06101481,   3.21372477,
         3.45884196,   1.10215251,  -2.84584554,  -5.55214437,
        -4.47157796,   1.19199626,   9.82578532,  17.78611247,
        21.46830241,  19.88987223,  15.4222819 ,  12.22532145,
        13.67142741,  19.82865397,  26.57010905,  28.20707194,
        22.27689616,  11.72092692,   2.19327799,  -2.31618245,
        -1.41945394,   2.80411784,   8.05625407,  13.21390788,
        18.01322428,  21.73551432,  22.72715251,  19.78751628,
        14.18857829,   9.75815837,   9.98081462,  14.58072917,
        19.56046549,  21.2514445 ,  20.00828044,  19.36161296,
        21.82633464,  26.11735026,  28.51212565,  26.80137126,
        22.72342936,  20.01774089,  20.02378337,  20.05131022,  16.52195231])]

    return a
    
def get_data():
    """ Returns tuple of data"""
    data= {\
            'McKenzie':                 (-123.1043, 44.1256,    1,  3307033881.96,-122.287768,  44.14907, 1, 1), \
            'Middle Fork Willamette':   (-122.9073, 43.9998,    2,  3482874058.62,-122.39528,	43.757159, 19, 10),\
            'Upper Yamhill':            (-123.1445, 45.2257,    3,  1340602668.23, -123.440166,	45.095052, 21, 11),\
            'Pudding':                  (-122.7162, 45.2976,    4,  2268590002.85,-122.606776,	45.0444, 3, 2),\
            'Clackamas':                (-122.6077, 45.3719,    5,  2434914144.62,-122.088399,	45.11371, 5, 3),\
            'Long Tom':                 (-123.2569, 44.3807,    6,  1050268949.3,-123.309363,	44.088905, 7, 4),\
            'Marys':                    (-123.2615, 44.5564,    7,  778831948.728,-123.429468,	44.504221, 9, 5),\
            'North Santiam':            (-123.1432, 44.7501,    8,  1976850713.48,-122.230379,	44.715461, 11, 6),\
            'South Santiam':            (-123.007,  44.6855,    9,  2694079717.91,-122.522354,	44.517834, 13, 7),\
            'Tualatin':                 (-122.6501, 45.3377,    10, 1829685666.99,-123.052358,	45.538177, 15, 8),\
            'Coast Fork Willamette':    (-123.0082, 44.0208,    11, 1691632167.43,-122.901411,	43.719156, 17, 9),\
            'Willamette':               (-122.7651, 45.6537,    12 , 29728000000., -122.7651,    45.6537, 2, 1)\
            }
    scenarios = {\
            'Reference':                '_Ref_Run0',\
            'HighClim':                 '_HighClim_Run0',\
            'LowClim':                  '_LowClim_Run0',\
            'HighPop':                  '_HighPop_Run0',\
            'UrbExpand':                '_UrbExpand_Run0',\
            'FireSuppress':             '_FireSuppress_Run0',\
            'FullCostUrb':              '_FullCostUrb_Run0'
            }

    return data, scenarios

def getfilenames(data_path, searchword):
    import glob
    files = glob.glob(data_path + '/*.csv')
    filenamelist = []
    fileswopath = [eachfile.partition(data_path)[2] for eachfile in files]    
    for filename in fileswopath:
        if filename.startswith(searchword): filenamelist.append(data_path+filename)
    return filenamelist
    
def ct(water_yr_array):
    """
    Calculate center of timing for each water year in the water_yr_array
    Return CT for each year (vector)
    water_yr_array = array size 365 by water years containing values
    """
    CT = np.zeros_like(range(0, water_yr_array.shape[0]))
    m0 = np.zeros_like(range(0, water_yr_array.shape[0]))
    m1 = np.zeros_like(range(0, water_yr_array.shape[0]))
    m0 = [np.trapz(water_yr_array[i,:], x=None, dx=1.0, axis=-1) for i in range(89)]
    m1 = [np.trapz(np.multiply(water_yr_array[i,:],range(365)), x=None, dx=1.0, axis=-1) for i in range(89)]
    CT = np.divide(m1,m0) + cst.day_of_year_oct1
    return CT

def get_metadata():
    """Add metadata to plot
    """
    import time as timetool, os.path
    textstr = 'Willamette Water 2100' + \
              '\n' + '  Graph generated on ' + str(datetime.date.today()) +\
              '\n' + '  File: ' + file_nm +\
              '\n' + '  Data generated on ' + timetool.ctime(os.path.getctime(file_nm))        
    return textstr
    
def write_tinyfigs(datalist,figsize,mind,maxd,redblue, num_yrs,\
                facecolor='0.8',linewidth = 1.):
    """Write tiny figs to be plotted on map
    """
    from matplotlib import pyplot as plt
    
    for i in range(len(datalist)):
        plt.figure(figsize = figsize[i])
        plt.axis('off')
        plt.ylim( (mind,maxd) )
        plt.fill_between(range(num_yrs),0.,datalist[i],where=datalist[i]>=0., facecolor=redblue[0],lw=0,alpha=0.95) 
        plt.fill_between(range(num_yrs),0.,datalist[i],where=datalist[i]<=0., facecolor=redblue[1],lw=0,alpha=0.95) 
        plt.savefig('tinyfig'+str(i)+'.png', format="png", dpi=300, bbox_inches='tight',transparent=True)
        plt.close()

    return



def interp(x_orig, data, start,stop,num):
    """Interpolate data, returning both x and y values as floats
    """
    x = np.linspace(start,stop,num)
    y = np.interp(x,x_orig,data)
    return x, y

def colorline(x, y, z=None, cmap=plt.get_cmap('copper'), norm=plt.Normalize(0.0, 1.0), linewidth=3, alpha=1.0,maxd=1,mind=0):
    '''
    Plot a colored line with coordinates x and y
    Specify colors in the array = y (could be some other array)
    Optionally specify a colormap, a norm function and a line width
    '''
 # modified from http://nbviewer.ipython.org/github/dpsanders/matplotlib-examples/blob/master/colorline.ipynb    

    points = np.array([x, y]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)   
    lc = LineCollection(segments, array = y, cmap=cmap, norm=norm, linewidth=linewidth, alpha=alpha)
    
    return lc
        
     
        
def write_tinyfigs2(datalist,upper, lower,figsize,mind,maxd,redblue, num_yrs,\
                facecolor='0.8',linewidth = 1.):
    """Write tiny figs to be plotted on map
    """
    from matplotlib import pyplot as plt
    
    if redblue[0] == 'red':
        cmap = ListedColormap(['b','r'])
    else:
        cmap = ListedColormap(['r','b'])
    # Create a 'norm' (normalizing function) which maps data values to the interval [0,1]:
    norm = BoundaryNorm([-1e-3, 0, 1.e-3], cmap.N)  # cmap.N is number of items in the colormap
    
    for i in range(len(datalist)):
        plt.figure(figsize = figsize[i])
        plt.axis('off')
        plt.ylim( (mind,maxd) )
        x,y = interp(range(num_yrs), datalist[i], 0.,float(num_yrs-1),3*num_yrs)
        plt.fill_between(range(num_yrs),upper[i], lower[i], facecolor='0.6',lw=0,alpha=1.)
        lc = colorline(x, y, z=y, cmap=cmap, norm=norm, linewidth=1.5,maxd=maxd,mind=mind)
        plt.gca().add_collection(lc)
        plt.xlim(0,num_yrs)
        plt.savefig('tinyfig'+str(i)+'.png', format="png", dpi=300, bbox_inches='tight',transparent=True)
        plt.close()

    return


def write_legend(data,figsize,mind,maxd,redblue, num_yrs,ylabel,xlabel,\
                facecolor='0.8',linewidth = 1.):
    """Write tiny legend to be plotted on map
    """
    from matplotlib import pyplot as plt

    figleg = plt.figure(figsize=figsize)
    axleg = Subplot(figleg,111)
    figleg.add_subplot(axleg)
    axleg.axis['top'].set_visible(False)
    axleg.axis['bottom'].set_visible(False)
    axleg.axis['right'].set_visible(False)
    yloc = plt.MaxNLocator(5)
    axleg.yaxis.set_major_locator(yloc)
    plt.ylim( (mind,maxd) )
    plt.fill_between(range(num_yrs),0.,data,where=data>=0., facecolor=redblue[0],lw=0,alpha = 0.95) 
    plt.fill_between(range(num_yrs),0.,data,where=data<=0., facecolor=redblue[1],lw=0,alpha = 0.95) 
    font = {'size':'6'}           
    mpl.rc('font', **font)
    plt.ylabel(ylabel, fontsize=6)
    axleg.text(-30., mind*1.5, xlabel, fontsize=6,
            verticalalignment='top')
    plt.savefig('tinyfig'+'12'+'.png', format="png", dpi=300, bbox_inches='tight',transparent=True)
    plt.close()
    mpl.rcdefaults()

    return
    
def write_legend2(data,upper,lower,figsize,mind,maxd,redblue, num_yrs,ylabel,xlabel,\
                facecolor='0.8',linewidth = 1.):
    """Write tiny legend to be plotted on map
    """
    from matplotlib import pyplot as plt

    figleg = plt.figure(figsize=figsize)
    axleg = Subplot(figleg,111)
    figleg.add_subplot(axleg)
    axleg.axis['top'].set_visible(False)
    axleg.axis['bottom'].set_visible(False)
    axleg.axis['right'].set_visible(False)
    yloc = plt.MaxNLocator(5)
    axleg.yaxis.set_major_locator(yloc)
    plt.ylim( (mind,maxd) )
    plt.xlim(0,num_yrs)
    if redblue[0] == 'blue':
        cmap = ListedColormap(['r','b'])
    else:
        cmap = ListedColormap(['b','r'])
        
    norm = BoundaryNorm([-1e-3, 0, 1.e-3], cmap.N)  # cmap.N is number of items in the colormap
    x,y = interp(range(num_yrs), data, 0., float(num_yrs-1), 3*num_yrs)
    plt.fill_between(range(num_yrs),upper, lower, facecolor='0.6',lw=0,alpha=1.)
    lc = colorline(x, y, z=y, cmap=cmap, norm=norm, linewidth=linewidth,maxd=maxd,mind=mind)
    plt.gca().add_collection(lc)
    font = {'size':'6'}           
    mpl.rc('font', **font)
    plt.ylabel(ylabel, fontsize=6)
    axleg.text(-30., mind*1.5, xlabel, fontsize=6,
            verticalalignment='top')
    plt.savefig('tinyfig'+'12'+'.png', format="png", dpi=300, bbox_inches='tight',transparent=True)
    plt.close()
    mpl.rcdefaults()

    return
    
    
def write_map(title, lons, lats, file_graphics, textstr, shp, graphs=range(13)):
    """Write the map
    """
    from matplotlib import pyplot as plt
    
    fig = plt.figure(figsize=(6,8))
    ax2 = fig.add_axes()
    plt.axes(frameon=False)
    
    WBmap=basemap.Basemap(projection='tmerc', llcrnrlat=lat_bounds[0], llcrnrlon=long_bounds[1], 
                urcrnrlat=lat_bounds[1], urcrnrlon=long_bounds[0], ax=ax2, lon_0=-123., lat_0=(77.+34.4)/2.)
#        im = plt.imread('C:\\code\\maplot\\ElevationMap_hi-res.png')
    im = plt.imread('C:\\code\\maplot\\ElevationMap_lt.png')
    WBmap.imshow(im, origin='upper') #interpolation='lanczos', 
    WBmap.readshapefile(shp, 'metadata', drawbounds=True,linewidth=0.25, color='k', )
    
    plt.title(title)
    
    x,y=WBmap(lons,lats)
    
    plt.text(0., 0., textstr, fontsize=3,verticalalignment='top')        
    for i in graphs:
        marker = np.array(Image.open('tinyfig'+str(i)+'.png'))
        im = OffsetImage(marker, zoom=1)
        ab = AnnotationBbox(im, (x[i],y[i]), xycoords='data', frameon=False, box_alignment=(xctr, yctr))
        WBmap._check_ax().add_artist(ab)
#        plt.show()
    plt.savefig(png_path+file_graphics, format="png", dpi=300, bbox_inches='tight')
    plt.close()       

    return

###############################################################################
###############################################################################
###############################################################################

lat_bounds = 43.31342817420548, 45.84870876153576
long_bounds = -121.401130054521,-124.151784119791

subbasin_data, scenarios = get_data()

shp = 'C:\\code\\maplot\\shpf\\Sub_Area_gc'
png_path = 'C:\\code\\maplot pngs\\'
data_path = 'C:\\code\\maplot data\\'

subbasin_data_list = [subbasin_data[key] for key in subbasin_data]
subbasin_data_list = sorted(subbasin_data_list,key=lambda x: x[2])  # order list by column number
subbasin_data_lons = [subbasin_data_list[i][4] for i in range(len(subbasin_data_list))]
subbasin_data_lats = [subbasin_data_list[i][5] for i in range(len(subbasin_data_list))]
subbasin_data_order = [subbasin_data_list[i][2] for i in range(len(subbasin_data_list))]
subbasin_data_area = [subbasin_data_list[i][3] for i in range(len(subbasin_data_list))]
subbasin_data_climate_col = [subbasin_data_list[i][6] for i in range(len(subbasin_data_list))]
subbasin_data_snow_col = [subbasin_data_list[i][7] for i in range(len(subbasin_data_list))]

lons = subbasin_data_lons
lons[11]=subbasin_data_lons[11]+0.2
lons.append(-123.8)
lats = subbasin_data_lats
lats.append(43.9)

figsize=[(0.6,0.6) for i in range(11)]
figsize.append((1.1,0.6))
figsize_leg = (0.6,0.6)

#plots_to_plot = range(4,5)
plots_to_plot = [4,5,70,8,9]
print 'Plots to be plotted are:', '\t', plots_to_plot
for plot_num in plots_to_plot:
    
    
############  Specific Discharge ############    
    if plot_num == 0: 
        fig = plt.figure(figsize=(6,8))
        ax2 = fig.add_axes()
        plt.axes(frameon=False)
        
        WBmap=basemap.Basemap(projection='tmerc', llcrnrlat=lat_bounds[0], llcrnrlon=long_bounds[1], 
                    urcrnrlat=lat_bounds[1], urcrnrlon=long_bounds[0], ax=ax2, lon_0=-123., lat_0=(77.+34.4)/2.)
        im = plt.imread('C:\\code\\maplot\\ElevationMap_hi-res.png')
        WBmap.imshow(im, origin='upper') #interpolation='lanczos', 
        WBmap.readshapefile(shp, 'metadata', drawbounds=True,linewidth=0.25, color='k', )
        plt.title("Specific Discharge")
        file_nm = data_path + 'Discharge_(Subbasins)_Ref_Run0.csv'
        data1=[mfx(file_nm,column=subbasin_data_order[i],skip=cst.day_of_year_oct1) for i in range(12)]
        data1[7] = data1[7] - data1[8]  # correct N Santiam for S Santiam contribution
        data1_spQ=[np.mean(data1[i])/subbasin_data_area[i]*cst.seconds_in_yr*100. for i in range(12)]
        summer_Q = [nrc(data1[i],[1,260],[88,350]) for i in range(12)]
        
        import heapq
        data1_2nd_lgst = heapq.nlargest(2, summer_Q)[1]  #find second-largest number
        data1_size = np.clip(200.*np.array(summer_Q)/data1_2nd_lgst,30.,20000.)
        
        colord = np.array(data1_spQ)
        
        x,y=WBmap(subbasin_data_lons,subbasin_data_lats)
        cmap1 = mpl.colors.LinearSegmentedColormap.from_list('my_cmap',['white','blue'],128)
        WBmap.scatter(x, y, marker='o',  s=data1_size, lw=0,c=colord,cmap = cmap1)
        
        file_graphics = 'spQ.png'     
        plt.text(0., 0, get_metadata(), fontsize=3,
                verticalalignment='top')        
        #plt.show()
        plt.savefig(png_path+file_graphics, format="png", dpi=300, bbox_inches='tight')
        plt.close()       
        
############  Summer Hydrologic Drought ############    
    elif plot_num == 1:
        fig = plt.figure(figsize=(6,8))
        ax2 = fig.add_axes()
        plt.axes(frameon=False)
        
        WBmap=basemap.Basemap(projection='tmerc', llcrnrlat=lat_bounds[0], llcrnrlon=long_bounds[1], 
                    urcrnrlat=lat_bounds[1], urcrnrlon=long_bounds[0], ax=ax2, lon_0=-123., lat_0=(77.+34.4)/2.)
        im = plt.imread('C:\\code\\maplot\\ElevationMap_hi-res.png')
        WBmap.imshow(im, origin='upper') #interpolation='lanczos', 
        WBmap.readshapefile(shp, 'metadata', drawbounds=True,linewidth=0.25, color='k', )
        
        plt.title("Change in Summer Hydrologic Drought")
        
        file_nm = data_path + 'Discharge_(Subbasins)_Ref_Run0.csv'

        data1=[mfx(file_nm, column=subbasin_data_order[i], skip=cst.day_of_year_oct1,
                   movingaveragevec=np.ones(30)/30.) for i in range(12)]
        data1[7] = data1[7] - data1[8]  # correct N Santiam for S Santiam contribution
        data_hd1 = data1
        
        data1=[mfx(file_nm.replace('_Ref_','_HighClim_'), column=subbasin_data_order[i], skip=cst.day_of_year_oct1,
                   movingaveragevec=np.ones(30)/30.) for i in range(12)]
        data1[7] = data1[7] - data1[8]  # correct N Santiam for S Santiam contribution
        data_hd2 = data1
        
        data1=[mfx(file_nm.replace('_Ref_','_LowClim_'), column=subbasin_data_order[i], skip=cst.day_of_year_oct1,
                   movingaveragevec=np.ones(30)/30.) for i in range(12)]
        data1[7] = data1[7] - data1[8]  # correct N Santiam for S Santiam contribution
        data_hd3 = data1
        
        data_avg = [(data_hd1[i]+data_hd2[i]+data_hd3[i])/3. for i in range(12)]
        Q10 = [np.percentile(data_avg[i][0:10,:], 10.,axis=0) for i in range(12)]
        data_hd_binary = [compare_rows(data_avg[i],Q10[i]) for i in range(12)]  #1's are drought
        
        diff_drought_days = [
                       nrc(data_hd_binary[i],[69,260],[88,350], oper='sum') \
                    -  nrc(data_hd_binary[i],[0, 260],[19,350], oper='sum') \
                    for i in range(12)]  #+ve numbers are increasing drought
       
        colord = np.array(diff_drought_days)
        
        x,y=WBmap(subbasin_data_lons,subbasin_data_lats)
        cmap1 = mpl.colors.LinearSegmentedColormap.from_list('my_cmap',['blue','white','red'],128)
        WBmap.scatter(x, y, marker='o',  s=data1_size, lw=0,c=colord,cmap = cmap1)
        
        file_graphics = 'drought_days.png'        
        plt.text(0., 0, get_metadata(), fontsize=3,
                verticalalignment='top')        
        #plt.show()
        plt.savefig(png_path+file_graphics, format="png", dpi=300, bbox_inches='tight')
        plt.close()       



############  Precipitation ############    
    elif plot_num == 2:
        fig = plt.figure(figsize=(6,8))
        ax2 = fig.add_axes()
        plt.axes(frameon=False)
        
        WBmap=basemap.Basemap(projection='tmerc', llcrnrlat=lat_bounds[0], llcrnrlon=long_bounds[1], 
                    urcrnrlat=lat_bounds[1], urcrnrlon=long_bounds[0], ax=ax2, lon_0=-123., lat_0=(77.+34.4)/2.)
        im = plt.imread('C:\\code\\maplot\\ElevationMap_hi-res.png')
        WBmap.imshow(im, origin='upper') #interpolation='lanczos', 
        WBmap.readshapefile(shp, 'metadata', drawbounds=True,linewidth=0.25, color='k', )
        
        plt.title("Change in Annual Precipitation")
        
        file_nm = data_path + 'Climate_(Subbasin)_Ref_Run0.csv'
        data1=[mfx(file_nm, column=subbasin_data_climate_col[i], skip=cst.day_of_year_oct1) for i in range(11)]
        file_nmWB = data_path + 'Climate_Ref_Run0.csv'
        data1.append(mfx(file_nmWB, column=subbasin_data_climate_col[11], skip=cst.day_of_year_oct1))
        data_hd1 = data1
        
        diff_ann_precip = [
                    + nrc(data_hd1[i],[0,0],[19,364], oper='avg') \
                    - nrc(data_hd1[i],[69, 0],[88,364], oper='avg') \
                    for i in range(12)]  # +ve numbers are decreasing precip
        print nrc(data_hd1[0],[0,0],[19,364], oper='avg')
        print nrc(data_hd1[0],[69, 0],[88,364], oper='avg')
        print diff_ann_precip
       
        colord = np.array(diff_ann_precip)
        
        x,y=WBmap(subbasin_data_lons,subbasin_data_lats)
        cmap1 = mpl.colors.LinearSegmentedColormap.from_list('my_cmap',['blue','white'],128)
        WBmap.scatter(x, y, marker='o',  s=data1_size, lw=0,c=colord,cmap = cmap1)
        
        file_graphics = 'diff_ann_precip.png'        
        plt.text(0., 0, get_metadata(), fontsize=3,
                verticalalignment='top')        
        #plt.show()
        plt.savefig(png_path+file_graphics, format="png", dpi=300, bbox_inches='tight')
        plt.close()       



############  Winter Temperature ############    
    elif plot_num == 3:
        fig = plt.figure(figsize=(6,8))
        ax2 = fig.add_axes()
        plt.axes(frameon=False)
        
        WBmap=basemap.Basemap(projection='tmerc', llcrnrlat=lat_bounds[0], llcrnrlon=long_bounds[1], 
                    urcrnrlat=lat_bounds[1], urcrnrlon=long_bounds[0], ax=ax2, lon_0=-123., lat_0=(77.+34.4)/2.)
        im = plt.imread('C:\\code\\maplot\\ElevationMap_hi-res.png')
        WBmap.imshow(im, origin='upper') #interpolation='lanczos', 
        WBmap.readshapefile(shp, 'metadata', drawbounds=True,linewidth=0.25, color='k', )
        
        plt.title("Change in Winter (Nov 1 - Mar 31) Temp")
        
        file_nm = data_path + 'Climate_(Subbasin)_Ref_Run0.csv'
        data1=[mfx(file_nm, column=subbasin_data_climate_col[i]+1, skip=cst.day_of_year_oct1) for i in range(11)]
        file_nmWB = data_path + 'Climate_Ref_Run0.csv'
        data1.append(mfx(file_nmWB, column=subbasin_data_climate_col[11]-1, skip=cst.day_of_year_oct1))
        data_hd1 = data1
        
        diff_winter_temp = [
                      nrc(data_hd1[i],[69,31],[88,182], oper='avg') \
                    - nrc(data_hd1[i],[0, 31],[19,182], oper='avg') \
                    for i in range(12)]  #+ve numbers are increasing temp
        print 'early cent', '\t',nrc(data_hd1[i],[69,31],[88,182], oper='avg')
        print 'late cent', '\t',nrc(data_hd1[i],[0, 31],[19,182], oper='avg')
        print np.array(diff_winter_temp)
       
        colord = np.array(diff_winter_temp)
        
        x,y=WBmap(subbasin_data_lons,subbasin_data_lats)
        cmap1 = mpl.colors.LinearSegmentedColormap.from_list('my_cmap',['white','red'],128)
        WBmap.scatter(x, y, marker='o',  s=200., lw=0,c=colord,cmap = cmap1)
        
        file_graphics = 'diff_winter_Temp.png'        
        plt.text(0., 0, get_metadata(), fontsize=3,
                verticalalignment='top')        
        #plt.show()
        plt.savefig(png_path+file_graphics, format="png", dpi=300, bbox_inches='tight')
        plt.close()       




############  Summer Hydrologic Drought w mini figs/LINES & SHADING ############    
    elif plot_num == 4:
        plt.close()
        
        # Calculate Baseline
        file_nm = data_path + 'Discharge_(Subbasins)_Ref_Run0.csv'       
        data1=[mfx(file_nm, column=subbasin_data_order[i], skip=cst.day_of_year_oct1,
                   movingaveragevec=np.ones(30)/30.) for i in range(12)]
        data1[7] = data1[7] - data1[8]  # correct N Santiam for S Santiam contribution
        data_hd1 = data1
        
        data1=[mfx(file_nm.replace('_Ref_','_HighClim_'), column=subbasin_data_order[i], skip=cst.day_of_year_oct1,
                   movingaveragevec=np.ones(30)/30.) for i in range(12)]
        data1[7] = data1[7] - data1[8]  # correct N Santiam for S Santiam contribution
        data_hd2 = data1
        
        data1=[mfx(file_nm.replace('_Ref_','_LowClim_'), column=subbasin_data_order[i], skip=cst.day_of_year_oct1,
                   movingaveragevec=np.ones(30)/30.) for i in range(12)]
        data1[7] = data1[7] - data1[8]  # correct N Santiam for S Santiam contribution
        data_hd3 = data1
        
        data_avg = [(data_hd1[i]+data_hd2[i]+data_hd3[i])/3. for i in range(12)]
        Q10 = [np.percentile(data_avg[i][0:10,:], 10.,axis=0) for i in range(12)]
        data_hd_binary = [compare_rows(data_hd1[i],Q10[i]) for i in range(12)]  #1's are drought
        
        summer_dr_d = [np.sum(data_hd_binary[i][:,260:351],1) for i in range(12)]
        baseline = [np.mean(summer_dr_d[i][:30]) for i in range(12)]
        
        # Calculate baseline-subtracted value
        window = binomial_window(15)
        summer_dr_d_smthd = [np.subtract(movingaverage(summer_dr_d[i],window), baseline[i]) for i in range(12)]
        
        data_to_stack = []
        for key in scenarios:
            data_hd1=[mfx(file_nm.replace('_Ref_Run0',scenarios[key]), column=subbasin_data_order[i], skip=cst.day_of_year_oct1,
                       movingaveragevec=np.ones(30)/30.) for i in range(12)]
            data_hd1[7] = data_hd1[7] - data_hd1[8]  # correct N Santiam for S Santiam contribution
            data_hd_binary = [compare_rows(data_hd1[i],Q10[i]) for i in range(12)]  #1's are drought
            summer_dr_d = [np.sum(data_hd_binary[i][:,260:351],1) for i in range(12)]
            data_to_stack.append([np.subtract(movingaverage(summer_dr_d[i],window), baseline[i]) for i in range(12)])  
        
        data_to_stack = [tuple([data_to_stack[j][i] for j in range(len(data_to_stack))]) for i in range(12)]
        
        data_stacked = [np.column_stack(data_to_stack[i]) for i in range(12)] 
        upper = [np.max(data_stacked[i],1) for i in range(12)]
        lower = [np.min(data_stacked[i],1) for i in range(12)]
        
        maxd = np.max(np.array([np.max(upper[i]) for i in range(12)]))
        mind = np.min(np.array([np.min(lower[i]) for i in range(12)]))
        xctr = 0.5
        yctr = 0.5
        
        redblue = ['red','blue']
        num_yrs = len(summer_dr_d_smthd[0])
        write_tinyfigs2(summer_dr_d_smthd,upper, lower, figsize,
                        mind,maxd,redblue, num_yrs, facecolor = '0.6',
                        linewidth = 1.5)
        
        ylabel = r'$\Delta \, Drought\,$ [days]'
        xlabel = 'Red = Drier'
        write_legend2(summer_dr_d_smthd[0], upper[0], lower[0],figsize_leg,
                      mind,maxd,redblue,num_yrs,ylabel,xlabel, facecolor='0.6',
                      linewidth=1.5)
               
        title = "Change in Summer Hydrologic Drought"
        file_graphics = 'change_in_drought_days_wGrphs.png'

        write_map(title, lons, lats, file_graphics, get_metadata(), shp)



############  Winter Temperature w mini figs ############    
    elif plot_num == 5:
        plt.close()
        file_nm = data_path + 'Climate_(Subbasin)_Ref_Run0.csv'
        file_nmWB = data_path + 'Climate_Ref_Run0.csv'
       
        # Calculate Baseline
        data1=[mfx(file_nm, column=subbasin_data_climate_col[i]+1, skip=cst.day_of_year_oct1) for i in range(11)]
        data1.append(mfx(file_nmWB, column=subbasin_data_climate_col[11]-1, skip=cst.day_of_year_oct1))
        data_hd1 = data1
        data_winter = [data_hd1[i][:,29:182] for i in range(12)]
        winter_tmps = [np.mean(data_winter[i],1) for i in range(12)]  # avg over winter each year for ea subbasin
        
        data1=[mfx(file_nm.replace('_Ref_','_HighClim_'), column=subbasin_data_climate_col[i]+1, skip=cst.day_of_year_oct1)
                   for i in range(11)]
        data1.append(mfx(file_nmWB.replace('_Ref_','_HighClim_'), column=subbasin_data_climate_col[11]-1, skip=cst.day_of_year_oct1))
        data_hd2 = data1
        
        data1=[mfx(file_nm.replace('_Ref_','_LowClim_'), column=subbasin_data_climate_col[i]+1, skip=cst.day_of_year_oct1)
                   for i in range(11)]
        data1.append(mfx(file_nmWB.replace('_Ref_','_LowClim_'), column=subbasin_data_climate_col[11]-1, skip=cst.day_of_year_oct1))
        data_hd3 = data1
        
        data_avg = [(data_hd1[i]+data_hd2[i]+data_hd3[i])/3. for i in range(12)]
        baseline = [nrc(data_avg[i],[0, 10],[29,182]) for i in range(12)]  
                
        window = binomial_window(15)
        winter_temps_smthd = [np.subtract(movingaverage(winter_tmps[i],window), baseline[i])[8:83] for i in range(12)]
        
        data_to_stack = []
        for key in scenarios:
            data_hd1=[mfx(file_nm.replace('_Ref_Run0',scenarios[key]), column=subbasin_data_climate_col[i]+1, skip=cst.day_of_year_oct1) for i in range(11)]
            data_hd1.append(mfx(file_nmWB.replace('_Ref_Run0',scenarios[key]), column=subbasin_data_climate_col[11]-1, skip=cst.day_of_year_oct1))
            data_winter = [data_hd1[i][:,29:182] for i in range(12)]
            winter_tmps = [np.mean(data_winter[i],1) for i in range(12)]  # avg over winter each year for ea subbasin
            winter_temps_smthd1 = [np.subtract(movingaverage(winter_tmps[i],window), baseline[i])[8:83] for i in range(12)]
            data_to_stack.append([winter_temps_smthd1[i] for i in range(12)])  
                
        data_to_stack = [tuple([data_to_stack[j][i] for j in range(len(data_to_stack))]) for i in range(12)]
        
        data_stacked = [np.column_stack(data_to_stack[i]) for i in range(12)] 
        upper = [np.max(data_stacked[i],1) for i in range(12)]
        lower = [np.min(data_stacked[i],1) for i in range(12)]
        
        maxd = np.max(np.array([np.max(upper[i]) for i in range(12)]))
        mind = np.min(np.array([np.min(lower[i]) for i in range(12)]))
        xctr = 0.5
        yctr = 0.5

        redblue = ['red','blue']
        num_yrs = len(winter_temps_smthd[0])
        write_tinyfigs2(winter_temps_smthd,upper, lower, figsize,
                        mind,maxd,redblue, num_yrs, facecolor = '0.6',
                        linewidth = 1.5)
        
        ylabel = r'$\Delta \, Temp\,$ [$^{\circ}\mathrm{C}$]'
        xlabel = 'Red = Warmer'
        write_legend2(winter_temps_smthd[0], upper[0], lower[0],figsize_leg,
                      mind,maxd,redblue,num_yrs,ylabel,xlabel, facecolor='0.6',
                      linewidth=1.5)
        
        title = "Change in Winter Temperatures (Nov - Mar)"
        file_graphics = 'change_in_winter_temp_wGrphs.png'

        write_map(title, lons, lats, file_graphics, get_metadata(), shp)




############  Econ w mini figs ############    
    elif plot_num == 6:
        plt.close()
        
        econ_files = getfilenames(data_path,'subbasin')
        econ_fileswopath = [eachfile.partition(data_path)[2] for eachfile in econ_files]
        for file_nm in econ_files:
#            file_nm=data_path+'subbasin_tot_ac_of_developed_land_by_SUB_AREA_EarlyReFill_Run0.csv'
            file_nmWB = file_nm     
            title = file_nm.partition(data_path)[2][:-4]
            png_file_nm = title+'.png'
            data_v = np.array(np.genfromtxt(file_nm, delimiter=',',skip_header=1)) # Read csv file
            data1 = [data_v[2:,subbasin_data_order[i]+1] for i in range(11)]
            data1.append(data_v[2:,1])
            data1 = [np.subtract(data1[i],data1[i][0]) for i in range(11)]
            maxd = np.max(np.array([np.max(data1[i]) for i in range(11)]))
            mind = np.min(np.array([np.min(data1[i]) for i in range(11)]))
            if maxd >= abs(mind):
                xctr = 0.75
                yctr = 0.5
            else:
                xctr = 0.75
                yctr = 0.7
                
            redblue = ['red','blue']
            num_yrs = len(data1[0])
            write_tinyfigs(data1,figsize,mind,maxd,redblue, num_yrs)
            
            ylabel = r'$\Delta \, value\,$'
            xlabel = ' '
            write_legend(data1[4],figsize_leg,mind,maxd,redblue,num_yrs,ylabel,xlabel)
            
            file_graphics = png_file_nm        
    
            graphs = range(11)
            graphs.append(12)
            write_map(title, lons, lats, file_graphics, get_metadata(), shp, graphs=graphs)
            
#            assert False
            
            
            
            
            
############  Econ w mini figs normalized by land area ############    
    elif plot_num == 7:
        plt.close()
        run_names = [\
        ('subbasin_tot_LR_farm_rent_by_SUB_AREA_Ref_Run0.csv','subbasin_tot_ac_of_ag_land_by_SUB_AREA_Ref_Run0.csv'),\
        ('subbasin_tot_SR_farm_rent_by_SUB_AREA_Ref_Run0.csv','subbasin_tot_ac_of_ag_land_by_SUB_AREA_Ref_Run0.csv'),\
        ('subbasin_tot_LR_farm_rent_irrigable_GW_by_SUB_AREA_Ref_Run0.csv','subbasin_tot_ac_of_irrigable_ag_land_GW_by_SUB_AREA_Ref_Run0.csv'),\
        ('subbasin_tot_SR_farm_rent_irrigable_GW_by_SUB_AREA_Ref_Run0.csv','subbasin_tot_ac_of_irrigable_ag_land_GW_by_SUB_AREA_Ref_Run0.csv'),\
        ('subbasin_tot_LR_farm_rent_irrigable_SW_by_SUB_AREA_Ref_Run0.csv','subbasin_tot_ac_of_irrigable_ag_land_SW_by_SUB_AREA_Ref_Run0.csv'),\
        ('subbasin_tot_SR_farm_rent_irrigable_SW_by_SUB_AREA_Ref_Run0.csv','subbasin_tot_ac_of_irrigable_ag_land_SW_by_SUB_AREA_Ref_Run0.csv')\
        ]
        
        for key in scenarios:
            
            for files in run_names:
                files_scen = (files[0].replace(scenarios['Reference'],scenarios[key]),files[1].replace(scenarios['Reference'],scenarios[key]))
                print files_scen
                title = files_scen[0][:-4]
                file_nm_num = data_path + files_scen[0]
                file_nm_denom = data_path + files_scen[1]
                file_nmWB = file_nm_num     
                png_file_nm = title+'_divided_by_area'+'.png'
                data_v_num = np.array(np.genfromtxt(file_nm_num, delimiter=',',skip_header=1)) # Read csv file
                data_v_denom = np.array(np.genfromtxt(file_nm_denom, delimiter=',',skip_header=1)) # Read csv file
                data1_num = [data_v_num[2:,subbasin_data_order[i]+1] for i in range(11)]
                data1_denom = [data_v_denom[2:,subbasin_data_order[i]+1] for i in range(11)]
                data1_num.append(data_v[2:,1])
                data1_denom.append(data_v[2:,1])
                data1 = [np.divide(data1_num[i],data1_denom[i]) for i in range(11)]
                data1 = [np.subtract(data1[i],data1[i][0]) for i in range(11)]
                maxd = np.max(np.array([np.max(data1[i]) for i in range(11)]))
                mind = np.min(np.array([np.min(data1[i]) for i in range(11)]))
                if maxd >= abs(mind):
                    xctr = 0.75
                    yctr = 0.5
                else:
                    xctr = 0.75
                    yctr = 0.7
                    
                redblue = ['red','blue']
                num_yrs = len(data1[0])
                write_tinyfigs(data1,figsize,mind,maxd,redblue, num_yrs)
                
                ylabel = r'$\Delta \, Value\,$' +r'[\$/ac]'
                xlabel = ' '
                write_legend(data1[4],figsize_leg,mind,maxd,redblue,num_yrs,ylabel,xlabel)
                
                file_graphics = png_file_nm        
        
                graphs = range(11)
                graphs.append(12)
                write_map(title, lons, lats, file_graphics, get_metadata(), shp, graphs=graphs)
                
#                assert False
            
            
            
            
############  Econ w mini figs normalized by land area ############    
    elif plot_num == 70:
        plt.close()
        run_names = [\
        ('subbasin_tot_LR_farm_rent_by_SUB_AREA_Ref_Run0.csv','subbasin_tot_ac_of_ag_land_by_SUB_AREA_Ref_Run0.csv'),\
        ('subbasin_tot_SR_farm_rent_by_SUB_AREA_Ref_Run0.csv','subbasin_tot_ac_of_ag_land_by_SUB_AREA_Ref_Run0.csv'),\
        ('subbasin_tot_LR_farm_rent_irrigable_GW_by_SUB_AREA_Ref_Run0.csv','subbasin_tot_ac_of_irrigable_ag_land_GW_by_SUB_AREA_Ref_Run0.csv'),\
        ('subbasin_tot_SR_farm_rent_irrigable_GW_by_SUB_AREA_Ref_Run0.csv','subbasin_tot_ac_of_irrigable_ag_land_GW_by_SUB_AREA_Ref_Run0.csv'),\
        ('subbasin_tot_LR_farm_rent_irrigable_SW_by_SUB_AREA_Ref_Run0.csv','subbasin_tot_ac_of_irrigable_ag_land_SW_by_SUB_AREA_Ref_Run0.csv'),\
        ('subbasin_tot_SR_farm_rent_irrigable_SW_by_SUB_AREA_Ref_Run0.csv','subbasin_tot_ac_of_irrigable_ag_land_SW_by_SUB_AREA_Ref_Run0.csv')\
        ]
        
            
        for files in run_names:
            data_to_stack = []
            title = files[0][:-13]
            print title
            for key in scenarios:
                files_scen = (files[0].replace(scenarios['Reference'],scenarios[key]),files[1].replace(scenarios['Reference'],scenarios[key]))
                file_nm_num = data_path + files_scen[0]
                file_nm_denom = data_path + files_scen[1]
                file_nmWB = file_nm_num     
                png_file_nm = title+'_divided_by_area'+'.png'
                data_v_num = np.array(np.genfromtxt(file_nm_num, delimiter=',',skip_header=1)) # Read csv file
                data_v_denom = np.array(np.genfromtxt(file_nm_denom, delimiter=',',skip_header=1)) # Read csv file
                data1_num = [data_v_num[2:,subbasin_data_order[i]+1] for i in range(11)]
                data1_denom = [data_v_denom[2:,subbasin_data_order[i]+1] for i in range(11)]
#                data1_num.append(data_v_num)
#                data1_denom.append(data_v_denom)
                data1 = [np.divide(data1_num[i],data1_denom[i]) for i in range(11)]
                data1 = [np.subtract(data1[i],data1[i][0]) for i in range(11)]
                data_to_stack.append([data1[i] for i in range(11)])  
                
            data_to_stack = [tuple([data_to_stack[j][i] for j in range(len(data_to_stack))]) for i in range(11)]
            
            data_stacked = [np.column_stack(data_to_stack[i]) for i in range(11)] 
            upper = [np.max(data_stacked[i],1) for i in range(11)]
            lower = [np.min(data_stacked[i],1) for i in range(11)]
            
            maxd = np.max(np.array([np.max(upper[i]) for i in range(11)]))
            mind = np.min(np.array([np.min(lower[i]) for i in range(11)]))
            if maxd >= abs(mind):
                xctr = 0.75
                yctr = 0.5
            else:
                xctr = 0.75
                yctr = 0.7
                
            redblue = ['red','blue']
            num_yrs = len(data1[0])
            write_tinyfigs2(data1,upper, lower, figsize, mind,maxd,redblue, 
                            num_yrs, facecolor='0.6', linewidth = 1.5)
            
            ylabel = r'$\Delta \, Value\,$' +r'[\$/ac]'
            xlabel = ' '
            write_legend2(data1[4],upper[4], lower[4], figsize_leg,
                          mind,maxd,redblue,num_yrs,ylabel,xlabel, facecolor='0.6',
                          linewidth=1.5)
            
            file_graphics = png_file_nm        
    
            graphs = range(11)
            graphs.append(12)
            write_map(title, lons, lats, file_graphics, get_metadata(), shp, graphs=graphs)
            
            
            
            
############  Center of Timing w mini figs ############    
    elif plot_num == 8:
        file_nm = data_path + 'Discharge_(Subbasins)_Ref_Run0.csv'
       
        plt.close()
        
        # Calculate Baseline
        data1=[mfx(file_nm, column=subbasin_data_order[i], skip=cst.day_of_year_oct1) for i in range(12)]
        data1[7] = data1[7] - data1[8]  # correct N Santiam for S Santiam contribution
        data_hd1 = data1
        
        data1=[mfx(file_nm.replace('_Ref_','_HighClim_'), column=subbasin_data_order[i], 
                   skip=cst.day_of_year_oct1) for i in range(12)]
        data1[7] = data1[7] - data1[8]  # correct N Santiam for S Santiam contribution
        data_hd2 = data1
        
        data1=[mfx(file_nm.replace('_Ref_','_LowClim_'), column=subbasin_data_order[i], 
                   skip=cst.day_of_year_oct1) for i in range(12)]
        data1[7] = data1[7] - data1[8]  # correct N Santiam for S Santiam contribution
        data_hd3 = data1
        
        data_avg = [(data_hd1[i]+data_hd2[i]+data_hd3[i])/3. for i in range(12)]
        ctList = [np.array(ct(data_avg[i])) for i in range(12)]
        ctdata_hd1 = [np.array(ct(data_hd1[i])) for i in range(12)]
        
        baseline = [np.mean(ctList[i][:30]) for i in range(12)]
        
        window = binomial_window(15)
        delta_discharge_timing = [-1.*np.subtract(movingaverage(ctdata_hd1[i],window), baseline[i]) for i in range(12)]
        
        data_to_stack = []
        for key in scenarios:
            data1=[mfx(file_nm.replace('_Ref_Run0',scenarios[key]), column=subbasin_data_order[i], skip=cst.day_of_year_oct1) for i in range(12)]
            data1[7] = data1[7] - data1[8]  # correct N Santiam for S Santiam contribution
            ctdata = [np.array(ct(data1[i])) for i in range(12)]
            delta_discharge_timing = [-1.*np.subtract(movingaverage(ctdata[i],window), baseline[i]) for i in range(12)]
            data_to_stack.append([delta_discharge_timing[i] for i in range(12)])  

        data_to_stack = [tuple([data_to_stack[j][i] for j in range(len(data_to_stack))]) for i in range(12)]
        
        data_stacked = [np.column_stack(data_to_stack[i]) for i in range(12)] 
        upper = [np.max(data_stacked[i][8:83],1) for i in range(12)]
        lower = [np.min(data_stacked[i][8:83],1) for i in range(12)]
            
        maxd = np.max(np.array([np.max(upper[i]) for i in range(12)]))
        mind = np.min(np.array([np.min(lower[i]) for i in range(12)]))
        delta_discharge_timing = np.array([delta_discharge_timing[i][8:83] for i in range(12)])

        redblue = ['red','blue']
        num_yrs = len(delta_discharge_timing[0])
        write_tinyfigs2(delta_discharge_timing, upper, lower, figsize,
                        mind,maxd,redblue, num_yrs, facecolor = '0.6',
                        linewidth = 1.5)
        
        ylabel = r'$\Delta \, CT\,$ [days]'
        xlabel = 'Red = Earlier'
        write_legend2(delta_discharge_timing[0], upper[0], lower[0],figsize_leg,
                      mind,maxd,redblue,num_yrs,ylabel,xlabel, facecolor='0.6',
                      linewidth=1.5)
            
        title = "Change in Timing of Discharge (CT)"
        file_graphics = 'change_in_discharge_timing_wGrphs.png'        

        write_map(title, lons, lats, file_graphics, get_metadata(), shp)
            
            
            
            
############  Max SWE w mini figs ############    
    elif plot_num == 9:
        plt.close()
        
        # Calculate Baseline
        file_nm = data_path + 'Snow_(Subbasin)_Ref_Run0.csv'
        file_nmWB = data_path + 'Snow_(mm)_Ref_Run0.csv'
       
        data1=[mfx(file_nm, column=subbasin_data_snow_col[i], skip=cst.day_of_year_oct1) for i in range(11)]
        data1.append(mfx(file_nmWB, column=subbasin_data_snow_col[11], skip=cst.day_of_year_oct1))
        SWE1 = [np.max(data1[i],1)*subbasin_data_area[i]/10./subbasin_data_area[11] for i in range(12)]  # max SWE (cm) over winter each year for ea subbasin
        
        data1=[mfx(file_nm.replace('_Ref_','_HighClim_'), column=subbasin_data_snow_col[i], skip=cst.day_of_year_oct1)
                   for i in range(11)]
        data1.append(mfx(file_nmWB.replace('_Ref_','_HighClim_'), column=subbasin_data_snow_col[11], skip=cst.day_of_year_oct1))
        SWE2 = [np.max(data1[i],1)*subbasin_data_area[i]/10./subbasin_data_area[11] for i in range(12)]  # max SWE (cm) over winter each year for ea subbasin
        
        data1=[mfx(file_nm.replace('_Ref_','_LowClim_'), column=subbasin_data_snow_col[i], skip=cst.day_of_year_oct1)
                   for i in range(11)]
        data1.append(mfx(file_nmWB.replace('_Ref_','_LowClim_'), column=subbasin_data_snow_col[11], skip=cst.day_of_year_oct1))
        SWE3 = [np.max(data1[i],1)*subbasin_data_area[i]/10./subbasin_data_area[11] for i in range(12)]  # max SWE (cm) over winter each year for ea subbasin
        
        SWE_avg = [(SWE1[i]+SWE2[i]+SWE3[i])/3. for i in range(12)]
        baseline = [np.mean(SWE_avg[i][0:10]) for i in range(12)]  #1's are drought
                
        # Calculate baseline-subtracted value
        window = binomial_window(15)
        SWE_smthd = [np.subtract(movingaverage(SWE1[i],window), baseline[i]) for i in range(12)]
        
        data_to_stack = []
        for key in scenarios:
            data1=[mfx(file_nm.replace('_Ref_Run0',scenarios[key]), column=subbasin_data_snow_col[i], 
                       skip=cst.day_of_year_oct1) for i in range(11)]
            data1.append(mfx(file_nmWB.replace('_Ref_Run0',scenarios[key]), 
                             column=subbasin_data_snow_col[11], skip=cst.day_of_year_oct1))
            SWE1 = [np.max(data1[i],1)*subbasin_data_area[i]/10./subbasin_data_area[11] for i in range(12)]  # max SWE (cm) over winter each year for ea subbasin
            data_to_stack.append([np.subtract(movingaverage(SWE1[i],window), baseline[i]) for i in range(12)])  

        data_to_stack = [tuple([data_to_stack[j][i] for j in range(len(data_to_stack))]) for i in range(12)]
        data_stacked = [np.column_stack(data_to_stack[i]) for i in range(12)] 
        upper = [np.max(data_stacked[i][8:83],1) for i in range(12)]
        lower = [np.min(data_stacked[i][8:83],1) for i in range(12)]
            
        maxd = np.max(np.array([np.max(upper[i]) for i in range(12)]))
        mind = np.min(np.array([np.min(lower[i]) for i in range(12)]))
        SWE_smthd = [SWE_smthd[i][8:83] for i in range(12)]
        xctr = 0.5
        yctr = 0.75
        
        redblue = ['blue','red']
        num_yrs = len(SWE_smthd[0])
        write_tinyfigs2(SWE_smthd, upper, lower, figsize,
                        mind,maxd,redblue, num_yrs, facecolor = '0.6',
                        linewidth = 1.5)
        
        ylabel = r'$\Delta \, SWE\,$ [cm]'
        xlabel = 'Red = Less SWE'
        write_legend2(SWE_smthd[0], upper[0], lower[0],figsize_leg,
                      mind,maxd,redblue,num_yrs,ylabel,xlabel, facecolor='0.6',
                      linewidth=1.5)
               
        
        title = "Change in Basin-Averaged Max SWE"
        file_graphics = 'change_in_max_SWE_wGrphs.png'        

        write_map(title, lons, lats, file_graphics, get_metadata(), shp)
       
