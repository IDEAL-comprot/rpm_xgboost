#coding:utf-8
class FeatureParser():#����һ����FeatureParser
    def __init__(self, data): #����һ���ṹ�壬���������data���ṹ������ĸ���Ա sections updataParams parseCount updateZerocount
        self.sections = self.getSplitResult(data) 
        self.updateParams()
        self.parseCount(data)
        self.updateZeroCount()

    @staticmethod
    def getSplitResult(data):
        sections = {}
        for i in range(28):
            lst = []
            cur = []
            for j in range(28):
                if int(data[i*28 + j]) == 0:
                    if len(cur) > 0:
                        lst.append(cur)
                        cur = []
                    continue
                if len(cur) == 0:
                    cur = [j, j]
                else:
                    cur[1] = j
            if len(cur) > 0:
                lst.append(cur)
            if len(lst) > 0:
                sections[i] = lst
        return sections


    def updateParams(self):
        self.up = min(self.sections.keys())
        self.down = max(self.sections.keys())
        self.left = min([item[0][0] for item in self.sections.values()])
        self.right = max([item[-1][1] for item in self.sections.values()])
        self.x_mid = (self.right+self.left)/2
        self.y_mid = (self.down+self.up)/2

        self.ones = sum([1 for item in self.sections.values() if len(item) == 1])
        self.twos = sum([1 for item in self.sections.values() if len(item) == 2])
        self.threes = sum([1 for item in self.sections.values() if len(item) >= 3])

        #����ֻ��һ�ε����֣������ֳ��������ֵ���߻����ұ� 3ʱ���῿��5ʱһ��һ�ҵȡ�
        self.one_left_up, self.one_left_down, self.one_mid, self.one_right_up, self.one_right_down = 0, 0, 0, 0, 0
        for i, item in self.sections.items():
            if len(item) != 1: continue
            if item[0][1] <= self.x_mid:
                if i < self.y_mid :
                    self.one_left_up += 1
                else:
                    self.one_left_down += 1
            elif item[0][0] >= self.x_mid:
                if i < self.y_mid:
                    self.one_right_up += 1
                else:
                    self.one_right_down += 1
            else:
                self.one_mid += 1
        # print(" ones: ", self.one_left_up, self.one_left_down, self.one_mid, self.one_right_up, self.one_right_down, self.ones)
        section_all = []
        for item in self.sections.values():
            for slice in item:
                section_all.append(slice[1] - slice[0] + 1)
        self.max_width = max(section_all)
        self.avg_width = sum(section_all)/len(section_all)

    def parseCount(self, data):
        #�����ֳַ�4������ͳ��ÿ������ĵ�ĸ���
        self.left_top, self.right_top, self.left_down, self.right_down = 0, 0, 0, 0
        for i in range(28):
            for j in range(28):
                if int(data[i*28 + j]) == 0: continue
                if j < self.x_mid and i < self.y_mid : self.left_top += 1
                if j > self.x_mid and i < self.y_mid:  self.right_top += 1
                if j < self.x_mid and i > self.y_mid:  self.left_down += 1
                if j > self.x_mid and i > self.y_mid:  self.right_down += 1

    def updateZeroCount(self):
        self. zero_count = 0
        last_i, last_item, start_ones = 0, None, False
        for i, item in self.sections.items():

            if last_item is None:
                last_i, last_item = i, item
                continue

            if len(last_item) == 1 and len(item) > 1:
                start_ones = (item[0][1] +1 >= last_item[0][0] and item[-1][0]-1 <= last_item[0][1])

            if start_ones and len(last_item) > 1 and len(item) == 1:
                if item[0][0] - 1 <= last_item[0][1] and item[0][1]+1 >= last_item[-1][0]:
                    self. zero_count += 1
                start_ones = False
            last_i, last_item = i, item


    def getFeature(self):
        all_count = sum((self.left_top, self.right_top, self.left_down, self.right_down))
        height = sum((self.ones, self.twos, self.threes))
        return ((self.right - self.left+1)/(self.down - self.up + 1), #�����
                self.left_top/all_count,    #���ϵ��
                self.right_top/all_count,   #���ϵ��
                self.left_down/all_count,   #���µ��
                self.right_down/all_count,  #���µ��
                self.ones/height,   #һ��ռ��
                (self.twos + self.threes)/height,   #����һ��ռ��
                self.one_left_up/self.ones,
                self.one_left_down/self.ones,
                self.one_mid/self.ones,
                self.one_right_up/self.ones,
                self.one_right_down/self.ones,
                self.max_width/self.avg_width,
                self.zero_count
            )


line_number = 0
with open("train.txt", "w") as wFile: #���ļ�train.txt������Ϊ��д�ļ��������ھ��½�
    with open("train.csv", "r") as mFile: #��train.csv �ļ�������Ϊֻ��
        for line in mFile: #����train.csv��line=train.csv��һ�У�forѭ����ȡtrain.csv�������в���ÿһ�и�ֵ��line��line���ַ�������
            line_number += 1
            if line_number <= 1:continue #���line_number<1 �����
            # if line_number > 20: break
            lst = line.split(',') #list��һ���б��洢line���水,���ѿ��������ݡ�������line="'1','2','3','4'"����lst=[1,2,3,4]
            # print(",".join(["%.3f" % item for item in FeatureParser(lst[1:]).getFeature()] + [str(lst[0])]) + "\n")
            wFile.write(",".join(["%.3f" % item for item in FeatureParser(lst[1:]).getFeature()] + [str(lst[0])]) + "\n")
            #�ȿ����õ��Ӻ���FeatureParser().getFeature()���������Ϊlst�б��У���һ�е����һ�С�����lst=[1,2,3,4]�������Ӻ�����#��#Ϊ[2,3,4]��������getFeature()����
            #
            #
            #
