from pos_tagging import pos_tagging
from DeviceSelection import DeviceSelection
from time import time

#Testing pos_tagging
R=('Noun', 'Modal', 'Verb')
S=('Will', 'Mary', 'Spot', 'Jane')
T=dict()
T['Start']={'Noun': 3/4, 'Modal': 1/4, 'Verb': 0, 'End': 0}
T['Noun']={'Noun': 1/9, 'Modal': 3/9, 'Verb': 1/9, 'End': 4/9}
T['Modal']={'Noun': 1/4, 'Modal': 0, 'Verb': 3/4, 'End': 0}
T['Verb']={'Noun': 1, 'Modal': 0, 'Verb': 0, 'End': 0}
E=dict()
E['Will']={'Noun': 1/4, 'Modal': 3/4, 'Verb': 0}
E['Mary']={'Noun': 1, 'Modal': 0, 'Verb': 0}
E['Spot']={'Noun': 1/2, 'Modal': 0, 'Verb': 1/2}
E['Jane']={'Noun': 1, 'Modal': 0, 'Verb': 0}
out={'Will': 'Modal', 'Mary': 'Noun', 'Spot': 'Verb', 'Jane': 'Noun'}

start = time()
sol = pos_tagging(R, S, T, E)
end = time()-start

if sol != out:
    print('FAIL')
else:
    print('True')
    print(end)

#Testing DeviceSelection

