# encoding: utf-8

import gvsig
from org.gvsig.topology.lib.spi import AbstractTopologyRuleAction

#from addons.TopologyRuleMustNotOverlapPolygon.mustNotOverlapPolygonFactory import MustNotOverlapPolygonRuleFactory
#from mustNotOverlapPolygonFactory import MustNotOverlapPolygonRuleFactory
from org.gvsig.topology.lib.api import ExecuteTopologyRuleActionException

#from mustBeDisjointPointRuleFactory import MustBeDisjointPointRuleFactory

class DeletePoint(AbstractTopologyRuleAction):

  def __init__(self):
    AbstractTopologyRuleAction.__init__(
      self,
      "MustBeDisjointPoint", #MustBeDisjointPointRuleFactory.NAME,
      "DeletePoint",
      "Delete Point",
      ""#CAMBIAR
    )
  def execute(rule, line, parameters):
    #TopologyRule rule, TopologyReportLine line, DynObject parameters) {
    try:
      #DOING
      
      pass
    except Exception as ex:
      #throw new ExecuteTopologyRuleActionException(ex);
      raise ExecuteTopologyRuleActionException(ex)

def main(*args):

    c = DeletePoint()
    pass
