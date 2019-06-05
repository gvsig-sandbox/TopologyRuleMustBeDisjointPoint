from gvsig import uselib

uselib.use_plugin("org.gvsig.topology.app.mainplugin")

import sys


from org.gvsig.topology.lib.spi import AbstractTopologyRule


from gvsig import logger
from gvsig import LOGGER_WARN,LOGGER_INFO,LOGGER_ERROR

from org.gvsig.topology.lib.api import TopologyLocator

from org.gvsig.expressionevaluator import ExpressionEvaluatorLocator

from DeletePoint import DeletePoint


class MustBeDisjointPointRule(AbstractTopologyRule):
  
  geomName = None
  expression = None
  expressionBuilder = None
  
  def __init__(self, plan, factory, tolerance, dataSet1, dataSet2):
    #        TopologyPlan plan,
    #        TopologyRuleFactory factory,
    #        double tolerance,
    #        String dataSet1
    #        String dataSet2
    
    AbstractTopologyRule.__init__(self, plan, factory, tolerance, dataSet1, dataSet2)
    self.addAction(DeletePoint())
  
  def check(self, taskStatus, report, feature1):
    #SimpleTaskStatus taskStatus, 
    #TopologyReport report, 
    #Feature feature1

    try:
      logger("tak", LOGGER_INFO)
      store2 = self.getDataSet2().getFeatureStore()
      tolerance = self.getTolerance()
      #logger("1", LOGGER_INFO)
      
      if (self.expression == None):
        manager = ExpressionEvaluatorLocator.getManager()
        self.expression = manager.createExpression()
        self.expressionBuilder = manager.createExpressionBuilder()
        self.geomName = store2.getDefaultFeatureType().getDefaultGeometryAttributeName()
      
      point = feature1.getDefaultGeometry()
      pointTolerance = point.buffer(tolerance) #polygon
      
      if( point==None ):
        return
      #logger("1", LOGGER_INFO)
      
      theDataSet1 = self.getDataSet1()
      theDataSet2 = self.getDataSet2()
      #logger("2", LOGGER_INFO)
      if theDataSet2.getSpatialIndex() != None:
        #logger("if", LOGGER_INFO)
        for reference in theDataSet2.query(point):
            #FeatureReference reference
            # Misma feature
            #logger("ref"+str(reference), LOGGER_INFO)
            if (reference.equals(feature1.getReference())):
              continue;
            
            feature2 = reference.getFeature()
            otherPoint = feature2.getDefaultGeometry()
            if (otherPoint!=None and not pointTolerance.disjoint(otherPoint)):
              error = pointTolerance.intersection(otherPoint)
              report.addLine(self,
                theDataSet1,
                theDataSet2,
                point,
                error,
                feature1.getReference(),
                feature2.getReference(),
                False,
                "The point is not disjoint."
              )
              break
            
      else:
        logger("else", LOGGER_INFO)
        self.expression.setPhrase(
          self.expressionBuilder.ifnull(
            self.expressionBuilder.column(self.geomName),
            self.expressionBuilder.constant(False),
            self.expressionBuilder.ST_Overlaps(
              self.expressionBuilder.column(self.geomName),
              self.expressionBuilder.geometry(point)
            )
          ).toString()
        )
        feature = theDataSet2.findFirst(self.expression)
        if feature != None:
            otherPoint = feature.getDefaultGeometry()
            error = None
            if otherPoint!=None :
              error = point.difference(otherPoint)
            
            report.addLine(self,
              theDataSet1,
              theDataSet2,
              point,
              error,
              feature1.getReference(),
              feature2.getReference(),
              False,
              "The point is not disjoint."
            )
        logger("end", LOGGER_INFO)
    except: # Exception as ex:
      #logger("2 Can't check feature."+str(ex), LOGGER_WARN)
      ex = sys.exc_info()[1]
      logger("Can't execute rule. Class Name:" + ex.__class__.__name__ + " Except:" + str(ex))
    finally:
      pass
def main(*args):
  # testing class m = MustBeDisjointPointRule(None, None, 3, None)
  print "* Executing MustBeDisjointPoint RULE main."
  tm = TopologyLocator.getTopologyManager()
  
  from mustBeDisjointPointRuleFactory import MustBeDisjointPointRuleFactory
  a = MustBeDisjointPointRuleFactory()
  tm.addRuleFactories(a)