X = 7
#data = {'Device 1': (100, 99, 85, 77, 63), 'Device 2': (101, 88, 82, 75, 60), 'Device 3': (98, 89, 84, 76, 61), 'Device 4': (110, 65, 65, 67, 80), 'Device 5': (95, 80, 80, 63, 60)}
#partition = [['Device 1', 'Device 3', 'Device 5'], ['Device 2'], ['Device 4']]
#data = {'Device 1': (5, 5, 5, 5, 5), 'Device 2': (1,1,1,1,3), 'Device 3': (4,4, 4, 4, 2), 'Device 4': (3,3,3,3,10)}
data = {
'Device 0':(467, 538, 596, 574, 218),
'Device 1':(472, 408, 459, 559, 210),
'Device 2':(490, 338, 647, 635, 131),
'Device 3':(466, 477, 667, 677, 239),
'Device 4':(573, 293, 713, 713, 253),
'Device 5':(449, 384, 723, 621, 307),
'Device 6':(393, 526, 617, 555, 154),
'Device 7':(524, 434, 554, 595, 351),
'Device 8':(360, 335, 517, 520, 182),
'Device 9':(537, 380, 733, 726, 205),
'Device 10':(322, 438, 702, 726, 129),
'Device 11':(488, 432, 667, 689, 299),
'Device 12':(469, 456, 657, 714, 301),
'Device 13':(480, 318, 645, 721, 158),
'Device 14':(447, 566, 580, 738, 346),
'Device 15':(498, 325, 698, 677, 167),
'Device 16':(504, 505, 695, 545, 272),
'Device 17':(523, 425, 645, 556, 194),
'Device 18':(474, 480, 589, 689, 147),
'Device 19':(608, 493, 611, 690, 249),
'Device 20':(351, 523, 639, 682, 214),
'Device 21':(377, 398, 719, 576, 403),
'Device 22':(376, 572, 554, 751, 230),
'Device 23':(470, 467, 552, 589, 178),
'Device 24':(407, 472, 639, 619, 211),
'Device 25':(433, 289, 437, 675, 248),
'Device 26':(440, 289, 554, 653, 210),
'Device 27':(364, 469, 646, 471, 117),
'Device 28':(488, 334, 633, 540, 230),
'Device 29':(498, 290, 478, 560, 187),
'Device 30':(579, 325, 574, 529, 290),
'Device 31':(582, 453, 558, 533, 162),
'Device 32':(483, 520, 624, 604, 157),
'Device 33':(469, 433, 495, 549, 323),
'Device 34':(388, 264, 458, 681, 340),
'Device 35':(430, 287, 659, 654, 359),
'Device 36':(484, 293, 442, 683, 155),
'Device 37':(333, 385, 691, 685, 247),
'Device 38':(428, 469, 572, 665, 317),
'Device 39':(509, 334, 708, 729, 246),
'Device 40':(527, 380, 596, 583, 398),
'Device 41':(398, 352, 661, 468, 139),
'Device 42':(484, 484, 509, 473, 170),
'Device 43':(389, 244, 562, 688, 188),
'Device 44':(504, 534, 604, 631, 236),
'Device 45':(275, 456, 537, 673, 266),
'Device 46':(431, 274, 462, 506, 235),
'Device 47':(305, 460, 601, 627, 323),
'Device 48':(485, 323, 517, 609, 193),
'Device 49':(503, 360, 612, 594, 371),
'Device 50':(566, 505, 744, 536, 269),
'Device 51':(345, 322, 687, 629, 321),
'Device 52':(381, 272, 496, 670, 128),
'Device 53':(503, 545, 724, 619, 219),
'Device 54':(468, 355, 556, 541, 280),
'Device 55':(375, 357, 655, 706, 219),
'Device 56':(451, 271, 487, 616, 183),
'Device 57':(403, 390, 574, 722, 358),
'Device 58':(348, 299, 725, 686, 218),
'Device 59':(338, 373, 615, 471, 198),
'Device 60':(361, 420, 469, 537, 143),
'Device 61':(381, 479, 689, 549, 317),
'Device 62':(319, 346, 532, 624, 186),
'Device 63':(543, 288, 537, 707, 272),
'Device 64':(533, 453, 744, 555, 317),
'Device 65':(367, 391, 681, 686, 195),
'Device 66':(437, 357, 630, 498, 216),
'Device 67':(468, 348, 495, 646, 316),
'Device 68':(578, 523, 618, 748, 178),
'Device 69':(584, 487, 655, 648, 172),
'Device 70':(535, 476, 589, 504, 212),
'Device 71':(543, 430, 487, 550, 361),
'Device 72':(486, 475, 665, 669, 380),
'Device 73':(508, 436, 515, 684, 323),
'Device 74':(345, 440, 483, 680, 324),
'Device 75':(486, 448, 443, 556, 118),
'Device 76':(459, 453, 541, 572, 247),
'Device 77':(579, 318, 656, 512, 233),
'Device 78':(288, 391, 511, 619, 238),
'Device 79':(377, 408, 625, 692, 274),
'Device 80':(476, 286, 586, 501, 265),
'Device 81':(374, 292, 484, 449, 227),
'Device 82':(368, 494, 581, 557, 343),
'Device 83':(380, 341, 510, 708, 142),
'Device 84':(564, 486, 623, 739, 299),
'Device 85':(458, 461, 661, 611, 351),
'Device 86':(475, 353, 574, 519, 148),
'Device 87':(562, 506, 683, 706, 204),
'Device 88':(506, 430, 623, 641, 247),
'Device 89':(341, 532, 553, 734, 336),
'Device 90':(439, 504, 695, 579, 298),
'Device 91':(283, 272, 676, 550, 107),
'Device 92':(395, 439, 596, 500, 299),
'Device 93':(376, 371, 454, 496, 198),
'Device 94':(287, 349, 557, 572, 152),
'Device 95':(393, 515, 562, 596, 301),
'Device 96':(357, 354, 613, 641, 236),
'Device 97':(425, 347, 624, 711, 215),
'Device 98':(469, 327, 622, 648, 125),
'Device 99':(398, 457, 702, 692, 227)
}
N = tuple(data.keys())
partition = [['Device 0'],['Device 1', 'Device 3'],['Device 2'],['Device 4', 'Device 7'],['Device 6'],['Device 8'],['Device 9', 'Device 5']]

start = time()
ds=DeviceSelection(N, X, data)
C=ds.countDevices()
subsets = [[] for i in range(C)]
for i in range(C):
    dev = ds.nextDevice(i)
    while dev is not None:
        subsets[i].append(dev)
        dev = ds.nextDevice(i)
end=time()-start
print(subsets)

if sorted(subsets) != sorted(partition):
    print('FAIL')
else:
    print('True')
    print(end)
