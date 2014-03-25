import os

from utils_standard import contexts_to_standard
from statistical_report import StatisticalReport

#
# FILE write for analysis and report
#
def report_generate(obj, timestamp, iteration):
    report = StatisticalReport(obj, timestamp, iteration)
    hostname = "host%d" % obj.id
    base_directory = obj.configuration("test_directory")
    filepath = base_directory + os.sep + "%s" % hostname + os.sep + "%04d" % timestamp + os.sep + "%04d.txt" % iteration
    dir_name = os.path.dirname(filepath)
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

    with open(filepath,"w") as f:
        f.write("## INPUT\n")
        f.write(str(obj.input.to_string()) + "\n")
        f.write("## DB\n")
        f.write(obj.context_database.to_string(timestamp) + "\n")
        f.write("## ASSORTED CONTEXTS\n")
        f.write(obj.assorted_context_database.to_string(timestamp) + "\n")
        f.write("## FILTERED SINGLES\n")
        r = contexts_to_standard(obj.filtered_singles)
        f.write("%s\n" % r[0])
        f.write("## NEW AGGREGATES\n")
        aggr_string = "*" if obj.new_aggregate is None else obj.new_aggregate
        f.write("%s\n" % aggr_string)
        f.write("## CONTEXT HISTORY\n")
        f.write(str(obj.context_history.get(timestamp)) + "\n")
        f.write("## OUTPUT\n")
        f.write(str(obj.output.to_string()))

        f.write("\n\n-------------------\n")
        f.write("## STATISTICS\n")
        f.write("%s" % report.run())
