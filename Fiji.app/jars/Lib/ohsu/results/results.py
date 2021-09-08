from ij import IJ, WindowManager
from ij.measure import ResultsTable

class Results:

    def close(self):
        results = WindowManager.getWindow('Results')
        if results is None:
            return
        results.close(False)

    def getResultsArray(self):
        rt = self.getResults()
        if (rt is None):
            return
        data = []
        for i in range(0, rt.size()):
            row = rt.getRowAsString(i)
            if "\t" in row:
                row = row.split("\t")
            else:
                row = row.split(",")
            data.append(row)
        return (list(rt.getHeadings()), data)

    def save(self, path):
        rt = self.getResults()
        rt.saveAs(path)

    def getResults(self):
        return ResultsTable.getResultsTable()