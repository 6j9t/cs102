import csv
import os
from collections import defaultdict
from operator import itemgetter
from itertools import groupby
from tabulate import tabulate


class DataFrame:

    def __init__(self, headers, rows):
        self._headers = headers
        self._rows = rows

    @property
    def headers(self):
        return self._headers

    @headers.setter
    def headers(self, new_headers):
        assert len(self._headers) == len(new_headers)
        self._headers = new_headers

    @property
    def rows(self):
        return self._rows

    def group_by(self, by):
        groups = []
        groupkeys = []
        for i in range(len(self.headers)):
            if self.headers[i] == by:
                index = i
                break
        for s in self.rows:
            word = s[index]
            word = word.strip(' ')
            if groups.count(word) == 0:
                groups.append(word)
                groupkeys.append(s)
            else:
                groupkeys.append(s)
        d = dict.fromkeys(groups)
        return GrouppedDataFrame(by, self.headers, groups, groupkeys)

    def merge(self, df, by):
        pass

    def __getitem__(self, name):
        pass

    def __setitem__(self, name):
        pass

    def __str__(self):
        return tabulate(self.rows, headers=self.headers)

    @staticmethod
    def from_file(path):
        file1 = open(path, "r", encoding="utf-8-sig")
        i = 0
        list = []
        cr = csv.reader(file1)
        for line in cr:
            if i == 0:
                headers = line
                i += 1
            else:
                line[-1] = line[-1].strip(' ')
                line[-1] = line[-1].strip('\n')
                line[-1] = line[-1].strip('\r')
                list.append(line)
        file1.close()
        return DataFrame(headers, list)

    def to_csv(self, path):
        file1 = open(path, "w", encoding="utf-8-sig", newline='')
        cw = csv.writer(file1)
        cw.writerow(self.headers)
        cw.writerows(self.rows)
        file1.close()


class GrouppedDataFrame:

    def __init__(self, by, headers, groups, groupkeys):
        self._by = by
        self._headers = headers
        self._groups = groups
        self._groupkeys = groupkeys

    def sum_by(self, by):
        list = []
        for i in range(len(self._headers)):
            if self._headers[i] == by:
                indexby = i
                break
        a = self._groupkeys[0]
        for i in range(len(self._groupkeys[0])):
            if self._groupkeys[0][i] == self._groups[0]:
                indexequal = i
                break
        j = 0
        sum = 0
        for i in self._groupkeys:
            if i[indexequal].strip(' ') == self._groups[j]:
                sum += int(i[indexby])
            else:
                list.append([self._groups[j], sum])
                j += 1
                sum = 0
                sum += int(i[indexby])
        headers = []
        headers.append(self._headers[indexequal])
        headers.append(self._headers[indexby])
        return DataFrame(headers, list)


BASE_PATH = 'C:\\Users\\MSI NB\\Downloads'
PATH = os.path.join(BASE_PATH, 'spb_cameras.csv')
POPULATION_PATH = os.path.join(BASE_PATH, 'spb_population_per_district.csv')
CAMERAS_PATH = os.path.join(BASE_PATH, 'cameras_per_district.csv')

# ===================================================
df = DataFrame.from_file(PATH)
amount_df = df.group_by('district').sum_by('amount')
amount_df.headers = ['Район', 'Число Камер']
amount_df.to_csv('cameras_per_district.csv')
print(amount_df)
# Район                Число Камер
# -----------------  -------------
# Адмиралтейский               396
# Василеостровский             588
# Выборгский                  3299
# Калининский                 3369
# Кировский                    732
# ...


# ===================================================
# amount_df = DataFrame.from_file(CAMERAS_PATH)
# pop_df = DataFrame.from_file(POPULATION_PATH)
# full_df = amount_df.merge(pop_df, by='Район')
# print(full_df)
# Район                Число Камер    Население    Площадь
# -----------------  -------------  -----------  ---------
# Калининский                 3369       538258      40.18
# Выборгский                  3299       509592     115.52
# Фрунзенский                 2787       401410      37.52
# Красногвардейский           2379       357906      56.35
# ...

# full_df['Плотность'] = #1
# full_df.to_csv('exam_done.csv')
# print(full_df)
# Район                Число Камер    Население    Площадь    Плотность
# -----------------  -------------  -----------  ---------  -----------
# Калининский                 3369       538258      40.18      13396.2
# Выборгский                  3299       509592     115.52      4411.29
# ...
