# encoding: utf-8

import gvsig
from org.gvsig.topology.lib.spi import AbstractTopologyRuleAction
import sys

from gvsig import logger
from gvsig import LOGGER_WARN,LOGGER_INFO,LOGGER_ERROR

#from addons.TopologyRuleMustNotOverlapPolygon.mustNotOverlapPolygonFactory import MustNotOverlapPolygonRuleFactory
#from mustNotOverlapPolygonFactory import MustNotOverlapPolygonRuleFactory
from org.gvsig.topology.lib.api import ExecuteTopologyRuleActionException

#from mustBeDisjointPointRuleFactory import MustBeDisjointPointRuleFactory

class DeletePointAction(AbstractTopologyRuleAction):

  def __init__(self):
    AbstractTopologyRuleAction.__init__(
      self,
      "MustBeDisjointPoint", #MustBeDisjointPointRuleFactory.NAME,
      "DeletePointAction",
      "Delete Point Action",
      ""#CAMBIAR
    )
  
  logger("1", LOGGER_INFO)
  def execute(self, rule, line, parameters):
    #TopologyRule rule, TopologyReportLine line, DynObject parameters
    try:
    
      #logger("2", LOGGER_INFO)
      dataSet = rule.getDataSet1()
      dataSet.delete(line.getFeature1())
      
    except:
      ex = sys.exc_info()[1]
      print "Error", ex.__class__.__name__, str(ex)
      #throw new ExecuteTopologyRuleActionException(ex);
      #raise ExecuteTopologyRuleActionException(ex)

def main(*args):

    c = DeletePointAction()
    pass
