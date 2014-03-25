import os

class StatisticalReport(object):
    def __init__(self, report_object, timestamp, iteration):
        self.obj = report_object
        self.timestamp = timestamp
        self.iteration = iteration

    def run(self):
        result = ""

        # 1. get the number of received packets
        s,a = self.obj.input.get_number_of_contexts()
        result += "Received: %d (%d-%d)\n" % (s+a, s, a)

        # 2. get the number of sent packets
        s,a = self.obj.output.get_number_of_contexts()
        result += "Sent: %d (%d-%d)\n\n" % (s+a, s, a)

        # 3. calculate the accuracy
        sample = self.obj.get_sample()
        if sample is not None:
            result += "Correct values: %s\n" % sample.get_values(self.timestamp)
            result += "Correct average: %4.2f\n" % sample.get_average(self.timestamp)
        else:
            result += "No sample data found\n"

        return result

