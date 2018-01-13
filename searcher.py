#!/usr/bin/python
# -*- coding:utf-8 -*-
import numpy as np
import csv


class Searcher:
    def __init__(self, indexPath):
        # store index path
        self.indexPath = indexPath

    def search(self, queryFeatures, limit=9):
        # initialize the dictionary of results
        results = {}
        #open the index file for reading
        with open(self.indexPath) as f:
            #initialize the CSV reader
            reader = csv.reader(f)

            #loop over the rows in the index
            for row in reader:
                #parse out the image ID and features, then compute the
                #chi-squared distance between the features in the index
                #and the query features
                i = 0
                while (True):
                    try:
                        float(row[i])
                    except:
                        i += 1
                    else:
                        break
                features = [float(x) for x in row[i:]]
                d = self.chi2_distance(features, queryFeatures)
                results[row[0]] = d


            #close the reader
            f.close()
        #sort result , so that the smaller distance are at the front of the list
        results = sorted([(v, k) for (k, v) in results.items()])
        results = results[:limit]
        finresults=[]
        for i in results:
            if(i[0]<10):
                finresults.append(i)

        #return the results
        return  finresults

    def chi2_distance(self, histA, histB, eps = 1e-10):
        #compute the chi-squared distance
        d = 0.5 * np.sum([((a - b) ** 2) / (a + b + eps) for (a, b) in zip(histA, histB)])

        #return the chi—squared distance
        return d



