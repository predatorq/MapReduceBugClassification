from mrjob.job import MRJob, MRStep


class Count(MRJob):
    def mapper1(self, key, line):
        index, title, label, set_type = line.split(',')
        if set_type == 'train':
            title = title.split(' ')
            for word in title:
                yield (word, label), 1  # 某个单词在某个类中出现的次数
                yield ('ALL', label), 1  # 所有单词在某个类中出现的次数之和
            yield (label.upper(), label), 1  # 某个类出现的次数

    def combiner(self, tag, counts):
        yield tag, sum(counts)

    def reducer(self, tag, counts):
        yield tag, sum(counts)

    def mapper2(self, tag, counts):
        word, label = tag
        yield tag, counts
        yield ('WORDCOUNT', label), 1  # 某个类出现的单词个数

    def steps(self):
        return [
            MRStep(mapper=self.mapper1,
                   combiner=self.combiner,
                   reducer=self.reducer),
            MRStep(mapper=self.mapper2,
                   combiner=self.combiner,
                   reducer=self.reducer)
        ]


if __name__ == '__main__':
    Count.run()
