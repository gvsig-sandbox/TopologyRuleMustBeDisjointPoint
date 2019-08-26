from gvsig import uselib

uselib.use_plugin("org.gvsig.topology.app.mainplugin")

import sys

from org.gvsig.topology.lib.spi import AbstractTopologyRule

from gvsig import logger
from gvsig import LOGGER_WARN,LOGGER_INFO,LOGGER_ERROR

from org.gvsig.topology.lib.api import TopologyLocator

from org.gvsig.expressionevaluator import ExpressionEvaluatorLocator

from DeletePointAction import DeletePointAction


class MustBeDisjointPointRule(AbstractTopologyRule):
  
  geomName = None
  expression = None
  expressionBuilder = None
  
  def __init__(self, plan, factory, tolerance, dataSet1):
    #        TopologyPlan plan,
    #        TopologyRuleFactory factory,
    #        double tolerance,
    #        String dataSet1
    
    AbstractTopologyRule.__init__(self, plan, factory, tolerance, dataSet1)
    self.addAction(DeletePointAction())
  
  def check(self, taskStatus, report, feature1):
    #SimpleTaskStatus taskStatus, 
    #TopologyReport report, 
    #Feature feature1

    try:

      if (self.expression == None):
        manager = ExpressionEvaluatorLocator.getManager()
        self.expression = manager.createExpression()
        self.expressionBuilder = manager.createExpressionBuilder()
        self.geomName = feature1.getType().getDefaultGeometryAttributeName()

      point = feature1.getDefaultGeometry()
      tolerance = self.getTolerance()
      pointTolerance = point.buffer(tolerance)

      if point==None:
        return

      if pointTolerance==None:
        pointTolerance = point

      theDataSet = self.getDataSet1()
      if theDataSet.getSpatialIndex() != None:
        for reference in theDataSet.query(pointTolerance):
            #FeatureReference reference
            # Same feature
            if reference.equals(feature1.getReference()):
              continue;
            
            feature = reference.getFeature()
            otherPoint = feature.getDefaultGeometry()
            if otherPoint!=None and not pointTolerance.disjoint(otherPoint):
              error = point
              report.addLine(self,
                theDataSet,
                None,
                point,
                error,
                feature1.getReference(),
                None,
                -1,
                -1,
                False,
                "The point is not disjoint.",
                ""
              )
              break
            
      else:
        logger("else", LOGGER_INFO)
        self.expression.setPhrase(self.expressionBuilder.ifnull(
            self.expressionBuilder.column(self.geomName),
            self.expressionBuilder.constant(False),
            self.expressionBuilder.ST_Disjoint(
              self.expressionBuilder.column(self.geomName),
              self.expressionBuilder.geometry(pointTolerance)
            )
          ).toString()
        )

        feature = theDataSet.findFirst(self.expression)
        if feature != None:
            otherPoint = feature.getDefaultGeometry()
            error = None
            if otherPoint != None:
              error = point
              
            report.addLine(self,
              theDataSet,
              None,
              point,
              error,
              feature1.getReference(),
              None,
              -1,
              -1,
              False,
              "The point is not disjoint."
              ""
            )
    except:
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
