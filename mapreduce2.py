from mrjob.job import MRJob
import pandas as pd
import csv
import math

from mrjob.step import MRStep

dictionary = []
all_label = ['content', 'invalid', 'other', 'action', 'engineering']
pc_sum = 0


class Classification(MRJob):
    def mapper1(self, key, line):
        index, title, true_label, set_type = line.split(',')
        if set_type == 'test':
            title = title.split(' ')
            pxc_count = 0
            for id in range(len(dictionary)):
                if dictionary[id][0] == 'WORDCOUNT':
                    pxc_count = pxc_count + int(dictionary[id][2])
            for guess_label in all_label:
                pc, pxc_all, pxc1 = 0, 0, 0
                for id in range(len(dictionary)):
                    if dictionary[id][0] == guess_label.upper():
                        pc = int(dictionary[id][2]) / pc_sum
                        break
                for id in range(len(dictionary)):
                    if dictionary[id][0] == 'ALL' and dictionary[id][1] == guess_label:
                        pxc_all = int(dictionary[id][2])
                        break
                pcx = math.log(pc)
                for word in title:
                    for id in range(len(dictionary)):
                        if dictionary[id][0] == word and dictionary[id][1] == guess_label:
                            pxc1 = int(dictionary[id][2])
                            break
                    pcx = pcx + math.log((pxc1 + 1) / (pxc_all + pxc_count))
                yield (index, true_label), (pcx, guess_label)

    def combiner1(self, tag, counts):
        yield tag, max(counts)

    def reducer1(self, tag, counts):
        yield tag, max(counts)

    def mapper2(self, tag, counts):
        index, true_label = tag
        _, guess_label = counts
        if true_label == guess_label:
            yield (true_label, 'correct'), 1
        yield (true_label, 'all'), 1

    def combiner2(self, tag, counts):
        yield tag, sum(counts)

    def reducer2(self, tag, counts):
        yield tag, sum(counts)

    def steps(self):
        return [
            MRStep(mapper=self.mapper1,
                   combiner=self.combiner1,
                   reducer=self.reducer1),
            MRStep(mapper=self.mapper2,
                   combiner=self.combiner2,
                   reducer=self.reducer2)
        ]


if __name__ == '__main__':
    # open the CSV file in read mode
    with open('result.csv', 'r', encoding="utf-16le") as file:
        # create a CSV reader object
        reader = csv.reader(file, delimiter='\t')
        # iterate over the rows of the file
        for row in reader:
            # row[0] contains the list, row[1] contains the number
            data_list_string = row[0]
            data_number = row[1]
            # remove the square brackets and quotes from the list string
            data_list = data_list_string.strip('[]').replace('"', '').replace(' ', '').replace('[', '').replace(
                '\ufeff', '').split(',')
            # assign the variables
            var_1 = data_list[0]
            var_2 = data_list[1]
            var_3 = data_number
            temp = [var_1, var_2, var_3]
            dictionary.append(temp)

    for i in range(len(dictionary)):
        if dictionary[i][1].upper() == dictionary[i][0]:
            pc_sum = pc_sum + int(dictionary[i][2])

    Classification.run()

