from ij import WindowManager
from ij.measure import ResultsTable

class Results:

    def __init__(self, table = None):
        self.table = table

    def close(self):
        results = WindowManager.getWindow('Results')
        if results is None:
            return
        results.close(False)

    '''
    Get the headers & rows from this ResultsTable

    return tuple([headers], [[roi measurements]])
    '''
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
        return (['ROI'] + list(rt.getHeadings()), data)

    def save(self, path):
        rt = self.getResults()
        rt.saveAs(path)

    def getResults(self):
        if self.table is None:
            return ResultsTable.getResultsTable()
        return self.table